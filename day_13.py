#python day_13.py < .\input\input13.txt

import sys
from heapq import heappush, heappop, heapify

def readAllLines():
    return [line.rstrip() for line in sys.stdin]

def computeDepartures(timestamp, busID):
    r = int(timestamp / busID)
    if (r * busID) == timestamp:
        return (0, busID)
    return ((r + 1) * busID - timestamp, busID)

def waitBySort():
    lines = readAllLines()
    t = int(lines[0])
    bs = [int(x) for x in lines[1].split(',') if x != 'x']
    sortedDepartures = sorted([computeDepartures(t, b) for b in bs], key = lambda x: x[0])
    return sortedDepartures[0][0] * sortedDepartures[0][1]

def waitByHeap():
    lines = readAllLines()
    t = int(lines[0])
    bs = [int(x) for x in lines[1].split(',') if x != 'x']
    h = []
    for b in bs: heappush(h, computeDepartures(t, b))
    return h[0][0] * h[0][1]

def day13_part1():
    #wait = waitBySort()
    wait = waitByHeap()
    print(wait)

def day13_part2():
    lines = readAllLines()
    t = int(lines[0])
    bs = [(int(x), i) for i, x in enumerate(lines[1].split(',')) if x != 'x']
    timestamp, timestampStep = 0, 1
    #DBG
    #print(bs)
    for (id_, step_) in bs:
        while (timestamp + step_) % id_ != 0:
            #DBG
            #print(id_, timestamp)
            timestamp += timestampStep
        #DBG
        #print(id_, timestamp)
        timestampStep *= id_
    print(timestamp)

if __name__ == "__main__":
    #day13_part1() #Your puzzle answer was 3035.
    day13_part2() #Your puzzle answer was 725169163285238.
