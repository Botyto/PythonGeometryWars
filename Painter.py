import math
import pygame as pg
from numbers import Number

from Point import Point

class TransformMatrix:
    def __init__(self):
        self.m = [0 for i in range(9)]
        self.m[0 + 0*3] = 1
        self.m[1 + 1*3] = 1
        self.m[2 + 2*3] = 1

    @classmethod
    def identity(cls):
        return cls()

    @classmethod
    def translation(cls, dx, dy):
        result = cls()
        result.set(2, 0, dx)
        result.set(2, 1, dy)
        return result

    @classmethod
    def rotation(cls, radians):
        result = cls()
        sin = math.sin(radians)
        cos = math.cos(radians)
        result.set(0, 0, cos)
        result.set(1, 0, -sin)
        result.set(0, 1, sin)
        result.set(1, 1, cos)
        return result

    @classmethod
    def scale(cls, sx, sy):
        result = cls()
        result.set(0, 0, sx)
        result.set(1, 1, sy)
        return result        

    def get(self, x, y):
        return self.m[x + y*3]

    def set(self, x, y, value):
        self.m[x + y*3] = value

    def __add__(self, value):
        map(lambda x, y: x + y, zip(self.m, value.m))

    def __sub__(self, value):
        map(lambda x, y: x - y, zip(self.m, value.m))

    def __mul__(self, value):
        result = TransformMatrix()
        if isinstance(value, Point):
            return Point(
                self.m[0]*value.x + self.m[1]*value.y + self.m[2],
                self.m[3]*value.x + self.m[4]*value.y + self.m[5])
        if isinstance(value, TransformMatrix):
            for x in range(3):
                for y in range(3):
                    s = 0
                    for i in range(3):
                        s += self.get(i, y)*value.get(x, i)
                    result.set(x, y, s) 

        elif isinstance(value, Number):
            result.m = [x*value for x in self.m]
        else:
            raise ValueError("Matrix can multiply by mat and number")

        return result

class Painter:
    def __init__(self, surface):
        self.surface = surface
        self.stack = [TransformMatrix.identity()]


    def push(self, matrix):
        self.stack.append(self.stack[-1] * matrix)


    def pop(self):
        self.stack.pop()


    def _t(self, point):
        if isinstance(point, Point):
            return (self.stack[-1]*point).coords
        else:
            temp = Point(point[0], point[1])
            return (self.stack[-1]*temp).coords


    def clear(self, color):
        self.surface.fill(color)


    def blit(self, sprite, pos):
        self.surface.blit(sprite, self._t(pos))


    def fill_rect(self, rectangle, color):
        rect(rectangle, color, 0)


    def rect(self, rectangle, color, width = 1):
        pg.draw.rect(self.surface, color, rectangle, width)


    def fill_circle(self, center, radius, color):
        circle(center, radius, color, 0)


    def circle(self, center, radius, color, width = 1):
        pg.draw.circle(self.surface, color, self._t(center), radius, width)


    def rline(self, begin, end, color, width = 1):
        pg.draw.line(self.surface, color, self._t(begin), self._t(end), width)


    def rlines(self, points, color, closed = False, width = 1):
        pg.draw.lines(self.surface, color, closed, points, width)


    def aaline(self, begin, end, color, width = 1):
        pg.draw.aaline(self.surface, color, self._t(begin), self._t(end), 1)


    def aalines(self, points, color, closed = False, width = 1):
        pg.draw.aalines(self.surface, color, closed, points, 1)


    def lines(self, points, color, closed = False, width = 1):
        self._lines([self._t(pt) for pt in points], color, closed, width)

    line = rline
    _lines = rlines
