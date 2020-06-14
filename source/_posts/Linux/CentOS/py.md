---
title: PY 云新增 CentOS 7.7 64 位
date: 2019-10-28 23:13:25
tags:
  - CentOS 
count: 2
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
[root@localhost ~]# rpm -q centos-release
centos-release-7-7.1908.0.el7.centos.x86_64
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
[root@localhost ~]# cat /etc/sysconfig/network-scripts/ifcfg-ens192 
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
IPADDR=192.168.25.7
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
[root@py ~]# dpkg -i smartdns.1.2020.02.25-2212.x86_64-linux-all.tar.gz 
-bash: dpkg: command not found
[root@py ~]# tar zxf smartdns.1.2020.02.25-2212.x86_64-linux-all.tar.gz 
[root@py ~]# cd smartdns
[root@py smartdns]# chmod +x ./install
[root@py smartdns]# ./install -i
install: creating directory ‘/etc/smartdns’
‘src/smartdns’ -> ‘/usr/sbin/smartdns’
‘etc/smartdns/smartdns.conf’ -> ‘/etc/smartdns/smartdns.conf’
‘etc/default/smartdns’ -> ‘/etc/default/smartdns’
‘etc/init.d/smartdns’ -> ‘/etc/init.d/smartdns’
‘systemd/smartdns.service’ -> ‘/usr/lib/systemd/system/smartdns.service’
Created symlink from /etc/systemd/system/smartdns.service to /usr/lib/systemd/system/smartdns.service.
Created symlink from /etc/systemd/system/multi-user.target.wants/smartdns.service to /usr/lib/systemd/system/smartdns.service.
[root@py smartdns]# vim /etc/smartdns/smartdns.conf
[root@py smartdns]# vim /etc/smartdns/smartdns.conf
[root@py smartdns]# cd /var/log
[root@py log]# mkdir smartdns
[root@py log]# systemctl enable smartdns
[root@py log]# systemctl status smartdns
```
配置文件

<details><summary>点击此处 ← 查看折叠</summary>

``` bash
 cat /etc/smartdns/smartdns.conf                                            ✔  pi@rpi  21:09:26 
# dns server name, defaut is host name
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
cache-size 1024

# prefetch domain
# prefetch-domain [yes|no]
prefetch-domain yes

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
# force-AAAA-SOA yes

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
log-file /var/log/smartdns.log
log-size 1024k
log-num 10

# dns audit
# audit-enable [yes|no]: enable or disable audit.
audit-enable yes
# audit-SOA [yes|no]: enable or disalbe log soa result.
# audit-size size of each audit file, support k,m,g
audit-file /var/log/smartdns-audit.log
audit-size 1024k
audit-num 10

# remote udp dns server list
# server [IP]:[PORT] [-blacklist-ip] [-whitelist-ip] [-check-edns] [-group [group] ...] [-exclude-default-group]
# default port is 53
#   -blacklist-ip: filter result with blacklist ip
#   -whitelist-ip: filter result whth whitelist ip,  result in whitelist-ip will be accepted.
#   -check-edns: result must exist edns RR, or discard result.
#   -group [group]: set server to group, use with nameserver /domain/group.
#   -exclude-default-group: exclude this server from default group.
# server 8.8.8.8 -blacklist-ip -check-edns -group g1 -group g2
server 114.114.114.114
server 1.1.1.1
server 8.8.8.8
server 192.168.25.248
server 219.149.6.99
server 240c::6666
server 240e:41:c900:ffff::

# remote tcp dns server list
# server-tcp [IP]:[PORT] [-blacklist-ip] [-whitelist-ip] [-group [group] ...] [-exclude-default-group]
# default port is 53
# server-tcp 114.114.114.114 1.1.1.1 8.8.8.8 240c::6666

# remote tls dns server list
# server-tls [IP]:[PORT] [-blacklist-ip] [-whitelist-ip] [-spki-pin [sha256-pin]] [-group [group] ...] [-exclude-default-group]
#   -spki-pin: TLS spki pin to verify.
#   -tls-host-check: cert hostname to verify.
#   -hostname: TLS sni hostname.
# Get SPKI with this command:
#    echo | openssl s_client -connect '[ip]:853' | openssl x509 -pubkey -noout | openssl pkey -pubin -outform der | openssl dgst -sha256 -binary | openssl enc -base64
# default port is 853
# server-tls 8.8.8.8
# server-tls 1.0.0.1

# remote https dns server list
# server-https https://[host]:[port]/path [-blacklist-ip] [-whitelist-ip] [-spki-pin [sha256-pin]] [-group [group] ...] [-exclude-default-group]
#   -spki-pin: TLS spki pin to verify.
#   -tls-host-check: cert hostname to verify.
#   -hostname: TLS sni hostname.
#   -http-host: http host.
# default port is 443
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

## 0x07.引用
> [ifconfig命令不存在command not found](https://web.archive.org/web/20191028144703/https://blog.csdn.net/dong_alex/article/details/80873733)
[CentOS7安装VMware Tools](https://web.archive.org/web/20200404101734/https://www.cnblogs.com/roooookie/p/8473640.html)

未完待续……