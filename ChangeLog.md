<h1 align="center">ChangeLog</h1>

## 0.5.0
- Optimization and Bugfix

## 0.4.9
- Fixed a lot of bugs from the previous version
- Fixed bugs (also from previous version ._.)
- Small optimization  
[Browse files](https://github.com/Ethosa/social_ethosa/tree/b46af9e1bc42fff6fbc1b389216af970e4b39e29)

## 0.4.8
- Optimized all imports
- Removed unnecessary methods
- Added documentation comments  
[Browse files](https://github.com/Ethosa/social_ethosa/tree/464d528e3afac5607e621134cf2447d224958650)

## 0.4.7
- added new method in vkcom:
```python
@vk.on_message(text="hello")
def a(msg):
  return "hello world!"
```
[Browse files](https://github.com/Ethosa/social_ethosa/tree/c52a9e300021c784398de57042714adb21757d87)

## 0.4.6
- New functionality in botwrapper:
```python
from social_ethosa import *

bbs = BetterBotBase("usersFolder")
bbs.autoInstall(1) # 1 is file name
bbs.model1.money += 1000 # model1 -> model 1 -> 1 -> 1 is file name
bbs.saveSelf() # save all opened users
print(bbs.model1.money) # 1000
```
[Browse files](https://github.com/Ethosa/social_ethosa/tree/8f07e0fe16cca0f7d14d105f22b184f56ad66de6)

## 0.4.4
:heavy_exclamation_mark: IMPORTANT :heavy_exclamation_mark: - changed method names in BetterBotBase and BotBase! note this change when updating your current version. 
- removed some unnecessary async methods. 
- small fixes  
[Browse files](https://github.com/Ethosa/social_ethosa/tree/11f61d75caad7b0cb7783ee48ebd8f0d6e9af8cc)

## 0.4.2
- Added graphics module  
[Browse files](https://github.com/Ethosa/social_ethosa/tree/d2143b2525809cf8b1223e5b74dd59bcb14ed9a3)

## 0.4.12
- fixed keyboard and OOP style.  
[Browse files](https://github.com/Ethosa/social_ethosa/tree/8b2f6c74860459dd81e47ccb5e229f1fe34e036e)
