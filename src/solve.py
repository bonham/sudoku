from SudokuGrid import SudokuGrid
from SudokuNode import SudokuNode
from SolveWalker import SolveWalker
from typing import Dict
import random

type Solution = list[int]
type Solutions = list[Solution]


def findAllSolutions2(grid: SudokuGrid) -> Solutions:

  solutions: Solutions = []
  sw = SolveWalker(grid)
  rootNode = SudokuNode.superNode()

  solutions = solveFromNode2(rootNode, sw, solutions)

  print("Found {} solutions".format(len(solutions)))

  for s in solutions:
    print(list(s))

  return solutions


# The startNode is a node being part of a successful solution
# The values of the successful solution on this node are in 'node.validValues()'
# The values which have no solution downwards are stored in 'node.noSolutionValues()'
#
# solveFromNode will determine if there are possible solutions below the node and picks a value v
# it checks for actual solution for v
# if no solution found we will blacklist v in noSolutionValues.
# if a solution found we add a chain of child nodes representing the found solution.
# The solution is also added to 'solutions' list.
def solveFromNode2(startNode: SudokuNode, sw: SolveWalker, solutions: Solutions) -> Solutions:

  nodeStack: list[SudokuNode] = [startNode]

  while nodeStack:

    node = nodeStack.pop(0)

    # set grid values
    sw.prepareGridValuesFromNode(node)

    # nothing to do for a leaf node
    if sw.isLeafNode(node):
      continue

    # check if values are possible
    cValueOpts = sw.possibleChildValuesForNode(node)

    if len(cValueOpts) == 0:

      if node.isRootNode():

        continue  # TODO: or return??

      else:
        # nothing to be done
        continue

    else:
      # there are options
      childValueToCheck = min(cValueOpts)

      # set grid values
      sw.prepareGridValuesFromNode(node)

      solution = sw.discoverSolution(
          node, childValueToCheck, nodeStack)  # modifies stack

      if solution is None:
        node.addNoSolutionChildValue(childValueToCheck)
        sw.prepareGridValuesFromNode(node)
        if sw.possibleChildValuesForNode(node):
          nodeStack.insert(0, node)

      else:
        # yeah - solution found
        # grid is fully populated
        # stack has new values
        solutions.append(solution)
        sw.prepareGridValuesFromNode(node)
        if sw.possibleChildValuesForNode(node):
          nodeStack.insert(0, node)

  return solutions


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
