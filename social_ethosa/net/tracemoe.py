# -*- coding: utf-8 -*-
# author: ethosa

from ..utils import Thread_VK, requests, base64
from copy import copy

class TraceMoe:
    """
    Tracemode-class for interaction with the trace.moe (site for search anime on the picture)
    its main method is search
    there are also methods:
    getMe
    getVideo
    getImagePreview
    search
    """
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            "Content-Type" : "application/json"
        }
        self.api = "https://trace.moe/api/"
        self.trace = "https://trace.moe/"
        self.media = "https://media.trace.moe/"
        self.contents = []

    def getImagePreview(self, response):
        """you can get previews of the matched scene.
        (not 100% accurate due to timecode and seeking method)
        
        Arguments:
            response {dict} -- found anime moment
        
        Returns:
            bytes -- image for write in file
        """
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

    def getMe(self):
        """Let you check the search quota and limit for your account (or IP address).
        
        Returns:
            dict -- limit info
        """
        response = self.session.post("%s%s" % (self.api, "me")).json()
        self.contents.append({"type" : "me", "response" : response})
        return response

    def getVideo(self, response, mute=0):
        """video preview
        
        Arguments:
            response {dict} -- found anime moment
        
        Keyword Arguments:
            mute {int} -- mute sound (default: {0})
        
        Returns:
            bytes -- video for write in file
        """
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

    def search(self, path, isLink=0, filterSearch=1):
        """find anime moment via anime screenshot
        
        Arguments:
            path {str} -- path to screenshot
        
        Keyword Arguments:
            isLink {number} -- using a link instead of a file path (default: {0})
            filterSearch {number} -- filter (default: {1})
        
        Returns:
            dict -- found anime moment
        """
        url = "%s%s" % (self.api, "search")
        if isLink:
            return self.session.get('%ssearch' % (self.api), params={'url': path}).json()
        else:
            with open(path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            data = {"filter" : filterSearch, "image" : encoded_string}
        response = self.session.post(url, json=data).json()
        self.contents.append({"type" : "search", "response" : response})
        return response

    def writeFile(self, path, content):
        """write getted bytes to file
        
        Arguments:
            path {str} -- path to image or video (the image or video may not exist)
            content {bytes} -- bytes for write in file
        """
        with open(path, "wb") as f:
            f.write(content)
