from SudokuGrid import SudokuGrid
import random
import numpy as np
from datetime import datetime
import sys
from typing import Any, Dict


def emptyString2Zero(input: Any) -> int:
    if input == "":
        return 0
    else:
        return int(input)


# global
grid = None

if len(sys.argv) == 2:

    try:
        loadednp = np.loadtxt(
            sys.argv[1], dtype='i', delimiter=',', converters=emptyString2Zero)
    except FileNotFoundError as e:
        print(f"Failed to load '{sys.argv[1]}': {e}")
        exit(1)
    else:
        grid = SudokuGrid(initGrid=loadednp)

elif len(sys.argv) == 1:
    grid = SudokuGrid()
    print("\nGenerating full sudoku from scratch")
else:
    print("""
Usage to generate a sudoku:

    main.py

Usage to solve partial sudoku

    main.py Aufgabe.csv

Note: The undefined cells need to have zero values

""")
    exit(1)


####
# check which cells are zero
emptyCellIndexes = grid.getEmptyCellIndexes()

# Prepare dict of emtpy sets to store blacklisted values
blacklist: Dict = {emptyCellIndexes[key]: set()
                   for key in range(0, len(emptyCellIndexes))}

# Loop over indexes of elements with zeroes
i = 0
while (i < len(emptyCellIndexes)):
    idx = emptyCellIndexes[i]
    allowed = grid.allowedValuesLinear(idx).difference(blacklist[idx])

    if len(allowed) == 0:

        # print("Es geht nicht weiter x {} y {}".format(x, y))

        # go a step back
        prevIdx = emptyCellIndexes[i - 1]

        numberToBeBlackListed = grid.getLinear(prevIdx)
        blacklist[prevIdx].add(numberToBeBlackListed)
        blacklist[idx].clear()  # invalidate current blacklist
        grid.clearLinear(prevIdx)

        i = i - 1

    else:
        value = random.choice(list(allowed))
        grid.setLinear(idx, value)
        i += 1

print("\n"+grid.str())
filename = datetime.today().strftime('out/%Y-%m-%d-%Hh%M%S.csv')
print("\nOutput grid is in file {}\n".format(filename))
np.savetxt(filename, grid.grid, delimiter=',', fmt='%d')
