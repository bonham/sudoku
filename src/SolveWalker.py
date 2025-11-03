from SudokuGrid import SudokuGrid
from SudokuNode import SudokuNode
import random
from typing import Dict


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

  def getIndexForLevel(self, level: int) -> int:
    return self.initialEmptyCellIndex[level]

  def getValueForLevel(self, level: int) -> int:

    idx = self.initialEmptyCellIndex[level]
    return self.grid(idx)

  def setValueForLevel(self, level: int, value: int, override=False) -> None:

    idx = self.initialEmptyCellIndex[level]
    self.grid.setLinear(idx, value, override)

  def clearValueForLevel(self, level: int) -> None:

    idx = self.initialEmptyCellIndex[level]
    self.grid.clearLinear(idx)

  def setValueFromNode(self, node: SudokuNode) -> None:
    level = node.emptyCellNum
    value = node.value
    self.setValueForLevel(level, value)

  def clearValueFromNode(self, node: SudokuNode) -> None:
    level = node.emptyCellNum
    idx = self.getIndexForLevel(level)
    self.grid.clearLinear(idx)

  def discoverSolution(self, node: SudokuNode, childValue: int, nodeStack: list[SudokuNode]) -> Solution | None:
    """Find solution below given node

    Node must have set a value. (except if node is root node)

    No solution found:
      Returns None
      Grid has cells cleared below node level

    Solution found;:
      - Returns full solution list
      - Appends new cells to subtree
      - Grid has all cells solved
      - Node list added to stack
    """

#    nodeValue = node.value

    if self.isLeafNode(node):
      return None

    else:
      currentLevel = node.emptyCellNum
      childLevel = currentLevel + 1  # could be leaf
      self.setValueForLevel(childLevel, childValue)

      subSolution: None | list[int]

      if childLevel == self.cidMaxLevel:
        subSolution = [childValue]

      else:
        subEmptyCellIdx = self.splitEmptyCellIndex(childLevel+1)[1]
        subSolution = findSingleSolutionForSubtree(subEmptyCellIdx, self.grid)

      if subSolution is None:
        # check if grid is clean
        gridEmptyCid = self.grid.getEmptyCellIndexes()
        assert gridEmptyCid == subEmptyCellIdx

        self.clearValueForLevel(childLevel)
        return None

      else:
        childNode = node.newChild(childValue)

        nodeListAppended = appendNodeChain(childNode, subSolution)
        nodeListAppended.append(childNode)

        leafNode = nodeListAppended[0]
        assert self.isLeafNode(leafNode)  # cid equal maxCid

        # prepend nodeList to stack
        nodeStack[:0] = nodeListAppended

        fullSolution = self.returnCurrentFullSolution()
        self.clearValueForLevel(childLevel)  # need something better
        return fullSolution

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

  def splitEmptyCellIndex(self, level: int) -> tuple[CellIndex, CellIndex]:
    """Splits empty cell index into two

    Returns tuple with first tuple being empty cell index
    from 0 to level - 1
    and second tuple being cell index
    from level to len - 1"""

    if level == -1:
      raise ValueError("Level needs to be >= 0")
    else:
      # this is also correct for level == 0
      return (
          self.initialEmptyCellIndex[0:level],
          self.initialEmptyCellIndex[level:],
      )

  def checkZeroesFromLevel(self, level: int) -> None:
    """Check grid zero / nonzero valules

    All values from level and below should be zero.
    All values up to level - 1 should be nonzero"""

    (topEmptyCellIndex, subEmptyCellIdx) = self.splitEmptyCellIndex(level)

    # check integrity of grid
    for i in subEmptyCellIdx:
      val = self.grid.getLinear(i)
      if val != 0:
        raise RuntimeError(
            "Cell {} has value {} but should be 0".format(i, val))
    for i in topEmptyCellIndex:
      val = self.grid.getLinear(i)
      if val == 0:
        raise RuntimeError(
            "Cell {} has value {} but should be >0".format(i, val))

  def prepareGridValuesFromNode(self, node: SudokuNode) -> None:
    """Set grid zero, nonzero values based on node

    Level is determined from node.

    All values below node should be zero.
    All values from 0 to up to level should be nonzero, filled with solution from tree.
    """
    topValues: list[int] = []
    valueNode = node
    splitLevel = node.emptyCellNum

    while valueNode.emptyCellNum >= 0:  # skip root node
      topValues.insert(0, valueNode.value)
      if (valueNode.parentNode is None):
        raise RuntimeError("Should not happen")
      valueNode = valueNode.parentNode
    assert len(topValues) == splitLevel + 1

    # first write zeros everywhere, but from end of grid
    for lev in range(self.cidMaxLevel, -1, -1):
      self.clearValueForLevel(lev)

    # now write values but from top
    for lev in range(0, splitLevel+1):
      self.setValueForLevel(lev, topValues[lev], True)

  def possibleChildValuesForNode(self, parentNode: SudokuNode) -> list[int]:
    """Returns possible values for a child of a given node

    Take into account from parent
    - noSolutionChildValue
    - validChildSolutionValues

    and

    grid.allowedValues()
    from next lower level

    It is recommended to run prepareGridValuesFromNode on parent first"""

    if self.isLeafNode(parentNode):
      raise RuntimeError("Calling this function is not allowed for leaf nodes")

    nextLevel = parentNode.emptyCellNum + 1  # <= maxLevel

    nextLevelIdx = self.getIndexForLevel(nextLevel)
    gridOpts = self.grid.allowedValuesLinear(nextLevelIdx)

    return gridOpts.difference(parentNode.checkedChildValues())


