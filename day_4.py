#python day_4.py < .\input\input4.txt

import sys
import re

VALID_KEYS  = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
IGNORE_KEYS = {"cid"}

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

def validPassportsByKey(xs):
    keys = VALID_KEYS
    keysCounter = len(VALID_KEYS)
    valids = []
    for xs in [str.split(x, " ") for x in xs]:
        ys = []
        counter = 0 
        for x in xs:
            temp = str.split(x, ":")
            k, v = temp[0], temp[1]
            if k not in IGNORE_KEYS:
                counter = counter + (1 if k in keys else 0)
            ys.append((k, v))
        if (counter == keysCounter):
            valids.append(dict(ys))
    return valids

def validateValues(kv):
    #byr (Birth Year) - four digits; at least 1920 and at most 2002.
    byr = re.search("^\d{4}$", kv["byr"])
    if byr != None:
        if not (1920 <= int(byr.group(0)) <= 2002):
            return False
    #iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    iyr = re.search("^\d{4}$", kv["iyr"])
    if iyr != None:
        if not (2010 <= int(iyr.group(0)) <= 2020):
            return False
    #eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    eyr = re.search("^\d{4}$", kv["eyr"])
    if eyr != None:
        if not (2020 <= int(eyr.group(0)) <= 2030):
            return False
    #hgt (Height) - a number followed by either cm or in:
    #If cm, the number must be at least 150 and at most 193.
    #If in, the number must be at least 59 and at most 76.
    hgt = re.search("^(\d*)(in|cm)+$", str(kv["hgt"]))
    if hgt != None:
        if (hgt.group(2) == "cm"):
            if not (150 <= int(hgt.group(1)) <= 193):
                return False
        else:
            if not (59 <= int(hgt.group(1)) <= 76):
                return False
    else:
        return False
    #hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    hcl = re.search("^#[0-9a-f]{6}$", kv["hcl"])
    if hcl == None:
        return False
    #ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    ecl = re.search("^(amb)|(blu)|(brn)|(gry)|(grn)|(hzl)|(oth)$", kv["ecl"])
    if ecl == None:
        return False
    #pid (Passport ID) - a nine-digit number, including leading zeroes.
    pid = re.search("^[0-9]{9}$", kv["pid"])
    if pid == None:
        return False
    #DBG
    #print(kv["byr"], "\t", kv["iyr"], "\t", kv["eyr"], "\t", kv["hgt"], "\t", kv["hcl"], "\t", kv["ecl"], "\t", kv["pid"])
    return True

def day4_part1():
    validPassports = validPassportsByKey(readAllLines())
    validPassportsByKeyCounter = len(validPassports)
    print(validPassportsByKeyCounter)

def day4_part2():
    validPassports = validPassportsByKey(readAllLines())
    validPassportsCounter = sum([validateValues(validPassportByKey) for validPassportByKey in validPassports])
    print(validPassportsCounter) 

if __name__ == "__main__":
    #day4_part1() #Your puzzle answer was 216.
    day4_part2() #Your puzzle answer was 150.
