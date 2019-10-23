# -*- coding: utf-8 -*-
# author: ethosa

from ..utils import *
from copy import copy

class TraceMoe:
    """
    Tracemode-class for interaction with the trace site.mode (site for search anime on the picture)
    its main method is search
    there are also methods:
    getMe
    getVideo
    getImagePreview
    """
    def __init__(self, *args, **kwargs):
        self.session = requests.Session()
        self.session.headers = {
            "Content-Type" : "application/json"
        }
        self.api = "https://trace.moe/api/"
        self.trace = "https://trace.moe/"
        self.media = "https://media.trace.moe/"
        self.contents = []
        self.searchA = lambda path, url1=0, filterSearch=1: Thread_VK(self.search, path, url1, filterSearch).start()
        self.getMeA = lambda: Thread_VK(self.getMe).start()
        self.getVideoA = lambda response, mute=0: Thread_VK(self.getVideo, response, mute).start()
        self.getImagePreviewA = lambda response: Thread_VK(self.getImagePreview, response).start()

    def search(self, path, url1=0, filterSearch=1):
        url = "%s%s" % (self.api, "search")
        if url1:
            return self.session.get(f'{self.api}search', params={'url': path}).json()
        else:
            with open(path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            data = {"filter" : filterSearch, "image" : encoded_string}
        response = self.session.post(url, json=data).json()
        self.contents.append({"type" : "search", "response" : response})
        return response

    def getMe(self):
        url = "%s%s" % (self.api, "me")
        response = self.session.post(url).json()
        self.contents.append({"type" : "me", "response" : response})
        return response

    def getVideo(self, response, mute=0):
        if "docs" in response:
            response = response["docs"][0]
        anilist_id = response["anilist_id"]
        filename = response["filename"]
        at = response["at"]
        tokenthumb = response["tokenthumb"]
        url = "%s%s/%s/%s?t=%s&token=%s%s" % (self.media, "video", anilist_id,
                    filename, at, tokenthumb, "&mute" if mute else "")
        response = self.session.get(url).content
        self.contents.append({"type" : "video", "response" : response})
        return response

    def getImagePreview(self, response):
        if "docs" in response:
            response = response["docs"][0]
        anilist_id = response["anilist_id"]
        filename = response["filename"]
        at = response["at"]
        tokenthumb = response["tokenthumb"]
        url = "%s%s?anilist_id=%s&file=%s&t=%s&token=%s" % (self.trace, "thumbnail.php",
                            anilist_id, filename, at, tokenthumb)
        response = self.session.get(url).content
        self.contents.append({"type" : "image", "response" : response})
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
