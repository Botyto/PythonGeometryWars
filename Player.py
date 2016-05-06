import math
import pygame as pg

from Painter import TransformMatrix as tmat
from GameObject import GameObject
from Point import Point
import Shape as sh
import Colors

class Player(sh.ShapeObject):
	def __init__(self, scene, x, y):
		super().__init__(scene)
		self.position = Point(x, y)
		self.set_shape(sh.PLAYER_SHAPE, Colors.player, True, 5)
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
			if self._shoot_timer >= 10:
				self._shoot_timer = 0
				self.add_object(Bullet(self.scene, self.x, self.y, self.direction))
			else:
				self._shoot_timer += 1

class Bullet(sh.ShapeObject):
	def __init__(self, scene, x, y, direction):
		super().__init__(scene)
		self.position = Point(x, y)
		self.set_shape(sh.BULLET_SHAPE, Colors.bullet, True, 5)
		self.direction = direction
		self._velocity = Point.anglelen(direction, 15)

	def update(self):
		if self.is_outside:
			self.destroy()
			return

		self.position += self._velocity
