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
    def __init__(self, websocket):
        self._websocket = websocket
        self._shell = None
        self._id = 0
        self.ssh = paramiko.SSHClient()

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
            # server_id=data['server_id']
            # server=get_server(server_id)
            # server['ispwd']=True
            if server:  # self.isPassword(server):
                self.ssh.connect(
                    hostname=server.host,
                    port=int(server.port),
                    username=server.username,
                    password=server.secret,
                )

            else:
                self.ssh.connect(
                    hostname=server.host,
                    port=int(server.port),
                    username=server.username,
                    pkey=self.privaterKey(server.secret, None)
                )

        except AuthenticationException:
            raise Exception("auth failed user:%s ,passwd:%s" %
                            (server.username, server.secret))
        except SSHException:
            raise Exception("could not connect to host:%s:%s" %
                            (server.hostname, server.port))

        self.establish(data)

    def establish(self, data,term="xterm"):
        self._shell = self.ssh.invoke_shell(
            term, width=int(data.get('width',80)), height=int(data.get('height',24)))
        self._shell.setblocking(0)
        self._id = self._shell.fileno()
        # IOLoop.instance().register(self)
        # IOLoop.instance().add_future(self.trans_back())
        self._trans_back = self.trans_back()
        next(self._trans_back)
        callback = functools.partial(self.connection_ready, self.shell)
        io_loop=IOLoop.current()
        io_loop.add_handler(self._shell.fileno(),
                            callback, io_loop.READ)
    """
    def _read_remote_result(self,*args,**kwargs):
        future=TracebackFuture()
        callback=kwargs.get('callback',None)
        if callback and callable(callback):
            IOLoop.current().add_future(future,lambda future:callback(future.result()))
        
        pass
    """

    def connection_ready(self, shell, fd, events):

        # while True:
        try:
                # try:
                #                data = self.bridges[fd].shell.recv(MAX_DATA_BUFFER)
                #            except socket.error as e:
                #                if isinstance(e, socket.timeout):
                #                    break
                #                else:
                #                    self.close(fd)
            gen_log.info('connection_read')
            data = self._shell.recv(MAX_DATA_BUFFER)
            self._trans_back.send(data) # todo send data to client directly
        except socket.error as e:
            if e.args and e.args[0] not in (errno.EWOULDBLOCK, errno.EAGAIN):
                gen_log.error('errno.EWOULDBLOCK, errno.EAGAIN')
                self.destroy()
            if isinstance(e, socket.timeout):
                gen_log.error('socket.timeout')
                self.destroy()
            # else:
            #    gen_log.info('connection_read3')
        # self.destroy()

    def trans_forward(self, data=""):
        if self._shell:
            self._shell.send(data)

    def trans_back(self):
        # yield self.id
        # print(type(arg1))
        # print(type(arg2))
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
        self._websocket.close()
        if self._shell:
            IOLoop.current().remove_handler(self._shell.fileno())
        self.ssh.close()
