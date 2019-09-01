import requests
import json
import os

def get_val(obj, string, returned=None):
    return obj[string] if (string in obj.keys() if type(obj) == dict else string in obj) else returned

def upl(file, name):
    return { name : open(file, 'rb') }

def upload_files(upload_url, file):
    return requests.post(upload_url, files=file, verify=False).json()

users_event = {
    'chat_name_changed' : 4,
    'chat_photo_changed' : 4,
    'chat_admin_new' : 3,
    'chat_message_pinned' : 5,
    'chat_user_new' : 6,
    'chat_user_kick' : 7,
    'chat_user_ban' : 8,
    'chat_admin_deleted' : 9
}

class Translator_debug:
    def __init__(self, *args, **kwargs):
        try:
            with open(f'{os.path.dirname(os.path.abspath(__file__))}\\translate.py', 'r', encoding='utf-8') as f:
                self.base = json.loads(f.read())
        except:
            with open(f'{os.path.dirname(os.path.abspath(__file__))}/translate.py', 'r', encoding='utf-8') as f:
                self.base = json.loads(f.read())

    def translate(self, *args):
        text = args[0]
        lang = args[1]
        if text in self.base.keys():
            if lang in self.base[text].keys():
                return self.base[text][lang]
            else: return text
        else: return text