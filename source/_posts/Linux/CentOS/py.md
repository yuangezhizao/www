---
title: PY 云新增 CentOS 7.7 64 位
date: 2019-10-28 23:13:25
tags:
  - CentOS 
count: 5
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
``` bash
[root@py ~]# rpm -q centos-release
centos-release-7-9.2009.1.el7.centos.x86_64
```

## 0x01.配置
### 1. 查看`IP`
搁这`VNC`？里干一件事情就足够了，就再也不用进来了（`grub`除外
``` bash
[root@localhost ~]# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:0c:29:b6:21:03 brd ff:ff:ff:ff:ff:ff
    inet 192.168.25.7/24 brd 192.168.25.255 scope global noprefixroute ens192
       valid_lft forever preferred_lft forever
    inet6 240e:<rm>/128 scope global noprefixroute dynamic 
       valid_lft 5419sec preferred_lft 1819sec
    inet6 240e:<rm>/64 scope global noprefixroute dynamic 
       valid_lft 7086sec preferred_lft 3486sec
    inet6 fe80::<rm>/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
[root@localhost ~]# cat /etc/sysconfig/network-scripts/ifcfg-ens192
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
NAME="ens192"
UUID="6bae1cb0-202e-4e92-a829-7df7c1f988b9"
DEVICE="ens192"
ONBOOT="yes"
```
然后就可以回到日常使用的`XShell`了（妙
注：还不确定设定静态`ip`会不会有影响~~（其实是不会），所以就先不设了……~~这么简单的配置怎么好意思说不会呢？
`2020-4-4 16:52:59`：配置如下
``` bash
[root@py ~]# cat /etc/sysconfig/network-scripts/ifcfg-ens192 
TYPE="Ethernet"
PROXY_METHOD="none"
BROWSER_ONLY="no"
BOOTPROTO="static"
DEFROUTE="yes"
IPV4_FAILURE_FATAL="no"
IPV6INIT="yes"
IPV6_AUTOCONF="yes"
IPV6_DEFROUTE="yes"
IPV6_FAILURE_FATAL="no"
IPV6_ADDR_GEN_MODE="stable-privacy"
NAME="ens192"
UUID="6bae1cb0-202e-4e92-a829-7df7c1f988b9"
DEVICE="ens192"
ONBOOT="yes"
IPADDR=192.168.25.237
GATEWAY=192.168.25.254
DNS1=192.168.25.30
```

### 2. 修改主机名
``` bash
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
``` bash
yum update -y
yum install vim git wget screen -y

yum install epel-release -y
yum install htop axel -y
```

## 0x02.编译安装[python382](https://www.python.org/downloads/release/python-382/)环境
同[编译安装python382环境](./server.html#0x04-编译安装python382环境)

## 0x03.`git`配置
``` bash
git config --global user.name "yuangezhizao-serveraccount"
git config --global user.email yuangezhizao@gmail.com
git commit --amend --reset-author

git config --global credential.helper store
```

## 0x04.`NTP`[配置](https://web.archive.org/web/20191107152042/https://cloud.tencent.com/document/product/213/30393)
![NTPD](https://i1.yuangezhizao.cn/Win-10/20200619201038.jpg!webp)

> 网络时间协议`（Network Time Protocol，NTP）`，用于同步网络中各个计算机的时间的协议。其用途是将计算机的时钟同步到世界协调时`UTC`。在`NTP`设计时考虑到了各种网络延迟，当您通过公共网络同步时，误差可以降低到`10`毫秒以内；当您通过本地网络同步时，误差可以降低到`1`毫秒
腾讯云提供了内网`NTP`服务器供腾讯云内网设备使用，对于非腾讯云设备，可以使用腾讯云提供的公网`NTP`服务器

> `NTPD（Network Time Protocol daemon）`是`Linux`操作系统的一个守护进程，用于校正本地系统与时钟源服务器之前的时间，完整的实现了`NTP`协议。`NTPD`与`NTPDate`的区别是`NTPD`是步进式的逐渐校正时间，不会出现时间跳变，而`NTPDate`是断点更新

![公网好评](https://i1.yuangezhizao.cn/Win-10/20191107231606.jpg!webp)
安装`NTPD`
`yum -y install ntp`
配置`NTP`
`vim /etc/ntp.conf`
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

![修改](https://i1.yuangezhizao.cn/Win-10/20200404182849.jpg!webp)

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
udp        0      0 192.168.25.7:123        0.0.0.0:*                           9836/ntpd           
udp        0      0 127.0.0.1:123           0.0.0.0:*                           9836/ntpd           
udp        0      0 0.0.0.0:123             0.0.0.0:*                           9836/ntpd           
udp6       0      0 fe80::<rm>:123 :::*                                         9836/ntpd           
udp6       0      0 240e:<rm>::123 :::*                                         9836/ntpd           
udp6       0      0 240e:<rm>::123 :::*                                         9836/ntpd           
udp6       0      0 ::1:123                 :::*                                9836/ntpd           
udp6       0      0 :::123                  :::*                                9836/ntpd           
udp6       0      0 fe80::<rm>:546 :::*                                         2085/dhclient           
```
查看`NTPD`状态
``` bash
[root@py ~]# service ntpd status
Redirecting to /bin/systemctl status ntpd.service
● ntpd.service - Network Time Service
   Loaded: loaded (/usr/lib/systemd/system/ntpd.service; enabled; vendor preset: disabled)
   Active: active (running) since Sat 2020-04-04 18:29:35 CST; 1min 39s ago
 Main PID: 9836 (ntpd)
   CGroup: /system.slice/ntpd.service
           ├─9836 /usr/sbin/ntpd -u ntp:ntp -g
           └─9837 /usr/sbin/ntpd -u ntp:ntp -g

Apr 04 18:29:37 py.yuangezhizao.cn ntpd_intres[9837]: host name not found: time1.cloud.tencent.com
Apr 04 18:29:37 py.yuangezhizao.cn ntpd_intres[9837]: host name not found: time2.cloud.tencent.com
Apr 04 18:29:37 py.yuangezhizao.cn ntpd_intres[9837]: host name not found: time3.cloud.tencent.com
Apr 04 18:29:37 py.yuangezhizao.cn ntpd_intres[9837]: host name not found: time4.cloud.tencent.com
Apr 04 18:29:37 py.yuangezhizao.cn ntpd_intres[9837]: host name not found: time5.cloud.tencent.com
Apr 04 18:30:40 py.yuangezhizao.cn ntpd_intres[9837]: host name not found: time1.cloud.tencent.com
Apr 04 18:30:40 py.yuangezhizao.cn ntpd_intres[9837]: host name not found: time2.cloud.tencent.com
Apr 04 18:30:40 py.yuangezhizao.cn ntpd_intres[9837]: host name not found: time3.cloud.tencent.com
Apr 04 18:30:40 py.yuangezhizao.cn ntpd_intres[9837]: host name not found: time4.cloud.tencent.com
Apr 04 18:30:40 py.yuangezhizao.cn ntpd_intres[9837]: host name not found: time5.cloud.tencent.com
```
草
``` bash
[root@py ~]# service ntpd status
Redirecting to /bin/systemctl status ntpd.service
● ntpd.service - Network Time Service
   Loaded: loaded (/usr/lib/systemd/system/ntpd.service; enabled; vendor preset: disabled)
   Active: active (running) since Sat 2020-04-04 18:34:09 CST; 11s ago
  Process: 9981 ExecStart=/usr/sbin/ntpd -u ntp:ntp $OPTIONS (code=exited, status=0/SUCCESS)
 Main PID: 9982 (ntpd)
   CGroup: /system.slice/ntpd.service
           └─9982 /usr/sbin/ntpd -u ntp:ntp -g

Apr 04 18:34:09 py.yuangezhizao.cn ntpd[9982]: Listen normally on 2 lo 127.0.0.1 UDP 123
Apr 04 18:34:09 py.yuangezhizao.cn ntpd[9982]: Listen normally on 3 ens192 192.168.25.7 UDP 123
Apr 04 18:34:09 py.yuangezhizao.cn ntpd[9982]: Listen normally on 4 lo ::1 UDP 123
Apr 04 18:34:09 py.yuangezhizao.cn ntpd[9982]: Listen normally on 5 ens192 240e:<rm>:f89...123
Apr 04 18:34:09 py.yuangezhizao.cn ntpd[9982]: Listen normally on 6 ens192 240e:<rm>:caa...123
Apr 04 18:34:09 py.yuangezhizao.cn ntpd[9982]: Listen normally on 7 ens192 fe80::<rm>:f...123
Apr 04 18:34:09 py.yuangezhizao.cn ntpd[9982]: Listening on routing socket on fd #24 for interfac...tes
Apr 04 18:34:09 py.yuangezhizao.cn ntpd[9982]: 0.0.0.0 c016 06 restart
Apr 04 18:34:09 py.yuangezhizao.cn ntpd[9982]: 0.0.0.0 c012 02 freq_set kernel 0.000 PPM
Apr 04 18:34:09 py.yuangezhizao.cn ntpd[9982]: 0.0.0.0 c011 01 freq_not_set
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
注：`chrony`与`NTPD`冲突，可能引起`NTPD`开机启动失败
``` bash
[root@py ~]# systemctl is-enabled chronyd.service
enabled
[root@py ~]# systemctl disable chronyd.service
Removed symlink /etc/systemd/system/multi-user.target.wants/chronyd.service.
```

## 0x05.`VMware Tools`
首先安装依赖
``` bash
yum install perl gcc gcc-c++ make cmake kernel kernel-headers kernel-devel net-tools -y
```
然后挂载复制到本地
``` bash
[root@py ~]# mkdir -p /mnt/cdrom
[root@py ~]# mount -t auto /dev/cdrom /mnt/cdrom
mount: /dev/sr0 is write-protected, mounting read-only
[root@py ~]# cp /mnt/cdrom/VMwareTools-10.3.21-14772444.tar.gz ~
[root@py ~]# umount /dev/cdrom
[root@py ~]# tar -zxvf VMwareTools-10.3.21-14772444.tar.gz
[root@py ~]# cd vmware-tools-distrib/
[root@py vmware-tools-distrib]# ll
total 376
drwxr-xr-x.  2 root root     87 Oct  2  2019 bin
drwxr-xr-x.  5 root root     39 Oct  2  2019 caf
drwxr-xr-x.  2 root root     67 Oct  2  2019 doc
drwxr-xr-x.  5 root root   4096 Oct  2  2019 etc
-rw-r--r--.  1 root root 146996 Oct  2  2019 FILES
-rw-r--r--.  1 root root   2538 Oct  2  2019 INSTALL
drwxr-xr-x.  2 root root     95 Oct  2  2019 installer
drwxr-xr-x. 14 root root    181 Oct  2  2019 lib
drwxr-xr-x.  3 root root     21 Oct  2  2019 vgauth
-rwxr-xr-x.  1 root root 227024 Oct  2  2019 vmware-install.pl
```
运行`vmware-install.pl`开始安装

<details><summary>点击此处 ← 查看终端</summary>

``` bash
[root@py vmware-tools-distrib]# ./vmware-install.pl
open-vm-tools packages are available from the OS vendor and VMware recommends 
using open-vm-tools packages. See http://kb.vmware.com/kb/2073803 for more 
information.
Do you still want to proceed with this installation? [yes] 

