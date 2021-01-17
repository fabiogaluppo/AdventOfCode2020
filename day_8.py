#python day_8.py < .\input\input8.txt

import sys
import re

def readAllLines():
    return [line.rstrip() for line in sys.stdin]

def parse(line):
    res = re.search("^(nop|acc|jmp) ((\+|-)([0-9])+)$", line)
    return (res.group(1), int(res.group(2)), res.group(0))

def runInterpreter(program, checkpoint):
    pc, acc, last = 0, 0, len(program)
    while pc < last:
        if not checkpoint(program, pc, acc):
            break
        opcode, immediate, _ = program[pc]
        if opcode == "nop":
            pc = pc + 1
        elif opcode == "acc":
            acc = acc + immediate
            pc = pc + 1
        elif opcode == "jmp":
            pc = pc + immediate
        else:
            pass #should fail
    return acc

def checkpointInstructionRunsTwice():
    visited = set()
    def checkpointInstructionRunsTwiceInternal(program, pc, acc):
        if pc not in visited:
            visited.add(pc)
            return True
        else:
            return False
    return checkpointInstructionRunsTwiceInternal

def checkpointInstructionRunsTwice2(instructionsToRetarget):
    visited = set()
    stack = []
    def checkpointInstructionRunsTwiceInternal(program, pc, acc):
        stack.append(pc)
        if pc not in visited:
            visited.add(pc)
            return True
        else:
            #DBG
            #print("stack:", [(pc, program[pc]) for pc in stack], "current:", program[pc], "pc:", pc, "acc:", acc)
            #print("steps: ", [pc for pc in stack])
            instructionsToRetarget.extend([(pc, program[pc][2]) for pc in stack if program[pc][0] != "acc"])
            #print("instructions:", instructionsToRetarget)
            return False
    return checkpointInstructionRunsTwiceInternal

def replaceOpcode(opcode):
    if opcode == "nop":
        return "jmp"
    elif opcode == "jmp":
        return "nop"
    else:
        pass #should fail

def day8_part1():
    program = [parse(line) for line in readAllLines()]
    acc = runInterpreter(program, checkpointInstructionRunsTwice())
    print(acc)

def day8_part2():
    program = [parse(line) for line in readAllLines()]
    instructionsToRetarget = []
    acc = runInterpreter(program, checkpointInstructionRunsTwice2(instructionsToRetarget))
    if len(instructionsToRetarget) > 0:
        for pc, _ in instructionsToRetarget:
            opcode, immediate, instruction = program[pc]
            oldInstruction = program[pc]
            program[pc] = (replaceOpcode(opcode), immediate, instruction)
            temp = []
            acc = runInterpreter(program, checkpointInstructionRunsTwice2(temp))
            if len(temp) == 0:
                #DBG
                #print("replaced", oldInstruction[0], "to", program[pc][0], "at line", pc)
                break
            program[pc] = oldInstruction
    print(acc)

if __name__ == "__main__":
    #day8_part1() #Your puzzle answer was 1420.
    day8_part2() #Your puzzle answer was 1245.
