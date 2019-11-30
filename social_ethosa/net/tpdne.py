# -*- coding: utf-8 -*-
# author: ethosa
from ..utils import Thread_VK, requests
from copy import copy

class ThisPerson:
    def __init__(self):
        self.person = "https://thispersondoesnotexist.com/image"
        self.waifu = "https://www.thiswaifudoesnotexist.net/example-"
        self.cat = "https://thiscatdoesnotexist.com/"
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'
        }
        self.contents = []

    def getRandomPerson(self):
        """get random human image
        
        Returns:
            bytes -- content for write in file.
        """
        response = self.session.get(self.person).content
        self.contents.append(response)
        return response

    def getRandomWaifu(self):
        """get random anime image
        
        Returns:
            bytes -- content for write in file.
        """
        response = self.session.get("%s%s.jpg" % (self.waifu, random.randint(1, 200_000))).content
        self.contents.append(response)
        return response

    def getBestRandomWaifu(self):
        """get random anime image with better quality
        
        Returns:
            bytes -- content for write in file.
        """
        response = self.session.get("%s%s.jpg" % (self.waifu, random.randint(100_000, 200_000))).content
        self.contents.append(response)
        return response

    def getRandomCat(self):
        """get random cat image
        
        Returns:
            bytes -- content for write in file.
        """
        response = self.session.get(self.cat).content
        self.contents.append(response)
        return response

    def writeFile(self, path, content):
        """write getted bytes to file
        
        Arguments:
            path {str} -- path to image (the image may not exist)
            content {bytes} -- bytes for write in file
        """
        with open(path, "wb") as f:
            f.write(content)

    def onReceiving(self, func):
        """run new images listener
        
        Arguments:
            func {method, function or class} -- the object to be called
        """
        def asd():
            while 1:
                if self.contents:
                    current = copy(self.contents[0])
                    self.contents.pop()
                    func(current)
        Thread_VK(asd).start()
