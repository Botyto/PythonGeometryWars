from ParticleSystem import ParticleSystem
from Painter import Painter
from Point import Point
import Colors


class BaseScene:
    def __init__(self, manager):
        self.manager = manager
        self.objects = []
        self.size = (1000, 1000)
        self._ps = ParticleSystem(self)
        self.objects.append(self._ps)

    @property
    def particle_system(self):
        return self._ps

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        self.objects.remove(obj)

    def update(self):
        for obj in self.objects:
            obj.update()

        for obj1 in self.objects:
            for obj2 in self.objects:
                if obj1 is obj2:
                    continue
                r = obj1.collision_radius_sqr() + obj2.collision_radius_sqr()
                if (obj1.position - obj2.position).length_sqr() <= r:
                    obj1.collide_with(obj2)
                    obj2.collide_with(obj1)

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
        mp = self.manager.mouse_position()
        return Point(mp[0], mp[1])
