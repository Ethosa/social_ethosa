# -*- coding: utf-8 -*-
# author: Ethosa

class AMarkov:
    def __init__(self, rules={}, text=""):
        self.rules = rules
        self.text = text

    def compile(self, text=None):
        if not text:
            text = self.text[:]
        for rule in self.rules:
            text = text.replace(rule, self.rules[rule], 1)
        for rule in self.rules:
            if rule in text:
                text = self.compile(text)
        return text

    def setText(self, text):
        self.text = text

    def addRule(self, key, value):
        self.rules[key] = value

    def delRule(self, key):
        del self.rules[key]