INPUT: [yes]  default

A previous installation of VMware Tools has been detected.

The previous installation was made by the tar installer (version 4).

Keeping the tar4 installer database format.

You have a version of VMware Tools installed.  Continuing this install will 
first uninstall the currently installed version.  Do you wish to continue? 
(yes/no) [yes] 

INPUT: [yes]  default

Uninstalling the tar installation of VMware Tools.

manageSELinux uninstall: The 'semanage' utility was not found.
There was an error configuring the SELinux security context for VMware Tools.  
Please make certain that SELinux is configured correctly.

Stopping services for VMware Tools

Stopping vmware-tools (via systemctl):  [  OK  ]

cat: /tmp/_cafenv-appconfig_: No such file or directory
This program previously created the directory /etc/vmware-caf/pme/config, and 
was about to remove it. Since there are files in that directory that this 
program did not create, it will not be removed.

This program previously created the directory /etc/vmware-caf/pme, and was 
about to remove it. Since there are files in that directory that this program 
did not create, it will not be removed.

This program previously created the directory /etc/vmware-caf, and was about to
remove it. Since there are files in that directory that this program did not 
create, it will not be removed.

The removal of VMware Tools 10.3.21 build-14772444 for Linux completed 
successfully.

Installing VMware Tools.

In which directory do you want to install the binary files? 
[/usr/bin] 

INPUT: [/usr/bin]  default

What is the directory that contains the init directories (rc0.d/ to rc6.d/)? 
[/etc/rc.d] 

INPUT: [/etc/rc.d]  default

What is the directory that contains the init scripts? 
[/etc/rc.d/init.d] 

INPUT: [/etc/rc.d/init.d]  default

In which directory do you want to install the daemon files? 
[/usr/sbin] 

INPUT: [/usr/sbin]  default

In which directory do you want to install the library files? 
[/usr/lib/vmware-tools] 

INPUT: [/usr/lib/vmware-tools]  default

The path "/usr/lib/vmware-tools" does not exist currently. This program is 
going to create it, including needed parent directories. Is this what you want?
[yes] 

INPUT: [yes]  default

In which directory do you want to install the common agent library files? 
[/usr/lib] 

INPUT: [/usr/lib]  default

In which directory do you want to install the common agent transient files? 
[/var/lib] 

INPUT: [/var/lib]  default

In which directory do you want to install the documentation files? 
[/usr/share/doc/vmware-tools] 

INPUT: [/usr/share/doc/vmware-tools]  default

The path "/usr/share/doc/vmware-tools" does not exist currently. This program 
is going to create it, including needed parent directories. Is this what you 
want? [yes] 

INPUT: [yes]  default

The installation of VMware Tools 10.3.21 build-14772444 for Linux completed 
successfully. You can decide to remove this software from your system at any 
time by invoking the following command: "/usr/bin/vmware-uninstall-tools.pl".

Before running VMware Tools for the first time, you need to configure it by 
invoking the following command: "/usr/bin/vmware-config-tools.pl". Do you want 
this program to invoke the command for you now? [yes] 

INPUT: [yes]  default

Initializing...


Making sure services for VMware Tools are stopped.

Stopping vmware-tools (via systemctl):  [  OK  ]


The module vmci has already been installed on this system by another installer 
or package and will not be modified by this installer.

The module vsock has already been installed on this system by another installer
or package and will not be modified by this installer.

The module vmxnet3 has already been installed on this system by another 
installer or package and will not be modified by this installer.

The module pvscsi has already been installed on this system by another 
installer or package and will not be modified by this installer.

The module vmmemctl has already been installed on this system by another 
installer or package and will not be modified by this installer.

The VMware Host-Guest Filesystem allows for shared folders between the host OS 
and the guest OS in a Fusion or Workstation virtual environment.  Do you wish 
to enable this feature? [yes] 

INPUT: [yes]  default


Before you can compile modules, you need to have the following installed... 

make
gcc
kernel headers of the running kernel


Searching for GCC...
Detected GCC binary at "/bin/gcc".
The path "/bin/gcc" appears to be a valid path to the gcc binary.
Would you like to change it? [no] 

INPUT: [no]  default

Searching for a valid kernel header path...
Detected the kernel headers at 
"/lib/modules/3.10.0-1062.18.1.el7.x86_64/build/include".
The path "/lib/modules/3.10.0-1062.18.1.el7.x86_64/build/include" appears to be
a valid path to the 3.10.0-1062.18.1.el7.x86_64 kernel headers.
Would you like to change it? [no] 

INPUT: [no]  default

Using kernel build system.
make: Entering directory `/tmp/modconfig-xU5hFj/vmhgfs-only'
/bin/make -C /lib/modules/3.10.0-1062.18.1.el7.x86_64/build/include/.. SUBDIRS=$PWD SRCROOT=$PWD/. \
  MODULEBUILDDIR= modules
make[1]: Entering directory `/usr/src/kernels/3.10.0-1062.18.1.el7.x86_64'
  CC [M]  /tmp/modconfig-xU5hFj/vmhgfs-only/backdoorGcc64.o
  CC [M]  /tmp/modconfig-xU5hFj/vmhgfs-only/message.o
  CC [M]  /tmp/modconfig-xU5hFj/vmhgfs-only/dir.o
  CC [M]  /tmp/modconfig-xU5hFj/vmhgfs-only/request.o
/tmp/modconfig-xU5hFj/vmhgfs-only/backdoorGcc64.o: warning: objtool: BackdoorHbIn()+0xd: duplicate frame pointer save
/tmp/modconfig-xU5hFj/vmhgfs-only/backdoorGcc64.o: warning: objtool: BackdoorHbOut()+0xd: duplicate frame pointer save
  CC [M]  /tmp/modconfig-xU5hFj/vmhgfs-only/filesystem.o
  CC [M]  /tmp/modconfig-xU5hFj/vmhgfs-only/cpName.o
  CC [M]  /tmp/modconfig-xU5hFj/vmhgfs-only/rpcout.o
  CC [M]  /tmp/modconfig-xU5hFj/vmhgfs-only/stubs.o
  CC [M]  /tmp/modconfig-xU5hFj/vmhgfs-only/hgfsUtil.o
  CC [M]  /tmp/modconfig-xU5hFj/vmhgfs-only/hgfsEscape.o
  CC [M]  /tmp/modconfig-xU5hFj/vmhgfs-only/link.o
  CC [M]  /tmp/modconfig-xU5hFj/vmhgfs-only/transport.o
  CC [M]  /tmp/modconfig-xU5hFj/vmhgfs-only/module.o
  CC [M]  /tmp/modconfig-xU5hFj/vmhgfs-only/file.o
  CC [M]  /tmp/modconfig-xU5hFj/vmhgfs-only/super.o
  CC [M]  /tmp/modconfig-xU5hFj/vmhgfs-only/bdhandler.o
  CC [M]  /tmp/modconfig-xU5hFj/vmhgfs-only/fsutil.o
  CC [M]  /tmp/modconfig-xU5hFj/vmhgfs-only/cpNameLinux.o
  CC [M]  /tmp/modconfig-xU5hFj/vmhgfs-only/hgfsBd.o
  CC [M]  /tmp/modconfig-xU5hFj/vmhgfs-only/page.o
  CC [M]  /tmp/modconfig-xU5hFj/vmhgfs-only/backdoor.o
  CC [M]  /tmp/modconfig-xU5hFj/vmhgfs-only/inode.o
  CC [M]  /tmp/modconfig-xU5hFj/vmhgfs-only/dentry.o
  CC [M]  /tmp/modconfig-xU5hFj/vmhgfs-only/cpNameLite.o
  CC [M]  /tmp/modconfig-xU5hFj/vmhgfs-only/kernelStubsLinux.o
  LD [M]  /tmp/modconfig-xU5hFj/vmhgfs-only/vmhgfs.o
  Building modules, stage 2.
  MODPOST 1 modules
  CC      /tmp/modconfig-xU5hFj/vmhgfs-only/vmhgfs.mod.o
  LD [M]  /tmp/modconfig-xU5hFj/vmhgfs-only/vmhgfs.ko
