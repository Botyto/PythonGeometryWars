from BaseScene import BaseScene
from Point import Point
from Painter import Painter

from Grid import PhysicsGrid
from FastGrid import FastGrid
from StaticGrid import StaticGrid
from Player import Player
import Enemy as en

class GameScene(BaseScene):
	def __init__(self, manager):
		super().__init__(manager)
		self.grid = StaticGrid(self, 30, 40)
		self.add_object(self.grid)
		self.player = Player(self, 50, 50)
		self.add_object(self.player)

		self.add_object(en.Dumb(self, 300, 100))
		self.add_object(en.Follower(self, 300, 600))


	def update(self):
		super().update()


	def draw(self):
		super().draw()
