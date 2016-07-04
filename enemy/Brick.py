from enemy.Enemy import Enemy
from Point import Point
import Shape as sh
import Colors

ACCELERATION = 0.3
SPEED = 3
SPEED_SQR = SPEED*SPEED
MASS = 0.2
SCALE = 9
ANGULAR_SPEED = 0.025
SLEEP_TIME = 15


class Brick(Enemy):
    def __init__(self, scene, x, y, n=2):
        super().__init__(scene, x, y)
        self._velocity = Point(0, 0)
        self._size = n
        myscale = SCALE - n*2
        self.set_shape(sh.BRICK_SHAPE[n], Colors.split, True, myscale)
        self._sleep = SLEEP_TIME if n < 2 else 0

    def destroy(self):
        if self._size > 0:
            s = SCALE
            off = self._size*s
            n = self._size - 1
            for x in range(0, 2):
                for y in range(0, 2):
                    celloffset = Point(off + x*s, off + y*s)
                    cellpos = self.position + celloffset
                    child = Brick(self._scene, cellpos.x, cellpos.y, n)
                    child._velocity = (cellpos - self.position)*2
                    self._scene.add_object(child)

        super().destroy()

    def update(self):
        if self._sleep <= 0:
            player = self._scene.player
            dirvec = player.position - self.position
            self._velocity += dirvec * ACCELERATION / dirvec.length()
        else:
            self._sleep -= 1

        if self._velocity.length_sqr() > SPEED:
                self._velocity.normalize()
                self._velocity *= SPEED

        self.position += self._velocity
        self.direction += self._velocity.length()*ANGULAR_SPEED
        super().update()
