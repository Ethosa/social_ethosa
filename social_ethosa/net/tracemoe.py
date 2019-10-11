# -*- coding: utf-8 -*-
# author: ethosa
from ..utils import *

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

    def search(self, path, url1=0, filterSearch=1):
        url = "%s%s" % (self.api, "search")
        if url1:
            return self.session.get(f'{self.api}search', params={'url': path}).json()
        else:
            with open(path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            data = {"filter" : filterSearch, "image" : encoded_string}
        return self.session.post(url, json=data).json()

    def getMe(self):
        url = "%s%s" % (self.api, "me")
        return self.session.post(url).json()

    def getVideo(self, response, mute=0):
        if "docs" in response:
            response = response["docs"][0]
        anilist_id = response["anilist_id"]
        filename = response["filename"]
        at = response["at"]
        tokenthumb = response["tokenthumb"]
        url = "%s%s/%s/%s?t=%s&token=%s%s" % (self.media, "video", anilist_id,
                    filename, at, tokenthumb, "&mute" if mute else "")
        return self.session.get(url).content

    def getImagePreview(self, response):
        if "docs" in response:
            response = response["docs"][0]
        anilist_id = response["anilist_id"]
        filename = response["filename"]
        at = response["at"]
        tokenthumb = response["tokenthumb"]
        url = "%s%s?anilist_id=%s&file=%s&t=%s&token=%s" % (self.trace, "thumbnail.php",
                            anilist_id, filename, at, tokenthumb)
        return self.session.get(url).content

    def writeFile(self, path, content):
        with open(path, "wb") as f:
            f.write(content)
