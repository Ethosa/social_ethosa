# -*- coding: utf-8 -*-
# author: Ethosa

from copy import copy
import asyncio
import random

class EQueue:
    def __init__(self):
        self.queue = []
        self.getNext = lambda: asyncio.run(self.getNextA())
        self.getLast = lambda: asyncio.run(self.getLastA())
        self.getRandom = lambda: asyncio.run(self.getRandomA())
        self.len = lambda: asyncio.run(self.lenA())
        self.onNewObject = lambda: None

    async def getNextA(self):
        if self.queue:
            n = copy(self.queue[0])
            self.queue.pop(0)
            return n

    async def getLastA(self):
        if self.queue:
            n = copy(self.queue[-1])
            self.queue.pop()
            return n

    async def getRandomA(self):
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

    async def lenA(self):
        return len(self.queue)

    def __len__(self):
        return len(self.queue)

    def __iter__(self):
        for i in range(len(self.queue)):
            yield self.getNext()
