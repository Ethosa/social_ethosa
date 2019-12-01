# -*- coding: utf-8 -*-
# author: Ethosa

from copy import copy
from random import randint

class EQueue:
    def __init__(self):
        """constructor for EQueue
        """
        self.queue = []
        self.onNewObject = lambda: None

    def getNext(self):
        """get first object in queue
        
        Returns:
            any
        """
        if self.queue:
            return self.queue.pop(0)

    def getLast(self):
        """get last object in queue
        
        Returns:
            any
        """
        if self.queue:
            return self.queue.pop()

    def getRandom(self):
        """get random object in queue
        
        Returns:
            any
        """
        if self.queue:
            return self.queue.pop(randint(0, len(self)-1))

    def onAdd(self, function):
        """call function on added new object
        
        Arguments:
            function {function, method or class} -- callable object
        """
        self.onNewObject = function

    def add(self, val):
        """add new object in queue
        
        Arguments:
            val {any}
        """
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

    def __str__(self):
        return "<EQueue with %s items>" % len(self)
