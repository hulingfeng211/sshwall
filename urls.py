__author__ = 'xsank'

from handlers import *
from tornado.web import url
from auth import *
from tornado.web import RedirectHandler

handlers = [
    url(r"/webssh/", IndexHandler,{},name='home'),
    (r"/", RedirectHandler,{"url":"/webssh/"}),
    url(r"/webssh/server", ServerHandler,{},name='server'),
    url(r"/webssh/group", GroupHandler,{},name='group'),
    url(r"/webssh/user", UserHandler,{},name='user'),
    url(r"/webssh/user/server", UserServerHandler,{},name='user.server'),
    url(r"/webssh/terminal", TerminalHandler,{},name='terminal'),
    url(r"/webssh/login", LoginHandler,{},name='login'),
    url(r"/webssh/changepwd", ChangePasswordHandler,{},name='changepwd'),
    url(r"/webssh/logout", LogoutHandler,{},name='logout'),
    url(r"/webssh/ws", WSHandler,{},name='ternimal')
]
