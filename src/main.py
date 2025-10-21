import random
import numpy as np
from datetime import datetime
from typing import Dict
from helpers import parseArgsAndLoadFile
from pathlib import Path


# load grid from file or create empty grid
grid = parseArgsAndLoadFile()

# obtain all cells not filled in.
emptyCellIndexes = grid.getEmptyCellIndexes()

# Prepare dict of emtpy sets to store blacklist values
#
# The keys are the indexes of the empty cells. The values are empty Sets.
#
# A 'blacklisted' value is added to a cell
# when the sudoku is not solvable for that value
blacklist: Dict = {emptyCellIndexes[key]: set()
                   for key in range(0, len(emptyCellIndexes))}

# Loop over empty cells
n = 0
while (n < len(emptyCellIndexes)):

    # check cell for allowed values
    idx = emptyCellIndexes[n]
    allowed = grid.allowedValuesLinear(idx).difference(blacklist[idx])

    # If there are no allowed values then this is a wrong path with no solution
    if len(allowed) == 0:

        # ### The value of the parent cell was a 'wrong' decision ###

        # go a step back and blacklist the value of the previous cell
        parentCell = emptyCellIndexes[n - 1]
        numberToBeBlackListed = grid.getLinear(parentCell)
        blacklist[parentCell].add(numberToBeBlackListed)

        # ### Reset current cell ###

        # clear blacklist of Current cell
        blacklist[idx].clear()
        # mark current cell as 'free'
        grid.clearLinear(parentCell)

        # Go one level up and repeat the search for the parent cell.
        n = n - 1

        # If we are already at the top then whole sudoku has no solution.
        if n < 0:
            print("\nThe Sudoku puzzle is not solvable\n")
            exit(0)

    else:
        value = random.choice(list(allowed))
        grid.setLinear(idx, value)
        n += 1

# print solution
print("\n"+grid.str())

# save solution as csv
Path('out').mkdir(parents=True, exist_ok=True)
filename = datetime.today().strftime('out/%Y-%m-%d-%Hh%M%S.csv')
print("\nOutput grid is in file {}\n".format(filename))
np.savetxt(filename, grid.grid, delimiter=',', fmt='%d')
