# -*- coding: utf-8 -*-
# author: ethosa
from ..utils import *

class YandexRoot:
    # Yandex Root-the main class in order to reduce the code of obtaining a token when initializing the class.
    def __init__(self, *args, **kwargs):
        self.token = getValue(kwargs, "token")
        self.session = requests.Session()

class YTranslator(YandexRoot):
    # YTranslator - class to use Yandex Translate
    # We recommend that you read its documentation before using this class
    # Used to translate text
    def __init__(self, *args, **kwargs):
        super(YTranslator, self).__init__(*args, **kwargs)
        self.detectUrl = "https://translate.yandex.net/api/v1.5/tr.json/detect"
        self.getLangsUrl = "https://translate.yandex.net/api/v1.5/tr.json/getLangs"
        self.translateUrl = "https://translate.yandex.net/api/v1.5/tr.json/translate"

    def detect(self, text, **kwargs):
        kwargs["key"] = self.token
        kwargs["text"] = text
        response = self.session.post(self.detectUrl, data=kwargs).json()
        return response

    def getLangs(self, ui, **kwargs):
        kwargs["key"] = self.token
        kwargs["ui"] = ui
        response = self.session.post(self.getLangsUrl, data=kwargs).json()
        return response

    def translate(self, text, lang, **kwargs):
        kwargs["key"] = self.token
        kwargs["lang"] = lang
        kwargs["text"] = text
        print(kwargs)
        response = self.session.post(self.translateUrl, data=kwargs).json()
        return response


class YDictionary(YandexRoot):
    # YDictionary-class to use Yandex Dictionary
    # We recommend that you read its documentation before using this class
    def __init__(self, *args, **kwargs):
        super(YDictionary, self).__init__(*args, **kwargs)
        self.getLangsUrl = "https://dictionary.yandex.net/api/v1/dicservice.json/getLangs"
        self.lookupUrl = "https://dictionary.yandex.net/api/v1/dicservice.json/lookup"

    def getLangs(self):
        data = {"key" : self.token}
        return self.session.post(self.getLangsUrl, data=data).json()

    def lookup(self, lang, text, **kwargs):
        kwargs["key"] = self.token
        kwargs["text"] = text
        kwargs["lang"] = lang
        return self.session.post(self.lookupUrl, data=kwargs).json()


class YPredictor(YandexRoot):
    # YPredictor-class to use Yandex Predictor
    # We recommend that you read its documentation before using this class
    def __init__(self, *args, **kwargs):
        super(YPredictor, self).__init__(*args, **kwargs)
        self.getLangsUrl = "https://predictor.yandex.net/api/v1/predict.json/getLangs"
        self.completeUrl = "https://predictor.yandex.net/api/v1/predict.json/complete"

    def getLangs(self, **kwargs):
        kwargs["key"] = self.token
        return self.session.post(self.getLangsUrl, data=data).json()

    def complete(self, lang, q, **kwargs):
        kwargs["key"] = self.token
        kwargs["q"] = q
        kwargs["lang"] = lang
        return self.session.post(self.completeUrl, data=kwargs).json()


class YSpeller(YandexRoot):
    # YSpeller-class to use Yandex Speller
    # We recommend that you read its documentation before using this class
    def __init__(self, *args, **kwargs):
        super(YSpeller, self).__init__(*args, **kwargs)
        self.checkTextUrl = "https://speller.yandex.net/services/spellservice.json/checkText"
        self.checkTextsUrl = "https://speller.yandex.net/services/spellservice.json/checkTexts"

    def checkText(self, text, **kwargs):
        kwargs["text"] = text
        return self.session.post(self.checkTextUrl, data=kwargs).json()

    def checkTexts(self, text, **kwargs):
        kwargs["text"] = text
        return self.session.post(self.checkTextsUrl, data=kwargs).json()


class YImagesSearch:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
            'Accept-Encoding':'gzip, deflate',
            'Connection':'keep-alive',
            'DNT':'1'
        }
        self.url = "https://yandex.ru/images/search"

    def search(self, q):
        data = {
            "text" : q,
            "from" : "tabbar"
        }
        response = self.session.post(self.url, params=data).text.split('<h1 class="a11y-hidden">Результаты поиска</h1>', 1)[1].split('<div class="serp-item serp-item_type_search')
        out = []
        for r in response:
            if "<img class=\"serp-item__thumb justifier__thumb\" src=\"" in r:
                r = r.split("<img class=\"serp-item__thumb justifier__thumb\" src=\"", 1)[1].split('"', 1)[0]
                if r.startswith("//"):
                    r = "http:%s" % r
                out.append(r)
        return out

