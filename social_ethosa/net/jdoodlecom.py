# -*- coding: utf-8 -*-
# author: ethosa
import requests
import json


class JDoodle:
    """
    Usage:

    compiler = JDoodle(clientId="your client id", clientSecret="your client secret")

    compiler.setLanguage("python3")
    compiler.setScript("puts 'hello world'")

    compiled = compiler.compile()

    print(compiled["response"])
    print(compiled["output"])
    print(compiled["statusCode"])
    print(compiled["memory"])
    print(compiled["cpuTime"])
    """
    def __init__(self, language="python3", clientId="", clientSecret=""):
        """initialize JDoodle

        Keyword Arguments:
            language {str} -- computer language (default: {"python3"})
            clientId {str} -- client id (default: {""})
            clientSecret {str} -- client secret (default: {""})
        """
        self.language = "python3"
        self.versionIndex = "0"
        self.stdin = ""
        self.script = ""

        self.url = "https://api.jdoodle.com/v1/execute"
        self.url1 = "https://api.jdoodle.com/v1/credit-spent"

    def setLanguage(self, language):
        """set language code

        Arguments:
            langName {str}
        """
        self.language = language

    def setScript(self, script):
        """set code for compile

        Arguments:
            script {str}
        """
        self.script = script

    def setStdin(self, stdin):
        """set input to compile

        Arguments:
            stdin {str}
        """
        self.stdin = stdin

    def setVersionIndex(self, versionindex):
        """set language version index

        Arguments:
            versionindex {int}
        """
        self.versionIndex = versionindex

    def compile(self, language="python3", versionIndex=0, script="", stdin=""):
        """compile source code

        Keyword Arguments:
            language {str} -- script language (default: {"python3"})
            versionIndex {number} -- language version (default: {0})
            script {str} -- source code (default: {""})
            stdin {str} -- input (default: {""})

        Returns:
            dict -- compiled code
        """
        data = {
            "clientId": self.clientId,
            "clientSecret": self.clientSecret,
            "script": script if script else self.script,
            "language": language if language else self.language,
            "stdin": stdin if stdin else self.stdin,
            "versionIndex": versionIndex if versionIndex else self.versionIndex
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.url, data=json.dumps(data), headers=headers).json()
        return response

    def getUsed(self):
        """get used info

        Returns:
           dict  -- used info
        """
        data = {
            "clientId": self.clientId,
            "clientSecret": self.clientSecret
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.url1, data=json.dumps(data), headers=headers).json()
        return response
