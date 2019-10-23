# -*- coding: utf-8 -*-
# author: ethosa
from ..utils import *
from copy import copy

class ThisPerson:
    def __init__(self, *args, **kwargs):
        self.person = "https://thispersondoesnotexist.com/image"
        self.waifu = "https://www.thiswaifudoesnotexist.net/example-"
        self.cat = "https://thiscatdoesnotexist.com/"
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'
        }
        self.contents = []
        self.getRandomPersonA = lambda: Thread_VK(self.getRandomPerson).start()
        self.getRandomWaifuA = lambda: Thread_VK(self.getRandomWaifu).start()
        self.getBestRandomWaifuA = lambda: Thread_VK(self.getBestRandomWaifu).start()
        self.getRandomCatA = lambda: Thread_VK(self.getRandomCat).start()
        self.onReceivingA = lambda func: Thread_VK(self.onReceiving, func).start()

    def getRandomPerson(self):
        response = self.session.get(self.person).content
        self.contents.append(response)
        return response

    def getRandomWaifu(self):
        response = self.session.get("%s%s.jpg" % (self.waifu, random.randint(1, 200_000))).content
        self.contents.append(response)
        return response

    def getBestRandomWaifu(self):
        response = self.session.get("%s%s.jpg" % (self.waifu, random.randint(100_000, 200_000))).content
        self.contents.append(response)
        return response

    def getRandomCat(self):
        response = self.session.get(self.cat).content
        self.contents.append(response)
        return response

    def writeFile(self, path, content):
        with open(path, "wb") as f:
            f.write(content)

    def onReceiving(self, func):
        def asd():
            while 1:
                if self.contents:
                    current = copy(self.contents[0])
                    self.contents.pop(0)
                    func(current)
        Thread_VK(asd).start()
