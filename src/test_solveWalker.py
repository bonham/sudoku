from SolveWalker import SolveWalker
from SudokuGrid import SudokuGrid
from SudokuNode import SudokuNode


def test_something():

  grid = SudokuGrid()

  sw = SolveWalker(grid)
  rootNodeVal = 7  # random
  root = SudokuNode.rootNode(rootNodeVal)
  grid.setLinear(0, rootNodeVal)

  solution = sw.discoverSolution(root)
  assert solution is not None
  assert len(solution) == 81
