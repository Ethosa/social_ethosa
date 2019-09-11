from contextlib import contextmanager
import requests
import inspect
import timeit
import json
import sys
import os

def timeIt(function, count=1):
    def timer(count=count):
        setup = "def" + inspect.getsource(function).split('def', 1)[1]
        return min(timeit.Timer("%s()" % function.__name__, setup=setup).repeat(1, count))
    return timer

def autoRun(callObject, *args, **kwargs):
    callObject(*args, **kwargs)

def printf(a, b=""):
    sys.stdout.write("%s\n" % (a % b if b else a))

def downloadFileFromUrl(url, path):
    response = requests.get(url)
    if response.ok:
        with open(path, 'wb') as f:
            f.write(response.content)
        return True
    else: return False

def getValue(obj, string, returned=False):
    return obj[string] if string in obj else returned

def upl(file, name): return { name : open(file, "rb") }

def upload_files(upload_url, file):
    return requests.post(upload_url, files=file, verify=False).json()


users_event = {
    "chat_name_changed" : 4,
    "chat_photo_changed" : 4,
    "user_message_new" : 4,
    "chat_admin_new" : 3,
    "chat_message_pinned" : 5,
    "chat_message_edit" : 5,
    "chat_user_new" : 6,
    "chat_user_kick" : 7,
    "chat_user_ban" : 8,
    "chat_admin_deleted" : 9
}

class Translator_debug:
    def __init__(self, *args, **kwargs):
        path = os.path.dirname(os.path.abspath(__file__))
        with open("%s/translate.py" % (os.path.dirname(os.path.abspath(__file__))), 'r', encoding='utf-8') as f:
            self.base = json.loads(f.read())

    def translate(self, *args):
        text = args[0]
        lang = args[1]
        if text in self.base.keys():
            if lang in self.base[text].keys():
                return '%s\n' % self.base[text][lang]
            else: return text
        else: return text