from SolveWalker import SolveWalker
from SudokuGrid import SudokuGrid
from SudokuNode import SudokuNode
# from helpers import loadGridFromFile


def test_empty():

  grid = SudokuGrid()

  sw = SolveWalker(grid)
  rootNodeVal = 7  # random
  firstlevelNode = SudokuNode(None, 7, 0)
  grid.setLinear(0, rootNodeVal)

  nodeStack = []

  solution = sw.discoverSolution(firstlevelNode, nodeStack)
  assert solution is not None
  assert len(solution) == 81
  assert len(nodeStack) == 80


def test_supernode():

  grid = SudokuGrid()
  superNode = SudokuNode.superNode()
  sw = SolveWalker(grid)

  nodeStack = []

  solution = sw.discoverSolution(superNode, nodeStack)
  assert solution is not None
  assert len(solution) == 81
  assert len(nodeStack) == 81
