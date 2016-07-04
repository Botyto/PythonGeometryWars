import time

from collections import defaultdict
from Painter import Painter


class SceneManager:
    def __init__(self):
        self.scene = None
        self._keys = defaultdict(lambda: False)
        self._buttons = (False, False, False)
        self._mouse = (0, 0)
        self._surface = None
        self._window_size = (640, 480)

    def begin(self, sceneType):
        self.scene = sceneType(self)

    def update(self):
        if self.scene:
            begin = time.clock()
            self.scene.update()
            end = time.clock()
            print("update :: %fms" % ((end - begin)*1000))

    def draw(self):
        if self.scene:
            begin = time.clock()
            self.scene.draw()
            end = time.clock()
            print("draw :: %fms" % ((end - begin)*1000))

    def handle_event(self, ev):
        if self.scene:
            self.scene.handle_event(ev)

    def window_size(self):
        return self._window_size

    def update_window_size(self, w, h):
        self._window_size = (w, h)

    def drawing_surface(self):
        return self._surface

    def key_state(self, key):
        return self._keys[key]

    def button_state(self, button):
        return self._buttons[button]

    def mouse_position(self):
        return self._mouse

    def retarget_drawing(self, surface):
        self._surface = surface

    def update_keys(self, keys):
        self._keys = keys

    def update_buttons(self, buttons):
        self._buttons = buttons

    def update_mouse(self, mouse_position):
        self._mouse = mouse_position
