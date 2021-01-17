#python day_20.py < .\input\input20.txt

import sys
import math
import functools
import itertools

def readAllLines():
    return [line.rstrip() for line in sys.stdin]

TOP, RIGHT, DOWN, LEFT = 0, 1, 2, 3

def flip(rows):
    isString = isinstance(rows[0], str)

    if isString:
        rows = [list(row) for row in rows] 

    for i in range(len(rows)):
        rows[i] = rows[i][::-1] #reverse

    if isString:
        rows = [''.join(row) for row in rows]

    return rows

def rotateSquare(rows):
    #rotate 90 degrees clockwise
    i, j, k, l = 0, len(rows[0]), 0, len(rows)
    assert j == l, "Number of columns must be the same number of rows"

    isString = isinstance(rows[0], str)

    if isString:
        rows = [list(row) for row in rows]
    
    while i < j:
        for c in range(i, j - 1):
            rows[k + l - 1 - c][i], rows[k][c] = rows[k][c], rows[k + l - 1 - c][i]
        for r in range(k + 1, l):
            rows[r][i], rows[l - 1][r] = rows[l - 1][r], rows[r][i]
        for c in range(i + 1, j):
            rows[l - 1][c], rows[k + l - 1 - c][j - 1] = rows[k + l - 1 - c][j - 1], rows[l - 1][c]
        i = i + 1
        j = j - 1
        k = k + 1
        l = l - 1
    
    if isString:
        rows = [''.join(row) for row in rows]
    
    return rows

class Tile:
    def __init__(self, id, rows):
        self._id = id
        self._rows = rows
        self._borders = self.__computeBorders(rows)
    def flip(self):
        self._rows = flip(self._rows)
        self._borders = self.__computeBorders(self._rows)
    def rotate(self):
        self._rows = rotateSquare(self._rows)
        self._borders = self.__computeBorders(self._rows)
    def deepcopy(self):
        return Tile(self._id, self._rows)
    def __borderToInt(self, xs):
        return int(''.join(['1' if x == '#' else '0' for x in xs]), 2)
    def __computeBorders(self, rows):
        #clockwise: TOP, RIGHT, DOWN, LEFT
        return [self.__borderToInt(rows[0]),
                self.__borderToInt([row[len(row) - 1] for row in rows]),
                self.__borderToInt(rows[len(rows) - 1]),
                self.__borderToInt([row[0] for row in rows])]
    @property
    def id(self):
        return self._id
    @property
    def rows(self):
        return self._rows
    @property
    def borders(self):
        return self._borders
    def __str__(self):
        return "Tile: {}".format(self._id)    
    def __repr__(self):
        return self.__str__()

def flipAll(tiles):
    for tile in tiles:
        tile.flip()

def rotateAll(tiles):
    for tile in tiles:
        tile.rotate()

def indexToRowCol(i, N):
    #square dimension N * N
    row, col = int(i / N), int(i % N)
    return (row, col)

def rowColToIndex(row, col, N):
    #square dimension N * N
    return row * N + col

def printRows(rows):
        print(''.join([(row + '\n') for row in rows]), sep = '')

def testRotate():
    a = ['ABC', 'DEF', 'GHI']
    b = ['ABCD', 'EFGH', 'IJKL', 'MNOP']
    c = ['ABCDE', 'FGHIJ', 'KLMNO', 'PQRST', 'UVXYZ']
    d = ['AB', 'DE']
    for x in [a, b, c, d]:
        print('before:') 
        printRows(x)
        print('after:')
        printRows(rotateSquare(x))

def findSquareArrangementRec(tiles, acc, N):
    def generateTransitions(tile):
        #9 transitions - flips and rotations until the original source
        yield tile
        tile.flip()
        yield tile
        for _ in range(3):
            tile.flip()
            tile.rotate()
            yield tile
            tile.flip()
            yield tile
        tile.flip()
        tile.rotate()
        yield tile
    if tiles == []:
        return (True, acc)
    for i, t in enumerate(tiles):
        t = t.deepcopy()
        it = generateTransitions(t)
        for _ in range(8):
            t = next(it)
            if acc == []:
                acc.append(t)
                result = findSquareArrangementRec(tiles[:i] + tiles[i + 1:], acc, N)
                if result[0]:
                    return result
                else:
                    acc.pop()
            else:
                match = []
                row, col = indexToRowCol(len(acc), N)
                #top
                if (0 <= row - 1 < N and 0 <= col < N):
                    j = rowColToIndex(row - 1, col, N)
                    t_ = acc[j]
                    match.append(t.borders[TOP] == t_.borders[DOWN])
                #right
                if (0 <= row < N and 0 <= col + 1 < N):
                    j = rowColToIndex(row, col + 1, N)
                    if (j < len(acc)):
                        t_ = acc[j]
                        match.append(t.borders[RIGHT] == t_.borders[LEFT])
                #down
                if (0 <= row + 1 < N and 0 <= col < N):
                    j = rowColToIndex(row + 1, col, N)
                    if (j < len(acc)):
                        t_ = acc[j]
                        match.append(t.borders[DOWN] == t_.borders[TOP])
                #left
                if (0 <= row < N and 0 <= col - 1 < N):
                    j = rowColToIndex(row, col - 1, N)
                    t_ = acc[j]
                    match.append(t.borders[LEFT] == t_.borders[RIGHT])
                if (all(match)):
                    acc.append(t)
                    result = findSquareArrangementRec(tiles[:i] + tiles[i + 1:], acc, N)
                    if result[0]:
                        return result
                    else:
                        acc.pop()
        #t = next(it) #don't need, because it was cloned and will be discarded
    return (False, acc)

