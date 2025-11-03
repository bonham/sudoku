# Sudoku generator

Python code to create a valid sudoku from scratch or solve a given sudoku in csv format.

## Prerequisites

- Script was developed with Python 3.12 but might work with other versions too.
- Before running the script please install packages with `pip install -r requirements.txt`

## Usage

Generate a random full sudoku:

```
main.py
```

Generate a partial sudoku and solve it

```
main.py --emptycells 20
```

Load partial sudoku from csv file and solve it
```
main.py --file Aufgabe.csv
```

More arguments:
```
usage: main.py [-h] [--file FILE] [--emptycells EMPTYCELLS] [--maxcalculations MAXCALCULATIONS] [--maxdisplay MAXDISPLAY]

Sudoku Solver

options:
  -h, --help            show this help message and exit
  --file FILE           Path to input file containing Sudoku grid
  --emptycells EMPTYCELLS
                        Number of empty cells to create in random grid (0-81). ( Has no effect with --file <f>)
  --maxcalculations MAXCALCULATIONS
                        Limit search for solutions to maxcalculations (default: 100)
  --maxdisplay MAXDISPLAY
                        Limit display of solutions to maxdisplay (default: 10)
```

## csv input format:
Should be a 9 x 9 comma separated csv file with optional double quotes. Example: [Aufgabe1-quotes.csv](Aufgaben/Aufgabe1-quotes.csv) . The undefined cells need to have empty or values or zeros.

## example output
```
> python .\src\main.py  --emptycells 40


Sparse grid:
+-------+-------+-------+
| · · 9 | 2 4 · | 8 · 3 |
| · 3 · | · · 8 | · · · |
| 2 7 8 | · · · | 6 4 · |
+-------+-------+-------+
| 5 2 3 | · · 6 | 4 · 1 |
| · 9 · | · · · | 7 2 5 |
| 7 · 1 | · 2 5 | · · · |
+-------+-------+-------+
| 3 · 4 | · 6 · | · · · |
| 9 · · | · 5 3 | 1 6 4 |
| 1 6 7 | 4 · · | 5 3 · |
+-------+-------+-------+
Empty cells: 40
Solve ...
Found 2 solutions
[6, 1, 7, 5, 4, 5, 6, 9, 2, 1, 7, 5, 3, 1, 9, 8, 7, 9, 8, 6, 3, 1, 4, 4, 9, 3, 8, 6, 5, 1, 2, 9, 7, 8, 8, 2, 7, 8, 9, 2]
[6, 1, 7, 5, 4, 5, 6, 9, 2, 1, 7, 5, 3, 1, 9, 9, 7, 8, 8, 6, 3, 1, 4, 4, 8, 3, 9, 6, 5, 1, 2, 9, 7, 8, 8, 2, 7, 8, 9, 2]
```