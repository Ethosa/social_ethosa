# -*- coding: utf-8 -*-
# author: ethosa
from ..utils import browserFake
from .vkauth import VKAuth
import requests
import json
import re

class Audio:
    """
    docstring for Audio

    usage:
    audio = Audio(login='Your login', password='Your password')

    printf(audio.get())
    """
    def __init__(self, login="", password=""):
        auther = VKAuth(login, password)
        response = auther.logIn()
        url = 'https://vk.com%s' % response.text.split('onLoginDone(', 1)[1].split("'")[1]
        self.session = auther.session
        self.user_id = self.session.get(url).text.split('<a id="profile_photo_link"', 1)[1].split('/photo', 1)[1].split('_', 1)[0]

    def get(self, owner_id=None, offset=0, count=None):

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
        

    def getCount(self, owner_id=None):
        return len(self.get(owner_id if owner_id else self.user_id))

    def getById(self, audio_id, owner_id=None):
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

    def search(self, q=None):
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
