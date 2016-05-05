from Point import Point
from Painter import Painter

class GameObject:
    def __init__(self, scene):
        self._scene = scene
        self.position = Point(0, 0)


    @property   
    def scene(self):
        return self._scene


    @property
    def scene_manager(self):
        return self._scene.manager


    @property
    def painter(self):
        return Painter(self.scene_manager.drawing_surface())
    
    
    def update(self):
        pass


    def draw(self):
        pass
