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


DUMB_SPEED = 2
DUMB_ACCELERATION = 0.1
DUMB_ANGULAR_SPEED = math.pi/70
class Dumb(Enemy):
	def __init__(self, scene, x, y):
		super().__init__(scene, x, y)
		angl = random.uniform(0, math.pi*2)
		self._velocity = Point.anglelen(angl, DUMB_SPEED)
		self.set_shape(sh.PINWHEEL_SHAPE, Colors.dumb, True, 5)


	def update(self):
		super().update()
		angl = random.uniform(0, math.pi*2)
		self._velocity += Point.anglelen(angl, DUMB_ACCELERATION)
		self._velocity *= DUMB_SPEED / self._velocity.length()
		self.position += self._velocity
		self.direction += DUMB_ANGULAR_SPEED

		w = self.scene_manager.window_size()
		if self.position.x < 0 or self.position.x > w[0]:
			self._velocity.x *= -1
		if self.position.y < 0 or self.position.y > w[1]:
			self._velocity.y *= -1


FOLLOWER_SPEED = 2
class Follower(Enemy):
	def __init__(self, scene, x, y):
		super().__init__(scene, x, y)
		angl = random.uniform(0, math.pi*2)
		self.set_shape(sh.HOURGLASS_SHAPE, Colors.follow, True, 5)

	def update(self):
		super().update()
		dirvec = self._scene.player.position - self.position
		self.position += dirvec * FOLLOWER_SPEED / dirvec.length()
		self.direction = math.atan2(dirvec.y, dirvec.x)
