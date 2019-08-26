try:
    import requests
    requests.packages.urllib3.disable_warnings()
except:
    raise ImportError('Please install requests library! "pip install requests".')

from threading import Thread
from .smiles import *
from pprint import pprint
import traceback
import datetime
import random
import time
import json
import sys

class Vk:
    '''
    docstring for Vk

    Get vk access token here:
    https://vkhost.github.io/ (choose the Kate mobile.)

    used:
    vk = Vk(token=Access_Token) # if you want auth to user
    vk = Vk(token=Group_Access_Token) # if you want auth to group

    use param version_api for change verison api. Default value is 5.101
    use param debug=True for debugging!
    use param lang='en' for set debug language! # en, ru, de, fr, ja

    for handling new messages:
    In the official VK API documentation, the event of a new message is called "message_new", so use:

    @on_message_new
    def get_new_message(obj):
        print(obj)
        print('text message:', obj.text) # see https://vk.com/dev/objects/message for more info
        print(obj.obj)
        print(obj.peer_id)

    use any vk api method:
    vk.method(method='messages.send', message='message', peer_id=1234567890, random_id=0)

    use messages methods:
    vk.messages.send(message='message', peer_id=1234567890)
    '''

    def __init__(self, *args, **kwargs):
        self.token_vk = get_val(kwargs, 'token') # Must be string
        self.debug = get_val(kwargs, 'debug') # Must be boolean
        self.version_api = get_val(kwargs, 'version_api', '5.101') # Can be float / integer / string
        self.group_id = get_val(kwargs, 'group_id') # can be string or integer
        self.lang = get_val(kwargs, 'lang', 'en') # must be string

        # Initialize methods
        self.longpoll = LongPoll(access_token=self.token_vk, group_id=self.group_id, version_api=self.version_api)
        self.method = Method(access_token=self.token_vk, version_api=self.version_api).use

        # Other variables:
        self.translate = Translator_debug().translate
        self.vk_api_url = 'https://api.vk.com/method/'

        if self.token_vk:
            if self.debug: print(self.translate('Токен установлен. Проверяем его валидность ...', self.lang))
            test = ''.join(requests.get(f'{self.vk_api_url}messages.getLongPollServer?access_token={self.token_vk}&v={self.version_api}{f"&group_id={self.group_id}" if self.group_id else ""}').json().keys())
            if self.debug: print(self.translate('Ошибка' if test == 'error' else 'Успешно!', self.lang))


    # Also you can use the easy way to upload files in vk!
    def upload_album_photo(self, album_id, first=True, *args, **kwargs):

        # param files is list of string, example: ['photo.png', 'photo.jpg', 'mushroom.png']
        # param album_id must be Integer
        # param formatting must be boolean. return the list of photos if True, example: ['photo123_456', 'photo789_123']
        # param first can't used

        files = get_val(kwargs, 'files', [])
        formatting = get_val(kwargs, 'formatting')
        if first: self.uploaded = []
        if len(files) > 5:
            self.uploaded.append(self.upload_album_photo(album_id=album_id, files=files[5:], first=False))
            files = files[:5]
            if self.debug: print(self.translate('Файлов не должно быть больше 5! Я автоматически урезала количество файлов до нужной длины.', self.lang))
        upload_url = self.photos.getUploadServer(album_id=album_id, **kwargs)['response']['upload_url']
        filess = {f'file{current+1}' : open(files[current], 'rb') for current in range(len(files))}
        response = requests.post(upload_url, files=filess, verify=False).json()
        response = self.method(method='photos.save', hash=response['hash'], album_id=album_id,
                                server=response['server'], photos_list=response['photos_list'], aid=response['aid'])['response']
        if not first: return response
        else:
            self.uploaded.append(response)
            if formatting:
                upls = []
                for photos_list in self.uploaded:
                    for photo in photos_list:
                        upls.append(f'photo{photo["owner_id"]}_{photo["id"]}')
                return upls
            return self.uploaded

    def upload_wall_photo(self, group_id=None, user_id=None, first=True, *args, **kwargs):

        # param files is list of string, example: ['photo.png', 'photo.jpg', 'mushroom.png']
        # use one of two variables: group_id or user_id: they must be integer
        # param formatting must be boolean. return the list of photos if True, example: ['photo123_456', 'photo789_123']
        # param first can't used

        files = get_val(kwargs, 'files', [])
        formatting = get_val(kwargs, 'formatting')
        if first: self.uploaded = []
        if len(files) > 1:
            self.uploaded.append(self.upload_wall_photo(files=files[1:], group_id=group_id, user_id=user_id, first=False))
            files = [files[0]]
            if self.debug:
                print(self.translate('Файлов не должно быть больше 1! Я автоматически урезала количество файлов до нужной длины.', self.lang))
        upload_url = self.photos.getWallUploadServer(**kwargs)['response']['upload_url']
        filess = {f'file{current+1}' : open(files[current], 'rb') for current in range(len(files))}
        response = requests.post(upload_url, files=filess, verify=False).json()
        if group_id:
            response = self.method(method='photos.saveWallPhoto', hash=response['hash'],
                                    server=response['server'], photo=response['photo'], group_id=group_id)['response'][0]
        else:
            response = self.method(method='photos.saveWallPhoto', hash=response['hash'],
                                    server=response['server'], photo=response['photo'], user_id=user_id)['response'][0]
        if not first: return response
        else:
            self.uploaded.append(response)
            if formatting:
                upls = []
                for photo in self.uploaded:
                    upls.append(f'photo{photo["owner_id"]}_{photo["id"]}')
                return upls
            return self.uploaded

    def upload_message_photo(self, peer_id, first=True, *args, **kwargs):

        # param files is list of string, example: ['photo.png', 'photo.jpg', 'mushroom.png']
        # param peer_id must be integer
        # param formatting must be boolean. return the list of photos if True, example: ['photo123_456', 'photo789_123']
        # param first can't used

        files = get_val(kwargs, 'files', [])
        formatting = get_val(kwargs, 'formatting')
        if first: self.uploaded = []
        if len(files) > 1:
            self.uploaded.append(self.upload_message_photo(files=files[1:], peer_id=peer_id, first=False))
            files = [files[0]]
            if self.debug:
                print(self.translate('Файлов не должно быть больше 1! Я автоматически урезала количество файлов до нужной длины.', self.lang))
        upload_url = self.photos.getMessagesUploadServer(peer_id=peer_id, **kwargs)['response']['upload_url']
        filess = { 'photo' : open(files[0], 'rb') }
        response = requests.post(upload_url, files=filess, verify=False).json()
        response = self.method(method='photos.saveMessagesPhoto', hash=response['hash'],
                                        server=response['server'], photo=response['photo'])['response'][0]
        if not first: return response
        else:
            self.uploaded.append(response)
            if formatting:
                upls = []
                for photo in self.uploaded:
                    upls.append(f'photo{photo["owner_id"]}_{photo["id"]}')
                return upls
            return self.uploaded

    def upload_user_photo(self, user_id, *args, **kwargs):

        # param user_id must be integer
        # param file must be string of path, example: 'photo.png'

        file = get_val(kwargs, 'file', '')
        upload_url = self.photos.getOwnerPhotoUploadServer(user_id)['response']['upload_url']
        file = { 'photo' : open(file, 'rb') }
        response = requests.post(upload_url, files=file, verify=False).json()
        response = self.method(method='photos.saveOwnerPhoto', hash=response['hash'],
                                server=response['server'], photo=response['photo'])['response']
        return response

    def upload_chat_photo(self, chat_id, *args, **kwargs):

        # param chat_id must be integer
        # param file must be string of path, example: 'photo.png'

        file = get_val(kwargs, 'file', '')
        upload_url = self.photos.getChatUploadServer(chat_id)['response']['upload_url']
        file = { 'photo' : open(file, 'rb') }
        response = requests.post(upload_url, files=file, verify=False).json()
        response = self.method(method='messages.setChatPhoto', file=response['response'])['response']
        return response

    def upload_market_photo(self, group_id, *args, **kwargs):

        # param chat_id must be integer
        # param file must be string of path, example: 'photo.png'

        file = get_val(kwargs, 'file', '')
        upload_url = self.photos.getMarketUploadServer(group_id=group_id)['response']['upload_url']
        file = { 'photo' : open(file, 'rb') }
        response = requests.post(upload_url, files=file, verify=False).json()
        response = self.method(method='photos.saveMarketPhoto', group_id=group_id, photo=response['photo'],
                                hash=response['hash'], server=response['server'], crop_data=response['crop_data'],
                                crop_hash=response['crop_hash'])['response']
        return response

    def upload_market_album_photo(self, group_id, *args, **kwargs):

        # param chat_id must be integer
        # param file must be string of path, example: 'photo.png'

        if self.debug: print(self.translate('Осторожно! Размер картинки должен быть не меньше 1280х720', self.lang))
        file = get_val(kwargs, 'file', '')
        upload_url = self.photos.getMarketAlbumUploadServer(group_id=group_id)['response']['upload_url']
        file = upl(file, 'file')
        response = requests.post(upload_url, files=file, verify=False).json()
        response = self.method(method='photos.saveMarketAlbumPhoto', group_id=group_id, photo=response['photo'],
                                hash=response['hash'], server=response['server'])['response']
        return response

    def upload_audio(self, artist='', title='', *args, **kwargs):

        # param chat_id must be integer
        # param file must be string of path, example: 'mil_tokyo.mp3'

        file = get_val(kwargs, 'file', '')
        upload_url = self.audio.getUploadServer()['response']['upload_url']
        file = upl(file, 'file')
        response = requests.post(upload_url, files=file, verify=False).json()
        print(response)
        response = self.method(method='audio.save', title=title, artist=artist, audio=response['audio'],
                                hash=response['hash'], server=response['server'])['response']
        return response

    def upload_audio_message(self, peer_id, *args, **kwargs):

        # param chat_id must be integer
        # param file must be string of path, example: 'message.ogg'

        file = get_val(kwargs, 'file', '')
        del kwargs['file']
        upload_url = self.docs.getMessagesUploadServer(type='audio_message', peer_id=peer_id, **kwargs)['response']['upload_url']
        file = upl(file, 'file')
        response = requests.post(upload_url, files=file, verify=False).json()['file']
        response = self.method(method='docs.save', file=response, **kwargs)['response']
        return response

    def upload_video(self, *args, **kwargs):

        # param chat_id must be integer
        # param file must be string of path, example: 'pron.mp4' :D

        file = get_val(kwargs, 'file', '')
        upload_url = self.video.save(**kwargs)['response']['upload_url']
        file = upl(file, 'file')
        response = requests.post(upload_url, files=file, verify=False).json()
        return response


    # Handlers:
    # use handlers:
    # @vk.*nam function*
    # def function(obj):
    #     pass
    #
    # Example:
    # @vk.on_wall_post_new
    # def get_message(obj):
    #     print("post text is", obj.text)
    def on_user_message_new(self, function):
        def listen():
            for event in self.longpoll.listen():
                if not self.group_id:
                    if event.update[0] == 4 and not 'source_act' in event.update[6].keys():
                        if self.debug: print(self.translate('Новое сообщение!', self.lang))
                        try: function(New_user_message(event.update))
                        except Exception as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            line = traceback.extract_tb(exc_tb)[-1][1]
                            self.longpoll.errors.append(Error(line=line, message=str(e), code=type(e).__name__))
        thread = Thread_VK(listen).start()

    def on_user_message_edit(self, function):
        def listen():
            for event in self.longpoll.listen():
                if not self.group_id:
                    if event.update[0] == 5:
                        try: function(Edit_user_message(event.update))
                        except Exception as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            line = traceback.extract_tb(exc_tb)[-1][1]
                            self.longpoll.errors.append(Error(line=line, message=str(e), code=type(e).__name__))
        thread = Thread_VK(listen).start()

    # Hander longpolls errors:
    # return object with variables:
    # object.message, object.line, object.code
    def on_error(self, function):
        def parse_error():
            while True:
                if self.longpoll.errors:
                    for error in self.longpoll.errors:
                        function(error)
                        self.longpoll.errors.remove(error)
        Thread_VK(parse_error).start()


    # Handler wrapper
    def listen_wrapper(self, type_value, class_wrapper, function, user=False, e='type'):
        def listen(e=e):
            for event in self.longpoll.listen():
                print(event.update)
                if self.group_id:
                    if event.update[e] == type_value:
                        if self.debug: print(type_value)
                        try: function(class_wrapper(event.update))
                        except Exception as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            line = traceback.extract_tb(exc_tb)[-1][1]
                            self.longpoll.errors.append(Error(line=line, message=str(e), code=type(e).__name__))
        Thread_VK(listen).start()

    def __getattr__(self, method):
        if method.startswith('on_'):
            return lambda function: self.listen_wrapper(method[3:], Obj, function)
        else: return Method(access_token=self.token_vk, version_api=self.version_api, method=method)

    def __str__(self):
        return f'''{"-"*10}
The Vk object with params:
token = {f"{self.token_vk[:5]}{'*'*10}{self.token_vk[-5:]}"}
debug = {self.debug}
version_api = {self.version_api}
group_id = {self.group_id}
{"-"*10}'''


