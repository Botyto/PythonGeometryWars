import Shape as sh
import Player as pl
from Point import Point


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
