# -*- coding: utf-8 -*-
# author: Ethosa
# Import what we need
from social_ethosa import Vk

# Declare constant variables
TOKEN = ""

# we authorize through the user
vk = Vk(token=TOKEN)

# Start listening for new messages in a separate thread
@vk.on_user_message_new
def get_new_message(msg):
    # Output the received message
    print(msg)
