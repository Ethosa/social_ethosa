import requests

def get_val(obj, string, returned=None):
    return obj[string] if string in obj.keys() else returned

def upl(file, name):
    return { name : open(file, 'rb') }

def upload_files(upload_url, file):
    return requests.post(upload_url, files=file, verify=False).json()