from .utils import get_val
import requests
import datetime
import random
import time
import json
import math
import os

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
    """

    def __init__(self):
        self.count_use = 0
        self.validate_for_calc = list('1234567890^-+/*')
        self.eng = list('''QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?qwertyuiop[]asdfghjkl;'zxcvbnm,./&''')
        self.rus = list('''ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,йцукенгшщзхъфывапролджэячсмитьбю.?''')
        self.eng_rus = {self.eng[i] : self.rus[i] for i in range(len(self.rus))}
        self.rus_eng = {self.rus[i] : self.eng[i] for i in range(len(self.rus))}
        self.smiles = [
            "&#127815;",
            "&#127821;",
            "&#127826;",
            "&#127827;"
        ]

    def randomDate(self):
        self.count_use += 1
        return randomDate("01.01.2001 00:00:00", "01.01.3001 00:00:00", random.random())

    def randomChance(self):
        self.count_use += 1
        return "%s%%" % random.randint(0, 100)

    def yesOrNo(self):
        self.count_use += 1
        return random.choice(["Да", "Нет"])

    def textReverse(self, text):
        return text[::-1]

    def space(self, text):
        return ' '.join(list(text))

    def translit(self, text):
        return ''.join([self.rus_eng[i] if i in self.rus_eng else self.eng_rus[i] if i in self.eng_rus else i for i in text])

    def delirium(self):
        resp = requests.get("https://fish-text.ru/get?type=sentence&number=1&format=json")
        resp.encoding = resp.apparent_encoding
        return json.loads(resp.text)['text']

    def calc(self, text):
        text = text.replace("^", "**") # ''.join(i for i in text if i in self.validate_for_calc)
        glb = {
            "pi" : math.pi,
            "e" : math.e,
            "sin" : math.sin,
            "cos" : math.cos,
            "factorial" : math.factorial,
            "ceil" : math.ceil,
            "floor" : math.floor,
            "floor" : math.floor,
            "pow" : math.pow,
            "log" : math.log,
            "sqrt" : math.sqrt,
            "tan" : math.tan,
            "arccos" : math.acos,
            "arcsin" : math.asin,
            "arctan" : math.atan,
            "degrees" : math.degrees,
            "radians" : math.radians,
            "sinh" : math.sinh,
            "cosh" : math.cosh,
            "tanh" : math.tanh,
            "arccosh" : math.acosh,
            "arcsinh" : math.asinh,
            "arctanh" : math.atanh,
        }
        return eval(text, glb, {})

    def casino(self):
        one = random.choice(self.smiles)
        two = random.choice(self.smiles)
        three = random.choice(self.smiles)
        koef = 0
        if one == two and two == three:
            koef = 2
        elif one == two or two == three or one == three:
            koef = 1.5
        return ("%s%s%s" % (one, two, three), koef)


class User:
    def __init__(self, *args, **kwargs):
        self.obj = kwargs

    def isMoneyMoreThenZero(self):
        return self.obj['money'] > 0

    def changeName(self, name):
        self.obj['name'] = name

    def addMoney(self, amount):
        self.obj['money'] += amount

    def __getattr__(self, attribute):
        return get_val(self.obj, attribute)
        

class BotBase:
    def __init__(self, *args):
        self.path = args[0] if args else None
        self.users = []
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def addNewUser(self, user_id, name='Пользователь', role='user', status=""):
        user = {
            "id" : user_id,
            "name" : name,
            "money" : 0,
            "role" : role,
            "status" : status
        }
        with open("%s/%s.json" % (self.path, user_id), 'w', encoding='utf-8') as f:
            f.write(json.dumps(user))

        self.users.append(User(**user))

        return self.users[len(self.users)-1]

    def addNewValue(self, key, defult_value=0):
        for user in os.listdir(self.path):
            with open("%s/%s" % (self.path, user), 'r', encoding='utf-8') as f:
                current =  json.loads(f.read())

            current[key] = defult_value

            with open("%s/%s" % (self.path, user), 'w', encoding='utf-8') as f:
                f.write(json.dumps(current))
        for i in range(len(self.users)):
            self.users[i].obj[key] = defult_value

    def saveUser(self, user):
        with open("%s/%s.json" % (self.path, user.obj["id"]), 'w', encoding='utf-8') as f:
            f.write(json.dumps(user.obj))

    def loadUser(self, user_id):
        with open("%s/%s.json" % (self.path, user_id), 'r', encoding='utf-8') as f:
            user =  json.loads(f.read())
        return User(**user)

    def notInBD(self, user_id):
        return not os.path.exists("%s/%s.json" % (self.path, user_id))

    def autoInstallUser(self, user_id, vk):
        if user_id > 0:
            if self.notInBD(user_id):
                name = vk.users.get(user_ids=user_id)['response'][0]["first_name"]
                return self.addNewUser(user_id, name=name)
            else:
                return self.loadUser(user_id)
                