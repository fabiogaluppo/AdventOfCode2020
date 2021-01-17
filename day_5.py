#python day_5.py < .\input\input5.txt

import sys
import math

def readAllLines():
    return [line.rstrip() for line in sys.stdin]

def F(t):
    return (t[0], math.floor(t[0] + (t[1] - t[0]) / 2))

def L(t):
    return F(t)

def B(t):
    return (math.ceil(t[0] + (t[1] - t[0]) / 2), t[1])

def R(t):
    return B(t)

def computeSeatId(s):
    a = (0, 127)
    for ch in s[:7]:
        if ch == 'F':
            a = F(a)
        else: #'B'
            a = B(a)
    b = (0, 7)
    for ch in s[7:]:
        if ch == 'L':
            b = L(b)
        else: #'R'
            b = R(b)
    return a[0] * 8 + b[0]

def findMissingAdjacent(xs):
    found = False
    for i in range(0, len(xs)):
        if (xs[i + 1] - xs[i] != 1):
            return xs[i] + 1
    return -1

def day5_part1():
    seatsId = [computeSeatId(s) for s in readAllLines()]
    maxSeatId = max(seatsId)
    print(maxSeatId)

def day5_part2():
    seatsId = [computeSeatId(s) for s in readAllLines()]
    seatsId.sort()
    myseatId = findMissingAdjacent(seatsId)
    print(myseatId)

if __name__ == "__main__":
    #day5_part1() #Your puzzle answer was 926.
    day5_part2() #Your puzzle answer was 657.
