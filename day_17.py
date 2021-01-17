#python day_17.py < .\input\input17.txt

import sys
import functools

ACTIVE = '#'
INACTIVE = '.'

def readAllLines():
    return [line.rstrip() for line in sys.stdin]

def countIf(xs, target):
    return functools.reduce(lambda acc, x: acc + (1 if x == target else 0), xs, 0)

def getNeighborsCubes(cubes, x, y, z, X, Y, Z):
    def neighborsGenerator():
        for z_ in range(z - 1, z + 1 + 1):
            for y_ in range(y - 1, y + 1 + 1):
                for x_ in range(x - 1, x + 1 + 1):
                    if (0 <= x_ < X and 0 <= y_ < Y and 0 <= z_ < Z) and not (x_ == x and y_ == y and z_ == z):
                        yield (x_, y_, z_)
    return list(neighborsGenerator())

def countActivesCubes(cubes):
    acc = 0
    Y, Z = len(cubes[0]), len(cubes)
    for z_ in range(0, Z):
        for y_ in range(0, Y):
            acc = acc + countIf(cubes[z_][y_], ACTIVE)
    return acc

def computeActivationCubes(cubes, x, y, z):
    X, Y, Z = len(cubes[0][0]), len(cubes[0]), len(cubes)
    ns = [cubes[z_][y_][x_] for (x_, y_, z_) in getNeighborsCubes(cubes, x, y, z, X, Y, Z)]
    neighbors = countIf(ns, ACTIVE)
    me = cubes[z][y][x]
    if me == ACTIVE:
        return ACTIVE if neighbors == 2 or neighbors == 3 else INACTIVE
    elif me == INACTIVE:
        return ACTIVE if neighbors == 3 else INACTIVE
    else:
        pass #should fail

def cloneCubes(cubes):
    Y, Z = len(cubes[0]), len(cubes)
    return [[cubes[z_][y_] for y_ in range(0, Y)] for z_ in range(0, Z)]

def updateCubes(cubes):
    zs = cloneCubes(cubes)
    X, Y, Z = len(zs[0][0]), len(zs[0]), len(zs)
    for z_ in range(0, Z):
        for y_ in range(0, Y):
            activation = [computeActivationCubes(cubes, x_, y_, z_) for x_ in range(0, X)]
            zs[z_][y_] = ''.join(activation)
    return zs

def expandCubes(cubes):
    X, Y, Z = len(cubes[0][0]), len(cubes[0]), len(cubes)
    zs = []
    for z_ in range(0, Z):
        ys = ['.' * (X + 2)]
        for y_ in range(0, Y):
            ys.append('.{}.'.format(cubes[z_][y_]))
        ys.append('.' * (X + 2))
        zs.append(ys)
    side = zs[0]
    frontSide, backSide = side, side
    zs = [frontSide] + zs + [backSide]
    return zs

def initCubes(X, Y, middleLayer = None):
    side = ['.' * X] * Y
    cubes = [side, middleLayer if middleLayer != None else side, side]
    return cubes

def getNeighborsHypercubes(hypercubes, x, y, z, w, X, Y, Z, W):
    def neighborsGenerator():
        for w_ in range(w - 1, w + 1 + 1):
            for z_ in range(z - 1, z + 1 + 1):
                for y_ in range(y - 1, y + 1 + 1):
                    for x_ in range(x - 1, x + 1 + 1):
                        if (0 <= x_ < X and 0 <= y_ < Y and 0 <= z_ < Z and 0 <= w_ < W) and not (x_ == x and y_ == y and z_ == z and w_ == w):
                            yield (x_, y_, z_, w_)
    return list(neighborsGenerator())

def countActivesHypercubes(hypercubes):
    acc = 0
    Y, Z, W = len(hypercubes[0][0]), len(hypercubes[0]), len(hypercubes)
    for w_ in range(0, W):
        for z_ in range(0, Z):
            for y_ in range(0, Y):
                acc = acc + countIf(hypercubes[w_][z_][y_], ACTIVE)
    return acc