class LongPoll:
    '''
    docstring for LongPoll

    use it for longpolling

    example use:
    longpoll = LongPoll(access_token='your_access_token123')
    for event in longpoll.listen():
        print(event)
    '''
    def __init__(self, *args, **kwargs):
        self.group_id = get_val(kwargs, 'group_id')
        self.access_token = kwargs['access_token']
        self.vk_api_url = 'https://api.vk.com/method/'
        self.version_api = get_val(kwargs, 'version_api', '5.101')
        self.ts = '0'
        self.key = None
        self.server = None
        self.errors = []

    def listen(self):
        if self.group_id:
            response = requests.get(f'{self.vk_api_url}groups.getLongPollServer?access_token={self.access_token}&v={self.version_api}&group_id={self.group_id}').json()['response']
            self.ts = response['ts']
            self.key = response['key']
            self.server = response['server']

            while True:
                response = requests.get(f'{self.server}?act=a_check&key={self.key}&ts={self.ts}&wait=25').json()
                self.ts = response['ts']
                updates = response['updates']

                if updates:
                    for update in updates:
                        yield Event(update=update)
        else:
            response = requests.get(f'{self.vk_api_url}messages.getLongPollServer?access_token={self.access_token}&v={self.version_api}').json()['response']
            self.ts = response['ts']
            self.key = response['key']
            self.server = response['server']

            while True:
                response = requests.get(f'https://{self.server}?act=a_check&key={self.key}&ts={self.ts}&wait=25&mode=202&version=3').json()
                self.ts = response['ts']
                updates = response['updates']

                if updates:
                    for update in updates:
                        yield Event(update=update)


