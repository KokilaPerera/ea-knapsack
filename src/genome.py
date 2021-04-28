from knapsack import Item
from typing import List
from random import choices, uniform, random

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

    def __copy__(self):
        clone = Genome(genome = self.genome.copy())
        clone.k = self.k
        clone.p = self.p
        clone.ew = self.ew
        clone.n = self.n
        return clone

    def __str__(self):
        return str(self.k)+ " items : p = " + str(self.p) + " ew = " + str(self.ew)

    def offspring(self, items:[Item])->'Genome':
        child = self.__copy__()
        child.mutation(items)
        return child
    
    def mutation(self, items= []):
        g = self.genome
        i = 0
        while i < self.n :
##            mutationPos = int(uniform(0, self.n))
            mutationPos = int(random()* 100)
            if mutationPos == i :
                g[i]= abs(g[i] - 1)
                if(len(items) > 0):
                    if g[i] == 1 :
                        self.k += 1
                        self.ew += items[i].expected_weight
                        self.p += items[i].profit
                    else :
                        self.k -= 1
                        self.ew -= items[i].expected_weight
                        self.p -= items[i].profit
            i += 1
            #break

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
