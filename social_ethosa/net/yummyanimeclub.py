# -*- coding: utf-8 -*-
# author: ethosa
from ..utils import *

class YummyAnime:
    # The main class to interact with yummyanime.club
    def __init__(self, **kwargs):
        self.login = getValue(kwargs, "login", "")
        self.password = getValue(kwargs, "password", "")
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
            'Accept-Encoding':'gzip, deflate',
            'Connection':'keep-alive',
            'DNT':'1'
        }
        self.mainPageUrl = "https://yummyanime.club/"
        self.updatesPage = "https://yummyanime.club/anime-updates"
        self.loginUrl = "https://yummyanime.club/login"
        self.searchByNameUrl = "http://yummyanime.club/search"
        self.randomAnime = "http://yummyanime.club/random"
        self.profilePageUrl = "https://yummyanime.club/profile"
        self.updateProfileImage = "https://yummyanime.club/profile/update"
        self.logged = 0
        self.userName = ""

        if self.login and self.password:
            self.logIn(self.login, self.password)

    def logIn(self, login, password):
        self.mainPage = self.session.post(self.loginUrl, data={"email" : login, "password" : password}).text
        if '<li title="Мой профиль">' in self.mainPage:
            self.userName = self.mainPage.split('<span id="login" class="user-name-text">', 1)[1].split("</span>", 1)[0].strip()
            self.logged = 1
            sys.stdout.write("Login sucessfull.\n")
        else:
            sys.stdout.write("Login error.\n")

    def isLogin(self): return self.logged

    def logOut(self):
        if self.isLogin():
            self.mainPage = self.session.post("%slogout" % self.mainPageUrl).text
            self.logged = 0

    def getRandomAnime(self):
        return YummyPage(self.session.post(self.randomAnime))

    def getUpdates(self, page=1):
        return YummyUpdates(self.session.get(self.updatesPage, params={"page" : page}), self.session)

    def getProfile(self):
        if self.isLogin():
            return YummyProfile(self.session.get(self.profilePageUrl), self.session, self.userName)

    def onNewUpdate(self, timer=60):
        def asd1(func):
            self.lastUpdate = self.getUpdates()[0]
            def asd():
                while 1.0:
                    lastUpdate = self.getUpdates()[0]
                    if self.lastUpdate != lastUpdate:
                        self.lastUpdate = lastUpdate
                        func(self.lastUpdate)
                    time.sleep(timer)
            Thread_VK(asd).start()
        return func


