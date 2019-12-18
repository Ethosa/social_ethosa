# -*- coding: utf-8 -*-
# author: Ethosa
from random import choice


class MarkovChains:
    def __init__(self):
        self.chains = {}
        self.magic = lambda s: s.lstrip(">").rstrip("<").strip()

    def addChain(self, name, value):
        if name not in self.chains:
            self.chains[name] = [value]
        else:
            self.chains[name].append(value)

    def deleteChain(self, name):
        for key in self.chains:
            while name in self.chains[key]:
                self.chains[key].remove(name)
        del self.chains[name]

    def generateSequence(self, length, auth=None):
        if not auth:
            auth = choice([key for key in self.chains])
        current = self.chains[auth]
        out = []
        for now in range(length):
            key = choice(current)
            current = self.chains[key]
            out.append(key)
        return out

    def execute(self, string):
        out = string.replace("=", "-").split("-")
        for i in range(len(out)):
            current = out[i]
            post = out[i+1] if i < len(out)-1 else None
            pre = out[i-1] if i > 0 else None
            if current.endswith("<") and post:
                self.addChain(self.magic(post), self.magic(current))
            if current.startswith(">") and pre:
                self.addChain(self.magic(pre), self.magic(current))
            if not current.endswith("<") and not current.endswith(">") and post:
                self.addChain(self.magic(current), self.magic(post))
