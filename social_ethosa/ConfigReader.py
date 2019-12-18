# -*- coding: utf-8 -*-
# author: ethosa

from .net import *
import os

if os.path.exists("cfg.py"):
    from cfg import *
    vk = Vk(**vk)
