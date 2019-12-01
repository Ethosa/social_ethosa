# -*- coding: utf-8 -*-
# author: ethosa
from ..utils import *
from .vkauth import VKAuth
requests.packages.urllib3.disable_warnings()
from .vkaudio import Audio
from copy import copy
from .uploader import Uploader

class Vk:
    '''
    docstring for Vk

    Get vk access token here:
    https://vkhost.github.io/ (choose the Kate mobile.)

    for handling new messages:
    In the official VK API documentation, the event of a new message is called "message_new", so use:

    @vk.on_message_new
    def getMessage(obj):
        printf(obj)
        printf('text message:', obj.text) # see https://vk.com/dev/objects/message for more info
        printf(obj.obj)
        printf(obj.peer_id)
    '''

    def __init__(self, token="", version_api="5.103",
            group_id="", login="", password=""):
        """initialization method
        
        Required for authorization in VK via token
        
        Arguments:
            token {str} -- VK token
            version_api {float or str} -- the version of VK API
            group_id {str or int} -- ID groups (if you authorize through the group)
            login {str} -- login in vk for get token and auth (default:{""})
            password {str} -- password in vk for get token and auth (default:{""})
        """
        if login and password:
            auther = VKAuth(login, password)
            auther.logIn()
            token = auther.getToken()
        self.token_vk = token
        self.version_api = version_api
        self.group_id = group_id

        # Initialize methods
        self.longpoll = LongPoll(self)
        self.method = Method(self).use
        self.fastMethod = Method(self).fuse
        self.execute = lambda code: self.fastMethod("execute", {"code" : code})

        self.help = Help

        self.vk_api_url = "https://api.vk.com/method/"

        printf("The token is set. Check that it is correct ...")
        test = ''.join(
            requests.get(
                '%smessages.getLongPollServer?access_token=%s&v=%s%s' % (self.vk_api_url,
                    self.token_vk,
                    self.version_api,
                    "&group_id=%s" % (self.group_id) if self.group_id else "")).json())
        printf("Error!" if test == "error" else 'Succesfull!')

        self.uploader = Uploader(vk=self)

    def getUserHandlers(self):
        """get all user handlers
        """
        return ["on_%s" % i for i in users_event]


    # Handler wrapper
    # Use it:
    # def a(func): vk.listenWrapper('message_new', Obj, func)
    # @a
    # def get_mess(obj):
    #   print(obj.text)
    def listenWrapper(self, type_value, classWrapper, function, e="type"):
        def listen(e=e):
            if isinstance(type_value, int):
                e = 0
            for event in self.longpoll.listen():
                if event.update[e] == type_value:
                    function(classWrapper(event.update))
        if "%s" % type(function) == "<class 'function'>" or "%s" % type(function) == "<class 'method'>":
            Thread_VK(listen).start()
        else:
            classWrapper = function
            return lambda function: self.listenWrapper(type_value, classWrapper, function)

    def on_message(self, classWrapper=dict, command=None, text=None, startCommand=["/"]):
        def listen(function):
            type_value = "message_new" if self.group_id else 4
            e = "type" if self.group_id else 0

            def send(update):
                update["text"] = update["text"][len("/%s" % command):]
                returned = function(update)
                attachments = getValue(returned, "attachments", [])
                sticker_id = getValue(returned, "sticker_id", 0)
                self.messages.send(message=getValue(returned, "message", returned),
                        peer_id=getValue(returned, "peer_id", update["peer_id"]),
                        attachment=",".join(attachments),
                        sticker_id=sticker_id)

            def l():
                for event in self.longpoll.listen():
                    if event.update[e] == type_value:
                        update = classWrapper(event.update)

                        for cmd in startCommand:
                            if update["text"].startswith(cmd):
                                update["text"] = update["text"][len(cmd):]

                        if update["text"] == text or update["text"].startswith("%s" % (command)):
                            Thread_VK(send, update).start()
            Thread_VK(l).start()
        return copy(listen)

    def getRandomId(self):
        return random.randint(-2_000_000, 2_000_000)

    def __getattr__(self, method):
        if method.startswith("on_"):
            method = method[3:]
            if method not in users_event.keys():
                return lambda function: self.listenWrapper(method, Obj, function)
            else:
                return lambda function: self.listenWrapper(users_event[method][0], Obj, function)
        else: return Method(vk=self, method=method)

    def __str__(self):
        return "<Vk %s object at 0x%0x (group_id=%s)>" % (self.version_api, self.__hash__(), self.group_id)


class VkError(Exception):
    def __init__(self, message): self.message = message


