from typing import Dict, Set, Union


# Leaf node is one with no children and proper emptyCellNum
# If parent is None we are root node
#
class SudokuNode:

  def __init__(self, parentNode: Union["SudokuNode", None], value: int, emptyCellNum: int) -> None:
    self._noSolutionValues: Set[int] = set()
    self.children: Dict[int, SudokuNode] = dict()
    self.emptyCellNum: int = emptyCellNum
    self.parentNode: SudokuNode | None = parentNode
    self.value: int = value

  def newChild(self, value: int) -> "SudokuNode":
    """Appends new child to node

    value is the value of the child

    """

    if value in self.children:
      raise RuntimeError(
          "Child with value {} already exists".format(value))
    else:
      newChildNode = SudokuNode(self, value, self.emptyCellNum + 1)
      self.children[value] = newChildNode
      return newChildNode

  def validChildValues(self) -> Set[int]:
    return set(self.children.keys())

  def noSolutionChildValues(self):
    return self._noSolutionValues

  def addNoSolutionChildValue(self, val: int):
    self._noSolutionValues.add(val)

  def checkedChildValues(self):
    return self.noSolutionChildValues().union(self.validChildValues())

  @classmethod
  def rootNode(cls, v):
    """Class method
    """
    return cls(None, v, 0)
