# -*- coding: utf-8 -*-
# author: ethosa
import requests

class JDoodle:
    JAVA = "java"
    C = "c"
    C99 = "c99"
    CPP = "cpp"
    CPP14 = "cpp14"
    PHP = "php"
    PERL = "perl"
    PYTHON2 = "python2"
    PYTHON3 = "python3"
    RUBY = "ruby"
    GOLANG = "go"
    SCALA = "scala"
    BASH = "bash"
    SQL = "sql"
    PASCAL = "pascal"
    CSHARP = "csharp"
    VBNET = "vbn"
    HASKELL = "haskell"
    OBJECTIVEC = "objc"
    SWIFT = "swift"
    GROOVY = "groovy"
    FORTRAN = "fortran"
    BRAINFUCK = "brainfuck"
    LUA = "lua"
    TCL = "tcl"
    HACK = "hack"
    RUST = "rust"
    D = "d"
    ADA = "ada"
    RLANG = "r"
    FREEBASIC = "freebasic"
    VERILOG = "verilog"
    COBOL = "cobol"
    DART = "dart"
    YABASIC = "yabasic"
    CLOJURE = "clojure"
    NODEJS = "nodejs"
    SCHEME = "scheme"
    FORTH = "forth"
    PROLOG = "prolog"
    OCTAVE = "octave"
    COFFEESCRIPT = "coffeescript"
    ICON = "icon"
    FSHARP = "fsharp"
    NASM = "nasm"
    GCCASM = "gccasm"
    INTERCAL = "intercal"
    NEMERLE = "nemerle"
    OCAML = "ocaml"
    UNLAMBDA = "unlambda"
    PICOLISP = "picolisp"
    SPIDERMONKEY = "spidermonkey"
    RHINO = "rhino"
    CLISP = "clisp"
    ELIXIR = "elixir"
    FACTOR = "factor"
    FALCON = "falcon"
    FANTOM = "fantom"
    NIM = "nim"
    PIKE = "pike"
    SMALLTALK = "smalltalk"
    OZMOZART = "mozart"
    LOLCODE = "lolcode"
    RACKET = "racket"
    KOTLIN = "kotlin"
    WHITESPACE = "whatespace"
    """
    Usage:

    compiler = JDoodle(clientId="your client id", clientSecret="your client secret")

    compiler.setLanguage(JDoodle.RUBY)
    compiler.setScript("puts 'hello world'")

    compiled = compiler.compile()

    print(compiled.response)
    print(compiled.output)
    print(compiled.statusCode)
    print(compiled.memory)
    print(compiled.cpuTime)
    """
    def __init__(self, language="python3", clientId="", clientSecret=""):
        """initialize JDoodle
        
        Keyword Arguments:
            language {str} -- computer language (default: {"python3"})
            clientId {str} -- client id (default: {""})
            clientSecret {str} -- client secret (default: {""})
        """
        self.programLanguage = JDoodle.PYTHON3
        self.versionIndex = "0"
        self.stdin = ""
        self.script = ""

        self.url = "https://api.jdoodle.com/v1/execute"
        self.url1 = "https://api.jdoodle.com/v1/credit-spent"

    def setLanguage(self, langName):
        """set language code
        
        Arguments:
            langName {str}
        """
        self.programLanguage = langName

    def setScript(self, script):
        """set code for compile
        
        Arguments:
            script {str}
        """
        self.script = script

    def setStdIn(self, stdin):
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
        data = { "clientId" : self.clientId,
            "clientSecret" : self.clientSecret,
            "script" : script,
            "language" : language,
            "stdin" : stdin,
            "versionIndex" : versionIndex }
        headers = { "Content-Type": "application/json" }
        response = requests.post(self.url, data=json.dumps(data), headers=headers).json()
        return response

    def getUsed(self):
        """get used info
        
        Returns:
           dict  -- used info
        """
        data = { "clientId" : self.clientId,
            "clientSecret" : self.clientSecret }
        headers = { "Content-Type": "application/json" }
        response = requests.post(self.url1, data=json.dumps(data), headers=headers).json()
        return response
