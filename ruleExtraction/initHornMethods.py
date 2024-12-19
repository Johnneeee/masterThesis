import numpy as np
from itertools import combinations
from hornAlgorithm import *
from intepretor import *

def define_variables(number):
    s = "".join(['v'+str(i)+',' for i in range(number)])
    V = [e for e in symbols(s)]
    return V

def generateBackground(V, attLengths):
    # two values from the same attrutube dimention cant be true simultaneously
    splitIndexes = []
    i = 0
    for x in attLengths:
        i += x
        splitIndexes.append(i)
    splitted = np.split(V, splitIndexes)
    background = set()

    for x in splitted:
        background.update(set(combinations(x, 2)))

    background = set(map(lambda x: ~(x[0] & x[1]),background))
    return background