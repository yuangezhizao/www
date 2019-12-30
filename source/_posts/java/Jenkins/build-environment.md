---
title: 腾讯云开发者实验室（beta）——《Jenkins 环境搭建》
date: 2017-8-22 13:57:22
tags:
  - Jenkins
  - java
count: 1
os: 0
os_1: 10.0.15063 Pro
browser: 0
browser_1: 61.0.3153.0 Dev
place: 家
key: 19
---
    持续集成
<!-- more -->
## 0x00.前言
![](https://i1.yuangezhizao.cn/Win-10/20170822135216.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20170822135949.jpg!webp)
## 0x01.引用
### 1.0 安装`Jenkins`
### 1.1 `Jenkins`简介
`Jenkins`是一个开源软件项目，是基于`Java`开发的一种持续集成工具，用于监控持续重复的工作，旨在提供一个开放易用的软件平台，使软件的持续集成变成可能。
![](https://i1.yuangezhizao.cn/Win-10/20170822140043.jpg!webp)
### 1.2 `Java`安装
首先我们需要准备`Java`环境，使用下面命令来安装`Java`：
`yum -y install java-1.8.0-openjdk-devel`
![](https://i1.yuangezhizao.cn/Win-10/20170822140523.jpg!webp)

### 1.3 `Jenkins`安装
为了使用`Jenkins`仓库，我们要执行以下命令：
`sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo`
`sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key`
如果您以前从`Jenkins`导入过`key`，那么`rpm --import`将失败，因为您已经有一个`key`。请忽略，继续下面步骤。
安装
接着我们可以使用`yum`安装`Jenkins`：
`yum -y install jenkins`
![](https://i1.yuangezhizao.cn/Win-10/20170822141145.jpg!webp)

### 2.0 启动`Jenkins`
### 2.1 启动
启动`Jenkins`并设置为开机启动：
`systemctl start jenkins.service`
`chkconfig jenkins on`
![](https://i1.yuangezhizao.cn/Win-10/20170822141316.jpg!webp)
### 2.2 测试访问
`Jenkins`默认运行在`8080`端口。
稍等片刻，打开`http://119.29.23.67:8080`测试访问。
![](https://i1.yuangezhizao.cn/Win-10/20170822141355.jpg!webp)

### 3.0 进入`Jenkins`
### 3.1 管理员密码
登入`Jenkins`需要输入管理员密码，按照提示，我们使用以下命令查看初始密码：
`cat /var/lib/jenkins/secrets/initialAdminPassword`
复制密码，填入，进入`Jenkins`。
![](https://i1.yuangezhizao.cn/Win-10/20170822141632.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20170822141829.jpg!webp)
### 3.2 定制`Jenkins`
我们选择默认的`install suggested plugins`来安装插件。
![](https://i1.yuangezhizao.cn/Win-10/20170822141924.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20170822142031.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20170822142242.jpg!webp)
### 3.3 创建用户
请填入相应信息创建用户，然后即可登入`Jenkins`的世界。
![](https://i1.yuangezhizao.cn/Win-10/20170822142324.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20170822142456.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20170822142602.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20170822142640.jpg!webp)

## 0x02.后记
![](https://i1.yuangezhizao.cn/Win-10/20170822142657.jpg!webp)
