# -*- coding: utf-8 -*-
# author: ethosa

from ..utils import *

class Pastebin:
    def __init__(self, token=""):
        """auth in pastebin
        
        Arguments:
            token {[str]} -- api key
        """
        self.token = token
        self.session = requests.Session()

    def createNewPaste(self, text="", private=1, name="text.txt",
                        expire="10M", form=""):
        """create new paste on pastebin.com
        
        Keyword Arguments:
            text {str} -- [paste text] (default: {""})
            private {number} -- [paste private. can be 0, 1 or 2] (default: {1})
            name {str} -- [name of paste] (default: {"text.txt"})
            expire {str} -- [expire date] (default: {"10M"})
            form {str} -- [format file] (default: {""})
        
        Returns:
            [str] -- [created paste url or error]
        """
        data = {
            "api_dev_key" : self.token,
            "api_paste_code" : text,
            "api_paste_private" : private,
            "api_paste_name" : name,
            "api_paste_expire_date" : expire,
            "api_paste_format" : form,
            "api_option" : "paste"
        }
        response = self.session.post("https://pastebin.com/api/api_post.php", 
                    data=data).text
        return response
