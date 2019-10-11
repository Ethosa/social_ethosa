# -*- coding: utf-8 -*-
# author: ethosa
from ..utils import *

class BloggerRoot:
    def __init__(self, blogger):
        self.apiKey = blogger.apiKey
        self.clientId = blogger.clientId
        self.clientSecret = blogger.clientSecret
        self.debug = blogger.debug
        self.session = blogger.session
        self.url = blogger.url


class Blogger:
    def __init__(self, **kwargs):
        # Getting arguments
        self.apiKey = getValue(kwargs, "apiKey", "")
        self.clientId = getValue(kwargs, "clientId", "")
        self.clientSecret = getValue(kwargs, "clientSecret", "")
        self.debug = getValue(kwargs, "debug")

        self.session = requests.Session()
        self.url = "https://www.googleapis.com/blogger/v3/"

        self.blogs = Blogs(self)
        self.posts = Posts(self)
        self.comments = Comments(self)
        self.pages = Pages(self)

        if self.debug:
            if self.apiKey or (self.clientSecret and self.clientId):
                printf("Successfully!")
            else:
                printf("Api key is wrong!")


class Blogs(BloggerRoot):
    def __init__(self, blogger):
        super(Blogs, self).__init__(blogger)

    def get(self, blogId):
        return Obj(self.session.get("%sblogs/%s" % (self.url, blogId),
                                        params={"key" : self.apiKey}).json())

    def getByUrl(self, blogUrl):
        return Obj(self.session.get("%sblogs/byurl" % (self.url),
                                params={"url" : blogUrl, "key" : self.apiKey}).json())


class Posts(BloggerRoot):
    def __init__(self, blogger):
        super(Posts, self).__init__(blogger)

    def search(self, blogId, q):
        return Obj(self.session.get("%sblogs/%s/posts/search" % (self.url, blogId),
                                params={"q" : q, "key" : self.apiKey}).json())
    def get(self, blogId):
        return Obj(self.session.get("%sblogs/%s/posts" % (self.url, blogId),
                                params={"key" : self.apiKey}).json())
    def getById(self, blogId, postId):
        return Obj(self.session.get("%sblogs/%s/posts/%s" % (self.url, blogId, postId),
                                params={"key" : self.apiKey}).json())
    def getByPath(self, blogId, path):
        return Obj(self.session.get("%sblogs/%s/posts/bypath" % (self.url, blogId),
                                params={"path" : path, "key" : self.apiKey}).json())


class Comments(BloggerRoot):
    """
    comments object
    """
    def __init__(self, blogger):
        super(Comments, self).__init__(blogger)

    def get(self, blog, post):
        """Receiving comments from the post
        
        Arguments:
            blog {int} -- [blog id]
            post {int} -- [post id]
        
        Returns:
            Obj -- dictionary object
        """
        return Obj(self.session.get("%sblogs/%s/posts/%s/comments" % (self.url, blog, post),
                                params={"key" : self.apiKey}).json())

    def getSpecific(self, blog, post, cid):
        """Receiving comment from the post
        
        Arguments:
            blog {int} -- [blog id]
            post {int} -- [post id]
            cid {int} -- [comment id]
        
        Returns:
            Obj -- dictionary object
        """
        return Obj(self.session.get("%sblogs/%s/posts/%s/comments/%s" % (self.url, blog, post, cid),
                                params={"key" : self.apiKey}).json())


class Pages(BloggerRoot):
    """
    pages object
    """
    def __init__(self, blogger):
        super(Pages, self).__init__(blogger)

    def get(self, blog):
        """Getting a pages from blog
        
        Arguments:
            blog {[int]} -- [blog id]
        
        Returns:
            [Obj] -- [dictionary object]
        """
        return Obj(self.session.get("%sblogs/%s/pages" % (self.url, blog),
                                params={"key" : self.apiKey}).json())
    def getSpecific(self, blog, pid):
        """Getting a pages from blog
        
        Arguments:
            blog {[int]} -- [blog id]
            pid {[int]} -- [page id]
        
        Returns:
            [Obj] -- [dictionary object]
        """
        return Obj(self.session.get("%sblogs/%s/pages/%s" % (self.url, blog, pid),
                                params={"key" : self.apiKey}).json())
