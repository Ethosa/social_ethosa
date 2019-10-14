# -*- coding: utf-8 -*-
# author: ethosa
from .utils import *
from .net.vkcom import Thread_VK
import time

class UtilsManager:
    def __init__(self, vk):
        self.vk = vk # vk parameter must be user

    def getLastPost(self, owner_id=None, domain=None):
        if owner_id:
            wall = self.vk.wall.get(owner_id=owner_id, count=2)["response"]
        elif domain:
            wall = self.vk.wall.get(domain=domain, count=2)["response"]
        post = {}

        if wall["count"] > 1:
            wall = wall["items"]
            if "is_pinned" not in wall[0]:
                post = wall[0]
            else:
                post = wall[1]
        elif wall["count"] > 0:
            post = wall["items"][0]

        return post

    def autoStatus(self, timer=300, text=["Hello vk api"], group_id=None, onChange=None):
        # timer must contain the number of seconds after which the status changes
        # text must contain a string or a list of strings
        # group_id - arbitrarily
        
        def start():
            returned = True
            if type(text) == str:
                while returned:
                    if group_id:
                        self.vk.status.set(text=text, group_id=group_id)
                    else:
                        self.vk.status.set(text=text)
                    if onChange:
                        returned = onChange()
                    time.sleep(timer)
            elif type(text) == list or type(text) == tuple:
                while returned:
                    if group_id:
                        self.vk.status.set(text=random.choice(text), group_id=group_id)
                    else:
                        self.vk.status.set(text=random.choice(text))
                    if onChange:
                        returned = onChange()
                    time.sleep(timer)

        Thread_VK(start).start()
