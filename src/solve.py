from SudokuGrid import SudokuGrid
from SudokuNode import SudokuNode
from typing import Dict, List
import random


def findAllSolutions(grid: SudokuGrid) -> list[list[int]]:

  # savedsolutions
  solutions: List[List[int]] = []
  initialEmptyCellIndexes = grid.getEmptyCellIndexes()
  rootNode = SudokuNode(None, -1, 0)
  solutions = solveFromNode(rootNode, grid, initialEmptyCellIndexes, solutions)

  print("Found {} solutions".format(len(solutions)))

  for s in solutions:
    print(list(s))

  return (solutions)


# Grid will be changed in place

# nodes?
# - nodes are only created on successful solution


# The startNode is a node with one or multiple successful solutions ( rootNode might be exception )
# The values of the successful solution on this node are in 'node.validValues()'
# The values which have no solution downwards are stored in 'node.noSolutionValues()'
#
# solveFromNode will check the following: for a given value 'v' for startNode - we check if below there is any solution
# if not we will blacklist v in noSolutionValues.
# if yes we add a chain of child nodes representing the found solution.
def solveFromNode(currentNode: "SudokuNode", grid: SudokuGrid, initialEmptyCellIndexes: list[int], solutions: List[List[int]]) -> List[List[int]]:

  currEmptyCN = currentNode.emptyCellNum
  # check allowed values and pick start value
  checkedValues = currentNode.checkedValues()
  sIdx = initialEmptyCellIndexes[currEmptyCN]
  assert grid.getLinear(sIdx) == 0

  allowedValues = grid.allowedValuesLinear(
      sIdx).difference(checkedValues)

  print("{}-{} ".format(currEmptyCN, len(allowedValues)), end='')
  if len(allowedValues) == 0:
    # nothing left to do here
    # print("-- No more solutions in level {}. Already having {}. Going up".format(
    #    currentNode.emptyCellNum, len(currentNode.validValues())))

    # check for root node
    if currentNode.parentNode is None:
      print("-- Done")
      return solutions

    # Just an assertion
    parentNode = currentNode.parentNode
    if parentNode is None:
      raise RuntimeError("Parent Node None should not happen here")

    idx = initialEmptyCellIndexes[parentNode.emptyCellNum]
    grid.clearLinear(idx)
    # not root node -> go up
    return solveFromNode(parentNode, grid, initialEmptyCellIndexes, solutions)

  else:
    # we have at least one additional value
    # startAllowedValues > 0
    # if random TODO
    valueToCheck = min(allowedValues)
    grid.setLinear(sIdx, valueToCheck)

    # start one level below - here we do not have a node yet ?

    emptyCellNumBelow = \
        currentNode.emptyCellNum + 1  # 0..len(initialEmptyCellIndexes)

    # if we are already in leaf node then skip finding solution for subtree
    if emptyCellNumBelow == len(initialEmptyCellIndexes) - 1:

      grid.clearLinear(sIdx)
      partialEmptyCellIndexes = initialEmptyCellIndexes[emptyCellNumBelow:]
      subSolution1 = findSingleSolutionForSubtree(
          partialEmptyCellIndexes, grid)
      if subSolution1 is None:
        raise RuntimeError("No no")
      else:
        realSolution1 = [grid.getLinear(i) for i in initialEmptyCellIndexes]
        solutions.append(realSolution1)
      currentNode.newChild(valueToCheck)
      return solveFromNode(currentNode, grid, initialEmptyCellIndexes, solutions)

    # Not in leaf
    else:

      partialEmptyCellIndexes = initialEmptyCellIndexes[emptyCellNumBelow:]
      subSolution2 = findSingleSolutionForSubtree(
          partialEmptyCellIndexes, grid)

      if subSolution2 is None:
        grid.clearLinear(sIdx)
        currentNode.addNoSolutionValue(valueToCheck)
        # we need to try again on same level because there could be more options
        return solveFromNode(currentNode, grid, initialEmptyCellIndexes, solutions)

      else:
        # determine solution
        realSolution2 = [grid.getLinear(i) for i in initialEmptyCellIndexes]
        solutions.append(realSolution2)

        # append child chain + add solution
        tmpNode = currentNode
        for i in range(currentNode.emptyCellNum, len(initialEmptyCellIndexes)):
          idx = initialEmptyCellIndexes[i]
          v = grid.getLinear(idx)
          tmpNode = tmpNode.newChild(v)

        lastNode = tmpNode
        assert lastNode.emptyCellNum == len(
            initialEmptyCellIndexes)  # ??? TODO

        # leave grid unchanged

        # return solve from lowest end -last node is one too low
        nextNode = lastNode.parentNode
        if nextNode is None:
          raise RuntimeError("Next node is none - why")

        grid.clearLinear(initialEmptyCellIndexes[nextNode.emptyCellNum])
        return solveFromNode(nextNode, grid, initialEmptyCellIndexes, solutions)


def findSingleSolutionForSubtree(emptyCellIndexes: list[int], grid: SudokuGrid) -> list[int] | None:
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
