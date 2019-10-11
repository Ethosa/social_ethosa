# -*- coding: utf-8 -*-
# author: ethosa
from ..utils import *

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
    def __init__(self, *args, **kwargs):
        self.lang = getValue(kwargs, "lang", "")
        self.clientId = getValue(kwargs, "clientId", "")
        self.clientSecret = getValue(kwargs, "clientSecret", "")
        self.debug = getValue(kwargs, "debug", 0)
        self.programLanguage = JDoodle.PYTHON3
        self.versionIndex = "0"
        self.stdin = ""
        self.script = ""

        self.url = "https://api.jdoodle.com/v1/execute"
        self.url1 = "https://api.jdoodle.com/v1/credit-spent"

    def setLanguage(self, langName): self.programLanguage = langName
    def setScript(self, script): self.script = script
    def setStdIn(self, stdin): self.stdin = stdin
    def setVersionIndex(self, versionindex): self.versionIndex = versionindex

    def compile(self, **kwargs):
        language = getValue(kwargs, "language", self.programLanguage)
        versionIndex = getValue(kwargs, "versionIndex", self.versionIndex)
        script = getValue(kwargs, "script", self.script)
        stdin = getValue(kwargs, "stdin", self.stdin)
        data = { "clientId" : self.clientId,
            "clientSecret" : self.clientSecret,
            "script" : script,
            "language" : language,
            "stdin" : stdin,
            "versionIndex" : versionIndex }
        headers = { "Content-Type": "application/json" }
        response = requests.post(self.url, data=json.dumps(data), headers=headers).json()
        return Compiled(response)

    def getUsed(self):
        data = { "clientId" : self.clientId,
            "clientSecret" : self.clientSecret }
        headers = { "Content-Type": "application/json" }
        response = requests.post(self.url1, data=json.dumps(data), headers=headers).json()
        return response["used"]

class Compiled:
    def __init__(self, response):
        self.response = response
    def __getattr__(self, attr):
        return self.response[attr]
