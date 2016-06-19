import sys
import math
import random

import Colors
import Shape as sh
import Player as pl
from Point import Point
from GameObject import GameObject

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
		self.set_shape(sh.HOURGLASS_SHAPE, Colors.follow, True, 5)

	def update(self):
		super().update()
		dirvec = self._scene.player.position - self.position
		self.position += dirvec * FOLLOWER_SPEED / dirvec.length()
		self.direction = math.atan2(dirvec.y, dirvec.x)


AVOID_SPEED = 3
AVOID_SPEED_SQR = AVOID_SPEED*AVOID_SPEED
AVOID_DISTANCE = 100
AVOID_DISTANCE_SQR = AVOID_DISTANCE*AVOID_DISTANCE
AVOID_ACCELERATION = 0.5
AVOID_DODGE = 2
class Avoider(Enemy):
	def __init__(self, scene, x, y):
		super().__init__(scene, x, y)
		self._velocity = Point(0, 0)
		self.set_shape(sh.STAR_SHAPE, Colors.avoid, True, 5)

	def _angle_distance(self, alpha, beta):
		phi = abs(beta - alpha) % 360
		distance = 360 - phi if phi > 180 else phi
		return distance

	def update(self):
		player = self._scene.player
		vec_to_player = player.position - self.position
		dir_to_player = math.atan2(vec_to_player.y, vec_to_player.x)

		angle = self._angle_distance(player.direction, dir_to_player)
		if angle < math.pi/2:
			dirvec = vec_to_player
			speed = AVOID_ACCELERATION
		else:
			avoid_point = Point(1, 1)
			avoid_count = 0

			for obj in self.scene.objects:
				if isinstance(obj, pl.Bullet):
					distance = (obj.position - self.position).length_sqr()
					if distance <= AVOID_DISTANCE_SQR:
						avoid_point += obj.position
						avoid_count += 1

			if avoid_count > 0:
				avoid_point /= avoid_count
				dirvec = self.position - avoid_point
				speed = AVOID_DODGE
			else:
				dirvec = vec_to_player
				speed = AVOID_ACCELERATION

		self._velocity += dirvec * speed / dirvec.length()

		if self._velocity.length_sqr() > AVOID_SPEED_SQR:
			self._velocity.normalize()
			self._velocity *= AVOID_SPEED

		self.position += self._velocity
		self.direction += DUMB_ANGULAR_SPEED

BRICK_ACCELERATION = 0.3
BRICK_SPEED = 3
BRICK_SPEED_SQR = BRICK_SPEED*BRICK_SPEED
BRICK_MASS = 0.2
BRICK_SCALE = 7
BRICK_ANGULAR_SPEED = 0.025
BRICK_SLEEP_TIME = 15
class Brick(Enemy):
	def __init__(self, scene, x, y, n = 2):
		super().__init__(scene, x, y)
		self._velocity = Point(0, 0)
		self._size = n
		myscale = BRICK_SCALE + 3 - n
		self.set_shape(sh.BRICK_SHAPE[n], Colors.split, True, myscale)
		self._sleep = BRICK_SLEEP_TIME if n < 2 else 0

	def destroy(self):
		if self._size > 0:
			s = BRICK_SCALE
			off = self._size*s
			n = self._size - 1
			for x in range(0, 2):
				for y in range(0, 2):
					celloffset = Point(off + x*s, off + y*s)
					cellpos = self.position + celloffset
					child = Brick(self._scene, cellpos.x, cellpos.y, n)
					child._velocity = (cellpos - self.position)*2
					self._scene.add_object(child)

		super().destroy()

	def update(self):
		super().update()
		if self._sleep <= 0:
			player = self._scene.player
			dirvec = player.position - self.position
			self._velocity += dirvec * BRICK_ACCELERATION / dirvec.length()
		else:
			self._sleep -= 1

		if self._velocity.length_sqr() > BRICK_SPEED:
				self._velocity.normalize()
				self._velocity *= BRICK_SPEED

		self.position += self._velocity
		self.direction += self._velocity.length()*BRICK_ANGULAR_SPEED