make[1]: Leaving directory `/usr/src/kernels/3.10.0-1062.18.1.el7.x86_64'
/bin/make -C $PWD SRCROOT=$PWD/. \
  MODULEBUILDDIR= postbuild
make[1]: Entering directory `/tmp/modconfig-xU5hFj/vmhgfs-only'
make[1]: `postbuild' is up to date.
make[1]: Leaving directory `/tmp/modconfig-xU5hFj/vmhgfs-only'
cp -f vmhgfs.ko ./../vmhgfs.o
make: Leaving directory `/tmp/modconfig-xU5hFj/vmhgfs-only'

The vmxnet driver is no longer supported on kernels 3.3 and greater. Please 
upgrade to a newer virtual NIC. (e.g., vmxnet3 or e1000e)

The vmblock enables dragging or copying files between host and guest in a 
Fusion or Workstation virtual environment.  Do you wish to enable this feature?
[no] yes

INPUT: [yes]

NOTICE:  It appears your system does not have the required fuse packages 
installed.  The VMware blocking filesystem requires the fuse packages and its 
libraries to function properly.  Please install the fuse or fuse-utils package 
using your systems package management utility and re-run this script in order 
to enable the VMware blocking filesystem. 

VMware automatic kernel modules enables automatic building and installation of
VMware kernel modules at boot that are not already present. This feature can
be enabled/disabled by re-running vmware-config-tools.pl.

Would you like to enable VMware automatic kernel modules?
[yes] 

INPUT: [yes]  default

Do you want to enable Guest Authentication (vgauth)? Enabling vgauth is needed 
if you want to enable Common Agent (caf). [yes] 

INPUT: [yes]  default

Do you want to enable Common Agent (caf)? [no] 

INPUT: [no]  default

No X install found.


Skipping rebuilding initrd boot image for kernel as no drivers to be included 
in boot image were installed by this installer.

Generating the key and certificate files.
Successfully generated the key and certificate files.
manageSELinux install: The 'semanage' utility was not found.
There was an error configuring the SELinux security context for VMware Tools.  
Please make certain that SELinux is configured correctly.

The configuration of VMware Tools 10.3.21 build-14772444 for Linux for this 
running kernel completed successfully.

You must restart your X session before any mouse or graphics changes take 
effect.

To enable advanced X features (e.g., guest resolution fit, drag and drop, and 
file and text copy/paste), you will need to do one (or more) of the following:
1. Manually start /usr/bin/vmware-user
2. Log out and log back into your desktop session
3. Restart your X session.

Enjoy,

--the VMware team

[root@py vmware-tools-distrib]# 
```

</details>

