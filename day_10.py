#python day_10.py < .\input\input10.txt

import sys
import functools

def readAllLines():
    return [int(line.rstrip()) for line in sys.stdin]

def countIf(xs, target):
    return functools.reduce(lambda acc, x: acc + (1 if x == target else 0), xs, 0)

def countDistinctArrangementsRec(xs, i, acc, memo):
    if xs[i] in memo:
        return memo[xs[i]]
    if i < len(xs) - 1:
        if i + 1 < len(xs) and 1 <= xs[i + 1] - xs[i] <= 3:
            acc = acc + countDistinctArrangementsRec(xs, i + 1, acc, memo)
        if i + 2 < len(xs) and 1 <= xs[i + 2] - xs[i] <= 3:
            acc = acc + countDistinctArrangementsRec(xs, i + 2, acc, memo)
        if i + 3 < len(xs) and 1 <= xs[i + 3] - xs[i] <= 3:
            acc = acc + countDistinctArrangementsRec(xs, i + 3, acc, memo)
    else:
        acc = 1    
    memo.update({xs[i] : acc})
    #DBG
    #print(xs[i], acc)
    return acc

def countDistinctArrangements(xs):
    return countDistinctArrangementsRec(xs, 0, 0, {})

def day10_part1():
    xs = readAllLines()
    xs.sort()
    ys = [xs[0]]
    ys.extend([x - xs[i] for i, x in enumerate(xs[1:])])
    ys.extend([3])
    ys.sort()
    result = countIf(ys, 1) * countIf(ys, 3)
    print(result)
    
def day10_part2():
    xs = readAllLines()
    xs.extend([0])
    xs.sort()
    counter = countDistinctArrangements(xs)
    print(counter)

if __name__ == "__main__":
    #day10_part1() #Your puzzle answer was 2450.
    day10_part2() #Your puzzle answer was 32396521357312.
