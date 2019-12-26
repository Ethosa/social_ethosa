# -*- coding: utf-8 -*-
# author: Ethosa
# Import what we need
from social_ethosa import Vk

# Declare constant variables
TOKEN = ""

# we authorize through the user
vk = Vk(token=TOKEN)

class Main:
    def __init__(self):
        # Start listening for new messages in a separate thread
        vk.on_user_message_new(self.get_new_message)

    def get_new_message(self, msg):
        # Output the received message
        print(msg)

if __name__ == "__main__":
    main = Main()
