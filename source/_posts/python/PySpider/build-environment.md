---
title: 腾讯云开发者实验室（beta）——《搭建 PySpider 爬虫服务》
date: 2017-8-22 14:52:44
tags:
  - PySpider
  - python
count: 1
os: 0
os_1: 10.0.15063 Pro
browser: 0
browser_1: 61.0.3153.0 Dev
place: 家
key: 20
---
    emmm……
<!-- more -->
## 0x00.前言
![](https://i1.yuangezhizao.cn/Win-10/20170822145129.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20170822145419.jpg!webp)
## 0x01.引用
#### 1.0 环境准备
#### 1.1 前置环境部署
在开始部署前，我们需要做一些前置准备（该步骤可选，但为了部署的稳定性，推荐执行）。
`yum`更新（该步骤耗时可能较长（5~10min），请耐心等待）
` yum update -y`
安装开发编译工具
`yum install gcc gcc-c++ -y`
安装依赖库
`yum install python-pip python-devel python-distribute libxml2 libxml2-devel python-lxml libxslt libxslt-devel`
`openssl openssl-devel -y`
升级`pip`
`pip install --upgrade pip`
![](https://i1.yuangezhizao.cn/Win-10/20170822150424.jpg!webp)
#### 2.0 部署 mariadb
由于`CentOS 7`中`MySQL`数据库已从默认的程序列表中移除，我们使用`mariadb`代替。
#### 2.1 安装 mariadb
`yum install mariadb-server mariadb -y`
![](https://i1.yuangezhizao.cn/Win-10/20170822150532.jpg!webp)

#### 2.2 启动 mariadb 服务
`systemctl start mariadb`
![](https://i1.yuangezhizao.cn/Win-10/20170822150615.jpg!webp)
emmm……
![](https://i1.yuangezhizao.cn/Win-10/20170822151002.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20170822150900.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20170822151025.jpg!webp)

看来是我遇到`bug`了……重试了两次
![](https://i1.yuangezhizao.cn/Win-10/20170822151503.jpg!webp)

不过文章还是要写的，那就直接结束实验看文档吧……
![](https://i1.yuangezhizao.cn/Win-10/20170822151653.jpg!webp)

#### 2.3 设置`root`密码
默认的`root`用户密码为空，你可以使用以下命令来创建`root`用户的密码（该步骤也可以跳过，`password`后的`Password`可以改为任何你希望设置的密码）
`mysqladmin -u root password "Password"`

#### 2.4 检查是否安装成功
现在你可以尝试通过以下命令来连接到`Mysql`服务器（如果您未设置密码，直接使用`mysql`即可）
`mysql -u root -p`
然后输入您刚才设置的密码（ 默认：`Password`），如果一切正常，您应该可以在命令行看到以`MariaDB [(none)]>`或`mysql>`开头的提示了，说明连接成功。
此时输入`SHOW DATABASES;`并回车，应该可以看到类似下面这样的输出，说明一切正常。
```
mysql> SHOW DATABASES;
+----------+
| Database |
+----------+
| mysql    |
| test     |
+----------+
2 rows in set (0.13 sec)
```
完成后，可以通过快捷键`Ctrl+C`或命令行键入`exit`来退出，进入下一步。

#### 3.0 部署`redis`
#### 3.1 下载、解压安装包
下载安装包
`wget http://download.redis.io/redis-stable.tar.gz`
解压安装包
`tar -xzvf redis-stable.tar.gz`
移动解压包到`/usr/local`内
`mv redis-stable /usr/local/redis`
编译安装
`cd /usr/local/redis`
`make`
`make install`
#### 3.2 设置`redis`配置
设置配置文件路径
`mkdir -p /etc/redis`
`cp /usr/local/redis/redis.conf /etc/redis/redis.conf`
修改`/etc/redis/redis.conf`文件的`daemonize`配置项为如下：
`daemonize yes`
#### 3.3 启动`redis`服务
`/usr/local/bin/redis-server /etc/redis/redis.conf`

#### 4.0 部署 pyspider
#### 4.1 安装依赖
`pip install --upgrade chardet`
`easy_install mysql-connector==2.1.3`
`easy_install redis`
#### 4.2 安装`pyspider`
`pip install pyspider`
#### 4.3 配置`pyspider`
首先创建配置目录
`mkdir /etc/pyspider`
然后`/etc/pyspider`目录下创建`pyspider.conf.json`，参考下面的内容。
具体配置的说明文档请参考[官方文档](http://docs.pyspider.org/en/latest/Deployment/#configjson)
示例代码：`/etc/pyspider/pyspider.conf.json`
```
{
  "taskdb": "mysql+taskdb://root:Password@127.0.0.1:3306/taskdb",
  "projectdb": "mysql+projectdb://root:Password@127.0.0.1:3306/projectdb",
  "resultdb": "mysql+resultdb://root:Password@127.0.0.1:3306/resultdb",
  "message_queue": "redis://127.0.0.1:6379/db",
  "webui": {
    "username": "root",
    "password": "Password",
    "need-auth": true
  }
}
```
其中`mysql`配置中的`root`为您`mysql`的用户名， `root:`后面的`Password`为您刚设置的密码。
`webui`配置中的`username`及`password`为您访问`WebUI`时候需要的用户名，你也可以不设置用户名密码，直接将`need-auth`设为 `false`即可。
#### 4.4 启动服务
`pyspider -c /etc/pyspider/pyspider.conf.json`
如果一切正常，现在访问`http://<您的 CVM IP 地址>:5000`，您应该可以看到`pyspider dashboard`的首页了。
服务能够正常启动后，我们需要让它能够在后台运行，您可以通过以下命令让服务在后台运行
`nohup pyspider -c /etc/pyspider/pyspider.conf.json &`
也可以使用官方推荐的[Supervisor](http://supervisord.org/) 来启动，这里就不详细介绍了，具体用法可以参考`Supervisor`的文档
