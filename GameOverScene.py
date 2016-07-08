import pygame as pg

from BaseScene import BaseScene
import GameScene
from Painter import Painter
import Colors


class GameOverScene(BaseScene):
    def __init__(self, manager):
        super().__init__(manager)
        self.score = -1
        self.high = -1
        self.newhigh = False
        self.exiting = False

    def set_score(self, score):
        with open("high.txt") as f:
            self.high = int(f.read())

        self.score = score
        if self.score > self.high:
            print("***** NEW HIGHSCORE *****")
            self.newhigh = True
            with open("high.txt", "w") as f:
                f.write(str(self.score))
        
    def update(self):
        super().update()

        if self.key_down(pg.K_RETURN):
            self.exiting = True

        if self.key_up(pg.K_RETURN) and self.exiting:
            self.manager.begin(GameScene.GameScene)

    def draw(self):
        painter = Painter(self.manager.drawing_surface())
        painter.clear(Colors.black)

        scorestr = "Score: " + str(self.score)
        highstr = "Highscore: " + str(self.high)
        newstr = "*** New highscore ***" if self.newhigh else ""

        painter.text((300, 280), scorestr, Colors.white)
        painter.text((300, 305), highstr, Colors.white)
        painter.text((300, 330), newstr, Colors.white)
