#python day_1.py < .\input\input1.txt

import sys

TARGET = 2020

def day1_part1():
    d = {}
    for x in sys.stdin:
        k = int(x)
        if k in d:
            print(d[k] * k)
            break
        d[TARGET - k] = k

def day1_part2():
    xs = []
    for x in sys.stdin:
        xs.append(x)
    d = {}
    for i in range(len(xs)):
        k = int(xs[i])
        t = TARGET - k
        d[t] = k
        d2 = {}
        for j in range(i, len(xs)):
            k2 = int(xs[j])
            if k2 in d2:
                print(d[t] * k2 * d2[k2])
                return
            d2[t - k2] = k2

if __name__ == "__main__":
    #day1_part1() #Your puzzle answer was 805731.
    day1_part2() #Your puzzle answer was 192684960.
