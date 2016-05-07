import math
import random

from GameObject import GameObject
import Shape as sh
from Point import Point
import Player as pl
import Colors

class Enemy(sh.ShapeObject):
	def __init__(self, scene, x, y):
		super().__init__(scene)
		self.position = Point(x, y)

	def collide_with(self, other):
		if isinstance(other, pl.Bullet):
			self.scene.particle_system.explode(self.position, self.color, 3)
			self.destroy()
		elif isinstance(other, pl.Player):
			self.destroy()

DUMB_SPEED = 3
DUMB_ACCELERATION = 0.5
class Dumb(Enemy):
	def __init__(self, scene, x, y):
		super().__init__(scene, x, y)
		angl = random.uniform(0, math.pi*2)
		self._velocity = Point.anglelen(angl, DUMB_SPEED)
		self.set_shape(sh.PINWHEEL_SHAPE, Colors.dumb, True, 5)

	def update(self):
		angl = random.uniform(0, math.pi*2)
		self._velocity += Point.anglelen(angl, DUMB_ACCELERATION)
