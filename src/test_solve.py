from helpers import loadGridFromFile
from solve import findAllSolutions


def test_findAllSolutions10():

  s10 = loadGridFromFile('Aufgaben/10-solutions.csv')
  solutions = findAllSolutions(s10)

  assert len(solutions) == 10


def test_findAllSolutions16():

  s16 = loadGridFromFile('Aufgaben/16-solutions.csv')
  solutions = findAllSolutions(s16)

  assert len(solutions) == 16
