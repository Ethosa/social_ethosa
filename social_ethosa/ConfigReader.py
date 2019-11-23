# -*- coding: utf-8 -*-
# author: ethosa

from .net import *

try:
    from cfg import *
    vk = Vk(**vk)
except:
    pass