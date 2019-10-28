# -*- coding: utf-8 -*-
# author: Ethosa

from ..utils import getValue

class User:
    def __init__(self, *args, **kwargs):
        self._obj = kwargs

    @property
    def obj(self):
        return self._obj

    @obj.getter
    def obj(self):
        lst = dir(self)
        for i in lst:
            if i in self._obj:
                self._obj[i] = eval("self.%s" % i)
        return self._obj

    def __getattr__(self, attribute):
        value = getValue(self.obj, attribute)
        exec("self.%s = %s" % (attribute, repr(value)))
        return eval("self.%s" % attribute)
        