def computeActivationHypercubes(hypercubes, x, y, z, w):
    X, Y, Z, W = len(hypercubes[0][0][0]), len(hypercubes[0][0]), len(hypercubes[0]), len(hypercubes)
    ns = [hypercubes[w_][z_][y_][x_] for (x_, y_, z_, w_) in getNeighborsHypercubes(hypercubes, x, y, z, w, X, Y, Z, W)]
    neighbors = countIf(ns, ACTIVE)
    me = hypercubes[w][z][y][x]
    if me == ACTIVE:
        return ACTIVE if neighbors == 2 or neighbors == 3 else INACTIVE
    elif me == INACTIVE:
        return ACTIVE if neighbors == 3 else INACTIVE
    else:
        pass #should fail

def cloneHypercubes(hypercubes):
    Y, Z, W = len(hypercubes[0][0]), len(hypercubes[0]), len(hypercubes)
    return [[[hypercubes[w_][z_][y_] for y_ in range(0, Y)] for z_ in range(0, Z)] for w_ in range(0, W)]

def updateHypercubes(hypercubes):
    ws = cloneHypercubes(hypercubes)
    X, Y, Z, W = len(ws[0][0][0]), len(ws[0][0]), len(ws[0]), len(ws)
    for w_ in range(0, W):
        for z_ in range(0, Z):
            for y_ in range(0, Y):
                activation = [computeActivationHypercubes(hypercubes, x_, y_, z_, w_) for x_ in range(0, X)]
                ws[w_][z_][y_] = ''.join(activation)
    return ws

def expandHypercubes(hypercubes):
    W = len(hypercubes)
    ws = [expandCubes(hypercubes[w_]) for w_ in range(0, W)]
    side = ws[0]
    frontSide, backSide = side, side
    ws = [frontSide] + ws + [backSide]
    return ws

def initHypercubes(X, Y, middleLayer = None):
    hypercubes = [initCubes(X, Y), initCubes(X, Y, middleLayer), initCubes(X, Y)]
    return hypercubes

def printCubes(cubes, i):
    X, Y, Z = len(cubes[0][0]), len(cubes[0]), len(cubes)
    print(i, 'Cube dimensions:', 'X:', X, 'Y:', Y, 'Z:', Z)
    for z_ in range(0, Z):
        for y_ in range(0, Y):
            print(cubes[z_][y_], sep = '', end = '')
            print()
        print()

def printHypercubes(hypercubes, i):
    X, Y, Z, W = len(hypercubes[0][0][0]), len(hypercubes[0][0]), len(hypercubes[0]), len(hypercubes)
    print(i, 'Hypercube dimensions:', 'X:', X, 'Y:', Y, 'Z:', Z, 'W:', W)
    for w_ in range(0, W):
        for z_ in range(0, Z):
            for y_ in range(0, Y):
                print(hypercubes[w_][z_][y_], sep = '', end = '')
                print()
            print()
        print('=' * X)
        print()

def day17_part1():    
    lines = readAllLines()
    X, Y = len(lines[0]), len(lines)
    cubes = initCubes(X, Y, lines)
    for i in range(1, 6 + 1):
        cubes = updateCubes(expandCubes(cubes))
        #DBG
        #printCubes(cubes, i)
    numberOfActives = countActivesCubes(cubes)
    print(numberOfActives)

def day17_part2():
    lines = readAllLines()
    X, Y = len(lines[0]), len(lines)
    hypercubes = initHypercubes(X, Y, lines)
    for i in range(1, 6 + 1):
        hypercubes = updateHypercubes(expandHypercubes(hypercubes))
        #DBG
        #printHypercubes(hypercubes, i)
    numberOfActives = countActivesHypercubes(hypercubes)
    print(numberOfActives)

if __name__ == "__main__":
    day17_part1() #Your puzzle answer was 313.
    #day17_part2() #Your puzzle answer was 2640.
