from SudokuGrid import SudokuGrid
import random

grid = SudokuGrid()

# Prepare dict of emtpy sets to store blacklisted values
blacklist = {key: set() for key in range(0, 81)}

# Loop over each element
idx = 0
while (idx < 81):

    allowed = grid.allowedValuesLinear(idx).difference(blacklist[idx])

    if len(allowed) == 0:

        # print("Es geht nicht weiter x {} y {}".format(x, y))

        # go a step back
        prevIdx = idx - 1

        numberToBeBlackListed = grid.getLinear(prevIdx)
        blacklist[prevIdx].add(numberToBeBlackListed)
        blacklist[idx].clear()  # invalidate current blacklist
        grid.clearLinear(prevIdx)
        idx = prevIdx

    else:
        value = random.choice(list(allowed))
        grid.setLinear(idx, value)
        idx += 1

print(grid.str())
