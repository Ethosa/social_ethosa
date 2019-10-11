# -*- coding: utf-8 -*-
# author: ethosa
from ..utils import *

class ThisPerson:
    def __init__(self, *args, **kwargs):
        self.person = "https://thispersondoesnotexist.com/image"
        self.waifu = "https://www.thiswaifudoesnotexist.net/example-"
        self.cat = "https://thiscatdoesnotexist.com/"
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'
        }

    def getRandomPerson(self):
        return self.session.get(self.person).content

    def getRandomWaifu(self):
        return self.session.get("%s%s.jpg" % (self.waifu, random.randint(1, 200000))).content

    def getRandomCat(self):
        return self.session.get(self.cat).content

    def writeFile(self, path, content):
        with open(path, "wb") as f:
            f.write(content)