def appendNodeChain(startNode: SudokuNode, valueList: list[int]) -> list[SudokuNode]:
  """Appends a chain of children (a branch) to a node

  Node values are taken from valueList

  The appended nodes are returned as a list. Deepest levels first"""

  nodeList: list[SudokuNode] = []

  node = startNode
  for v in valueList:
    nextNode = node.newChild(v)
    nodeList.insert(0, nextNode)  # lowest node should be first in list
    node = nextNode

  return nodeList  # should be last node


def findSingleSolutionForSubtree(emptyCellIndexes: list[int], grid: SudokuGrid) -> list[int] | None:
  """Finds a single solution

  Manipulates the grid

  Solution found:
  - grid is filled with solution

  Solution not found:
  - grid is returned as before - with all cells cleared corresponding to emptyCellIndexes

  The function does not know about partial or full solution and what was initial empty cell index
  It always returns solution of same size as emptyCellIndex ( could be sub - solution )
  """
  # print("\n+++++++++++++++")
  blacklist: Dict = {emptyCellIndexes[key]: set()
                     for key in range(0, len(emptyCellIndexes))}

  # emptyCellIndexes is partial ( see above )
  n = 0
  while (n < len(emptyCellIndexes)):
    # print("+++ level {}".format(n))

    # check cell for allowed values
    idx = emptyCellIndexes[n]
    allowed = grid.allowedValuesLinear(idx).difference(blacklist[idx])

    # If there are no allowed values then this is a wrong path with no solution
    if len(allowed) == 0:

      # if this happens at top level then we are done
      if n == 0:
        # print("++ No solution")
        grid.clearLinear(idx)
        return None

      else:
        # We are not at the top level, but the value of the parent cell was a 'wrong' decision #
        # go a step back and blacklist the value of the previous cell
        parentCell = emptyCellIndexes[n - 1]
        numberToBeBlackListed = grid.getLinear(parentCell)
        blacklist[parentCell].add(numberToBeBlackListed)
        # print("+++ Blacklist {} in level {}".format(numberToBeBlackListed, n - 1))
        # ### Reset current cell ###
        # clear blacklist of Current cell
        blacklist[idx].clear()
        # mark current cell as 'free'
        grid.clearLinear(parentCell)

        # Go one level up and repeat the search for the parent cell.
        n = n - 1

    else:
      # there are still options
      value = random.choice(list(allowed))
      grid.setLinear(idx, value)
      n += 1

  # end of while block - we have a solution
  solution = [grid.getLinear(i) for i in emptyCellIndexes]
  return solution