class LongPoll:
    def __init__(self, vk=None):
        """constructor for Longpoll
        
        Keyword Arguments:
            vk {Vk} -- Vk authed object (default: {None})
        """
        if vk:
            self.group_id = vk.group_id
            self.access_token = vk.token_vk
            self.version_api = vk.version_api
        self.vk_api_url = 'https://api.vk.com/method/'
        self.ts = "0"
        self.session = requests.Session()
        self.session.headers = {
            "Content-Type" : "application/json"
        }

    def listen(self):
        """listening to longpoll
        
        Yields:
            [Event] -- event
        """
        if self.group_id:
            response = self.session.get("%sgroups.getLongPollServer?access_token=%s&v=%s&group_id=%s" %
                                (self.vk_api_url, self.access_token, self.version_api, self.group_id)).json()
            try:
                response = response['response']
            except Exception as e:
                raise VkError("auth error, %s. response: <%s>" % (e, response))
            self.ts = response['ts']
            self.key = response['key']
            self.server = response['server']
            emptyUpdates = []

            while 1.0:
                response = self.session.get('%s?act=a_check&key=%s&ts=%s&wait=25' % (self.server, self.key, self.ts)).json()
                self.ts = getValue(response, 'ts', self.ts)
                updates = getValue(response, 'updates')

                if updates:
                    for update in updates: yield Event(update)
                else:
                    emptyUpdates.append(0)
                if len(emptyUpdates) > 100:
                    break
            for e in self.listen():
                yield e
        else:
            response = self.session.get("%smessages.getLongPollServer?access_token=%s&v=%s" %
                                (self.vk_api_url, self.access_token, self.version_api)).json()
            try:
                response = response['response']
            except Exception as e:
                raise VkError("auth error, %s. response: <%s>" % (e, response))
            self.ts = response["ts"]
            self.key = response["key"]
            self.server = response["server"]
            emptyUpdates = []

            while 1.0:
                response = self.session.get('https://%s?act=a_check&key=%s&ts=%s&wait=25&mode=202&version=3' % (self.server,
                                            self.key, self.ts)).json()
                self.ts = getValue(response, 'ts', self.ts)
                updates = getValue(response, 'updates')

                if updates:
                    for update in updates: yield Event(update)
                else:
                    emptyUpdates.append(0)
                if len(emptyUpdates) > 100:
                    break
            for e in self.listen():
                yield e


# Class for use anything vk api method
# Usage:
# response = vk.method(method='wall.post', message='Hello, world!')
class Method:
    def __init__(self, vk=None, method=""):
        if vk:
            self.group_id = vk.group_id
            self.access_token = vk.token_vk
            self.version_api = vk.version_api
            self.getRandomId = vk.getRandomId
        self.method = method

    def use(self, method, **kwargs):
        url = "https://api.vk.com/method/%s" % method
        kwargs['access_token'] = self.access_token
        kwargs['v'] = self.version_api
        response = requests.post(url, data=kwargs).json()
        if "error" in response:
            raise VkError("error in method call <%s>" % response)
        return response

    def fuse(self, method, kwargs):
        url = "https://api.vk.com/method/%s" % method
        kwargs['access_token'] = self.access_token
        kwargs['v'] = self.version_api
        response = requests.post(url, data=kwargs).json()
        if "error" in response:
            raise VkError("error in method call <%s>" % response)
        return response

    def __getattr__(self, method):
        method = "%s.%s" % (self.method, method)
        def send(**kwargs):
            if method == "messages.send":
                kwargs["random_id"] = self.getRandomId()
            return self.fuse(method, kwargs)
        return lambda **kwargs: send(**kwargs)

