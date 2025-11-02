from SolveWalker import SolveWalker
from SudokuGrid import SudokuGrid
from SudokuNode import SudokuNode
from helpers import loadGridFromFile


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


def test_prepareGridValuesFromNode():

  grid = loadGridFromFile("Aufgaben/10-solutions.csv")
  # has 47 zeros
  eclen = 47
  initialEci = grid.getEmptyCellIndexes()
  assert len(initialEci) == eclen

  firstPartOfSolution = [9, 2, 8, 7, 5, 4, 4, 6, 1, 5]  # 10

  # build tree
  tmpNode = SudokuNode.superNode()
  for v in firstPartOfSolution:
    child = tmpNode.newChild(v)
    tmpNode = child

  leaf = child

  sw = SolveWalker(grid)

  sw.prepareGridValuesFromNode(leaf)

  assert sw.grid.getEmptyCellIndexes() == initialEci[10:]
  assert (len(sw.grid.getEmptyCellIndexes())
          == eclen - len(firstPartOfSolution))


def test_possibleValuesForNode():

  grid = loadGridFromFile("Aufgaben/2-solutions.csv")

  """
  20 empty cells
  2 solutions

  Solution vectors:

  [9, 3, 6, 7, 8, 9, 7, 4, 9, 7, 4, 7, 1, 3, 8, 6, 3, 8, 6, 9]
  [9, 3, 8, 7, 6, 9, 7, 4, 9, 7, 4, 7, 1, 3, 8, 6, 3, 6, 8, 9]
  """
  sw = SolveWalker(grid)

  rootNode = SudokuNode.superNode()
  child0 = rootNode.newChild(9)
  child1 = child0.newChild(3)

  sw.prepareGridValuesFromNode(child1)
  values = sw.possibleChildValuesForNode(child1)
  assert set(values) == set([6, 8])

  child1.newChild(6)
  values2 = sw.possibleChildValuesForNode(child1)

  assert values2 == set([8])
