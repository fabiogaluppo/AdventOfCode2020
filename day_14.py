#python day_14.py < .\input\input14.txt

import sys
import re
import functools

def readAllLines():
    return [line.rstrip() for line in sys.stdin]

def deriveAllMasks(mask):
    def deriveAllMasksRec(mask):
        i = mask.find('X')
        if i == -1:
            return [mask]
        left, right, temp = deriveAllMasksRec(mask[:i]), deriveAllMasksRec(mask[i + 1:]), []
        for l in left:
            for r in right:
                temp.append(l + '0' + r)
                temp.append(l + '1' + r)
        return temp
    return deriveAllMasksRec(mask)

def copyBits(src, dst, mask):
    return (dst & ~mask) | (src & mask)

def copyMask(mask):
    return ''.join(['1' if c != 'X' else '0' for c in mask])

def bitmaskRule(bitmask, memory):
    temp = []
    for i in range(len(bitmask)):
        if bitmask[i] == 'X':
            temp.append('X')
        elif bitmask[i] == '0':
            temp.append(memory[i])
        elif bitmask[i] == '1':
            temp.append('1')
        else:
            pass
    return ''.join(temp)

def getAddresses(v, mask):
    newMask = bitmaskRule(mask, "{:036b}".format(v))
    return [int(m, 2) for m in deriveAllMasks(newMask)]

def getResult(v, mask):
    return copyBits(int(mask.replace('X', '0'), 2), v, int(copyMask(mask), 2))

def sumAll(d):
    return functools.reduce(lambda acc, k: acc + d[k], d, 0)

def day14_part1():
    mask = ''
    mem = {}
    addrSpcMask = 68719476735 #36-bit address space
    lines = readAllLines()
    for line in lines:
        res = re.search("^(mask) = ([X0-1]+)|(mem)\[([0-9]+)\] = ([0-9]+)$", line)
        if res.group(1) != None:
            mask = res.group(2)
        else:
            k, v = int(res.group(4)), int(res.group(5))
            if k in mem:
                mem[k] = addrSpcMask & getResult(v, mask)
            else:
                mem.update({k : addrSpcMask & getResult(v, mask)})
    sumOfAllValuesInMemory = sumAll(mem)
    print(sumOfAllValuesInMemory)

def day14_part2():
    mask = ''
    mem = {}
    lines = readAllLines()
    for line in lines:
        res = re.search("^(mask) = ([X0-1]+)|(mem)\[([0-9]+)\] = ([0-9]+)$", line)
        if res.group(1) != None:
            mask = res.group(2)
        else:
            k, v = int(res.group(4)), int(res.group(5))
            for m in getAddresses(k, mask):
                if m in mem:
                    mem[m] = v
                else:
                    mem.update({m : v})
    sumOfAllValuesInMemory = sumAll(mem)
    print(sumOfAllValuesInMemory)

if __name__ == "__main__":
    #day14_part1() #Your puzzle answer was 7611244640053.
    day14_part2() #Your puzzle answer was 3705162613854.
