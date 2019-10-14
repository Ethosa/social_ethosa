# social ethosa
Библиотека Python, использующая requests

## Get started
Установка: `pip install --upgrade social-ethosa`  
Импорт:
```python
from social_ethosa import *
```

## Vkcom
```python
vk = Vk(token="Your token is here", group_id=12345, debug=True, lang="en")
# group_id параметр необходим в том случае, если вы собираетесь авторизироваться через группу
# В этом примере мы будем использовать авторизацию через группу.

@vk.on_message_new
# Этот декоратор является обработчиком событий, который выполняет функцию при новом сообщении, переданную ему
# Название декоратора взято из официальной документации vk.com, но с префиксом "on_"
# Пожалуйста, ознакомьтесь с документацией по ссылке https://vk.com/dev/groups_events
def getMessage(message):
  text = message.text
  peer_id = message.peer_id
  from_id = message.from_id
  attachments = message.attachments
```

Использование загрузчика файлов:
```python
vk.uploader.getUploadUrl("message_photo") # getting a link to upload files
# Вы также можете использовать другие аргументы (argument=value)
# для получения всех названий UploadUrl, используйте метод:
# uploader.getAllTypes()
```
Загрузка файлов:
```python
response = vk.uploader.uploadFile("path") # ы также можете использовать другие аргументы (argument=value)
```

