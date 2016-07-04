import math

import Colors
from Point import Point
from GameObject import GameObject


class StaticGrid(GameObject):
    def __init__(self, scene, size, scale):
        super().__init__(scene)
        self._size = size if size % 2 == 0 else size + 1
        self._scale = scale
        self._points = []

        w = self.scene_manager.window_size()
        for i in range(self._size):
            if i % 2 == 1:
                self._points.append((i*scale, 0   ))
                self._points.append((i*scale, w[1]))
            else:
                self._points.append((i*scale, w[1]))
                self._points.append((i*scale, 0   ))

        for i in range(self._size):
            if i % 2 == 0:
                self._points.append((w[0], i*scale))
                self._points.append((0,    i*scale))
            else:
                self._points.append((0,    i*scale))
                self._points.append((w[0], i*scale))

    def draw(self):
        self.painter.lines(self._points, Colors.grid, False, 2)
