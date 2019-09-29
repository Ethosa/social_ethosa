# social_ethosa
The social ethosa library using Python.

You can get a token from the user [here](https://vkhost.github.io/) (Choose Kate Mobile.)

Installation: `pip install social-ethosa --upgrade`

Use:
```python
from social_ethosa import *

token = 'Your token here'

vk = Vk(token=Group_Access_Token, group_id='id your group') # if you want auth to group

@vk.on_message_new # handler new messages
def get_message(obj):
  peer_id = obj.peer_id
  message = obj.text
  vk.messages.send(message='hello vkcom!', peer_id=peer_id, random_id=0)

@vk.on_error # errors handler
def get_error(error):
  print(error.message) # Example: No module named 'aa'
  print(error.line) # Example: 1
  print(error.code) # Example: ModuleNotFoundError
```

Need help? No problem!
```python
print(vk.help())
print()
print(vk.help('messages'))
print()
print(vk.help('messages.send'))
```

Example of loading audio messages:
```python
from social_ethosa.vkcom import *

token = 'user token here'

vk = Vk(token=token, debug=True, lang='ru')

file = 'mil_tokyo1.ogg'
vk.uploader.getUploadUrl('audio_message', peer_id=1234567890)
response = vk.uploader.uploadFile(file=file)

audio_message = f'doc{response["audio_message"]["owner_id"]}_{response["audio_message"]["id"]}'

vk.messages.send(peer_id=1234567890, message='test uploader', attachment=audio_message, random_id=random.randint(0, 1000))
```

Example of uploading photos to messages:
```python
from social_ethosa.vkcom import *

token = 'user token here'

vk = Vk(token=token, debug=True, lang='ru')

file = 'b.png'
vk.uploader.getUploadUrl('message_photo')
response = vk.uploader.uploadFile(file=file)

photo = f'photo{response["owner_id"]}_{response["id"]}'

vk.messages.send(peer_id=1234567890, message='test uploader', attachment=photo, random_id=random.randint(0, 1000))
```

Working with audio methods:
```python
from social_ethosa.vkcom import *

login = '71234567890'
password = 'hi_i_passowrd'

audio = Audio(login=login, password=password, debug=True, lang='ru')

print(audio.get()) # return your audios
print(audio.get(123)) # return audios of user with id 123
print(audio.getCount()) # return count of your audios
print(audio.getCount(123)) # return count audios of user with id 123
pprint(audio.getById(owner_id=-148928912, audio_id=456239018)) # return audio-148928912_456239018
pprint(audio.search('minecraft')) # return dictionary with audios list, playlists list, artists list
```

Help using utils:
```python
@autoRun # this decorator automatically starts the next callee
def hello():
  print("Hello world!")

listObject = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(splitList(listObject, 2)) # the splitList function attempts to split the list into equal parts
```
