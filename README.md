# social ethosa
A Python library that uses requests

## Get started
Installation: `pip install --upgrade social-ethosa`  
Import:
```python
from social_ethosa import *
```

## Vkcom
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
## Yandex api
Using Yandex api:
```python
TOKEN = "translate token"
yt = YTranslator(token=TOKEN)
text = "Пайтон - хороший язык программирования"
response = yt.translate(text=text, lang="en") # Text translation
print(response)
```
## Trace moe
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

## BotWrapper
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

## BetterBotBase
This class uses pickle to maintain the database.  
Let's initialize this class.
```python
bbs = BetterBotBase("users folder", "dat")
# The first argument is the name of the folder where users will be stored
# the second argument is the Postfix of the files, in our case the files will look like this:
# 123123123.dat
```

BetterBotBase can also be used with Vkcom:
```python
@vk.on_message_new
def getNewMessage(message):
  from_id = message.from_id
  if from_id > 0:
    user = bbs.autoInstallUser(from_id, vk)
# autoInstallUser automatically creates or loads users and returns the user for further action with it.
```

BotWrapper can also be used to interact with BetterBotBase!
```python
text = bw.answerPattern("Hello, <name>, your money is <money>!", user)
# the answer Pattern method automatically substitutes variables from user,
# thus making it a little easier to format the string
```

You can define your own templates to the database!
```python
# right after BetterBotBase announcement
bbs.addPattern("countMessages", 0)
# the first argument is the variable name
# the second argument is the default value of the variable (when creating a user)
```

You created a template, but it was not added to the old users? not a problem!
```python
bbs.addNewVariable("countMessages", 0)
# this method works the same as addPattern, but with older users
```


## ThisPerson api
Initialization is quite simple
```python
person = ThisPerson()
```

In the class now only 3 methods to retrieve non-existent people/cats/waifu
```python
rperson = person.getRandomPerson()
rcat = person.getRandomCat()
rwaifu = person.getRandomWaifu()
```

after receiving the generated photo, it should be written to a file.
```python
person.writeFile("person.png", rperson)
person.writeFile("cat.png", rcat)
person.writeFile("waifu.png", rwaifu)
```

## Yummyanime club
There are few methods here, as I have not found an official API. Let's get started.
```python
ym = YummyAnime()
ym = YummyAnime(login="yourmail@gmail.com", password="iampassword")
# You can log in to your account if you need to
```
Getting random anime
```python
randomAnime = ym.getRandomAnime()
print(dir(randomAnime))
print(randomAnime())
```
You can also get a list of anime updates
```python
updates = ym.getUpdates()
anime = updates[0].open() # You will get the same object that the getRandomAnime() method returns
print(updates)
print(anime)
```
And also you can view your profile
```python
profile = ym.getProfile()
print(profile)
```

## eMath
I decided that very few people will need this module, so importing it separately from the main one:
```python
from social_ethosa.eMath import *
```
### Point
You can create an N-dimensional point:
```python
point = Point(0, 0, 0)
point1 = Point(4, 2, 3)
```
And also you can find the Euclidean distance between them:
```python
distance = point.euclideanDistance(point1)
print(distance)
```
### Matrix
Also this module has a Matrix class
```python
matrix = Matrix(3, 3) # Creating a 3x3 matrix
matrix1 = Matrix([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]]) # Creating a 3x3 matrix
```
You can transpose the matrix
```python
matrix1.transpose()
# 1 4 7
# 2 5 8
# 3 6 9
```
And multiply the matrix by the number
```python
matrix1 *= 3
# 3 12 21
# 6 15 24
# 9 18 27
```
The addition of two matrices is also possible
```python
matrix2 = Matrix([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])
matrix1 += matrix2
# 4 14 24
# 10 20 30
# 16 26 36
```
Matrix multiplication? No problem!
```python
matrix = Matrix([[1, 2, 3],
                [4, 5, 6]])
matrix1 = Matrix([[1, 2],
                [3, 4],
                [5, 6]])
matrix *= matrix1
# 22, 28 
# 49, 64

matrix = Matrix([[1, 2],
                [3, 4]])
matrix1 = Matrix([[1, 2],
                [3, 4]])
matrix *= matrix1
# 7, 10
# 15, 22
```
You can also clear or fill the matrix with any numbers!
```python
matrix = Matrix([[1, 2],
                [3, 4]])
# 1 2
# 3 4

matrix.clear()
# 0 0
# 0 0

matrix.fill()
# 0 0
# 0 0

matrix.fill(7)
# 7 7
# 7 7
```
you can also edit individual parts of the matrix
```python
matrix.setAt(0, 0, 8)
# 8 7
# 7 7

a = matrix.getAt(0, 1)
# 7
```
And also you can mirror the matrix:
```python
matrix.flip()
# 7 7
# 7 8
```

### ArithmeticSequence
There are many ways to initialize an arithmetic sequence.
```python
ars = ArithmeticSequence(0, 2)
ars = ArithmeticSequence([0, 2])
ars.getElem(1) # 2
ars.getElem(0) # 0
ars.getElem(4) # 8
```
You can also get the sum of the elements
```python
ars = ArithmeticSequence(5, 5)
ars.getSum(0) # 5
ars.getSum(2) # 15
```

### GeometricSequence
There are many ways to initialize an arithmetic sequence.
```python
ars = GeometricSequence(1, 2)
ars = GeometricSequence([1, 2])
ars.getElem(1) # 2
ars.getElem(0) # 1
ars.getElem(4) # 16
```
You can also get the sum of the elements
```python
ars = ArithmeticSequence(1, 2)
ars.getSum(0) # 1
ars.getSum(2) # 7
ars.getSum(1) # 3
```

## utils
This module can make your life much easier.
```python
def smthDef(arg1, arg2, **kwargs):
    print(getValue(kwargs, "argument", None))
# getValue - abbreviation of kwargs["argument"] if "argument" in kwargs else None

@autoRun
# the decorator simply automatically invokes the object as soon as it is initialized
def hello():
    print("hi")

downloadFileFromUrl("url", "path to file")
# this method downloads the file from the link and places it in the specified path.

updateLibrary("0.2.42")
# this method automatically updates the library to the specified version.
# if no version is specified, the library is updated to the latest version.

lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
print(splitList(lst, 2))
# [[1, 2], [3, 4], [5, 6], [7, 8], [9, 0]]

lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
print(splitList(lst, 3))
# [[1, 2, 3], [4, 5, 6], [7, 8, 9], [0]]
# the splitList method tries to divide the passed list into equal parts

timer = Timer()
# Timer-class for calling certain functions after a certain time.

@timer.after(1000)
# after method run this function after 1000 milliseconds
def hi():
  print("hello world")

@timer.afterEvery(100, 1000)
# the after Every method starts this function after 100 milliseconds and will call it every subsequent 1000 milliseconds
def hello(): print("hello")

timer.cancel()
# when the timer method is called.cancel will automatically close all running timers of this timer

```
