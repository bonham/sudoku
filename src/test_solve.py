from helpers import loadGridFromFile
from solve import findAllSolutions, findAllSolutions2


def test_findAllSolutions10():

  s10 = loadGridFromFile('Aufgaben/10-solutions.csv')
  solutions = findAllSolutions(s10)

  assert len(solutions) == 10


def test_findAllSolutions16():

  s16 = loadGridFromFile('Aufgaben/16-solutions.csv')
  solutions = findAllSolutions(s16)

  assert len(solutions) == 16


def test_find2sol2():

  s2 = loadGridFromFile('Aufgaben/2-solutions.csv')
  solutions = findAllSolutions2(s2)
  assert len(solutions) == 2


def test_find2sol10():

  s2 = loadGridFromFile('Aufgaben/10-solutions.csv')
  solutions = findAllSolutions2(s2)
  assert len(solutions) == 10


def test_find2sol16():

  s2 = loadGridFromFile('Aufgaben/16-solutions.csv')
  solutions = findAllSolutions2(s2)
  assert len(solutions) == 16
