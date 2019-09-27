from threading import Thread
import requests
import inspect
import timeit
import time
import json
import sys
import os

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

class TranslatorDebug:
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
            else: return "%s\n" % text
        else: return "%s\n" % text

class Thread_VK(Thread):
    def __init__(self, function, *args, **kwargs):
        Thread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs
    def run(self):
        return self.function(*self.args, **self.kwargs)

def timeIt(count=1, libs=[], launch="thread"):
    def timer(function):
        global Thread_VK
        a = None
        def asd():
            setup = "\n".join(["import %s" % i for i in libs])
            setup += "\ndef" + inspect.getsource(function).split('def', 1)[1]
            return min(timeit.Timer("%s()" % function.__name__, setup=setup).repeat(1, count))
        if launch == "thread":
            print("%s() - %s time" % (function.__name__, Thread_VK(asd).run()))
        elif launch == "not thread":
            return print("%s() - %s time" % (function.__name__, asd()))
        elif launch == "variable":
            return "%s() - %s time" % (function.__name__, asd())
    return timer

class Timer:
    """
    Timer is used to call certain functions after N seconds or milliseconds,
    or you can use it to execute functions every N seconds or milliseconds after Y seconds or milliseconds.
    You can specify whether to use seconds or milliseconds using the setSeconds and setMilliseconds methods
    """ 
    def __init__(self, *args, **kwargs):
        self.canceled = 0
        self.ms = 1000

    def after(self, ms):
        def decorator(function):
            def func():
                time.sleep(ms/self.ms)
                function()
            Thread_VK(func).start()
        return decorator

    def afterEvery(self, ms1, ms2):
        time.sleep(ms1/self.ms)
        def decorator(function):
            def func():
                while not self.canceled:
                    function()
                    time.sleep(ms2/self.ms)
                    if self.canceled:
                        self.canceled = 0
                        break
            Thread_VK(func).start()
        return decorator

    def setSeconds(self): self.ms = 1
    def setMilliseconds(self): self.ms = 1000
    def cancel(self): self.canceled = 1
    