# Class for use anything vk api method
# You can use it:
# response = vk.method(method='messages.send', message='Hello, world!', peer_id=1)
class Method:
    def __init__(self, *args, **kwargs):
        self.access_token = kwargs['access_token']
        self.vk_api_url = 'https://api.vk.com/method/'
        self.version_api = get_val(kwargs, 'version_api', '5.101')
        self.method = get_val(kwargs, 'method', '')

    def use(self, *args, **kwargs):
        url = f'''{self.vk_api_url}{kwargs["method"]}'''
        data = kwargs
        data['access_token'] = self.access_token
        data['v'] = self.version_api
        del data['method']
        response = requests.post(url, data=data).json()
        return response

    def __getattr__(self, method):
        return lambda **kwargs: self.use(method=f'{self.method}.{method}', **kwargs)



class Keyboard:

    """
    docstring for Keyboard

    use it for add keyboard in message

    keyboard = Keyboard()
    keyboard.add_button(Button(type='text', label='lol'))
    keyboard.add_line()
    keyboard.add_button(Button(type='text', label='hello', color=ButtonColor.POSITIVE))
    keyboard.add_button(Button(type='text', label='world', color=ButtonColor.NEGATIVE))
    # types "location", "vkpay", "vkapps" can't got colors. also this types places on all width line.
    keyboard.add_button(Button(type='location''))
    keyboard.add_button(Button(type='vkapps'', label='hello, world!'))
    keyboard.add_button(Button(type='vkpay''))
    """

    def __init__(self, *args, **kwargs):
        self.keyboard = {
            'one_time' : get_val(kwargs, 'one_time', True),
            'buttons' : get_val(kwargs, 'buttons', [[]])
        }

    def add_line(self):
        if len(self.keyboard['buttons']) < 10:
            self.keyboard['buttons'].append([])

    def add_button(self, button):
        if len(self.keyboard['buttons'][::-1][0]) <= 4:
            if button['action']['type'] != 'text' and len(self.keyboard['buttons'][-1]) >= 1:
                self.add_line()
            if len(self.keyboard['buttons']) < 10:
                self.keyboard['buttons'][::-1][0].append(button)
        else:
            self.add_line()
            if len(self.keyboard['buttons']) < 10:
                self.add_button(button)


    def compile(self):
        return json.dumps(self.keyboard)

