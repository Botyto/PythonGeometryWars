from BaseScene import BaseScene
from Point import Point
from Painter import Painter

from Grid import PhysicsGrid
from FastGrid import FastGrid
from StaticGrid import StaticGrid
from Player import Player
from enemy import *


class GameScene(BaseScene):
    def __init__(self, manager):
        super().__init__(manager)
        self.grid = StaticGrid(self, 30, 40)
        self.add_object(self.grid)
        self.player = Player(self, 0, 0)
        self.player.position.coords = self.size
        self.player.position /= 2
        self.add_object(self.player)
        self.spawner = Spawner.Spawner(self)
        self.add_object(self.spawner)
        
    def update(self):
        super().update()

    def draw(self):
        super().draw()
