---
title: 腾讯云开发者实验室（beta）——《搭建 Docker 环境》
date: 2017-8-23 12:10:15
tags:
  - Docker
  - go
count: 1
os: 0
os_1: 10.0.15063 Pro
browser: 0
browser_1: 61.0.3153.0 Dev
place: 家
key: 23
gitment: true
---
    emmm……
<!-- more -->
## 0x00.前言
![](https://i1.yuangezhizao.cn/Win-10/20170823121055.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20170823121138.jpg!webp)
## 0x01.引用
### 1.0 安装与配置`Docker`
### 1.1 安装`Docker`
`Docker`软件包已经包括在默认的`CentOS-Extras`软件源里。因此想要安装`docker`，只需要运行下面的`yum`命令：
`yum install docker-io -y`
直接`yum`安装，安装成功后查看版本
`docker -v`
启动`docker`
`service docker start`
设置开机启动
`chkconfig docker on`
![](https://i1.yuangezhizao.cn/Win-10/20170823121641.jpg!webp)

### 1.2 配置`Docker`
因为国内访问`Docker Hub`较慢, 可以使用腾讯云提供的国内镜像源, 加速访问`Docker Hub`
依次执行以下命令
`echo "OPTIONS='--registry-mirror=https://mirror.ccs.tencentyun.com'" >> /etc/sysconfig/docker`
`systemctl daemon-reload`
`service docker restart`
![](https://i1.yuangezhizao.cn/Win-10/20170823122515.jpg!webp)

### 2.0 下载镜像
下载一个官方的`CentOS`镜像到本地
`docker pull centos`
下载好的镜像就会出现在镜像列表里
`docker images`
![](https://i1.yuangezhizao.cn/Win-10/20170823122656.jpg!webp)

### 2.1 运行容器
这时我们可以在刚才下载的`CentOS`镜像生成的容器内操作了。
生成一个`centos`镜像为模板的容器并使用`bash shell`
`docker run -it centos /bin/bash`
这个时候可以看到命令行的前端已经变成了`[root@(一串 hash Id)]`的形式, 这说明我们已经成功进入了`CentOS`容器。
在容器内执行任意命令, 不会影响到宿主机, 如下
`mkdir -p /data/simple_docker`
可以看到`/data`目录下已经创建成功了`simple_docker`文件夹
`ls /data`
退出容器
`exit`
查看宿主机的`/data`目录, 并没有`simple_docker`文件夹, 说明容器内的操作不会影响到宿主机
`ls /data`
![](https://i1.yuangezhizao.cn/Win-10/20170823122918.jpg!webp)

### 2.2 保存容器
查看所有的容器信息，能获取容器的`id`
`docker ps -a`
然后执行如下命令（请自行将 -m 后面的信息改成自己的容器的信息），保存镜像：
`docker commit -m="备注" 你的CONTAINER_ID 你的IMAGE`
已完成，下一步
![](https://i1.yuangezhizao.cn/Win-10/20170823123222.jpg!webp)

## 0x02.后记
emmm……`htop`爱好者
![](https://i1.yuangezhizao.cn/Win-10/20170823123350.jpg!webp)
