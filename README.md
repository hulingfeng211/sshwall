# sshwall
> `sshwall`是一个简易的实现`linux ssh`堡垒机的应用，实现了如下功能：
* 可以通过浏览器模拟`ssh`连接到远程服务器
* 根据不同用户授权不同的服务器
* 对应用服务器进行分组


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



