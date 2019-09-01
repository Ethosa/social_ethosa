# social_ethosa
The social ethosa library using Python.

Get vk access token here:
https://vkhost.github.io/ (choose the Kate mobile.)

install:
`
pip install social-ethosa --upgrade`

usage:
```python
from social_ethosa.vkcom import *

token = 'Your token here'

vk = Vk(token=token) # if you want auth to user
vk = Vk(token=Group_Access_Token, group_id='id your group') # if you want auth to group

@vk.on_message_new # handler new messages
def get_message(obj):
  peer_id = obj.peer_id
  message = obj.text
  vk.messages.send(message='hello vkcom!', peer_id=peer_id, random_id=0)

@vk.on_error # errors handler
def get_error(error):
  print(error.msg) # Example: No module named 'aa'
  print(error.line) # Example: 1
  print(error.code) # Example: ModuleNotFoundError
  
```

need help? no problem!
```python
print(vk.help())
print()
print(vk.help('messages'))
print()
print(vk.help('messages.send'))
```

You can also use Smile to get smiley codes!
```python
print(Smile('Улыбка'))
print(Smile('Красная книга'))
print(Smile().smiles) # it return ALL SMILEY CODES!
```


Example audio message:
```python
from social_ethosa.vkcom import *

token = 'token group'

vk = Vk(token=token, debug=True, lang='ru', group_id='185684225')

@vk.on_message_new
def lol(obj):
    if obj.text == '/lol':
        response = vk.upload_audio_message(peer_id=obj.peer_id, file='mil_tokyo1.ogg')
        audio = f'doc{response["audio_message"]["owner_id"]}_{response["audio_message"]["id"]}'
        print(audio)
        vk.messages.send(attachment=audio, message='ban :|', random_id=random.randint(0, 100), peer_id=obj.peer_id)
```

working with audio:
```python
from social_ethosa.vkcom import *

login = '71234567890'
password = 'hi_i_passowrd'

audio = VkAudio(login=login, password=password, debug=True, lang='ru')

print(audio.get()) # return your audios
print(audio.get(123)) # return audios of user with id 123
print(audio.getCount()) # return count of your audios
print(audio.getCount(123)) # return count audios of user with id 123
```