class Button:
    def __init__(self, *args, **kwargs):
        self.type = kwargs['type'] if 'type' in kwargs.keys() else 'text'

        actions = {
            'text' : {
                'type' : 'text',
                'label' : kwargs['label'] if 'label' in kwargs.keys() else 'бан',
                'payload' : kwargs['payload'] if 'payload' in kwargs.keys() else ''
            },
            'location' : {
                'type' : 'location',
                'payload' : kwargs['payload'] if 'payload' in kwargs.keys() else ''
            },
            'vkpay' : {
                'type' : 'vkpay',
                'payload' : kwargs['payload'] if 'payload' in kwargs.keys() else '',
                'hash' : kwargs['hash'] if 'hash' in kwargs.keys() else 'action=transfer-to-group&group_id=1&aid=10'
            },
            'vkapps' : {
                'type' : 'open_app',
                'payload' : kwargs['payload'] if 'payload' in kwargs.keys() else '',
                'hash' : kwargs['hash'] if 'hash' in kwargs.keys() else 'ethosa_lib',
                'label' : kwargs['label'] if 'label' in kwargs.keys() else '',
                'owner_id' : kwargs['owner_id'] if 'owner_id' in kwargs.keys() else -181108510,
                'app_id' : kwargs['app_id'] if 'app_id' in kwargs.keys() else 6979558
            }
        }

        self.action = get_val(actions, kwargs['type'], actions['text'])
        self.color = get_val(kwargs, 'color', ButtonColor.PRIMARY)

    def __new__(self, *args, **kwargs):
        self.__init__(self, *args, **kwargs)
        kb = {'action' : self.action, 'color' : self.color}
        if kb['action']['type'] != 'text':
            del kb['color']
        return kb


