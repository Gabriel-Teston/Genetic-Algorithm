import numpy as np
import math


class Frogs:
    def __init__(self, window, dna, lillypads, target):
        self.window = window
        self.dna = dna
        self.lillypads = lillypads
        self.target = target
        self.nodes = np.zeros((0, 3))
        self.position = np.zeros(2, )
        self.velocity = np.zeros(2, )
        self.acceleration = np.zeros(2, )
        self.fitness = 0
        self.dead = False
        self.life_time = 0
        self.color = (0, 250, 0)
        self.complete = False

    def apply_force(self, force):
        self.acceleration = np.add(self.acceleration, force)

    def update(self, count):
        angle = math.atan2(self.velocity[0], self.velocity[1])
        self.apply_force(self.dna[count])
        self.velocity = np.add(self.velocity, self.acceleration)
        matrix = self.translation_matrix(self.velocity[0], self.velocity[1])
        angle = math.atan2(self.velocity[0], self.velocity[1]) - angle
        self.position = self.find_center()
        self.rotate(self.position, -angle)
        self.transform(matrix)
        self.acceleration = np.multiply(self.acceleration, 0)
        self.dead = True
        self.color = (0, 0, 0)
        if self.position[0] <= self.window.width or self.position[0] >= 0 or self.position[1] <= self.window.height or \
                        self.position[1] >= 0:
            for lillypad in self.lillypads:
                x, y = self.find_center()
                if math.hypot(x - lillypad.cord[0], y - lillypad.cord[1]) <= 50:
                    self.dead = False
                    self.color = (0, 255, 0)
                    self.life_time += 1
        if math.hypot(self.position[0] - self.target.cord[0], self.position[1] - self.target.cord[1]) <= 50:
            self.complete = True

    def translation_matrix(self, dx=0, dy=0):
        """ Return matrix for translation along vector (dx, dy). """

        return np.array([[1, 0, 0],
                         [0, 1, 0],
                         [dx, dy, 1]])

    def show(self):
        self.window.draw_polygon([[node[0], node[1]] for node in self.nodes], 0, self.color)

    def transform(self, matrix):
        self.nodes = np.dot(self.nodes, matrix)

    def rotate(self, (cx, cy), radians):
        for node in self.nodes:
            x = node[0] - cx
            y = node[1] - cy
            d = math.hypot(y, x)
            theta = math.atan2(y, x) + radians
            node[0] = cx + d * math.cos(theta)
            node[1] = cy + d * math.sin(theta)

    def find_center(self):
        num_nodes = len(self.nodes)
        mean_x = sum([node[0] for node in self.nodes]) / num_nodes
        mean_y = sum([node[1] for node in self.nodes]) / num_nodes
        return mean_x, mean_y

    def add_nodes(self, node_array):
        ones_column = np.ones((len(node_array), 1))
        ones_added = np.hstack((node_array, ones_column))
        self.nodes = np.vstack((self.nodes, ones_added))
        self.position = np.hstack(self.find_center())

    def calc_fitness(self):
        x, y = self.find_center()
        dist = math.hypot(x - self.target.cord[0], y - self.target.cord[1])
        self.fitness = 100 / dist + self.life_time / 100
        if self.dead:
            # self.fitness /= 10
            pass
