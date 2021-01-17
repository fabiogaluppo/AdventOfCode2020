#python day_19.py < .\input\input19.txt

import sys
import re

def readAllLines():
    return [line.rstrip() for line in sys.stdin]

def parseRule(rule, reCompiled):
    x = reCompiled.match(rule)
    if x.group(7) != None:
        return (int(x.group(1)), [x.group(7)]) #terminal
    else:
        links1 = [int(x.group(2))]
        if x.group(3) != None:
            links1 = links1 + [int(x.group(3))]
        if x.group(4) != None:
            links1 = links1 + [int(x.group(4))]
        if x.group(5) == None:
            return (int(x.group(1)), links1) #non-terminal

        links2 = [int(x.group(5))]
        if x.group(6) != None:
            links2 = links2 + [int(x.group(6))]
        return (int(x.group(1)), [(links1, links2)]) #non-terminal

def matchRec(rules, rule, msg):
    #DBG
    #print("rule:", rule, "msg:", msg)
    if rule != []:
        if msg == '':
            return (False, msg)
        
        if rule[0] == msg[0]:
            return matchRec(rules, rule[1:], msg[1:])
    
        if isinstance(rule[0], int):
            return matchRec(rules, rules[rule[0]] + rule[1:], msg)
    
        if isinstance(rule[0], tuple):
            for r in rule[0]:
                match_, msg_ = matchRec(rules, r + rule[1:], msg)
                if match_:
                    return (True, msg_)

        return (False, msg)
    #else: rule == []
    return (True, msg)

def match(rules, k,  msg):
    match_, msg_ = matchRec(rules, rules[k], msg)
    return match_ and len(msg_) == 0

def matchWithRecRuleFunc(rules, messages):
    #DBG
    #print('messages:', messages)
    #print('rules:', rules)
    return sum([match(rules, 0, message) for message in messages])

def readRulesAndMessages():
    lines = readAllLines()
    i = lines.index('')
    rules, messages = lines[:i], lines[i + 1:]
    reCompiled = re.compile("^([0-9]+): (?:(?:([0-9]+)(?:(?: ([0-9]+))?)(?:(?: ([0-9]+))?)(?:(?: \| ([0-9]+)(?:(?: ([0-9]+))?)))?)|(?:\"([a-z]{1})\"))$")
    rules = {key: value for key, value in [parseRule(rule, reCompiled) for rule in rules]}    
    return rules, messages

def day19_part1():
    rules, messages = readRulesAndMessages()
    matchRule0Counter = matchWithRecRuleFunc(rules, messages)
    print(matchRule0Counter)

def day19_part2():
    rules, messages = readRulesAndMessages()
    rules[8] = [rules[8][0], ([], [8])]
    rules[11] = [rules[11][0], ([], [11]), rules[11][1]]
    matchRule0Counter = matchWithRecRuleFunc(rules, messages)
    print(matchRule0Counter)
    #DBG
    #print(match(rules, 0, "babbbbaabbbbbabbbbbbaabaaabaaa"))
    return

if __name__ == "__main__":
    #day19_part1() #Your puzzle answer was 192.
    day19_part2() #Your puzzle answer was 296.
