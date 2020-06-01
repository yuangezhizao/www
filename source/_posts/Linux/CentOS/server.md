---
title: 换新系统之腾讯云学生机 CentOS 7.7 64 位
date: 2019-5-9 18:22:34
tags:
  - CentOS
  - server
count: 8
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
如果在创建实例时**高级设置**里指定了**主机名**，则会自动配置
``` bash
[root@txy ~]# cat /etc/hosts
127.0.0.1 txy txy
127.0.0.1 localhost.localdomain localhost
127.0.0.1 localhost4.localdomain4 localhost4

::1 txy txy
::1 localhost.localdomain localhost
::1 localhost6.localdomain6 localhost6
```
否则，手动更改
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

## 0x01.修改`ssh`端口
改成非`22`端口防止爆破
```
[root@txy ~]# vim /etc/ssh/sshd_config 
……
# If you want to change the port on a SELinux system, you have to tell
# SELinux about this change.
# semanage port -a -t ssh_port_t -p tcp #PORTNUMBER
#
#Port 22
……
[root@txy ~]# systemctl restart sshd
```
注意一定要新开个`shell`测试新端口是否生效，生效则可关闭旧`shell`，否则需重新配置

## 0x02.软件
``` bash
yum update -y
yum install htop screen git axel iftop -y
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
![现有路径](https://i1.yuangezhizao.cn/Win-10/20191107225633.jpg!webp)

全新：
```
[root@txy ~]# whereis python
python: /usr/bin/python /usr/bin/python2.7 /usr/lib/python2.7 /usr/lib64/python2.7 /etc/python /usr/include/python2.7 /usr/share/man/man1/python.1.gz
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

