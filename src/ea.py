from genome import Genome
from knapsack import Knapsack
from math import exp

CHEBYSHEV = 1
CHERNOFF = 2

class EA:
    instance = None
    def __init__(self, instance:Knapsack):
        self.instance = instance

    def run(alpha, delta,fitness_evaluations, method)->int:
        pass

    def mutation(self, parent:Genome) :
        child = parent.offspring(self.instance.items)
        return child;

    # k = sum of x_i in solution X
    # diff = B - Ew(X)
    def chebyshev_v(self, k, diff, alpha, delta):
        if (delta >0):
            temp1 = k * ( delta ** 2 )
            temp2 = 3 * ( diff ** 2)
            temp = temp1 / (temp1 + temp2)
            return temp - alpha
        return -1

        # k = sum of x_i in solution X
    # diff = B - Ew(X)
    # return the value by which the prob exceed alpha
    def chernoff_v(self, k, diff, alpha, delta):
        if (delta > 0):
            if ( k == 0 ):
                return 0
            epsilon = diff / (k * delta)
            dividend = exp(epsilon)
            divisor = ( epsilon + 1) ** ( epsilon + 1 )

            temp = dividend / divisor
            temp = temp ** (k / 2)
            return temp - alpha
        return -1

    ## 'compare' takes 2 int parameters x and y
    ## return -1 if x is less than y
    ## otherwise return 1
    def compare(self,x,y) -> int:
        if x > y:
            return 1 ## 
        else:
            return -1
        
