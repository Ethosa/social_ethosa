# -*- coding: utf-8 -*-
# author: Ethosa

from ..utils import getValue
from .User import User
import json
import os

class BotBase:
    """
    doctsring for BotBase
    You can use it how BD:
    bs = BotBase("Users folder", "json")
    bs.addPattern("key", "value") # Here you add a new pattern to all new users

    user = bs.addNewUser(1, name="Ethosa", role="Admin", status="Hello kitti")
    print(user) # {"name" : "Ethosa", "key" : "value", "role" : "Admin",
                    "status" : "Hello kitti", "money" : 0, "uid" : 1}

    """
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

            if key not in current:
                current[key] = defult_value

            with open("%s/%s" % (self.path, user), 'w', encoding='utf-8') as f:
                f.write(json.dumps(current))
        for i in range(len(self.users)):
            self.users[i].obj[key] = defult_value

    def saveUser(self, user):
        with open("%s/%s.%s" % (self.path, user.obj["uid"], self.postfix), 'w', encoding='utf-8') as f:
            f.write(json.dumps(user.obj))

    def saveUsers(self, *users):
        for user in users:
            self.saveUser(user)

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
        pattern["uid"] = 0
        pattern["name"] = "user"
        pattern["money"] = 0
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
        allUsers = [self.loadUser(i[:-len(self.postfix)-1]).obj for i in os.listdir(self.path)]

        args = [i for i in args]
        args.append("uid")

        return [{
            key : user[key] for key in args
        } for user in allUsers]

    def getSortedUsersByKey(self, key, count=None, offset=0, sortType="1-9", formatting=False, otherKeys=[]):
        sortedUsers = sorted(self.getUsersByKeys(key, "name", *otherKeys), key=itemgetter(key), reverse=True if sortType == "1-9" else False if sortType == "9-1" else True)
        if formatting:
            for user in sortedUsers:
                user["formatted"] = "[id%s|%s]" % (user["uid"], user["name"])
        if count:
            return sortedUsers[offset:count+offset]
        else:
            return sortedUsers[offset:]

    def calcMiddleValueByKey(self, key, otherKeys=[], roundInt=0, returnUsers=False):
        users = self.getUsersByKeys(key, "name", *otherKeys)
        a = sum([user[key] if type(user[key]) == int else len(user[key]) for user in users])/len(users)
        if not returnUsers:
            users = None
        if not roundInt:
            return {"amount" : a, "users" : users}
        elif roundInt > 0:
            return {"amount" : math.ceil(a), "users" : users}
        elif roundInt < 0:
            return {"amount" : math.floor(a), "users" : users}
