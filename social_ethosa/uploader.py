from .utils import *
from .vkcom import Method

class Uploader:

    """
    docstring for uploader
    """

    def __init__(self, *args, **kwargs):
        self.vk = get_val(kwargs, 'vk')
        if self.vk:
            self.debug = self.vk.debug
            self.lang = self.vk.lang
            self.translate = self.vk.translate
            self.method = self.vk.method
            self.token = self.vk.token
            self.group_id = self.vk.group_id
            self.version_api =self.vk.version_api
            self.working = True
            self.types = {
                'album_photo' : ['file', lambda album_id, **kwargs: self.vk.photos.getUploadServer(album_id=album_id, **kwargs)['response']['upload_url'],
                                lambda response: self.method(method='photos.save', hash=response['hash'], album_id=album_id,
                                                             server=response['server'], photos_list=response['photos_list'], aid=response['aid'])['response']],
                'wall_photo' : ['file', lambda **kwargs: self.vk.photos.getWallUploadServer(**kwargs)['response']['upload_url'],
                                lambda response, **kwargs: self.method(method='photos.saveWallPhoto', hash=response['hash'],
                                                             server=response['server'], photo=response['photo'], **kwargs)['response'][0]],
                'message_photo' : ['photo', lambda **kwargs: self.vk.photos.getMessagesUploadServer(**kwargs)['response']['upload_url'],
                                   lambda response: self.method(method='photos.saveMessagesPhoto', hash=response['hash'],
                                                                server=response['server'], photo=response['photo'])['response'][0]],
                'user_photo' : ['photo', lambda user_id, **kwargs: self.vk.photos.getOwnerPhotoUploadServer(user_id)['response']['upload_url'],
                                lambda response: self.method(method='photos.saveOwnerPhoto', hash=response['hash'],
                                                             server=response['server'], photo=response['photo'])['response']],
                'chat_photo' : ['photo', lambda chat_id, **kwargs: self.vk.photos.getChatUploadServer(chat_id)['response']['upload_url'],
                                lambda response: self.method(method='messages.setChatPhoto', file=response['response'])['response']],
                'market_photo' : ['photo', lambda group_id, **kwargs: self.vk.photos.getMarketUploadServer(group_id=group_id)['response']['upload_url'],
                                  lambda response: self.method(method='photos.saveMarketPhoto', group_id=group_id, photo=response['photo'],
                                                               hash=response['hash'], server=response['server'], crop_data=response['crop_data'],
                                                               crop_hash=response['crop_hash'])['response']],
                'market_album_photo' : ['file', lambda group_id, **kwargs: self.vk.photos.getMarketAlbumUploadServer(group_id=group_id)['response']['upload_url'],
                                        lambda response: self.method(method='photos.saveMarketAlbumPhoto', group_id=group_id, photo=response['photo'],
                                                                     hash=response['hash'], server=response['server'])['response']],
                'audio' : ['file', lambda **kwargs: self.vk.audio.getUploadServer()['response']['upload_url'],
                           lambda response: self.method(method='audio.save', title=title, artist=artist, audio=response['audio'],
                                                        hash=response['hash'], server=response['server'])['response']],
                'audio_message' : ['file', lambda peer_id, **kwargs: self.vk.docs.getMessagesUploadServer(type='audio_message', peer_id=peer_id, **kwargs)['response']['upload_url'],
                                   lambda response: self.method(method='docs.save', file=response, **kwargs)['response']],
                'doc_message' : ['file', lambda type, **kwargs: self.vk.docs.getMessagesUploadServer(type=type, **kwargs)['response']['upload_url'],
                                 lambda response: self.method(method='docs.save', file=response, **kwargs)['response']],
                'video' : ['file', lambda **kwargs: self.vk.video.save(**kwargs)['response']['upload_url']]
            }
        else:
            self.working = False
            self.error_msg()
        self.url = ''
        self.current = ''


    def getUploadUrl(self, type_obj, *args, **kwargs):
        if self.working:
            self.url = get_val(self.types, type_obj)[1](**kwargs)
            self.current = type_obj
            if self.debug: print(self.translate('Ошибка' if not self.url else 'Успешно!', self.lang))
        else:
            self.error_msg()

    def uploadFile(self, file, *args, **kwargs):

        # usage:
        # param file must be path to file
        file = upl(file, self.types[self.current][0])

        if len(self.types[self.current]) > 2:
            response = upload_files(self.url, file)
            return self.types[self.current][2](response, **kwargs)
        else:
            return upload_files(self.url, file)

    def error_msg(self):
        print('param "vk" undefined')