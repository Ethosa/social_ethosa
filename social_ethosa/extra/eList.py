# -*- coding: utf-8 -*-
# author: Ethosa

from ..utils import *
from copy import copy
import math

class EList:
    __metaclass__ = list
    COMB_SORT = 0
    GNOME_SORT = 1
    ODD_EVEN_SORT = 2
    def __init__(self, *args):
        """custom list create
        
        Keyword Arguments:
            lst {list} -- [object for create list] (default: {[]})
        """
        if len(args) == 1:
            lst = args[0]
            if isinstance(lst, EList):
                self.lst = list(lst.lst[:])
            else:
                self.lst = list(lst)
        elif len(args) == 0:
            self.lst = []
        else:
            self.lst = list(args)
        self.sitem = 0

    def pop(self, num=-1):
        self.lst.pop(num)

    def append(self, val):
        self.lst.append(val)

    def insert(self, pos, val):
        self.lst.insert(pos, val)

    def remove(self, val):
        self.lst.remove(val)

    def index(self, val, start=0, end=-1):
        return self.lst.index(val, start, end)

    def count(self, val):
        return self.lst.count(val)

    def sum(self): return math.fsum(self.lst)

    def extend(self, lst):
        if isinstance(other, list) or isinstance(other, EList):
            for i in other:
                self.append(i)

    def __set__(self, value):
        if isinstance(value, EList) or isinstance(value, list):
            self.__init__(value)
        else:
            raise ValueError("%s isn't list object" % value)

    def reverse(self):
        self.lst = self.lst.reverse()

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

    def sort(self, key):
        return self.lst.sort(key)

    def sortA(self, method, reverse=False):
        if method == EList.COMB_SORT:
            alen = len(self.lst)
            gap = (alen * 10 // 13) if alen > 1 else 0
            while gap:
                if 8 < gap < 11:    ## variant "comb-11"
                    gap = 11
                swapped = False
                for i in range(alen - gap):
                    if self.lst[i + gap] < self.lst[i]:
                        self.lst[i], self.lst[i + gap] = self.lst[i + gap], self.lst[i]
                        swapped = True
                gap = (gap * 10 // 13) or swapped
        elif method == EList.GNOME_SORT:
            pos = 0
            while pos < len(self.lst):
                if pos == 0 or self.lst[pos] >= self.lst[pos-1]:
                    pos += 1
                else:
                    self.swap(pos, pos-1)
                    pos -= 1
        elif method == EList.ODD_EVEN_SORT:
            srtd = 0
            while not srtd:
                srtd = 1
                for i in range(1, len(self.lst)-1):
                    if self.lst[i] > self.lst[i + 1]:
                        self.swap(i, i+1)
                        srtd = 0
                for i in range(0, len(self.lst)-1):
                    if self.lst[i] > self.lst[i + 1]:
                        self.swap(i, i+1)
                        srtd = 0
        if reverse:
            self.lst = self.lst[::-1]

    def clear(self):
        self.lst = []

    def swap(self, i, j):
        o = copy(self.lst[i])
        self.lst[i] = copy(self.lst[j])
        self.lst[j] = o

    def __setitem__(self, item, value):
        if isinstance(item, int):
            if item > len(self.lst)-1:
                while item > len(self.lst)-1:
                    self.lst.append(self.sitem)
                self.lst[item] = value
            else:
                self.lst[item] = value

    def __getitem__(self, index):
        return self.lst[index]

    def standartItem(self, item):
        self.sitem = item

    def split(self, number=1):
        return EList(splitList(self.lst, number))

    def copy(self):
        return self.lst[:]

    def __str__(self): return "%s" % self.lst
    def str(self): return self.__str__()

    def __repr__(self): return "%s" % self.lst
    def repr(self): return self.__repr__()

    def __len__(self): return len(self.lst)
    def len(self): return len(self.lst)

    def __eq__(self, other):
        if isinstance(other, list):
            return self.lst == other
        elif isinstance(other, EList):
            return self.lst == other.lst
        else:
            return 0
    def equals(self, other):
        return self.__eq__(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __iter__(self):
        for i in self.lst:
            yield i

    def __reversed__(self):
        return EList(self.lst[::-1])
    def reversed(self): return self.__reversed__()

    def __contains__(self, val):
        return val in self.lst
    def contains(self, val):
        return self.__contains__(val)

    def __instancecheck__(self, instance):
        return isinstance(instance, EList)

    def __bool__(self):
        return True if self.lst else False
    def bool(self): return self.__bool__()

    def __add__(self, other):
        if isinstance(other, list) or isinstance(other, EList):
            out = EList(self)
            for i in other:
                out.append(i)
            return out
        elif isinstance(other, int) or isinstance(other, float):
            out = EList(self)
            out.append(other)
            return out

    def __iadd__(self, other):
        return self.__add__(other)
