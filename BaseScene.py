from Painter import Painter
import Colors

class BaseScene:
	def __init__(self, manager):
		self.manager = manager
		self.objects = []
		self.size = (1000, 1000)


	def add_object(self, obj):
		self.objects.append(obj)


	def update(self):
		for obj in self.objects:
			obj.update()


	def draw(self):
		p = Painter(self.manager.drawing_surface())
		p.clear(Colors.black)

		for obj in self.objects:
			obj.draw()


	def key_down(self, key):
		return self.manager.key_state(key) == True


	def key_up(self, key):
		return self.manager.key_state(key) == False


	def button_down(self, button):
		return self.manager.button_state(button) == True


	def button_up(self, button):
		return self.manager.button_state(button) == False


	def mouse_position(self):
		return self.manager.mouse_position()
