# -*- coding:utf-8 -*- 

from handlers import BaseHandler
from tornado.gen import coroutine
from models import *

class LoginHandler(BaseHandler):
    
    @coroutine
    def post(self,*args,**kwargs):
        username=self.get_argument('username',None)
        password=self.get_argument('password',None)

        if all([username,password]):
            user=self.db.query(User).filter(User.username==username).first()
            #assert len(list(users))==1
            #user=users[0]
            if user and username==user.username and password==user.password:
                #set cookie 
                self.set_secure_cookie('user_id',str(user.id))
                self.redirect(self.reverse_url('home'))
            else:
                self.write('username or password error,try again.')
        else:
            self.write('username and password are not allow empty.')

class LogoutHandler(BaseHandler):
    def get(self,*args,**kwargs):
        self.clear_cookie('user_id')
        self.redirect(self.reverse_url('home'))


class ChangePasswordHandler(BaseHandler):
    def post(self,*args,**kwargs):
        old_pwd=self.get_argument('old_pwd',None)
        new_pwd=self.get_argument('new_pwd',None)
        if self.current_user.password==old_pwd:
            self.current_user.password=new_pwd
            self.db.add(self.current_user)
            self.db.commit()
            self.clear_cookie('user_id')#logout
            self.send_client('Change Password Successfuly')
        else:
            self.send_client('Password incorrect.',status_code=-1)
        
    