import math
import pygame as pg

from Painter import TransformMatrix as tmat
from GameOverScene import GameOverScene
from GameObject import GameObject
from enemy.Enemy import Enemy
from Point import Point
import Shape as sh
import Colors

TRIPLE_SPREAD = math.pi/30
FULL_COUNT = 10
BULLET_SPEED = 15

PLAYER_GUNS = ["light", "triple", "heavy", "full"]


class Player(sh.ShapeObject):
    def __init__(self, scene, x, y):
        super().__init__(scene)
        self.position = Point(x, y)
        self.set_shape(sh.PLAYER_SHAPE, Colors.player, True, 5)
        self.gun = 0
        self.score = 0
        self.lives = 5
        self._prev_score = 0
        self._shoot_timer = 0

    def update(self):
        diff = self.scene.mouse_position() - self.position
        self.direction = math.atan2(diff.y, diff.x)

        if self.key_down(pg.K_a):
            self.position += Point(-5, 0)

        if self.key_down(pg.K_d):
            self.position += Point(5, 0)

        if self.key_down(pg.K_w):
            self.position += Point(0, -5)

        if self.key_down(pg.K_s):
            self.position += Point(0, 5)

        super().update()

        if self.button_up(0):
            self._shoot_timer -= 1
            if self._shoot_timer <= 0:
                self.shoot()

        self.try_change_gun()
        self.try_gain_lives()
        self._prev_score = self.score

    def draw(self):
        super().draw()

        def write(row, title, content):
            text = title + ": " + str(content)
            self.painter.text((5, 5 + row*20), text, Colors.white)            

        write(0, "Score", self.score)
        write(1, "Lives", "<3 "*self.lives)

        write(3, "Gun", PLAYER_GUNS[self.gun])
        write(4, "Difficulty", self.scene.spawner.level + 1)

    def collide_with(self, other):
        if isinstance(other, Enemy):
            print("---- DEATH (lives: %s) ----" % self.lives)

            self.lives -= 1
            if self.lives == 0:
                scene_man = self.scene.manager
                scene_man.begin(GameOverScene)
                scene_man.scene.set_score(self.score)

            to_destroy = []
            for obj in self.scene.objects:
                if isinstance(obj, (Enemy,Bullet)):
                    to_destroy.append(obj)

            for obj in to_destroy:
                obj.destroy()

            self.scene.particle_system.explode(self.position, Colors.white, 10)
            self.position.coords = self.scene.size
            self.position /= 2
            self.scene.spawner.timer = 60*3

    def try_gain_lives(self):
        if (self._prev_score % 10000 != 0 and
            self.score % 10000 == 0):
            self.lives += 1

    def try_change_gun(self):
        step = [500, 1500, 5000][self.scene.spawner.level]
        if (self._prev_score % step != 0 and
            self.score % step == 0):
            self.gun = (self.gun + 1) % 4

    def shoot(self):
        def boom(direction):
            self.add_object(Bullet(self.scene, self.x, self.y, direction))

        # light
        if self.gun == 0:
            boom(self.direction)
            self._shoot_timer = 10
        # triple
        elif self.gun == 1:
            boom(self.direction - TRIPLE_SPREAD)
            boom(self.direction                )
            boom(self.direction + TRIPLE_SPREAD)
            self._shoot_timer = 18
        # heavy
        elif self.gun == 2:
            boom(self.direction - TRIPLE_SPREAD*1.0)
            boom(self.direction - TRIPLE_SPREAD*0.5)
            boom(self.direction                    )
            boom(self.direction + TRIPLE_SPREAD*0.5)
            boom(self.direction + TRIPLE_SPREAD*1.0)
            self._shoot_timer = 28
        # full
        elif self.gun == 3:
            for i in range(FULL_COUNT):
                boom(self.direction + i/FULL_COUNT*math.pi*2)
            self._shoot_timer = 60
        # fast single shot fallback
        else:
            boom(self.direction)
            self._shoot_timer = 1


class Bullet(sh.ShapeObject):
    def __init__(self, scene, x, y, direction):
        super().__init__(scene)
        self.position = Point(x, y)
        self.set_shape(sh.BULLET_SHAPE, Colors.bullet, True, 5)
        self.direction = direction
        self._velocity = Point.anglelen(direction, BULLET_SPEED)
        self._clamp_inside = False

    def update(self):
        if self.is_outside:
            w = self._scene.size
            d = 0
            if self.x > w[0]:
                d = math.pi
            elif self.y < 0:
                d = math.pi/2
            elif self.y > w[1]:
                d = math.pi*3/2

            self.scene.particle_system.burst(self.position, d, Colors.bullet, 1)

            self.destroy()
            return

        self.position += self._velocity
        super().update()

    @property
    def velocity(self):
        return self._velocity

    def collide_with(self, other):
        if isinstance(other, Enemy):
            self.scene.particle_system.explode(self.position, Colors.bullet, 1)
            self.scene.player.score += 100
            self.destroy()
