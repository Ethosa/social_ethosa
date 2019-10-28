# -*- coding: utf-8 -*-
# author: Ethosa

from ..utils import getValue

class BetterUser:
    def __init__(self, **kwargs):
        self.obj = kwargs
        for key in kwargs:
            value = kwargs[key]
            exec("self.%s = %s" % (key, repr(value)))

    def __str__(self):
        return "%s" % {key : eval("self.%s" % key, {}, {"self" : self}) for key in self.obj}

    def __setitem__(self, item, value):
        exec("self.%s = %s" % (item, repr(value)))

    def __getitem__(self, item):
        return eval("self.%s" % item)