![VMware Tools 10.3.21 build 14772444](https://i1.yuangezhizao.cn/Win-10/20200406210003.jpg!webp)

## 0x06.[SmartDNS](https://github.com/pymumu/smartdns)
安装
``` bash
[root@cn-py-dl-c8 ~]# wget https://github.com/pymumu/smartdns/releases/download/Release33/smartdns.1.2020.09.08-2235.x86_64-linux-all.tar.gz
[root@cn-py-dl-c8 ~]# ll
total 1576
-rw-------. 1 root root    1490 Mar 21 14:07 anaconda-ks.cfg
-rw-r--r--. 1 root root 1606759 Sep  8  2020 smartdns.1.2020.09.08-2235.x86_64-linux-all.tar.gz
[root@cn-py-dl-c8 ~]# tar zxf smartdns.1.2020.09.08-2235.x86_64-linux-all.tar.gz 
[root@cn-py-dl-c8 ~]# cd smartdns
[root@cn-py-dl-c8 smartdns]# chmod +x ./install
[root@cn-py-dl-c8 smartdns]# ./install -i
install: creating directory '/etc/smartdns'
'usr/sbin/smartdns' -> '/usr/sbin/smartdns'
'etc/smartdns/smartdns.conf' -> '/etc/smartdns/smartdns.conf'
'etc/default/smartdns' -> '/etc/default/smartdns'
'etc/init.d/smartdns' -> '/etc/init.d/smartdns'
'systemd/smartdns.service' -> '/usr/lib/systemd/system/smartdns.service'
Synchronizing state of smartdns.service with SysV service script with /usr/lib/systemd/systemd-sysv-install.
Executing: /usr/lib/systemd/systemd-sysv-install enable smartdns
Created symlink /etc/systemd/system/smartdns.service → /usr/lib/systemd/system/smartdns.service.
Created symlink /etc/systemd/system/multi-user.target.wants/smartdns.service → /usr/lib/systemd/system/smartdns.service.
[root@cn-py-dl-c8 smartdns]# vim /etc/smartdns/smartdns.conf
[root@cn-py-dl-c8 smartdns]# cd /var/log
[root@cn-py-dl-c8 log]# mkdir smartdns
[root@cn-py-dl-c8 ~]# systemctl enable smartdns
[root@cn-py-dl-c8 ~]# systemctl restart smartdns
[root@cn-py-dl-c8 ~]# systemctl status smartdns
```
配置文件

<details><summary>点击此处 ← 查看折叠</summary>

``` bash
[root@cn-py-dl-c8 ~]# cat /etc/smartdns/smartdns.conf
# dns server name, default is host name
# server-name, 
# example:
#   server-name smartdns
#

# Include another configuration options
# conf-file [file]
# conf-file blacklist-ip.conf

# dns server bind ip and port, default dns server port is 53, support binding multi ip and port
# bind udp server
#   bind [IP]:[port] [-group [group]] [-no-rule-addr] [-no-rule-nameserver] [-no-rule-ipset] [-no-speed-check] [-no-cache] [-no-rule-soa] [-no-dualstack-selection]
# bind tcp server
#   bind-tcp [IP]:[port] [-group [group]] [-no-rule-addr] [-no-rule-nameserver] [-no-rule-ipset] [-no-speed-check] [-no-cache] [-no-rule-soa] [-no-dualstack-selection]
# option:
#   -group: set domain request to use the appropriate server group.
#   -no-rule-addr: skip address rule.
#   -no-rule-nameserver: skip nameserver rule.
#   -no-rule-ipset: skip ipset rule.
#   -no-speed-check: do not check speed.
#   -no-cache: skip cache.
#   -no-rule-soa: Skip address SOA(#) rules.
#   -no-dualstack-selection: Disable dualstack ip selection.
#   -force-aaaa-soa: force AAAA query return SOA.
# example: 
#  IPV4: 
#    bind :53
#    bind :6053 -group office -no-speed-check
#  IPV6:
#    bind [::]:53
#    bind-tcp [::]:53
bind [::]:53

# tcp connection idle timeout
# tcp-idle-time [second]

# dns cache size
# cache-size [number]
#   0: for no cache
cache-size 4096

# enable persist cache when restart
# cache-persist yes

# cache persist file
# cache-file /tmp/smartdns.cache

# prefetch domain
# prefetch-domain [yes|no]
prefetch-domain yes

# cache serve expired 
# serve-expired [yes|no]
# serve-expired yes

# cache serve expired TTL
# serve-expired-ttl [num]
# serve-expired-ttl 0

# reply TTL value to use when replying with expired data
# serve-expired-reply-ttl [num]
# serve-expired-reply-ttl 30

# List of hosts that supply bogus NX domain results 
# bogus-nxdomain [ip/subnet]

# List of IPs that will be filtered when nameserver is configured -blacklist-ip parameter
# blacklist-ip [ip/subnet]

# List of IPs that will be accepted when nameserver is configured -whitelist-ip parameter
# whitelist-ip [ip/subnet]

# List of IPs that will be ignored
# ignore-ip [ip/subnet]

# speed check mode
# speed-check-mode [ping|tcp:port|none|,]
# example:
   speed-check-mode ping,tcp:80,tcp:443
#   speed-check-mode tcp:443,ping
#   speed-check-mode none

# force AAAA query return SOA
# force-AAAA-SOA [yes|no]

# Enable IPV4, IPV6 dual stack IP optimization selection strategy
# dualstack-ip-selection-threshold [num] (0~1000)
# dualstack-ip-selection [yes|no]
dualstack-ip-selection yes

# edns client subnet
# edns-client-subnet [ip/subnet]
# edns-client-subnet 192.168.1.1/24
# edns-client-subnet [8::8]/56

# ttl for all resource record
# rr-ttl: ttl for all record
# rr-ttl-min: minimum ttl for resource record
# rr-ttl-max: maximum ttl for resource record
# example:
# rr-ttl 300
# rr-ttl-min 60
# rr-ttl-max 86400

# set log level
# log-level: [level], level=fatal, error, warn, notice, info, debug
# log-file: file path of log file.
# log-size: size of each log file, support k,m,g
# log-num: number of logs
log-level info
log-file /var/log/smartdns/smartdns.log
log-size 100m
log-num 90

# dns audit
# audit-enable [yes|no]: enable or disable audit.
audit-enable yes
# audit-SOA [yes|no]: enable or disable log soa result.
# audit-size size of each audit file, support k,m,g
audit-file /var/log/smartdns/smartdns-audit.log
audit-size 100m
audit-num 90

# certificate file
# ca-file [file]
# ca-file /etc/ssl/certs/ca-certificates.crt

# certificate path
# ca-path [path]
# ca-path /etc/ss/certs

# remote udp dns server list
# server [IP]:[PORT] [-blacklist-ip] [-whitelist-ip] [-check-edns] [-group [group] ...] [-exclude-default-group]
# default port is 53
#   -blacklist-ip: filter result with blacklist ip
#   -whitelist-ip: filter result whth whitelist ip,  result in whitelist-ip will be accepted.
#   -check-edns: result must exist edns RR, or discard result.
#   -group [group]: set server to group, use with nameserver /domain/group.
#   -exclude-default-group: exclude this server from default group.
# server 8.8.8.8 -blacklist-ip -check-edns -group g1 -group g2
# server 114.114.114.114
server 172.64.36.1
server 172.64.36.2
server 1.1.1.1
server 8.8.8.8
server 219.149.6.99

server 2a06:98c1:54::1802
server 240c::6666
server 240e:41:c900:ffff::

# remote tcp dns server list
# server-tcp [IP]:[PORT] [-blacklist-ip] [-whitelist-ip] [-group [group] ...] [-exclude-default-group]
# default port is 53
# server-tcp 8.8.8.8

# remote tls dns server list
# server-tls [IP]:[PORT] [-blacklist-ip] [-whitelist-ip] [-spki-pin [sha256-pin]] [-group [group] ...] [-exclude-default-group]
#   -spki-pin: TLS spki pin to verify.
#   -tls-host-verify: cert hostname to verify.
#   -host-name: TLS sni hostname.
#   -no-check-certificate: no check certificate.
# Get SPKI with this command:
#    echo | openssl s_client -connect '[ip]:853' | openssl x509 -pubkey -noout | openssl pkey -pubin -outform der | openssl dgst -sha256 -binary | openssl enc -base64
# default port is 853
# server-tls 8.8.8.8
# server-tls 1.0.0.1

# remote https dns server list
# server-https https://[host]:[port]/path [-blacklist-ip] [-whitelist-ip] [-spki-pin [sha256-pin]] [-group [group] ...] [-exclude-default-group]
#   -spki-pin: TLS spki pin to verify.
#   -tls-host-verify: cert hostname to verify.
#   -host-name: TLS sni hostname.
#   -http-host: http host.
#   -no-check-certificate: no check certificate.
# default port is 443
server-https https://9u12dgz3lz.cloudflare-gateway.com/dns-query
server-https https://cloudflare-dns.com/dns-query
server-https https://dns.google/dns-query

# specific nameserver to domain
# nameserver /domain/[group|-]
# nameserver /www.example.com/office, Set the domain name to use the appropriate server group.
# nameserver /www.example.com/-, ignore this domain

# specific address to domain
# address /domain/[ip|-|-4|-6|#|#4|#6]
# address /www.example.com/1.2.3.4, return ip 1.2.3.4 to client
# address /www.example.com/-, ignore address, query from upstream, suffix 4, for ipv4, 6 for ipv6, none for all
# address /www.example.com/#, return SOA to client, suffix 4, for ipv4, 6 for ipv6, none for all

# enable ipset timeout by ttl feature
# ipset-timeout [yes]

# specific ipset to domain
# ipset /domain/[ipset|-]
# ipset /www.example.com/block, set ipset with ipset name of block 
# ipset /www.example.com/-, ignore this domain

# set domain rules
# domain-rules /domain/ [-speed-check-mode [...]]
# rules:
#   -speed-check-mode [mode]: speed check mode
#                             speed-check-mode [ping|tcp:port|none|,]
#   -address [address|-]: same as address option
#   -nameserver [group|-]: same as nameserver option
#   -ipset [ipset|-]: same as ipset option
```

</details>

## 0x07.[Docker](https://web.archive.org/web/20200614132813/https://docs.docker.com/engine/install/centos/)
``` bash
[root@py ~]# yum remove docker \
>                   docker-client \
>                   docker-client-latest \
>                   docker-common \
>                   docker-latest \
>                   docker-latest-logrotate \
>                   docker-logrotate \
>                   docker-engine
Loaded plugins: fastestmirror
No Match for argument: docker
No Match for argument: docker-client
No Match for argument: docker-client-latest
No Match for argument: docker-common
No Match for argument: docker-latest
No Match for argument: docker-latest-logrotate
No Match for argument: docker-logrotate
No Match for argument: docker-engine
No Packages marked for removal
[root@py ~]# yum install -y yum-utils
[root@py ~]# yum-config-manager \
>     --add-repo \
>     https://download.docker.com/linux/centos/docker-ce.repo
Loaded plugins: fastestmirror
adding repo from: https://download.docker.com/linux/centos/docker-ce.repo
grabbing file https://download.docker.com/linux/centos/docker-ce.repo to /etc/yum.repos.d/docker-ce.repo
repo saved to /etc/yum.repos.d/docker-ce.repo
[root@py ~]# yum install docker-ce docker-ce-cli containerd.io
[root@py ~]# systemctl start docker
[root@py ~]# docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
0e03bdcc26d7: Pull complete 
Digest: sha256:8e3114318a995a1ee497790535e7b88365222a21771ae7e53687ad76563e8e76
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/

[root@py ~]# 
[root@py ~]# docker pull portainer/portainer
Using default tag: latest
latest: Pulling from portainer/portainer
d1e017099d17: Pull complete 
a7dca5b5a9e8: Pull complete 
Digest: sha256:4ae7f14330b56ffc8728e63d355bc4bc7381417fa45ba0597e5dd32682901080
Status: Downloaded newer image for portainer/portainer:latest
docker.io/portainer/portainer:latest
[root@py ~]# docker volume create portainer_data
portainer_data
[root@py ~]# docker run -d -p 9000:9000 --name portainer --restart always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer
1e66ec7242a7ec5255a6acb4ee8ddcc58c0bd6ed373a5cf4b304b5ad7408274c
```
配置镜像源：https://web.archive.org/web/20200614132904/https://mirrors.ustc.edu.cn/help/dockerhub.html

## 0x07.安装[SmokePing](https://oss.oetiker.ch/smokeping/index.en.html)
参照[How to install SmokePing](https://web.archive.org/web/20210817144328/https://oss.oetiker.ch/smokeping/doc/smokeping_install.en.html)
``` bash
[root@cn-py-dl-c8 ~]# yum install rrdtool perl-rrdtool openssl-devel -y
[root@cn-py-dl-c8 ~]# yum install perl-core fping curl gcc-c++ -y
[root@cn-py-dl-c8 ~]# wget https://oss.oetiker.ch/smokeping/pub/smokeping-2.8.2.tar.gz
[root@cn-py-dl-c8 ~]# tar -zxvf smokeping-2.8.2.tar.gz
[root@cn-py-dl-c8 ~]# cd smokeping-2.8.2
[root@cn-py-dl-c8 smokeping-2.8.2]# ./configure --prefix=/opt/smokeping
[root@cn-py-dl-c8 smokeping-2.8.2]# make install
```
经过巨巨巨长的时间之后，安装完成了？

<details><summary>点击此处 ← 查看折叠</summary>

``` bash
[root@cn-py-dl-c8 smokeping-2.8.2]# make install
Making install in lib
make[1]: Entering directory '/root/smokeping-2.8.2/lib'
make[2]: Entering directory '/root/smokeping-2.8.2/lib'
make[2]: Nothing to be done for 'install-exec-am'.
 /usr/bin/mkdir -p '/opt/smokeping/lib'
 /usr/bin/mkdir -p '/opt/smokeping/lib/Smokeping/probes'
 /usr/bin/install -c -m 644  Smokeping/probes/EchoPingSmtp.pm Smokeping/probes/OpenSSHJunOSPing.pm Smokeping/probes/skel.pm Smokeping/probes/EchoPingWhois.pm Smokeping/probes/EchoPingHttp.pm Smokeping/probes/TelnetIOSPing.pm Smokeping/probes/EchoPingDiscard.pm Smokeping/probes/CiscoRTTMonDNS.pm Smokeping/probes/IOSPing.pm Smokeping/probes/AnotherCurl.pm Smokeping/probes/FPing.pm Smokeping/probes/TraceroutePing.pm Smokeping/probes/TacacsPlus.pm Smokeping/probes/RemoteFPing.pm Smokeping/probes/Curl.pm Smokeping/probes/basevars.pm Smokeping/probes/EchoPingIcp.pm Smokeping/probes/Qstat.pm Smokeping/probes/base.pm Smokeping/probes/WebProxyFilter.pm Smokeping/probes/basefork.pm Smokeping/probes/FPingContinuous.pm Smokeping/probes/TCPPing.pm Smokeping/probes/EchoPingLDAP.pm Smokeping/probes/SSH.pm Smokeping/probes/EchoPingHttps.pm Smokeping/probes/TelnetJunOSPing.pm Smokeping/probes/SendEmail.pm Smokeping/probes/passwordchecker.pm Smokeping/probes/EchoPing.pm Smokeping/probes/AnotherDNS.pm Smokeping/probes/CiscoRTTMonTcpConnect.pm Smokeping/probes/SipSak.pm Smokeping/probes/LDAP.pm Smokeping/probes/FPing6.pm Smokeping/probes/IRTT.pm Smokeping/probes/NFSping.pm Smokeping/probes/EchoPingPlugin.pm Smokeping/probes/Radius.pm Smokeping/probes/AnotherSSH.pm '/opt/smokeping/lib/Smokeping/probes'
 /usr/bin/mkdir -p '/opt/smokeping/lib/Smokeping/sorters'
 /usr/bin/install -c -m 644  Smokeping/sorters/base.pm Smokeping/sorters/Median.pm Smokeping/sorters/Max.pm Smokeping/sorters/Loss.pm Smokeping/sorters/StdDev.pm '/opt/smokeping/lib/Smokeping/sorters'
 /usr/bin/install -c -m 644  BER.pm Smokeping.pm SNMP_util.pm SNMP_Session.pm '/opt/smokeping/lib/.'
 /usr/bin/mkdir -p '/opt/smokeping/lib/Smokeping/matchers'
 /usr/bin/install -c -m 644  Smokeping/matchers/CheckLoss.pm Smokeping/matchers/Avgratio.pm Smokeping/matchers/CheckLatency.pm Smokeping/matchers/ConsecutiveLoss.pm Smokeping/matchers/base.pm Smokeping/matchers/Median.pm Smokeping/matchers/ExpLoss.pm Smokeping/matchers/Medratio.pm '/opt/smokeping/lib/Smokeping/matchers'
 /usr/bin/mkdir -p '/opt/smokeping/lib/Smokeping/probes'
 /usr/bin/install -c -m 644  Smokeping/probes/CiscoRTTMonEchoICMP.pm Smokeping/probes/EchoPingDNS.pm Smokeping/probes/DismanPing.pm Smokeping/probes/OpenSSHEOSPing.pm Smokeping/probes/DNS.pm Smokeping/probes/FTPtransfer.pm Smokeping/probes/EchoPingChargen.pm '/opt/smokeping/lib/Smokeping/probes'
 /usr/bin/mkdir -p '/opt/smokeping/lib/Smokeping'
 /usr/bin/install -c -m 644  Smokeping/Slave.pm Smokeping/pingMIB.pm Smokeping/Graphs.pm Smokeping/ciscoRttMonMIB.pm Smokeping/RRDtools.pm Smokeping/Colorspace.pm Smokeping/Examples.pm Smokeping/Info.pm Smokeping/RRDhelpers.pm Smokeping/Config.pm Smokeping/Master.pm '/opt/smokeping/lib/Smokeping'
make[2]: Leaving directory '/root/smokeping-2.8.2/lib'
make[1]: Leaving directory '/root/smokeping-2.8.2/lib'
Making install in thirdparty
make[1]: Entering directory '/root/smokeping-2.8.2/thirdparty'
echo "** Installing Dependencies using Carton install"
** Installing Dependencies using Carton install
test -f cpanfile-5.26.snapshot && cp cpanfile-5.26.snapshot ../cpanfile.snapshot || true
test -x carton/bin/carton || PERL_CPANM_OPT= PERL_CPANM_HOME=/root/smokeping-2.8.2/thirdparty PERL_CARTON_PATH=/root/smokeping-2.8.2/thirdparty /usr/bin/perl bin/cpanm -q --notest --local-lib-contained /root/smokeping-2.8.2/thirdparty/carton Carton
Successfully installed Module-CPANfile-1.1004
Successfully installed ExtUtils-MakeMaker-CPANfile-0.09
Successfully installed Parse-PMFile-0.43
Successfully installed Win32-ShellQuote-0.003001
Successfully installed ExtUtils-Helpers-0.026
Successfully installed URI-5.09
Successfully installed Capture-Tiny-0.48
Successfully installed ExtUtils-Config-0.008
Successfully installed ExtUtils-InstallPaths-0.012
Successfully installed CPAN-DistnameInfo-0.12
Successfully installed Tie-Handle-Offset-0.004
Successfully installed Class-Tiny-1.008
Successfully installed CPAN-Common-Index-0.010
Successfully installed File-pushd-1.016
Successfully installed File-Which-1.27
Successfully installed IPC-Run3-0.048
Successfully installed HTTP-Tinyish-0.17
Successfully installed CPAN-Meta-Check-0.014
Successfully installed String-ShellQuote-1.04
Successfully installed local-lib-2.000024
Successfully installed Menlo-1.9019
Successfully installed Menlo-Legacy-1.9022
Successfully installed Path-Tiny-0.118
Successfully installed Try-Tiny-0.30
Successfully installed Carton-v1.0.34
25 distributions installed
PERL_CPANM_OPT= PERL_CPANM_HOME=/root/smokeping-2.8.2/thirdparty PERL_CARTON_PATH=/root/smokeping-2.8.2/thirdparty PERL5LIB=/root/smokeping-2.8.2/thirdparty/carton/lib/perl5 /usr/bin/perl /root/smokeping-2.8.2/thirdparty/carton/bin/carton install
Installing modules using /root/smokeping-2.8.2/cpanfile
Successfully installed Net-SSLeay-1.90
Successfully installed Mozilla-CA-20200520
Successfully installed IO-Socket-SSL-2.072
Successfully installed Cpanel-JSON-XS-4.26
Successfully installed JSON-MaybeXS-1.004003
Successfully installed Module-Build-0.4231
Successfully installed InfluxDB-LineProtocol-1.014
Successfully installed Net-OpenSSH-0.80
Successfully installed Data-HexDump-0.04
Successfully installed Net-IP-1.26
Successfully installed Authen-Radius-0.32
Successfully installed Convert-ASN1-0.31
Successfully installed Text-Soundex-3.05
Successfully installed URI-5.09
Successfully installed perl-ldap-0.68
Successfully installed Path-Tiny-0.118
Successfully installed FCGI-0.82
Successfully installed InfluxDB-HTTP-0.04
Successfully installed IO-String-1.08

gzip: stdin: unexpected end of file
/usr/bin/tar: Child returned status 1
/usr/bin/tar: Error is not recoverable: exiting now
! The distribution doesn't have a proper Makefile.PL/Build.PL See /root/smokeping-2.8.2/thirdparty/work/1629212965.50837/build.log for details.
Successfully installed Clone-0.45
Successfully installed Task-Weaken-1.06
Successfully installed PPI-1.270
Successfully installed Keyword-Simple-0.04
Successfully installed ExtUtils-MakeMaker-7.62 (upgraded from 7.24)
Successfully installed ExtUtils-Depends-0.8001
Successfully installed B-Hooks-OP-Check-0.22
Successfully installed Sub-Name-0.26
Successfully installed Test-Requires-0.11
Successfully installed Sub-Exporter-Progressive-0.001013
Successfully installed Try-Tiny-0.30
Successfully installed Module-Runtime-0.016
Successfully installed Module-Implementation-0.09
Successfully installed Variable-Magic-0.62
Successfully installed B-Hooks-EndOfScope-0.24
Successfully installed Devel-Declare-0.006022
Successfully installed ExtUtils-Helpers-0.026
Successfully installed ExtUtils-Config-0.008
Successfully installed ExtUtils-InstallPaths-0.012
Successfully installed Module-Build-Tiny-0.039
Successfully installed Const-Fast-0.014
Successfully installed Devel-CheckCompiler-0.07
Successfully installed Devel-PPPort-3.63 (upgraded from 3.35)
Successfully installed Module-Build-XSUtil-0.19
Successfully installed Mouse-v2.5.10
Successfully installed Any-Moose-0.27
Successfully installed Sub-Uplevel-0.2800
Successfully installed Test-Warn-0.36
Successfully installed Test-Exception-0.43
Successfully installed Lexical-SealRequireHints-0.011
Successfully installed Method-Signatures-20170211
Successfully installed Object-Result-0.000003
Successfully installed Socket6-0.29
Successfully installed IO-Tty-1.16
Successfully installed Config-Grammar-1.13
Successfully installed Net-Telnet-3.05
Successfully installed TimeDate-2.33
Successfully installed Time-Local-1.30 (upgraded from 1.25)
Successfully installed HTTP-Date-6.05
Successfully installed WWW-RobotRules-6.02

gzip: stdin: unexpected end of file
/usr/bin/tar: Unexpected EOF in archive
/usr/bin/tar: Error is not recoverable: exiting now
! The distribution doesn't have a proper Makefile.PL/Build.PL See /root/smokeping-2.8.2/thirdparty/work/1629212965.50837/build.log for details.

gzip: stdin: unexpected end of file
/usr/bin/tar: Unexpected EOF in archive
/usr/bin/tar: Error is not recoverable: exiting now
! Installing Encode failed. See /root/smokeping-2.8.2/thirdparty/work/1629212965.50837/build.log for details. Retry with --force to force install it.
Successfully installed IO-HTML-1.004
Successfully installed LWP-MediaTypes-6.04
Successfully installed Encode-Locale-1.05
! Installing the dependencies failed: Installed version (2.97) of Encode is not in range '3.01'
! Bailing out the installation for HTTP-Message-6.33.
! Installing the dependencies failed: Module 'HTTP::Headers' is not installed
! Bailing out the installation for HTTP-Negotiate-6.01.
Successfully installed File-Listing-6.14
Successfully installed Net-HTTP-6.21
! Installing the dependencies failed: Module 'HTTP::Request' is not installed, Module 'HTTP::Headers::Util' is not installed
! Bailing out the installation for HTTP-Cookies-6.10.
! Installing the dependencies failed: Module 'HTTP::Request::Common' is not installed, Module 'HTTP::Negotiate' is not installed, Module 'HTTP::Request' is not installed, Module 'HTML::Entities' is not installed, Module 'HTTP::Response' is not installed, Module 'HTTP::Cookies' is not installed, Module 'HTML::HeadParser' is not installed, Module 'HTTP::Status' is not installed
! Bailing out the installation for libwww-perl-6.56.
! Installing the dependencies failed: Module 'HTML::Entities' is not installed
! Bailing out the installation for CGI-4.53.
Successfully installed Digest-HMAC-1.04
Successfully installed Net-DNS-1.32
! Installing the dependencies failed: Module 'CGI' is not installed
! Bailing out the installation for CGI-Fast-2.15.
Successfully installed Net-SNMP-v6.0.1
! Installing the dependencies failed: Module 'LWP' is not installed, Module 'CGI' is not installed, Module 'CGI::Fast' is not installed
! Bailing out the installation for /root/smokeping-2.8.2/.
67 distributions installed
Installing modules failed
make[1]: *** [Makefile:432: cpanfile-5.26.snapshot] Error 25
make[1]: Leaving directory '/root/smokeping-2.8.2/thirdparty'
make: *** [Makefile:359: install-recursive] Error 1
```

</details>

但是有报错草，于是又来了一遍`make install`

<details><summary>点击此处 ← 查看折叠</summary>

``` bash
[root@cn-py-dl-c8 smokeping-2.8.2]# make install
Making install in lib
make[1]: Entering directory '/root/smokeping-2.8.2/lib'
make[2]: Entering directory '/root/smokeping-2.8.2/lib'
make[2]: Nothing to be done for 'install-exec-am'.
 /usr/bin/mkdir -p '/opt/smokeping/lib'
 /usr/bin/mkdir -p '/opt/smokeping/lib/Smokeping/probes'
 /usr/bin/install -c -m 644  Smokeping/probes/EchoPingSmtp.pm Smokeping/probes/OpenSSHJunOSPing.pm Smokeping/probes/skel.pm Smokeping/probes/EchoPingWhois.pm Smokeping/probes/EchoPingHttp.pm Smokeping/probes/TelnetIOSPing.pm Smokeping/probes/EchoPingDiscard.pm Smokeping/probes/CiscoRTTMonDNS.pm Smokeping/probes/IOSPing.pm Smokeping/probes/AnotherCurl.pm Smokeping/probes/FPing.pm Smokeping/probes/TraceroutePing.pm Smokeping/probes/TacacsPlus.pm Smokeping/probes/RemoteFPing.pm Smokeping/probes/Curl.pm Smokeping/probes/basevars.pm Smokeping/probes/EchoPingIcp.pm Smokeping/probes/Qstat.pm Smokeping/probes/base.pm Smokeping/probes/WebProxyFilter.pm Smokeping/probes/basefork.pm Smokeping/probes/FPingContinuous.pm Smokeping/probes/TCPPing.pm Smokeping/probes/EchoPingLDAP.pm Smokeping/probes/SSH.pm Smokeping/probes/EchoPingHttps.pm Smokeping/probes/TelnetJunOSPing.pm Smokeping/probes/SendEmail.pm Smokeping/probes/passwordchecker.pm Smokeping/probes/EchoPing.pm Smokeping/probes/AnotherDNS.pm Smokeping/probes/CiscoRTTMonTcpConnect.pm Smokeping/probes/SipSak.pm Smokeping/probes/LDAP.pm Smokeping/probes/FPing6.pm Smokeping/probes/IRTT.pm Smokeping/probes/NFSping.pm Smokeping/probes/EchoPingPlugin.pm Smokeping/probes/Radius.pm Smokeping/probes/AnotherSSH.pm '/opt/smokeping/lib/Smokeping/probes'
 /usr/bin/mkdir -p '/opt/smokeping/lib/Smokeping/sorters'
 /usr/bin/install -c -m 644  Smokeping/sorters/base.pm Smokeping/sorters/Median.pm Smokeping/sorters/Max.pm Smokeping/sorters/Loss.pm Smokeping/sorters/StdDev.pm '/opt/smokeping/lib/Smokeping/sorters'
 /usr/bin/install -c -m 644  BER.pm Smokeping.pm SNMP_util.pm SNMP_Session.pm '/opt/smokeping/lib/.'
 /usr/bin/mkdir -p '/opt/smokeping/lib/Smokeping/matchers'
 /usr/bin/install -c -m 644  Smokeping/matchers/CheckLoss.pm Smokeping/matchers/Avgratio.pm Smokeping/matchers/CheckLatency.pm Smokeping/matchers/ConsecutiveLoss.pm Smokeping/matchers/base.pm Smokeping/matchers/Median.pm Smokeping/matchers/ExpLoss.pm Smokeping/matchers/Medratio.pm '/opt/smokeping/lib/Smokeping/matchers'
 /usr/bin/mkdir -p '/opt/smokeping/lib/Smokeping/probes'
 /usr/bin/install -c -m 644  Smokeping/probes/CiscoRTTMonEchoICMP.pm Smokeping/probes/EchoPingDNS.pm Smokeping/probes/DismanPing.pm Smokeping/probes/OpenSSHEOSPing.pm Smokeping/probes/DNS.pm Smokeping/probes/FTPtransfer.pm Smokeping/probes/EchoPingChargen.pm '/opt/smokeping/lib/Smokeping/probes'
 /usr/bin/mkdir -p '/opt/smokeping/lib/Smokeping'
 /usr/bin/install -c -m 644  Smokeping/Slave.pm Smokeping/pingMIB.pm Smokeping/Graphs.pm Smokeping/ciscoRttMonMIB.pm Smokeping/RRDtools.pm Smokeping/Colorspace.pm Smokeping/Examples.pm Smokeping/Info.pm Smokeping/RRDhelpers.pm Smokeping/Config.pm Smokeping/Master.pm '/opt/smokeping/lib/Smokeping'
make[2]: Leaving directory '/root/smokeping-2.8.2/lib'
make[1]: Leaving directory '/root/smokeping-2.8.2/lib'
Making install in thirdparty
make[1]: Entering directory '/root/smokeping-2.8.2/thirdparty'
echo "** Installing Dependencies using Carton install"
** Installing Dependencies using Carton install
test -f cpanfile-5.26.snapshot && cp cpanfile-5.26.snapshot ../cpanfile.snapshot || true
test -x carton/bin/carton || PERL_CPANM_OPT= PERL_CPANM_HOME=/root/smokeping-2.8.2/thirdparty PERL_CARTON_PATH=/root/smokeping-2.8.2/thirdparty /usr/bin/perl bin/cpanm -q --notest --local-lib-contained /root/smokeping-2.8.2/thirdparty/carton Carton
PERL_CPANM_OPT= PERL_CPANM_HOME=/root/smokeping-2.8.2/thirdparty PERL_CARTON_PATH=/root/smokeping-2.8.2/thirdparty PERL5LIB=/root/smokeping-2.8.2/thirdparty/carton/lib/perl5 /usr/bin/perl /root/smokeping-2.8.2/thirdparty/carton/bin/carton install
Installing modules using /root/smokeping-2.8.2/cpanfile
Successfully installed Encode-3.12 (upgraded from 2.88)
Successfully installed HTTP-Message-6.33
Successfully installed HTTP-Cookies-6.10
Successfully installed HTML-Tagset-3.20
Successfully installed HTML-Parser-3.76
Successfully installed HTTP-Negotiate-6.01
Successfully installed libwww-perl-6.56
Successfully installed CGI-4.53
Successfully installed CGI-Fast-2.15
9 distributions installed
Complete! Modules were installed into /root/smokeping-2.8.2/thirdparty
mv ../cpanfile.snapshot cpanfile-5.26.snapshot
touch touch
echo "** Installing Dependencies using cpanm and cpanfile-5.26.snapshot"
** Installing Dependencies using cpanm and cpanfile-5.26.snapshot
cp cpanfile-5.26.snapshot ../cpanfile.snapshot
PERL_CPANM_OPT= PERL_CPANM_HOME=/root/smokeping-2.8.2/thirdparty PERL_CARTON_PATH=/root/smokeping-2.8.2/thirdparty /usr/bin/perl bin/cpanm -q --notest --local-lib-contained /root/smokeping-2.8.2/thirdparty --installdeps ..
rm -f ../cpanfile.snapshot
touch touch
make[2]: Entering directory '/root/smokeping-2.8.2/thirdparty'
make  install-exec-hook
make[3]: Entering directory '/root/smokeping-2.8.2/thirdparty'
cp -fr lib/perl5/* /opt/smokeping/lib
make[3]: Leaving directory '/root/smokeping-2.8.2/thirdparty'
make[2]: Nothing to be done for 'install-data-am'.
make[2]: Leaving directory '/root/smokeping-2.8.2/thirdparty'
make[1]: Leaving directory '/root/smokeping-2.8.2/thirdparty'
Making install in bin
make[1]: Entering directory '/root/smokeping-2.8.2/bin'
make[2]: Entering directory '/root/smokeping-2.8.2/bin'
 /usr/bin/mkdir -p '/opt/smokeping/bin'
 /usr/bin/install -c smokeinfo smokeping smokeping_cgi tSmoke '/opt/smokeping/bin'
make  install-exec-hook
make[3]: Entering directory '/root/smokeping-2.8.2/bin'
test "" = ""  || cd "/opt/smokeping/bin" && /usr/bin/perl -i -p -e 's{.*# PERL5LIB}{use lib (split /:/, q{}); # PERL5LIB}'  smokeinfo smokeping smokeping_cgi tSmoke
cd "/opt/smokeping/bin" && /usr/bin/perl -i -p -e 's{.*# LIBDIR}{use lib qw(/opt/smokeping/lib); # LIBDIR}' smokeinfo smokeping smokeping_cgi tSmoke
cd "/opt/smokeping/bin" && /usr/bin/perl -i -p -e 's{^#!.*perl.*}{#!/usr/bin/perl};'  smokeinfo smokeping smokeping_cgi tSmoke
make[3]: Leaving directory '/root/smokeping-2.8.2/bin'
make[2]: Nothing to be done for 'install-data-am'.
make[2]: Leaving directory '/root/smokeping-2.8.2/bin'
make[1]: Leaving directory '/root/smokeping-2.8.2/bin'
Making install in doc
make[1]: Entering directory '/root/smokeping-2.8.2/doc'
pod2man --release=2.8.2 --center=SmokePing ../bin/smokeping --section 1 > smokeping.1
pod2man --release=2.8.2 --center=SmokePing ../bin/smokeping_cgi --section 1 > smokeping_cgi.1
pod2man --release=2.8.2 --center=SmokePing ../bin/tSmoke --section 1 > tSmoke.1
pod2man --release=2.8.2 --center=SmokePing ../bin/smokeinfo --section 1 > smokeinfo.1
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::EchoPingSmtp > Smokeping_probes_EchoPingSmtp.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_EchoPingSmtp.pod --section 3 > Smokeping_probes_EchoPingSmtp.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::OpenSSHJunOSPing > Smokeping_probes_OpenSSHJunOSPing.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_OpenSSHJunOSPing.pod --section 3 > Smokeping_probes_OpenSSHJunOSPing.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::skel > Smokeping_probes_skel.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_skel.pod --section 3 > Smokeping_probes_skel.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::EchoPingWhois > Smokeping_probes_EchoPingWhois.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_EchoPingWhois.pod --section 3 > Smokeping_probes_EchoPingWhois.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::EchoPingHttp > Smokeping_probes_EchoPingHttp.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_EchoPingHttp.pod --section 3 > Smokeping_probes_EchoPingHttp.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::TelnetIOSPing > Smokeping_probes_TelnetIOSPing.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_TelnetIOSPing.pod --section 3 > Smokeping_probes_TelnetIOSPing.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::EchoPingDiscard > Smokeping_probes_EchoPingDiscard.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_EchoPingDiscard.pod --section 3 > Smokeping_probes_EchoPingDiscard.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::CiscoRTTMonDNS > Smokeping_probes_CiscoRTTMonDNS.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_CiscoRTTMonDNS.pod --section 3 > Smokeping_probes_CiscoRTTMonDNS.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::IOSPing > Smokeping_probes_IOSPing.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_IOSPing.pod --section 3 > Smokeping_probes_IOSPing.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::AnotherCurl > Smokeping_probes_AnotherCurl.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_AnotherCurl.pod --section 3 > Smokeping_probes_AnotherCurl.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::FPing > Smokeping_probes_FPing.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_FPing.pod --section 3 > Smokeping_probes_FPing.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::TraceroutePing > Smokeping_probes_TraceroutePing.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_TraceroutePing.pod --section 3 > Smokeping_probes_TraceroutePing.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::TacacsPlus > Smokeping_probes_TacacsPlus.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_TacacsPlus.pod --section 3 > Smokeping_probes_TacacsPlus.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::RemoteFPing > Smokeping_probes_RemoteFPing.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_RemoteFPing.pod --section 3 > Smokeping_probes_RemoteFPing.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::Curl > Smokeping_probes_Curl.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_Curl.pod --section 3 > Smokeping_probes_Curl.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::basevars > Smokeping_probes_basevars.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_basevars.pod --section 3 > Smokeping_probes_basevars.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::EchoPingIcp > Smokeping_probes_EchoPingIcp.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_EchoPingIcp.pod --section 3 > Smokeping_probes_EchoPingIcp.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::Qstat > Smokeping_probes_Qstat.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_Qstat.pod --section 3 > Smokeping_probes_Qstat.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::base > Smokeping_probes_base.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_base.pod --section 3 > Smokeping_probes_base.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::WebProxyFilter > Smokeping_probes_WebProxyFilter.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_WebProxyFilter.pod --section 3 > Smokeping_probes_WebProxyFilter.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::basefork > Smokeping_probes_basefork.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_basefork.pod --section 3 > Smokeping_probes_basefork.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::FPingContinuous > Smokeping_probes_FPingContinuous.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_FPingContinuous.pod --section 3 > Smokeping_probes_FPingContinuous.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::TCPPing > Smokeping_probes_TCPPing.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_TCPPing.pod --section 3 > Smokeping_probes_TCPPing.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::EchoPingLDAP > Smokeping_probes_EchoPingLDAP.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_EchoPingLDAP.pod --section 3 > Smokeping_probes_EchoPingLDAP.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::SSH > Smokeping_probes_SSH.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_SSH.pod --section 3 > Smokeping_probes_SSH.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::EchoPingHttps > Smokeping_probes_EchoPingHttps.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_EchoPingHttps.pod --section 3 > Smokeping_probes_EchoPingHttps.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::TelnetJunOSPing > Smokeping_probes_TelnetJunOSPing.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_TelnetJunOSPing.pod --section 3 > Smokeping_probes_TelnetJunOSPing.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::SendEmail > Smokeping_probes_SendEmail.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_SendEmail.pod --section 3 > Smokeping_probes_SendEmail.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::passwordchecker > Smokeping_probes_passwordchecker.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_passwordchecker.pod --section 3 > Smokeping_probes_passwordchecker.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::EchoPing > Smokeping_probes_EchoPing.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_EchoPing.pod --section 3 > Smokeping_probes_EchoPing.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::AnotherDNS > Smokeping_probes_AnotherDNS.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_AnotherDNS.pod --section 3 > Smokeping_probes_AnotherDNS.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::CiscoRTTMonTcpConnect > Smokeping_probes_CiscoRTTMonTcpConnect.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_CiscoRTTMonTcpConnect.pod --section 3 > Smokeping_probes_CiscoRTTMonTcpConnect.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::SipSak > Smokeping_probes_SipSak.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_SipSak.pod --section 3 > Smokeping_probes_SipSak.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::LDAP > Smokeping_probes_LDAP.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_LDAP.pod --section 3 > Smokeping_probes_LDAP.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::FPing6 > Smokeping_probes_FPing6.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_FPing6.pod --section 3 > Smokeping_probes_FPing6.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::IRTT > Smokeping_probes_IRTT.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_IRTT.pod --section 3 > Smokeping_probes_IRTT.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::NFSping > Smokeping_probes_NFSping.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_NFSping.pod --section 3 > Smokeping_probes_NFSping.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::EchoPingPlugin > Smokeping_probes_EchoPingPlugin.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_EchoPingPlugin.pod --section 3 > Smokeping_probes_EchoPingPlugin.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::Radius > Smokeping_probes_Radius.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_Radius.pod --section 3 > Smokeping_probes_Radius.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::AnotherSSH > Smokeping_probes_AnotherSSH.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_AnotherSSH.pod --section 3 > Smokeping_probes_AnotherSSH.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::CiscoRTTMonEchoICMP > Smokeping_probes_CiscoRTTMonEchoICMP.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_CiscoRTTMonEchoICMP.pod --section 3 > Smokeping_probes_CiscoRTTMonEchoICMP.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::EchoPingDNS > Smokeping_probes_EchoPingDNS.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_EchoPingDNS.pod --section 3 > Smokeping_probes_EchoPingDNS.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::DismanPing > Smokeping_probes_DismanPing.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_DismanPing.pod --section 3 > Smokeping_probes_DismanPing.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::OpenSSHEOSPing > Smokeping_probes_OpenSSHEOSPing.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_OpenSSHEOSPing.pod --section 3 > Smokeping_probes_OpenSSHEOSPing.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::DNS > Smokeping_probes_DNS.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_DNS.pod --section 3 > Smokeping_probes_DNS.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::FTPtransfer > Smokeping_probes_FTPtransfer.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_FTPtransfer.pod --section 3 > Smokeping_probes_FTPtransfer.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod Smokeping::probes::EchoPingChargen > Smokeping_probes_EchoPingChargen.pod
pod2man --release=2.8.2 --center=SmokePing Smokeping_probes_EchoPingChargen.pod --section 3 > Smokeping_probes_EchoPingChargen.3
pod2man --release=2.8.2 --center=SmokePing ../lib/Smokeping/matchers/CheckLoss.pm --section 3 > Smokeping_matchers_CheckLoss.3
pod2man --release=2.8.2 --center=SmokePing ../lib/Smokeping/matchers/Avgratio.pm --section 3 > Smokeping_matchers_Avgratio.3
pod2man --release=2.8.2 --center=SmokePing ../lib/Smokeping/matchers/CheckLatency.pm --section 3 > Smokeping_matchers_CheckLatency.3
pod2man --release=2.8.2 --center=SmokePing ../lib/Smokeping/matchers/ConsecutiveLoss.pm --section 3 > Smokeping_matchers_ConsecutiveLoss.3
pod2man --release=2.8.2 --center=SmokePing ../lib/Smokeping/matchers/base.pm --section 3 > Smokeping_matchers_base.3
pod2man --release=2.8.2 --center=SmokePing ../lib/Smokeping/matchers/Median.pm --section 3 > Smokeping_matchers_Median.3
pod2man --release=2.8.2 --center=SmokePing ../lib/Smokeping/matchers/ExpLoss.pm --section 3 > Smokeping_matchers_ExpLoss.3
pod2man --release=2.8.2 --center=SmokePing ../lib/Smokeping/matchers/Medratio.pm --section 3 > Smokeping_matchers_Medratio.3
pod2man --release=2.8.2 --center=SmokePing ../lib/Smokeping/sorters/base.pm --section 3 > Smokeping_sorters_base.3
pod2man --release=2.8.2 --center=SmokePing ../lib/Smokeping/sorters/Median.pm --section 3 > Smokeping_sorters_Median.3
pod2man --release=2.8.2 --center=SmokePing ../lib/Smokeping/sorters/Max.pm --section 3 > Smokeping_sorters_Max.3
pod2man --release=2.8.2 --center=SmokePing ../lib/Smokeping/sorters/Loss.pm --section 3 > Smokeping_sorters_Loss.3
pod2man --release=2.8.2 --center=SmokePing ../lib/Smokeping/sorters/StdDev.pm --section 3 > Smokeping_sorters_StdDev.3
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5 -I../lib -mSmokeping -e 'Smokeping::main()' -- --makepod > smokeping_config.pod
pod2man --release=2.8.2 --center=SmokePing smokeping_config.pod --section 5 > smokeping_config.5
/usr/bin/mkdir -p examples
PERL5LIB= /usr/bin/perl -I../thirdparty/lib/perl5  -I../lib -mSmokeping -e 'Smokeping::main()' -- --gen-examples
Generating example files...
        examples/config.simple ...
        examples/config.multiple-probes ...
        examples/config.fping-instances ...
        examples/config.targetvars-with-Curl ...
        examples/config.echoping ...
        examples/config.template ...
        smokeping_examples.pod ...
done.
pod2man --release=2.8.2 --center=SmokePing smokeping_examples.pod --section 5 > smokeping_examples.5
pod2man --release=2.8.2 --center=SmokePing smokeping_extend.pod --section 7 > smokeping_extend.7
pod2man --release=2.8.2 --center=SmokePing smokeping_install.pod --section 7 > smokeping_install.7
pod2man --release=2.8.2 --center=SmokePing smokeping_master_slave.pod --section 7 > smokeping_master_slave.7
pod2man --release=2.8.2 --center=SmokePing smokeping_upgrade.pod --section 7 > smokeping_upgrade.7
make[2]: Entering directory '/root/smokeping-2.8.2/doc'
make[2]: Nothing to be done for 'install-exec-am'.
 /usr/bin/mkdir -p '/opt/smokeping/etc/examples'
 /usr/bin/install -c -m 644 examples/config.fping-instances examples/config.multiple-probes examples/config.simple examples/config.echoping examples/config.template examples/config.targetvars-with-Curl '/opt/smokeping/etc/examples'
 /usr/bin/mkdir -p '/opt/smokeping/share/man/man1'
 /usr/bin/install -c -m 644 smokeping.1 smokeping_cgi.1 tSmoke.1 smokeinfo.1 '/opt/smokeping/share/man/man1'
 /usr/bin/mkdir -p '/opt/smokeping/share/man/man3'
 /usr/bin/install -c -m 644 Smokeping_probes_EchoPingSmtp.3 Smokeping_probes_OpenSSHJunOSPing.3 Smokeping_probes_skel.3 Smokeping_probes_EchoPingWhois.3 Smokeping_probes_EchoPingHttp.3 Smokeping_probes_TelnetIOSPing.3 Smokeping_probes_EchoPingDiscard.3 Smokeping_probes_CiscoRTTMonDNS.3 Smokeping_probes_IOSPing.3 Smokeping_probes_AnotherCurl.3 Smokeping_probes_FPing.3 Smokeping_probes_TraceroutePing.3 Smokeping_probes_TacacsPlus.3 Smokeping_probes_RemoteFPing.3 Smokeping_probes_Curl.3 Smokeping_probes_basevars.3 Smokeping_probes_EchoPingIcp.3 Smokeping_probes_Qstat.3 Smokeping_probes_base.3 Smokeping_probes_WebProxyFilter.3 Smokeping_probes_basefork.3 Smokeping_probes_FPingContinuous.3 Smokeping_probes_TCPPing.3 Smokeping_probes_EchoPingLDAP.3 Smokeping_probes_SSH.3 Smokeping_probes_EchoPingHttps.3 Smokeping_probes_TelnetJunOSPing.3 Smokeping_probes_SendEmail.3 Smokeping_probes_passwordchecker.3 Smokeping_probes_EchoPing.3 Smokeping_probes_AnotherDNS.3 Smokeping_probes_CiscoRTTMonTcpConnect.3 Smokeping_probes_SipSak.3 Smokeping_probes_LDAP.3 Smokeping_probes_FPing6.3 Smokeping_probes_IRTT.3 Smokeping_probes_NFSping.3 Smokeping_probes_EchoPingPlugin.3 Smokeping_probes_Radius.3 Smokeping_probes_AnotherSSH.3 '/opt/smokeping/share/man/man3'
 /usr/bin/install -c -m 644 Smokeping_probes_CiscoRTTMonEchoICMP.3 Smokeping_probes_EchoPingDNS.3 Smokeping_probes_DismanPing.3 Smokeping_probes_OpenSSHEOSPing.3 Smokeping_probes_DNS.3 Smokeping_probes_FTPtransfer.3 Smokeping_probes_EchoPingChargen.3 Smokeping_matchers_CheckLoss.3 Smokeping_matchers_Avgratio.3 Smokeping_matchers_CheckLatency.3 Smokeping_matchers_ConsecutiveLoss.3 Smokeping_matchers_base.3 Smokeping_matchers_Median.3 Smokeping_matchers_ExpLoss.3 Smokeping_matchers_Medratio.3 Smokeping_sorters_base.3 Smokeping_sorters_Median.3 Smokeping_sorters_Max.3 Smokeping_sorters_Loss.3 Smokeping_sorters_StdDev.3 '/opt/smokeping/share/man/man3'
 /usr/bin/mkdir -p '/opt/smokeping/share/man/man5'
 /usr/bin/install -c -m 644 smokeping_config.5 smokeping_examples.5 '/opt/smokeping/share/man/man5'
 /usr/bin/mkdir -p '/opt/smokeping/share/man/man7'
 /usr/bin/install -c -m 644 smokeping_extend.7 smokeping_install.7 smokeping_master_slave.7 smokeping_upgrade.7 '/opt/smokeping/share/man/man7'
make[2]: Leaving directory '/root/smokeping-2.8.2/doc'
rm Smokeping_probes_IOSPing.pod Smokeping_probes_EchoPing.pod Smokeping_probes_SipSak.pod Smokeping_probes_EchoPingPlugin.pod Smokeping_probes_SSH.pod Smokeping_probes_FPing6.pod Smokeping_probes_EchoPingIcp.pod Smokeping_probes_Curl.pod Smokeping_probes_CiscoRTTMonDNS.pod Smokeping_probes_EchoPingDNS.pod Smokeping_probes_Qstat.pod Smokeping_probes_DismanPing.pod Smokeping_probes_IRTT.pod Smokeping_probes_WebProxyFilter.pod Smokeping_probes_RemoteFPing.pod Smokeping_probes_OpenSSHJunOSPing.pod Smokeping_probes_EchoPingLDAP.pod Smokeping_probes_LDAP.pod Smokeping_probes_TacacsPlus.pod Smokeping_probes_TelnetIOSPing.pod Smokeping_probes_NFSping.pod Smokeping_probes_basefork.pod Smokeping_probes_OpenSSHEOSPing.pod Smokeping_probes_EchoPingChargen.pod Smokeping_probes_basevars.pod Smokeping_probes_EchoPingSmtp.pod Smokeping_probes_FPing.pod Smokeping_probes_TraceroutePing.pod Smokeping_probes_FTPtransfer.pod Smokeping_probes_EchoPingHttps.pod Smokeping_probes_EchoPingDiscard.pod Smokeping_probes_AnotherSSH.pod Smokeping_probes_CiscoRTTMonEchoICMP.pod Smokeping_probes_passwordchecker.pod Smokeping_probes_base.pod Smokeping_probes_TelnetJunOSPing.pod Smokeping_probes_SendEmail.pod Smokeping_probes_EchoPingHttp.pod Smokeping_probes_AnotherDNS.pod Smokeping_probes_Radius.pod Smokeping_probes_AnotherCurl.pod Smokeping_probes_TCPPing.pod Smokeping_probes_EchoPingWhois.pod Smokeping_probes_skel.pod Smokeping_probes_DNS.pod Smokeping_probes_FPingContinuous.pod Smokeping_probes_CiscoRTTMonTcpConnect.pod
make[1]: Leaving directory '/root/smokeping-2.8.2/doc'
Making install in etc
make[1]: Entering directory '/root/smokeping-2.8.2/etc'
make[2]: Entering directory '/root/smokeping-2.8.2/etc'
make[2]: Nothing to be done for 'install-exec-am'.
 /usr/bin/mkdir -p '/opt/smokeping/etc'
 /usr/bin/install -c -m 644 basepage.html.dist config.dist smokemail.dist smokeping_secrets.dist tmail.dist '/opt/smokeping/etc'
make[2]: Leaving directory '/root/smokeping-2.8.2/etc'
make[1]: Leaving directory '/root/smokeping-2.8.2/etc'
Making install in htdocs
make[1]: Entering directory '/root/smokeping-2.8.2/htdocs'
make[2]: Entering directory '/root/smokeping-2.8.2/htdocs'
make[2]: Nothing to be done for 'install-exec-am'.
/usr/bin/mkdir -p /opt/smokeping/htdocs
/usr/bin/echo   "#!/bin/sh" > /opt/smokeping/htdocs/smokeping.fcgi.dist
/usr/bin/echo   "exec /opt/smokeping/bin/smokeping_cgi /opt/smokeping/etc/config" >> /opt/smokeping/htdocs/smokeping.fcgi.dist
chmod +x /opt/smokeping/htdocs/smokeping.fcgi.dist
 /usr/bin/mkdir -p '/opt/smokeping/htdocs'
 /usr/bin/mkdir -p '/opt/smokeping/htdocs/js'
 /usr/bin/install -c -m 644  js/smokeping.js js/prototype.js '/opt/smokeping/htdocs/js'
 /usr/bin/mkdir -p '/opt/smokeping/htdocs/js/scriptaculous'
 /usr/bin/install -c -m 644  js/scriptaculous/controls.js js/scriptaculous/slider.js js/scriptaculous/sound.js js/scriptaculous/effects.js js/scriptaculous/unittest.js js/scriptaculous/builder.js js/scriptaculous/scriptaculous.js js/scriptaculous/dragdrop.js '/opt/smokeping/htdocs/js/scriptaculous'
 /usr/bin/mkdir -p '/opt/smokeping/htdocs/js/cropper'
 /usr/bin/install -c -m 644  js/cropper/cropper.js js/cropper/licence.txt js/cropper/marqueeVert.gif js/cropper/cropper.uncompressed.js js/cropper/cropper.css js/cropper/marqueeHoriz.gif '/opt/smokeping/htdocs/js/cropper'
 /usr/bin/mkdir -p '/opt/smokeping/htdocs/css'
 /usr/bin/install -c -m 644  css/smokeping-print.css css/smokeping-screen.css '/opt/smokeping/htdocs/css'
make[2]: Leaving directory '/root/smokeping-2.8.2/htdocs'
make[1]: Leaving directory '/root/smokeping-2.8.2/htdocs'
make[1]: Entering directory '/root/smokeping-2.8.2'
make[2]: Entering directory '/root/smokeping-2.8.2'
make[2]: Nothing to be done for 'install-exec-am'.
make[2]: Nothing to be done for 'install-data-am'.
make[2]: Leaving directory '/root/smokeping-2.8.2'
make[1]: Leaving directory '/root/smokeping-2.8.2'
```

</details>

``` bash
[root@cn-py-dl-c8 smokeping]#  ./bin/smokeping --config=/opt/smokeping/etc/config --debug
ERROR: /opt/smokeping/etc/config, line 6: File '/usr/sbin/sendmail' does not exist
[root@cn-py-dl-c8 smokeping]# vim etc/config
[root@cn-py-dl-c8 smokeping]#  ./bin/smokeping --config=/opt/smokeping/etc/config --debug
ERROR: /opt/smokeping/etc/config, line 10: Directory '/var/lib/smokeping/images' does not exist
[root@cn-py-dl-c8 smokeping]# mkdir /var/lib/smokeping/images
mkdir: cannot create directory ‘/var/lib/smokeping/images’: No such file or directory
[root@cn-py-dl-c8 smokeping]# mkdir /var/lib/smokeping
[root@cn-py-dl-c8 smokeping]# mkdir /var/lib/smokeping/images
[root@cn-py-dl-c8 smokeping]#  ./bin/smokeping --config=/opt/smokeping/etc/config --debug
ERROR: /opt/smokeping/etc/config, line 12: Directory '/var/lib/smokeping/rrd' does not exist
[root@cn-py-dl-c8 smokeping]# mkdir /var/lib/smokeping/rrd
[root@cn-py-dl-c8 smokeping]#  ./bin/smokeping --config=/opt/smokeping/etc/config --debug
ERROR: /opt/smokeping/etc/config, line 13: Directory '/var/run/smokeping' does not exist
[root@cn-py-dl-c8 smokeping]# mkdir /var/run/smokeping
[root@cn-py-dl-c8 smokeping]#  ./bin/smokeping --config=/opt/smokeping/etc/config --debug
ERROR: /opt/smokeping/etc/config, line 15: File '/etc/smokeping/smokemail' does not exist
[root@cn-py-dl-c8 smokeping]#  ./bin/smokeping --config=/opt/smokeping/etc/config --debug
ERROR: /opt/smokeping/etc/config, line 16: File '/etc/smokeping/tmail' does not exist
[root@cn-py-dl-c8 smokeping]#  ./bin/smokeping --config=/opt/smokeping/etc/config --debug
ERROR: /opt/smokeping/etc/config, line 50: template '/etc/smokeping/basepage.html' not readable
[root@cn-py-dl-c8 etc]# mv basepage.html.dist basepage.html
```

## 0x08.引用
> [ifconfig命令不存在command not found](https://web.archive.org/web/20191028144703/https://blog.csdn.net/dong_alex/article/details/80873733)
[CentOS7安装VMware Tools](https://web.archive.org/web/20200404101734/https://www.cnblogs.com/roooookie/p/8473640.html)

未完待续……