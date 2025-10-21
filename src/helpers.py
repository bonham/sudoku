import sys
from typing import Any
from SudokuGrid import SudokuGrid
import numpy as np


def emptyString2Zero(input: Any) -> int:
    if input == "":
        return 0
    else:
        return int(input)


def parseArgsAndLoadFile() -> SudokuGrid:

    if len(sys.argv) == 2:

        try:
            loadednp = np.loadtxt(
                sys.argv[1],
                dtype='i',
                delimiter=',',
                quotechar='"',
                converters=emptyString2Zero)

        except FileNotFoundError as e:
            print(f"Failed to load '{sys.argv[1]}': {e}")
            exit(1)
        else:
            grid = SudokuGrid(initGrid=loadednp)
            return grid

    elif len(sys.argv) == 1:

        grid = SudokuGrid()
        print("\nGenerating full sudoku from scratch")
        return grid

    else:
        print("""
Usage to generate a sudoku:

    main.py

Usage to solve partial sudoku

    main.py Aufgabe.csv

Note: The undefined cells need to have zero values

""")
    exit(1)
