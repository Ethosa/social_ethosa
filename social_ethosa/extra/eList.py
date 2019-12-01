# -*- coding: utf-8 -*-
# author: Ethosa

from ..utils import *
from copy import copy
import math

class EList(list):
    COMB_SORT = 0
    GNOME_SORT = 1
    ODD_EVEN_SORT = 2
    def __init__(self, arg):
        super().__init__(arg)
        self.sitem = 0

    def sum(self):
        return math.fsum(self)

    def __set__(self, value):
        if isinstance(value, EList) or isinstance(value, list):
            self = value
        else:
            raise ValueError("%s isn't list object" % value)

    def binarySearch(self, T):
        n = len(self)-1
        L = 0
        R = n - 1
        while L <= R:
            m = (L + R) // 2
            if self[m] < T:
                L = m + 1
            elif self[m] > T:
                R = m - 1
            else:
                return m

    def interpolationSearch(self, key):
        low = 0
        high = len(self)-1
        mid = None
        while self[high] != self[low] and key >= self[low] and key <= self[high]:
            mid = low + ((key - self[low]) * (high - low) // (self[high] - self[low]))

            if self[mid] < key:
                low = mid + 1
            elif key < self[mid]:
                high = mid - 1
            else: return mid

        if key == self[low]: return low
        else: return None

    def sortMethod(self, method, reverse=False):
        if method == EList.COMB_SORT:
            alen = len(self)
            gap = (alen * 10 // 13) if alen > 1 else 0
            while gap:
                if 8 < gap < 11:
                    gap = 11
                swapped = False
                for i in range(alen - gap):
                    if self[i + gap] < self[i]:
                        self[i], self[i + gap] = self[i + gap], self[i]
                        swapped = True
                gap = (gap * 10 // 13) or swapped

        elif method == EList.GNOME_SORT:
            pos = 0
            while pos < len(self):
                if pos == 0 or self[pos] >= self[pos-1]:
                    pos += 1
                else:
                    self.swap(pos, pos-1)
                    pos -= 1

        elif method == EList.ODD_EVEN_SORT:
            srtd = 0
            while not srtd:
                srtd = 1
                for i in range(1, len(self)-1):
                    if self[i] > self[i + 1]:
                        self.swap(i, i+1)
                        srtd = 0
                for i in range(0, len(self)-1):
                    if self[i] > self[i + 1]:
                        self.swap(i, i+1)
                        srtd = 0
        if reverse:
            self = self[::-1]

    def swap(self, i, j):
        o = copy(self[i])
        self[i] = copy(self[j])
        self[j] = o

    def __setitem__(self, item, value):
        if not item > len(self)-1:
            super().__setitem__(item, value)
        else:
            while item > len(self)-1:
                self.append(self.sitem)
            self.__setitem__(item, value)

    def setStandartItem(self, item):
        self.sitem = item

    def split(self, number=1):
        return EList(splitList(self, number))

    def str(self):
        return self.__str__()

    def repr(self):
        return self.__repr__()

    def len(self):
        return len(self)

    def equals(self, other):
        return self.__eq__(other)

    def reversed(self):
        return self.__reversed__()

    def contains(self, val):
        return self.__contains__(val)

    def bool(self):
        return self.__bool__()
