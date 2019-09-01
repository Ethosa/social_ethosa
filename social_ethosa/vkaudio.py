from .utils import *
import lxml.html

class VkAudio:

    """
    docstring for VkAudio

    usage:
    audio = VkAudio(login='Your login', password='Your password')

    """

    def __init__(self, *args, **kwargs):
        self.login = get_val(kwargs, 'login', '')
        self.password = get_val(kwargs, 'password', '')
        self.debug = get_val(kwargs, 'debug')
        self.lang = get_val(kwargs, 'lang', 'en')
        url = 'https://vk.com'

        self.translate = Translator_debug().translate

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
            'Accept-Encoding':'gzip, deflate',
            'Connection':'keep-alive',
            'DNT':'1'
        }
        self.session = requests.session()
        data = self.session.get(url, headers=self.headers)
        page = lxml.html.fromstring(data.content)

        form = page.forms[0]
        form.fields['email'] = self.login
        form.fields['pass'] = self.password

        response = self.session.post(form.action, data=form.form_values())
        if self.debug: print(self.translate('Успешно!' if 'onLoginDone' in response.text else 'Ошибка', self.lang))
        if 'onLoginDone' in response.text:
            url = f'''https://vk.com{response.text.split('onLoginDone(', 1)[1].split("'")[1]}'''

            self.user_id = self.session.get(url, headers=self.headers).text.split('<a id="profile_photo_link"', 1)[1].split('/photo', 1)[1].split('_', 1)[0]

    def get(self, owner_id=None, offset=0, count=None, *args, **kwargs):

        # params owner_id, offset and count must be integer
        # get() method return list of dictionaries with audios

        owner_id = owner_id if owner_id else self.user_id
        url = f'https://vk.com/audios{owner_id}'

        response = self.session.get(url, headers=self.headers).text.split('<div class="audio_page__audio_rows_list _audio_page__audio_rows_list _audio_pl audio_w_covers "', 1)[1].split('</div></div><div class="audio_', 1)[0].replace('&amp;', '&').replace('&quot;', '"').split('<div')
        response.pop(0)

        audios = []
        for audio in response:
            if 'data-full-id="' in audio:
                current_full_id = audio.split('data-full-id="', 1)[1].split('"')[0]
                current_data_audio = json.loads(audio.split('data-audio="', 1)[1].split('" onmouseover')[0])
                audios.append({
                        'data-full-id' : current_full_id,
                        'data-audio' : self.parse(current_data_audio)
                    })

        if not count:
            return audios[offset:]
        else:
            return audios[offset:count]

    def getCount(self, owner_id=None, *args, **kwargs):
        return len(self.get(owner_id if owner_id else self.user_id))

    def parse(self, data_audio):
        return {
            'id' : data_audio[0],
            'owner_id' : data_audio[1],
            'artist' : data_audio[4],
            'title' : data_audio[3],
            'duration' : data_audio[5],
            'cover' : data_audio[14].split(','),
            'is_hq' : data_audio[-2],
            'no_search' : data_audio[-3],
            'genre_id' : data_audio[-10]['puid22']
        }