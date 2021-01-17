#python day_24.py < .\input\input24.txt

import sys
import functools

def readAllLines():
    return [line.rstrip() for line in sys.stdin]

BLACK = 0
WHITE = 1

class Hexboard:
    def __init__(self):
        self._origin = (0, 0)
        self._current = self._origin
        self._board = {self._origin : WHITE}
    @property
    def board(self):
        return self._board
    @board.setter
    def board(self, newBoard):
        self._board = newBoard
    def __flip(self):
        self._board[self._current] = BLACK if self._board[self._current] == WHITE else WHITE
    def __move(self, direction):
        row, col = self._current
        if   direction == 'nw':
            self._current = (row - 1, col)
        elif direction == 'ne':
            self._current = (row - 1, col + 1)
        elif direction == 'e':
            self._current = (row + 0, col + 1)
        elif direction == 'se':
            self._current = (row + 1, col + 0)
        elif direction == 'sw':
            self._current = (row + 1, col - 1)
        elif direction == 'w':
            self._current = (row + 0, col - 1)
        else:
            pass #should fail        
    def moves(self, directions):
        self._current = self._origin #current starts at reference tile
        for direction in directions:
            self.__move(direction)
        if self._current not in self._board: self._board.update({self._current : WHITE})
        self.__flip()        
    def __str__(self):
        s = 'current: {}\n'.format(self._current)
        s += str(self._board)
        s += '\n'
        return s
    def __repr__(self):
        return self.__str__()

def lineToMoves(line):
    i, N = 0, len(line)
    moves = []
    while i < N:
        if line[i] == 'n' or line[i] == 's':
            moves.append(line[i:i + 2])
            i += 2
        else:
            moves.append(line[i])
            i += 1
    return moves

def countColors(colors, targetColor):
    return functools.reduce(lambda acc, x: acc + (1 if x == targetColor else 0), colors, 0)

def adjacents(row, col):
    return [(row - 1, col), (row - 1, col + 1), (row + 0, col + 1), (row + 1, col + 0), (row + 1, col - 1), (row + 0, col - 1)]

def flip(board, row, col):
    current = board[row, col]
    adjs = [(board[row_, col_] if (row_, col_) in board else WHITE) for row_, col_ in adjacents(row, col)]
    blackTilesCounter = countColors(adjs, BLACK)
    #zero or more than 2 black tiles immediately adjacent to it is flipped to white.
    if current == BLACK and (blackTilesCounter == 0 or blackTilesCounter > 2):
        return WHITE
    #exactly 2 black tiles immediately adjacent to it is flipped to black.
    elif current == WHITE and blackTilesCounter == 2:
        return BLACK
    else:
        return board[row, col]

def expandBoard(board):
    temp = dict(board)
    for row, col in board:
        for row_, col_ in adjacents(row, col):
            if (row_, col_) not in temp:
                temp.update({(row_, col_) : WHITE})
    return temp

def day24_part1():
    hexboard = Hexboard()
    for line in readAllLines():
        hexboard.moves(lineToMoves(line))
    blackTilesCounter = countColors(hexboard.board.values(), BLACK)
    #DBG
    #print(hexboard)
    print(blackTilesCounter)

def day24_part2():
    hexboard = Hexboard()
    lines = readAllLines()
    for line in lines:
        hexboard.moves(lineToMoves(line))
    blackTilesCounter = 0
    for day in range(1, 100 + 1):
        hexboard.board = expandBoard(hexboard.board)
        newBoard = dict(hexboard.board)
        for (row, col) in hexboard.board:
            newBoard[row, col] = flip(hexboard.board, row, col)
        hexboard.board = newBoard
        blackTilesCounter = countColors(hexboard.board.values(), BLACK)
        #DBG
        #print("Day {}:".format(day), blackTilesCounter)
    print(blackTilesCounter)
    
if __name__ == "__main__":
    #day24_part1() #Your puzzle answer was 538.
    day24_part2() #Your puzzle answer was 4259.
