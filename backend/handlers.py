# -*- coding:utf-8 -*- 

import uuid
import tornado.websocket

from daemon import Bridge
from data import ClientData
from utils import check_ip, check_port
from tornado.log import gen_log
from tornado.gen import coroutine
from tornado.web import escape,authenticated
from models import *

class BaseHandler(tornado.web.RequestHandler):
     
    @property
    def db(self):
        return self.application.db
    
    #@authenticated
    def prepare(self,*args,**kwargs):
        pass

    def get_current_user(self):
        user_id = self.get_secure_cookie("user_id")
        gen_log.info(user_id)
        if not user_id:
            return None
        user= self.db.query(User).get(int(user_id))
        return user
    
    def send_client(self,data,status_code=0):
        
        self.set_header('content-type','application/json')
        self.write(escape.json_encode({'data':data,'status':status_code}))

    def has_login(self):
        return current_user!=None

class UserServerHandler(BaseHandler):
    def post(self,*args,**kwargs):
        gen_log.info(self.request.body)
        user_id=self.get_argument('userid')
        server_id=self.get_argument('serverid')
        is_add=self.get_argument('is_add')
        if all([user_id,server_id,is_add]):
            user=self.db.query(User).get(int(user_id))
            server=self.db.query(Server).get(int(server_id))
            #gen_log.info(is_add)
            if  is_add=='false':
                #gen_log.info('remove')
                user.servers.remove(server)
            else:
                user.servers.append(server)
            self.db.commit()
            self.send_client('ok')
        else:
            self.send_client('error',status_code=1)

class UserHandler(BaseHandler):
    def get(self,*args,**kwargs):
        groups=self.db.query(Group).all()
        servers=self.db.query(Server).all()
        users=self.db.query(User).filter(User.is_super==False).all()
        self.render('user.mgt.html',groups=groups,servers=servers,users=users)        
    
    def post(self,*args,**kwargs):
        userid=self.get_argument('id',None)
        servers=self.get_arguments('server')
        username=self.get_argument('username',None)
        password=self.get_argument('password',None)

        if all([username,password]):
            if userid:
                user=self.db.query(User).get(int(userid))
                user.username=username
                user.password=password
            else:
                user=User(username=username,password=password)
            if servers:
                server_list=self.db.query(Server).filter(Server.id.in_([int(server_id) for server_id in servers])).all()
                user.servers=server_list
            self.db.add(user)
            self.db.commit()
            self.redirect(self.reverse_url('user'))
        else:
            self.flush('username and password are not allow empty.')
    
    def delete(self,*args,**kwargs):
        user_id=self.get_argument("userid",None)

        if user_id:
            user=self.db.query(User).get(int(user_id))
            self.db.delete(user)
            self.db.commit()
            self.send_client('ok')
        else:
            self.send_client('error',status_code=1)
            


class GroupHandler(BaseHandler):
    def get(self,*args,**kwargs):
        groups=self.db.query(Group).all()
        self.render('group.mgt.html',groups=groups)
    
    def post(self,*args,**kwargs):
        group_name=self.get_argument('groupname',None)
        if group_name:
            group=Group(name=group_name)
            self.db.add(group)
            self.db.commit()
            self.redirect(self.reverse_url('group'))
    
    def delete(self,*args,**kwargs):
        id=self.get_argument('id',None)
        if id:
            group=self.db.query(Group).get(int(id))
            self.db.delete(group)
            self.db.commit()
            #self.redirect(self.reverse_url('group'))
            self.write('OK')
            
            

class IndexHandler(BaseHandler):
    @coroutine
    def get(self):
        groups=self.db.query(Group).all()
        group_id=self.get_argument('group',None)
        if self.current_user is None:
            self.render('index.html',server_list=[],groups=groups)
            return 
        if group_id:
            if self.current_user.is_super:
                servers=self.db.query(Server).filter(Server.group_id==int(group_id))
            else:
                servers=[server for server in self.current_user.servers if server.group_id==int(group_id)]
        else:

            if self.current_user.is_super:
                servers=self.db.query(Server).all()
            else:
                servers=self.current_user.servers
        self.render("index.html",server_list=servers,groups=groups)

class TerminalHandler(BaseHandler):
    def get(self,*args,**kwargs):
        id=self.get_argument('id',-1)
        server=self.db.query(Server).get(int(id))
        #get_server(id)
        if server:
            self.render('server.html',server=server)
        else:
            self.write('Server {} is not exists'.format(id));

