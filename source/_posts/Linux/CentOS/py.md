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

## 0x02.编译安装[python380](https://www.python.org/downloads/release/python-380/)环境
1. 查看现有位置
``` bash
[root@py ~]# whereis python
python: /usr/bin/python /usr/bin/python2.7 /usr/lib/python2.7 /usr/lib64/python2.7 /etc/python /usr/include/python2.7 /usr/share/man/man1/python.1.gz
```
2. 安装编译工具
``` bash
yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc make libffi-devel
```
> 这里面有一个包很关键`libffi-devel`，因为只有`3.7`才会用到这个包，如果不安装这个包的话，在`make`阶段会出现如下的报错：`# ModuleNotFoundError: No module named '_ctypes'`

3. 下载源码包
``` bash
wget --no-check-certificate https://www.python.org/ftp/python/3.8.0/Python-3.8.0.tar.xz
```
![下载卡爆，proxy 中转爽到！](https://i1.yuangezhizao.cn/Win-10/20191107224750.jpg!webp)

4. 解压
``` bash
tar xvJf Python-3.8.0.tar.xz 
cd Python-3.8.0
```
5. 编译
``` bash
sudo ./configure --prefix=/usr/local/python3
sudo make && make install
```
![全新路径](https://i1.yuangezhizao.cn/Win-10/20191107225633.jpg!webp)

6. ~~修改默认为`Python 3`~~
~~将`/usr/bin`中的`python`备份，然后创建`python3`的软链接，这样默认的`Python`版本就替换为`Python 3`了~~
``` bash
[root@py ~]# sudo mv /usr/bin/python /usr/bin/python.bak
[root@py ~]# sudo ln -s /usr/local/python3/bin/python3 /usr/bin/python
[root@py ~]# python
Python 3.8.0 (default, Nov  7 2019, 22:54:02) 
[GCC 4.8.5 20150623 (Red Hat 4.8.5-39)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> exit()
```
~~这样做在使用`yum`的时候会出现`bug`，需要自行修复……~~
```
[root@py bin]# cd ~
[root@py ~]# yum update -y
  File "/usr/bin/yum", line 30
    except KeyboardInterrupt, e:
                            ^
SyntaxError: invalid syntax
[root@py ~]# 
```
7. 创建软链接（`python3`&`pip3`）
``` bash
[root@txy ~]# sudo ln -s /usr/local/python3/bin/python3 /usr/bin/python3
[root@txy ~]# sudo ln -s /usr/local/python3/bin/pip3.8 /usr/bin/pip3

[root@txy ~]# python -V
Python 2.7.5
[root@txy ~]# python2 -V
Python 2.7.5
[root@txy ~]# python3 -V
Python 3.8.0

[root@py ~]# pip -V
-bash: pip: command not found
[root@py ~]# pip2 -V
-bash: pip2: command not found
[root@py ~]# pip3 -V
pip 19.3.1 from /usr/local/python3/lib/python3.8/site-packages/pip (python 3.8)
```
> 这样就可以通过`python`/`python2`命令使用`Python`，`python3`来使用`Python 3`

8. 升级`pip3`
``` bash
[root@py Python-3.8.0]# cd /usr/local/python3/bin
[root@py bin]# ./pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U
Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple
Collecting pip
  Downloading https://pypi.tuna.tsinghua.edu.cn/packages/00/b6/9cfa56b4081ad13874b0c6f96af8ce16cfbc1cb06bedf8e9164ce5551ec1/pip-19.3.1-py2.py3-none-any.whl (1.4MB)
     |████████████████████████████████| 1.4MB 1.0MB/s 
Installing collected packages: pip
  Found existing installation: pip 19.2.3
    Uninstalling pip-19.2.3:
      Successfully uninstalled pip-19.2.3
Successfully installed pip-19.3.1
[root@py bin]# ./pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
Writing to /root/.config/pip/pip.conf
```

## 0x03.`git`配置
``` bash
git config --global user.name "yuangezhizao-serveraccount"
git config --global user.email yuangezhizao@gmail.com
git commit --amend --reset-author

git config --global credential.helper store
```

## 0x04.`NTP`配置
> 网络时间协议`（Network Time Protocol，NTP）`，用于同步网络中各个计算机的时间的协议。其用途是将计算机的时钟同步到世界协调时`UTC`。在`NTP`设计时考虑到了各种网络延迟，当您通过公共网络同步时，误差可以降低到`10`毫秒以内；当您通过本地网络同步时，误差可以降低到`1`毫秒
腾讯云提供了内网`NTP`服务器供腾讯云内网设备使用，对于非腾讯云设备，可以使用腾讯云提供的公网`NTP`服务器

> `NTPD（Network Time Protocol daemon）`是`Linux`操作系统的一个守护进程，用于校正本地系统与时钟源服务器之前的时间，完整的实现了`NTP`协议。`NTPD`与`NTPDate`的区别是`NTPD`是步进式的逐渐校正时间，不会出现时间跳变，而`NTPDate`是断点更新

![公网好评](https://i1.yuangezhizao.cn/Win-10/20191107231606.jpg!webp)
安装`NTPD`
`yum -y install ntp`
配置`NTP`
`vim /etc/ntp.conf`
![修改](https://i1.yuangezhizao.cn/Win-10/20191107231814.jpg!webp)
``` bash
# Use public servers from the pool.ntp.org project.
# Please consider joining the pool (http://www.pool.ntp.org/join.html).
# server 0.centos.pool.ntp.org iburst
# server 1.centos.pool.ntp.org iburst
# server 2.centos.pool.ntp.org iburst
# server 3.centos.pool.ntp.org iburst
server time1.cloud.tencent.com
server time2.cloud.tencent.com
server time3.cloud.tencent.com
server time4.cloud.tencent.com
server time5.cloud.tencent.com
```
运行`NTPD`并自启
``` bash
[root@py ~]# rpm -qa | grep ntp
ntpdate-4.2.6p5-29.el7.centos.x86_64
ntp-4.2.6p5-29.el7.centos.x86_64
fontpackages-filesystem-1.44-8.el7.noarch
[root@py ~]# systemctl restart ntpd.service
[root@py ~]# systemctl enable ntpd.service
Created symlink from /etc/systemd/system/multi-user.target.wants/ntpd.service to /usr/lib/systemd/system/ntpd.service.
```
查看`NTP`服务端口`UDP 123`端口是否被正常监听
``` bash
[root@py ~]# netstat -nupl
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
udp        0      0 0.0.0.0:68              0.0.0.0:*                           1069/dhclient       
udp        0      0 192.168.25.42:123       0.0.0.0:*                           77501/ntpd          
udp        0      0 127.0.0.1:123           0.0.0.0:*                           77501/ntpd          
udp        0      0 0.0.0.0:123             0.0.0.0:*                           77501/ntpd          
udp6       0      0 240e:<rm>::123 :::*                                77501/ntpd          
udp6       0      0 fe80::<rm>:123 :::*                                77501/ntpd          
udp6       0      0 240e:<rm>::123 :::*                                77501/ntpd          
udp6       0      0 ::1:123                 :::*                                77501/ntpd          
udp6       0      0 :::123                  :::*                                77501/ntpd          
udp6       0      0 fe80::<rm>:546 :::*                                1595/dhclient       
```
查看`NTPD`状态
``` bash
[root@py ~]# service ntpd status
Redirecting to /bin/systemctl status ntpd.service
● ntpd.service - Network Time Service
   Loaded: loaded (/usr/lib/systemd/system/ntpd.service; disabled; vendor preset: disabled)
   Active: active (running) since Thu 2019-11-07 23:18:57 CST; 16s ago
  Process: 77500 ExecStart=/usr/sbin/ntpd -u ntp:ntp $OPTIONS (code=exited, status=0/SUCCESS)
 Main PID: 77501 (ntpd)
   CGroup: /system.slice/ntpd.service
           └─77501 /usr/sbin/ntpd -u ntp:ntp -g

Nov 07 23:18:57 py.yuangezhizao.cn ntpd[77501]: Listen normally on 2 lo 127.0.0.1 UDP 123
Nov 07 23:18:57 py.yuangezhizao.cn ntpd[77501]: Listen normally on 3 ens32 192.168.25.42 UDP 123
Nov 07 23:18:57 py.yuangezhizao.cn ntpd[77501]: Listen normally on 4 lo ::1 UDP 123
Nov 07 23:18:57 py.yuangezhizao.cn ntpd[77501]: Listen normally on 5 ens32 240e:<rm>:...123
Nov 07 23:18:57 py.yuangezhizao.cn ntpd[77501]: Listen normally on 6 ens32 fe80::<rm>...123
Nov 07 23:18:57 py.yuangezhizao.cn ntpd[77501]: Listen normally on 7 ens32 240e:<rm>...123
Nov 07 23:18:57 py.yuangezhizao.cn ntpd[77501]: Listening on routing socket on fd #24 for interface...tes
Nov 07 23:18:58 py.yuangezhizao.cn ntpd[77501]: 0.0.0.0 c016 06 restart
Nov 07 23:18:58 py.yuangezhizao.cn ntpd[77501]: 0.0.0.0 c012 02 freq_set kernel 0.000 PPM
Nov 07 23:18:58 py.yuangezhizao.cn ntpd[77501]: 0.0.0.0 c011 01 freq_not_set
Hint: Some lines were ellipsized, use -l to show in full.
```
查看`NTP`是否正常启动以及是否配置到正确的`NTP`时钟源服务器：输出当前`NTP`时钟源服务器的`IP`地址，此`IP`地址应为上述配置的`NTP`时钟源服务器的`IP`地址
``` bash
[root@py ~]# ntpstat
unsynchronised
  time server re-starting
   polling server every 8 s
```
获取更详细的`NTP`服务信息
``` bash
[root@py ~]# ntpq -p
     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
 139.199.215.251 100.122.36.4     2 u   32   64    1   57.452   -1.940   0.000
 111.230.189.174 100.122.36.196   2 u   32   64    1   59.803   -1.716   0.000
 139.199.214.202 100.122.36.4     2 u   31   64    1   57.946    0.590   0.000
 134.175.254.134 100.122.36.4     2 u   31   64    1   57.897   -2.392   0.000
 134.175.253.104 100.122.36.4     2 u   32   64    1   59.239   -0.167   0.000
```
过了一会儿重新来看
``` bash
[root@py ~]# ntpstat
synchronised to NTP server (134.175.254.134) at stratum 3
   time correct to within 45 ms
   polling server every 64 s
[root@py ~]# ntpq -p
     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
+139.199.215.251 100.122.36.196   2 u   71  128  377   56.945   -1.334   0.556
*111.230.189.174 100.122.36.196   2 u   53  128  377   59.046    1.035   1.348
-139.199.214.202 100.122.36.4     2 u   52  128  377   57.424    3.607   0.707
-134.175.254.134 100.122.36.196   2 u  193  128  376   57.452    2.038   0.768
+134.175.253.104 100.122.36.196   2 u  126  128  377   58.659   -0.204   0.623
```
然后顺便去看了眼`txy`机子
``` bash
[root@txy bt]# ntpq -p
     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
*10.237.208.123  100.122.36.196   2 u  861 1024  377   32.771    0.215   0.555
```

## 0x04.引用
> [ifconfig命令不存在command not found](https://web.archive.org/web/20191028144703/http://web.archive.org/screenshot/https://blog.csdn.net/dong_alex/article/details/80873733)
[Linux 实例设置 NTP 服务](https://web.archive.org/web/20191107152042/http://web.archive.org/screenshot/https://cloud.tencent.com/document/product/213/30393)

未完待续……