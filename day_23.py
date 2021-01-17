#python day_23.py < .\input\input23.txt

import sys

def readInput():
    lines = [line.rstrip() for line in sys.stdin]
    return lines[0]

class Node:
    def __init__(self, number, next = None):
        self._number = number
        self._next = next
    @property
    def number(self):
        return self._number
    @property
    def next(self):
        return self._next
    @next.setter
    def next(self, node):
        self._next = node
    def __str__(self):
        return '{}->{}'.format(self._number, self._next.number if self._next != None else '\\')
    def __repr__(self):
        return self.__str__()

def nodesToList(node):
    if node == None:
        return []
    xs = []
    while True:
        xs.append(node.number)
        node = node.next
        if (node == None or node.number == xs[0]):
            break
    return xs

def doMoves(cups, nMoves, nCups):
    def linkAll(cups, N):
        for i in range(0, N - 1): cups[i].next = cups[i + 1]
        cups[N - 1].next = cups[0]
        return cups
    N = nCups
    cups = linkAll([Node(cup) for cup in ([int(cup) for cup in cups] + [cup for cup in range(len(cups) + 1, N + 1)])], N) #cups as list of Nodes
    current = cups[0]
    cups = {cup.number : cup for cup in cups} #cups as dict of Node values with cup (int) as key
    for move in range(1, nMoves + 1):
        #DBG
        #print('-- move {} --'.format(move))
        #print('current:', current.number)
        a = current.next
        b = a.next 
        c = b.next
        current.next = c.next
        #DBG
        #print('pick up:', [a.number, b.number, c.number])        
        destination = current.number - 1 if current.number > 1 else N
        while destination == a.number or destination == b.number or destination == c.number:
            destination = destination - 1
            if destination == 0: destination = N
        #DBG
        #print('destination:', destination)
        #print()
        destination = cups[destination]
        c.next = destination.next
        destination.next = a
        current = current.next
    #DBG
    #print('cups:', nodesToList(current))
    return cups

def after(cups, cup):
    return ''.join([str(cup) for cup in nodesToList(cups[cup])[1:]])
    
def day23_part1():
    cups = readInput()
    cups = doMoves(cups, 100, len(cups))
    #DBG
    #print(cups)
    after1 = after(cups, 1)
    print(after1)

def day23_part2():
    cups = doMoves(readInput(), 10000000, 1000000)
    #DBG
    #print(cups[1].next.number, cups[1].next.next.number)
    labelsMul = cups[1].next.number * cups[1].next.next.number
    print(labelsMul)
    
if __name__ == "__main__":
    #day23_part1() #Your puzzle answer was 46978532.
    day23_part2() #Your puzzle answer was 163035127721.