def findSquareArrangement(tiles):
    return findSquareArrangementRec(tiles, [], int(math.sqrt(len(tiles))))

def flatmap(f, xs):
    return itertools.chain.from_iterable(map(f, xs))

def identity():
    return lambda x: x

def countIf(xs, target):
    return functools.reduce(lambda acc, x: acc + (1 if x == target else 0), xs, 0)

def readTiles():
    lines = readAllLines()
    i = 0
    tiles = []
    while lines != []:
        t = lines[i:i+12]
        lines = lines[i+12:]
        id = int(t[0].split(' ')[1][:-1])
        rows = t[1:-1]
        tiles.append(Tile(id, rows))
    return tiles

def cutBordersAndJoin(tiles):
    rows = [[row[1:-1] for row in tile.rows[1:-1]] for tile in tiles]
    N, M = int(math.sqrt(len(tiles))), len(rows[0])
    temp = []
    for row in range(N):
        for j in range(M):
            line = ''.join([rows[rowColToIndex(row, col, N)][j] for col in range(N)])
            temp.append(line)
    return temp

def findSeaMonsters(rows):
    def generateTransitions(rows):
        #9 transitions - flips and rotations until the original source
        yield rows
        rows = flip(rows)
        yield rows
        for _ in range(3):
            rows = flip(rows)
            rows = rotateSquare(rows)
            yield rows
            rows = flip(rows)
            yield rows
        rows = flip(rows)
        rows = rotateSquare(rows)
        yield rows
    def internalFindSeaMonsters(rows):
        #find in a square matrix
        N = len(rows)
        assert len(rows[0]) == N, "Number of columns must be the same number of rows"
        seaMonsterPattern = ["                  # ",
                             "#    ##    ##    ###",
                             " #  #  #  #  #  #   "]
        H, W = len(seaMonsterPattern), len(seaMonsterPattern[0])
        #scanning the pattern - to improve scanning, just jump pattern width if there is a match
        coords = []
        for i in range(N - H):
            for j in range(N - W):
                for k in range(H):
                    match = False
                    for l in range(W):
                        if seaMonsterPattern[k][l] == '#':
                            match = rows[i + k][j + l] == seaMonsterPattern[k][l]
                            if not match:
                                break
                    if not match:
                        break
                if match:
                    coords.append((i, j))
        return coords
    it = generateTransitions(rows)
    for i in range(8):
        rows = next(it)
        coords = internalFindSeaMonsters(rows)
        if len(coords) > 0:
            return (coords, rows)
    return ([], rows)

def day20_part1():
    _, tiles = findSquareArrangement(readTiles())
    N = int(math.sqrt(len(tiles)))
    corners = [tiles[rowColToIndex(0, 0, N)], tiles[rowColToIndex(0, N - 1, N)], 
               tiles[rowColToIndex(N - 1, 0, N)], tiles[rowColToIndex(N - 1, N - 1, N)]]
    #DBG
    #print(corners)
    cornersMul = functools.reduce(lambda acc, t: acc * t.id, corners, 1)
    print(cornersMul)

def day20_part2():
    _, tiles = findSquareArrangement(readTiles())
    rows = cutBordersAndJoin(tiles)
    coords, rows = findSeaMonsters(rows)
    #DBG
    #printRows(rows)
    #print(coords)
    flattenedGrid = list(flatmap(identity(), rows))
    notPartOfSeaMonsters = countIf(flattenedGrid, '#') - len(coords) * 15
    print(notPartOfSeaMonsters)

if __name__ == "__main__":
    #day20_part1() #Your puzzle answer was 19955159604613.
    day20_part2() #Your puzzle answer was 1639.
