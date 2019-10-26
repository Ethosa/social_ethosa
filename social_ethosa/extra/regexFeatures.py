# -*- coding: utf-8 -*-
# author: Ethosa

import textwrap
import re

class RegExp:
    def __init__(self, text=""):
        self.text = text

    def findEmail(self, text=""):
        if text:
            self.text = text
        return re.findall("\S*@\S*", text)

    def findPhone(self, text=""):
        if text:
            self.text = text
        numbers = re.findall(r"\d{10,}", text)
        out = []
        for n in numbers:
            n = n[::-1]
            out.append(("%s-%s-%s-)%s( %s" % (n[:2], n[2:4], n[4:7], n[7:10], n[10:]))[::-1])
        return (out, numbers)

    def findUrl(self, text=""):
        if text:
            self.text = text
        return re.findall("https://\w+\.\w{2,}\S*", text)
