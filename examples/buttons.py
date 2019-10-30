# -*- coding: utf-8 -*-
# author: Ethosa
# we import the functionality we need
from social_ethosa import Button, printf

# let's create a simple text type button
text_button = Button(type="text", label="Hello world", color=Button.POSITIVE)
# the color can be one of the following four:
# Button.PRIMARY
# Button.SECONDARY
# Button.NEGATIVE
# Button.POSITIVE
# default button color - Button.PRIMARY

# Let's create a button and parse it
standart_button = Button()
# We created a button with the following parameters
# {'action': {
#     'type': 'text',
#     'label': 'бан',
#     'payload': ''
#  },
#  'color': 'primary'
# }

# Now let's create 3 special buttons
location_button = Button(type="location", payload="")
vkpay_button = Button(type="vkpay", hash="action=transfer-to-group&group_id=1&aid=10")
vkapps_button = Button(type="vkapps", label="open app", app_id=1, owner_id=1, hash="hello world")
# it is worth noting that the special buttons do not have a color parameter