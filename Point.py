from numbers import Number
import math

class Point:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y


    @classmethod
    def anglelen(cls, radians, length):
        return Point(math.cos(radians)*length, math.sin(radians)*length)


    def length(self):
        return math.sqrt(self.length_sqr())


    def length_sqr(self):
        return self.x**2 + self.y**2


    def normalize(self):
        length = self.length()
        self.x /= length
        self.y /= length


    def normalized(self):
        length = self.length()
        return self/length


    def rotate_around(self, anchor, radians):
        diff = self - anchor
        sin = math.sin(radians)
        cos = math.cos(radians)
        x = diff.x*cos - diff.y*sin
        y = diff.x*sin + diff.y*cos
        self += anchor

    @property
    def coords(self):
        return (self.x, self.y)


    @coords.setter
    def coords(self, value):
        self.x = value[0]
        self.y = value[1]


    def __eq__(self, value):
        if isinstance(value, Point):
            return self.coords() == value.coords()
        else:
            raise ValueError("Point can be compared to Point")


    def __add__(self, value):
        if isinstance(value, Point):
            return Point(self.x + value.x, self.y + value.y)
        elif isinstance(value, Number):
            return Point(self.x + value, self.y + value)
        else:
            raise ValueError("Point can be added to Point or number")


    def __sub__(self, value):
        if isinstance(value, Point):
            return Point(self.x - value.x, self.y - value.y)
        elif isinstance(value, Number):
            return Point(self.x - value, self.y - value)
        else:
            raise ValueError("Point or number be subtracted from Point")


    def __neg__(self):
        return Point(-self.x, -self.y)


    def __mul__(self, value):
        if isinstance(value, Number):
            return Point(self.x*value, self.y*value)
        else:
            raise ValueError("Point can be multiplied by number")


    def __truediv__(self, value):
        if isinstance(value, Number):
            return Point(self.x/value, self.y/value)
        else:
            raise ValueError("Point can be divided by number")


    def __floordiv__(self, value):
        if isinstance(value, Number):
            return Point(self.x//value, self.y//value)
        else:
            raise ValueError("Point can be divided by number")


    def __str__(self):
        return "(%f, %f)" % (self.x, self.y)
