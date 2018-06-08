---
title: VMware 安装 Ubuntu Desktop 16.04 x64
date: 2018-2-24 15:00:31
tags:
  - Ubuntu
  - VMware
count: 1
os: 0
os_1: 10.0.14393 2016-LTSB
browser: 0
browser_1: 64.0.3282.140 Stable
place: 家
key: 33
---
    多图预警
<!-- more -->
## 0x00.安装

## 0x01.移除`Amazon`
`sudo apt-get remove unity-webapps-common`

## 0x02.卸载`libreoffice`
`sudo apt-get remove libreoffice-common`
`sudo apt autoremove`

## 0x06.安装[Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
卸载旧版本
`sudo apt-get remove docker docker-engine docker.io`
更新`apt`包
`sudo apt-get update`
安装`https`支持包
```
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
```
添加`Docker`官方`GPG`密钥
`curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -`
```
$ sudo apt-key fingerprint 0EBFCD88

pub   4096R/0EBFCD88 2017-02-22
      Key fingerprint = 9DC8 5822 9FC7 DD38 854A  E2D8 8D81 803C 0EBF CD88
uid                  Docker Release (CE deb) <docker@docker.com>
sub   4096R/F273FCD8 2017-02-22
```
添加稳定版的仓库源（amd64）
```
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
```
安装`DOCKER CE`
`sudo apt-get update`
`sudo apt-get install docker-ce`
`sudo systemctl enable docker`
`sudo systemctl start docker`
配置加速器
`curl -sSL https://get.daocloud.io/daotools/set_mirror.sh | sh -s http://e6d6fb48.m.daocloud.io`
测试，需要`sudo`
`sudo docker run hello-world`
建立`docker`用户组
`sudo groupadd docker`
`sudo usermod -aG docker $(whoami)`
重新登录，这样无需`sudo`
`docker run hello-world`