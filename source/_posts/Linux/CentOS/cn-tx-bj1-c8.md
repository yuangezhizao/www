---
title: 换新系统之腾讯云学生机 CentOS 8.5.2111
date: 2019-5-9 18:22:34
tags:
  - CentOS
  - server
count: 20
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

## 0x01.修改`SSH`端口
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

## 0x04.编译安装[python3104](https://www.python.org/downloads/release/python-3104)环境
### 1. 查看现有位置
``` bash
[root@txy ~]# whereis python
```
![现有路径](https://i1.yuangezhizao.cn/Win-10/20191107225633.jpg!webp)

全新：
```
[root@cn-py-dl-r8 ~]# whereis python
python: /usr/bin/python3.6 /usr/bin/python3.6m /usr/lib/python3.6 /usr/lib64/python3.6 /usr/include/python3.6m /usr/share/man/man1/python.1.gz
```

### 2. 安装编译工具
~~`yum groupinstall 'Development Tools' -y`~~
``` bash
dnf install gcc make gcc-c++ zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel libffi-devel gdbm-devel xz-devel -y
dnf install libnsl2-devel bluez-libs-devel tix-devel -y
```
或参照[Install dependencies](https://devguide.python.org/setup/#build-dependencies)解决依赖`dnf install dnf-plugins-core && dnf builddep python3`
> 这里面有一个包很关键`libffi-devel`，因为只有`3.7`才会用到这个包，如果不安装这个包的话，在`make`阶段会出现如下的报错：`# ModuleNotFoundError: No module named '_ctypes'`

### 3. 下载源码包
~~`wget https://www.python.org/ftp/python/3.10.4/Python-3.10.4.tar.xz`~~
![下载卡爆，jsproxy 启动！](https://i1.yuangezhizao.cn/Win-10/20191016210358.jpg!webp)

或![下载卡爆，proxy 中转爽到！](https://i1.yuangezhizao.cn/Win-10/20191107224750.jpg!webp)

``` bash
CloudFlare（推荐）：
wget https://proxy-cf.yuangezhizao.cn/dl/Python-3.10.4.tar.xz
Skysilk：
wget http://proxy.yuangezhizao.cn/dl/Python-3.10.4.tar.xz
```

### 4. 解压
``` bash
tar xvJf Python-3.10.4.tar.xz
cd Python-3.10.4
```

### 5. 编译
> 参照：https://docs.python.org/zh-cn/3/using/configure.html#configure-options

注：添加`--enable-optimizations`（以配置文件主导的优化`PGO`）和`--with-lto`（链接时间优化`LTO`）之后的编译速度会变慢，但理论上编译产物的运行效率？会提高
~~不添加`--enable-shared`（生成动态链接库）编译会报错：`command 'gcc' failed with exit status 1`~~
~~`rm -rf /usr/local/python3`~~
~~`./configure --prefix=/usr/local/python3 --enable-shared --enable-optimizations --with-lto`~~
`./configure --prefix=/usr/local/python3 --enable-optimizations --with-lto`
`make && make install`
并且，当开启了`--with-lto`编译标志位时，编译时需保证峰值空闲有`3G`内存，否则在`ar`的时候会因内存不足而终止
``` bash
gcc -pthread -c -Wno-unused-result -Wsign-compare -DNDEBUG -g -fwrapv -O3 -Wall    -fno-semantic-interposition -flto -fuse-linker-plugin -ffat-lto-objects -flto-partition=none -g -std=c99 -Wextra -Wno-unused-result -Wno-unused-parameter -Wno-missing-field-initializers -Werror=implicit-function-declaration -fvisibility=hidden -fprofile-generate -I./Include/internal  -I. -I./Include    -DPy_BUILD_CORE -o Python/frozen.o Python/frozen.c
rm -f libpython3.10.a
ar rcs libpython3.10.a Modules/getbuildinfo.o Parser/token.o  Parser/pegen.o Parser/parser.o Parser/string_parser.o Parser/peg_api.o Parser/myreadline.o Parser/tokenizer.o Objects/abstract.o Objects/accu.o Objects/boolobject.o Objects/bytes_methods.o Objects/bytearrayobject.o Objects/bytesobject.o Objects/call.o Objects/capsule.o Objects/cellobject.o Objects/classobject.o Objects/codeobject.o Objects/complexobject.o Objects/descrobject.o Objects/enumobject.o Objects/exceptions.o Objects/genericaliasobject.o Objects/genobject.o Objects/fileobject.o Objects/floatobject.o Objects/frameobject.o Objects/funcobject.o Objects/interpreteridobject.o Objects/iterobject.o Objects/listobject.o Objects/longobject.o Objects/dictobject.o Objects/odictobject.o Objects/memoryobject.o Objects/methodobject.o Objects/moduleobject.o Objects/namespaceobject.o Objects/object.o Objects/obmalloc.o Objects/picklebufobject.o Objects/rangeobject.o Objects/setobject.o Objects/sliceobject.o Objects/structseq.o Objects/tupleobject.o Objects/typeobject.o Objects/unicodeobject.o Objects/unicodectype.o Objects/unionobject.o Objects/weakrefobject.o Python/_warnings.o Python/Python-ast.o Python/asdl.o Python/ast.o Python/ast_opt.o Python/ast_unparse.o Python/bltinmodule.o Python/ceval.o Python/codecs.o Python/compile.o Python/context.o Python/dynamic_annotations.o Python/errors.o Python/frozenmain.o Python/future.o Python/getargs.o Python/getcompiler.o Python/getcopyright.o Python/getplatform.o Python/getversion.o Python/hamt.o Python/hashtable.o Python/import.o Python/importdl.o Python/initconfig.o Python/marshal.o Python/modsupport.o Python/mysnprintf.o Python/mystrtoul.o Python/pathconfig.o Python/preconfig.o Python/pyarena.o Python/pyctype.o Python/pyfpe.o Python/pyhash.o Python/pylifecycle.o Python/pymath.o Python/pystate.o Python/pythonrun.o Python/pytime.o Python/bootstrap_hash.o Python/structmember.o Python/symtable.o Python/sysmodule.o Python/thread.o Python/traceback.o Python/getopt.o Python/pystrcmp.o Python/pystrtod.o Python/pystrhex.o Python/dtoa.o Python/formatter_unicode.o Python/fileutils.o Python/suggestions.o Python/dynload_shlib.o    Modules/config.o Modules/getpath.o Modules/main.o Modules/gcmodule.o Modules/posixmodule.o  Modules/errnomodule.o  Modules/pwdmodule.o  Modules/_sre.o  Modules/_codecsmodule.o  Modules/_weakref.o  Modules/_functoolsmodule.o  Modules/_operator.o  Modules/_collectionsmodule.o  Modules/_abc.o  Modules/itertoolsmodule.o  Modules/atexitmodule.o  Modules/signalmodule.o  Modules/_stat.o  Modules/timemodule.o  Modules/_threadmodule.o  Modules/_localemodule.o  Modules/_iomodule.o Modules/iobase.o Modules/fileio.o Modules/bytesio.o Modules/bufferedio.o Modules/textio.o Modules/stringio.o  Modules/faulthandler.o  Modules/_tracemalloc.o  Modules/symtablemodule.o  Modules/xxsubtype.o Python/frozen.o
gcc -pthread   -fno-semantic-interposition -flto -fuse-linker-plugin -ffat-lto-objects -flto-partition=none -g -fprofile-generate -Xlinker -export-dynamic -o python Programs/python.o libpython3.10.a -lcrypt -lpthread -ldl  -lutil -lm   -lm 
gcc: fatal error: Killed signal terminated program as
compilation terminated.
lto-wrapper: fatal error: gcc returned 1 exit status
compilation terminated.
/usr/bin/ld: error: lto-wrapper failed
collect2: error: ld returned 1 exit status
make[3]: *** [Makefile:601: python] Error 1
make[3]: Leaving directory '/root/Python-3.10.1'
make[2]: *** [Makefile:531: build_all_generate_profile] Error 2
make[2]: Leaving directory '/root/Python-3.10.1'
make[1]: *** [Makefile:507: profile-gen-stamp] Error 2
make[1]: Leaving directory '/root/Python-3.10.1'
make: *** [Makefile:519: profile-run-stamp] Error 2
[root@cn-tx-bj7-c8 Python-3.10.1]# 
```

### 6. 修复
①`2020-9-7 23:33:59`：`CentOS 8`自带版本已为`8`，直接编译，成功！
~~`2020-5-22 00:06:54`：`CentOS`自带`gcc`版本是`4`，升级至版本`8`即可解决（而之前在`ubuntu`编译的时候是版本`7`，因此可以直接编译通过~~
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

### 7. 创建软链接（`python3`&`pip3`）
此法不会破坏自带`py`环境，因此无需修改任何`yum`文件
~~注：更改`yum`配置~~
~~`vim /usr/bin/yum`~~
~~`vim /usr/libexec/urlgrabber-ext-down`~~
~~`vim /bin/yum-config-manager`~~
~~把`#! /usr/bin/python`修改为`#! /usr/bin/python2`~~

重新创建`/usr/bin/python3`和`/usr/bin/pip3`的软链接
``` bash
[root@cn-py-dl-r8 Python-3.10.4]# rm -rf /usr/bin/python3
[root@cn-py-dl-r8 Python-3.10.4]# ln -s /usr/local/python3/bin/python3 /usr/bin/python3
[root@cn-py-dl-r8 Python-3.10.4]# rm -rf /usr/bin/pip3
[root@cn-py-dl-r8 Python-3.10.4]# ln -s /usr/local/python3/bin/pip3.10 /usr/bin/pip3
[root@cn-py-dl-r8 Python-3.10.4]# ll /usr/bin | grep py
-rwxr-xr-x. 1 root root        3555 May 15  2019 bno_plot.py
-rwxr-xr-x. 1 root root       15244 Aug 13  2018 lsusb.py
lrwxrwxrwx. 1 root root           6 Aug 12  2018 mcopy -> mtools
-rwxr-xr-x. 1 root root      245864 Oct 20  2021 objcopy
lrwxrwxrwx. 1 root root          30 Apr 23 14:39 pip3 -> /usr/local/python3/bin/pip3.10
lrwxrwxrwx. 1 root root          25 Mar 27 02:07 pydoc-3 -> /etc/alternatives/pydoc-3
lrwxrwxrwx. 1 root root          24 Mar 27 02:07 pydoc3 -> /etc/alternatives/pydoc3
-rwxr-xr-x. 1 root root          89 Sep  9  2021 pydoc3.6
-rwxr-xr-x. 1 root root          78 Aug 11  2021 pydoc3.8
-rwxr-xr-x. 1 root root         404 Nov 15  2018 pyinotify
lrwxrwxrwx. 1 root root          30 Apr 23 14:39 python3 -> /usr/local/python3/bin/python3
lrwxrwxrwx. 1 root root          31 Aug 11  2021 python3.6 -> /usr/libexec/platform-python3.6
lrwxrwxrwx. 1 root root          32 Aug 11  2021 python3.6m -> /usr/libexec/platform-python3.6m
-rwxr-xr-x. 1 root root        7768 Aug 11  2021 python3.8
lrwxrwxrwx. 1 root root          26 Mar 27 02:07 pyvenv-3 -> /etc/alternatives/pyvenv-3
-rwxr-xr-x. 1 root root         446 Sep  9  2021 pyvenv-3.6
-rwxr-xr-x. 1 root root       21488 Jan  3  2020 sg_copy_results
-rwxr-xr-x. 1 root root       41688 Jan  3  2020 sg_xcopy
-rwxr-xr-x. 1 root root       10694 Jul 12  2021 ssh-copy-id
lrwxrwxrwx. 1 root root          24 Mar 27 02:06 unversioned-python -> /etc/alternatives/python
-rwxr-xr-x. 1 root root       42888 Aug 13  2018 xdpyinfo
[root@cn-py-dl-r8 Python-3.10.4]# ll /usr/bin | grep pip
-rwxr-xr-x. 1 root root        3143 Aug 12  2018 lesspipe.sh
lrwxrwxrwx. 1 root root          23 Mar 27 02:07 pip-3 -> /etc/alternatives/pip-3
lrwxrwxrwx. 1 root root          30 Apr 23 14:39 pip3 -> /usr/local/python3/bin/pip3.10
lrwxrwxrwx. 1 root root           8 Jun 18  2021 pip-3.6 -> ./pip3.6
-rwxr-xr-x. 1 root root         209 Jun 18  2021 pip3.6
lrwxrwxrwx. 1 root root           8 Aug 11  2021 pip-3.8 -> ./pip3.8
-rwxr-xr-x. 1 root root         536 Aug 11  2021 pip3.8
-rwxr-xr-x. 1 root root       25440 Jun 23  2020 pipewire
-rwxr-xr-x. 1 root root      437160 Jun 23  2020 pipewire-media-session
[root@cn-py-dl-r8 Python-3.10.4]# python -V
bash: python: command not found...
^C
[root@cn-py-dl-r8 Python-3.10.4]# python3 -V
Python 3.10.4
[root@cn-py-dl-r8 Python-3.10.4]# pip3 -V
pip 22.0.4 from /usr/local/python3/lib/python3.10/site-packages/pip (python 3.10)
[root@cn-py-dl-r8 Python-3.10.4]# python3
Python 3.10.4 (main, Apr 23 2022, 14:21:11) [GCC 8.5.0 20210514 (Red Hat 8.5.0-4)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
[1]+  Stopped                 python3
```
~~这样就可以通过`python`/`python2`命令使用`Python`，`python3`来使用`Python 3`~~好了，`CentOS 8`这下`2`终于彻底没有了

### 8. 升级`pip3`
你云环境下会自动配置镜像源
~~`pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U`~~
~~`pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple`~~
`python3 -m pip install --upgrade pip`
安装`pip3`的另一种方法
``` bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

### 9. 加入环境变量
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

## 0x05.安装[PHPStudy Linux 面板](https://www.xp.cn/linux.html)
![官网](https://i1.yuangezhizao.cn/Win-10/20191016213712.jpg!webp)
![V0.2 公测版](https://i1.yuangezhizao.cn/Win-10/20191016213828.jpg!webp)

一键安装
`yum install -y wget && wget -O install.sh https://download.xp.cn/install.sh && sh install.sh`
![还不错的面板](https://i1.yuangezhizao.cn/Win-10/20191016214057.jpg!webp)
![吊炸天的监控](https://i1.yuangezhizao.cn/Win-10/20191016214130.jpg!webp)

## 0x06.编译安装[Nginx](https://nginx.org/)
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

## 0x07.测试延迟
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
③`cn-tx-bj3-c8`
``` bash
[root@txy ~]# ping jrmkt.jd.com
PING jrmkt.jd.com.gslb.qianxun.com (61.48.89.125) 56(84) bytes of data.
64 bytes from 61.48.89.125 (61.48.89.125): icmp_seq=1 ttl=251 time=7.03 ms
64 bytes from 61.48.89.125 (61.48.89.125): icmp_seq=2 ttl=251 time=7.00 ms
64 bytes from 61.48.89.125 (61.48.89.125): icmp_seq=3 ttl=251 time=7.02 ms
64 bytes from 61.48.89.125 (61.48.89.125): icmp_seq=4 ttl=251 time=7.01 ms
64 bytes from 61.48.89.125 (61.48.89.125): icmp_seq=5 ttl=251 time=7.01 ms
^C
--- jrmkt.jd.com.gslb.qianxun.com ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 1005ms
rtt min/avg/max/mdev = 7.004/7.012/7.029/0.092 ms
```
由此可见家里肯定是最慢的了，另外**北京一区**比**北京三区**快`1ms`

## 0x08.安装[Pyston](https://github.com/pyston/pyston)
`wget https://proxy-cf.yuangezhizao.cn/dl/pyston_2.2_portable.tar.gz`
`tar -zxvf pyston_2.2_portable.tar.gz`
``` bash
[root@txy ~]# ./pyston
Python 3.8.8 (heads/rel2.2:6287d61, Apr 29 2021, 15:46:12)
[Pyston 2.2.0, GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> ^Z
[5]+  Stopped                 ./pyston
```
`./pyston -m venv pyston-venv`
``` bash
(pyston-venv) [root@txy jd]# pip --version`
pip 20.2.3 from /root/jd/pyston-venv/lib/pyston3.8/site-packages/pip (python 3.8)
(pyston-venv) [root@txy sku]# pyston JD_Sku_Demo.py 
Traceback (most recent call last):
  File "JD_Sku_Demo.py", line 3, in <module>
    from JD_Sku.sku import SKu
ImportError: cannot import name 'SKu' from 'JD_Sku.sku' (/root/jd/sku/JD_Sku/sku.py)
(pyston-venv) [root@txy sku]# tree
.
├── cookies.txt
├── examples
│   ├── address.json
│   └── stock.json
├── JD_Sku
│   ├── account.py
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── account.cpython-39.pyc
│   │   ├── account.pyston-22.pyc
│   │   ├── __init__.cpython-39.pyc
│   │   ├── __init__.pyston-22.pyc
│   │   ├── sku.cpython-39.pyc
│   │   ├── sku.pyston-22.pyc
│   │   ├── utf8logger.cpython-39.pyc
│   │   └── utf8logger.pyston-22.pyc
│   ├── sku.py
│   └── utf8logger.py
└── JD_Sku_Demo.py

3 directories, 16 files
(pyston-venv) [root@txy JD_Sku]# rm -rf JD_Sku/__pycache__/
(pyston-venv) [root@txy JD_Sku]# cd ..
(pyston-venv) [root@txy sku]# pyston JD_Sku_Demo.py 
[2021-06-05 20:37:18,286][_get_nick_name:47]【INFO】远哥制造 cookies is OK
[2021-06-05 20:37:18,290][normal_mode:27]【INFO】= = = 就 绪 = = =
[2021-06-05 20:37:18,416][normal_mode:43]【INFO】4953.583314697265
^CTraceback (most recent call last):
  File "JD_Sku_Demo.py", line 10, in <module>
    a.normal_mode('2021-06-05 22:00:00')
  File "/root/jd/sku/JD_Sku/sku.py", line 44, in normal_mode
    time.sleep(cha)
KeyboardInterrupt
```



## 0x10.引用
[python --enable-shared](https://web.archive.org/web/20200521142009/https://www.cnblogs.com/Tommy-Yu/p/6144512.html)
[CentOS 7 升级gcc/g++编译器](https://web.archive.org/web/20200521161733/https://www.cnblogs.com/ToBeExpert/p/10297697.html)
[3.7.0 build error with --enable-optimizations](https://web.archive.org/web/20200521161845/https://bugs.python.org/issue34112)
[开启Link Time Optimization(LTO)后到底有什么优化？](https://web.archive.org/web/20211011094746/https://www.jianshu.com/p/58fef052291a)
[CentOS 源码编译安装 Python3](https://web.archive.org/web/20220111032520/https://www.cnblogs.com/michael-xiang/p/10466819.html)
[在 CentOS 上编译安装 Python 3](https://web.archive.org/web/20220111062219/https://zhuanlan.zhihu.com/p/418309354)
