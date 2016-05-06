import math

import Colors
from Point import Point
from GameObject import GameObject

TENSION = 0.1

class FastMass:
    def __init__(self, x, y):
        self.position = Point(x, y)
        self._initial = Point(x, y)

    def update(self):
        self.position += (self._initial - self.position)*TENSION

class FastGrid(GameObject):
    def __init__(self, scene, size, scale):
        super().__init__(scene)
        self._size = size
        self._scale = scale
        self._rng = range(0, size)

        self._points = []
        for y in self._rng:
            for x in self._rng:
                self._points.append(FastMass(x*scale, y*scale))

        self.directed(Point(300, 200), 300, Point(150, 0))


    def update(self):
        for mass in self._points:
            mass.update()


    def directed(self, position, radius, force):
        sqradius = radius**2
        for mass in self._points:
                sqdist = (position - mass.position).length_sqr()
                if sqdist < sqradius:
                    dist = math.sqrt(sqdist)
                    mass.position += force * (10 / (10 + dist))


    def point(self, x, y):
        return self._points[x + y*self._size]


    def draw(self):
        painter = self.painter
        for x in range(0, self._size - 1):
            for y in range(0, self._size - 1):
                this  = self.point(x,     y    ).position
                right = self.point(x + 1, y    ).position
                down  = self.point(x,     y + 1).position

                painter.line(this.coords, right.coords, Colors.grid)
                painter.line(this.coords, down.coords,  Colors.grid)
