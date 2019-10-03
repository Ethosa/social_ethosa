from copy import copy
import math

class Matrix:
    def __init__(self, *args):
        if len(args) == 2:
            self.width, self.height = args
            self.obj = [[0 for x in range(self.width)] for y in range(self.height)]
        elif len(args) == 1:
            if type(args[0]) == Matrix:
                self.width, self.height = args[0].width, args[0].height
                self.obj = args[0].obj
            if type(args[0]) == list or type(args[0]) == tuple:
                self.width = len(args[0])
                self.height = len(args[0][0])
                self.obj = args[0]

    def clear(self):
        for x in range(self.width):
            for y in range(self.height):
                self.obj[x][y] = 0

    def setAt(self, x, y, value):
        self.obj[x][y] = value

    def getAt(self, x, y):
        return self.obj[x][y]

    def transpose(self):
        width = self.height
        height = self.width
        self.obj = [[self.obj[x][y] for x in range(self.height)] for y in range(self.width)]
        self.width = width
        self.height = height

    def __neg__(self):
        obj = copy(self.obj)
        for x in range(self.width):
            for y in range(self.height):
                obj[x][y] = obj[x][y] * -1
        return Matrix(obj)

    def __add__(self, other):
        for x in range(self.width):
            for y in range(self.height):
                self.obj[x][y] += other.obj[x][y]

    def __iadd__(self, other):
        obj = copy(self.obj)
        for x in range(self.width):
            for y in range(self.height):
                obj[x][y] += other.obj[x][y]
        return Matrix(obj)

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
            if len(other) == len(self):
                if len(self.obj[0]) == len(other.obj[0]):
                    return 1
                else: return 0
            else: return 0
        else: return 0


class Point:
    def __init__(self, *args):
        if len(args) == 1:
            if type(args[0]) == Point:
                self.points = args[0].points
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

    def __str__(self):
        return "<Point %s>" % self.points
