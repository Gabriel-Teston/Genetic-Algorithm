import pygame
from pygame.locals import *


class Window:
    def __init__(self, (width, height), background_color):
        self.width = width
        self.height = height
        self.background_color = background_color
        self.window_surface = pygame.display.set_mode((self.width, self.height), HWSURFACE | DOUBLEBUF | RESIZABLE)
        pygame.display.set_caption("Runnig!")

    def fill(self):
        self.window_surface.fill(self.background_color)

    def draw_circle(self, (x, y), size, thickness, colour):
        pygame.draw.circle(self.window_surface, colour, (x, y), size, thickness)

    def draw_polygon(self, nodes, thickness, colour):
        pygame.draw.polygon(self.window_surface, colour, nodes, thickness)

    def draw_line(self, start, end, thickness, colour):
        pygame.draw.line(self.window_surface, colour, start, end, thickness)

    @staticmethod
    def update():
        pygame.display.flip()
