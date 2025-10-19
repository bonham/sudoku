from random import randint
import numpy as np
# main

from Grid import Grid

g = Grid()

# add one element to each block

for bn in range(9):

    i = randint(0, 8)
    v = randint(0, 8)

    g.setElementInBlockLinear(bn, i, v)

print(g.str())
