import math
import random

from enemy.Enemy import Enemy
from Point import Point
import Shape as sh
import Colors

SPEED = 2
ACCELERATION = 0.1
ANGULAR_SPEED = math.pi/70


class Dumb(Enemy):
    def __init__(self, scene, x, y):
        super().__init__(scene, x, y)
        angl = random.uniform(0, math.pi*2)
        self._velocity = Point.anglelen(angl, SPEED)
        self.set_shape(sh.PINWHEEL_SHAPE, Colors.dumb, True, 5)

    def update(self):
        angl = random.uniform(0, math.pi*2)
        self._velocity += Point.anglelen(angl, ACCELERATION)
        self._velocity *= SPEED / self._velocity.length()
        self.position += self._velocity
        self.direction += ANGULAR_SPEED

        w = self.scene_manager.window_size()
        if self.position.x < 0 or self.position.x > w[0]:
            self._velocity.x *= -1
        if self.position.y < 0 or self.position.y > w[1]:
            self._velocity.y *= -1

        super().update()
