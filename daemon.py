# -*- coding:utf-8 -*-

import paramiko
from paramiko.ssh_exception import AuthenticationException, SSHException
from tornado.websocket import WebSocketClosedError
from tornado.gen import IOLoop
from tornado.log import gen_log
import functools
import socket
import errno
from tornado.log import gen_log
from tornado.concurrent import TracebackFuture
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

MAX_DATA_BUFFER = 1024 * 1024


class Bridge(object):
    '''
    websocket与ssh的其桥接对象
    '''

    def __init__(self, websocket):
        self._websocket = websocket
        self._shell = None
        self._id = 0
        self.ssh = paramiko.SSHClient()
        self._trans_back=None

    @property
    def id(self):
        return self._id

    @property
    def websocket(self):
        return self._websocket

    @property
    def shell(self):
        return self._shell

    def privaterKey(self, _PRIVATE_KEY, _PRIVATE_KEY_PWD):
        try:
            pkey = paramiko.RSAKey.from_private_key(
                StringIO(_PRIVATE_KEY), _PRIVATE_KEY_PWD)
        except paramiko.SSHException:
            pkey = paramiko.DSSKey.from_private_key(
                StringIO(_PRIVATE_KEY), _PRIVATE_KEY_PWD)
        return pkey

    def isPassword(self, data):
        return data.get("ispwd", True)

    def open(self, data={}, server=None):
        self.ssh.set_missing_host_key_policy(
            paramiko.AutoAddPolicy())
        try:
            if server:  # self.isPassword(server):
                self.ssh.connect(
                    hostname=server.host,
                    port=int(server.port),
                    username=server.username,
                    password=server.secret,
                )
            # 暂不支持privatekey的方式进行登录
            '''else:
                self.ssh.connect(
                    hostname=server.host,
                    port=int(server.port),
                    username=server.username,
                    pkey=self.privaterKey(server.secret, None)
                )'''

        except AuthenticationException:
            raise Exception("auth failed user:%s ,passwd:%s" %
                            (server.username, server.secret))
        except SSHException:
            raise Exception("could not connect to host:%s:%s" %
                            (server.hostname, server.port))

        self.establish(data)

    def establish(self, data, term="xterm"):
        self._shell = self.ssh.invoke_shell(
            term, width=int(data.get('width', 80)), height=int(data.get('height', 24)))
        self._shell.setblocking(0)
        self._id = self._shell.fileno()
        self._trans_back = self.trans_back()
        next(self._trans_back) #激活websocket传输数据的协程
        
        def trans_data_ready(shell, fd, events):
            '''
            接收IOLoop的事件回调，当ssh server有数据需要传输的时候回调此方法
            '''
            try:
                gen_log.info('connection_read')
                data = shell.recv(MAX_DATA_BUFFER)
                # todo send data to client directly
                self._trans_back.send(data)
            except socket.error as e:
                if e.args and e.args[0] not in (errno.EWOULDBLOCK, errno.EAGAIN):
                    gen_log.error('errno.EWOULDBLOCK, errno.EAGAIN')
                    self.destroy()
                if isinstance(e, socket.timeout):
                    gen_log.error('socket.timeout')
                    self.destroy()

        callback = functools.partial(trans_data_ready, self.shell)
        io_loop = IOLoop.current()
        io_loop.add_handler(self._shell.fileno(),callback, io_loop.READ)

    def trans_forward(self, data=""):
        '''
        将数据通过ssh shell发送给后台的ssh server
        '''
        if self._shell:
            self._shell.send(data)

    def trans_back(self):
        '''
        传输ssh数据到浏览器的协成，通过websocket对象将数据传给浏览器
        '''
        connected = True
        while connected:
            result = yield
            if self._websocket:
                try:
                    gen_log.info('trans_back')
                    self._websocket.write_message(result)
                except WebSocketClosedError:
                    gen_log.error('WebSocketClosedError')
                    connected = False
                if result.strip() == 'logout':
                    gen_log.error('logout')
                    connected = False
        self.destroy()

    def destroy(self):
        '''
        销毁桥接对象持有的资源
        '''
        self._websocket.close()
        if self._shell:
            IOLoop.current().remove_handler(self._shell.fileno())
        self.ssh.close()
