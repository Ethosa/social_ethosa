# -*- coding: utf-8 -*-
# author: ethosa
from copy import copy, deepcopy
import math

class Matrix:
    def createUnitMatrix(width, height):
        matrix = []
        currentX = 0
        for x in range(width):
            timed = [0 if currentX != i else 1 for i in range(height)]
            currentX += 1
            matrix.append(timed)
        return Matrix(matrix)

    def createTriangularMatrix(width, height):
        matrix = []
        currentX = 0
        for x in range(width):
            timed = [0 if currentX > i else 1 for i in range(height)]
            currentX += 1
            matrix.append(timed)
        return Matrix(matrix)

    def createNullMatrix(width, height):
        return Matrix(width, height)

    def __init__(self, *args):
        if len(args) == 2:
            self.width, self.height = args
            self.obj = [[0 for x in range(self.width)] for y in range(self.height)]
            self.widthFill = 1
        elif len(args) == 1:
            if type(args[0]) == Matrix:
                self.width, self.height = copy(args[0].width), copy(args[0].height)
                self.obj = args[0].obj[:]
                self.widthFill = copy(args[0].widthFill)
            if type(args[0]) == list or type(args[0]) == tuple:
                self.width = len(args[0])
                self.height = len(args[0][0])
                self.obj = args[0]
                self.widthFill = len("%s" % args[0][0][0])

    def clear(self):
        for x in range(self.width):
            for y in range(self.height):
                self.obj[x][y] = 0
        self.widthFill = 1

    def fill(self, value=0):
        for x in range(self.width):
            for y in range(self.height):
                self.obj[x][y] = value
        self.widthFill = len("%s" % value)

    def setAt(self, x, y, value):
        self.obj[x+1][y+1] = value
        if len("%s" % value) > self.widthFill:
            self.widthFill = len("%s" % value)

    def getAt(self, x, y):
        return self.obj[x+1][y+1]

    def transpose(self):
        width = self.height
        height = self.width
        self.obj = [[self.obj[x][y] for x in range(self.height)] for y in range(self.width)]
        self.width = width
        self.height = height

    def flipSave(self):
        obj = []
        for x in range(self.width):
            obj.append(self.obj[x][:])
            self.obj[x] = [i for i in reversed(self.obj[x])]
        self.obj = [i for i in reversed(self.obj)]
        for x in range(self.width):
            for y in range(self.height):
                a, b = obj[x][y], self.obj[x][y]
                if a < 0 and b > 0 or a > 0 and b < 0:
                    self.obj[x][y] *= -1

    def flip(self):
        for x in range(self.width):
            obj.append(self.obj[x][:])
            self.obj[x] = [i for i in reversed(self.obj[x])]
        self.obj = [i for i in reversed(self.obj)]

    def getSum(self):
        s = 0
        for x in range(self.width):
            s += sum(self.obj[x][y] for y in range(self.height))
        return s

    def minor(self, xm, ym):
        matrix = []
        for x in range(self.width):
            t = []
            for y in range(self.height):
                if x != xm and y != ym:
                    t.append(self.obj[x][y])
            if t:
                matrix.append(t)
        if len(matrix) == 2:
            if len(matrix[0]) == 2 and len(matrix[1]) == 2:
                return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
        return Matrix(matrix)

    def elemCofactor(self, xc, yc):
        koef = (-1)**(xc+yc)
        minor = self.minor(xc, yc)
        return minor*koef

    def __neg__(self):
        obj = copy(self.obj)
        for x in range(self.width):
            for y in range(self.height):
                obj[x][y] = obj[x][y]*-1
        return Matrix(obj)

    def __add__(self, other):
        obj = copy(self.obj)
        if type(other) == Matrix:
            for x in range(self.width):
                for y in range(self.height):
                    obj[x][y] += other.obj[x][y]
        else:
            for x in range(self.width):
                for y in range(self.height):
                    obj[x][y] += other
        return Matrix(obj)

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        obj = copy(self.obj)
        for x in range(self.width):
            for y in range(self.height):
                obj[x][y] -= other.obj[x][y]
        return Matrix(obj)

    def __mul__(self, other):
        if other == 0:
            return 0
        elif other == 1:
            return self
        elif type(other) == int:
            for x in range(self.width):
                for y in range(self.height):
                    self.obj[x][y] *= other
            return self
        elif type(other) == Matrix:
            if self.width == other.height:
                s = 0
                width = self.width
                height = other.height
                matrix = []
                matrixTimed = []

                for z in range(len(self.obj)):
                    for j in range(len(other.obj[0])):
                        for i in range(len(self.obj[0])):
                            s = s + self.obj[z][i]*other.obj[i][j]
                        matrixTimed.append(s)
                        s = 0
                    matrix.append(matrixTimed)
                    matrixTimed = []
                return Matrix(matrix)
            else:
                return self

    def __imul__(self, other): return self.__mul__(other)
    def __len__(self): return len(self.obj)
    def __isub__(self, other): return self.__sub__(other)
    def __pos__(self): return -self

    def __eq__(self, other):
        if type(other) == Matrix:
            if other.obj == self.obj: return 1
            else: return 0
        else: return 0

    def __str__(self):
        return "%s\n" % "\n".join(" ".join("%s" % i if len("%s" % i) == self.widthFill else
                                    "%s%s" % (" "*(self.widthFill-len("%s" % i)), i) if len("%s" % i) < 6 else "%s" % i
                                    for i in self.obj[x])
                        for x in range(len(self.obj)))


