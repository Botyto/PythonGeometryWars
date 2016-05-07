import math
import random

from Point import Point
from GameObject import GameObject

class Particle:
	def __init__(self, position, direction, speed, color):
		self.velocity = Point.anglelen(direction, speed)
		self.position = position
		self.color = color


	def update(self):
		self.position += self.velocity
		self.velocity *= PS_DECAY


	def is_dead(self):
		return self.velocity.length_sqr() <= 2


PS_COEF = 3
PS_SPEED = 15
PS_SPEED_DIFF = 10
PS_DECAY = 0.93


class ParticleSystem(GameObject):
	def __init__(self, scene):
		super().__init__(scene)
		self._parts = []

	def update(self):
		to_remove = []
		for part in self._parts:
			part.update()
			if part.is_dead():
				to_remove.append(part)

		for part in to_remove:
			self._parts.remove(part)

	def burst(self, position, direction, color, count, wiggle = math.pi/2):
		for i in range(count*PS_COEF):
			dd = direction + random.uniform(-wiggle, +wiggle)
			ss = PS_SPEED + random.uniform(0, PS_SPEED_DIFF)
			self._parts.append(Particle(position, dd, ss, color))

	def explode(self, position, color, count):
		for i in range(count*PS_COEF):
			dd = random.uniform(0, 2*math.pi)
			ss = PS_SPEED + random.uniform(0, PS_SPEED_DIFF)
			self._parts.append(Particle(position, dd, ss, color))

	def draw(self):
		p = self.painter
		for part in self._parts:
			p.line(part.position, part.position + part.velocity*3, part.color, 2)
