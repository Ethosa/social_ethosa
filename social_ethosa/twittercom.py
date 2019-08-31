try:
    import requests
    requests.packages.urllib3.disable_warnings()
except:
    raise ImportError('Please install requests library! "pip install requests".')

from threading import Thread
from .smiles import *
from .utils import *
import traceback
import datetime
import random
import time
import json
import sys
import os

class Twitter:
    """
    docstring for Twitter
    """
    def __init__(self, *args, **kwargs):
        self.token = get_val(kwargs, 'token', '')
        