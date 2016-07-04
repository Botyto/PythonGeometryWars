import math

from enemy.Enemy import Enemy
from Point import Point
import Player as pl
import Shape as sh
import Colors

SPEED = 3
SPEED_SQR = SPEED*SPEED
DISTANCE = 100
DISTANCE_SQR = DISTANCE*DISTANCE
ACCELERATION = 0.5
DODGE = 2
ANGULAR_SPEED = math.pi/70


class Avoider(Enemy):
    def __init__(self, scene, x, y):
        super().__init__(scene, x, y)
        self._velocity = Point(0, 0)
        self.set_shape(sh.STAR_SHAPE, Colors.avoid, True, 5)

    def update(self):
        player = self._scene.player
        vec_to_player = player.position - self.position
        dir_to_player = math.atan2(vec_to_player.y, vec_to_player.x)

        angle = self._angle_distance(player.direction, dir_to_player)
        if angle < math.pi/2:
            dirvec = vec_to_player
            speed = ACCELERATION
        else:
            avoid_point = Point(1, 1)
            avoid_count = 0

            for obj in self.scene.objects:
                if isinstance(obj, pl.Bullet):
                    distance = (obj.position - self.position).length_sqr()
                    if distance <= DISTANCE_SQR:
                        avoid_point += obj.position
                        avoid_count += 1

            if avoid_count > 0:
                avoid_point /= avoid_count
                dirvec = self.position - avoid_point
                speed = DODGE
            else:
                dirvec = vec_to_player
                speed = ACCELERATION

        self._velocity += dirvec * speed / dirvec.length()

        if self._velocity.length_sqr() > SPEED_SQR:
            self._velocity.normalize()
            self._velocity *= SPEED

        self.position += self._velocity
        self.direction += ANGULAR_SPEED
        super().update()

    def _angle_distance(self, alpha, beta):
        phi = abs(beta - alpha) % 360
        distance = 360 - phi if phi > 180 else phi
        return distance
