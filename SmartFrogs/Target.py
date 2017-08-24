class Target:
    def __init__(self, window):
        self.window = window
        self.cord = (window.width / 2, 100)

    def show(self):
        self.window.draw_circle(self.cord, 50, 1, (0, 0, 255))
