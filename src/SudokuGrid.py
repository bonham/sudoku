import numpy as np


class SudokuGrid:

    def __init__(
            self,
            disableValueCheck=False,
            initGrid: np.ndarray | None = None):

        self.disableValueCheck = disableValueCheck

        if isinstance(initGrid, np.ndarray):
            if initGrid.shape == (9, 9):
                self.grid = initGrid
            else:
                print(
                    "Grid is not in 9x9 format, but {}".format(
                        initGrid.shape
                    )
                )
                exit(1)
        else:
            self.grid = np.zeros((9, 9), dtype='i')

        self.flat = self.grid.reshape(81)

        self.blocks = [
            self.grid[i:i+3, j:j+3]
            for i in range(0, 9, 3)
            for j in range(0, 9, 3)
        ]

    def copy(self):
        newGrid = SudokuGrid(
            disableValueCheck=self.disableValueCheck,
            initGrid=np.copy(self.grid)
        )
        return newGrid

    def getLinear(self, i):
        return self.flat[i]

    def setLinear(self, i, v):

        # prevent setting a value if it is not zero
        if self.getLinear(i) != 0:
            raise SudokuExistsError

        allowed = self.allowedValuesLinear(i)

        if (v in allowed) or self.disableValueCheck:
            self.flat[i] = v
        else:
            raise SudokuValueError

    def getXY(self, x, y):
        return self.grid[y, x]

    def setXY(self, x, y, v):

        # prevent setting a value if it is not zero
        if self.getXY(x, y) != 0:
            raise SudokuExistsError

        allowed = self.allowedValuesXY(x, y)

        if (v in allowed) or self.disableValueCheck:
            self.grid[y, x] = v
        else:
            raise SudokuValueError

    def getBlock(self, bNum):
        return self.blocks[bNum]

    def allowedValuesXY(self, ix, iy):

        blockNum = blockNumByXY(ix, iy)
        blockSet = set(self.getBlock(blockNum).flatten().tolist())

        rowSet = set(self.getRow(iy).tolist())
        colSet = set(self.getCol(ix).tolist())

        numbersInGrid = blockSet.union(rowSet, colSet)

        onetonine = set(range(1, 10))  # 1..9

        return onetonine.difference(numbersInGrid)

    def allowedValuesLinear(self, i):
        (x, y) = linear2xy(i)
        return self.allowedValuesXY(x, y)

    def getRow(self, rowIndex):
        return self.grid[rowIndex, :]

    # Col is all elements with fixed x
    def getCol(self, colIndex):
        return self.grid[:, colIndex]

    # return string representation for printing
    def str(self):
        out = ""
        for index, line in enumerate(self.grid):

            # replace zero with dot for better visibility
            # Use the Unicode middle dot character (U+00B7)
            lineList = ["·" if x == 0 else x for x in line.tolist()]

            if index % 3 == 0:
                out += "+-------+-------+-------+\n"

            t = "| {} {} {} | {} {} {} | {} {} {} |\n".format(*lineList)
            out += t

        out += "+-------+-------+-------+\n"
        return out

    def clearLinear(self, i):
        self.flat[i] = 0

    def getEmptyCellIndexes(self):
        return np.asarray(self.flat == 0).nonzero()[0].tolist()

    def getFilledCellIndexes(self):
        return np.asarray(self.flat != 0).nonzero()[0].tolist()
    # - - - - - - - - -                                - -
    # Below methods are not needed for simple sudoku solver

    def getFlatList(self):
        return self.flat

    def getElementInBlockLinear(self, bNum, elementNum):

        return self.getBlock(bNum)[elementNum//3, elementNum % 3]

    def setElementInBlockLinear(self, bNum, elementNum, value):

        self.getBlock(bNum)[elementNum//3, elementNum % 3] = value


def linear2xy(linearIndex) -> list[int]:

    if (linearIndex >= 81 or linearIndex < 0):
        raise ValueError

    x = linearIndex % 9
    y = linearIndex // 9

    return [x, y]


def xy2linear(x, y):

    if (x > 8 or y > 8 or x < 0 or y < 0):
        raise ValueError

    return y * 9 + x


def blockCoordsByBlockIndex(bx, by):

    r = []

    for y in range(3):

        for x in range(3):

            n = bx * 3 + x + y * 9 + by * 9 * 3
            r.append(n)

    return r


def blockNumByXY(x, y):
    # Note: args are xy - grid index is yx
    bx = x // 3
    by = y // 3
    r = by * 3 + bx
    return r


class SudokuValueError(ValueError):
    pass


class SudokuExistsError(SudokuValueError):
    pass
