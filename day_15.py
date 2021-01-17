#python day_15.py < .\input\input15.txt

import sys

def readLine():
    return [int(c) for c in sys.stdin.readline().rstrip().split(',')]

def playTheGame(nthTurn):
    startingNumbers = readLine()
    turns = {k : [i + 1] for i, k in enumerate(startingNumbers)}
    turn = len(turns)
    lastSpoken = startingNumbers[-1:][0]   
    while turn < nthTurn:
        turn = turn + 1
        if lastSpoken in turns:
            lastSpoken = 0 if len(turns[lastSpoken]) == 1 else turns[lastSpoken][0] - turns[lastSpoken][1]
            turns[lastSpoken] = [turn, turns[lastSpoken][0]] if lastSpoken in turns else [turn]
        else:
            turns[lastSpoken] = [turn]
    return lastSpoken

def day15_part1():
    lastSpoken = playTheGame(2020)
    print(lastSpoken)

def day15_part2():
    lastSpoken = playTheGame(30000000)
    print(lastSpoken)

if __name__ == "__main__":
    #day15_part1() #Your puzzle answer was 240.
    day15_part2() #Your puzzle answer was 505.