class YummyPage:
    # Class for easy interaction with anime pages
    def __init__(self, page):
        self.url = page.url
        self.page = page.text
        self.content = page.text.split('<div class="content">', 1)[1].split("</div></div><script>", 1)[0]
        self.name = self.content.split("<h1>", 1)[1].split("</h1>", 1)[0].strip()
        try:
            self.rating = {
                "rating" : self.content.split('<span class="main-rating">', 1)[1].split("</span>", 1)[0].strip(),
                "voices" : self.content.split('<span class="main-rating-info">', 1)[1].split("</span>", 1)[0].strip()
            }
        except:
            self.rating = {
                "rating" : "Для этого аниме",
                "voices" : "рейтинг недоступен."
            }
        self.views = self.content.split('<span>Просмотров:</span>', 1)[1].split('<i', 1)[0].strip()
        try:
            self.status = self.content.split('<span class="badge review">', 1)[1].split('</span>', 1)[0].strip()
        except:
            self.status = ""
        try:
            self.year = self.content.split('<span>Год: </span>', 1)[1].split('</li>', 1)[0].strip()
        except:
            self.year = ""
        try:
            self.season = self.content.split('<span>Сезон:</span>', 1).split('</li>', 1)[0].strip()
        except:
            self.season = ""
        try:
            self.ageRating = self.content.split('<span>Возрастной рейтинг:</span>', 1)[1].split('</li>', 1)[0].strip()
        except:
            self.ageRating = ""
        try:
            genreList = self.content.split('<span class="genre">Жанр:</span>', 1)[1].split('<ul class="categories-list">', 1)[1].split("</ul>", 1)[0].split('href="')
            genreList.pop(0)
            self.genreList = [{
            "url" : "https://yummyanime.club%s" % i.split('"', 1)[0],
            "name" : i.split('>', 1)[1].split('<', 1)[0].strip()
            } for i in genreList]
        except:
            self.genreList = ""
        try:
            self.original = self.content.split('<span>Первоисточник:</span>', 1)[1].split('</li>', 1)[0].strip()
        except:
            self.original = ""
        try:
            genreList = self.content.split('<span class="genre">Студия:</span>', 1)[1].split('<ul class="categories-list">', 1)[1].split("</ul>", 1)[0].split('href="')
            genreList.pop(0)
            self.studioList = [{
                "url" : "https://yummyanime.club%s" % i.split('"', 1)[0],
                "name" : i.split('>', 1)[1].split('<', 1)[0].strip()
            } for i in genreList]
        except:
            self.studioList = [{"name" : ""}]
        try:
            producer = self.content.split('<span>Режиссер:</span>', 1)[1].split('</a>', 1)[0]
            self.producer = {
                "name" : producer.split('>', 1)[1].strip(),
                "url" : "https://yummyanime.club%s" % producer.split('href="', 1)[1].split('"', 1)[0]
            }
        except:
            self.producer = {"name" : ""}
        try:
            self.type = self.content.split("<span>Тип:</span>", 1)[1].split('</li>', 1)[0].strip()
        except:
            self.type = ""
        try:
            self.series = self.content.split("<span>Серии:</span>", 1)[1].split('</li>')[0].strip()
        except:
            self.series = ""
        try:
            self.translate = self.content.split('<span>Перевод:</span>', 1)[1].split('</li>', 1)[0].strip()
        except:
            self.translate = ""
        try:
            self.voiceActing = self.content.split('<span>Озвучка:</span>', 1)[1].split('</li>            </ul>\n\n            <div ', 1)[0].strip().replace("&amp;", "&")
            if '<a class="studio-name">' in self.voiceActing:
                self.voiceActing = self.voiceActing.split('dropdown">')
                self.voiceActing.pop(0)
                self.voiceActing = [{
                    "name" : i.split('<a class="studio-name">', 1)[1].split('</a>', 1)[0].strip(),
                    "vocalized" : [name.split('</li>', 1)[0].strip()
                                    for name in i.split('<ul class="dub-content">', 1)[0].split('</ul>')[0].split('<li class="list">')]
                } for i in self.voiceActing]
        except:
            self.voiceActing = []
        try:
            self.description = self.content.split('<div id="content-desc-text"><p>', 1)[1].split('</p>', 1)[0].strip()
            self.description = self.description.replace('<br />', '').replace("&nbsp;", "").replace("&mdash;", "—").replace("&quot;", '"').replace("&hellip;", "...").replace("&ndash;", "—").replace("&laquo;", "«").replace("&raquo;", "»")
            while "<" in self.description and ">" in self.description:
                start = self.description.find("<")
                end = self.description.find(">")
                self.description = self.description[:start] + self.description[end+1:]
        except:
            self.description = ""
        try:
            self.posterImageUrl = self.content.split('<div class="poster-block">', 1)[1].split('src="', 1)[1].split('"', 1)[0].strip()
            self.posterImageUrl = "https://yummyanime.club%s" % self.posterImageUrl
        except:
            self.posterImageUrl = ""

    def __str__(self):
        return """%s (%s) 
Рейтинг: [%s %s]
Просмотры: %s
Сезон: %s
Жанр: %s
Режиссер: %s
Студия: %s
Тип: %s
Перевод: %s
Серии: %s
Первоисточник: %s
Возрастной рейтинг: %s
Ссылка на аниме: %s
Озвучили: %s
------------------
%s""" % (self.name, self.year,
        self.rating["rating"], self.rating["voices"], self.views, self.season,
        ", ".join(i["name"] for i in self.genreList),
        self.producer["name"], ", ".join(i["name"] for i in self.studioList),
        self.type, self.translate, self.series, self.original, self.ageRating,
        self.url, self.voiceActing if type(self.voiceActing) == str else
            ", ".join(i["name"] for i in self.voiceActing),
        self.description)


class YummyUpdates:
    def __init__(self, updatePage, session):
        self.page = updatePage.text
        self.content = self.page.split('<div class="content-page">', 1)[1]
        self.updateList = self.content.split('<ul class="update-list">', 1)[1].split('</ul>', 1)[0].split('<li>')
        self.updateList = [YummyUpdate(i, session) for i in self.updateList if '<span class="update-title">' in i]

    def __getitem__(self, num):
        return self.updateList[num]

    def __str__(self):
        return "\n".join(str(i) for i in self.updateList)


class YummyUpdate:
    def __init__(self, updateText, session):
        self.name = updateText.split('<span class="update-title">', 1)[1].split('</span>', 1)[0].strip()
        self.whatSerie = updateText.split('<span class="update-info">', 1)[1].split('</span>', 1)[0].strip()
        self.posterImage = "https://yummyanime.club%s" % updateText.split('img src="', 1)[1].split('"', 1)[0].strip()
        self.url = "https://yummyanime.club%s" % updateText.split('a href="', 1)[1].split('"', 1)[0].strip()
        self.date = updateText.split('<span class="update-date">', 1)[1].split('</span>', 1)[0].strip()
        self.session = session

    def open(self):
        return YummyPage(self.session.get(self.url))

    def __str__(self):
        return """%s (%s) - %s""" % (self.name, self.date, self.whatSerie)


class YummyProfile:
    def __init__(self, page, session, name):
        self.page = page.text
        self.session = session
        self.name = name
        self.penaltyPoints = self.page.split('<strong>Штрафные баллы:</strong>', 1)[1].split('<span', 1)[0].strip()
        self.registerDate = self.page.split('<strong>Дата регистрации:</strong>', 1)[1].split('</p>', 1)[0].strip()
        self.group = self.page.split('<strong>Группа:</strong>', 1)[1].split('</p>', 1)[0].strip()
        self.profileUrl = "https://yummyanime.club/users/id%s" % self.page.split('Ссылка на этот профиль', 1)[0].split('/users/id', 1)[1].split('"', 1)[0].strip()

    def __str__(self):
        return """%s.
Штрафные баллы - %s
Дата регистрации - %s
Группа - %s
Ссылка на профиль - %s""" % (self.name, self.penaltyPoints, self.registerDate, self.group, self.profileUrl)
