from SudokuGrid import SudokuGrid
import random

g = SudokuGrid()

# Create dict with keys=1..81 and empty set as value.
blacklist = {key: set() for key in range(0, 81)}

idx = 0

while (idx < 81):

    allowed = g.allowedValuesLinear(idx).difference(blacklist[idx])

    if len(allowed) == 0:

        # print("Es geht nicht weiter x {} y {}".format(x, y))

        # go a step back
        prevIdx = idx - 1
        numberToBlackList = g.getLinear(prevIdx)
        blacklist[prevIdx].add(numberToBlackList)
        blacklist[idx].clear()  # invalidate current blacklist
        g.clearLinear(prevIdx)
        idx = prevIdx

    else:
        value = random.choice(list(allowed))
        g.setLinear(idx, value)
        idx += 1

print(g.str())
