#python day_11.py < .\input\input11.txt

import sys
import functools
import itertools

def readAllLines():
    return [line.rstrip() for line in sys.stdin]

def adjacentsOf(grid, x, y):
    H, W = len(grid), len(grid[0])
    leftOk = x - 1 >= 0
    rightOk = x + 1 < W
    upOk = y - 1 >= 0
    downOk = y + 1 < H
    adjs = []
    if leftOk:
        adjs.append(grid[y][x - 1]) #left
        if upOk: 
            adjs.append(grid[y - 1][x - 1]) #up left
        if downOk: 
            adjs.append(grid[y + 1][x - 1]) #down left
    if rightOk:
        adjs.append(grid[y][x + 1]) #right
        if upOk:
            adjs.append(grid[y - 1][x + 1]) #up right
        if downOk:        
            adjs.append(grid[y + 1][x + 1]) #down right
    if upOk:
        adjs.append(grid[y - 1][x]) #up
    if downOk:
        adjs.append(grid[y + 1][x]) #down
    return adjs

def leftWalk(grid, x, y):
    for x_ in range(x - 1, -1, -1):
        if grid[y][x_] != '.':
            return grid[y][x_]
    return '.'

def upLeftWalk(grid, x, y):
    for (y_, x_) in zip(range(y - 1, -1, -1), range(x - 1, -1, -1)):
        if grid[y_][x_] != '.':
            return grid[y_][x_]
    return '.'

def downLeftWalk(grid, x, y):
    H = len(grid)
    for (y_, x_) in zip(range(y + 1, H), range(x - 1, -1, -1)):
        if grid[y_][x_] != '.':
            return grid[y_][x_]
    return '.'

def rightWalk(grid, x, y):
    W = len(grid[0])
    for x_ in range(x + 1, W):
        if grid[y][x_] != '.':
            return grid[y][x_]
    return '.'

def upRightWalk(grid, x, y):
    W = len(grid[0])
    for (y_, x_) in zip(range(y - 1, -1, -1), range(x + 1, W)):
        if grid[y_][x_] != '.':
            return grid[y_][x_]
    return '.'

def downRightWalk(grid, x, y):
    H, W = len(grid), len(grid[0])
    for (y_, x_) in zip(range(y + 1, H), range(x + 1, W)):
        if grid[y_][x_] != '.':
            return grid[y_][x_]
    return '.'

def upWalk(grid, x, y):
    for y_ in range(y - 1, -1, -1):
        if grid[y_][x] != '.':
            return grid[y_][x]
    return '.'

def downWalk(grid, x, y):
    H = len(grid)
    for y_ in range(y + 1, H):
        if grid[y_][x] != '.':
            return grid[y_][x]
    return '.'

def firstSeatsOf(grid, x, y):
    return [leftWalk(grid, x, y), upLeftWalk(grid, x, y), downLeftWalk(grid, x, y), rightWalk(grid, x, y), 
            upRightWalk(grid, x, y), downRightWalk(grid, x, y), upWalk(grid, x, y), downWalk(grid, x, y)]

def becomesOccupied(seat, adjacents):
    return seat == 'L' and all([adj != '#' for adj in adjacents])

def becomesEmpty(seat, adjacents, atLeastOccupied):
    return seat == '#' and sum([1 if adj == '#' else 0 for adj in adjacents]) >= atLeastOccupied

def areGridsEqual(grid, otherGrid):
    H, W = len(grid), len(grid[0])
    for y in range(H):
        for x in range(W):
            if grid[y][x] != otherGrid[y][x]:
                return False
    return True

def flatmap(f, xs):
    return itertools.chain.from_iterable(map(f, xs))

def identity():
    return lambda x: x

def countIf(xs, target):
    return functools.reduce(lambda acc, x: acc + (1 if x == target else 0), xs, 0)

def printGrid(grid):
    for y in range(len(grid)):
        print(grid[y])
    print()

def getNextSeat(seat, adjs, toBecomesEmpty):
    if becomesOccupied(seat, adjs):
        return '#'
    elif becomesEmpty(seat, adjs, toBecomesEmpty):
        return 'L'
    else:
        return seat

def countOccupiedSeats(seatsOf, toBecomesEmpty):
    grid = readAllLines()
    H, W = len(grid), len(grid[0])
    #DBG
    #printGrid(grid)
    while True:
        newGrid = [''.join([getNextSeat(grid[y][x], seatsOf(grid, x, y), toBecomesEmpty) for x in range(W)]) for y in range(H)]
        #DBG
        #printGrid(newGrid)
        if areGridsEqual(grid, newGrid):
            break
        else:
            grid = newGrid
    flattenedGrid = list(flatmap(identity(), grid))
    return countIf(flattenedGrid, '#')

def day11_part1():
    occupiedCounter = countOccupiedSeats(adjacentsOf, 4)
    print(occupiedCounter)

def day11_part2():
    occupiedCounter = countOccupiedSeats(firstSeatsOf, 5)
    print(occupiedCounter)

if __name__ == "__main__":
    #day11_part1() #Your puzzle answer was 2453.
    day11_part2() #Your puzzle answer was 2159.
