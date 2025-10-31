from typing import Dict, Set, Union


# Leaf node is one with no children and proper emptyCellNum
# If parent is None we are root node
#
class SudokuNode:
  def __init__(self, parentNode: Union["SudokuNode", None], parentNodeValue: int, emptyCellNum: int) -> None:
    self._noSolutionValues: Set[int] = set()
    self.children: Dict[int, SudokuNode] = dict()
    self.emptyCellNum: int = emptyCellNum
    self.parentNode: SudokuNode | None = parentNode
    self.parentNodeValue: int = parentNodeValue

  def newChild(self, value: int) -> "SudokuNode":

    if value in self.children:
      raise RuntimeError(
          "Child with value {} already exists".format(value))
    else:
      newChildNode = SudokuNode(self, value, self.emptyCellNum + 1)
      self.children[value] = newChildNode
      return newChildNode

  def validValues(self) -> Set[int]:
    return set(self.children.keys())

  def noSolutionValues(self):
    return self._noSolutionValues

  def addNoSolutionValue(self, val: int):
    self._noSolutionValues.add(val)

  def checkedValues(self):
    return self.noSolutionValues().union(self.validValues())
