# -*- coding: utf-8 -*-
# author: Ethosa
from random import choice


class MarkovChains:
    def __init__(self):
        self.chains = {}
        self.magic = lambda s: s.lstrip(">").rstrip("<").strip()

    def addChain(self, name, value):
        """Adds a new chain.

        Arguments:
            name {str} -- chain name
            value {str} -- other chain name
        """
        if name not in self.chains:
            self.chains[name] = [value]
        else:
            self.chains[name].append(value)

    def deleteChain(self, name):
        """Removes all links to this chain.

        Arguments:
            name {str} -- chain name
        """
        for key in self.chains:
            while name in self.chains[key]:
                self.chains[key].remove(name)
        del self.chains[name]

    def generateSequence(self, length, auth=None):
        """generates a list, selects random keys from a dictionary

        Arguments:
            length {int} -- list length

        Keyword Arguments:
            auth {str} -- the key from which the generation begins.
                If not cauldron, then randomly selected (default: {None})

        Returns:
            list -- generated list
        """
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
        """Adds new chains based on the passed string

        Arguments:
            string {str} -- string to execute

        Example using:
            execute("z => y <=> x <= z")
            this is equivalent to the following code:
            addChain("z", "y")
            addChain("y", "x")
            addChain("x", "y")
            addChain("z", "x")
        """
        out = string.replace("=", "-").split("-")
        for i, current in enumerate(out):
            post = out[i+1] if i < len(out)-1 else None
            pre = out[i-1] if i > 0 else None
            if current.endswith("<") and post:
                self.addChain(self.magic(post), self.magic(current))
            if current.startswith(">") and pre:
                self.addChain(self.magic(pre), self.magic(current))
            if not current.endswith("<") and not current.endswith(">") and post:
                self.addChain(self.magic(current), self.magic(post))
