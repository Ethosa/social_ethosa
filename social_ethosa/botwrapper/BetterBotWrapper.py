# -*- coding: utf-8 -*-
# author: Ethosa

from copy import copy
import pickle

import regex


class BetterBotWrapper:
    """BetterBotWrapper class

    You can use it to store a database of answers
    """
    def __init__(self, bbw=None):
        """constructor for BetterBotWrapper class

        creates an instance of a class

        Keyword Arguments:
            bbw {BetterBotWrapper} -- other (default: {None})
        """
        self.base = copy(bbw.base) if bbw else {}

    def addPattern(self, q, a, mode="==", answer_type="method"):
        """create new pattern

        Arguments:
            q {str} -- question
            a {str} -- answer

        Keyword Arguments:
            mode {str} -- answer mode, may be "==", ":==",
                            "==:", "re" (default: {"=="})
            answer_type {str} -- answer type, may be "method" (default: {"method"})
        """
        answer = {
            "answer": a.__name__,
            "mode": mode,
            "answer_type": answer_type
        }
        exec("self.%s = a" % (a.__name__))
        if q not in self.base:
            self.base[q] = [answer]
        else:
            self.base[q].append(answer)

    def answer(self, q):
        """get the answer to the question

        Arguments:
            q {str} -- question

        Returns:
            object -- answer
        """
        for i in self.base:
            for j in self.base[i]:
                f = eval("self.%s" % j["answer"])
                if j["mode"] == "==":
                    if q == i:
                        if j["answer_type"] == "method":
                            return f(q)
                elif j["mode"] == ":==":
                    if q.startswith(i):
                        if j["answer_type"] == "method":
                            return f(q[len(i):].strip())
                elif j["mode"] == "==:":
                    if q.endswith(i):
                        if j["answer_type"] == "method":
                            return j["answer"](q[:-len(i)].strip())
                elif j["mode"] == "re":
                    if regex.search(i, q):
                        searched = regex.search(i, q)
                        if j["answer_type"] == "method":
                            return f(searched, q)

    def pattern(self, q, mode="=="):
        def answer(m):
            self.addPattern(q, m, mode)
        return answer

    def removePattern(self, q):
        """remove pattern from db

        Arguments:
            q {str} -- question
        """
        del self.base[q]
