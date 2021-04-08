from knapsack import Item
from typing import List
from random import choices, uniform

class Genome:
    ew = -1
    p = -1
    k = -1
    n = 0
    genome = List[int]

    def __init__(self, genome:List[int]= None, n=0):
        
        if(n > 0):
            self.n = n
            self.genome = choices([0,1], k=n)
        else:
            self.n = len(genome)
            self.genome = genome

    #mutation with 1/n probability for each gene
    def offspring(self, items:[Item])->'Genome':
        child = Genome(genome = self.genome.copy())
        child.k = self.k
        child.p = self.p
        child.ew = self.ew
        child.n = self.n

        g = child.genome
        i = 1
        while i < self.n:
            mutationPos = int(uniform(1,self.n))
            if mutationPos == i  :
                g[i-1]= abs(g[i-1] - 1)
                if g[i-1] == 1 :
                    child.k += 1
                    child.ew += items[i-1].expected_weight
                    child.p += items[i-1].profit
                else :
                    child.k -= 1
                    child.ew -= items[i-1].expected_weight
                    child.p -= items[i-1].profit
            i+=1
        return child

    def expected_weight(self, items:[Item]):
        if(self.ew < 0):
            self.calculate_ew_p(items)
        return self.ew;


    def profit(self, items:[Item]):
        if(self.p < 0):
            self.calculate_ew_p(items)
        return self.p;

    def countItems(self):
        if(self.k < 0):
            self.k = 0
            for gene in self.genome:
                self.k += gene
        return self.k;

    def calculate_ew_p(self, items:[Item]):
        self.b = 0
        self.ew = 0
        self.k = 0
        i = 0
        while i < len(items):
            if(self.genome[i] == 1):
                self.ew += (items[i].expected_weight)
                self.p += (items[i].profit)
                self.k += 1
            i+=1
