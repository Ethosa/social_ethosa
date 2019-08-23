try:
    import requests
    requests.packages.urllib3.disable_warnings()
except:
    raise ImportError('Please install requests library! "pip install requests".')

from threading import Thread
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
        self.token_vk = kwargs['token'] if 'token' in kwargs.keys() else None # Must be string
        self.debug = kwargs['debug'] if 'debug' in kwargs.keys() else False # Must be boolean
        self.version_api = kwargs['version_api'] if 'version_api' in kwargs.keys() else '5.101' # Can be float / integer / string
        self.group_id = kwargs['group_id'] if 'group_id' in kwargs.keys() else None # can be string or integer
        self.lang = kwargs['lang'] if 'lang' in kwargs.keys() else 'en' # must be string

        self.longpoll = LongPoll(access_token=self.token_vk, group_id=self.group_id, version_api=self.version_api)
        self.method = Method(access_token=self.token_vk, version_api=self.version_api).use
        self.messages = Messages(access_token=self.token_vk, version_api=self.version_api)
        self.photos = Photos(access_token=self.token_vk, version_api=self.version_api)
        self.audio = Audio(access_token=self.token_vk, version_api=self.version_api)
        self.video = Video(access_token=self.token_vk, version_api=self.version_api)
        self.docs = Docs(access_token=self.token_vk, version_api=self.version_api)
        self.translate = Translator_debug().translate

        self.vk_api_url = 'https://api.vk.com/method/'

        if self.token_vk:
            if self.debug: print(self.translate('Токен установлен. Проверяем его валидность ...', self.lang))
            test = ''.join(requests.get(f'{self.vk_api_url}messages.getLongPollServer?access_token={self.token_vk}&v={self.version_api}{f"&group_id={self.group_id}" if self.group_id else ""}').json().keys())
            if self.debug: print(self.translate('Ошибка' if test == 'error' else 'Успешно!', self.lang))


    # Also you can use the easy way to upload files in vk!
    def upload_album_photo(self, album_id, first=True, *args, **kwargs):
        files = kwargs['files'] if 'files' in kwargs.keys() else []
        formatting = kwargs['formatting'] if 'formatting' in kwargs.keys() else False
        if first:
            self.uploaded = []
        if len(files) > 5:
            self.uploaded.append(self.upload_album_photo(album_id=album_id, files=files[5:], first=False))
            files = files[:5]
            if self.debug: print(self.translate('Файлов не должно быть больше 5! Я автоматически урезала количество файлов до нужной длины.', self.lang))
        upload_url = self.photos.getUploadServer(album_id=album_id, **kwargs)['response']['upload_url']
        filess = {f'file{current+1}' : open(files[current], 'rb') for current in range(len(files))}
        response = requests.post(upload_url, files=filess, verify=False).json()
        response = self.method(method='photos.save', hash=response['hash'], album_id=album_id,
                                server=response['server'], photos_list=response['photos_list'], aid=response['aid'])['response']
        if not first:
            return response
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
        files = kwargs['files'] if 'files' in kwargs.keys() else []
        formatting = kwargs['formatting'] if 'formatting' in kwargs.keys() else False
        if first:
            self.uploaded = []
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
        if not first:
            return response
        else:
            self.uploaded.append(response)
            if formatting:
                upls = []
                for photo in self.uploaded:
                    upls.append(f'photo{photo["owner_id"]}_{photo["id"]}')
                return upls
            return self.uploaded

    def upload_message_photo(self, peer_id, first=True, *args, **kwargs):
        files = kwargs['files'] if 'files' in kwargs.keys() else []
        formatting = kwargs['formatting'] if 'formatting' in kwargs.keys() else False
        if first:
            self.uploaded = []
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
        if not first:
            return response
        else:
            self.uploaded.append(response)
            if formatting:
                upls = []
                for photo in self.uploaded:
                    upls.append(f'photo{photo["owner_id"]}_{photo["id"]}')
                return upls
            return self.uploaded

    def upload_user_photo(self, user_id, *args, **kwargs):
        file = kwargs['file'] if 'file' in kwargs.keys() else ''
        upload_url = self.photos.getOwnerPhotoUploadServer(user_id)['response']['upload_url']
        file = { 'photo' : open(file, 'rb') }
        response = requests.post(upload_url, files=file, verify=False).json()
        response = self.method(method='photos.saveOwnerPhoto', hash=response['hash'],
                                server=response['server'], photo=response['photo'])['response']
        return response

    def upload_chat_photo(self, chat_id, *args, **kwargs):
        file = kwargs['file'] if 'file' in kwargs.keys() else ''
        upload_url = self.photos.getChatUploadServer(chat_id)['response']['upload_url']
        file = { 'photo' : open(file, 'rb') }
        response = requests.post(upload_url, files=file, verify=False).json()
        response = self.method(method='messages.setChatPhoto', file=response['response'])['response']
        return response

    def upload_market_photo(self, group_id, *args, **kwargs):
        file = kwargs['file'] if 'file' in kwargs.keys() else ''
        upload_url = self.photos.getMarketUploadServer(group_id=group_id)['response']['upload_url']
        file = { 'photo' : open(file, 'rb') }
        response = requests.post(upload_url, files=file, verify=False).json()
        response = self.method(method='photos.saveMarketPhoto', group_id=group_id, photo=response['photo'],
                                hash=response['hash'], server=response['server'], crop_data=response['crop_data'],
                                crop_hash=response['crop_hash'])['response']
        return response

    def upload_market_album_photo(self, group_id, *args, **kwargs):
        if self.debug: print(self.translate('Осторожно! Размер картинки должен быть не меньше 1280х720', self.lang))
        file = kwargs['file'] if 'file' in kwargs.keys() else ''
        upload_url = self.photos.getMarketAlbumUploadServer(group_id=group_id)['response']['upload_url']
        file = { 'file' : open(file, 'rb') }
        response = requests.post(upload_url, files=file, verify=False).json()
        response = self.method(method='photos.saveMarketAlbumPhoto', group_id=group_id, photo=response['photo'],
                                hash=response['hash'], server=response['server'])['response']
        return response

    def upload_audio(self, artist='', title='', *args, **kwargs):
        file = kwargs['file'] if 'file' in kwargs.keys() else ''
        upload_url = self.audio.getUploadServer()['response']['upload_url']
        file = { 'file' : open(file, 'rb') }
        response = requests.post(upload_url, files=file, verify=False).json()
        print(response)
        response = self.method(method='audio.save', title=title, artist=artist, audio=response['audio'],
                                hash=response['hash'], server=response['server'])['response']
        return response

    def upload_audio(self, artist='', title='', *args, **kwargs):
        file = kwargs['file'] if 'file' in kwargs.keys() else ''
        upload_url = self.audio.getUploadServer()['response']['upload_url']
        file = { 'file' : open(file, 'rb') }
        response = requests.post(upload_url, files=file, verify=False).json()
        response = self.method(method='audio.save', title=title, artist=artist, audio=response['audio'],
                                hash=response['hash'], server=response['server'])['response']
        return response

    def upload_audio_message(self, peer_id, *args, **kwargs):
        file = kwargs['file'] if 'file' in kwargs.keys() else ''
        del kwargs['file']
        upload_url = self.docs.getMessagesUploadServer(type='audio_message', peer_id=peer_id, **kwargs)['response']['upload_url']
        file = { 'file' : open(file, 'rb') }
        response = requests.post(upload_url, files=file, verify=False).json()['file']
        response = self.method(method='docs.save', file=response, **kwargs)['response']
        return response

    def upload_video(self, *args, **kwargs):
        file = kwargs['file'] if 'file' in kwargs.keys() else ''
        upload_url = self.video.save(**kwargs)['response']['upload_url']
        file = { 'file' : open(file, 'rb') }
        response = requests.post(upload_url, files=file, verify=False).json()
        return response


    # Handlers:
    def on_message_new(self, function):
        def listen():
            for event in self.longpoll.listen():
                if self.group_id:
                    if event.update['type'] == 'message_new':
                        if self.debug: print(self.translate('Новое сообщение!', self.lang))
                        try:
                            function(New_group_message(event.update['object']))
                        except Exception as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            line = traceback.extract_tb(exc_tb)[-1][1]
                            self.longpoll.errors.append(Error(line=line, message=str(e), code=type(e).__name__))
                else:
                    if event.update[0] == 4 and not 'source_act' in event.update[6].keys():
                        if self.debug: print(self.translate('Новое сообщение!', self.lang))
                        try:
                            function(New_user_message(event.update))
                        except Exception as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            line = traceback.extract_tb(exc_tb)[-1][1]
                            self.longpoll.errors.append(Error(line=line, message=str(e), code=type(e).__name__))
        thread = Thread_VK(listen).start()

    def on_message_edit(self, function):
        def listen():
            for event in self.longpoll.listen():
                if self.group_id:
                    if event.update['type'] == 'message_edit':
                        try:
                            function(Edit_group_message(event.update['object']))
                        except Exception as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            line = traceback.extract_tb(exc_tb)[-1][1]
                            self.longpoll.errors.append(Error(line=line, message=str(e), code=type(e).__name__))
                else:
                    if event.update[0] == 5:
                        try:
                            function(Edit_user_message(event.update))
                        except Exception as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            line = traceback.extract_tb(exc_tb)[-1][1]
                            self.longpoll.errors.append(Error(line=line, message=str(e), code=type(e).__name__))
        thread = Thread_VK(listen).start()

    def on_photo_new(self, function):
        listen = self.group_listen_wrapper('photo_new', New_photo_group)
        thread = Thread_VK(listen).start()

    def on_photo_comment_new(self, function):
        listen = self.group_listen_wrapper('photo_comment_new', Comment_photo_group)
        thread = Thread_VK(listen).start()

    def on_photo_comment_edit(self, function):
        listen = self.group_listen_wrapper('photo_comment_edit', Comment_photo_group)
        thread = Thread_VK(listen).start()

    def on_photo_comment_restore(self, function):
        listen = self.group_listen_wrapper('photo_comment_restore', Comment_photo_group)
        thread = Thread_VK(listen).start()

    def on_photo_comment_delete(self, function):
        listen = self.group_listen_wrapper('photo_comment_delete', Deleted_comment_photo)
        thread = Thread_VK(listen).start()

    def on_audio_new(self, function):
        listen = self.group_listen_wrapper('audio_new', Audio_obj)
        thread = Thread_VK(listen).start()

    def on_video_new(self, function):
        listen = self.group_listen_wrapper('video_new', Video_obj)
        thread = Thread_VK(listen).start()

    def on_video_comment_new(self, function):
        listen = self.group_listen_wrapper('video_comment_new', Comment_video)
        thread = Thread_VK(listen).start()

    def on_video_comment_edit(self, function):
        listen = self.group_listen_wrapper('video_comment_edit', Comment_video)
        thread = Thread_VK(listen).start()

    def on_video_comment_restore(self, function):
        listen = self.group_listen_wrapper('video_comment_restore', Comment_video)
        thread = Thread_VK(listen).start()

    def on_video_comment_delete(self, function):
        listen = self.group_listen_wrapper('video_comment_delete', Deleted_comment_video)
        thread = Thread_VK(listen).start()

    def on_wall_post_new(self, function):
        listen = self.group_listen_wrapper('wall_post_new', Wall_obj)
        thread = Thread_VK(listen).start()

    def on_wall_repost(self, function):
        listen = self.group_listen_wrapper('wall_repost', Wall_obj)
        thread = Thread_VK(listen).start()

    def on_wall_reply_new(self, function):
        listen = self.group_listen_wrapper('wall_reply_new', Comment_wall)
        thread = Thread_VK(listen).start()

    def on_wall_reply_edit(self, function):
        listen = self.group_listen_wrapper('wall_reply_edit', Comment_wall)
        thread = Thread_VK(listen).start()

    def on_wall_reply_restore(self, function):
        listen = self.group_listen_wrapper('wall_reply_restore', Comment_wall)
        thread = Thread_VK(listen).start()

    def on_wall_reply_delete(self, function):
        listen = self.group_listen_wrapper('wall_reply_delete', Deleted_comment_wall)
        thread = Thread_VK(listen).start()

    def on_board_post_new(self, function):
        listen = self.group_listen_wrapper('board_post_new', Comment_topic)
        thread = Thread_VK(listen).start()

    def on_board_post_edit(self, function):
        listen = self.group_listen_wrapper('board_post_edit', Comment_topic)
        thread = Thread_VK(listen).start()

    def on_board_post_restore(self, function):
        listen = self.group_listen_wrapper('board_post_restore', Comment_topic)
        thread = Thread_VK(listen).start()

    def on_board_post_delete(self, function):
        listen = self.group_listen_wrapper('board_post_delete', Deleted_comment_topic)
        thread = Thread_VK(listen).start()

    def on_market_comment_new(self, function):
        listen = self.group_listen_wrapper('market_comment_new', Comment_marketm)
        thread = Thread_VK(listen).start()

    def on_market_comment_edit(self, function):
        listen = self.group_listen_wrapper('market_comment_edit', Comment_marketm)
        thread = Thread_VK(listen).start()

    def on_market_comment_restore(self, function):
        listen = self.group_listen_wrapper('market_comment_restore', Comment_marketm)
        thread = Thread_VK(listen).start()

    def on_market_comment_delete(self, function):
        listen = self.group_listen_wrapper('market_comment_delete', Deleted_comment_market)
        thread = Thread_VK(listen).start()

    def on_group_join(self, function):
        listen = self.group_listen_wrapper('group_join', Group_join)
        thread = Thread_VK(listen).start()

    def on_group_leave(self, function):
        listen = self.group_listen_wrapper('group_leave', Group_leave)
        thread = Thread_VK(listen).start()

    def on_user_block(self, function):
        listen = self.group_listen_wrapper('user_block', User_block)
        thread = Thread_VK(listen).start()

    def on_user_unblock(self, function):
        listen = self.group_listen_wrapper('user_unblock', User_unblock)
        thread = Thread_VK(listen).start()

    def on_poll_vote_new(self, function):
        listen = self.group_listen_wrapper('poll_vote_new', Poll_vote_new)
        thread = Thread_VK(listen).start()

    def on_group_officers_edit(self, function):
        listen = self.group_listen_wrapper('group_officers_edit', Group_officers_edit)
        thread = Thread_VK(listen).start()

    def on_group_change_settings(self, function):
        listen = self.group_listen_wrapper('group_change_settings', Group_change_settings)
        thread = Thread_VK(listen).start()

    def on_group_change_photo(self, function):
        listen = self.group_listen_wrapper('group_change_photo', Group_change_photo)
        thread = Thread_VK(listen).start()

    def on_vkpay_transaction(self, function):
        listen = self.group_listen_wrapper('vkpay_transaction', Vkpay_transaction)
        thread = Thread_VK(listen).start()

    def on_app_payload(self, function):
        listen = self.group_listen_wrapper('app_payload', App_payload)
        thread = Thread_VK(listen).start()

    def on_error(self, function):
        def parse_error():
            while True:
                if self.longpoll.errors:
                    for error in self.longpoll.errors:
                        function(error)
                        self.longpoll.errors.remove(error)
        Thread_VK(parse_error).start()



    def group_listen_wrapper(self, type_value, class_wrapper):
        def listen():
            for event in self.longpoll.listen():
                if self.group_id:
                    if event.update['type'] == type_value:
                        if self.debug: print(type_value)
                        try:
                            function(class_wrapper(event.update))
                        except Exception as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            line = traceback.extract_tb(exc_tb)[-1][1]
                            self.errors.append(Error(line=line, message=str(e), code=type(e).__name__))
        return listen


    def user_listen_wrapper(self, type_value, class_wrapper):
        def listen():
            for event in self.longpoll.listen():
                if not self.group_id:
                    if event.update[0] == type_value:
                        try:
                            function(class_wrapper(event.update))
                        except Exception as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            line = traceback.extract_tb(exc_tb)[-1][1]
                            self.errors.append(Error(line=line, message=str(e), code=type(e).__name__))
        return listen

    def __str__(self):
        return f'''{"-"*10}
The Vk object with params:
token = {f"{self.token_vk[:5]}{'*'*10}{self.token_vk[-5:]}"}
debug = {self.debug}
version_api = {self.version_api}
group_id = {self.group_id}
{"-"*10}'''

    def __repr__(self):
        return f'''{"-"*10}
The Vk object with params:
token = {f"{self.token_vk[:5]}{'*'*10}{self.token_vk[-5:]}"}
debug = {self.debug}
version_api = {self.version_api}
group_id = {self.group_id}
{"-"*10}'''

