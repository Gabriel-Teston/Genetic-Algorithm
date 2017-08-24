import numpy as np
from Window import *
import math
import random


class Population:
    def __init__(self, window):
        self.window = window
        self.rockets = []
        self.dna = DNA()
        self.popsize = 200
        self.target = Target(self.window)
        self.obstacles = []
        self.obstacles.append(Obstacle(self.window, (window.width / 2, window.height - 200)))
        # self.obstacles.append(Obstacle(self.window, (window.width / 2, window.height - 450)))
        # self.obstacles.append(Obstacle(self.window, (window.width-150, window.height - 300)))
        # self.obstacles.append(Obstacle(self.window, (50, window.height - 300)))
        self.matingpool = []
        for rocket in xrange(self.popsize):
            self.rockets.append(Rockets(self.window, self.target, self.dna.get_random_dna()))
            rocket_nodes = (lambda x, y: [(x + 0, y + 0), (x + 10, y + 0), (x + 5, y + 15)])
            self.rockets[rocket].add_nodes(rocket_nodes(self.window.width / 2, self.window.height - 10))

    def update(self, count):
        min_dist = self.window.height * self.window.width
        for rocket in self.rockets:
            if not rocket.complete:
                rocket.update(count, self.obstacles)
            dist = math.hypot(self.target.cord[0] - rocket.position[0], self.target.cord[1] - rocket.position[1])
            if dist < min_dist:
                closer = rocket
                min_dist = dist
            rocket.show((255, 0, 0))
        closer.show((0, 255, 0))
        self.target.show()
        for obstacle in self.obstacles:
            obstacle.show()

    def evaluate(self):
        max_fitness = 0
        min_time = 400
        self.matingpool = []
        for rocket in self.rockets:
            rocket.calc_fitness()
            if rocket.fitness > max_fitness:
                max_fitness = rocket.fitness
            if rocket.time < min_time and rocket.reach == True:
                min_time = rocket.time
        print max_fitness, min_time
        for rocket in self.rockets:
            rocket.fitness /= max_fitness
            if rocket.time < min_time and rocket.reach == True:
                rocket.time /= min_time
        for rocket in self.rockets:
            n = int(rocket.fitness * rocket.time)
            for j in range(n):
                self.matingpool.append(rocket)

    def selection(self):
        new_rockets = []
        for rocket in self.rockets:
            parent_a_dna = self.matingpool[random.randint(0, len(self.matingpool) - 1)].dna
            parent_b_dna = self.matingpool[random.randint(0, len(self.matingpool) - 1)].dna
            child_dna = self.dna.crossover(parent_a_dna, parent_b_dna)
            new_rocket = Rockets(self.window, self.target, child_dna)
            new_rocket_nodes = (lambda x, y: [(x + 0, y + 0), (x + 10, y + 0), (x + 5, y + 15)])
            new_rocket.add_nodes(new_rocket_nodes(self.window.width / 2, self.window.height - 10))
            new_rockets.append(new_rocket)

        self.rockets = new_rockets


class Rockets:
    def __init__(self, window, target, dna):
        self.nodes = np.zeros((0, 3))
        self.position = np.zeros(2, )
        self.window = window
        self.target = target
        self.velocity = np.zeros(2, )
        self.acceleration = np.zeros(2, )
        self.dna = dna
        self.fitness = 0
        self.complete = False
        self.reach = False
        self.time = 0

    def apply_force(self, force):
        self.acceleration = np.add(self.acceleration, force)

    def update(self, count, obstacles):
        self.time = count
        angle = math.atan2(self.velocity[0], self.velocity[1])
        self.apply_force(self.dna[count])
        self.velocity = np.add(self.velocity, self.acceleration)
        matrix = translation_matrix(self.velocity[0], self.velocity[1])
        angle = math.atan2(self.velocity[0], self.velocity[1]) - angle
        self.position = self.find_center()
        if self.position[0] > self.window.width or self.position[0] < 0 or self.position[1] > self.window.height or \
                        self.position[1] < 0:
            self.complete = True
        if math.hypot(self.target.cord[0] - self.position[0], self.target.cord[1] - self.position[1]) <= 10:
            self.complete = True
            self.reach = True
        for obstacle in obstacles:
            if self.position[0] >= obstacle.left_side and self.position[0] <= obstacle.right_side and self.position[
                1] <= obstacle.lower_side and self.position[1] >= obstacle.upper_side:
                self.complete = True
        self.rotate(self.position, -angle)
        self.transform(matrix)
        self.acceleration = np.multiply(self.acceleration, 0)

    def calc_fitness(self):
        dist = math.hypot(self.target.cord[0] - self.position[0], self.target.cord[1] - self.position[1])
        self.fitness = 1 / dist
        if dist <= 1:
            pass
            # self.fitness *=10

    def show(self, color):
        self.window.draw_polygon([[node[0], node[1]] for node in self.nodes], 0, color)

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
        # np.hstack((node_array[0][0] - 5, node_array[0][1]))


def translation_matrix(dx=0, dy=0):
    """ Return matrix for translation along vector (dx, dy). """

    return np.array([[1, 0, 0],
                     [0, 1, 0],
                     [dx, dy, 1]])


class DNA:
    def __init__(self, genes=None):
        self.genes = []
        self.dna_length = 400

    def crossover(self, parent_a_dna, parent_b_dna):
        self.new_genes = []
        mid = random.randint(0, len(self.genes))
        for gene in xrange(len(parent_a_dna)):
            if gene > mid:
                self.new_genes.append(parent_a_dna[gene])
                pass
            else:
                self.new_genes.append(parent_b_dna[gene])
        for gene in range(len(self.new_genes)):
            if random.randint(0, 1000) < 1:
                self.new_genes[gene] = np.random.random(2, ) - 0.5
        return self.new_genes

    def get_random_dna(self):
        self.genes = []
        for gene in xrange(400):
            self.genes.append(np.random.random(2, ) - 0.5)
        return self.genes


class Target:
    def __init__(self, window):
        self.window = window
        self.cord = np.zeros(2, )
        self.cord = np.hstack((window.width / 2, 100))

    def show(self):
        self.window.draw_circle(self.cord, 20, 1, (0, 0, 255))


class Obstacle:
    def __init__(self, window, cord):
        self.window = window
        self.cord = [(cord[0] - 200, cord[1] + 10), (cord[0] + 200, cord[1] + 10),
                     (cord[0] + 200, cord[1] - 10), (cord[0] - 200, cord[1] - 10)]
        self.left_side = cord[0] - 200
        self.right_side = cord[0] + 200
        self.upper_side = cord[1] - 10
        self.lower_side = cord[1] + 10
        print self.cord

    def show(self):
        self.window.draw_polygon(self.cord, 0, (0, 0, 0))


def main():
    window = Window((700, 700), (255, 255, 255))
    population = Population(window)
    running = 1
    i = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if i < 400:
            window.fill()
            population.update(i)
            window.update()
            i += 1
        else:
            population.evaluate()
            population.selection()
            i = 0


if __name__ == '__main__':
    main()
