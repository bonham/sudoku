import sys
from typing import Any
from SudokuGrid import SudokuGrid
import numpy as np


def emptyString2Zero(input: Any) -> int:
  if input == "":
    return 0
  else:
    return int(input)


def loadGridFromFile(filePath) -> SudokuGrid:

  try:
    loadednp = np.loadtxt(
        filePath,
        dtype='i',
        delimiter=',',
        quotechar='"',
        converters=emptyString2Zero)

  except (FileNotFoundError, ValueError) as e:
    print(f"Failed to load '{sys.argv[1]}': {e}")
    exit(1)

  else:
    # ensure loadednp is a 2D array with shape 9x9
    if (
        not hasattr(loadednp, "shape")
        or loadednp.ndim != 2
        or loadednp.shape != (9, 9)
    ):
      print(
          "Loaded grid from "
          f"'{sys.argv[1]}' does not have shape 9x9 "
          f"(got {getattr(loadednp, 'shape', None)})"
      )
      exit(1)

    grid = SudokuGrid(initGrid=loadednp)
    return grid
