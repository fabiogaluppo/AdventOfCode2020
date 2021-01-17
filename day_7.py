#python day_7.py < .\input\input7.txt

import sys
import re

def readAllLines():
    return [line.rstrip() for line in sys.stdin]

def parse(line):
    re0 = re.search("^([a-z]+ [a-z]+) bags contain ([0-9a-z ,.]*)$", line)
    res = [] if re0.group(2).startswith('no') else [(int(re1.group(1)), re1.group(2)) for re1 in [re.search("^([1-9]) ([a-z]+ [a-z]+) (bag|bags)$", pattern.lstrip()) for pattern in re.split('\.|,', re0.group(2))[:-1]]]
    return (re0.group(1), res)

class Digraph:
    def __init__(self, keys):
        self.K = keys #vertex names to indices
        self.I = [k for k in keys] #indices to vertex names
        self.V = len(keys) #number of vertices
        self.E = 0 #number of edges
        self.A =  [{} for _ in range(len(keys))] #adjacency list for vertex v
    def addEdge(self, fromVertex, toVertex):
        self.__addEdge(self.indexOfKey(fromVertex), self.indexOfKey(toVertex))
    def __addEdge(self, fromVertex, toVertex):
        adjs = self.A[fromVertex]
        if toVertex in adjs:
            adjs[toVertex] = adjs[toVertex] + 1
        else:
            adjs.update({toVertex : 1})
        self.E = self.E + 1
    def addEdges(self, fromVertex, toVertex, n):
        self.__addEdges(fromVertex, toVertex, n)
    def __addEdges(self, fromVertex, toVertex, n):
        for i in range(n):
            self.addEdge(fromVertex, toVertex)
    def indexOfKey(self, key):
        return self.K[key]
    def keyOfIndex(self, index):
        return self.I[index]
    def keys(self):
        return self.K
    def vertices(self):
        return self.V
    def edges(self):
        return self.E
    def adjacents(self, fromVertex):
        return self.__adjacents(self.indexOfKey(fromVertex))
    def __adjacents(self, fromVertex):
        return self.A[fromVertex]
    def reverse(self):
        d = Digraph(self.keys())
        for key in self.keys():
            for adj, n in self.adjacents(key).items():
                d.addEdges(self.keyOfIndex(adj), key, n)
        return d
    def __str__(self):
        return "{} vertices {} edges\n{}\n{}".format(self.V, self.E, self.K, ''.join(["{}: {}\n".format(i, adj) for i, adj in enumerate(self.A)]))

def depthFirstRec(d, key, visited, counter):
    if not key in visited:
        visited.add(key)
        for adj in d.adjacents(key):
            counter = depthFirstRec(d, d.keyOfIndex(adj), visited, counter)
        counter = counter + 1
    return counter

def countHowManyBagsCanEventuallyContainAtLeastOne(d, bag):
    return depthFirstRec(d, bag, set(), 0) - 1

def depthFirstRec2(d, key, m, visited):
    if not key in visited:
        visited.update({key : 0})
        acc = 0
        if len(d.adjacents(key)) > 0:
            xs = [1 if len(d.adjacents(d.keyOfIndex(adj))) > 0 else 0 for adj in d.adjacents(key)]
            ys = [(n, n * depthFirstRec2(d, d.keyOfIndex(adj), n, visited)) for adj, n in d.adjacents(key).items()]
            acc = sum([a * b + c for a, (b, c) in zip(xs, ys)])
        else:
            acc = 1
        visited[key] = acc
        return acc
    return visited[key]

def countHowManyIndividualBagsAreRequiredInside(d, bag):
    return depthFirstRec2(d, bag, 1, {})

def buildDigraph():
    entries = [parse(line) for line in readAllLines()]
    bags = {k:i for (i, (k, v)) in enumerate(entries)}
    d = Digraph(bags)
    for (fromVertex, toVertices) in entries:
        for (n, toVertex) in toVertices:
            d.addEdges(fromVertex, toVertex, n)
    return d

def day7_part1():
    d = buildDigraph()
    #How many bag colors can eventually contain at least one shiny gold bag?
    counter = countHowManyBagsCanEventuallyContainAtLeastOne(d.reverse(), "shiny gold")
    print(counter)

def day7_part2():
    d = buildDigraph()
    #How many individual bags are required inside your single shiny gold bag?
    counter = countHowManyIndividualBagsAreRequiredInside(d, "shiny gold")
    print(counter)

if __name__ == "__main__":
    #day7_part1() #Your puzzle answer was 185.
    day7_part2() #Your puzzle answer was 89084.
