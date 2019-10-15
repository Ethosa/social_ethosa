# -*- coding: utf-8 -*-
# author: Ethosa

from contextlib import contextmanager
import time

class LogManager:
    def __new__(self, fileName, text=""):
        self.fileName = fileName
        if not text:
            return self.__call__(LogManager)
        else:
            with self.__call__(LogManager) as f:
                f.write("%s" % text)
            return self.__call__(LogManager)

    @contextmanager
    def __call__(self):
        file = open(self.fileName, "a")
        try:
            file.write("%s\n" % time.ctime())
            yield file
        finally:
            file.write("\n----------\n")
            file.close()
