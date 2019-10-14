# -*- coding: utf-8 -*-
# author: ethosa
from copy import copy, deepcopy
from .Point import Point
import math


class Vector2:
    def create(list1, list2):
        """vreate vector
        
        Arguments:
            list1 {[number, number]} -- first point
            list2 {[number, number]} -- second point
        
        Returns:
            [Vector2]
        """
        vector2 = Vector2(list1, list2)
        return vector2

    def __init__(self, point1, point2):
        """create vector 2d
        
        Arguments:
            point1 {[number, number]} -- first point
            point2 {[number, number]} -- second point
        """
        self.a = Point(point1)
        self.b = Point(point2)

    def length(self):
        """getting vector length
        
        Returns:
            [float] -- [length of vector]
        """
        return self.a.euclideanDistance(self.b)

    def getMiddlePoint(self):
        x = (self.a.points[0]+self.b.points[0])/2
        y = (self.a.points[1]+self.b.points[1])/2
        return Point(x, y)

    def offset(self, what, x, y):
        """offset point
        
        Arguments:
            what {[Vector point]} -- [vector.a or vector.b]
            x {[number]} -- [offset x]
            y {[number]} -- [offset y]
        """
        if what == self.a:
            self.a.points[0] += x
            self.a.points[1] += y
        elif what == self.b:
            self.b.points[0] += x
            self.b.points[1] += y

    def isNullVector(self):
        return self.a.points == self.b.points

    def getDirection(self):
        """get vector direction
        
        Returns:
            [complex number or float] -- [direction]
        """
        p1 = self.a.points
        p2 = self.b.points
        direction = (p2[0]-p1[0])/((p2[0]-p1[0])**2 + (p2[1]-p1[1])**0.5)
        return direction

    def __mul__(self, other):
        if isinstance(obj, int) or isinstance(obj, float):
            self.b.points[0] *= other
            self.b.points[1] *= other
            self.a.points[0] *= other
            self.a.points[1] *= other
        return self

    def __imul__(self, other):
        return self.__mul__(other)

    def __str__(self):
        return "<Vector2 A(%s, %s), B(%s, %s)>" % (self.a.points[0], self.a.points[1],
                                                self.b.points[0], self.b.points[1])
