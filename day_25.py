#python day_25.py < .\input\input25.txt

import sys
from collections import namedtuple

def readAllLines():
    return [int(line.rstrip()) for line in sys.stdin]

def nextKeyGenerator(subjectNumber):
    key = 1
    while True:
        key = (key * subjectNumber) % 20201227
        yield key

Found = namedtuple('Found', ['key', 'loop'])
NotFound = None

def untilMatch(generator, matchFunc):
    for i, key in enumerate(generator):
        if matchFunc(i, key):
            return Found(key = key, loop = i)
    return NotFound

def day25_part1():
    lines = readAllLines()
    cardKey, doorKey = lines[0], lines[1]
    cardKeyLoop = untilMatch(nextKeyGenerator(7), lambda _, key: key == cardKey).loop
    encryptionKey = untilMatch(nextKeyGenerator(doorKey), lambda loop, _: loop == cardKeyLoop).key
    print(encryptionKey)
    
def day25_part2():
    #There's no part 2
    pass

if __name__ == "__main__":
    day25_part1() #Your puzzle answer was 16311885.
    #day25_part2()
