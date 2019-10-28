---
title: PY 云新增 CentOS 7.7 64 位
date: 2019-10-28 23:13:25
tags:
  - CentOS 
count: 1
os: 0
os_1: 10.0.17763.832 2019-LTSC
browser: 0
browser_1: 74.0.3729.169 Stable
place: 新家
key: 60
---
    每次的从头配置是最烦的（然而已经习惯了都
<!-- more -->
## 0x00.前言
> 还记得“续……”吗？
```
[root@localhost ~]# rpm -q centos-release
centos-release-7-7.1908.0.el7.centos.x86_64
```
## 0x01.配置
### 1. 查看`IP`
搁这`VNC`？里干一件事情就足够了，就再也不用进来了（`grub`除外
```
yum install net-tools -y
```
意外发现了镜像地址是`neusoft`，还真是最近的`hhh`
![记下 ipv4 地址](https://i1.yuangezhizao.cn/Win-10/20191028225005.png!webp)

然后就可以回到日常使用的`XShell`了（妙
注：还不确定设定静态`ip`会不会有影响，所以就先不设了……
```
[root@localhost ~]# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: ens32: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:0c:29:28:a6:ad brd ff:ff:ff:ff:ff:ff
    inet 192.168.25.42/24 brd 192.168.25.255 scope global noprefixroute dynamic ens32
       valid_lft 603442sec preferred_lft 603442sec
    inet6 <rm> scope global noprefixroute dynamic 
       valid_lft 5844sec preferred_lft 2244sec
    inet6 <rm> scope global noprefixroute dynamic 
       valid_lft 6964sec preferred_lft 3364sec
    inet6 <rm> scope link noprefixroute 
       valid_lft forever preferred_lft forever
[root@localhost ~]# cat /etc/sysconfig/network-scripts/ifcfg-ens32
TYPE="Ethernet"
PROXY_METHOD="none"
BROWSER_ONLY="no"
BOOTPROTO="dhcp"
DEFROUTE="yes"
IPV4_FAILURE_FATAL="no"
IPV6INIT="yes"
IPV6_AUTOCONF="yes"
IPV6_DEFROUTE="yes"
IPV6_FAILURE_FATAL="no"
IPV6_ADDR_GEN_MODE="stable-privacy"
NAME="ens32"
UUID="9e2d678d-9e9b-48b3-a8d5-9ea7baa81c39"
DEVICE="ens32"
ONBOOT="yes"
[root@localhost ~]# 
```
就先`BOOTPROTO="dhcp"`好了
### 2. 修改主机名
```
[root@localhost ~]# hostnamectl set-hostname py.yuangezhizao.cn
[root@localhost ~]# cat /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
[root@localhost ~]# vi /etc/hosts
[root@localhost ~]# cat /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4 py.yuangezhizao.cn py.yuangezhizao.cn
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6 py.yuangezhizao.cn py.yuangezhizao.cn
[root@localhost ~]# 
```
### 3. 安装常用软件
`yum update -y`
`yum install vim git wget -y`

`yum install epel-release -y`
`yum install htop axel -y`
## 0x03.引用
> [ifconfig命令不存在command not found](https://web.archive.org/web/20191028144703/http://web.archive.org/screenshot/https://blog.csdn.net/dong_alex/article/details/80873733)

未完待续……