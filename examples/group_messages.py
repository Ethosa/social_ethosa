# -*- coding: utf-8 -*-
# author: Ethosa
# Import what we need
from social_ethosa import Vk

# Declare constant variables
TOKEN = ""
GROUP_ID = 123123

# we authorize through the group
vk = Vk(token=TOKEN, group_id=GROUP_ID)

# Start listening for new messages in a separate thread
@vk.on_message_new
def get_new_message(msg):
    # Output the received message
    print(msg)
