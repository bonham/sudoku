from SudokuGrid import SudokuGrid, linear2xy, xy2linear, blockCoordsByBlockIndex, blockNumByXY, SudokuValueError, SudokuExistsError
import pytest


def test_setget():
    g = SudokuGrid(disableValueCheck=True)

    g.setLinear(1, 99)
    g.setLinear(10, 77)
    g.setLinear(17, 170)

    assert g.getLinear(1) == 99
    assert g.getLinear(10) == 77


def test_setLinear_getFlat():

    g = SudokuGrid(disableValueCheck=True)

    g.setLinear(10, 100)
    g.setLinear(11, 110)
    g.setLinear(17, 170)

    f = g.getFlatList()

    assert f[0:10].tolist() == [0] * 10
    assert f[10:12].tolist() == [100, 110]
    assert f[17].tolist() == 170
    assert f[18:81].tolist() == [0] * (81-18)


def test_getElementsInBlock():

    g = SudokuGrid(disableValueCheck=True)
    g.setLinear(10, 100)
    g.setLinear(11, 110)
    g.setLinear(17, 170)

    block0 = g.getBlock(0)

    assert block0[0, :].tolist() == [0] * 3
    assert block0[1, 0] == 0
    assert block0[1, 1] == 100
    assert block0[1, 2] == 110
    assert block0[2, :].tolist() == [0] * 3

    block2 = g.getBlock(2)
    assert block2[1, 2] == 170


def test_getElementsInCol():

    g = SudokuGrid(disableValueCheck=True)

    g.setLinear(10, 100)
    g.setLinear(11, 110)
    g.setLinear(17, 170)

    assert g.getCol(0).tolist() == [0] * 9
    assert g.getCol(1)[0:3].tolist() == [0, 100, 0]


def test_getElementsInRow():

    g = SudokuGrid(disableValueCheck=True)

    g.setLinear(10, 100)
    g.setLinear(11, 110)
    g.setLinear(17, 170)

    assert g.getRow(2).tolist() == [0] * 9
    assert g.getRow(1).tolist() == [0, 100, 110, 0, 0, 0, 0, 0, 170]


def test_linear2xy():

    assert linear2xy(0) == [0, 0]
    assert linear2xy(1) == [1, 0]
    assert linear2xy(8) == [8, 0]
    assert linear2xy(9) == [0, 1]
    assert linear2xy(10) == [1, 1]
    assert linear2xy(11) == [2, 1]
    assert linear2xy(17) == [8, 1]
    assert linear2xy(18) == [0, 2]
    assert linear2xy(80) == [8, 8]
    with pytest.raises(ValueError):
        linear2xy(81)


def test_xy2linear():

    assert xy2linear(8, 8) == 80
    assert xy2linear(0, 0) == 0
    assert xy2linear(1, 0) == 1
    assert xy2linear(8, 1) == 17


def test_blockCoordsByBlockIndex():

    assert blockCoordsByBlockIndex(0, 0) == [0, 1, 2, 9, 10, 11, 18, 19, 20]
    assert blockCoordsByBlockIndex(1, 0) == [3, 4, 5, 12, 13, 14, 21, 22, 23]
    assert blockCoordsByBlockIndex(
        0, 1) == [27, 28, 29, 36, 37, 38, 45, 46, 47]
    assert blockCoordsByBlockIndex(
        1, 1) == [30, 31, 32, 39, 40, 41, 48, 49, 50]


def test_getelementsinblocklinear():
    g = SudokuGrid()
    g.setLinear(10, 1)
    g.setLinear(11, 2)
    g.setLinear(17, 7)

    assert g.getElementInBlockLinear(0, 4) == 1
    assert g.getElementInBlockLinear(2, 5) == 7


def test_blockNumByXY():

    assert blockNumByXY(0, 0) == 0
    assert blockNumByXY(1, 0) == 0
    assert blockNumByXY(2, 0) == 0
    assert blockNumByXY(3, 0) == 1
    assert blockNumByXY(5, 0) == 1
    assert blockNumByXY(6, 0) == 2

    assert blockNumByXY(0, 1) == 0
    assert blockNumByXY(1, 1) == 0
    assert blockNumByXY(2, 1) == 0
    assert blockNumByXY(3, 1) == 1
    assert blockNumByXY(5, 1) == 1
    assert blockNumByXY(6, 1) == 2
    assert blockNumByXY(0, 2) == 0

    assert blockNumByXY(1, 2) == 0
    assert blockNumByXY(2, 2) == 0
    assert blockNumByXY(3, 2) == 1
    assert blockNumByXY(5, 2) == 1
    assert blockNumByXY(6, 2) == 2

    assert blockNumByXY(0, 3) == 3
    assert blockNumByXY(1, 3) == 3
    assert blockNumByXY(2, 3) == 3
    assert blockNumByXY(3, 3) == 4
    assert blockNumByXY(5, 3) == 4
    assert blockNumByXY(6, 3) == 5


def test_setxy():

    g = SudokuGrid()

    g.setXY(0, 0, 1)
    g.setXY(3, 0, 2)
    g.setXY(8, 0, 3)
    g.setXY(1, 1, 4)

    flat = g.getFlatList()[0:12]
    assert g.getFlatList()[0:11].tolist() == [
        1, 0, 0, 2, 0, 0, 0, 0, 3,
        0, 4
    ]


def test_allowedValuesxy():

    # 0 1 0 7
    # 2 ? 0 0 4
    # 0 0 0 9
    # 5 3 6

    # allowed for 1,1: 5,6,7,8,9

    g = SudokuGrid()

    g.setXY(1, 0, 1)
    g.setXY(3, 0, 7)

    g.setXY(0, 1, 2)
    g.setXY(4, 1, 4)

    g.setXY(3, 2, 9)
    g.setXY(0, 3, 5)
    g.setXY(1, 3, 3)
    g.setXY(2, 3, 6)

    assert g.allowedValuesXY(1, 1) == {5, 6, 7, 8, 9}
    assert g.allowedValuesXY(0, 4) == {1, 4, 7, 8, 9}

    with pytest.raises(SudokuValueError):
        g.setXY(0, 0, 7)

    with pytest.raises(SudokuValueError):
        g.setXY(0, 0, 2)

    with pytest.raises(SudokuValueError):
        g.setXY(0, 4, 6)

    with pytest.raises(SudokuExistsError):
        g.setXY(0, 3, 6)
