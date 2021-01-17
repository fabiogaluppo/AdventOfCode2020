#python day_22.py < .\input\input22.txt

import sys
from collections import deque
import functools
import itertools

def readAllLines():
    lines = [line.rstrip() for line in sys.stdin]
    i = lines.index('')
    player1, player2 = lines[:i], lines[i + 1:-1]
    player1Cards, player2Cards = [int(card) for card in player1[1:]], [int(card) for card in player2[1:]]
    return ((player1[0].split(':')[0], player1Cards), (player2[0].split(':')[0], player2Cards))

class Deck:
    def __init__(self, name, cards):
        self._name = name
        self.dq = deque(cards)
    def deepCopy(self, n = -1):
        it = self.iterator()
        return Deck(self.name, it if n < 0 else itertools.islice(it, n))
    @property
    def name(self):
        return self._name
    def pushFront(self, value):
        self.dq.appendleft(value)
    def popFront(self):
        return self.dq.popleft()
    def pushBack(self, value):
        self.dq.append(value)
    def popBack(self):
        return self.dq.pop()
    def top(self):
        return self.dq[0]
    def back(self):
        return self.dq[-1]
    def iterator(self):
        for x in self.dq:
            yield x
    def __str__(self):
        return '{}\'s deck: {}'.format(self._name, ', '.join([str(x) for x in self.iterator()]))
    def __repr__(self):
        return self.__str__()
    def __len__(self):
        return len(self.dq)
    def __eq__(self, other):
        if isinstance(other, Deck):
            return self._name == other._name and self.dq == other.dq
        return NotImplemented

def computeScore(cards):
    cardsAndWeights = zip(cards, list(range(len(cards), 0, -1)))
    return functools.reduce(lambda acc, cw: acc + cw[0] * cw[1], cardsAndWeights, 0)

def playCombat(p1Deck, p2Deck):
    round = 0
    while not (len(p1Deck) == 0 or len(p2Deck) == 0):
        round += 1
        #DBG
        #print('-- Round {} --'.format(round))
        #print(p1Deck)
        #print(p2Deck)
        #print('{} plays: {}'.format(p1Deck.name, p1Deck.top()))
        #print('{} plays: {}'.format(p2Deck.name, p2Deck.top()))
        winner, loser = (p1Deck, p2Deck) if p2Deck.top() < p1Deck.top() else (p2Deck, p1Deck)
        winner.pushBack(winner.popFront())
        winner.pushBack(loser.popFront())
        #DBG
        #print('{} wins the round!'.format(winner.name))
        #print()
    print('== Post-game results ==')
    print(p1Deck)
    print(p2Deck)
    print()
    return list(p1Deck.iterator() if len(p1Deck) > 0 else p2Deck.iterator())

def day22_part1():
    (p1Name, p1Cards), (p2Name, p2Cards) = readAllLines()
    p1Deck, p2Deck = Deck(p1Name, p1Cards), Deck(p2Name, p2Cards)
    winnerCards = playCombat(p1Deck, p2Deck)
    score = computeScore(winnerCards)
    print(score)

GAME = 1 #global variable

def playRecursiveCombatRec(p1Deck, p2Deck):
    global GAME
    game, round, winner, saved = GAME, 0, None, set()
    #DBG
    #print('=== Game {} ==='.format(game))
    #print()
    while not (len(p1Deck) == 0 or len(p2Deck) == 0):
        round += 1
        key = str('{} {}'.format(p1Deck, p2Deck))
        if round > 1 and key in saved:
            winner = p1Deck
            break
        saved.update({key})
        #DBG
        #print('-- Round {} (Game {}) --'.format(round, game))
        #print(p1Deck)
        #print(p2Deck)
        #print('{} plays: {}'.format(p1Deck.name, p1Deck.top()))
        #print('{} plays: {}'.format(p2Deck.name, p2Deck.top()))
        top1, top2 = p1Deck.popFront(), p2Deck.popFront()
        len1, len2 = len(p1Deck), len(p2Deck)
        if (top1 <= len1) and (top2 <= len2):
            #sub-game
            #DBG
            #print('Playing a sub-game to determine the winner...')
            #print()
            GAME += 1
            winner = playRecursiveCombatRec(p1Deck.deepCopy(top1), p2Deck.deepCopy(top2))
            #DBG
            #print('...anyway, back to game {}.'.format(game))
        else:
            winner = p1Deck if top2 < top1 else p2Deck        
        if winner.name == p1Deck.name:
            winner = p1Deck #adjust if the sub-game has defined the winner
            p1Deck.pushBack(top1)
            p1Deck.pushBack(top2)
        else:
            winner = p2Deck #adjust if the sub-game has defined the winner
            p2Deck.pushBack(top2)
            p2Deck.pushBack(top1)
        #DBG
        #print('{} wins round {} of game {}!'.format(winner.name, round, game))
        #print()    
    #DBG
    #print('The winner of game {} is {}!'.format(game, winner.name))
    #print()
    if (game == 1):
        print('== Post-game results ==')
        print(p1Deck)
        print(p2Deck)
        print()
    return winner

def playRecursiveCombat(p1Deck, p2Deck):
    winner = playRecursiveCombatRec(p1Deck, p2Deck)
    return list(winner.iterator())

def day22_part2():
    (p1Name, p1Cards), (p2Name, p2Cards) = readAllLines()
    p1Deck, p2Deck = Deck(p1Name, p1Cards), Deck(p2Name, p2Cards)
    winnerCards = playRecursiveCombat(p1Deck, p2Deck)
    score = computeScore(winnerCards)
    print(score)

if __name__ == "__main__":
    #day22_part1() #Your puzzle answer was 32824.
    day22_part2() #Your puzzle answer was 36515.
