# -*- coding: utf-8 -*-
# author: Ethosa

import textwrap
import re

class Regexp:
    def __init__(self, text=""):
        self.text = text

    def findEmail(self, text=""):
        if not text:
            text = self.text
        return re.findall(r"\S*@\S*", text)

    def findPhone(self, text=""):
        if not text:
            text = self.text
        numbers = re.findall(r"\+?\d{11,}", text)
        out = []
        for n in numbers:
            n = n[::-1]
            out.append(("%s-%s-%s-)%s( %s" % (n[:2], n[2:4], n[4:7], n[7:10], n[10:]))[::-1])
        return (out, numbers)

    def findUrl(self, text=""):
        if not text:
            text = self.text
        return re.findall(r"https://\S+\.\S+", text)
