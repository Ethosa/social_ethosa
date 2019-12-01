# -*- coding: utf-8 -*-
# author: Ethosa

from ..utils import browserFake
import requests
import sys
import re


class VKAuth:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.session = requests.Session()
        self.session.headers = browserFake
        self.authPage = ""

    def logIn(self):
        url = "https://vk.com"
        data = self.session.get(url).text
        start = re.search("<form.+name=\"login.+", data).start()
        end = re.search("<input type=\"submit\" class=\"submit\" />", data).start()
        data = data[start:end]
        lg_h = re.findall("<input.+lg_h.+", data)[0]
        lg_h = lg_h.split("value=\"", 1)[1].split("\"", 1)[0].strip()
        ip_h = re.findall("<input.+ip_h.+", data)[0]
        ip_h = ip_h.split("value=\"", 1)[1].split("\"", 1)[0].strip()
        form = {'act' : 'login', 'role' : 'al_frame', 'expire' : '',
                'recaptcha' : '', 'captcha_sid' : '', 'captcha_key' : '',
                '_origin': 'https://vk.com', 'ip_h': ip_h,
                'lg_h': lg_h, 'ul': '',
                'email': self.login, 'pass': self.password}
        response = self.session.post("https://login.vk.com/", data=form)
        if 'onLoginDone' in response.text:
            sys.stdout.write("auth completed.\n")
            self.authPage = response.text
        else:
            sys.stdout.write("auth error.\n")
        return response

    def getToken(self):
        url1 = ("https://oauth.vk.com/authorize?client_id=2685278"
                "&scope=1073737727&redirect_uri=https://oauth.vk."
                "com/blank.html&display=page&response_type=token")
        text = self.session.get(url1).text
        location = re.findall(r'location.href = "(\S+)"\+addr;', text)
        if location:
            token = re.findall(r"token=([^&]+)", self.session.get(location[0]).url)
            token = token[0]
        else:
            token = ""
        return token
        
