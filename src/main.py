from Grid import Grid, linear2xy

g = Grid()

# add one element to each block

# dict: key int (linear index), value= list of blacklisted numbers
blacklist = {key: set() for key in range(0, 81)}

idx = 0

while (idx < 81):

    (x, y) = linear2xy(idx)
    allowed = g.allowedValuesXY(x, y).difference(blacklist[idx])
    if len(allowed) == 0:
        print(g.str())
        print("Es geht nicht weiter x {} y {}".format(x, y))

        # go a step back
        prevIdx = idx - 1
        numberToBlackList = g.getLinear(prevIdx)
        blacklist[prevIdx].add(numberToBlackList)
        blacklist[idx] = set()  # clear this blacklist
        g.clearLinear(prevIdx)
        idx = prevIdx

    else:
        value = next(iter(allowed))
        g.setXY(x, y, value)
        idx += 1

print(g.str())
