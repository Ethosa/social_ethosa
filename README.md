# social ethosa
A Python library that uses requests

## Get started
Installation: `pip install --upgrade social-ethosa`  
Import:
```python
from social_ethosa import *
```

### Vkcom
```python
vk = Vk(token="Your token is here", group_id=12345, debug=True, lang="en")
# the group_id parameter should be used if you are going to log in through a group.
# In this example, we will use group authorization.

@vk.on_message_new
# This decorator is an event handler that executes the function passed to it on a new message
# The decorator's name is taken from the official names, but with the prefix " on_"
# https://vk.com/dev/groups_events
def getMessage(message):
  text = message.text
  peer_id = message.peer_id
  from_id = message.from_id
  attachments = message.attachments
```

using the file Uploader:
```python
vk.uploader.getUploadUrl("message_photo") # getting a link to upload files
# you can also pass other arguments (argument=value)
# to get the rest of the UploadUrl names, use the function
# uploader.getAllTypes
```
upload files:
```python
response = vk.uploader.uploadFile("path") # you can also pass other arguments (argument=value)
```

Some audio methods are also available in my library:
```python
login = "89007003535"
password = "qwertyuiop"

audio = Audio(login=login, password=password, debug=1)
audios = audio.get()
# Since the audio methods are not available in the official API, I had to make a parser of the site
```
### Yandex api
Using Yandex api:
```python
TOKEN = "translate token"
yt = YTranslator(token=TOKEN)
text = "Пайтон - хороший язык программирования"
response = yt.translate(text=text, lang="en") # Text translation
print(response)
```
### Trace moe
Using the [TraceMoe api](https://trace):
```python
tracemoe = TraceMoe() # initialization for future use
# In directory with script there is screenshot from anime " a. png"
response = tracemoe.search("a.png", False, 1)
# param 1 - path to image or image url
# param 2 - True, if param 1 is link
# param 3 - filter search
```
![Image did not load](https://i.pinimg.com/originals/33/55/37/335537e3904b0a3b204364907b22622f.jpg)

If the anime is found, you should get a video preview of the found moment:
```python
video = tracemoe.getVideo(response, mute=0) # The mute parameter must be 1 if you want to get video without sound
tracemoe.writeFile("file.mp4", video)
# param 1 is a path to write file
# param 2 is a video received by the get Video method
```

### BotWrapper
In the library there is a wrapper for bots!  
Initialization:
```python
bw = BotWrapper()
```
Getting a random date
```python
date = bw.randomDate(fromYear="2001", toYear="3001")
# Returned: string
# The fromYear and toYear parameters are optional
```

### BetterBotBase
This class uses pickle to maintain the database.  
Let's initialize this class.
```python
bbs = BetterBotBase("users folder", "dat")
# The first argument is the name of the folder where users will be stored
# the second argument is the Postfix of the files, in our case the files will look like this:
# 123123123.dat
```
