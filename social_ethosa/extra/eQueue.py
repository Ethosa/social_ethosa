# -*- coding: utf-8 -*-
# author: Ethosa

from copy import copy
import random

class EQueue:
    def __init__(self):
        self.queue = []
        self.onNewObject = lambda: None

    def getNext(self):
        if self.queue:
            n = copy(self.queue[0])
            self.queue.pop(0)
            return n

    def getLast(self):
        if self.queue:
            n = copy(self.queue[-1])
            self.queue.pop()
            return n

    def getRandom(self):
        if self.queue:
            number = random.randint(0, len(self.queue)-1)
            n = copy(self.queue[number])
            self.queue.pop(number)
            return n

    def onAdd(self, function):
        self.onNewObject = lambda: function()

    def add(self, val):
        self.queue.append(val)
        self.onNewObject()

    def iter(self):
        for i in range(len(self.queue)):
            yield self.getNext()

    def len(self):
        return len(self.queue)

    def __len__(self):
        return len(self.queue)

    def __iter__(self):
        for i in range(len(self.queue)):
            yield self.getNext()