class Keyboard:
    """
    docstring for Keyboard

    use it for add keyboard in message

    keyboard = Keyboard()
    keyboard.addButton(Button(type='text', label='lol'))
    keyboard.addLine()
    keyboard.addButton(Button(type='text', label='hello', color=ButtonColor.POSITIVE))
    keyboard.addButton(Button(type='text', label='world', color=ButtonColor.NEGATIVE))
    # types "location", "vkpay", "vkapps" can't got colors. also this types places on all width line.
    keyboard.addButton(Button(type='location''))
    keyboard.addButton(Button(type='vkapps'', label='hello, world!'))
    keyboard.addButton(Button(type='vkpay''))
    """
    def __init__(self, **kwargs):
        self.keyboard = {
            "one_time" : getValue(kwargs, "one_time", True),
            "buttons" : getValue(kwargs, "buttons", [[]]),
            "inline" : getValue(kwargs, "inline", False)
        }
        if self.keyboard["inline"]:
            self.maxSize = (3, 3)
            del self.keyboard["one_time"]
        else:
            self.maxSize = (4, 10)

    def addLine(self):
        if len(self.keyboard['buttons']) < self.maxSize[1]:
            self.keyboard['buttons'].append([])

    def addButton(self, button):
        if len(self.keyboard['buttons'][::-1][0]) < self.maxSize[0]:
            if button['action']['type'] != 'text' and len(self.keyboard['buttons'][-1]) >= 1:
                self.addLine()
            if len(self.keyboard['buttons']) < self.maxSize[1]+1:
                self.keyboard['buttons'][::-1][0].append(button)
        else:
            self.addLine()
            if len(self.keyboard['buttons']) < self.maxSize[1]+1:
                self.addButton(button)

    def compile(self):
        return json.dumps(self.keyboard)

    def clear(self):
        self.keyboard["buttons"] = [[]]

    def createAndPlaceButton(self, *args, **kwargs):
        self.addButton(Button(*args, **kwargs))

    def visualize(self):
        for line in self.keyboard["buttons"]:
            sys.stdout.write("%s\n" % " ".join(["[%s]" % button["action"]["label"]
                                                if "label" in button["action"] else "[%s button]" % button["action"]["type"]
                                                for button in line]))


class Button:
    """
    docstring for Button

    Button use for Keyboard.
    Usage:
    red_button = Button(label='hello!', color=ButtonColor.NEGATIVE)

    and use red button:
    keyboard.add_button(red_button) # easy and helpfull!
    """
    PRIMARY = "primary"
    SECONDARY = "secondary"
    NEGATIVE = "negative"
    POSITIVE = "positive"
    def __init__(self, type="text", label="бан", payload="",
            hash="action=transfer-to-group&group_id=1&aid=10", owner_id="-181108510",
            app_id="6979588", color="primary"):
        self.type = type

        actions = {
            "text" : {
                "type" : "text",
                "label" : label,
                "payload" : payload
            },
            "location" : {
                "type" : "location",
                "payload" : payload
            },
            "vkpay" : {
                "type" : "vkpay",
                "payload" : payload,
                "hash" : hash
            },
            "vkapps" : {
                "type" : "open_app",
                "payload" : payload,
                "hash" : hash,
                "label" : label,
                "owner_id" : owner_id,
                "app_id" : app_id
            }
        }

        self.action = getValue(actions, self.type, actions['text'])
        self.color = color

    def setText(self, text):
        if "label" in self.action:
            self.action["label"] = text

    def setColor(self, color):
        self.color = color

    def getButton(self):
        kb = {'action' : self.action, 'color' : self.color}
        if kb['action']['type'] != 'text':
            del kb['color']
        return kb

    def __new__(self, type="text", label="бан", payload="",
                hash="action=transfer-to-group&group_id=1&aid=10", owner_id="-181108510",
                app_id="6979588", color="primary"):
        self.__init__(self, type, label, payload, hash, owner_id, app_id, color)
        return self.getButton(self)


class Help:
    """
    docstring for Help

    usage:
    vk.help() - return list of all methods

    vk.help('messages') - return list of all messages methods

    vk.help('messages.send') - return list of all params method
    """
    def __new__(self, *args, **kwargs):
        if not args:
            resp = requests.get('https://vk.com/dev/methods').text
            response = resp.split('<div id="dev_mlist_submenu_methods" style="">')[1].split('</div>')[0].split('<a')
            return [i.split('>')[1].split('</a')[0].lower()
                    for i in response if len(i.split('>')) > 1 and i.split('>')[1].split('</a')[0] != '']
        else:
            return self.__getattr__(self, args[0])
    def __getattr__(self, method):
        if '.' not in method:
            resp = requests.get('https://vk.com/dev/%s' % method).text
            response = resp.split('<span class="dev_methods_list_span">')
            response = [i.split('</span>', 1)[0] for i in response if len(i.split('</span>', 1)[0]) <= 35]
            return response
        else:
            response = requests.get(
                'https://vk.com/dev/%s' % method).text.split('<table class="dev_params_table">')[1].split('</table>')[0]

            params = {
                i.split('<td')[1].split('>')[1].split('</td')[0] : i.split('<td')[2].split('>', 1)[1].split('</td')[0]
                for i in response.split('<tr') if len(i) > 2 }

            for i in params.keys():
                params[i] = params[i].replace('\n', ' ').replace('&lt;', '{').replace('&gt;', '}')
                while '<' in params[i]:
                    pos = [params[i].find('<'), params[i].find('>')]
                    params[i] = "%s%s" % (params[i][:pos[0]], params[i][pos[1]+1:])
            return params
