from .utils import *

class ThisPerson:
    def __init__(self, *args, **kwargs):
        self.person = "https://thispersondoesnotexist.com/image"
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'
        }

    def getRandomPerson(self):
        response = self.session.get(self.person).content
        return response

    def writeFile(self, path, content):
        with open(path, "wb") as f:
            f.write(content)
