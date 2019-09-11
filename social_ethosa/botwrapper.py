from .utils import getValue
import requests
import datetime
import pickle
import shutil
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
        self.count_use += 1
        resp = requests.get("https://fish-text.ru/get?type=sentence&number=%s&format=json" % number)
        resp.encoding = resp.apparent_encoding
        return json.loads(resp.text)['text']

    def calc(self, text):
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


class User:
    def __init__(self, *args, **kwargs):
        self._obj = kwargs

    @property
    def obj(self):
        return self._obj

    @obj.getter
    def obj(self):
        lst = dir(self)
        for i in lst:
            if i in self._obj:
                self._obj[i] = eval("self.%s" % i)
        return self._obj
    

    def isMoneyMoreThenZero(self):
        return self.obj['money'] > 0

    def changeName(self, name):
        self.obj['name'] = name

    def addMoney(self, amount):
        self.obj['money'] += amount

    def __getattr__(self, attribute):
        value = getValue(self.obj, attribute)
        exec("self.%s = %s%s%s" % (attribute, '"' if type(value) == str else '', value, '"' if type(value) == str else ''))
        return eval("self.%s" % attribute)
        

class BotBase:
    def __init__(self, *args):
        self.path = args[0] if args else "users"
        self.users = []
        self.pattern = lambda **kwargs: {
            "uid" : getValue(kwargs, "uid", 1),
            "name" : getValue(kwargs, "name", "Пользователь"),
            "money" : getValue(kwargs, "money", 0),
            "role" : getValue(kwargs, "role", "user"),
            "status" : getValue(kwargs, "status", "")
        }
        self.postfix = args[1] if len(args) > 1 else "json"
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def addNewUser(self, uid, name='Пользователь', role='user', status="", money=0 ,**kwargs):
        user = self.pattern(uid=uid, name=name, role=role, status=status, money=money, **kwargs)

        with open("%s/%s.%s" % (self.path, uid, self.postfix), 'w', encoding='utf-8') as f:
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
        with open("%s/%s.%s" % (self.path, user.obj["uid"], self.postfix), 'w', encoding='utf-8') as f:
            f.write(json.dumps(user.obj))

    def loadUser(self, user_id):
        with open("%s/%s.%s" % (self.path, user_id, self.postfix), 'r', encoding='utf-8') as f:
            user =  json.loads(f.read())

        self.users.append(User(**user))

        return self.users[len(self.users)-1]

    def notInBD(self, user_id):
        return not os.path.exists("%s/%s.%s" % (self.path, user_id, self.postfix))

    def autoInstallUser(self, uid, vk, **kwargs):
        if uid > 0:
            if self.notInBD(uid):
                name = vk.users.get(user_ids=uid)['response'][0]["first_name"]
                return self.addNewUser(uid=uid, name=name, **kwargs)
            else:
                return self.loadUser(uid)
                
    def clearPattern(self):
        self.pattern = lambda **kwargs: {
            "uid" : getValue(kwargs, "uid", 0)
        }

    def setPattern(self, pattern):
        self.pattern = lambda **kwargs: {
            i : getValue(kwargs, i, pattern[i]) for i in pattern
        }

    def addPattern(self, key, defult_value):
        current_pattern = self.pattern()
        current_pattern[key] = defult_value
        self.pattern = lambda **kwargs: {
            i : getValue(kwargs, i, current_pattern[i]) for i in current_pattern
        }

    def makeBackupCopy(self, directory):
        if not os.path.exists(directory):
            os.mkdir(directory)

        old_path = self.path
        new_path = directory

        for user in os.listdir(old_path):
            current_path = "%s/%s" % (old_path, user)
            shutil.copy(current_path, "%s/%s" % (new_path, user), follow_symlinks=True)

    def getUsersByKeys(self, *args):
        allUsers = [self.loadUser(i[:-len(self.postfix)]).obj for i in os.listdir(self.path)]

        args = [i for i in args]
        args.append("uid")

        return [{
            key : user[key] for key in args
        } for user in allUsers]


class BetterUser:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        for key in kwargs:
            value = kwargs[key]
            exec("self.%s = %s%s%s" % (key, '"' if type(value) == str else '', value, '"' if type(value) == str else ''))

    def __str__(self):
        return "%s" % {key : eval("self.%s" % key, {}, {"self" : self}) for key in self.kwargs}


class BetterBotBase(BotBase):
    """
    docstring for BetterBotBase
    """
    def __init__(self, *args):
        super().__init__(*args)
        self.postfix = args[1] if len(args) > 1 else "dat"

    def addNewUser(self, uid, name='Пользователь', role='user', status="", money=0 ,**kwargs):
        user = self.pattern(uid=uid, name=name, role=role, status=status, money=money, **kwargs)

        with open("%s/%s.%s" % (self.path, uid, self.postfix), 'wb') as f:
            pickle.dump(BetterUser(**user), f)

        self.users.append(BetterUser(**user))

        return self.users[len(self.users)-1]

    def addNewValue(self, key, defult_value=0):
        for user in os.listdir(self.path):
            current = self.loadUser(user[:-len(self.postfix)-1])
            value = defult_value
            exec("current.%s = %s%s%s" % (key, '"' if type(value) == str else '', value, '"' if type(value) == str else ''))
            current.kwargs[key] = defult_value
            self.saveUser(current)

        for i in range(len(self.users)):
            value = defult_value
            exec("self.users[i].%s = %s%s%s" % (key, '"' if type(value) == str else '', value, '"' if type(value) == str else ''))
            self.users[i].kwargs[key] = defult_value

    def saveUser(self, user):
        with open("%s/%s.%s" % (self.path, user.uid, self.postfix), 'wb') as f:
            pickle.dump(user, f)

    def loadUser(self, user_id):
        with open("%s/%s.%s" % (self.path, user_id, self.postfix), 'rb') as f:
            user =  pickle.load(f)

        self.users.append(user)

        return self.users[len(self.users)-1]

    def getUsersByKeys(self, *args):
        allUsers = [self.loadUser(i[:-len(self.postfix)-1]) for i in os.listdir(self.path)]

        args = [i for i in args]
        args.append("uid")

        return [{
            key : eval("user.%s" % key) for key in args
        } for user in allUsers]
