# -*- coding: utf-8 -*-
# author: Ethosa

from ..utils import *

class EList:
    __metaclass__ = list
    def __init__(self, *args):
        """custom list create
        
        Keyword Arguments:
            lst {list} -- [object for create list] (default: {[]})
        """
        if len(args) == 1:
            lst = args[0]
            if isinstance(lst, eList):
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

    def sum(self): return sum(self.lst)

    def extend(self, lst):
        if isinstance(other, list) or isinstance(other, eList):
            for i in other:
                self.append(i)

    def __set__(self, value):
        if isinstance(value, eList) or isinstance(value, list):
            self.__init__(value)
        else:
            raise ValueError("%s isn't list object" % value)

    def reverse(self):
        self.lst = self.lst[::-1]

    def sort(self, key):
        return self.lst.sort(key)

    def clear(self):
        self.lst = []

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
        return eList(splitList(self.lst, number))

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
        elif isinstance(other, eList):
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
        return eList(self.lst[::-1])
    def reversed(self): return self.__reversed__()

    def __contains__(self, val):
        return val in self.lst
    def contains(self, val):
        return self.__contains__(val)

    def __instancecheck__(self, instance):
        return isinstance(instance, eList)

    def __bool__(self):
        return True if self.lst else False
    def bool(self): return self.__bool__()

    def __add__(self, other):
        if isinstance(other, list) or isinstance(other, eList):
            out = eList(self)
            for i in other:
                out.append(i)
            return out
        elif isinstance(other, int) or isinstance(other, float):
            out = eList(self)
            out.append(other)
            return out

    def __iadd__(self, other):
        return self.__add__(other)