# Enums start here:
class Event:
    '''docstring for Event'''
    def __init__(self, *args, **kwargs):
        self.update = kwargs['update']

    def __str__(self):
        return f'{self.update}'

class Thread_VK(Thread):
    def __init__(self, function):
        Thread.__init__(self)
        self.function = function
    def run(self):
        self.function()
class ButtonColor:
    PRIMARY = 'primary'
    SECONDARY = 'secondary'
    NEGATIVE = 'negative'
    POSITIVE = 'positive'

class Error:
    def __init__(self, *args, **kwargs):
        self.code = kwargs['code']
        self.message = kwargs['message']
        self.line = kwargs['line']

    def __str__(self):
        return f'{self.code}:\n{self.message}. Line {self.line}'
    def __repr__(self):
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

class New_user_message(Obj):
    def __init__(self, obj):
        self.date = obj[4]
        self.strdate = datetime.datetime.utcfromtimestamp(self.date).strftime('%d.%m.%Y %H:%M:%S') if self.date else None
        self.text = obj[5]
        self.from_id = obj[6]['from'] if 'from' in obj[6].keys() else None
        self.peer_id = obj[3]
        self.message_id = obj[1]
        self.random_id = obj[8]
        self.attachments = obj[7]
        self.obj = obj

class Edit_user_message(Obj):
    def __init__(self, obj):
        self.message_id = obj[1]
        self.mask = obj[2]
        self.peer_id = obj[3]
        self.date = obj[4]
        self.strdate = datetime.datetime.utcfromtimestamp(self.date).strftime('%d.%m.%Y %H:%M:%S') if self.date else None
        self.text = obj[5]
        self.attachments = obj[6]
        self.obj = obj


