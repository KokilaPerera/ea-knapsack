from genome import Genome
from knapsack import Knapsack
from math import exp
from collections import namedtuple
from ea import EA, CHEBYSHEV, CHERNOFF


Fitness = namedtuple('Fitness',['u','v','p'])

class OnePlusOne (EA):
    def __init__(self, instance:Knapsack):
        super().__init__(instance)
        
        
    def run(self, alpha, delta,fitness_evaluations, method)->int:
        items = self.instance.items
        genomeX = Genome(n = len(items));
        fitnessX = self.fitness(genomeX, alpha, delta, method)
        ##print("\ti:0|k:", genomeX.countItems(),'|e:',genomeX.expected_weight(items), '|f:',fitnessX)
        
        i = 0
        j = 0
        while( i < fitness_evaluations ):
            i += 1
            genomeY = self.mutation(genomeX)
            fitnessY = self.fitness(genomeY, alpha, delta, method)
            if (self.selection(fitnessX,fitnessY)>0):
                print("\ti:",i,"|k:", genomeY.countItems(),'|e:',genomeY.expected_weight(items), '|f:',fitnessY )
                genomeX = genomeY            
                fitnessX = fitnessY
        
        print("****\ti:",i,"|k:", genomeX.countItems(),'|e:',genomeX.expected_weight(items), '|f:',fitnessX[2],"\n*****")
        return fitnessX[2]

    def selection(self, fitnessX:Fitness, fitnessY:Fitness) -> int:
        if(fitnessX.u==fitnessY.u):
            if (fitnessX.v==fitnessY.v):
                return self.compare(fitnessY.p,fitnessX.p)
            else:
                return self.compare(fitnessX.v,fitnessY.v)
        else:
            return self.compare(fitnessX.u,fitnessY.u)

    def fitness(self, genome, alpha, delta, method)-> Fitness:
        if (delta >0):
            items = self.instance.items
            B = self.instance.bound
            ew = genome.expected_weight(items)
            p = genome.profit(items)
            if ew < B :
                diff = B - ew
                k = genome.countItems()
                if(method == CHEBYSHEV):
                    v = max(chebyshev_v(k, diff, alpha, delta), 0)
                if(method == CHERNOFF):
                    v = max(chernoff_v(k, diff, alpha, delta),0)
                return Fitness(0, v, p)
            else:
                u = ew - B
                return Fitness(u,1,p)
        return []
