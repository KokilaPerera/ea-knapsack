from collections import namedtuple
from typing import List, Optional, Callable, Tuple

Item = namedtuple('Item',['index','profit','weight', 'expected_weight'])
gamma = 100

class Knapsack:
    label = ""
    items = List[Item]
    bound = -1
    n = 0
    def __init__(self, items:List[Item]= None,b = 0, label = ""):
        self.n = len(items)
        self.items = items
        self.bound = b
        self.label = label

    def __str__(self):
        return self.label + " instance with bound " + str(self.bound)

def load(file_path, label = "")-> List['Knapsack']:
    f = open(file_path, "r")
    B = loadWeights(f)
    items = loadItems(f)
    res = []
    B = adjustWeightBound(items, B, gamma)
    for b in B:
        res.append(Knapsack(items, b, label))
    return res

def loadWeights(file):
    n = 0
    B = []
    while n < 112:
        x = file.readline()
        if(n == 4):
            arr = x.split()
            for i in range(3, len(arr)):
                B.append(int(arr[i]))
        n += 1
    print("Default weight limit(s) : ", B)
    option = input("\tUse default (1) or override (2) ? ")
    if int(option) == 2:
        options = input("\tEnter space seperated values : ")
        arr = options.split()
        B1 = []
        for opt in arr:
            B1.append(int(opt))
        return B1
    return B
            
def loadItems(file):
    ITEMS = 100
    n = 0
    items = []
    while n < ITEMS:
        x = file.readline()
        items.append(createItem(x)) 
        n+=1
    return items

def createItem(line) -> Item:
    x = line.split()
    item = Item(int(x[0]),int(x[1]),int(x[2]), int(x[2])+gamma)
    return item

def adjustWeightBound(items:[Item],b:[], gamma) -> int:
    sorted_items = items.copy();
    sorted_items.sort(key = sortKey)
    temp = 0
    k = 0
    updatedBounds = []
    for bound in b:
        
        while(temp<=bound):
            temp += sorted_items[k].weight
            k += 1
        bound = bound + ((k-1)*gamma)
        updatedBounds.append ( bound )
    return updatedBounds

def sortKey(item)->int:
    return item.weight
