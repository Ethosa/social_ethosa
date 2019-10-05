# -*- coding: utf-8 -*-
# author: ethosa
from threading import Thread
import requests
import inspect
import base64
import timeit
import random
import time
import json
import sys
import os

def autoRun(callObject, *args, **kwargs):
    # Decorator for auto-call object
    callObject(*args, **kwargs)

def printf(a, *args):
    # faster than print
    sys.stdout.write("%s\n" % ("%s" % a % args))

def downloadFileFromUrl(url, path):
    response = requests.get(url)
    if response.ok:
        with open(path, 'wb') as f:
            f.write(response.content)
        return True
    else: return False

def getMaxPhoto(attachments):
    files = []
    for attachment in attachments:
        if attachment["type"] == "photo":
            sizes = attachment["photo"]["sizes"]
            width = height = 0
            url = ""
            for size in sizes:
                if size["width"] > width and size["height"] > height:
                    height = size["height"]
                    width = size["width"]
                    url = size["url"]
            files.append(url)
    return files

def getValue(obj, string, returned=False):
    return obj[string] if string in obj else returned

def upl(file, name): return { name : open(file, "rb") }

def upload_files(upload_url, file):
    return requests.post(upload_url, files=file, verify=False).json()


users_event = {
    "user_message_flags_replace" : [1, "message_id", "flags", "peer_id", "timestamp", "text", "object", "attachments", "random_id"],
    "user_message_flags_add" : [2, "message_id", "flags", "peer_id", "timestamp", "text", "object", "attachments", "random_id"],
    "user_message_flags_delete" : [3, "message_id", "flags", "peer_id", "timestamp", "text", "object", "attachments", "random_id"],
    "user_message_new" : [4, "message_id", "flags", "peer_id", "timestamp", "text", "object", "attachments", "random_id"],
    "user_message_edit" : [5, "message_id", "mask", "peer_id", "timestamp", "new_text", "attachments"],
    "user_read_input_messages" : [6, "peer_id", "local_id"],
    "user_read_out_messages" : [7, "peer_id", "local_id"],
    "friend_online" : [8, "user_id", "extra", "timestamp"],
    "friend_offline" : [9, "user_id", "flags", "timestamp"],
    "user_dialog_flags_delete" : [10, "peer_id", "mask"],
    "user_dialog_flags_replace" : [11, "peer_id", "flags"],
    "user_dialog_flags_add" : [12, "peer_id", "mask"],
    "delete_messages" : [13, "peer_id", "local_id"],
    "restore_messages" : [14, "peer_id", "local_id"],
    "chat_edt" : [51, "chat_edit", "self"],
    "chat_info_edit" : [52, "type_id", "peer_id", "info"],
    "user_typing_dialog" : [61, "user_id", "flags"],
    "user_typing_chat" : [62, "user_id", "chat_id"],
    "users_typing_chat" : [63, "user_ids", "peer_id", "total_count", "ts"],
    "users_record_audio" : [64, "user_ids", "peer_id", "total_count", "ts"],
    "user_was_call" : [70, "user_id", "call_id"],
    "count_left" : [80, "count"],
    "notification_settings_edit" : [114, "peer_id", "sound", "disable_until"]
}

class TranslatorDebug:
    def __init__(self, *args, **kwargs):
        self.path = os.path.dirname(os.path.abspath(__file__))
        with open("%s/translate.py" % self.path, 'r', encoding='utf-8') as f:
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
    # This class is used to run callables on another thread.
    # Use:
    # Thread_VK(function, *args, **kwargs).start()
    def __init__(self, function, *args, **kwargs):
        Thread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs
    def run(self):
        return self.function(*self.args, **self.kwargs)

def timeIt(count=1, libs=[], launch="thread"):
    # Use this as a decorator to measure the execution time of a function.
    # libs-list of libraries to be imported before speed measurement
    # count-number of repetitions, default is 1
    # launch option to run. default "thread"
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

def updateLibrary(version=None):
    if version:
        os.system("pip install social-ethosa==%s" % version)
    else:
        os.system("pip install social-ethosa --upgrade")
    
def splitList(lst, number):
    # This function is intended for equal division of the list, for example:
    # splitList([1, 2, 3, 4, 5], 2) return [[1, 2], [2, 3], [5]]
    number -= 1
    splitted = [[]]
    current = 0
    count = 0
    for i in lst:
        if count < number:
            splitted[current].append(i)
            count += 1
        else:
            splitted[current].append(i)
            count = 0
            current += 1
            splitted.append([])
    if not splitted[len(splitted)-1]:
        splitted.pop()
    return splitted

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
    