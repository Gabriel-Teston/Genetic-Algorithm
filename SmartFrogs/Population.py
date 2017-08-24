from Window import *
from Target import *
from Frogs import *
from LillyPad import *
from DNA import *
import time


class Population:
    def __init__(self, window):
        self.window = window
        self.frogs = []
        self.popsize =300
        self.dna = DNA()
        self.target = Target(self.window)
        self.lilly_pads = []
        self.matingpool = []
        self.count = 0
        for lillypad in range(0, 30):
            self.lilly_pads.append(
                LillyPad(self.window, (random.randrange(0, window.width), random.randrange(0, window.height))))
        self.lilly_pads.append(LillyPad(self.window, (self.window.width / 2, self.window.height - 50)))
        self.lilly_pads.append(LillyPad(self.window, (self.target.cord[0], self.target.cord[1])))
        for frog in xrange(self.popsize):
            self.frogs.append(Frogs(self.window, self.dna.get_random_dna(), self.lilly_pads, self.target))
            frog_nodes = (lambda x, y: [(x - 10, y - 10), (x + 10, y - 10), (x + 10, y + 10), (x - 10, y + 10)])
            self.frogs[frog].add_nodes(frog_nodes(self.window.width / 2, self.window.height - 50))

    def update(self):
        self.window.fill()
        for lillypad in self.lilly_pads:
            lillypad.show()
        for frog in self.frogs:
            if not frog.dead and not frog.complete:
                frog.update(self.count)
            frog.show()
        self.target.show()
        self.count += 1

    def evaluate(self):
        max_fitness = 0
        self.matingpool = []
        for frog in self.frogs:
            frog.calc_fitness()
            if frog.fitness > max_fitness:
                max_fitness = frog.fitness
        for frog in self.frogs:
            frog.fitness /= max_fitness
        for frog in self.frogs:
            n = int(frog.fitness)
            for i in xrange(n * 100):
                self.matingpool.append(frog)

    def selection(self):
        new_frogs = []
        for frog in self.frogs:
            parent_a_dna = random.choice(self.matingpool).dna
            parent_b_dna = self.matingpool[random.randint(0, len(self.matingpool) - 1)].dna
            child_dna = self.dna.crossover(parent_a_dna, parent_b_dna)
            new_frog = Frogs(self.window, child_dna, self.lilly_pads, self.target)
            new_frog_nodes = (lambda x, y: [(x - 10, y - 10), (x + 10, y - 10), (x + 10, y + 10), (x - 10, y + 10)])
            new_frog.add_nodes(new_frog_nodes(self.window.width / 2, self.window.height - 50))
            new_frogs.append(new_frog)
        self.frogs = new_frogs

    def shufle_lillypads(self):
        new_lillypads = []
        for lillypad in xrange(len(self.lilly_pads)):
            new_lillypads.append(LillyPad(self.window, (
            random.randrange(0, self.window.width), random.randrange(0, self.window.height))))
        new_lillypads.append(LillyPad(self.window, (self.window.width / 2, self.window.height - 50)))
        new_lillypads.append(LillyPad(self.window, (self.target.cord[0], self.target.cord[1])))
        self.lilly_pads = new_lillypads


def main():
    window = Window((700, 600), (0, 0, 105))
    population = Population(window)
    running = 1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    population.shufle_lillypads()
        if population.count < 30:

            population.update()
            window.update()
            # time.sleep(0.2)
        else:
            population.count = 0
            population.evaluate()
            population.selection()


if __name__ == '__main__':
    main()
