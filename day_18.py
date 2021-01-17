#python day_18.py < .\input\input18.txt

import sys
import functools

def strToExpression(s):
    return s.replace('(', '( ').replace(')', ' )').split(' ')

def readAllLines():
    return [strToExpression(line.rstrip()) for line in sys.stdin]

class Stack:
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        return self.stack.pop()
    def isEmpty(self):
        return len(self.stack) == 0
    def size(self):
        return len(self.stack)
    def top(self):
        return self.stack[len(self.stack) - 1] if not self.isEmpty() else None
    def __str__(self):
        return self.stack.__str__()

def evaluateExpressionLeftToRight(expression):
    def evaluateBinaryOperation(op, numbers):
        if  op == '+':
            numbers.push(numbers.pop() + numbers.pop())
        elif op == '*':
            numbers.push(numbers.pop() * numbers.pop())
        else:
            pass #should fail
    def evaluateParenthesis(operators, numbers, removeTopOperator):
        numbers2, operators2 = Stack(), Stack()
        numbers2.push(numbers.pop())
        while not operators.isEmpty() and operators.top() != '(':
            operators2.push(operators.pop())
            numbers2.push(numbers.pop())
        if removeTopOperator: operators.pop()
        while not operators2.isEmpty():
            evaluateBinaryOperation(operators2.pop(), numbers2)
        numbers.push(numbers2.pop())
    tokens, numbers, operators = expression, Stack(), Stack()
    openParenthesis = 0
    for token in tokens:
        #DBG
        #print(numbers, operators, openParenthesis)
        if '0' <= token <= '9':
            numbers.push(int(token))
        else:   
            operators.push(token)
            op = token
            if op == '(':
                openParenthesis = openParenthesis + 1
            elif op == ')':
                operators.pop()
                if numbers.size() >= 2:
                    evaluateParenthesis(operators, numbers, True)
                openParenthesis = openParenthesis - 1
                if numbers.size() >= 2:
                    evaluateParenthesis(operators, numbers, False)
                #DBG
                #print(numbers, operators, openParenthesis)
        op = operators.top()
        if openParenthesis == 0 and (op == '+' or op == '*') and numbers.size() >= 2:
            evaluateBinaryOperation(operators.pop(), numbers)
    if operators.size() == 1: operators.pop()
    #DBG
    #print(numbers, operators, openParenthesis)
    #print('-' * 10)
    return numbers.pop()

#Simple expression has no parenthesis, except at the beginning and ending
#Ex.: (1 + 2 + 3 * 4 + 5 + 6)
def reduceSimpleExpression(xs):
    i, j = 0, len(xs)
    if j > 1:
        if (xs[0] == '(') and (xs[j - 1] == ')'):
            xs = xs[i + 1:j - 1]
        else:
            pass #should fail
        ys = [xs[i]] if xs[i + 1] == '*' else []
        i, j = i + 1, len(xs)
        while (i < j):
            if xs[i] == '+':
                acc = xs[i - 1]
                while i < j and xs[i] != '*':
                    acc = acc + xs[i + 1]
                    i = i + 2 #jumps to next binary operator (+ or *)
                ys.append(acc)
            elif xs[i] == '*':
                if (i + 2 >= j or xs[i + 2] == '*'):
                    ys.append(xs[i + 1])
                i = i + 2 #jumps to next binary operator (+ or *)
            else:
                pass #should fail
        return functools.reduce(lambda acc, y: acc * y, ys, 1)
    return xs[0]

#DBG
#def printExpression(label, xs):
#    print(label, ''.join([str(x) for x in xs]))

def reduceInnerBlocks(xs):
    i = -1 #start of next block
    temp = []
    for j, x in enumerate(xs):
        if   x == '(':
            i = j
        elif x == ')':
            if i > -1:
                temp.append((reduceSimpleExpression(xs[i:j + 1]), (i, j + 1)))
                i = -1
    if temp != []:
        ys, k = [], 0
        for (reduced, (i, j)) in temp:
            ys = ys + xs[k:i] + [reduced]
            k = j
        ys = ys + xs[k:]
        #DBG
        #printExpression('->', ys)
        return (True, ys)
    return (False, [])

def evaluateExpressionLeftToRightWithAddBeforeMul(expression):
    xs = [int(x) if '0' <= x <= '9'  else x for x in expression]
    #DBG
    #printExpression('=>', expression)
    while True:
        canContinue, reduced = reduceInnerBlocks(xs)
        if not canContinue:
            break
        xs = reduced
    return reduceSimpleExpression(xs)

def day18_part1():
    resultingValues = [evaluateExpressionLeftToRight(expression) for expression in readAllLines()]
    #DBG
    #for rv in resultingValues: print(rv)
    #print('=' * 10)
    sumOfResultingValues = sum(resultingValues)
    print(sumOfResultingValues)

def day18_part2():
    resultingValues = [evaluateExpressionLeftToRightWithAddBeforeMul(expression) for expression in readAllLines()]
    #DBG
    #for rv in resultingValues: print(rv)
    #print('=' * 10)
    sumOfResultingValues = sum(resultingValues)
    print(sumOfResultingValues)

if __name__ == "__main__":
    #day18_part1() #Your puzzle answer was 12956356593940.
    day18_part2() #Your puzzle answer was 94240043727614.