class LongPoll:
    '''docstring for LongPoll'''
    def __init__(self, *args, **kwargs):
        self.group_id = kwargs['group_id'] if 'group_id' in kwargs.keys() else None
        self.access_token = kwargs['access_token']
        self.vk_api_url = 'https://api.vk.com/method/'
        self.version_api = kwargs['version_api'] if 'version_api' in kwargs.keys() else '5.101'
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


class Method:
    def __init__(self, *args, **kwargs):
        self.access_token = kwargs['access_token']
        self.vk_api_url = 'https://api.vk.com/method/'
        self.version_api = kwargs['version_api'] if 'version_api' in kwargs.keys() else '5.101'

    def use(self, *args, **kwargs):
        url = f'''{self.vk_api_url}{kwargs["method"]}'''
        data = kwargs
        data['access_token'] = self.access_token
        data['v'] = self.version_api
        del data['method']
        response = requests.post(url, data=data).json()
        return response


class Keyboard:
    def __init__(self, *args, **kwargs):
        self.keyboard = {
            'one_time' : kwargs['one_time'] if 'one_time' in kwargs.keys() else True,
            'buttons' : kwargs['buttons'] if 'buttons' in kwargs.keys() else [[]]
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

        if kwargs['type'] in actions.keys():
            self.action = actions[kwargs['type']]
        else:
            self.action = actions['text']

        self.color = kwargs['color'] if 'color' in kwargs.keys() else ButtonColor.PRIMARY

    def __new__(self, *args, **kwargs):
        self.__init__(self, *args, **kwargs)
        kb = {'action' : self.action, 'color' : self.color}
        if kb['action']['type'] != 'text':
            del kb['color']
        return kb

class ButtonColor:
    PRIMARY = 'primary'
    SECONDARY = 'secondary'
    NEGATIVE = 'negative'
    POSITIVE = 'positive'



class Messages:
    def __init__(self, *args, **kwargs):
        self.method = Method(access_token=kwargs['access_token'], version_api=kwargs['version_api']).use

    def markAsRead(self, message_ids, peer_id, **kwargs):
        return self.method(method='messages.markAsRead', message_ids=message_ids, peer_id=peer_id, **kwargs)

    def pin(self, message_id, **kwargs):
        return self.method(method='messages.pin', message_id=message_id, **kwargs)

    def removeChatUser(self, chat_id, **kwargs):
        return self.method(method='messages.removeChatUser', chat_id=chat_id, **kwargs)

    def restore(self, message_id, **kwargs):
        return self.method(method='messages.restore', message_id=message_id, **kwargs)

    def send(self, *args, **kwargs):
        return self.method(method='messages.send', random_id=random.getrandbits(32)*random.choice([-1, 1]), **kwargs)

    def search(self, q, peer_id, **kwargs):
        return self.method(method='messages.search', q=q, peer_id=peer_id, **kwargs)

    def searchConversations(self, q, **kwargs):
        return self.method(method='messages.searchConversations', q=q, **kwargs)

    def setChatPhoto(self, file, **kwargs):
        return self.method(method='messages.setChatPhoto', file=file, **kwargs)

    def setActivity(self, **kwargs):
        return self.method(method='messages.setActivity', **kwargs)

    def unpin(self, peer_id, **kwargs):
        return self.method(method='messages.unpin', peer_id=peer_id, **kwargs)

class Photos:
    def __init__(self, *args, **kwargs):
        self.method = Method(access_token=kwargs['access_token'], version_api=kwargs['version_api']).use

    def getMarketAlbumUploadServer(self, group_id, **kwargs):
        return self.method(method='photos.getMarketAlbumUploadServer', group_id=group_id, **kwargs)

    def getMarketUploadServer(self, group_id, **kwargs):
        return self.method(method='photos.getMarketUploadServer', group_id=group_id, **kwargs)

    def getChatUploadServer(self, chat_id, **kwargs):
        return self.method(method='photos.getChatUploadServer', chat_id=chat_id, **kwargs)

    def getMessagesUploadServer(self, peer_id, **kwargs):
        return self.method(method='photos.getMessagesUploadServer', peer_id=peer_id, **kwargs)

    def getUploadServer(self, **kwargs):
        return self.method(method='photos.getUploadServer', **kwargs)

    def getWallUploadServer(self, **kwargs):
        return self.method(method='photos.getWallUploadServer', **kwargs)

    def getOwnerPhotoUploadServer(self, user_id, **kwargs):
        return self.method(method='photos.getOwnerPhotoUploadServer', user_id=user_id, **kwargs)

    def save(self, hash, server, photos_list, **kwargs):
        return self.method(method='photos.save', hash=hash, server=server, photos_list=photos_list, **kwargs)

class Audio:
    def __init__(self, *args, **kwargs):
        self.method = Method(access_token=kwargs['access_token'], version_api=kwargs['version_api']).use

    def getUploadServer(self, **kwargs):
        return self.method(method='audio.getUploadServer', **kwargs)

class Video:
    def __init__(self, *args, **kwargs):
        self.method = Method(access_token=kwargs['access_token'], version_api=kwargs['version_api']).use

    def save(self, **kwargs):
        return self.method(method='video.save', **kwargs)

class Docs:
    def __init__(self, *args, **kwargs):
        self.method = Method(access_token=kwargs['access_token'], version_api=kwargs['version_api']).use

    def getMessagesUploadServer(self, **kwargs):
        return self.method(method='docs.getMessagesUploadServer', **kwargs)










# Enums start here:
class Event:
    '''docstring for Event'''
    def __init__(self, *args, **kwargs):
        self.update = kwargs['update']

    def __repr__(self):
        return f'{self.update}'

class Thread_VK(Thread):
    def __init__(self, function):
        Thread.__init__(self)
        self.function = function
    def run(self):
        self.function()

# Super classes:
class Wrapper_obj:
    def has(self, key):
        return key in self.obj
class Comment(Wrapper_obj):
    def __init__(self, obj):
        self.id = obj['id'] if 'id' in obj.keys() else None
        self.from_id = obj['from_id'] if 'from_id' in obj.keys() else None
        self.date = obj['date'] if 'date' in obj.keys() else None
        self.strdate = datetime.datetime.utcfromtimestamp(self.date).strftime('%d.%m.%Y %H:%M:%S')
        self.text = obj['text'] if 'text' in obj.keys() else None
        self.reply_to_user = obj['reply_to_user'] if 'reply_to_user' in obj.keys() else None
        self.reply_to_comment = obj['reply_to_comment'] if 'reply_to_comment' in obj.keys() else None
        self.attachments = obj['attachments'] if 'attachments' in obj.keys() else None
        self.parents_stack = obj['parents_stack'] if 'parents_stack' in obj.keys() else None
        self.thread = obj['thread'] if 'thread' in obj.keys() else None
        self.likes = obj['likes'] if 'likes' in obj.keys() else None
        self.obj = obj

    def __repr__(self):
        return f'''{self.text}, {self.strdate}.
photo ID: {self.id}'''
class Deleted_comment(Wrapper_obj):
    def __init__(self, obj):
        self.owner_id = obj['owner_id'] if 'owner_id' in obj.keys() else None
        self.deleter_id = obj['deleter_id'] if 'deleter_id' in obj.keys() else None
        self.user_id = obj['user_id'] if 'user_id' in obj.keys() else None
        self.id = obj['id'] if 'id' in obj.keys() else None
        self.obj = obj

class Error:
    def __init__(self, *args, **kwargs):
        self.code = kwargs['code']
        self.message = kwargs['message']
        self.line = kwargs['line']

    def __str__(self):
        return f'{self.code}:\n{self.message}. Line {self.line}'
    def __repr__(self):
        return f'{self.code}:\n{self.message}. Line {self.line}'


# Other classes:
class New_group_message(Wrapper_obj):
    def __init__(self, obj):
        self.date = obj['date']
        self.strdate = datetime.datetime.utcfromtimestamp(self.date).strftime('%d.%m.%Y %H:%M:%S')
        self.text = obj['text']
        self.from_id = obj['from_id']
        self.peer_id = obj['peer_id']
        self.out = obj['out']
        self.id = obj['id']
        self.conversation_message_id = obj['conversation_message_id']
        self.fwd_messages = obj['fwd_messages']
        self.important = obj['important']
        self.random_id = obj['random_id']
        self.attachments = obj['attachments']
        self.is_hidden = obj['is_hidden']
        self.action = obj['action'] if 'action' in obj.keys() else None
        self.obj = obj

    def __repr__(self):
        if not self.action:
            return f'''
{self.text}
{self.strdate}
ID: {self.id}
Hidden: {self.is_hidden}
Peer id: {self.peer_id}
From ID: {self.from_id}
'''
        else:
            return f'''
{self.strdate}
{self.action['type']}
ID: {self.id}
Hidden: {self.is_hidden}
Peer id: {self.peer_id}
'''

class Edit_group_message(Wrapper_obj):
    def __init__(self, obj):
        self.date = obj['date']
        self.strdate = datetime.datetime.utcfromtimestamp(self.date).strftime('%d.%m.%Y %H:%M:%S')
        self.text = obj['text']
        self.from_id = obj['from_id']
        self.peer_id = obj['peer_id']
        self.out = obj['out']
        self.id = obj['id']
        self.conversation_message_id = obj['conversation_message_id']
        self.fwd_messages = obj['fwd_messages']
        self.important = obj['important']
        self.random_id = obj['random_id']
        self.attachments = obj['attachments']
        self.is_hidden = obj['is_hidden']
        self.obj = obj

    def __repr__(self):
        return f'''
{self.text}
{self.strdate}
ID: {self.id}
Hidden: {self.is_hidden}
Peer id: {self.peer_id}
From ID: {self.from_id}
'''

class New_photo_group(Wrapper_obj):
    def __init__(self, obj):
        self.id = obj['id'] if 'id' in obj.keys() else None
        self.album_id = obj['album_id'] if 'album_id' in obj.keys() else None
        self.user_id = obj['user_id'] if 'user_id' in obj.keys() else None
        self.owner_id = obj['owner_id'] if 'owner_id' in obj.keys() else None
        self.text = obj['text'] if 'text' in obj.keys() else None
        self.date = obj['date'] if 'date' in obj.keys() else None
        self.strdate = datetime.datetime.utcfromtimestamp(self.date).strftime('%d.%m.%Y %H:%M:%S')
        self.sizes = obj['sizes'] if 'sizes' in obj.keys() else None
        self.obj = obj

    def __repr__(self):
        return f'''photo{self.owner_id}_{self.id}'''


class Comment_photo_group(Comment):
    def __init__(self, obj):
        Comment.__init__(self, obj)
        self.photo_id = obj['photo_id'] if 'photo_id' in obj.keys() else None
        self.photo_owner_id = obj['photo_owner_id'] if 'photo_owner_id' in obj.keys() else None
class Comment_video(Comment):
    def __init__(self, obj):
        Comment.__init__(self, obj)
        self.video_id = obj['video_id'] if 'video_id' in obj.keys() else None
        self.video_owner_id = obj['video_owner_id'] if 'video_owner_id' in obj.keys() else None
class Comment_wall(Comment):
    def __init__(self, obj):
        Comment.__init__(self, obj)
        self.post_id = obj['post_id'] if 'post_id' in obj.keys() else None
        self.post_owner_id = obj['post_owner_id'] if 'post_owner_id' in obj.keys() else None
class Comment_topic(Comment):
    def __init__(self, obj):
        Comment.__init__(self, obj)
        self.topic_id = obj['topic_id'] if 'topic_id' in obj.keys() else None
        self.topic_owner_id = obj['topic_owner_id'] if 'topic_owner_id' in obj.keys() else None
class Comment_market(Comment):
    def __init__(self, obj):
        Comment.__init__(self, obj)
        self.item_id = obj['item_id'] if 'item_id' in obj.keys() else None
        self.market_owner_id = obj['market_owner_id'] if 'market_owner_id' in obj.keys() else None


class Deleted_comment_photo(Deleted_comment):
    def __init__(self, obj):
        Deleted_comment.__init__(self, obj)
        self.photo_id = obj['photo_id'] if 'photo_id' in obj.keys() else None
class Deleted_comment_video(Deleted_comment):
    def __init__(self, obj):
        Deleted_comment.__init__(self, obj)
        self.video_id = obj['video_id'] if 'video_id' in obj.keys() else None
class Deleted_comment_wall(Deleted_comment):
    def __init__(self, obj):
        Deleted_comment.__init__(self, obj)
        self.post_id = obj['post_id'] if 'post_id' in obj.keys() else None
class Deleted_comment_topic(Deleted_comment):
    def __init__(self, obj):
        Deleted_comment.__init__(self, obj)
        self.topic_id = obj['topic_id'] if 'topic_id' in obj.keys() else None
        self.topic_owner_id = obj['topic_owner_id'] if 'topic_owner_id' in obj.keys() else None
class Deleted_comment_market(Deleted_comment):
    def __init__(self, obj):
        Deleted_comment.__init__(self, obj)
        self.item_id = obj['item_id'] if 'item_id' in obj.keys() else None


class Audio_obj(Wrapper_obj):
    def __init__(self, obj):
        self.id = obj['id'] if 'id' in obj.keys() else None
        self.owner_id = obj['owner_id'] if 'owner_id' in obj.keys() else None
        self.artist = obj['artist'] if 'artist' in obj.keys() else None
        self.title = obj['title'] if 'title' in obj.keys() else None
        self.duration = obj['duration'] if 'duration' in obj.keys() else None
        self.url = obj['url'] if 'url' in obj.keys() else None
        self.lyrics_id = obj['lyrics_id'] if 'lyrics_id' in obj.keys() else None
        self.album_id = obj['album_id'] if 'album_id' in obj.keys() else None
        self.genre_id = obj['genre_id'] if 'genre_id' in obj.keys() else None
        self.date = obj['date'] if 'date' in obj.keys() else None
        self.strdate = datetime.datetime.utcfromtimestamp(self.date).strftime('%d.%m.%Y %H:%M:%S')
        self.no_search = obj['no_search'] if 'no_search' in obj.keys() else None
        self.is_hq = obj['is_hq'] if 'is_hq' in obj.keys() else None
        self.obj = obj

    def __repr__(self):
        return f'''{self.title} ({self.artist})
{self.duration}
{self.url}'''

class Video_obj(Wrapper_obj):
    def __init__(self, obj):
        self.id = obj['id'] if 'id' in obj.keys() else None
        self.owner_id = obj['owner_id'] if 'owner_id' in obj.keys() else None
        self.title = obj['title'] if 'title' in obj.keys() else None
        self.description = obj['description'] if 'description' in obj.keys() else None
        self.duration = obj['duration'] if 'duration' in obj.keys() else None
        self.date = obj['date'] if 'date' in obj.keys() else None
        self.strdate = datetime.datetime.utcfromtimestamp(self.date).strftime('%d.%m.%Y %H:%M:%S')
        self.views = obj['views'] if 'views' in obj.keys() else None
        self.adding_date = obj['adding_date'] if 'adding_date' in obj.keys() else None
        self.comments = obj['comments'] if 'comments' in obj.keys() else None
        self.player = obj['player'] if 'player' in obj.keys() else None
        self.platform = obj['platform'] if 'platform' in obj.keys() else None
        self.can_add = obj['can_add'] if 'can_add' in obj.keys() else None
        self.can_edit = obj['can_edit'] if 'can_edit' in obj.keys() else None
        self.is_private = obj['is_private'] if 'is_private' in obj.keys() else None
        self.access_key = obj['access_key'] if 'access_key' in obj.keys() else None
        self.processing = obj['processing'] if 'processing' in obj.keys() else None
        self.live = obj['live'] if 'live' in obj.keys() else None
        self.uncomming = obj['uncomming'] if 'uncomming' in obj.keys() else None
        self.is_favorite = obj['is_favorite'] if 'is_favorite' in obj.keys() else None
        self.obj = obj

    def __repr__(self):
        return f'''
'''

class Wall_obj(Wrapper_obj):
    def __init__(self, obj):
        self.id = obj['id'] if 'id' in obj.keys() else None
        self.owner_id = obj['owner_id'] if 'owner_id' in obj.keys() else None
        self.from_id = obj['from_id'] if 'from_id' in obj.keys() else None
        self.created_by = obj['created_by'] if 'created_by' in obj.keys() else None
        self.text = obj['text'] if 'text' in obj.keys() else None
        self.date = obj['date'] if 'date' in obj.keys() else None
        self.strdate = datetime.datetime.utcfromtimestamp(self.date).strftime('%d.%m.%Y %H:%M:%S')
        self.views = obj['views'] if 'views' in obj.keys() else None
        self.reply_owner_id = obj['reply_owner_id'] if 'reply_owner_id' in obj.keys() else None
        self.reply_post_id = obj['reply_post_id'] if 'reply_post_id' in obj.keys() else None
        self.friends_only = obj['friends_only'] if 'friends_only' in obj.keys() else None
        self.comments = obj['comments'] if 'comments' in obj.keys() else None
        self.likes = obj['likes'] if 'likes' in obj.keys() else None
        self.reposts = obj['reposts'] if 'reposts' in obj.keys() else None
        self.post_type = obj['post_type'] if 'post_type' in obj.keys() else None
        self.post_source = obj['post_source'] if 'post_source' in obj.keys() else None
        self.attachments = obj['attachments'] if 'attachments' in obj.keys() else None
        self.geo = obj['geo'] if 'geo' in obj.keys() else None
        self.signer_id = obj['signer_id'] if 'signer_id' in obj.keys() else None
        self.can_pin = obj['can_pin'] if 'can_pin' in obj.keys() else None
        self.can_delete = obj['can_delete'] if 'can_delete' in obj.keys() else None
        self.can_edit = obj['can_edit'] if 'can_edit' in obj.keys() else None
        self.is_pinned = obj['is_pinned'] if 'is_pinned' in obj.keys() else None
        self.marked_as_ads = obj['marked_as_ads'] if 'marked_as_ads' in obj.keys() else None
        self.is_favorite = obj['is_favorite'] if 'is_favorite' in obj.keys() else None
        self.postponed_id = obj['postponed_id'] if 'postponed_id' in obj.keys() else None
        self.obj = obj

    def __repr__(self):
        return f'''
'''

class Group_leave(Wrapper_obj):
    def __init__(self, obj):
        self.user_id = obj['user_id'] if 'user_id' in obj.keys() else None
        self.self = obj['self'] if 'self' in obj.keys() else None
        self.obj = obj
class Group_join(Wrapper_obj):
    def __init__(self, obj):
        self.user_id = obj['user_id'] if 'user_id' in obj.keys() else None
        self.join_type = obj['join_type'] if 'join_type' in obj.keys() else None
        self.obj = obj
class User_block(Wrapper_obj):
    def __init__(self, obj):
        self.user_id = obj['user_id'] if 'user_id' in obj.keys() else None
        self.admin_id = obj['admin_id'] if 'admin_id' in obj.keys() else None
        self.unblock_date = obj['unblock_date'] if 'unblock_date' in obj.keys() else None
        self.reason = obj['reason'] if 'reason' in obj.keys() else None
        self.obj = obj
class User_unblock(Wrapper_obj):
    def __init__(self, obj):
        self.user_id = obj['user_id'] if 'user_id' in obj.keys() else None
        self.admin_id = obj['admin_id'] if 'admin_id' in obj.keys() else None
        self.by_end_date = obj['by_end_date'] if 'by_end_date' in obj.keys() else None
        self.obj = obj


class Poll_vote_new(Wrapper_obj):
    def __init__(self, obj):
        self.user_id = obj['user_id'] if 'user_id' in obj.keys() else None
        self.owner_id = obj['owner_id'] if 'owner_id' in obj.keys() else None
        self.option_id = obj['option_id'] if 'option_id' in obj.keys() else None
        self.poll_id = obj['poll_id'] if 'poll_id' in obj.keys() else None
        self.obj = obj

class Group_officers_edit(Wrapper_obj):
    def __init__(self, obj):
        self.admin_id = obj['admin_id'] if 'admin_id' in obj.keys() else None
        self.user_id = obj['user_id'] if 'user_id' in obj.keys() else None
        self.level_old = obj['level_old'] if 'level_old' in obj.keys() else None
        self.level_new = obj['level_new'] if 'level_new' in obj.keys() else None
        self.obj = obj

class Group_change_settings(Wrapper_obj):
    def __init__(self, obj):
        self.user_id = obj['user_id'] if 'user_id' in obj.keys() else None
        self.changes = obj['changes'] if 'changes' in obj.keys() else None
        self.old_value = obj['old_value'] if 'old_value' in obj.keys() else None
        self.new_value = obj['new_value'] if 'new_value' in obj.keys() else None

class Group_change_photo(Wrapper_obj):
    def __init__(self, *args, **kwargs):
        self.user_id = obj['user_id'] if 'user_id' in obj.keys() else None
        self.photo = obj['photo'] if 'photo' in obj.keys() else None

class Vkpay_transaction(Wrapper_obj):
    def __init__(self, *args, **kwargs):
        self.from_id = obj['from_id'] if 'from_id' in obj.keys() else None
        self.amount = obj['amount'] if 'amount' in obj.keys() else None
        self.description = obj['description'] if 'description' in obj.keys() else None
        self.date = obj['date'] if 'date' in obj.keys() else None
        self.strdate = datetime.datetime.utcfromtimestamp(self.date).strftime('%d.%m.%Y %H:%M:%S')

class App_payload(Wrapper_obj):
    def __init__(self, *args, **kwargs):
        self.user_id = obj['user_id'] if 'user_id' in obj.keys() else None
        self.app_id = obj['app_id'] if 'app_id' in obj.keys() else None
        self.payload = obj['payload'] if 'payload' in obj.keys() else None
        self.group_id = obj['group_id'] if 'group_id' in obj.keys() else None





class New_user_message(Wrapper_obj):
    def __init__(self, obj):
        self.date = obj[4]
        self.strdate = datetime.datetime.utcfromtimestamp(self.date).strftime('%d.%m.%Y %H:%M:%S')
        self.text = obj[5]
        self.from_id = obj[6]['from'] if 'from' in obj[6].keys() else None
        self.peer_id = obj[3]
        self.message_id = obj[1]
        self.random_id = obj[8]
        self.attachments = obj[7]
        self.obj = obj

    def __repr__(self):
        return f'''
{self.text}
{self.strdate}
ID: {self.message_id}
Peer id: {self.peer_id}
From ID: {self.from_id}
'''

class Edit_user_message(Wrapper_obj):
    def __init__(self, obj):
        self.message_id = obj[1]
        self.mask = obj[2]
        self.peer_id = obj[3]
        self.date = obj[4]
        self.strdate = datetime.datetime.utcfromtimestamp(self.date).strftime('%d.%m.%Y %H:%M:%S')
        self.text = obj[5]
        self.attachments = obj[6]
        self.obj = obj

    def __repr__(self):
        return f'''
{self.text}
{self.strdate}
ID: {self.message_id}
Peer id: {self.peer_id}
'''

class Translator_debug:
    def __init__(self, *args, **kwargs):
        self.base = {
            'Токен установлен. Проверяем его валидность ...' : {
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

class Smile:
    ANGEL = '&#128124;'
    ALIEN = '&#128125;'
    ALIEN_MONSTER = '&#128126;'
    BUST_SILHOUETTE = '&#128100;'
    BUST_SILHOUETTES = '&#128101;'
    CLOWN = '&#129313;'
    COOL = '&#127378;'
    EAR = '&#128066;'
    EVIL_IMP = '&#128527;'
    EYE = '&#128065;'
    EYES = '&#128064;'
    GHOST = '&#128123;'
    GOOD_IMP = '&#128520;'
    FREE = '&#127379;'
    ID = '&#127380;'
    JAPANESE_GOBLIN = '&#128122;'
    JAPANESE_OGRE = '&#128121;'
    HUMAN_SILHOUETTE = '&#128483;'
    NEW = '&#127381;'
    NG = '&#127382;'
    NOSE = '&#128067;'
    LETTER_A = '&#127344;'
    LETTER_B = '&#127345;'
    LETTER_O = '&#127358;'
    LETTER_P = '&#127359;'
    LETTERS_AB = '&#127374;'
    LETTERS_ABCD = '&#128288;'
    LETTERS_ABCD_1 = '&#128289;'
    LETTERS_1324 = '&#128290;'
    LETTERS_ABC = '&#128292;'
    LETTER_I = '&#8505;'
    LETTERS_CL = '&#127377;'
    LIPS = '&#128068;'
    ROBOT = '&#129302;'
    OK = '&#127383;'
    SKULL = '&#128128;'
    SYMBOLS = '&#128291;'
    VS = '&#127386;'
    UP = '&#127385;'
    XD = '&#128518;'