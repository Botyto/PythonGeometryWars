from Painter import TransformMatrix as tmat
from GameObject import GameObject
import Colors

class ShapeObject(GameObject):
    def __init__(self, scene):
        super().__init__(scene)
        self.set_shape([], Colors.white, True)
        self.__direction = 0

        self.__pos_mat = tmat.translation(0, 0)
        self.__rot_mat = tmat.rotation(0)


    @property
    def position(self):
        return self._position


    @position.setter
    def position(self, value):
        self._position = value
        self.__pos_mat = tmat.translation(value.x, value.y)


    @property
    def direction(self):
        return self.__direction


    @direction.setter
    def direction(self, value):
        self.__direction = value
        self.__rot_mat = tmat.rotation(value)


    def set_shape(self, points, color, closed, scale = 1.0):
        if scale == 1.0:
            self.__points = points
        else:
            self.__points = [tuple(c*scale for c in pt) for pt in points]
        self.__color = color
        self.__closed = closed


    def draw(self):
        p = self.painter
        p.push(self.__pos_mat)
        p.push(self.__rot_mat)
        p.lines(self.__points, self.__color, self.__closed)
        p.pop()
        p.pop()

PLAYER_SHAPE = [
    ( 2.5, -1.5),
    (-0.5, -2.5),
    (-2.5,  0  ),
    (-0.5,  2.5),
    ( 2.5,  1.5),
    ( 0.5,  1.5),
    (-0.5,  0  ),
    ( 0.5, -1.5)
]

BULLET_SHAPE = [
    ( 1.0,  0.0),
    (-1.0, -0.5),
    (-1.0,  0.5),
]
