import numpy as np


class Grid:

    def __init__(self):

        self.grid = np.zeros((9, 9), dtype='i')
        self.flat = self.grid.reshape(81)

        self.blocks = []
        for blockNumber in range(9):

            blockRowIdx = blockNumber // 3
            blockColIdx = blockNumber % 3

            block = self.grid[blockRowIdx:blockRowIdx +
                              3, blockColIdx:blockColIdx+3]
            self.blocks.append(block)

    # Index from 0 to 80

    def setLinear(self, i, v):
        self.flat[i] = v

    def setYX(self, y, x, v):
        self.grid[y, x] = v

    def getLinear(self, i):
        return self.flat[i]

    def getFlatList(self):
        return self.flat

    # bNum = 0..8
    def getElementsInBlock(self, bNum):
        return self.blocks[bNum].reshape(9)

    # Row is all elements with fixed y
    def getRow(self, rowIndex):

        return self.grid[rowIndex, :]

    # Col is all elements with fixed x
    def getCol(self, colIndex):

        return self.grid[:, colIndex]

    def str(self):

        return np.array2string(self.grid)


def linear2xy(l):

    if (l >= 81 or l < 0):
        raise ValueError

    x = l % 9
    y = l // 9

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
