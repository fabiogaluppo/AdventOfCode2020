#python day_2.py < .\input\input2.txt

import sys
import functools
from operator import xor

def day2_part1():
    valid = 0
    for x in sys.stdin:
        xs = str.split(x, " ")
        interval = str.split(xs[0], "-")
        t = xs[1][0]
        lo, hi = int(interval[0]), int(interval[1])
        counter = functools.reduce(lambda acc, ch: acc + (1 if ch == t else 0), xs[2], 0)
        valid = valid + (1 if lo <= counter <= hi else 0)
    print(valid)

def day2_part2():
    valid = 0
    for x in sys.stdin:
        xs = str.split(x, " ")
        position = str.split(xs[0], "-")
        t = xs[1][0]
        pos0, pos1 = int(position[0]) - 1, int(position[1]) - 1
        valid = valid + (1 if xor(xs[2][pos0] == t, xs[2][pos1] == t) else 0)
    print(valid)

if __name__ == "__main__":
    #day2_part1() #Your puzzle answer was 638.
    day2_part2() #Your puzzle answer was 699.
