# -*- coding: utf-8 -*-
# author: ethosa
from .Point import Point
from .Point2D import Point2D

class Path:
    def __init__(self, *args):
        self.path = [i if isinstance(i, Point) or isinstance(i, Point2D) else
                    Point(i) if isinstance(i, list) else i for i in args]

    def add(self, pnt):
        self.path.append(pnt if isinstance(pnt, Point) or isinstance(pnt, Point2D) else
                    Point(pnt) if isinstance(pnt, list) else pnt)

    def length(self):
        l = 0
        for p in range(len(self.path)):
            if p+1 < len(self.path):
                l += self.path[p].euclideanDistance(self.path[p+1])
        return l

    def __eq__(self, other):
        if isinstance(other, Path):
            return self.path == other.path

    def __gt__(self, other):
        if isinstance(other, Path):
            return self.length() > other.length()

    def __lt__(self, other):
        if isinstance(other, Path):
            return self.length() < other.length()

    def __iter__(self):
        for point in self.path:
            yield point

    def __str__(self):
        return "<Path %s>" % (" => ".join(["%s" % i for i in self.path]))
