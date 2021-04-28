from genome import Genome
from knapsack import Knapsack
from math import exp
from collections import namedtuple
from random import random
from ea import EA

CHEBYSHEV = 1
CHERNOFF = 2

Fitness = namedtuple('Fitness',['g1','g2'])

class GSEMO(EA):

    def __int__(self, problem:Knapsack, probability_method:int):
        super().__init__(instance)

    def run(self, alpha, delta,fitness_evaluations, method)->int:
        items = self.instance.items
        genomeX = Genome(n = len(items));
        fitnessX = self.fitness(genomeX, alpha, delta, method)
        ##print("\ti:0|k:", genomeX.countItems(),'|e:',genomeX.expected_weight(instance.items), '|f:',fitnessX)
        S = [genomeX]
        f_S = {genomeX:fitnessX}
        
        i = 0
        j = 0
        while( i < fitness_evaluations ):

            i += 1

            ## select x randomly from S
            randIndex = int(random() *len(S))
            x = S[randIndex]
            
            genomeY = self.mutation(x)
            fitnessY = self.fitness(genomeY, alpha, delta, method)
            count = 0
            for genomeX in S:
                fitnessX = f_S[genomeX]
                select_val = self.selection(fitnessX,fitnessY)
                if (select_val > -1):
                    count += 1                    
                    S.remove(genomeX)
                    rem = f_S.pop(genomeX)
                    if(select_val > 0):
                        print(i, "\tAdded ", fitnessY, " - ", genomeY )
                    
            if count > 0:
                flag = False
                S.append(genomeY)
                f_S[genomeY] = fitnessY
        
        print("****\t:",genomeX)
        return genomeX.profit(items)

    ## returns a +ve value if Y is better otherwise a -ve value
    def selection(self, fitnessX:Fitness, fitnessY:Fitness) -> int:
        if( fitnessY.g1 == fitnessX.g1 and  fitnessY.g2 == fitnessX.g2 ):
            return 0
        if( fitnessY.g1 < fitnessX.g1 or  fitnessY.g2 > fitnessX.g2 ):
            return -1
        else:
            return 1

    def fitness(self, genome, alpha, delta, method)-> Fitness:
        if (delta >0):
            items = self.instance.items
            diff = self.instance.bound - genome.expected_weight(items) 
            k = genome.countItems()

            g2_value = self.g2(k, diff,delta, method)

            if g2_value > alpha :
                g1_value = -1
            else:
                g1_value = genome.profit(items)
            return Fitness(g1_value, g2_value)
        return []

    #diff = B - ew
    def g2(self, k, diff, delta, method) -> int:
        if(0<diff):
            if(method == CHEBYSHEV):
                return self.chebyshev_v(k, diff, 0, delta)
            if(method == CHERNOFF):
                return self.chernoff_v(k, diff, 0, delta)
        else:
            return 1 - diff ## 1 + ( ew - B )
            