class Translator_debug:
    def __init__(self, *args, **kwargs):
        self.base = { 'Токен установлен. Проверяем его валидность ...' : {
                'ru' : 'Токен установлен. Проверяем его валидность ...',
                'en' : 'The token is set. Check its validity ...',
                'de' : 'Token installiert. Überprüfen Sie seine Validität ...',
                'fr' : 'Le jeton est défini. Nous vérifions sa validité ...',
                'ja' : 'トークンが設定されます。 その妥当性を確認します。..'
            },
            'Ошибка!' : {
                'ru' : 'Ошибка!',
                'en' : 'Error!',
                'de' : 'Fehler!',
                'fr' : 'Erreur!',
                'ja' : '間違いだ！'
            },
            'Успешно!' : {
                'ru' : 'Успешно!',
                'en' : 'Successfully!',
                'de' : 'Erfolgreich!',
                'fr' : 'Avec succès!',
                'ja' : '成功しました！'
            },
            'Новое сообщение!' : {
                'ru' : 'Новое сообщение!',
                'en' : 'New message!',
                'de' : 'Neue Nachricht!',
                'fr' : 'Nouveau message!',
                'ja' : '新しいメッセージ！'
            },
            'Файлов не должно быть больше 5! Я автоматически урезала количество файлов до нужной длины.' : {
                'ru' : 'Файлов не должно быть больше 5! Я автоматически урезала количество файлов до нужной длины.',
                'en' : 'Files should not be more than 5! I automatically cut the number of files to the desired length.',
                'de' : 'Dateien sollten nicht mehr als 5 sein! Ich habe die Anzahl der Dateien automatisch auf die gewünschte Länge reduziert.',
                'fr' : "Les fichiers ne doivent pas être plus de 5! J'ai automatiquement réduit le nombre de fichiers à la longueur désirée.",
                'ja' : 'ファイルは5を超えてはいけません！ 私は自動的にファイルの数を希望の長さにカットします。'
            },
            'Файлов не должно быть больше 1! Я автоматически урезала количество файлов до нужной длины.' : {
                'ru' : 'Файлов не должно быть больше 1! Я автоматически урезала количество файлов до нужной длины.',
                'en' : 'Files should not be more than 1! I automatically cut the number of files to the desired length.',
                'de' : 'Dateien sollten nicht mehr als 1 sein! Ich habe die Anzahl der Dateien automatisch auf die gewünschte Länge reduziert.',
                'fr' : "Les fichiers ne doivent pas être plus de 1! J'ai automatiquement réduit le nombre de fichiers à la longueur désirée.",
                'ja' : 'ファイルは5を超えてはいけません！ 私は自動的にファイルの数を希望の長さにカットします。'
            },
            'Осторожно! Размер картинки должен быть не меньше 1280х720' : {
                'ru' : "Осторожно! Размер картинки должен быть не меньше 1280х720",
                'en' : "Careful! The size of the pictures should be at least 1280x720",
                'de' : "Sei vorsichtig! Die Größe des Bildes sollte nicht kleiner als 1280x720 sein",
                'fr' : "Attention ! La taille de l'image ne doit pas être inférieure à 1280x720",
                'ja' : "気をつけろ! 映像のサイズは少なくとも1280x720べきです"
            },
            'empty' : {
                'ru' : "",
                'en' : "",
                'de' : "",
                'fr' : "",
                'ja' : ""
            }
        }

    def translate(self, *args):
        text = args[0]
        lang = args[1]
        if text in self.base.keys():
            if lang in self.base[text].keys():
                return self.base[text][lang]
            else:
                return text
        else:
            return text

def get_val(obj, string, returned=None):
    return obj[string] if string in obj.keys() else returned

def upl(file, name):
    return { name : open(file, 'rb') }