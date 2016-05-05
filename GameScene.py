from BaseScene import BaseScene
from Point import Point
from Painter import Painter
from Grid import PhysicsGrid

class GameScene(BaseScene):
	def __init__(self, manager):
		super().__init__(manager)
		self.grid_size = 100
		self.add_object(PhysicsGrid(self, 100, 40))


	def update(self):
		super().update()


	def draw(self):
		super().draw()