class ServerHandler(BaseHandler):
    def get(self,*args,**kwargs):
        id=self.get_argument('id',-1)
        server=self.db.query(Server).get(int(id))
        #get_server(id)
        if server:
            self.write(escape.json_encode({
            "id":server.id,
            "host":server.host,
            "port":server.port,
            "username":server.username,
            "secret":server.secret,
            "remark":server.remark,
            "name":server.name
        }))
            #self.write(escape.json_encode(server))
        else:
            self.write({})
    
    def delete(self,*args,**kwargs):
        server_id=self.get_argument('server',None)
        if server_id:
            server=self.db.query(Server).get(int(server_id))
            self.db.delete(server)
            self.db.commit()
        self.write('ok')
    
    def post(self,*args,**kwargs):
        gen_log.info(self.request.body);
        server_id=self.get_argument('id',None)
        name=self.get_argument('name',None)
        host=self.get_argument('host',None)
        port=self.get_argument('port',None)
        username=self.get_argument('username',None)
        password=self.get_argument('password',None)
        group_id=self.get_argument('group',None)
        remark=self.get_argument('remark',None)

        
        if all([name,host,port,username,password]):
            if server_id:#do update
                #server=get_server(server_id)
                #server_list.remove(server)                
                #server=Server(server_id,name,host,int(port),username,password,remark)                
                #server_list.append(server)
                server=self.db.query(Server).get(int(server_id))
                server.host=host
                server.port=port
                server.username=username
                server.secret=password
                if group_id:
                    group=self.db.query(Group).get(int(group_id))
                server.group=group
                self.db.commit()
            else:
                if group_id:
                    group=self.db.query(Group).get(int(group_id))
                server=Server(name=name,host=host,port=int(port),username=username,secret=password,remark=remark)
                server.group=group
                self.db.add(server)
                self.db.commit()
                #server=Server(uuid.uuid1().hex,name,host,int(port),username,password,remark)                
                #server_list.append(server)
            #save data to pickle
            #save_server_list()
        else:
            self.write('Some argument are not allow empty,please check.!!')

        self.redirect(self.reverse_url('home'))


class WSHandler(tornado.websocket.WebSocketHandler):
    
    clients = dict()
    
    def initialize(self):
        self.command_history=[]
    def get_client(self):
        return self.clients.get(self._id(), None)

    def put_client(self):
        bridge = Bridge(self)
        self.clients[self._id()] = bridge

    def remove_client(self):
        bridge = self.get_client()
        if bridge:
            bridge.destroy()
            del self.clients[self._id()]

    @staticmethod
    def _check_init_param(data):
        return 'server_id' in data  #check_ip(data["server_id"]) and check_port(data["port"])

    @staticmethod
    def _is_init_data(data):
        return data.get_type() == 'init'

    def _id(self):
        return id(self)

    def open(self):
        self.put_client()

    def on_message(self, message):
        bridge = self.get_client()
        gen_log.info(message)
        client_data = ClientData(message)
        if self._is_init_data(client_data):
            if self._check_init_param(client_data.data):
                server_id=client_data.data['server_id']
                db=self.application.db
                user_id=self.get_secure_cookie('user_id')
                if user_id:
                    user=db.query(User).get(int(user_id)) # todo 
                    if not user.is_super:
                        servers=[server for server in user.servers if server.id==int(server_id)]
                        assert len(servers)==1
                        bridge.open(client_data.data,servers[0])
                    else:
                        server=db.query(Server).get(int(server_id))
                        bridge.open(client_data.data,server)
                        gen_log.info('connection established from: %s' % self._id())
                else:
                    gen_log.warning('user is not valid')
                    self.remove_client()
            else:
                self.remove_client()
                gen_log.warning('init param invalid: %s' % client_data.data)
        else:
            if bridge:
                self.command_history.append(client_data.data)
                if self.command_history[-1]=='\r':
                    commmand=''.join(self.command_history)
                    db=self.application.db
                    server=db.query(Server).get(int(client_data.target))#get_server(client_data.target)
                    gen_log.info('server {} run command {}'.format(server.host,commmand))
                    self.command_history.clear()
                bridge.trans_forward(client_data.data)

    def on_close(self):
        self.remove_client()
        gen_log.info('client close the connection: %s' % self._id())

