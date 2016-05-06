import sys
import math

from GameObject import GameObject
from Point import Point
import Colors

MASS_DAMPING = 0.98

class PointMass:
    def __init__(self, x,  y, inverse_mass):
        self.inverse_mass = inverse_mass
        self.position = Point(x, y)
        self.velocity = Point(0, 0)
        self.acceleration = Point(0, 0)
        self.damping = MASS_DAMPING


    def apply(self, force):
        self.acceleration += force * self.inverse_mass


    def update(self):
        if self.acceleration.length_sqr() == 0 and self.velocity.length_sqr() == 0:
            return

        self.velocity += self.acceleration
        self.position += self.velocity
        self.acceleration.coords = (0, 0)
        if (self.velocity.length_sqr() < sys.float_info.epsilon):
            self.velocity.coords = (0, 0)

        self.velocity *= self.damping
        self.damping = self.damping


class Spring:
    def __init__(self, end1, end2, stiffness, damping):
        self.end1 = end1
        self.end2 = end2
        self._target = (end1.position - end2.position).length()*0.95
        self.stiffness = stiffness
        self.damping = damping


    def update(self):
        x = self.end1.position - self.end2.position
        length = x.length()
        if length < self._target or length == 0:
            return

        x = x * ((length - self._target) / length)
        dv = self.end2.velocity - self.end1.velocity
        force = x * self.stiffness - dv * self.damping

        self.end1.apply(-force)
        self.end2.apply(force)


class PhysicsGrid(GameObject):
    def __init__(self, scene, size, scale):
        super().__init__(scene)
        self._size = size
        self._scale = scale

        self._points = []
        self._springs = []

        for x in range(0, size):
            self._points.append([])
            for y in range(0, size):
                self._points[x].append(PointMass(x * self._scale, y * self._scale, 1))

        for x in range(0, size):
            for y in range(0, size):
                pt = self._points[x][y]
                fixed = PointMass(x * self._scale, y * self._scale, 0)
                if x == 0 or y == 0 or x == size - 1 or y == size - 1:
                    self._springs.append(Spring(fixed, pt, 0.1, 0.1))
                elif x % 3 == 0 and y % 3 == 0:
                    self._springs.append(Spring(fixed, pt, 0.002, 0.02))

                if x > 0:
                    left = self._points[x - 1][y]
                    self._springs.append(Spring(left, pt, 0.28, 0.06))

                if y > 0:
                    up = self._points[x][y - 1]
                    self._springs.append(Spring(up, pt, 0.28, 0.06))

        self.directed(Point(50, 50), 50, Point(20, 0))


    def directed(self, position, radius, force):
        sqradius = radius**2
        for column in self._points:
            for mass in column:
                sqdist = (position - mass.position).length_sqr()
                if sqdist < sqradius:
                    dist = math.sqrt(sqdist)
                    mass.apply(force * (10 / (10 + dist)))


    def implode(self, position, radius, force):
        pass


    def explode(self, position, radius, force):
        pass


    def update(self):
        for spring in self._springs:
            spring.update()

        for column in self._points:
            for mass in column:
                mass.update()


    def draw(self):
        painter = self.painter
        for x in range(0, self._size - 1):
            for y in range(0, self._size - 1):
                this  = self._points[x    ][y    ].position
                right = self._points[x + 1][y    ].position
                down  = self._points[x    ][y + 1].position

                painter.line(this.coords, right.coords, Colors.grid)
                painter.line(this.coords, down.coords,  Colors.grid)