或
![下载卡爆，proxy 中转爽到！](https://i1.yuangezhizao.cn/Win-10/20191107224750.jpg!webp)

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
~~不添加`--enable-shared`（生成动态链接库）编译会报错：`command 'gcc' failed with exit status 1`~~
``` bash
……
gcc -pthread -shared     -Wl,--no-as-needed -o libpython3.so -Wl,-hlibpython3.so libpython3.8.so
gcc -pthread     -Xlinker -export-dynamic -o python Programs/python.o -L. -lpython3.8 -lcrypt -lpthread -ldl  -lutil -lm   -lm 
LD_LIBRARY_PATH=/root/Python-3.8.3 ./python -E -S -m sysconfig --generate-posix-vars ;\
if test $? -ne 0 ; then \
	echo "generate-posix-vars failed" ; \
	rm -f ./pybuilddir.txt ; \
	exit 1 ; \
fi
Could not import runpy module
Traceback (most recent call last):
  File "/root/Python-3.8.3/Lib/runpy.py", line 15, in <module>
    import importlib.util
  File "/root/Python-3.8.3/Lib/importlib/util.py", line 14, in <module>
    from contextlib import contextmanager
  File "/root/Python-3.8.3/Lib/contextlib.py", line 4, in <module>
    import _collections_abc
SystemError: <built-in function compile> returned NULL without setting an error
generate-posix-vars failed
make[1]: *** [pybuilddir.txt] Error 1
make[1]: Leaving directory `/root/Python-3.8.3'
make: *** [profile-opt] Error 2
```
`rm -rf /usr/local/python3`
~~`./configure --prefix=/usr/local/python3 --enable-shared --enable-optimizations`~~
`./configure --prefix=/usr/local/python3 --enable-optimizations`
`make && make install`
6. 修复
①`2020-5-22 00:06:54`：`CentOS`自带`gcc`版本是`4`，升级至版本`8`即可解决（而之前在`ubuntu`编译的时候是版本`7`，因此可以直接编译通过
``` bash
[root@py Python-3.8.3]# gcc -v
Using built-in specs.
COLLECT_GCC=gcc
COLLECT_LTO_WRAPPER=/usr/libexec/gcc/x86_64-redhat-linux/4.8.5/lto-wrapper
Target: x86_64-redhat-linux
Configured with: ../configure --prefix=/usr --mandir=/usr/share/man --infodir=/usr/share/info --with-bugurl=http://bugzilla.redhat.com/bugzilla --enable-bootstrap --enable-shared --enable-threads=posix --enable-checking=release --with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions --enable-gnu-unique-object --enable-linker-build-id --with-linker-hash-style=gnu --enable-languages=c,c++,objc,obj-c++,java,fortran,ada,go,lto --enable-plugin --enable-initfini-array --disable-libgcj --with-isl=/builddir/build/BUILD/gcc-4.8.5-20150702/obj-x86_64-redhat-linux/isl-install --with-cloog=/builddir/build/BUILD/gcc-4.8.5-20150702/obj-x86_64-redhat-linux/cloog-install --enable-gnu-indirect-function --with-tune=generic --with-arch_32=x86-64 --build=x86_64-redhat-linux
Thread model: posix
gcc version 4.8.5 20150623 (Red Hat 4.8.5-39) (GCC) 
[root@py Python-3.8.3]# yum install centos-release-scl -y
……
Complete!
[root@py Python-3.8.3]# yum install devtoolset-8-gcc* -y
……
Dependencies Resolved

===================================================================================================================
 Package                                 Arch            Version                     Repository               Size
===================================================================================================================
Installing:
 devtoolset-8-gcc                        x86_64          8.3.1-3.2.el7               centos-sclo-rh           30 M
 devtoolset-8-gcc-c++                    x86_64          8.3.1-3.2.el7               centos-sclo-rh           12 M
 devtoolset-8-gcc-gdb-plugin             x86_64          8.3.1-3.2.el7               centos-sclo-rh          123 k
 devtoolset-8-gcc-gfortran               x86_64          8.3.1-3.2.el7               centos-sclo-rh           12 M
 devtoolset-8-gcc-plugin-devel           x86_64          8.3.1-3.2.el7               centos-sclo-rh          1.4 M
Installing for dependencies:
 audit-libs-python                       x86_64          2.8.5-4.el7                 os                       76 k
 checkpolicy                             x86_64          2.5-8.el7                   os                      295 k
 devtoolset-8-binutils                   x86_64          2.30-55.el7.2               centos-sclo-rh          5.5 M
 devtoolset-8-libquadmath-devel          x86_64          8.3.1-3.2.el7               centos-sclo-rh          155 k
 devtoolset-8-libstdc++-devel            x86_64          8.3.1-3.2.el7               centos-sclo-rh          2.7 M
 devtoolset-8-runtime                    x86_64          8.1-1.el7                   centos-sclo-rh           20 k
 gmp-devel                               x86_64          1:6.0.0-15.el7              os                      181 k
 libcgroup                               x86_64          0.41-21.el7                 os                       66 k
 libgfortran5                            x86_64          8.3.1-2.1.1.el7             os                      796 k
 libmpc-devel                            x86_64          1.0.1-3.el7                 os                       32 k
 libquadmath                             x86_64          4.8.5-39.el7                os                      190 k
 libsemanage-python                      x86_64          2.5-14.el7                  os                      113 k
 mpfr-devel                              x86_64          3.1.1-4.el7                 os                       68 k
 policycoreutils-python                  x86_64          2.5-34.el7                  os                      457 k
 python-IPy                              noarch          0.75-6.el7                  os                       32 k
 setools-libs                            x86_64          3.3.8-4.el7                 os                      620 k

……
Complete!
[root@py Python-3.8.3]# scl enable devtoolset-8 bash
[root@py Python-3.8.3]# which gcc
/opt/rh/devtoolset-8/root/usr/bin/gcc
[root@py Python-3.8.3]# gcc --version
gcc (GCC) 8.3.1 20190311 (Red Hat 8.3.1-3)
Copyright (C) 2018 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```
再次编译，成功！
``` bash
[root@txy Python-3.8.3]# python3
Python 3.8.3 (default, May 31 2020, 21:31:58) 
[GCC 8.3.1 20190311 (Red Hat 8.3.1-3)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
[1]+  Stopped                 python3
[root@txy ~]# ldd /usr/local/python3/bin/python3
	linux-vdso.so.1 =>  (0x00007ffdfe1d7000)
	libcrypt.so.1 => /lib64/libcrypt.so.1 (0x00007f58dfe8f000)
	libpthread.so.0 => /lib64/libpthread.so.0 (0x00007f58dfc73000)
	libdl.so.2 => /lib64/libdl.so.2 (0x00007f58dfa6f000)
	libutil.so.1 => /lib64/libutil.so.1 (0x00007f58df86c000)
	libm.so.6 => /lib64/libm.so.6 (0x00007f58df56a000)
	libc.so.6 => /lib64/libc.so.6 (0x00007f58df19c000)
	libfreebl3.so => /lib64/libfreebl3.so (0x00007f58def99000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f58e00c6000)
```
②旧法（不推荐使用）
~~添加`--enable-shared`编译之后会报找不到`so`的错误，此时可利用`ldd`工具查看详细~~
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
~~需要手动将所缺`so`库`libpython3.8.so.1.0`移至库目录下，具体生效路径为：`/usr/lib64/`，这里测试`/usr/lib/`、`/usr/local/lib/`、`/usr/local/lib64/`均无效……~~
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
[root@txy Python-3.8.3]# ln -s /usr/local/python3/bin/python3 /usr/bin/python3
ln: failed to create symbolic link ‘/usr/bin/python3’: File exists
[root@txy Python-3.8.3]# rm -rf /usr/bin/python3
[root@txy Python-3.8.3]# ln -s /usr/local/python3/bin/python3 /usr/bin/python3
[root@txy Python-3.8.3]# ln -s /usr/local/python3/bin/pip3.8 /usr/bin/pip3
ln: failed to create symbolic link ‘/usr/bin/pip3’: File exists
[root@txy Python-3.8.3]# rm -rf /usr/bin/pip3
[root@txy Python-3.8.3]# ln -s /usr/local/python3/bin/pip3.8 /usr/bin/pip3
[root@txy Python-3.8.3]# python -V
Python 2.7.5
[root@txy Python-3.8.3]# python2 -V
Python 2.7.5
[root@txy Python-3.8.3]# python3 -V
Python 3.8.3
[root@txy Python-3.8.3]# pip -V
-bash: pip: command not found
[root@txy Python-3.8.3]# pip2 -V
-bash: pip2: command not found
[root@txy Python-3.8.3]# pip3 -V
pip 19.2.3 from /usr/local/python3/lib/python3.8/site-packages/pip (python 3.8)
```
> 这样就可以通过`python`/`python2`命令使用`Python`，`python3`来使用`Python 3`

8. 升级`pip3`
你云环境下会自动配置镜像源
``` bash
[root@txy ~]# pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U
Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple
Collecting pip
  Downloading https://pypi.tuna.tsinghua.edu.cn/packages/43/84/23ed6a1796480a6f1a2d38f2802901d078266bda38388954d01d3f2e821d/pip-20.1.1-py2.py3-none-any.whl (1.5MB)
     |████████████████████████████████| 1.5MB 36.9MB/s 
Installing collected packages: pip
  Found existing installation: pip 19.2.3
    Uninstalling pip-19.2.3:
      Successfully uninstalled pip-19.2.3
Successfully installed pip-20.1.1
[root@txy ~]# pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
Writing to /root/.config/pip/pip.conf
[root@txy ~]# pip3 install --upgrade pip
Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple
Requirement already up-to-date: pip in /usr/local/python3/lib/python3.8/site-packages (20.1.1)
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
$ sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine
```
2. 使用源安装
``` bash
$ sudo yum install -y yum-utils

$ sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
```
因国外下载速度过慢不得不去看[Docker CE 源使用帮助](https://mirrors.ustc.edu.cn/help/docker-ce.html)
> `CentOS、Fedora`等用户在下载`docker-ce.repo`文件后，还需要将该文件中的`download.docker.com`地址换成`mirrors.ustc.edu.cn/docker-ce`

`yum clean all`再`yum makecache`后开始安装
3. 安装
`$ sudo yum install docker-ce docker-ce-cli containerd.io`
根据[Docker Hub 源使用帮助](https://mirrors.ustc.edu.cn/help/dockerhub.html)
``` bash
[root@txy ~]# mkdir /etc/docker
[root@txy ~]# cat /etc/docker/daemon.json
{
  "registry-mirrors": ["https://docker.mirrors.ustc.edu.cn/"]
}
```
4. 启动
`$ sudo systemctl start docker`
5. 测试
`$ sudo docker run hello-world`
输出如下：
``` bash
[root@txy ~]#  docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
0e03bdcc26d7: Pull complete 
Digest: sha256:6a65f928fb91fcfbc963f7aa6d57c8eeb426ad9a20c7ee045538ef34847f44f1
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
6. 自启
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
`./configure --add-module=/root/nginx_build/nginx-module-vts-0.1.18`
`make && make install`
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

## 0x09.测试延迟
也就只能凑合看下，不过拿来对比应该是可以的
①`cn-py-dl-c7`
``` bash
[root@py ~]# ping jrmkt.jd.com
PING jrmkt.jd.com.gslb.qianxun.com (61.48.89.125) 56(84) bytes of data.
64 bytes from 61.48.89.125 (61.48.89.125): icmp_seq=1 ttl=38 time=27.8 ms
64 bytes from 61.48.89.125 (61.48.89.125): icmp_seq=2 ttl=38 time=34.1 ms
64 bytes from 61.48.89.125 (61.48.89.125): icmp_seq=3 ttl=38 time=27.7 ms
64 bytes from 61.48.89.125 (61.48.89.125): icmp_seq=4 ttl=38 time=27.2 ms
64 bytes from 61.48.89.125 (61.48.89.125): icmp_seq=5 ttl=38 time=27.3 ms
^C
--- jrmkt.jd.com.gslb.qianxun.com ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 6565ms
rtt min/avg/max/mdev = 27.242/28.895/34.189/2.664 ms
```
②`cn-tx-bj1-w2d`
``` bash
C:\LAB>ping jrmkt.jd.com

正在 Ping jrmkt.jd.com.gslb.qianxun.com [49.7.26.66] 具有 32 字节的数据:
来自 49.7.26.66 的回复: 字节=32 时间=4ms TTL=250
来自 49.7.26.66 的回复: 字节=32 时间=4ms TTL=250
来自 49.7.26.66 的回复: 字节=32 时间=4ms TTL=250
来自 49.7.26.66 的回复: 字节=32 时间=4ms TTL=250

49.7.26.66 的 Ping 统计信息:
    数据包: 已发送 = 4，已接收 = 4，丢失 = 0 (0% 丢失)，
往返行程的估计时间(以毫秒为单位):
    最短 = 4ms，最长 = 4ms，平均 = 4ms
```
③`cn-tx-bj3-c7`
``` bash
[root@txy ~]# ping jrmkt.jd.com
PING jrmkt.jd.com.gslb.qianxun.com (61.48.89.125) 56(84) bytes of data.
64 bytes from 61.48.89.125 (61.48.89.125): icmp_seq=1 ttl=251 time=5.47 ms
64 bytes from 61.48.89.125 (61.48.89.125): icmp_seq=2 ttl=251 time=5.45 ms
64 bytes from 61.48.89.125 (61.48.89.125): icmp_seq=3 ttl=251 time=5.45 ms
64 bytes from 61.48.89.125 (61.48.89.125): icmp_seq=4 ttl=251 time=5.41 ms
64 bytes from 61.48.89.125 (61.48.89.125): icmp_seq=5 ttl=251 time=5.39 ms
^C
--- jrmkt.jd.com.gslb.qianxun.com ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4005ms
rtt min/avg/max/mdev = 5.396/5.438/5.474/0.085 ms
```
由此可见家里肯定是最慢的了，另外**北京一区**比**北京三区**快`1ms`

## 0x10.引用
[python --enable-shared](https://web.archive.org/web/20200521142009/https://www.cnblogs.com/Tommy-Yu/p/6144512.html)
[CentOS 7 升级gcc/g++编译器](https://web.archive.org/web/20200521161733/https://www.cnblogs.com/ToBeExpert/p/10297697.html)
[3.7.0 build error with --enable-optimizations](https://web.archive.org/web/20200521161845/https://bugs.python.org/issue34112)
