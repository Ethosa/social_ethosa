import requests

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