# -*- coding: utf-8 -*-
# author: ethosa
from copy import copy, deepcopy
from .Point import Point
import math

class Point2D(Point):
    def __init__(self, x, y):
        super(Point2D, self).__init__(x, y)
        self.x = self.points[0]
        self.y = self.points[1]