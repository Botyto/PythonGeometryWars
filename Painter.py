import pygame as pg

class Painter:
    def __init__(self, surface):
        self.surface = surface


    def clear(self, color):
        self.surface.fill(color)


    def blit(self, sprite, x, y):
        self.surface.blit()


    def fill_rect(self, rectangle, color):
        rect(rectangle, color, 0)


    def rect(self, rectangle, color, width = 1):
        pg.draw.rect(self.surface, color, rectangle, width)


    def fill_circle(self, center, radius, color):
        circle(center, radius, color, 0)


    def circle(self, center, radius, color, width = 1):
        pg.draw.circle(self.surface, color, center, radius, width)


    def rline(self, begin, end, color, width = 1):
        pg.draw.line(self.surface, color, begin, end, width)


    def aaline(self, begin, end, color, width = 1):
        pg.draw.aaline(self.surface, color, begin, end, width)


    line = rline
