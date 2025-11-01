from SudokuGrid import SudokuGrid
from SudokuNode import SudokuNode
from solve import findSingleSolutionForSubtree

type Solution = list[int]
type CellIndex = list[int]

# SolveWalker hilft

"""
- sicherstellen dass grid in sync ist mit tree
- findet lösungen
- fügt lösungen im tree hinzu
- löscht Teil-lösungen aus dem grid
- Navigiert in knoten
- prüft knoten auf weitere
- check boundaries of tree
"""


class SolveWalker:

  def __init__(self, grid: SudokuGrid):

    self.grid = grid.copy()
    self.initialEmptyCellIndex = grid.getEmptyCellIndexes()
    self.cidSize = len(self.initialEmptyCellIndex)
    self.cidMaxLevel = self.cidSize - 1

  def getValueForLevel(self, level: int) -> int:

    idx = self.initialEmptyCellIndex[level]
    return self.grid(idx)

  def setValueForLevel(self, level: int, value: int) -> None:

    idx = self.initialEmptyCellIndex[level]
    self.grid.setLinear(idx, value)

  def discoverSolution(self, node: SudokuNode) -> Solution | None:
    """Find solution below given node

    Node must have set a value.

    No solution found:
      Returns None
      Grid has cells cleared below node level

    Solution found;:
      - Returns full solution list
      - Appends new cells to subtree
      - Grid has all cells solved


    """

    nodeValue = node.value

    if self.isLeafNode(node):
      return None

    else:
      currentLevel = node.emptyCellNum

      self.setValueForLevel(currentLevel, nodeValue)
      subEmptyCellIdx = self.eCidSubtree(currentLevel + 1)

      # check integrity of grid
      for i in subEmptyCellIdx:
        assert self.grid.getLinear(i) == 0
      for i in self.initialEmptyCellIndex[:currentLevel + 1]:
        assert self.grid.getLinear(i) != 0

      subSolution = findSingleSolutionForSubtree(subEmptyCellIdx, self.grid)

      if subSolution is None:
        # check if grid is clean
        gridEmptyCid = self.grid.getEmptyCellIndexes()
        assert gridEmptyCid == subEmptyCellIdx

        return None

      else:
        tmpNode = appendNodeChain(node, subSolution)

        # while True:
        #   pv = tmpNode.value
        #   ecn = tmpNode.emptyCellNum

        #   print("{}:{} - ".format(ecn, pv), end='')
        #   if ecn == 0:
        #     break
        #   tmpNode = tmpNode.parentNode

        leafNode = tmpNode
        assert self.isLeafNode(leafNode)  # cid equal maxCid
        fullSolution = self.returnCurrentFullSolution()
        return fullSolution

  def eCidSubtree(self, level: int) -> CellIndex:
    return self.initialEmptyCellIndex[level:]

  def isLeafNode(self, node: SudokuNode) -> bool:
    currLevel = node.emptyCellNum
    assert currLevel <= self.cidMaxLevel
    return currLevel == self.cidMaxLevel

  def returnCurrentFullSolution(self) -> Solution:
    numEmpty = len(self.grid.getEmptyCellIndexes())
    if numEmpty != 0:
      raise ValueError(
          "Grid has {} empty cells. Cant't provide full solution".format(numEmpty))
    else:
      solution = [self.grid.getLinear(i) for i in self.initialEmptyCellIndex]
      return solution


def appendNodeChain(startNode: SudokuNode, valueList: list[int]):

  node = startNode
  for v in valueList:
    nextNode = node.newChild(v)
    node = nextNode

  return node  # should be last node
