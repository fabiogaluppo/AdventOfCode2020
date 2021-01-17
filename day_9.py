#python day_9.py < .\input\input9.txt

import sys

def readAllLines():
    return [int(line.rstrip()) for line in sys.stdin]

def findMismatch(numbers, preamble):
    i, j, size = 0, preamble, len(numbers)
    d = set(numbers[:preamble])
    while j < size:
        target = numbers[j]
        found = False
        #DBG
        #print(d, numbers[i:i+preamble], target)
        for e in d:
            c = target - e
            if (c in d) and (c != e):
                found = True
                break
        if not found:
            return target
        d.remove(numbers[i])
        d.add(numbers[j])
        i = i + 1
        j = j + 1
    return -1

def findContiguousSum(numbers, target):
    i, j, total, size = 0, 0, 0, len(numbers)
    while j < size:
        temp = total + numbers[j]
        if temp == target:
            return numbers[i:j + 1]
        elif temp < target:
            total = temp
            j = j + 1
        else: #if temp > target
            total = total - numbers[i]
            if i == j: j = j + 1
            i = i + 1
    return []

def minMax(xs):
    min = max = xs[0]
    for x in xs:
        if x < min: 
            min = x
        elif x > max: 
            max = x
    return min, max

def day9_part1():
    preamble = 25
    mismatch = findMismatch(readAllLines(), preamble)
    print(mismatch)

def day9_part2():
    preamble = 25
    numbers = readAllLines()
    mismatch = findMismatch(numbers, preamble)
    contiguousSum = findContiguousSum(numbers, mismatch)
    minMaxSum =sum(minMax(contiguousSum))
    #print(contiguousSum)
    print(minMaxSum)

if __name__ == "__main__":
    #day9_part1() #Your puzzle answer was 104054607.
    day9_part2() #Your puzzle answer was 13935797.
