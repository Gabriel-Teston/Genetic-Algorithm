import random


class LillyPad:
    def __init__(self, window, (x, y)):
        self.window = window
        self.cord = (x, y)

    def show(self):
        self.window.draw_circle(self.cord, 50, 50, (0, 100, 25))
