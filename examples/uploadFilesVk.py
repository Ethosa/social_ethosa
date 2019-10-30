# -*- coding: utf-8 -*-
# author: Ethosa
# we import the functionality we need
from social_ethosa import Vk, printf

# Declare constant variables
TOKEN = ""
GROUP_ID = 123123

# we authorize through the group (or user)
vk = Vk(token=TOKEN, group_id=GROUP_ID, debug=1)

# get a link to upload files to the server
vk.uploader.getUploadUrl("message_photo", peer_id=123123)

# here are all types:
# album_photo
# wall_photo
# message_photo
# user_photo
# chat_photo
# market_photo
# market_album_photo
# audio
# audio_message
# doc_message
# video

# after receiving the download link we can upload the files to the server
photo = vk.uploader.uploadFile("a.png")
photo2 = vk.uploader.uploadFile("b.png")

# you can use the following method to format the received data:
photo = "photo%s_%s" % (photo["owner_id"], photo["id"])
photo2 = "photo%s_%s" % (photo2["owner_id"], photo2["id"])

# after that, you can use the received data, for example, in sending a message
vk.messages.send(message="test", attachment=[photo, photo2])