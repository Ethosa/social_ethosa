# -*- coding: utf-8 -*-
# author: Ethosa
from .eList import EList
from random import choices, choice
import asyncio

class MarkovChains:
    def __init__(self):
        self.chains = {}
        self.execute = lambda string: asyncio.run(self.executing(string))
        self.deleteChain = lambda name: asyncio.run(self.deleteChainA(name))
        self.generateSequence = lambda length, auth=None: asyncio.run(self.generateSequenceA(length, auth))

    def addChain(self, name, value, weight=1):
        if name not in self.chains:
            self.chains[name] = [[value, weight]]
        else:
            self.chains[name].append([value, weight])

    async def deleteChainA(self, name):
        for key in self.chains:
            ns = [i[0] for i in self.chains[key]]
            ws = [i[1] for i in self.chains[key]]
            i = 0
            while name in ns:
                index = ns.index(name) + i
                o = [ns[index], ws[index]]
                self.chains[key].remove(o)
                ns.pop(index)
                ws.pop(index)
                i -= 1
        del self.chains[name]

    async def generateSequenceA(self, length, auth=None):
        out = []
        if not auth:
            auth = choice([key for key in self.chains])
        current = self.chains[auth]
        for now in range(length):
            key = choices([i[0] for i in current], weights=[i[1] for i in current])[0]
            current = self.chains[key]
            out.append(key)
        return out

    async def executing(self, string):
        out = string.replace("=", "-").split("-")
        for i in range(len(out)):
            current = out[i]
            next_ = None
            lasted = None
            if i-1 > -1:
                lasted = out[i-1]
            if i+1 < len(out)-1:
                next_ = out[i+1]
            c = current[:].replace(">", "").replace("<", "").strip()
            if lasted:
                l = lasted[:].replace(">", "").replace("<", "").strip()
            if next_:
                n = next_[:].replace(">", "").replace("<", "").strip()
            if current.endswith("<") and next_:
                if n not in self.chains:
                    self.addChain(n, c)
                else:
                    if c not in [i[0] for i in self.chains[n]]:
                        self.addChain(n, c)
            if current.startswith(">") and lasted:
                if l not in self.chains:
                    self.addChain(l, c)
                else:
                    if c not in [i[0] for i in self.chains[l]]:
                        self.addChain(l, c)
            if not current.endswith("<") and not current.endswith(">") and next_:
                if c not in self.chains:
                    self.addChain(c, n)
                else:
                    if n not in [i[0] for i in self.chains[c]]:
                        self.addChain(c, n)
