# -*- coding: utf-8 -*-
# author: Ethosa

from ..utils import *
import re

class Hentasis:
    def __init__(self):
        self.url = "http://hentasis.top/"
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
            'Accept-Encoding':'gzip, deflate',
            'Connection':'keep-alive',
            'DNT':'1'
        }

    def getPage(self, pageNum=1):
        response = HMainPage(self.session.get("%spage/1/" % self.url), self.session)
        return response

    def getRandom(self):
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
            current = {}
            current["name"] = h.split("short-link nowrap", 1)[1].split(">", 1)[1].split("<", 1)[0].replace("&#039;", "'")
            current["url"] = h.split("short-link nowrap", 1)[1].split('href="', 1)[1].split('"', 1)[0].replace("&#039;", "'")
            current["image"] = "%s%s" % ("http://hentasis.top", h.split('class="short-img">', 1)[1].split('src="', 1)[1].split('"', 1)[0].replace("&#039;", "'"))
            current["year"] = h.split('<div class="mov-label"><b>Год выпуска:</b></div>', 1)[1].split("<", 1)[0].strip().replace("&#039;", "'")
            current["genre"] = h.split('class="mov-label"><b>Жанр:</b></div>', 1)[1].split("<", 1)[0].strip().replace("&#039;", "'")
            current["episodes"] = h.split('<div class="mov-label"><b>Эпизоды:</b></div>', 1)[1].split('<', 1)[0].strip().replace("&#039;", "'")
            current["time"] = h.split('class="mov-label"><b>Продолжительность:</b></div>', 1)[1].split('<', 1)[0].strip().replace("&#039;", "'")
            current["censored"] = h.split('<div class="mov-label"><b>Цензура:</b></div>', 1)[1].split('<', 1)[0].strip().replace("&#039;", "'")
            current["rusVoice"] = h.split('<div class="mov-label"><b>Русская озвучка:</b></div>', 1)[1].split('<', 1)[0].strip().replace("&#039;", "'")
            current["rusSub"] = h.split('<div class="mov-label"><b>Русские субтитры:</b></div>', 1)[1].split('<', 1)[0].strip().replace("&#039;", "'")
            try:
                current["produser"] = h.split('<div class="mov-label"><b>Режиссер:</b></div>', 1)[1].split('<', 1)[0].strip().replace("&#039;", "'")
            except:
                current["produser"] = ""
            current["studio"] = h.split('div class="mov-label"><b>Студия:</b></div>', 1)[1].split('<', 1)[0].strip().replace("&#039;", "'")
            current["studio"] = h.split('div class="mov-label"><b>Студия:</b></div>', 1)[1].split('<', 1)[0].strip().replace("&#039;", "'")
            current["description"] = h.split('Описание:<br /></b></div>', 1)[1].split('</li>', 1)[0].replace("&#039;", "'")
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
        self.videos = re.findall("http://.+mp4", self.page)
        self.dict = h

