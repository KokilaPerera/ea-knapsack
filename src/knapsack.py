from collections import namedtuple
from typing import List, Optional, Callable, Tuple

Item = namedtuple('Item',['index','profit','weight', 'expected_weight'])
gamma = 100

def load(file_path)-> List[Item]:
    f = open(file_path, "r")
    items = []
    n = 0
    B = []
    while n < 112:
        x = f.readline()
        if(n == 4):
            arr = x.split()            
            for i in range(3, len(arr)):
                B.append(int(arr[i]))
            #print("DEBUG LOG: ",x)# prints capacity of knapsack
        n += 1
    ITEMS = 100
    n = 0 
    while n < ITEMS:
        x = f.readline()
        items.append(createItem(x)) 
        n+=1
    bounds = calculateWeightBound(items, B)
    return [items,bounds]

def createItem(line) -> Item:
    x = line.split()
    item = Item(int(x[0]),int(x[1]),int(x[2]), int(x[2])+gamma)
    return item

def calculateWeightBound(items:[Item],b:[]) -> int:
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
