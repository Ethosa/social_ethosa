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
