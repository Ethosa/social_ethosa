# -*- coding: utf-8 -*-
# author: ethosa
from ..utils import *
import re

class Audio:
    """
    docstring for Audio

    usage:
    audio = Audio(login='Your login', password='Your password')

    printf(audio.get())
    """
    def __init__(self, *args, **kwargs):
        self.login = getValue(kwargs, 'login', '')
        self.password = getValue(kwargs, 'password', '')
        self.debug = getValue(kwargs, 'debug')
        self.lang = getValue(kwargs, 'lang', 'en')
        url = 'https://vk.com'

        self.translate = TranslatorDebug().translate
        self.session = requests.session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
            'Accept-Encoding':'gzip, deflate',
            'Connection':'keep-alive',
            'DNT':'1'
        }
        data = self.session.get(url).text
        start = re.search("<form.+name=\"login.+", data).start()
        end = re.search("<input type=\"submit\" class=\"submit\" />", data).start()
        data = data[start:end]
        lg_h = re.findall("<input.+lg_h.+", data)[0]
        lg_h = lg_h.split("value=\"", 1)[1].split("\"", 1)[0].strip()
        ip_h = re.findall("<input.+ip_h.+", data)[0]
        ip_h = ip_h.split("value=\"", 1)[1].split("\"", 1)[0].strip()
        form = {'act' : 'login', 'role' : 'al_frame', 'expire' : '',
                'recaptcha' : '', 'captcha_sid' : '', 'captcha_key' : '',
                '_origin': 'https://vk.com', 'ip_h': ip_h,
                'lg_h': lg_h, 'ul': '',
                'email': self.login, 'pass': self.password}

        response = self.session.post("https://login.vk.com/", data=form)
        if self.debug: print(self.translate(u'Успешно!' if 'onLoginDone' in response.text else u'Ошибка', self.lang))
        if 'onLoginDone' in response.text:
            url = 'https://vk.com%s' % response.text.split('onLoginDone(', 1)[1].split("'")[1]

            self.user_id = self.session.get(url).text.split('<a id="profile_photo_link"', 1)[1].split('/photo', 1)[1].split('_', 1)[0]

    def get(self, owner_id=None, offset=0, count=None, *args, **kwargs):

        # params owner_id, offset and count must be integer
        # get() method return list of dictionaries with audios

        owner_id = owner_id if owner_id else self.user_id
        url = 'https://vk.com/audios%s' % owner_id

        response = self.session.get(url).text.split('<div class="audio_page__audio_rows_list _audio_page__audio_rows_list _audio_pl audio_w_covers "', 1)[1].split('</div></div><div class="audio_', 1)[0].replace('&amp;', '&').replace('&quot;', '"').split('<div')
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

        return audios[offset:] if not count else audios[offset:count+offset]
        

    def getCount(self, owner_id=None, *args, **kwargs):
        return len(self.get(owner_id if owner_id else self.user_id))

    def getById(self, audio_id, owner_id=None, *args, **kwargs):
        owner_id = owner_id if owner_id else self.user_id
        url = 'https://m.vk.com/audio%s_%s' % (owner_id, audio_id)

        response = self.session.get(url).text.split('<div id="audio%s_%s' % (owner_id, audio_id))[1].split('<div class="ai_controls">', 1)[0].replace('&quot;', '"')

        audio_url = response.split('<input type="hidden" value="', 1)[1].split('">', 1)[0]
        data_audio = json.loads(response.split('data-ads="', 1)[1].split('"  class="', 1)[0])
        title = response.split('<span class="ai_title">', 1)[1].split('</span>', 1)[0]
        artist = response.split('<span class="ai_artist">', 1)[1].split('</span>', 1)[0]

        return {
            'url' : audio_url,
            'duration' : data_audio['duration'],
            'content_id' : data_audio['content_id'],
            'genre_id' : data_audio['puid22'],
            'title' : title,
            'artist' : artist
        }

    def search(self, q=None, *args, **kwargs):
        url = 'https://m.vk.com/audios%s?q=%s' % (self.user_id, q)
        response = self.session.get(url).text

        artists = response.split('ColumnSlider__column', 1)[1].split('</div></div></div></div>')[0].split('OwnerRow__content al_artist"')
        playlists = response.split('AudioPlaylistSlider ColumnSlider Slider', 1)[1].split('Slider__line">', 1)[1].split('</div></div></div></div>')[0].split('ColumnSlider__column">')
        artists.pop(0)
        playlists.pop(0)

        allPlaylists = [{
                    'url' : playlist.split('href="', 1)[1].split('"', 1)[0],
                    'cover' : playlist.split('audioPlaylists__itemCover', 1)[1].split("url('", 1)[1].split("');", 1)[0],
                    'title' : playlist.split('audioPlaylists__itemTitle">', 1)[1].split('</', 1)[0],
                    'subtitle' : playlist.split('audioPlaylists__itemSubtitle">', 1)[1].split('<', 1)[0],
                    'year' : playlist.split('audioPlaylists__itemSubtitle">', 2)[2].split('<', 1)[0]
                } for playlist in playlists]
        allArtists = [{ artist.split('OwnerRow__title">')[1].split('<', 1)[0] : artist.split('href="', 1)[1].split('"', 1)[0] }
                        for artist in artists]

        url = "https://m.vk.com%s" % response.split('AudioBlock AudioBlock_audios Pad', 1)[1].split("Pad__corner al_empty", 1)[1].split('href="', 1)[1].split('"', 1)[0]
        response = self.session.get(url).text

        audios = response.split('artist_page_search_items">', 1)[1].split('</div></div></div></div>')[0].split('<div id="audio')
        audios.pop(0)

        allAudios = []
        for audio in audios:
            if '<input type="hidden" value="' in audio:
                data_audio = json.loads(audio.split('data-ads="', 1)[1].split('" ', 1)[0].replace('&quot;', '"'))
                allAudios.append({
                        'url' : audio.split('<input type="hidden" value="', 1)[1].split('"', 1)[0],
                        'image' : audio.split('ai_info')[1].split(':url(', 1)[1].split(')', 1)[0] if 'ai_info' in audio and ':url(' in audio else None,
                        'duration' : data_audio['duration'],
                        'content_id' : data_audio['content_id'],
                        'genre_id' : data_audio['puid22'],
                        'title' : audio.split('<span class="ai_title">', 1)[1].split('</span>', 1)[0],
                        'artist' : audio.split('<span class="ai_artist">', 1)[1].split('</span>', 1)[0]
                    })

        return {
            'playlists' : allPlaylists,
            'audios' : allAudios,
            'artists' : allArtists
        }

    def parse(self, data_audio):
        return { 'id' : data_audio[0],
            'owner_id' : data_audio[1],
            'artist' : data_audio[4],
            'title' : data_audio[3],
            'duration' : data_audio[5],
            'cover' : data_audio[14].split(','),
            'is_hq' : data_audio[-2],
            'no_search' : data_audio[-3],
            'genre_id' : data_audio[-10]['puid22']}