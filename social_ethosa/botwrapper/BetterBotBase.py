# -*- coding: utf-8 -*-
# author: Ethosa
from .BotBase import BotBase
from .BetterUser import BetterUser
import pickle
import json
import os

class BetterBotBase(BotBase):
    def __init__(self, *args):
        super().__init__(*args)
        self.postfix = args[1] if len(args) > 1 else "dat"

    def addNew(self, uid, name='Пользователь', role='user', status="", money=0 ,**kwargs):
        user = self.pattern(uid=uid, name=name, role=role, status=status, money=money, **kwargs)

        user = BetterUser(**user)
        with open("%s/%s.%s" % (self.path, uid, self.postfix), 'wb') as f:
            pickle.dump(user, f)

        if user not in self.users:
            self.users.append(user)
            return self.users[len(self.users)-1]
        else:
            return self.users[self.users.index(user)]

    def addNewValue(self, key, defult_value=0):
        for user in os.listdir(self.path):
            current = self.loadUser(user[:-len(self.postfix)-1])
            value = defult_value
            if key not in current.obj:
                exec("current.%s = %s%s%s" % (key, '"' if type(value) == str else '', value, '"' if type(value) == str else ''))
                current.obj[key] = defult_value
            self.saveUser(current)

        for i in range(len(self.users)):
            value = defult_value
            exec("self.users[i].%s = %s%s%s" % (key, '"' if type(value) == str else '', value, '"' if type(value) == str else ''))
            self.users[i].obj[key] = defult_value

    def save(self, user):
        with open("%s/%s.%s" % (self.path, user.uid, self.postfix), 'wb') as f:
            pickle.dump(user, f)

    def load(self, user_id):
        with open("%s/%s.%s" % (self.path, user_id, self.postfix), 'rb') as f:
            user =  pickle.load(f)

        if user not in self.users:
            self.users.append(user)
            return self.users[len(self.users)-1]
        else:
            return self.users[self.users.index(user)]

    def getByKeys(self, *args):
        allUsers = [self.loadUser(i[:-len(self.postfix)-1]) for i in os.listdir(self.path)]

        args = [i for i in args]
        args.append("uid")

        return [{
            key : eval("user.%s" % key, {"user" : user}) for key in args
        } for user in allUsers]
