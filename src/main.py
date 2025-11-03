import random
import numpy as np
from datetime import datetime
from helpers import loadGridFromFile
from pathlib import Path
import argparse
from SudokuGrid import SudokuGrid
from solve import findAllSolutions2, findSingleSolutionForSubtree

# Parse command line arguments
# 3 modes:
#
# 1. No arguments: Create random fully filled grid
# 2. --emptycells <n>: Create random grid with n random cells left empty
# 3. --file <filename>: load grid from file, analyze and solve it
parser = argparse.ArgumentParser(description='Sudoku Solver')
parser.add_argument('--file', type=str,
                    help='Path to input file containing Sudoku grid')
parser.add_argument('--emptycells', type=int,
                    help='Number of empty cells to create in random grid (0-81). ( Has no effect with --file <f>)')
parser.add_argument('--maxcalculations', type=int, default=100, help='Limit search for solutions to maxcalculations (default: 100)')
parser.add_argument('--maxdisplay', type=int, default=10, help='Limit display of solutions to maxdisplay (default: 10)')
args = parser.parse_args()
print("")

# load grid from file or create empty grid
sparseGrid: SudokuGrid

if args.emptycells is not None:
  if args.emptycells < 0 or args.emptycells > 81:
    print("Error: --emptycells must be between 0 and 81")
    exit(1)

if args.file:
  sparseGrid = loadGridFromFile(args.file)
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
print("Empty cells: {}".format(len(sparseGrid.getEmptyCellIndexes())))
print("Solve ...")

solutions = findAllSolutions2(sparseGrid, int(args.maxcalculations))

print("Found {} solutions".format(len(solutions)))
if len(solutions) >= args.maxcalculations:
  print("There are more solutions than {}, but stopped calculating.".format(args.maxcalculations))
if len(solutions) > args.maxdisplay:
  print("Printing only first {}".format(args.maxdisplay))
for i, s in enumerate(solutions):
  print(list(s))
  if i == args.maxdisplay - 1:
    break

# save solution as csv
Path('out').mkdir(parents=True, exist_ok=True)
filename = datetime.today().strftime('out/%Y-%m-%d-%Hh%M%S.csv')

print("Sparse grid saved to file {}\n".format(filename))
np.savetxt(filename, sparseGrid.grid, delimiter=',', fmt='%d')
