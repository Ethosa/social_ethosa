# -*- coding: utf-8 -*-
# author: Ethosa
# Import what we need
from social_ethosa import Vk, printf, autoRun

# Declare constant variables
TOKEN = ""

# we authorize through the user
vk = Vk(token=TOKEN, debug=1)

# Declare a class and run it immediately
@autoRun
class Main:
    def __init__(self):
        # Start listening for new messages in a separate thread
        vk.on_user_new_message(self.get_new_message)

    def get_new_message(self, msg):
        # Output the received message
        printf(msg)