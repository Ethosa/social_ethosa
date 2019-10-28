# -*- coding: utf-8 -*-
# author: ethosa
from ..utils import getValue
from operator import itemgetter, attrgetter
import requests
import datetime
import pickle
import random
import time
import json
import math
import os
import re

def strTimeProp(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(format, time.localtime(ptime))
def randomDate(start, end, prop):
    return strTimeProp(start, end, '%d.%m.%Y %H:%M:%S', prop)

class BotWrapper(object):

    """
    docstring for BotWrapper

    usage:
    from social_ethosa.botwrapper import BotWrapper

    botWrapper = BotWrapper()

    print(botWrapper.randomDate())
    print("chance is %s" % botWrapper.randomChance())
    """

    def __init__(self):
        self.count_use = 0
        self.validate_for_calc = list('1234567890^-+/*')
        self.eng = list('''QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?qwertyuiop[]asdfghjkl;'zxcvbnm,./&''')
        self.rus = list('''ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,йцукенгшщзхъфывапролджэячсмитьбю.?''')
        self.eng_rus = {self.eng[i] : self.rus[i] for i in range(len(self.rus))}
        self.rus_eng = {self.rus[i] : self.eng[i] for i in range(len(self.rus))}
        self.smiles = ["&#127815;", "&#127821;", "&#127826;", "&#127827;"]

    def randomDate(self, fromYear="2001", toYear="3001"):
        """generate random date
        
        Keyword Arguments:
            fromYear {str} -- [start generate year] (default: {"2001"})
            toYear {str} -- [end generate year] (default: {"3001"})
        
        Returns:
            [str] -- [generated date]
        """
        self.count_use += 1
        return randomDate("01.01.%s 00:00:00" % fromYear, "01.01.%s 00:00:00" % toYear, random.random())

    def randomChance(self):
        """generate random chance
        Returns:
            [str] -- [generated chance (7%)]
        """
        self.count_use += 1
        return "%s%%" % random.randint(0, 100)

    def yesOrNo(self):
        """return random yes or no
        
        Returns:
            [str] -- [yes or no]
        """
        self.count_use += 1
        return random.choice(["Да", "Нет"])

    def textReverse(self, text):
        # привет -> тевирп
        self.count_use += 1
        return text[::-1]

    def space(self, text):
        # привет -> п р и в е т
        self.count_use += 1
        return ' '.join(list(text))

    def translit(self, text):
        # ghbdtn -> привет
        self.count_use += 1
        return ''.join([self.rus_eng[i] if i in self.rus_eng else self.eng_rus[i] if i in self.eng_rus else i for i in text])

    def delirium(self, number=1):
        """generate random text
        
        Keyword Arguments:
            number {number} -- [number of sentense] (default: {1})
        
        Returns:
            [str] -- [generated text]
        """
        self.count_use += 1
        resp = requests.get("https://fish-text.ru/get?type=sentence&number=%s&format=json" % number)
        resp.encoding = resp.apparent_encoding
        return json.loads(resp.text)['text']

    def calc(self, text):
        """calculator
        
        Arguments:
            text {[str]} -- [example for calculation]
        
        Returns:
            [str] -- [result]
        """
        self.count_use += 1
        text = text.replace("^", "**") # ''.join(i for i in text if i in self.validate_for_calc)
        glb = {
            "pi" : math.pi, "e" : math.e,
            "sin" : math.sin, "cos" : math.cos,
            "factorial" : math.factorial, "ceil" : math.ceil,
            "floor" : math.floor, "floor" : math.floor,
            "pow" : math.pow, "log" : math.log,
            "sqrt" : math.sqrt, "tan" : math.tan,
            "arccos" : math.acos, "arcsin" : math.asin,
            "arctan" : math.atan, "degrees" : math.degrees,
            "radians" : math.radians, "sinh" : math.sinh,
            "cosh" : math.cosh, "tanh" : math.tanh,
            "arccosh" : math.acosh, "arcsinh" : math.asinh,
            "arctanh" : math.atanh, 'print' : lambda *args: " ".join(args),
            'exit' : lambda *args: " ".join(args)
        }
        return eval(text, glb, {})

    def casino(self):
        # It method return tuple, example:
        # ("smiles here", 1.5)
        self.count_use += 1
        one = random.choice(self.smiles)
        two = random.choice(self.smiles)
        three = random.choice(self.smiles)
        koef = 0
        if one == two and two == three:
            koef = 2
        elif one == two or two == three or one == three:
            koef = 1.5
        return ("%s%s%s" % (one, two, three), koef)

    def checkAttribute(self, text, attribute, user):
        return text.replace("<%s>" % attribute, "%s" % eval("user.%s" % attribute))

    def answerPattern(self, text, user):
        # param text must be string, example: Hello, <name>
        # param user must be User or BetterUser
        # answerPattern return string, example:
        # input: Hello, <name>, your money is <money>
        # output: Hello, Username, your money is 1000
        for attr in user.obj:
            text = self.checkAttribute(text, attr, user)

        setter = re.split(r"[\[\]]", text, maxsplit=1)
        while setter and ("[" in text or "]" in text):
            exec(setter[len(setter)-1][:-1].strip(), globals(), locals())
            text = text.replace("[%s" % setter[len(setter)-1], "").strip()
            setter = re.split(r"[\[\]]", text, maxsplit=1)

        return text
