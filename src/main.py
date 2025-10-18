from random import randint
# main

from Grid import Grid

g = Grid()

# add one element to each block

for bn in range(9):

    i = randint(0, 8)
    v = randint(0, 8)

    b = g.getElementsInBlock(bn)
    b[i] = v

print(g.str())
