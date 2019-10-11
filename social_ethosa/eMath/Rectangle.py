# -*- coding: utf-8 -*-
# author: ethosa
from copy import copy, deepcopy
from .Point import Point
import math


class Rectangle:
    def __init__(self, *args):
        if len(args) == 4:
            self.left, self.top, self.right, self.bottom = args
        elif len(args) == 1:
            if isinstance(args[0], Rectangle):
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
