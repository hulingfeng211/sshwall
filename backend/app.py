# -*- coding:utf-8 -*-

import os.path
import sys
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
from tornado.options import options, define
from urls import handlers
from tornado.log import gen_log
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

print(os.path.dirname(__file__))
define('port', default=8989, type=int, help='server listening port')
define('init', default=False, type=bool, help='init database')

settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    static_url_prefix="{0}/assets/".format(config.URI_SUB_PATH),
    cookie_secret='abcefgh12345690',
    debug=True)


class Application(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = scoped_session(sessionmaker(bind=engine))

    def initial_db(self, super_user_name, super_user_password):
        user = User(username=super_user_name,
                    password=super_user_password, is_super=True)
        self.db.add(user)
        self.db.commit()

def main():
    options.parse_command_line()
    app = Application()
    if options.init:
        create_all()
        super_user_name = input('input super user name,default root:')
        super_user_password = input('input super user password,default root:')
        super_user_name = super_user_name.strip() or 'root'
        super_user_password = super_user_password.strip() or 'root'
        app.initial_db(super_user_name, super_user_password)
        sys.exit(1)
    app.listen(options.port)
    gen_log.debug('server at:{%s}' % options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
