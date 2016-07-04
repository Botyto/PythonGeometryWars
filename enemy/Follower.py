import math

from enemy.Enemy import Enemy
from Point import Point
import Shape as sh
import Colors

SPEED = 2


class Follower(Enemy):
    def __init__(self, scene, x, y):
        super().__init__(scene, x, y)
        self.set_shape(sh.HOURGLASS_SHAPE, Colors.follow, True, 5)

    def update(self):
        dirvec = self._scene.player.position - self.position
        self.position += dirvec * SPEED / dirvec.length()
        self.direction = math.atan2(dirvec.y, dirvec.x)
        super().update()