class Point:
    def __init__(self, *args):
        if len(args) == 1:
            if type(args[0]) == Point:
                self.points = args[0].points
            elif type(args[0]) == list or type(args[0]) == tuple:
                self.points = args[0]
            else:
                self.points = [0, 0]
        elif len(args) == 0:
            self.points = [0, 0]
        else:
            self.points = args

    def euclideanDistance(self, *args):
        r = Point(*args)
        sum_sqr = sum([(self.points[i] - r.points[i])**2 for i in range(len(self.points))])
        distance = math.sqrt(sum_sqr)
        return distance

    def offset(self, points):
        for i in range(len(points)):
            self.points[i] += points[i]

    def __eq__(self, other): return self.points == other.points

    def __str__(self):
        return "<Point %s>" % self.points

class ArithmeticSequence:
    def __init__(self, *args):
        if len(args) == 0:
            self.start = 0
            self.d = 1
        elif len(args) == 1:
            obj = args[0]
            if type(obj) == ArithmeticSequence:
                self.start = copy(obj.start)
                self.d = copy(obj.d)
            elif type(obj) == list or type(obj) == tuple:
                if len(obj) == 0:
                    self.start = 0
                    self.d = 1
                elif len(obj) == 1:
                    self.start = obj[0]
                    self.d = 1
                else:
                    self.start = obj[0]
                    self.d = obj[1] - obj[0]
        else:
            self.start = args[0]
            self.d = args[1] - args[0]

    def getElem(self, number):
        s = copy(self.start)
        for i in range(number):
            s += self.d
        return s
    
    def getSum(self, number):
        lst = []
        s = copy(self.start)
        for i in range(number):
            s += self.d
            lst.append(copy(s))
        return sum(lst)

    def setIter(self, value):
        self.value = value

    def __iter__(self):
        for i in range(self.value):
            yield self.getElem(i)

    def __str__(self):
        return "<ArithmeticSequence (%s, %s, %s, %s, ...)>" % (self.getElem(0), self.getElem(1), self.getElem(2), self.getElem(3))


