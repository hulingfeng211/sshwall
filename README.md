# sshwall
> `sshwall`是一个简易的实现`linux ssh`堡垒机的应用，实现了如下功能：
* 可以通过浏览器模拟`ssh`连接到远程服务器
* 超级管理员可以根据不同用户授权不同的服务器
* 超级管理员可以对应用服务器进行分组管理和授权

> 使用场景如下:

* 当某些服务器需要临时开放给供应商进行配置而不希望提供密码给对方的时候可以临时开放服务给供应商
* 当内网的服务器不希望暴露`22`端口到外网又希望管理员能够从外网能`ssh`到内网的服务器时


### 安装方法

```
git clone https://github.com/hulingfeng211/sshwall.git
cd sshwall

```

* 安装依赖的模块

```
    pip3 install -r requirements.txt
```

* 安装依赖的css和js模块 

```
cd static 
npm install 
```

* 初始化管理员

```
cd sshwall 
python3 app.py --init=true 
```
**根据提示操作创建管理员帐号**

* 启动服务 

```
python3 app.py --logging=debug 

```

### 效果

![login](https://github.com/hulingfeng211/sshwall/blob/master/static/assets/login.png)
**用户登录**

![服务器列表](https://github.com/hulingfeng211/sshwall/blob/master/static/assets/serverlist.png)
**服务器列表**
![login](https://github.com/hulingfeng211/sshwall/blob/master/static/assets/add_server.png)
**添加服务器**
![login](https://github.com/hulingfeng211/sshwall/blob/master/static/assets/add_user.png)
**添加用户**
![login](https://github.com/hulingfeng211/sshwall/blob/master/static/assets/webssh.png)
**ssh 连接**