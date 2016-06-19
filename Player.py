import math
import pygame as pg

from Painter import TransformMatrix as tmat
from GameObject import GameObject
from Enemy import Enemy
from Point import Point
import Shape as sh
import Colors

TRIPLE_SPREAD = math.pi/30
FULL_COUNT = 10

class Player(sh.ShapeObject):
	def __init__(self, scene, x, y):
		super().__init__(scene)
		self.position = Point(x, y)
		self.set_shape(sh.PLAYER_SHAPE, Colors.player, True, 5)
		self.gun = "light"
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

		if self.button_up(0):
			self._shoot_timer -= 1
			if self._shoot_timer <= 0:
				self.shoot()

	def shoot(self):
		def shot(direction):
			self.add_object(Bullet(self.scene, self.x, self.y, direction))

		if self.gun == "light":
			shot(self.direction)
			self._shoot_timer = 8
		elif self.gun == "triple":
			shot(self.direction - TRIPLE_SPREAD)
			shot(self.direction                )
			shot(self.direction + TRIPLE_SPREAD)
			self._shoot_timer = 13
		elif self.gun == "heavy":
			shot(self.direction - TRIPLE_SPREAD*1.0)
			shot(self.direction - TRIPLE_SPREAD*0.5)
			shot(self.direction                    )
			shot(self.direction + TRIPLE_SPREAD*0.5)
			shot(self.direction + TRIPLE_SPREAD*1.0)
			self._shoot_timer = 17
		elif self.gun == "full":
			for i in range(FULL_COUNT):
				shot(self.direction + i/FULL_COUNT*math.pi*2)
			self._shoot_timer = 60
		else:
			shot(self.direction)
			self._shoot_timer = 1


BULLET_SPEED = 15
class Bullet(sh.ShapeObject):
	def __init__(self, scene, x, y, direction):
		super().__init__(scene)
		self.position = Point(x, y)
		self.set_shape(sh.BULLET_SHAPE, Colors.bullet, True, 5)
		self.direction = direction
		self._velocity = Point.anglelen(direction, BULLET_SPEED)

	def update(self):
		if self.is_outside:
			w = self.scene_manager.window_size()
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

	@property
	def velocity(self):
		return self._velocity

	def collide_with(self, other):
		if isinstance(other, Enemy):
			self.destroy()
