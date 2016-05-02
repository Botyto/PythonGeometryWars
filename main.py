import os
import pygame as pg

class Application:
    def __init__(self):
        self._running = False

    def run(self):
        self._running = True
        while (self._running):
            pass

    def stop(self):
        self._running = False

def main():
    pg.init()
    os.environ["SDL_VIDEO_CENTERED"] = "TRUE"
    pg.display.set_caption("Python Geometry Wars")
    pg.display.set_mode((640, 480))

    app = Application()
    app.run()

    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
