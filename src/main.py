import random
import numpy as np
from datetime import datetime
from typing import Dict
from helpers import loadFileFromGrid
from pathlib import Path
import argparse
from SudokuGrid import SudokuGrid
from solve import solve, findSingleSolutionForSubtree, solveFromNode

# Parse command line arguments
# 3 modes:
#
# 1. No arguments: Create random fully filled grid
# 2. --emptycells <n>: Create random grid with n random cells left empty
# 3. --file <filename>: load grid from file, analyze and solve it
parser = argparse.ArgumentParser(description='Sudoku Solver')
parser.add_argument('--file', type=str,
                    help='Path to input file containing Sudoku grid')
parser.add_argument('--emptycells', type=int, choices=range(0, 82),
                    help='Number of empty cells to create in random grid (0-81)')
args = parser.parse_args()
print("")

# load grid from file or create empty grid
sparseGrid: SudokuGrid

if args.file:
  sparseGrid = loadFileFromGrid(args.file)
  print("From file:\n"+sparseGrid.str())
else:
  tmpGrid = SudokuGrid()
  emptyCellIndexes = tmpGrid.getEmptyCellIndexes()  # all
  sol = findSingleSolutionForSubtree(emptyCellIndexes, tmpGrid)
  tmpFullGrid = tmpGrid

  if args.emptycells is None:
    print("Random full grid:\n"+tmpFullGrid.str())
    exit(0)

  else:
    # remove cells to create sparse grid
    sparseGrid = tmpFullGrid.copy()
    cellIndexes = sparseGrid.getFilledCellIndexes()
    random.shuffle(cellIndexes)
    for i in range(0, args.emptycells):
      sparseGrid.clearLinear(cellIndexes[i])

print("\nSparse grid:\n"+sparseGrid.str())

print("Solve ...")
solve(sparseGrid)

# save solution as csv
# Path('out').mkdir(parents=True, exist_ok=True)
# filename = datetime.today().strftime('out/%Y-%m-%d-%Hh%M%S.csv')

# print("\nSolved grid saved to file {}\n".format(filename))
# np.savetxt(filename, solvedGrid.grid, delimiter=',', fmt='%d')
