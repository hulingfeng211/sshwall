# -*- coding:utf-8 -*- 

from handlers import *
from tornado.web import url
from auth import *
from tornado.web import RedirectHandler

handlers = [
    url(r"{0}".format(config.URI_SUB_PATH), IndexHandler,{},name='home'),
    (r"/", RedirectHandler,{"url":config.URI_SUB_PATH}),
    url(r"{0}/server".format(config.URI_SUB_PATH), ServerHandler,{},name='server'),
    url(r"{0}/group".format(config.URI_SUB_PATH), GroupHandler,{},name='group'),
    url(r"{0}/user".format(config.URI_SUB_PATH), UserHandler,{},name='user'),
    url(r"{0}/user/server".format(config.URI_SUB_PATH), UserServerHandler,{},name='user.server'),
    url(r"{0}/terminal".format(config.URI_SUB_PATH), TerminalHandler,{},name='terminal'),
    url(r"{0}/login".format(config.URI_SUB_PATH), LoginHandler,{},name='login'),
    url(r"{0}/changepwd".format(config.URI_SUB_PATH), ChangePasswordHandler,{},name='changepwd'),
    url(r"{0}/logout".format(config.URI_SUB_PATH), LogoutHandler,{},name='logout'),
    url(r"{0}/ws".format(config.URI_SUB_PATH), WSHandler,{},name='websocket')
]
