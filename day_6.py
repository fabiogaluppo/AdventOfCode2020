#python day_6.py < .\input\input6.txt

import sys

def readAllLines():
    lines = []
    line = ''
    #terminates with two '\n' - check input files
    for input in sys.stdin:
        input = input.rstrip()
        if input != '':    
            line = line + " " + input
        else:
            lines.append(line.lstrip())
            line = ''
    return lines

def countAnyoneAnswers(ss):
    counter = set()
    for s in ss.split(" "):
        for ch in s:
            counter.update(ch)
    return len(counter)

def countEveryoneAnswers(ss):
    counter = {}
    ss = ss.split(" ")
    total = len(ss)
    for s in ss:
        for ch in s:
            if ch in counter:
                counter[ch] = counter[ch] + 1
            else:
                counter.update({ch : 1})
    return sum([counter[k] == total for k in counter])

def day6_part1():
    yesCounter = sum([countAnyoneAnswers(ss) for ss in readAllLines()])
    print(yesCounter)

def day6_part2():
    yesCounter = sum([countEveryoneAnswers(ss) for ss in readAllLines()])
    print(yesCounter)

if __name__ == "__main__":
    #day6_part1() #Your puzzle answer was 6534.
    day6_part2() #Your puzzle answer was 3402.
