# -*- coding: utf-8 -*-
# author: ethosa
from copy import copy, deepcopy
from .Point import Point
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
            self.obj = [[0 for x in range(self.height)] for y in range(self.width)]
            self.widthFill = 1
        elif len(args) == 1:
            if isinstance(args[0], Matrix):
                self.width, self.height = copy(args[0].width), copy(args[0].height)
                self.obj = args[0].obj[:]
                self.widthFill = copy(args[0].widthFill)
            if isinstance(args[0], list) or isinstance(args[0], tuple):
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
        self.obj[x][y] = value
        if len("%s" % value) > self.widthFill:
            self.widthFill = len("%s" % value)

    def getAt(self, x, y):
        return self.obj[x][y]

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
            self.obj[x] = [i for i in self.obj[x][::-1]]
        self.obj = [i for i in self.obj[::-1]]
        for x in range(self.width):
            for y in range(self.height):
                a, b = obj[x][y], self.obj[x][y]
                if a < 0 and b > 0 or a > 0 and b < 0:
                    self.obj[x][y] *= -1

    def rotate(self, angle, f=0):
        offsetX = offsetY = 10
        aRad = 180*angle/math.pi
        rMx = ((math.cos(aRad), -math.sin(aRad)), (math.sin(aRad), math.cos(aRad)))
        matrix = Matrix(self.width+self.width, self.height+self.width)
        matrix.fill(f)
        for y in range(self.height):
            for x in range(self.width):
                tx = (x-offsetX)*rMx[0][0] + (y-offsetY)*rMx[0][1] + offsetX
                ty = (x-offsetX)*rMx[1][0] + (y-offsetY)*rMx[1][1] + offsetY
                itx = int(tx)
                ity = int(ty)
                # rtx = round(tx)
                # rty = round(ty)
                # mtx = math.ceil(tx)
                # mty = math.ceil(ty)
                # if not [itx, ity] in timed:
                if itx < -self.width:
                    itx += self.width//2
                if ity < -self.height:
                    ity += self.height//2
                matrix.obj[itx][ity] = self.obj[x][y]
                    # timed.append([itx, ity])
                # elif not [rtx, rty] in timed:
                #     matrix.obj[rtx][rty] = self.obj[x][y]
                #     timed.append([rtx, rty])
                # elif not [mtx, mty] in timed:
                #     matrix.obj[mtx][mty] = self.obj[x][y]
                #     timed.append([mtx, mty])
            print(y)
        return matrix
        

    def lol(self):
        offset = [1, self.height-1]
        result = [0, 0, 0, 0]
        for y in range(self.height//2):
            for x in range(offset[0], offset[1]):
                result[0] += self.obj[y][x]
            offset[0] += 1
            offset[1] -= 1
        offset = [1, self.height-1]
        for y in range(self.height-1, self.height//2, -1):
            for x in range(offset[0], offset[1]):
                result[1] += self.obj[y][x]
            offset[0] += 1
            offset[1] -= 1
        obj = Matrix(self)
        obj.transpose()
        offset = [1, obj.height-1]
        for y in range(obj.height//2):
            for x in range(offset[0], offset[1]):
                result[2] += obj.obj[y][x]
            offset[0] += 1
            offset[1] -= 1
        offset = [1, obj.height-1]
        for y in range(obj.height-1, obj.height//2, -1):
            for x in range(offset[0], offset[1]):
                result[3] += obj.obj[y][x]
            offset[0] += 1
            offset[1] -= 1
        return result

    def scale(self, number):
        if isinstance(number, float):
            number = round(number)
        if isinstance(number, int):
            w, h = self.width*number, self.height*number
            matrix = Matrix(w, h)
            if number > 0:
                for x in range(self.width):
                    for y in range(self.height):
                        x1 = [i for i in range(x*number, x*number+number)]
                        y1 = [i for i in range(y*number, y*number+number)]
                        for i, j in zip(x1, y1):
                            matrix.obj[i][j] = self.obj[x][y]
                            for offset in range(1, number):
                                if i+offset < w:
                                    matrix.obj[i+offset][j] = self.obj[x][y]
                                if j+offset < h:
                                    matrix.obj[i][j+offset] = self.obj[x][y]
            else:
                obj = []
                c = 0
                for x in range(0, self.width, -number):
                    obj.append([])
                    for y in range(0, self.height, -number):
                        obj[c].append(self.obj[x][y])
                    c += 1
                matrix = Matrix(obj)
        return matrix

    def flip(self):
        obj = []
        for x in range(self.width):
            obj.append(self.obj[x][:])
            self.obj[x] = [i for i in self.obj[x][::-1]]
        self.obj = [i for i in self.obj[::-1]]

    def search(self, value):
        for x in range(self.width):
            for y in range(self.height):
                if self.obj[x][y] == value:
                    return [x, y]

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

    def determinant(self):
        if self.width == 2 == self.height:
            return self.obj[0][0]*self.obj[1][1] - self.obj[0][1]*self.obj[1][0]

    def __neg__(self):
        obj = copy(self.obj)
        for x in range(self.width):
            for y in range(self.height):
                obj[x][y] = obj[x][y]*-1
        return Matrix(obj)

    def __add__(self, other):
        obj = copy(self.obj)
        if isinstance(other, Matrix):
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
        elif isinstance(other, int):
            for x in range(self.width):
                for y in range(self.height):
                    self.obj[x][y] *= other
            return self
        elif isinstance(other, Matrix):
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
        if isinstance(other, Matrix):
            if other.obj == self.obj: return 1
            else: return 0
        else: return 0

    def __str__(self):
        return "%s\n" % "\n".join(" ".join("%s" % i if len("%s" % i) == self.widthFill else
                                    "%s%s" % (" "*(self.widthFill-len("%s" % i)), i) if len("%s" % i) < 6 else "%s" % i
                                    for i in self.obj[x])
                        for x in range(len(self.obj)))