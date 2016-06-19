import math

from Point import Point
from Painter import Painter

class GameObject:
    def __init__(self, scene):
        self._scene = scene
        self._position = Point(0, 0)
        self._collision_radius_sqr = 0
        self._clamp_inside = True


    @property
    def is_outside(self):
        w = self._scene.size
        return self.x < 0 or self.y < 0 or self.x > w[0]  or self.y > w[1]
    

    @property
    def position(self):
        return self._position
    

    @position.setter
    def position(self, value):
        self.position = value


    @property
    def scene(self):
        return self._scene


    @property
    def scene_manager(self):
        return self._scene.manager


    @property
    def painter(self):
        return Painter(self.scene_manager.drawing_surface())
    

    def collision_radius_sqr(self):
        return self._collision_radius_sqr


    def collision_radius(self):
        return math.sqrt(self._collision_radius_sqr)


    def add_object(self, obj):
        self.scene.add_object(obj)


    def destroy(self):
        self.scene.remove_object(self)


    @property
    def x(self):
        return self.position.x


    @property
    def y(self):
        return self.position.y
    
    
    def update(self):
        def clamp(x, low, high):
            return max(min(x, high), low)

        if self._clamp_inside:
            self.position.x = clamp(self.position.x, 0, self.scene.size[0])
            self.position.y = clamp(self.position.y, 0, self.scene.size[1])


    def draw(self):
        pass


    def collide_with(self, other):
        pass


    def key_down(self, key):
        return self._scene.key_down(key)


    def key_up(self, key):
        return self._scene.key_up(key)


    def mouse_position(self):
        return self._scene.mouse_position()


    def button_down(self, button):
        return self._scene.button_down(button)


    def button_up(self, button):
        return self._scene.button_up(button)
