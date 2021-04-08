from genome import Genome
from math import exp
from random import randint, uniform
from collections import namedtuple

CHEBYSHEV = 1
CHERNOFF = 2

GENOME_X = 0
GENOME_Y = 1


Fitness = namedtuple('Fitness',['u','v','p'])

def run(items, b, alpha, delta,method)->[int,int]:
    genomeX = Genome(n = len(items));
    fitnessX = fitness(genomeX, items, b,alpha, delta, method)
    i = 0
    j = 0
    while( i < 100000 ):
        genomeY = mutation(genomeX, items)
        fitnessY = fitness(genomeY,items, b, alpha, delta, method)
        if (selection(fitnessX,fitnessY)==GENOME_Y):
            #print("\ti:",i,"k:", genomeY.countItems(),'|e:',genomeY.expected_weight(items), '|f:',fitnessY )
            genomeX = genomeY            
            fitnessX = fitnessY
        i += 1
    
    #print(i,"k:", genomeX.countItems(),"\te:",genomeX.expected_weight(items),"\tp:",fitnessX[2])
    return fitnessX[2]

def mutation(parent:Genome, items) :
    child = parent.offspring(items)
    return child;

def selection(fitnessX:Fitness, fitnessY:Fitness) -> int:
    if(fitnessX.u==fitnessY.u):
        if (fitnessX.v==fitnessY.v):
            return selectMin_x_y(fitnessY.p,fitnessX.p)
        else:
            return selectMin_x_y(fitnessX.v,fitnessY.v)
    else:
        return selectMin_x_y(fitnessX.u,fitnessY.u)

#single objective
def fitness(genome, items, b, alpha, delta, method)-> Fitness:  
    
    if (delta >0):
        ew = genome.expected_weight(items)
        p = genome.profit(items)
        if ew < b :
            u = 0
            diff = b - ew
            k = genome.countItems()
            if(method == CHEBYSHEV):
                v = chebyshev_v(k, diff, alpha, delta)                
            if(method == CHERNOFF):
                v = chernoff_v(k, diff, alpha, delta)
        else:
            u = ew - b
            v = 1 ## v = 1 - alpha
        return Fitness(u,v,p)
    return []

# k = sum of x_i in solution X
# diff = B - Ew(X)
def chebyshev_v(k, diff, alpha, delta):
    if (delta >0):
        temp1 = k * ( delta ** 2 )
        temp2 = 3 * ( diff ** 2)
        temp1 = temp1 / (temp1 + temp2)
        if(temp1 < alpha):
            return 0
        return temp1 - alpha
    return -1

# k = sum of x_i in solution X
# diff = B - Ew(X)
# return the value by which the prob exceed alpha
def chernoff_v(k, diff, alpha, delta):
    if (delta > 0):        
        epsilon = diff / (k * delta)            
        dividend = exp(epsilon)
        epsilon += 1
        divisor = epsilon ** epsilon
        
        temp = dividend / divisor
##        exponent = k / 2
##        if(temp > alpha or exponent < 0.5):
##            temp = temp ** exponent
##            if temp > alpha:
##                return temp - alpha
        if temp > alpha:
            return temp - alpha
        return 0
    return -1

def selectMin_x_y(x,y) -> int:
    if x > y:
        return GENOME_Y
    else:
        return GENOME_X
