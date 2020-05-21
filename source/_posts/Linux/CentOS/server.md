---
title: 换新系统之腾讯云学生机 CentOS 7.6 64 位
date: 2019-5-9 18:22:34
tags:
  - CentOS
  - server
count: 5
os: 0
os_1: 10.0.17763.437 2019-LTSC
browser: 0
browser_1: 72.0.3626.121 Stable
place: 家
key: 50
---
    然后原来的一元机就换系统了……
<!-- more -->
## 0x00.修改主机名
``` bash
[root@txy ~]# hostnamectl set-hostname txy.yuangezhizao.cn
[root@txy ~]# hostname
txy.yuangezhizao.cn
[root@txy ~]# cat /etc/hosts
127.0.0.1 txy.yuangezhizao.cn txy.yuangezhizao.cn
127.0.0.1 localhost.localdomain localhost
127.0.0.1 localhost4.localdomain4 localhost4

::1 txy.yuangezhizao.cn txy.yuangezhizao.cn
::1 localhost.localdomain localhost
::1 localhost6.localdomain6 localhost6
[root@txy ~]# reboot
```

## 0x01.软件
``` bash
yum update -y
yum install htop screen git axel iftop lsof -y
```
1. `nfs-utils`：暂时`10G`免费
![腾讯云文件系统](https://i1.yuangezhizao.cn/Win-10/20190509232645.jpg!webp)

2. `COSFS`：https://github.com/tencentyun/cosfs
![直接在本地是相当爽了，可惜 Win 享受不到](https://i1.yuangezhizao.cn/Win-10/20190509232817.jpg!webp)

## 0x03.挂载第三方存储
1. 腾讯云文件存储即`CFS`
2. 腾讯云对象存储即`COS`
![白嫖的一年资源包](https://i1.yuangezhizao.cn/Win-10/20190509233243.jpg!webp)
![最终效果可以说是相当爽了](https://i1.yuangezhizao.cn/Win-10/20190509224926.jpg!webp)

## 0x04.编译安装[python383](https://www.python.org/downloads/release/python-383/)环境
1. 查看现有位置
``` bash
[root@txy ~]# whereis python
python: /usr/bin/python /usr/bin/python2.7 /usr/lib/python2.7 /usr/lib64/python2.7 /etc/python /usr/include/python2.7 /usr/local/python3/bin/python3.8-config /usr/local/python3/bin/python3.8 /usr/share/man/man1/python.1.gz
```
2. 安装编译工具
~~`yum groupinstall 'Development Tools' -y`~~
``` bash
yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc make libffi-devel -y
```
> 这里面有一个包很关键`libffi-devel`，因为只有`3.7`才会用到这个包，如果不安装这个包的话，在`make`阶段会出现如下的报错：`# ModuleNotFoundError: No module named '_ctypes'`

3. 下载源码包
~~`wget --no-check-certificate https://www.python.org/ftp/python/3.8.3/Python-3.8.3.tar.xz`~~
![下载卡爆，jsproxy 启动！](https://i1.yuangezhizao.cn/Win-10/20191016210358.jpg!webp)

``` bash
CloudFlare：
wget https://v2.yuangezhizao.cn/dl/Python-3.8.3.tar.xz
Skysilk：
wget http://proxy.yuangezhizao.cn/dl/Python-3.8.3.tar.xz
```
4. 解压
``` bash
tar xvJf Python-3.8.3.tar.xz
cd Python-3.8.3
```
5. 编译
注：添加`--enable-optimizations`（编译器优化）之后的编译速度会变慢，但理论上编译产物的运行效率？会提高
不添加`--enable-shared`（生成动态链接库）编译会报错：`command 'gcc' failed with exit status 1`
``` bash
rm -rf /usr/local/python3
./configure --prefix=/usr/local/python3 --enable-shared --enable-optimizations
make && make install
```
6. 修复
添加`--enable-shared`编译之后会报找不到`so`的错误，此时可利用`ldd`工具查看详细
``` bash
[root@txy ~]# python3 -V
python3: error while loading shared libraries: libpython3.8.so.1.0: cannot open shared object file: No such file or directory
[root@txy ~]# cd /usr/local/python3/bin/
[root@txy bin]# ls
2to3  2to3-3.8  easy_install-3.8  idle3  idle3.8  pip3  pip3.8  pydoc3  pydoc3.8  python3  python3.8  python3.8-config  python3-config
[root@txy bin]# ldd python3.8
        linux-vdso.so.1 =>  (0x00007ffd24de9000)
        libpython3.8.so.1.0 => not found
        libcrypt.so.1 => /lib64/libcrypt.so.1 (0x00007f9e9dd3c000)
        libpthread.so.0 => /lib64/libpthread.so.0 (0x00007f9e9db20000)
        libdl.so.2 => /lib64/libdl.so.2 (0x00007f9e9d91c000)
        libutil.so.1 => /lib64/libutil.so.1 (0x00007f9e9d719000)
        libm.so.6 => /lib64/libm.so.6 (0x00007f9e9d417000)
        libc.so.6 => /lib64/libc.so.6 (0x00007f9e9d049000)
        libfreebl3.so => /lib64/libfreebl3.so (0x00007f9e9ce46000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f9e9df73000)
```
需要手动将所缺`so`库`libpython3.8.so.1.0`移至库目录下，具体生效路径为：`/usr/lib64/`，这里测试`/usr/lib/`、`/usr/local/lib/`、`/usr/local/lib64/`均无效……
``` bash
[root@txy ~]# cp libpython3.8.so.1.0 /usr/lib64/
[root@txy ~]# python3 -V
Python 3.8.3
```
7. 创建软链接（`python3`&`pip3`）
此法不会破坏自带`py`环境，因此无需修改任何`yum`文件
~~注：更改`yum`配置~~
~~`vim /usr/bin/yum`~~
~~`vim /usr/libexec/urlgrabber-ext-down`~~
~~`vim /bin/yum-config-manager`~~
~~把`#! /usr/bin/python`修改为`#! /usr/bin/python2`~~
``` bash
……
Collecting setuptools
Collecting pip
Installing collected packages: setuptools, pip
Successfully installed pip-19.2.3 setuptools-41.2.0
[root@txy Python-3.8.2]# ln -s /usr/local/python3/bin/python3 /usr/bin/python3
ln: failed to create symbolic link ‘/usr/bin/python3’: File exists
[root@txy Python-3.8.2]# rm -rf /usr/bin/python3
[root@txy Python-3.8.2]# ln -s /usr/local/python3/bin/python3 /usr/bin/python3
[root@txy Python-3.8.2]# ln -s /usr/local/python3/bin/pip3.8 /usr/bin/pip3
ln: failed to create symbolic link ‘/usr/bin/pip3’: File exists
[root@txy Python-3.8.2]# rm -rf /usr/bin/pip3
[root@txy Python-3.8.2]# ln -s /usr/local/python3/bin/pip3.8 /usr/bin/pip3
[root@txy Python-3.8.2]# python -V
Python 2.7.5
[root@txy Python-3.8.2]# python2 -V
Python 2.7.5
[root@txy Python-3.8.2]# python3 -V
Python 3.8.2
[root@txy Python-3.8.2]# pip -V
-bash: pip: command not found
[root@txy Python-3.8.2]# pip2 -V
-bash: pip2: command not found
[root@txy Python-3.8.2]# pip3 -V
pip 19.2.3 from /usr/local/python3/lib/python3.8/site-packages/pip (python 3.8)
[root@txy Python-3.8.2]# python3
Python 3.8.2 (default, Feb 27 2020, 22:56:59) 
[GCC 4.8.5 20150623 (Red Hat 4.8.5-39)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
[1]+  Stopped                 python3
[root@txy Python-3.8.2]# 
```
> 这样就可以通过`python`/`python2`命令使用`Python`，`python3`来使用`Python 3`

8. 升级`pip3`
你云环境下会自动配置镜像源
``` bash
[root@txy Python-3.8.2]# pip3 install --upgrade pip
Looking in indexes: http://mirrors.tencentyun.com/pypi/simple
Collecting pip
  Downloading http://mirrors.tencentyun.com/pypi/packages/54/0c/d01aa759fdc501a58f431eb594a17495f15b88da142ce14b5845662c13f3/pip-20.0.2-py2.py3-none-any.whl (1.4MB)
     |████████████████████████████████| 1.4MB 661kB/s 
Installing collected packages: pip
  Found existing installation: pip 19.2.3
    Uninstalling pip-19.2.3:
      Successfully uninstalled pip-19.2.3
Successfully installed pip-20.0.2
```
安装`pip3`的另一种方法
``` bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```
9. 加入环境变量
``` bash
[root@txy ~]# cat ~/.bash_profile
# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
	. ~/.bashrc
fi

# User specific environment and startup programs

PATH=$PATH:$HOME/bin:/usr/local/python3/bin

export PATH
```

## 0x05.安装[Docker](https://docs.docker.com/install/linux/docker-ce/centos/)
1. 卸载旧版本
``` bash
sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine
```
2. 使用源安装
`sudo yum install -y yum-utils device-mapper-persistent-data lvm2`
`sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo`
3. 安装
`sudo yum install docker-ce docker-ce-cli containerd.io`
4. 启动
`sudo systemctl start docker`
5. 测试
`sudo docker run hello-world`
输出如下：
``` bash
[root@txy ~]# docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
1b930d010525: Pull complete 
Digest: sha256:6f744a2005b12a704d2608d8070a494ad1145636eeb74a570c56b94d94ccdbfc
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
```
6. 加速器
`curl -sSL https://get.daocloud.io/daotools/set_mirror.sh | sh -s http://e6d6fb48.m.daocloud.io`
7. 自启
`sudo systemctl enable docker`

## 0x06. 测速工具`speedtest-cli`
`pip3 install speedtest-cli`
``` bash
[root@txy ~]# speedtest-cli
Retrieving speedtest.net configuration...
Testing from Tencent cloud computing (<rm>)...
Retrieving speedtest.net server list...
Selecting best server based on ping...
Hosted by Beijing Unicom (Beijing) [1.69 km]: 28.199 ms
Testing download speed................................................................................
Download: 86.21 Mbit/s
Testing upload speed......................................................................................................
Upload: 1.27 Mbit/s
```

## 0x07.安装[PHPStudy Linux 面板](https://www.xp.cn/linux.html)
![官网](https://i1.yuangezhizao.cn/Win-10/20191016213712.jpg!webp)
![V0.2 公测版](https://i1.yuangezhizao.cn/Win-10/20191016213828.jpg!webp)

一键安装
`yum install -y wget && wget -O install.sh https://download.xp.cn/install.sh && sh install.sh`
![还不错的面板](https://i1.yuangezhizao.cn/Win-10/20191016214057.jpg!webp)
![吊炸天的监控](https://i1.yuangezhizao.cn/Win-10/20191016214130.jpg!webp)

## 0x08.编译安装[Nginx](https://nginx.org/)
准备
`mkdir nginx_build && cd nginx_build`
下载`1.17.3`版本`Nginx`源码
`wget http://nginx.org/download/nginx-1.17.3.tar.gz`
`tar -xvf nginx-1.17.3.tar.gz`
下载`0.1.18`版本`nginx-module-vts`源码
`wget https://github.com/vozlt/nginx-module-vts/archive/v0.1.18.tar.gz`
`tar -xvf v0.1.18.tar.gz`
安装依赖
`yum -y install gcc gcc-c++ pcre pcre-devel zlib zlib-devel openssl openssl-devel`
编译安装
`cd nginx-1.17.3/`
``` bash
[root@txy nginx-1.17.3]# ./configure --add-module=/root/nginx_build/nginx-module-vts-0.1.18
checking for OS
 + Linux 3.10.0-957.21.3.el7.x86_64 x86_64
checking for C compiler ... found
 + using GNU C compiler
 + gcc version: 4.8.5 20150623 (Red Hat 4.8.5-39) (GCC) 
checking for gcc -pipe switch ... found
checking for -Wl,-E switch ... found
checking for gcc builtin atomic operations ... found
checking for C99 variadic macros ... found
checking for gcc variadic macros ... found
checking for gcc builtin 64 bit byteswap ... found
checking for unistd.h ... found
checking for inttypes.h ... found
checking for limits.h ... found
checking for sys/filio.h ... not found
checking for sys/param.h ... found
checking for sys/mount.h ... found
checking for sys/statvfs.h ... found
checking for crypt.h ... found
checking for Linux specific features
checking for epoll ... found
checking for EPOLLRDHUP ... found
checking for EPOLLEXCLUSIVE ... not found
checking for O_PATH ... found
checking for sendfile() ... found
checking for sendfile64() ... found
checking for sys/prctl.h ... found
checking for prctl(PR_SET_DUMPABLE) ... found
checking for prctl(PR_SET_KEEPCAPS) ... found
checking for capabilities ... found
checking for crypt_r() ... found
checking for sys/vfs.h ... found
checking for nobody group ... found
checking for poll() ... found
checking for /dev/poll ... not found
checking for kqueue ... not found
checking for crypt() ... not found
checking for crypt() in libcrypt ... found
checking for F_READAHEAD ... not found
checking for posix_fadvise() ... found
checking for O_DIRECT ... found
checking for F_NOCACHE ... not found
checking for directio() ... not found
checking for statfs() ... found
checking for statvfs() ... found
checking for dlopen() ... not found
checking for dlopen() in libdl ... found
checking for sched_yield() ... found
checking for sched_setaffinity() ... found
checking for SO_SETFIB ... not found
checking for SO_REUSEPORT ... found
checking for SO_ACCEPTFILTER ... not found
checking for SO_BINDANY ... not found
checking for IP_TRANSPARENT ... found
checking for IP_BINDANY ... not found
checking for IP_BIND_ADDRESS_NO_PORT ... not found
checking for IP_RECVDSTADDR ... not found
checking for IP_SENDSRCADDR ... not found
checking for IP_PKTINFO ... found
checking for IPV6_RECVPKTINFO ... found
checking for TCP_DEFER_ACCEPT ... found
checking for TCP_KEEPIDLE ... found
checking for TCP_FASTOPEN ... found
checking for TCP_INFO ... found
checking for accept4() ... found
checking for eventfd() ... found
checking for int size ... 4 bytes
checking for long size ... 8 bytes
checking for long long size ... 8 bytes
checking for void * size ... 8 bytes
checking for uint32_t ... found
checking for uint64_t ... found
checking for sig_atomic_t ... found
checking for sig_atomic_t size ... 4 bytes
checking for socklen_t ... found
checking for in_addr_t ... found
checking for in_port_t ... found
checking for rlim_t ... found
checking for uintptr_t ... uintptr_t found
checking for system byte ordering ... little endian
checking for size_t size ... 8 bytes
checking for off_t size ... 8 bytes
checking for time_t size ... 8 bytes
checking for AF_INET6 ... found
checking for setproctitle() ... not found
checking for pread() ... found
checking for pwrite() ... found
checking for pwritev() ... found
checking for sys_nerr ... found
checking for localtime_r() ... found
checking for clock_gettime(CLOCK_MONOTONIC) ... found
checking for posix_memalign() ... found
checking for memalign() ... found
checking for mmap(MAP_ANON|MAP_SHARED) ... found
checking for mmap("/dev/zero", MAP_SHARED) ... found
checking for System V shared memory ... found
checking for POSIX semaphores ... not found
checking for POSIX semaphores in libpthread ... found
checking for struct msghdr.msg_control ... found
checking for ioctl(FIONBIO) ... found
checking for struct tm.tm_gmtoff ... found
checking for struct dirent.d_namlen ... not found
checking for struct dirent.d_type ... found
checking for sysconf(_SC_NPROCESSORS_ONLN) ... found
checking for sysconf(_SC_LEVEL1_DCACHE_LINESIZE) ... found
checking for openat(), fstatat() ... found
checking for getaddrinfo() ... found
configuring additional modules
adding module in /root/nginx_build/nginx-module-vts-0.1.18
 + ngx_http_vhost_traffic_status_module was configured
checking for PCRE library ... found
checking for PCRE JIT support ... found
checking for zlib library ... found
creating objs/Makefile

Configuration summary
  + using system PCRE library
  + OpenSSL library is not used
  + using system zlib library

  nginx path prefix: "/usr/local/nginx"
  nginx binary file: "/usr/local/nginx/sbin/nginx"
  nginx modules path: "/usr/local/nginx/modules"
  nginx configuration prefix: "/usr/local/nginx/conf"
  nginx configuration file: "/usr/local/nginx/conf/nginx.conf"
  nginx pid file: "/usr/local/nginx/logs/nginx.pid"
  nginx error log file: "/usr/local/nginx/logs/error.log"
  nginx http access log file: "/usr/local/nginx/logs/access.log"
  nginx http client request body temporary files: "client_body_temp"
  nginx http proxy temporary files: "proxy_temp"
  nginx http fastcgi temporary files: "fastcgi_temp"
  nginx http uwsgi temporary files: "uwsgi_temp"
  nginx http scgi temporary files: "scgi_temp"
```
``` bash
[root@txy nginx-1.17.3]# make && make install
make -f objs/Makefile
make[1]: Entering directory `/root/nginx_build/nginx-1.17.3'
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/nginx.o \
	src/core/nginx.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_log.o \
	src/core/ngx_log.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_palloc.o \
	src/core/ngx_palloc.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_array.o \
	src/core/ngx_array.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_list.o \
	src/core/ngx_list.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_hash.o \
	src/core/ngx_hash.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_buf.o \
	src/core/ngx_buf.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_queue.o \
	src/core/ngx_queue.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_output_chain.o \
	src/core/ngx_output_chain.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_string.o \
	src/core/ngx_string.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_parse.o \
	src/core/ngx_parse.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_parse_time.o \
	src/core/ngx_parse_time.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_inet.o \
	src/core/ngx_inet.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_file.o \
	src/core/ngx_file.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_crc32.o \
	src/core/ngx_crc32.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_murmurhash.o \
	src/core/ngx_murmurhash.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_md5.o \
	src/core/ngx_md5.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_sha1.o \
	src/core/ngx_sha1.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_rbtree.o \
	src/core/ngx_rbtree.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_radix_tree.o \
	src/core/ngx_radix_tree.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_slab.o \
	src/core/ngx_slab.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_times.o \
	src/core/ngx_times.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_shmtx.o \
	src/core/ngx_shmtx.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_connection.o \
	src/core/ngx_connection.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_cycle.o \
	src/core/ngx_cycle.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_spinlock.o \
	src/core/ngx_spinlock.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_rwlock.o \
	src/core/ngx_rwlock.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_cpuinfo.o \
	src/core/ngx_cpuinfo.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_conf_file.o \
	src/core/ngx_conf_file.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_module.o \
	src/core/ngx_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_resolver.o \
	src/core/ngx_resolver.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_open_file_cache.o \
	src/core/ngx_open_file_cache.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_crypt.o \
	src/core/ngx_crypt.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_proxy_protocol.o \
	src/core/ngx_proxy_protocol.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_syslog.o \
	src/core/ngx_syslog.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/event/ngx_event.o \
	src/event/ngx_event.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/event/ngx_event_timer.o \
	src/event/ngx_event_timer.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/event/ngx_event_posted.o \
	src/event/ngx_event_posted.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/event/ngx_event_accept.o \
	src/event/ngx_event_accept.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/event/ngx_event_udp.o \
	src/event/ngx_event_udp.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/event/ngx_event_connect.o \
	src/event/ngx_event_connect.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/event/ngx_event_pipe.o \
	src/event/ngx_event_pipe.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/os/unix/ngx_time.o \
	src/os/unix/ngx_time.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/os/unix/ngx_errno.o \
	src/os/unix/ngx_errno.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/os/unix/ngx_alloc.o \
	src/os/unix/ngx_alloc.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/os/unix/ngx_files.o \
	src/os/unix/ngx_files.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/os/unix/ngx_socket.o \
	src/os/unix/ngx_socket.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/os/unix/ngx_recv.o \
	src/os/unix/ngx_recv.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/os/unix/ngx_readv_chain.o \
	src/os/unix/ngx_readv_chain.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/os/unix/ngx_udp_recv.o \
	src/os/unix/ngx_udp_recv.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/os/unix/ngx_send.o \
	src/os/unix/ngx_send.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/os/unix/ngx_writev_chain.o \
	src/os/unix/ngx_writev_chain.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/os/unix/ngx_udp_send.o \
	src/os/unix/ngx_udp_send.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/os/unix/ngx_udp_sendmsg_chain.o \
	src/os/unix/ngx_udp_sendmsg_chain.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/os/unix/ngx_channel.o \
	src/os/unix/ngx_channel.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/os/unix/ngx_shmem.o \
	src/os/unix/ngx_shmem.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/os/unix/ngx_process.o \
	src/os/unix/ngx_process.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/os/unix/ngx_daemon.o \
	src/os/unix/ngx_daemon.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/os/unix/ngx_setaffinity.o \
	src/os/unix/ngx_setaffinity.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/os/unix/ngx_setproctitle.o \
	src/os/unix/ngx_setproctitle.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/os/unix/ngx_posix_init.o \
	src/os/unix/ngx_posix_init.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/os/unix/ngx_user.o \
	src/os/unix/ngx_user.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/os/unix/ngx_dlopen.o \
	src/os/unix/ngx_dlopen.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/os/unix/ngx_process_cycle.o \
	src/os/unix/ngx_process_cycle.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/os/unix/ngx_linux_init.o \
	src/os/unix/ngx_linux_init.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/event/modules/ngx_epoll_module.o \
	src/event/modules/ngx_epoll_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/os/unix/ngx_linux_sendfile_chain.o \
	src/os/unix/ngx_linux_sendfile_chain.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/src/core/ngx_regex.o \
	src/core/ngx_regex.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/ngx_http.o \
	src/http/ngx_http.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/ngx_http_core_module.o \
	src/http/ngx_http_core_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/ngx_http_special_response.o \
	src/http/ngx_http_special_response.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/ngx_http_request.o \
	src/http/ngx_http_request.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/ngx_http_parse.o \
	src/http/ngx_http_parse.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_log_module.o \
	src/http/modules/ngx_http_log_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/ngx_http_request_body.o \
	src/http/ngx_http_request_body.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/ngx_http_variables.o \
	src/http/ngx_http_variables.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/ngx_http_script.o \
	src/http/ngx_http_script.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/ngx_http_upstream.o \
	src/http/ngx_http_upstream.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/ngx_http_upstream_round_robin.o \
	src/http/ngx_http_upstream_round_robin.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/ngx_http_file_cache.o \
	src/http/ngx_http_file_cache.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/ngx_http_write_filter_module.o \
	src/http/ngx_http_write_filter_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/ngx_http_header_filter_module.o \
	src/http/ngx_http_header_filter_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_chunked_filter_module.o \
	src/http/modules/ngx_http_chunked_filter_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_range_filter_module.o \
	src/http/modules/ngx_http_range_filter_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_gzip_filter_module.o \
	src/http/modules/ngx_http_gzip_filter_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/ngx_http_postpone_filter_module.o \
	src/http/ngx_http_postpone_filter_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_ssi_filter_module.o \
	src/http/modules/ngx_http_ssi_filter_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_charset_filter_module.o \
	src/http/modules/ngx_http_charset_filter_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_userid_filter_module.o \
	src/http/modules/ngx_http_userid_filter_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_headers_filter_module.o \
	src/http/modules/ngx_http_headers_filter_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/ngx_http_copy_filter_module.o \
	src/http/ngx_http_copy_filter_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_not_modified_filter_module.o \
	src/http/modules/ngx_http_not_modified_filter_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_static_module.o \
	src/http/modules/ngx_http_static_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_autoindex_module.o \
	src/http/modules/ngx_http_autoindex_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_index_module.o \
	src/http/modules/ngx_http_index_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_mirror_module.o \
	src/http/modules/ngx_http_mirror_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_try_files_module.o \
	src/http/modules/ngx_http_try_files_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_auth_basic_module.o \
	src/http/modules/ngx_http_auth_basic_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_access_module.o \
	src/http/modules/ngx_http_access_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_limit_conn_module.o \
	src/http/modules/ngx_http_limit_conn_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_limit_req_module.o \
	src/http/modules/ngx_http_limit_req_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_geo_module.o \
	src/http/modules/ngx_http_geo_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_map_module.o \
	src/http/modules/ngx_http_map_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_split_clients_module.o \
	src/http/modules/ngx_http_split_clients_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_referer_module.o \
	src/http/modules/ngx_http_referer_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_rewrite_module.o \
	src/http/modules/ngx_http_rewrite_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_proxy_module.o \
	src/http/modules/ngx_http_proxy_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_fastcgi_module.o \
	src/http/modules/ngx_http_fastcgi_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_uwsgi_module.o \
	src/http/modules/ngx_http_uwsgi_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_scgi_module.o \
	src/http/modules/ngx_http_scgi_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_memcached_module.o \
	src/http/modules/ngx_http_memcached_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_empty_gif_module.o \
	src/http/modules/ngx_http_empty_gif_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_browser_module.o \
	src/http/modules/ngx_http_browser_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_upstream_hash_module.o \
	src/http/modules/ngx_http_upstream_hash_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_upstream_ip_hash_module.o \
	src/http/modules/ngx_http_upstream_ip_hash_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_upstream_least_conn_module.o \
	src/http/modules/ngx_http_upstream_least_conn_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_upstream_random_module.o \
	src/http/modules/ngx_http_upstream_random_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_upstream_keepalive_module.o \
	src/http/modules/ngx_http_upstream_keepalive_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/src/http/modules/ngx_http_upstream_zone_module.o \
	src/http/modules/ngx_http_upstream_zone_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g   -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/addon/src/ngx_http_vhost_traffic_status_module.o \
	/root/nginx_build/nginx-module-vts-0.1.18/src/ngx_http_vhost_traffic_status_module.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g   -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/addon/src/ngx_http_vhost_traffic_status_variables.o \
	/root/nginx_build/nginx-module-vts-0.1.18/src/ngx_http_vhost_traffic_status_variables.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g   -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/addon/src/ngx_http_vhost_traffic_status_string.o \
	/root/nginx_build/nginx-module-vts-0.1.18/src/ngx_http_vhost_traffic_status_string.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g   -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/addon/src/ngx_http_vhost_traffic_status_shm.o \
	/root/nginx_build/nginx-module-vts-0.1.18/src/ngx_http_vhost_traffic_status_shm.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g   -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/addon/src/ngx_http_vhost_traffic_status_node.o \
	/root/nginx_build/nginx-module-vts-0.1.18/src/ngx_http_vhost_traffic_status_node.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g   -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/addon/src/ngx_http_vhost_traffic_status_filter.o \
	/root/nginx_build/nginx-module-vts-0.1.18/src/ngx_http_vhost_traffic_status_filter.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g   -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/addon/src/ngx_http_vhost_traffic_status_control.o \
	/root/nginx_build/nginx-module-vts-0.1.18/src/ngx_http_vhost_traffic_status_control.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g   -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/addon/src/ngx_http_vhost_traffic_status_limit.o \
	/root/nginx_build/nginx-module-vts-0.1.18/src/ngx_http_vhost_traffic_status_limit.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g   -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/addon/src/ngx_http_vhost_traffic_status_display.o \
	/root/nginx_build/nginx-module-vts-0.1.18/src/ngx_http_vhost_traffic_status_display.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g   -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/addon/src/ngx_http_vhost_traffic_status_display_json.o \
	/root/nginx_build/nginx-module-vts-0.1.18/src/ngx_http_vhost_traffic_status_display_json.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g   -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/addon/src/ngx_http_vhost_traffic_status_display_prometheus.o \
	/root/nginx_build/nginx-module-vts-0.1.18/src/ngx_http_vhost_traffic_status_display_prometheus.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g   -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/addon/src/ngx_http_vhost_traffic_status_set.o \
	/root/nginx_build/nginx-module-vts-0.1.18/src/ngx_http_vhost_traffic_status_set.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g   -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs -I src/http -I src/http/modules \
	-o objs/addon/src/ngx_http_vhost_traffic_status_dump.o \
	/root/nginx_build/nginx-module-vts-0.1.18/src/ngx_http_vhost_traffic_status_dump.c
cc -c -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Werror -g  -I src/core -I src/event -I src/event/modules -I src/os/unix -I objs \
	-o objs/ngx_modules.o \
	objs/ngx_modules.c
cc -o objs/nginx \
objs/src/core/nginx.o \
objs/src/core/ngx_log.o \
objs/src/core/ngx_palloc.o \
objs/src/core/ngx_array.o \
objs/src/core/ngx_list.o \
objs/src/core/ngx_hash.o \
objs/src/core/ngx_buf.o \
objs/src/core/ngx_queue.o \
objs/src/core/ngx_output_chain.o \
objs/src/core/ngx_string.o \
objs/src/core/ngx_parse.o \
objs/src/core/ngx_parse_time.o \
objs/src/core/ngx_inet.o \
objs/src/core/ngx_file.o \
objs/src/core/ngx_crc32.o \
objs/src/core/ngx_murmurhash.o \
objs/src/core/ngx_md5.o \
objs/src/core/ngx_sha1.o \
objs/src/core/ngx_rbtree.o \
objs/src/core/ngx_radix_tree.o \
objs/src/core/ngx_slab.o \
objs/src/core/ngx_times.o \
objs/src/core/ngx_shmtx.o \
objs/src/core/ngx_connection.o \
objs/src/core/ngx_cycle.o \
objs/src/core/ngx_spinlock.o \
objs/src/core/ngx_rwlock.o \
objs/src/core/ngx_cpuinfo.o \
objs/src/core/ngx_conf_file.o \
objs/src/core/ngx_module.o \
objs/src/core/ngx_resolver.o \
objs/src/core/ngx_open_file_cache.o \
objs/src/core/ngx_crypt.o \
objs/src/core/ngx_proxy_protocol.o \
objs/src/core/ngx_syslog.o \
objs/src/event/ngx_event.o \
objs/src/event/ngx_event_timer.o \
objs/src/event/ngx_event_posted.o \
objs/src/event/ngx_event_accept.o \
objs/src/event/ngx_event_udp.o \
objs/src/event/ngx_event_connect.o \
objs/src/event/ngx_event_pipe.o \
objs/src/os/unix/ngx_time.o \
objs/src/os/unix/ngx_errno.o \
objs/src/os/unix/ngx_alloc.o \
objs/src/os/unix/ngx_files.o \
objs/src/os/unix/ngx_socket.o \
objs/src/os/unix/ngx_recv.o \
objs/src/os/unix/ngx_readv_chain.o \
objs/src/os/unix/ngx_udp_recv.o \
objs/src/os/unix/ngx_send.o \
objs/src/os/unix/ngx_writev_chain.o \
objs/src/os/unix/ngx_udp_send.o \
objs/src/os/unix/ngx_udp_sendmsg_chain.o \
objs/src/os/unix/ngx_channel.o \
objs/src/os/unix/ngx_shmem.o \
objs/src/os/unix/ngx_process.o \
objs/src/os/unix/ngx_daemon.o \
objs/src/os/unix/ngx_setaffinity.o \
objs/src/os/unix/ngx_setproctitle.o \
objs/src/os/unix/ngx_posix_init.o \
objs/src/os/unix/ngx_user.o \
objs/src/os/unix/ngx_dlopen.o \
objs/src/os/unix/ngx_process_cycle.o \
objs/src/os/unix/ngx_linux_init.o \
objs/src/event/modules/ngx_epoll_module.o \
objs/src/os/unix/ngx_linux_sendfile_chain.o \
objs/src/core/ngx_regex.o \
objs/src/http/ngx_http.o \
objs/src/http/ngx_http_core_module.o \
objs/src/http/ngx_http_special_response.o \
objs/src/http/ngx_http_request.o \
objs/src/http/ngx_http_parse.o \
objs/src/http/modules/ngx_http_log_module.o \
objs/src/http/ngx_http_request_body.o \
objs/src/http/ngx_http_variables.o \
objs/src/http/ngx_http_script.o \
objs/src/http/ngx_http_upstream.o \
objs/src/http/ngx_http_upstream_round_robin.o \
objs/src/http/ngx_http_file_cache.o \
objs/src/http/ngx_http_write_filter_module.o \
objs/src/http/ngx_http_header_filter_module.o \
objs/src/http/modules/ngx_http_chunked_filter_module.o \
objs/src/http/modules/ngx_http_range_filter_module.o \
objs/src/http/modules/ngx_http_gzip_filter_module.o \
objs/src/http/ngx_http_postpone_filter_module.o \
objs/src/http/modules/ngx_http_ssi_filter_module.o \
objs/src/http/modules/ngx_http_charset_filter_module.o \
objs/src/http/modules/ngx_http_userid_filter_module.o \
objs/src/http/modules/ngx_http_headers_filter_module.o \
objs/src/http/ngx_http_copy_filter_module.o \
objs/src/http/modules/ngx_http_not_modified_filter_module.o \
objs/src/http/modules/ngx_http_static_module.o \
objs/src/http/modules/ngx_http_autoindex_module.o \
objs/src/http/modules/ngx_http_index_module.o \
objs/src/http/modules/ngx_http_mirror_module.o \
objs/src/http/modules/ngx_http_try_files_module.o \
objs/src/http/modules/ngx_http_auth_basic_module.o \
objs/src/http/modules/ngx_http_access_module.o \
objs/src/http/modules/ngx_http_limit_conn_module.o \
objs/src/http/modules/ngx_http_limit_req_module.o \
objs/src/http/modules/ngx_http_geo_module.o \
objs/src/http/modules/ngx_http_map_module.o \
objs/src/http/modules/ngx_http_split_clients_module.o \
objs/src/http/modules/ngx_http_referer_module.o \
objs/src/http/modules/ngx_http_rewrite_module.o \
objs/src/http/modules/ngx_http_proxy_module.o \
objs/src/http/modules/ngx_http_fastcgi_module.o \
objs/src/http/modules/ngx_http_uwsgi_module.o \
objs/src/http/modules/ngx_http_scgi_module.o \
objs/src/http/modules/ngx_http_memcached_module.o \
objs/src/http/modules/ngx_http_empty_gif_module.o \
objs/src/http/modules/ngx_http_browser_module.o \
objs/src/http/modules/ngx_http_upstream_hash_module.o \
objs/src/http/modules/ngx_http_upstream_ip_hash_module.o \
objs/src/http/modules/ngx_http_upstream_least_conn_module.o \
objs/src/http/modules/ngx_http_upstream_random_module.o \
objs/src/http/modules/ngx_http_upstream_keepalive_module.o \
objs/src/http/modules/ngx_http_upstream_zone_module.o \
objs/addon/src/ngx_http_vhost_traffic_status_module.o \
objs/addon/src/ngx_http_vhost_traffic_status_variables.o \
objs/addon/src/ngx_http_vhost_traffic_status_string.o \
objs/addon/src/ngx_http_vhost_traffic_status_shm.o \
objs/addon/src/ngx_http_vhost_traffic_status_node.o \
objs/addon/src/ngx_http_vhost_traffic_status_filter.o \
objs/addon/src/ngx_http_vhost_traffic_status_control.o \
objs/addon/src/ngx_http_vhost_traffic_status_limit.o \
objs/addon/src/ngx_http_vhost_traffic_status_display.o \
objs/addon/src/ngx_http_vhost_traffic_status_display_json.o \
objs/addon/src/ngx_http_vhost_traffic_status_display_prometheus.o \
objs/addon/src/ngx_http_vhost_traffic_status_set.o \
objs/addon/src/ngx_http_vhost_traffic_status_dump.o \
objs/ngx_modules.o \
-ldl -lpthread -lcrypt -lpcre -lz \
-Wl,-E
sed -e "s|%%PREFIX%%|/usr/local/nginx|" \
	-e "s|%%PID_PATH%%|/usr/local/nginx/logs/nginx.pid|" \
	-e "s|%%CONF_PATH%%|/usr/local/nginx/conf/nginx.conf|" \
	-e "s|%%ERROR_LOG_PATH%%|/usr/local/nginx/logs/error.log|" \
	< man/nginx.8 > objs/nginx.8
make[1]: Leaving directory `/root/nginx_build/nginx-1.17.3'
make -f objs/Makefile install
make[1]: Entering directory `/root/nginx_build/nginx-1.17.3'
test -d '/usr/local/nginx' || mkdir -p '/usr/local/nginx'
test -d '/usr/local/nginx/sbin' \
	|| mkdir -p '/usr/local/nginx/sbin'
test ! -f '/usr/local/nginx/sbin/nginx' \
	|| mv '/usr/local/nginx/sbin/nginx' \
		'/usr/local/nginx/sbin/nginx.old'
cp objs/nginx '/usr/local/nginx/sbin/nginx'
test -d '/usr/local/nginx/conf' \
	|| mkdir -p '/usr/local/nginx/conf'
cp conf/koi-win '/usr/local/nginx/conf'
cp conf/koi-utf '/usr/local/nginx/conf'
cp conf/win-utf '/usr/local/nginx/conf'
test -f '/usr/local/nginx/conf/mime.types' \
	|| cp conf/mime.types '/usr/local/nginx/conf'
cp conf/mime.types '/usr/local/nginx/conf/mime.types.default'
test -f '/usr/local/nginx/conf/fastcgi_params' \
	|| cp conf/fastcgi_params '/usr/local/nginx/conf'
cp conf/fastcgi_params \
	'/usr/local/nginx/conf/fastcgi_params.default'
test -f '/usr/local/nginx/conf/fastcgi.conf' \
	|| cp conf/fastcgi.conf '/usr/local/nginx/conf'
cp conf/fastcgi.conf '/usr/local/nginx/conf/fastcgi.conf.default'
test -f '/usr/local/nginx/conf/uwsgi_params' \
	|| cp conf/uwsgi_params '/usr/local/nginx/conf'
cp conf/uwsgi_params \
	'/usr/local/nginx/conf/uwsgi_params.default'
test -f '/usr/local/nginx/conf/scgi_params' \
	|| cp conf/scgi_params '/usr/local/nginx/conf'
cp conf/scgi_params \
	'/usr/local/nginx/conf/scgi_params.default'
test -f '/usr/local/nginx/conf/nginx.conf' \
	|| cp conf/nginx.conf '/usr/local/nginx/conf/nginx.conf'
cp conf/nginx.conf '/usr/local/nginx/conf/nginx.conf.default'
test -d '/usr/local/nginx/logs' \
	|| mkdir -p '/usr/local/nginx/logs'
test -d '/usr/local/nginx/logs' \
	|| mkdir -p '/usr/local/nginx/logs'
test -d '/usr/local/nginx/html' \
	|| cp -R html '/usr/local/nginx'
test -d '/usr/local/nginx/logs' \
	|| mkdir -p '/usr/local/nginx/logs'
make[1]: Leaving directory `/root/nginx_build/nginx-1.17.3'
```
修改配置文件
`vim /usr/local/nginx/conf/nginx.conf`
``` bash
http {
    vhost_traffic_status_zone;

    ...

    server {

        ...

        location /status {
            vhost_traffic_status_display;
            vhost_traffic_status_display_format html;
        }
    }
}
```
运行
``` bash
[root@txy ~]# /usr/local/nginx/sbin/nginx
[root@txy ~]# ps aux | grep nginx
root      7895  0.0  0.0  21780   644 ?        Ss   21:42   0:00 nginx: master process /usr/local/nginx/sbin/nginx
nobody    7896  0.0  0.1  24236  1416 ?        S    21:42   0:00 nginx: worker process
root      7915  0.0  0.0 112708   976 pts/0    S+   21:42   0:00 grep --color=auto nginx
```
自启
将`/usr/local/nginx/sbin/nginx`命令加入`/etc/rc.d/rc.local`文件并赋予权限`chmod +x /etc/rc.d/rc.local`

## 0x09.引用
[python --enable-shared](https://www.cnblogs.com/Tommy-Yu/p/6144512.html)
