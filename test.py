from social_ethosa import *

bbs = BetterBotBase()
print(vk)

@vk.on_message(text="lol")
def a(msg):
    return "b"

@vk.on_message(command="ban ")
def a(msg):
    return "ты дохуя %s?" % msg["text"]

@vk.on_message(command="справедлива ")
def a(msg):
    return {"sticker_id" : 163}

@vk.on_message(command="add")
def a(msg):
    user = bbs.autoInstall(int(msg["object"]["from"]))
    user.money += 1
    bbs.saveSelf()
    return "У вас %s монет блять)" % user.money