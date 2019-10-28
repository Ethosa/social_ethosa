# -*- coding: utf-8 -*-
# author: Ethosa

from ..utils import *

class Telegram:
    def __init__(self, token="", proxy=""):
        self.url = "https://api.telegram.org/"
        self.token = token
        self.botUrl = "%sbot%s/" % (self.url, token)

        self.proxy = proxy
        self.session = requests.Session()
        self.session.headers = {
            "Content-Type" : "application/json"
        }
        self.session.proxies={self.proxy.split(":", 1)[0] : self.proxy}
        self.method = lambda method, **kwargs: TMethod(self).use(method, **kwargs)


class TMethod:
    def __init__(self, t, method=""):
        self.method = method
        self.session = t.session
        self.botUrl = t.botUrl
        self.token = t.token

    def use(self, method, **kwargs):
        response = self.session.post("%s%s" % (self.botUrl, method), data=kwargs)
        return response
