import os
import sys
import time
import pygame as pg

from SceneManager import SceneManager
from GameScene import GameScene

WIDTH = 800
HEIGHT = 600


class Application:
    def __init__(self):
        self._running = False
        self.target_fps = 60
        self.clock = pg.time.Clock()
        self.scene_manager = SceneManager()
        self.scene_manager.update_window_size(WIDTH, HEIGHT)
        self.scene_manager.retarget_drawing(pg.display.get_surface())
        self.scene_manager.begin(GameScene)

    def run(self):
        self._running = True
        while (self._running):
            self.events()
            self.update()
            self.draw()
            self.clock.tick(self.target_fps)

    def events(self):
        self.scene_manager.update_keys(pg.key.get_pressed())
        self.scene_manager.update_buttons(pg.mouse.get_pressed())
        self.scene_manager.update_mouse(pg.mouse.get_pos())
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                self.stop()

    def update(self):
        if not self.scene_manager.scene:
            self.stop()
            return
        self.scene_manager.update()

    def draw(self):
        self.scene_manager.draw()
        pg.display.flip()

    def stop(self):
        self._running = False


def main():
    time.clock()

    pg.init()
    os.environ["SDL_VIDEO_CENTERED"] = "TRUE"
    pg.display.set_caption("Python Geometry Wars")
    pg.display.set_mode((WIDTH, HEIGHT))

    app = Application()
    app.run()

    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
