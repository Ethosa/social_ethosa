# -*- coding: utf-8 -*-
# author: ethosa
from copy import copy, deepcopy
import math

class ArithmeticSequence:
    def __init__(self, *args):
        if len(args) == 0:
            self.start = 0
            self.d = 1
        elif len(args) == 1:
            obj = args[0]
            if isinstance(obj, ArithmeticSequence):
                self.start = copy(obj.start)
                self.d = copy(obj.d)
            elif isinstance(obj, list) or isinstance(obj, tuple):
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
            if isinstance(obj, GeometricSequence):
                self.start = copy(obj.start)
                self.d = copy(obj.start)
            elif isinstance(obj, list) or isinstance(obj, tuple):
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