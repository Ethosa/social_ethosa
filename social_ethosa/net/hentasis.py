# -*- coding: utf-8 -*-
# author: Ethosa

from ..utils import browserFake
import requests
import random
import re

class Hentasis:
    def __init__(self):
        self.url = "http://hentasis.top/"
        self.session = requests.Session()
        self.session.headers = browserFake

    def getPage(self, pageNum=1):
        """get hentai page
        
        Keyword Arguments:
            pageNum {number} -- number of hentai page (default: {1})
        
        Returns:
            HMainPage -- main page
        """
        response = HMainPage(self.session.get("%spage/1/" % self.url), self.session)
        return response

    def getRandom(self):
        """get random hentai
        
        Returns:
            HPage -- hentai page
        """
        page = random.randint(0, 54)
        num = random.randint(0, 10)
        return self.getPage(page).get(num)


class HMainPage:
    def __init__(self, response, session):
        self.page = response.text
        self.session = session
        end = re.search("<div id='dle-content'>", self.page).end()
        hentai = self.page[end:].split('<div class="short-item">')
        hentai.pop(0)
        self.list = []
        for h in hentai:
            h = h.replace("&#039;", "'")
            current = {}
            current["name"] = h.split("short-link nowrap", 1)[1].split(">", 1)[1].split("<", 1)[0]
            current["url"] = h.split("short-link nowrap", 1)[1].split('href="', 1)[1].split('"', 1)[0]
            current["image"] = "%s%s" % ("http://hentasis.top", h.split('class="short-img">', 1)[1].split('src="', 1)[1].split('"', 1)[0])
            current["year"] = h.split('<div class="mov-label"><b>Год выпуска:</b></div>', 1)[1].split("<", 1)[0].strip()
            current["genre"] = h.split('class="mov-label"><b>Жанр:</b></div>', 1)[1].split("<", 1)[0].strip()
            current["episodes"] = h.split('<div class="mov-label"><b>Эпизоды:</b></div>', 1)[1].split('<', 1)[0].strip()
            current["time"] = h.split('class="mov-label"><b>Продолжительность:</b></div>', 1)[1].split('<', 1)[0].strip()
            current["censored"] = h.split('<div class="mov-label"><b>Цензура:</b></div>', 1)[1].split('<', 1)[0].strip()
            current["rusVoice"] = h.split('<div class="mov-label"><b>Русская озвучка:</b></div>', 1)[1].split('<', 1)[0].strip()
            current["rusSub"] = h.split('<div class="mov-label"><b>Русские субтитры:</b></div>', 1)[1].split('<', 1)[0].strip()
            try:
                current["produser"] = h.split('<div class="mov-label"><b>Режиссер:</b></div>', 1)[1].split('<', 1)[0].strip()
            except:
                current["produser"] = ""
            current["studio"] = h.split('div class="mov-label"><b>Студия:</b></div>', 1)[1].split('<', 1)[0].strip()
            current["studio"] = h.split('div class="mov-label"><b>Студия:</b></div>', 1)[1].split('<', 1)[0].strip()
            current["description"] = h.split('Описание:<br /></b></div>', 1)[1].split('</li>', 1)[0]
            self.list.append(current)

    def get(self, number):
        return HPage(self.list[number], self.session)

    def count(self):
        return len(self.list)


class HPage:
    def __init__(self, h, session):
        for key in h:
            exec("self.%s = %s" % (key, repr(h[key])))
        self.page = session.get(self.url).text
        self.videos = re.findall(r"http://.+mp4", self.page)
        self.dict = h

