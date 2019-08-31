try:
    import requests
    requests.packages.urllib3.disable_warnings()
except:
    raise ImportError('Please install requests library! "pip install requests".')

from threading import Thread
from .smiles import *
from .utils import *
import traceback
import datetime
import random
import time
import json
import sys
import os

class Telegram:
    """
    docstring for Telegram
    """
    def __init__(self, *args, **kwargs):
        self.token = get_val(kwargs, 'token')
        self.link = f'https://api.telegram.org/bot{self.token}/'

        self.method = Method(token=self.token).use
        self.longpoll = LongPoll(token=self.token)

    def __getattr__(self, method):
        return lambda **kwargs: Method(token=self.token, method=method).use(method=method, **kwargs)


class LongPoll:
    """
    docstrring for LongPoll
    """
    def __init__(self, *args, **kwargs):
        self.token = get_val(kwargs, 'token')
        print(self.token)
        self.link = f'https://api.telegram.org/bot{self.token}/'
        self.errors = []
        self.updates = []
        self.method = Method(token=self.token).use

    def listen(self):
        event = self.method(method='getUpdates')
        print(event)


class Thread_VK(Thread):
    def __init__(self, function):
        Thread.__init__(self)
        self.function = function
    def run(self):
        self.function()


class Method:
    def __init__(self, *args, **kwargs):
        self.token = get_val(kwargs, 'token')
        self.link = f'https://api.telegram.org/bot{self.token}/'
        self.method = get_val(kwargs, 'method', '')
        if self.method:
            self.use(method=self.method, **kwargs)
        self.proxyDict = {
            'https' : 'https://10.10.1.11:1080',
            'http' : 'http://10.10.1.10:3128',
            'ftp' : 'ftp://10.10.1.10:3128'
        }

    def use(self, *args, **kwargs):
        url = f'''{self.link}{kwargs["method"]}'''
        data = kwargs
        del data['method']
        response = requests.post(url, data=data, proxies=self.proxyDict).json()
        return response


class Error:
    def __init__(self, *args, **kwargs):
        self.code = kwargs['code']
        self.message = kwargs['message']
        self.line = kwargs['line']

    def __str__(self):
        return f'{self.code}:\n{self.message}. Line {self.line}'


class Obj:
    def __init__(self, obj):
        self.obj = obj
        self.strdate = datetime.datetime.utcfromtimestamp(self.obj['date']).strftime('%d.%m.%Y %H:%M:%S') if 'date' in self.obj.keys() else None
    def has(self, key):
        return key in self.obj
    def __getattr__(self, attribute):
        val = get_val(self.obj, attribute)
        return val if val else get_val(self.obj['object'], attribute)