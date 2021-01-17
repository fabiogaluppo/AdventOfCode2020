#python day_12.py < .\input\input12.txt

import sys
from enum import IntEnum

def readAllLines():
    return [line.rstrip() for line in sys.stdin]

class Facing(IntEnum):
    #rotate left as reference
    EAST = 0
    NORTH = 90
    WEST = 180
    SOUTH = 270

class ShipNavigator:
    def __init__(self, xStartPoint, yStartPoint, facing):
        self.x = xStartPoint
        self.y = yStartPoint
        self.facing = facing
    def position(self):
        return (self.x, self.y)
    def N(self, v):
        self.y = self.y + v
    def S(self, v):
        self.y = self.y - v
    def E(self, v):
        self.x = self.x + v
    def W(self, v):
        self.x = self.x - v
    def L(self, v):
        facing = int(self.facing)
        facing = (facing + v) % 360
        self.facing = Facing(facing)
    def R(self, v):
        self.L(360 - v)
    def F(self, v):
        if self.facing == Facing.EAST:
            self.E(v)
        elif self.facing == Facing.NORTH:
            self.N(v)
        elif self.facing == Facing.WEST:
            self.W(v)
        elif self.facing == Facing.SOUTH:
            self.S(v)
        else:
            pass #ignored
    def __str__(self):
        return ''.join([str(abs(self.x)), " ", "east" if self.x >= 0 else "west", ", ", str(abs(self.y)), " ", "north" if self.y >= 0 else "south"])

class WaypointNavigator:
    def __init__(self, xStartPoint, yStartPoint):
        self.xWaypoint = xStartPoint
        self.yWaypoint = yStartPoint
        self.xShip = 0
        self.yShip = 0        
    def waypointPosition(self):
        return (self.xWaypoint, self.yWaypoint)
    def shipPosition(self):
        return (self.xShip, self.yShip)
    def N(self, v):
        self.yWaypoint = self.yWaypoint + v
    def S(self, v):
        self.yWaypoint = self.yWaypoint - v
    def E(self, v):
        self.xWaypoint = self.xWaypoint + v
    def W(self, v):
        self.xWaypoint = self.xWaypoint - v
    def L(self, v):
        if   v == 90:
            self.xWaypoint, self.yWaypoint = -self.yWaypoint, self.xWaypoint
        elif v == 180:
            self.xWaypoint, self.yWaypoint = -self.xWaypoint, -self.yWaypoint
        elif v == 270:
            self.xWaypoint, self.yWaypoint = self.yWaypoint, -self.xWaypoint
        else:
            pass #ignored
    def R(self, v):
        self.L(360 - v)
    def F(self, v):
        self.xShip = self.xShip + v * self.xWaypoint
        self.yShip = self.yShip + v * self.yWaypoint
    def __str__(self):
        def strOf(x, y):
            return ''.join([str(abs(x)), " ", "east" if x >= 0 else "west", ", ", str(abs(y)), " ", "north" if y >= 0 else "south"])
        return ''.join(["ship: ", strOf(self.xShip, self.yShip), " waypoint: ", strOf(self.xWaypoint, self.yWaypoint)])

def manhattanDistance(x0, y0, x1, y1):
    return abs(x0 - x1) + abs(y0 - y1)

def moveShip(navigator):
    moves = [(line[0], int(line[1:])) for line in readAllLines()]
    #x0, y0 = 0, 0
    n = navigator #ShipNavigator(x0, y0, Facing.EAST)
    for move, value in moves:
        if   move == 'N': n.N(value)
        elif move == 'S': n.S(value)
        elif move == 'E': n.E(value)
        elif move == 'W': n.W(value)
        elif move == 'L': n.L(value)
        elif move == 'R': n.R(value)
        elif move == 'F': n.F(value)
        else: pass #should fail
    return n

def day12_part1():
    x0, y0 = 0, 0
    n = moveShip(ShipNavigator(x0, y0, Facing.EAST))
    x1, y1 = n.position()
    distanceFromStartingPosition = manhattanDistance(x0, y0, x1, y1)
    print(distanceFromStartingPosition)

def day12_part2():
    x0, y0 = 0, 0
    n = moveShip(WaypointNavigator(10, 1))
    x1, y1 = n.shipPosition()
    distanceFromStartingPosition = manhattanDistance(x0, y0, x1, y1)
    print(distanceFromStartingPosition)

if __name__ == "__main__":
    #day12_part1() #Your puzzle answer was 1645.
    day12_part2() #Your puzzle answer was 35292.