class GeometricSequence:
    def __init__(self, *args):
        if len(args) == 0:
            self.start = 1
            self.d = 2
        elif len(args) == 1:
            obj = args[0]
            if type(obj) == GeometricSequence:
                self.start = copy(obj.start)
                self.d = copy(obj.start)
            elif type(obj) == list or type(obj) == tuple:
                if obj[0] == 0:
                    self.start = obj[0] + 1
                    self.d = (obj[1]+1) / self.start
                else:
                    self.start = obj[0]
                    self.d = obj[1] / self.start
            else:
                self.start = 1
                self.d = 2
        else:
            if args[0] == 0:
                self.start = args[0] + 1
                self.d = (args[1]+1) / self.start
            else:
                self.start = args[0]
                self.d = args[1] / self.start

    def getElem(self, number):
        s = copy(self.start)
        for i in range(number):
            s *= self.d
        return s
    
    def getSum(self, number):
        lst = []
        s = copy(self.start)
        for i in range(number):
            s *= self.d
            lst.append(copy(s))
        return sum(lst)

    def setIter(self, value):
        self.value = value

    def __iter__(self):
        for i in range(self.value):
            yield self.getElem(i)

    def __str__(self):
        return "<GeometricSequence (%s, %s, %s, %s, ...)>" % (self.getElem(0), self.getElem(1), self.getElem(2), self.getElem(3))


class Vector2:
    def __init__(self, *args):
        if len(args) == 0:
            self.a = self.b = Point(0, 0)
        elif len(args) == 1:
            obj = args[0]
            if type(obj) == Vector2:
                self.a = copy(obj.a)
                self.b = copy(obj.b)
            elif type(obj) == list or type(obj) == tuple:
                if len(obj) == 0:
                    self.a = self.b = Point(0, 0)
                elif len(obj) == 1:
                    self.a = Point(copy(obj[0]))
                    self.b = copy(self.a)
                else:
                    self.a = Point(copy(obj[0]))
                    self.b = Point(copy(obj[1]))
            elif type(obj) == Point:
                self.a = copy(obj.points[0])
                self.b = copy(obj.points[1])
            else:
                self.a = self.b = Point(0, 0)
        else:
            self.a = Point(copy(args[0]))
            self.b = Point(copy(args[1]))

    def length(self):
        return self.a.euclideanDistance(self.b)

    def offset(self, what, x, y):
        if what == self.a:
            self.a.points[0] += x
            self.a.points[1] += y
        elif what == self.b:
            self.b.points[0] += x
            self.b.points[1] += y

    def isNullVector(self):
        return self.a.points == self.b.points

    def getDirection(self):
        p1 = self.a.points
        p2 = self.b.points
        direction = (p2[0]-p1[0])/((p2[0]-p1[0])**2 + (p2[1]-p1[1])**0.5)
        dr = "%s" % direction
        print(dr)
        return float(direction) if not dr.endswith("j") else float(dr[:-1])

    def __mul__(self, other):
        if type(other) == int or type(other) == float:
            self.b.points[0] *= other
            self.b.points[1] *= other
        elif type(other) == Vector2:
            self.b.points[0] *= other.b.points[0]
            self.b.points[1] *= other.b.points[1]
        elif type(other) == Point:
            self.b.points[0] *= other.points[0]
            self.b.points[1] *= other.points[1]
        return self

    def __imul__(self, other):
        return self.__mul__(other)

    def __str__(self):
        return "<Vector2 A(%s, %s), B(%s, %s)>" % (self.a.points[0], self.a.points[1],
                                                self.b.points[0], self.b.points[1])


class Rectangle:
    def __init__(self, *args):
        if len(args) == 4:
            self.left, self.top, self.right, self.bottom = args
        elif len(args) == 1:
            if type(args[0]) == Rectangle:
                self.left, self.top, self.right, self.bottom = copy(args[0].left), copy(args[0].top), copy(args[0].right), copy(args[0].bottom)

    def containsPoint(self, point):
        x = point.points[0]
        y = point.points[1]
        return self.left < x < self.right and self.top < y < self.bottom

    def containsXY(self, x, y):
        return self.left < x < self.right and self.top < y < self.bottom

    def equalsPoint(self, point):
        x = point.points[0]
        y = point.points[1]
        return self.left <= x <= self.right and self.top <= y <= self.bottom

    def equalsXY(self, x, y):
        return self.left <= x <= self.right and self.top <= y <= self.bottom

    def width(self): return self.right - self.left
    def height(self): return self.bottom - self.top

    def __str__(self):
        return "<Rectangle (%s, %s, %s, %s)>" % (self.left, self.top, self.right, self.bottom)