Некоторые audio методы также доступны в моей библиотеке:
```python
login = "89007003535"
password = "qwertyuiop"

audio = Audio(login=login, password=password, debug=1)
audios = audio.get()
# Поскольку методы аудио недоступны в официальном API, мне пришлось сделать парсер сайта
```
## Yandex api
Использование Яндекс.Переводчика:
```python
TOKEN = "translate token"
yt = YTranslator(token=TOKEN)
text = "Пайтон - хороший язык программирования"
response = yt.translate(text=text, lang="en")
print(response)
```
## Trace moe
Использование [TraceMoe api](https://trace):
```python
tracemoe = TraceMoe() # Инициализация для будущего использования
# В директории со скриптом имеется скриншот из аниме с названием "a. png"
response = tracemoe.search("a.png", False, 1)
# param 1 - путь до изображения или url изображения
# param 2 - True, если param 1 является ссылкой
# param 3 - filter search
```
![Изображение не загрузилось :(](https://i.pinimg.com/originals/33/55/37/335537e3904b0a3b204364907b22622f.jpg)

Если аниме найдено, вы можете получить предварительный просмотр видео найденного момента:
```python
video = tracemoe.getVideo(response, mute=0) # mute параметр должен быть 1, если вы хотите получить видео без звука
tracemoe.writeFile("file.mp4", video)
# param 1 является путем до будущего файла
# param 2 это видео, полученное методом getVideo
```

## BotWrapper
В библиотеке имеется обертка для создания ботов!  
Инициализация:
```python
bw = BotWrapper()
```
Получение случайной даты
```python
date = bw.randomDate(fromYear="2001", toYear="3001")
# Возвращается: строка
# fromYear и toYear параметры не обязательные
```

## BetterBotBase
Этот класс использует pickle для обслуживания базы данных.  
Инициализация.
```python
bbs = BetterBotBase("users folder", "dat")
# Первый аргумент - название папки, которая создастся автоматически, если её нет
# Второй аргумент - постфикс файлов. В нашем случае названия файлов будут такими:
# 123123123.dat
```

BetterBotBase может также использоваться вместе с Vkcom:
```python
@vk.on_message_new
def getNewMessage(message):
  from_id = message.from_id
  if from_id > 0:
    user = bbs.autoInstallUser(from_id, vk)
# autoInstallUser автоматически создает или загружает пользователей и возвращает пользователя для дальнейших действий с ним.
```

BotWrapper cможет также взаимодействовать с BetterBotBase!
```python
text = bw.answerPattern("Hello, <name>, your money is <money>!", user)
# answerPattern метод автоматически заменяет переменные от пользователя,
# тем самым делая его немного легче отформатировать строку
```

Вы можете определить свои собственные шаблоны для базы данных!
```python
# сразу после объявления BetterBotBase 
bbs.addPattern("countMessages", 0)
# Первый аргумент - название переменной
# Второй аргумент - значение переменной по умолчанию (например при создании пользователя)
```

Вы создали шаблон, но у старых пользователей переменная не появилась? Нет проблем!
```python
bbs.addNewVariable("countMessages", 0)
# Этот метод работает также, как и addPattern, 
# но добавляет новые значения старым пользователям, если таких значений у них нет
```


## ThisPerson api
Инициализация:
```python
person = ThisPerson()
```

В классе теперь только 3 метода для извлечения несуществующих людей/кошек/вайфу
```python
rperson = person.getRandomPerson()
rcat = person.getRandomCat()
rwaifu = person.getRandomWaifu()
```

после получения сгенерированных фото, они должны быть записаны в файл.
```python
person.writeFile("person.png", rperson)
person.writeFile("cat.png", rcat)
person.writeFile("waifu.png", rwaifu)
```

## Yummyanime club
Здесь мало методов, так как я не нашел официального API. Давайте начнем.
```python
ym = YummyAnime()
ym = YummyAnime(login="yourmail@gmail.com", password="iampassword")
# Вы можете войти в свой аккаунт, если вам это нужно
```
Получение случайного аниме
```python
randomAnime = ym.getRandomAnime()
print(dir(randomAnime))
print(randomAnime())
```
Вы также можете получить список последних обновлений аниме
```python
updates = ym.getUpdates()
anime = updates[0].open() # Вы получите тот же объект, который возвращает метод getRandomAnime() 
print(updates)
print(anime)
```
Вы также можете посмотреть свой профиль
```python
profile = ym.getProfile()
print(profile)
```

## bloggercom api
Модуль для работы с [blogger.com](https://blogger.com)  
Инициализация:
```python
blogger = Blogger(apiKey="Ваш апи ключ")
```

Получение блога по его айди:
```python
blog = blogger.blogs.get(123123)
printf(blog["name"]) # Вы можете использовать blog как словарь
printf(blog.name) # или как объект
printf(blog)
```
Получение блога по его URL:
```python
blog = blogger.blogs.getByUrl("https://meethosa.blogspot.com")
```
Получение постов блога
```python
posts = blogger.posts.get(123123)
```
Получение страниц блога
```python
posts = blogger.pages.get(123123)
```

## eMath
Я решил, что этот модуль мало кому понадобится, поэтому его импорт отделен от основного:
```python
from social_ethosa.eMath import *
```
### Point
Вы можете создать N-мерную точку:
```python
point = Point(0, 0, 0)
point1 = Point(4, 2, 3)
```
А также вы можете найти Евклидово расстояние между ними:
```python
distance = point.euclideanDistance(point1)
print(distance)
```
### Matrix
Также этот модуль имеет класс Матрицы
```python
matrix = Matrix(3, 3) # Создание нулевой матриц 3х3
matrix1 = Matrix([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]]) # Создание матрицы из двухуровневого массива
```
Вы можете транспонировать матрицу
```python
matrix1.transpose()
# 1 4 7
# 2 5 8
# 3 6 9
```
А также умножить матрицу на число
```python
matrix1 *= 3
# 3 12 21
# 6 15 24
# 9 18 27
```
Сложение двух матриц также поддерживается
```python
matrix2 = Matrix([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])
matrix1 += matrix2
# 4 14 24
# 10 20 30
# 16 26 36
```
Произведение двух матриц тоже.
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
Вы также можете очистить матрицу или заполнить её!
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
А также можете установить значения для отдельных чатей матрицы
```python
matrix.setAt(1, 1, 8)
# 8 7
# 7 7

a = matrix.getAt(1, 2)
# 7
```
А также вы можете отразить матрицу
```python
matrix.flip()
# 7 7
# 7 8
```

### ArithmeticSequence
Существует множество способов инициализации арифметической последовательности.
```python
ars = ArithmeticSequence(0, 2)
ars = ArithmeticSequence([0, 2])
ars.getElem(1) # 2
ars.getElem(0) # 0
ars.getElem(4) # 8
```
Вы можете получить суму элементов
```python
ars = ArithmeticSequence(5, 5)
ars.getSum(0) # 5
ars.getSum(2) # 15
```

### GeometricSequence
Инициализация
```python
ars = GeometricSequence(1, 2)
ars = GeometricSequence([1, 2])
ars.getElem(1) # 2
ars.getElem(0) # 1
ars.getElem(4) # 16
```
Вы также можете получить сумму элементов
```python
ars = ArithmeticSequence(1, 2)
ars.getSum(0) # 1
ars.getSum(2) # 7
ars.getSum(1) # 3
```

## utils
Этот модуль сделает вашу жизнь легче.
```python
def smthDef(arg1, arg2, **kwargs):
    print(getValue(kwargs, "argument", None))
# getValue - сокращенная запись kwargs["argument"] if "argument" in kwargs else None

@autoRun
# Декоратор автоматически запускает переданную ему функцию
def hello():
    print("hi")

downloadFileFromUrl("url", "path to file")
# Данный метод скачивает файл по ссылке  помещает его в файл

updateLibrary("0.2.42")
# этот метод автоматически обновляет библиотеку до указанной версии.
# если версия не указана, библиотека обновляется до последней версии.

lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
print(splitList(lst, 2))
# [[1, 2], [3, 4], [5, 6], [7, 8], [9, 0]]

lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
print(splitList(lst, 3))
# [[1, 2, 3], [4, 5, 6], [7, 8, 9], [0]]
# метод split List пытается разделить переданный список на равные части

timer = Timer()
# Timer-класс для вызова определенных функций через определенное время.

@timer.after(1000)
# после метода запустите эту функцию через 1000 миллисекунд
def hi():
  print("hello world")

@timer.afterEvery(100, 1000)
# метод after Every запускает эту функцию через 100 миллисекунд и будет вызывать ее каждые последующие 1000 миллисекунд
def hello(): print("hello")

timer.cancel()
# при вызове метода timer.отмена автоматически закроет все таймеры этого таймера
```
## extra
Этот модуль также, как и eMath должен импортироваться отдельно:
```python
from social_ethosa.extra import *
```
в этом модуле пока что один класс: eList
```python
lst1 = eList() # create []
lst2 = eList("string") # create ["s", "t", "r", "i", "n", "g"]
lst3 = eList(1, 2, 3) # create [1, 2, 3]
lst4 = eList([1, 2, 3]) # create [1, 2, 3]
```
все методы обычных списков присутствуют в этом, однако здесь есть несколько особенностей 
```python
lst1 += 1 # [1]
lst1 += [1, 2] # [1, 1, 2]
lst1 += eList(3, 4) # [1, 1, 2, 3, 4]
lst1.clear() # []
lst1 += [1, 2, 3] # [1, 2, 3]
lst1.split(1) # [[1], [2], [3]]
lst1.clear()
lst1 += [1, 2, 3]
lst1[2] # 3
lst1[3] # error
lst1[3] = 4 # working!
lst1 # [1, 2, 3, 4]
lst1.len() == len(lst1) # True
lst1.sum() == sum(lst1) # True
lst1.standartItem(0)
lst1[8] = 1
lst1 # [1, 2, 3, 4, 0, 0, 0, 0, 1]
```
