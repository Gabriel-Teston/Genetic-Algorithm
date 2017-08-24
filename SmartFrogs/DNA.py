import numpy as np


class DNA:
    def __init__(self):
        self.dna_length = 30

    def crossover(self, parent_a_dna, parent_b_dna):
        self.new_genes = []
        mid = np.random.randint(0, self.dna_length)
        for gene in xrange(len(parent_a_dna)):
            if gene > mid:
                self.new_genes.append(parent_a_dna[gene])
                pass
            else:
                self.new_genes.append(parent_b_dna[gene])
        for gene in range(len(self.new_genes)):
            if np.random.randint(0, 100) < 1:
                self.new_genes[gene] = np.random.randint(0, 70) * np.random.random(2, ) - np.random.randint(0, 70) / 2
                # print "Mutation"
        return self.new_genes

    def get_random_dna(self):
        self.genes = []
        for gene in xrange(self.dna_length):
            self.genes.append(np.random.randint(0, 70) * np.random.random(2, ) - np.random.randint(0, 70) / 2)
        return self.genes
