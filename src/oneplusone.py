from genome import Genome
from knapsack import Knapsack
from math import exp
from collections import namedtuple

CHEBYSHEV = 1
CHERNOFF = 2

Fitness = namedtuple('Fitness',['u','v','p'])


def run(instance:Knapsack, alpha, delta,fitness_evaluations, method)->int:
    genomeX = Genome(n = len(instance.items));
    fitnessX = fitness(genomeX, instance, alpha, delta, method)
    ##print("\ti:0|k:", genomeX.countItems(),'|e:',genomeX.expected_weight(instance.items), '|f:',fitnessX)
    
    i = 0
    j = 0
    while( i < fitness_evaluations ):
        i += 1
        genomeY = mutation(genomeX, instance.items)
        fitnessY = fitness(genomeY, instance, alpha, delta, method)
        if (selection(fitnessX,fitnessY)>0):
            print("\ti:",i,"|k:", genomeY.countItems(),'|e:',genomeY.expected_weight(instance.items), '|f:',fitnessY )
            genomeX = genomeY            
            fitnessX = fitnessY
    
    print("****\ti:",i,"|k:", genomeX.countItems(),'|e:',genomeX.expected_weight(instance.items), '|f:',fitnessX[2],"\n*****")
    return fitnessX[2]

def mutation(parent:Genome, items) :
    child = parent.offspring(items)
    return child;

def selection(fitnessX:Fitness, fitnessY:Fitness) -> int:
    if(fitnessX.u==fitnessY.u):
        if (fitnessX.v==fitnessY.v):
            return compare(fitnessY.p,fitnessX.p)
        else:
            return compare(fitnessX.v,fitnessY.v)
    else:
        return compare(fitnessX.u,fitnessY.u)

def fitness(genome, instance:Knapsack, alpha, delta, method)-> Fitness:
    if (delta >0):
        ew = genome.expected_weight(instance.items)
        p = genome.profit(instance.items)
        if ew < instance.bound :
            diff = instance.bound - ew
            k = genome.countItems()
            if(method == CHEBYSHEV):
                v = max(chebyshev_v(k, diff, alpha, delta), 0)
            if(method == CHERNOFF):
                v = max(chernoff_v(k, diff, alpha, delta),0)
            return Fitness(0, v, p)
        else:
            u = ew - instance.bound
            return Fitness(u,1,p)
    return []

# k = sum of x_i in solution X
# diff = B - Ew(X)
def chebyshev_v(k, diff, alpha, delta):
    if (delta >0):
        temp1 = k * ( delta ** 2 )
        temp2 = 3 * ( diff ** 2)
        temp = temp1 / (temp1 + temp2)
        return temp - alpha
    return -1

# k = sum of x_i in solution X
# diff = B - Ew(X)
# return the value by which the prob exceed alpha
def chernoff_v(k, diff, alpha, delta):
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
def compare(x,y) -> int:
    if x > y:
        return 1
    else:
        return -1
