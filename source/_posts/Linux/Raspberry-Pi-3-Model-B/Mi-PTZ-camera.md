---
title: 米家摄像机云台版同步腾讯云 COS
date: 2020-1-22 19:07:58
tags:
  - Mi
count: 2
os: 0
os_1: 10.0.17763.973 2019-LTSC
browser: 0
browser_1: 74.0.3729.169 Stable
place: 新家
key: 71
---
    狗东 110-100 白条券使用完毕
    然后 19 年的社畜终于结束了草
<!-- more -->
## 0x00.前言
前阵子“非你莫鼠”领到了`110-100`白条优惠券，家里暂时也不需要米、面、油了，想着过年回家一周还得看着这面的情况（`7x24h`不断电的`rpi`以及`远程唤醒`台式机`(〃'▽'〃)`
所以就种草了个这玩楞，然鹅`199`草，看了下价格变化曲线感觉有戏，今天凌晨果然降价，于是立即购买！`(๑*◡*๑)`
![真·标准矩形价格曲线](https://i1.yuangezhizao.cn/Win-10/20200122191606.jpg!webp)
![于是等到凌晨果然降价](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-22-00-07-30-633_com.jingdong.a.jpg!webp)
![-100](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-22-00-12-20-406_com.jingdong.a.jpg!webp)
![一折？](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-22-00-12-48-503_com.jingdong.a.jpg!webp)
![赶紧把快过期的红包勾上](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-22-00-13-12-025_com.jingdong.a.jpg!webp)

预计下午配送，结果早上起来就发现到配送站了，于是立即`wx`联系说家里白天不会有人就扔蜂巢吧……晚上回来就拿到了`(￣▽￣)~*`
![你米外包装](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20200122_180749.jpg!view)

## 0x01.上电
`5V 1A`插菊花，然后这玩楞就突然发出响（语）声（音）草，倒是可海星没有太沙雕，掏出手机扫码再把屏幕上的码给摄像头扫（互扫嘛）就`ok`了`(＾＿－)`
其中还不支持`5G WiFi`还是有点儿遗憾（~~都上`H.265`视频编码了就不能支持下`5G`么草~~，后来才想到`5G`穿墙硬伤

![no 5G](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-22-18-15-38-682_com.xiaomi.sma.jpg!webp)

然后就日常升级固件到最新（毕竟新电子产品拿到手的第一步基本上都是更到最新，即使这并不一定是一个好习惯
![3.5.8_0415](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-22-18-23-01-189_com.xiaomi.sma.jpg!webp)

~~`0415`警觉，区号？~~然后就摸索`App`发现没插存储卡，然后……没找着插槽（一脸黑人问号`⊙▃⊙`
翻了半天开始怀疑人生自己是不是买错了，结果后来搜索到了结果（`(╯°Д°)╯︵┻━┻`

![这个 SD 卡槽的位置真是绝了](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20200122_183010.jpg!view)
![草](https://i1.yuangezhizao.cn/Win-10/20191016005155.jpg!webp)

（忘记先断电就直接）插……入……，之后提示异常，格式化之后就能使了（之前这张卡是给`rpi`做`OSMC`系统的
虽然已经是买的能力范围内最好的卡了，但是限于`3b`的硬件性能（不限于`GPU`）自第一次验证可行性之后就再也没用过了
当然，现在`rpi`装的是最新的官方系统，优化吊炸天异常丝滑，虽然是`32`为系统罢了`(￣.￣)`
于是这张闲置的卡就拿来做摄像头的本地存储了，好歹是`U1`的卡（应该是`Class 10`

![28.8G](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-22-18-32-00-328_com.xiaomi.sma.jpg!webp)

## 0x02.私有云存储
看了下`rpi`的剩余空间，结果还没有存储卡大（废话，毕竟都是`32G`的
``` bash
pi@rpi:~ $ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/root        29G   11G   16G  41% /
devtmpfs        370M     0  370M   0% /dev
tmpfs           374M     0  374M   0% /dev/shm
tmpfs           374M   39M  336M  11% /run
tmpfs           5.0M  4.0K  5.0M   1% /run/lock
tmpfs           374M     0  374M   0% /sys/fs/cgroup
/dev/mmcblk0p1  253M   52M  201M  21% /boot
tmpfs            75M     0   75M   0% /run/user/1000
```
于是准备干脆扔到`COS`上算了，立即开通存储桶
![私有读写 + 服务端加密](https://i1.yuangezhizao.cn/Win-10/20200122201740.png!webp)

### 1.安装[COSFS](https://github.com/tencentyun/cosfs)
先安装编译工具
``` bash
sudo apt-get install automake autotools-dev g++ git libcurl4-gnutls-dev libfuse-dev libssl-dev libxml2-dev make pkg-config fuse -y
```
然后下载源码编译安装，一气呵成（笑
<details><summary>点击此处 ← 查看终端</summary>

``` bash
pi@rpi:~/Downloads $ cd cosfs/
pi@rpi:~/Downloads/cosfs $ ls
aclocal.m4  autom4te.cache  configure     default_commit_hash  Makefile.in  src
AUTHORS     ChangeLog       configure.ac  INSTALL              README.md    test
autogen.sh  config.h.in     COPYING       Makefile.am          scripts
pi@rpi:~/Downloads/cosfs $ ./autogen.sh
--- Make commit hash file -------
--- Finished commit hash file ---
--- Start autotools -------------
configure.ac:31: installing './compile'
configure.ac:27: installing './config.guess'
configure.ac:27: installing './config.sub'
configure.ac:28: installing './install-sh'
configure.ac:28: installing './missing'
src/Makefile.am: installing './depcomp'
parallel-tests: installing './test-driver'
--- Finished autotools ----------
pi@rpi:~/Downloads/cosfs $ ./configure
checking build system type... armv7l-unknown-linux-gnueabihf
checking host system type... armv7l-unknown-linux-gnueabihf
checking target system type... armv7l-unknown-linux-gnueabihf
checking for a BSD-compatible install... /usr/bin/install -c
checking whether build environment is sane... yes
checking for a thread-safe mkdir -p... /bin/mkdir -p
checking for gawk... gawk
checking whether make sets $(MAKE)... yes
checking whether make supports nested variables... yes
checking for g++... g++
checking whether the C++ compiler works... yes
checking for C++ compiler default output file name... a.out
checking for suffix of executables... 
checking whether we are cross compiling... no
checking for suffix of object files... o
checking whether we are using the GNU C++ compiler... yes
checking whether g++ accepts -g... yes
checking whether make supports the include directive... yes (GNU style)
checking dependency style of g++... gcc3
checking for gcc... gcc
checking whether we are using the GNU C compiler... yes
checking whether gcc accepts -g... yes
checking for gcc option to accept ISO C89... none needed
checking whether gcc understands -c and -o together... yes
checking dependency style of gcc... gcc3
checking cosfs build with nettle(GnuTLS)... no
checking cosfs build with OpenSSL... no
checking cosfs build with GnuTLS... no
checking cosfs build with NSS... no
checking for pkg-config... /usr/bin/pkg-config
checking pkg-config is at least version 0.9.0... yes
checking for common_lib_checking... yes
checking compile cosfs with... OpenSSL
checking for DEPS... yes
checking for malloc_trim... yes
checking pthread mutex recursive... PTHREAD_MUTEX_RECURSIVE
checking for git... yes
checking for .git... yes
checking github short commit hash... ca01099
checking that generated files are newer than configure... done
configure: creating ./config.status
config.status: creating Makefile
config.status: creating src/Makefile
config.status: creating test/Makefile
config.status: creating config.h
config.status: executing depfiles commands
pi@rpi:~/Downloads/cosfs $ make
(CDPATH="${ZSH_VERSION+.}:" && cd . && /bin/bash /home/pi/Downloads/cosfs/missing autoheader)
rm -f stamp-h1
touch config.h.in
cd . && /bin/bash ./config.status config.h
config.status: creating config.h
config.status: config.h is unchanged
make  all-recursive
make[1]: Entering directory '/home/pi/Downloads/cosfs'
Making all in src
make[2]: Entering directory '/home/pi/Downloads/cosfs/src'
g++ -DHAVE_CONFIG_H -I. -I..  -D_FILE_OFFSET_BITS=64 -I/usr/include/fuse -I/usr/include/arm-linux-gnueabihf -I/usr/include/libxml2    -g -O2 -Wall -D_FILE_OFFSET_BITS=64 -MT s3fs.o -MD -MP -MF .deps/s3fs.Tpo -c -o s3fs.o s3fs.cpp
s3fs.cpp:176:12: warning: ‘int check_for_oss_format()’ declared ‘static’ but never defined [-Wunused-function]
 static int check_for_oss_format(void);
            ^~~~~~~~~~~~~~~~~~~~
s3fs.cpp:864:12: warning: ‘int do_create_bucket()’ defined but not used [-Wunused-function]
 static int do_create_bucket(void)
            ^~~~~~~~~~~~~~~~
s3fs.cpp:126:13: warning: ‘create_bucket’ defined but not used [-Wunused-variable]
 static bool create_bucket         = false;
             ^~~~~~~~~~~~~
mv -f .deps/s3fs.Tpo .deps/s3fs.Po
g++ -DHAVE_CONFIG_H -I. -I..  -D_FILE_OFFSET_BITS=64 -I/usr/include/fuse -I/usr/include/arm-linux-gnueabihf -I/usr/include/libxml2    -g -O2 -Wall -D_FILE_OFFSET_BITS=64 -MT curl.o -MD -MP -MF .deps/curl.Tpo -c -o curl.o curl.cpp
curl.cpp: In static member function ‘static bool S3fsCurl::UploadMultipartPostCallback(S3fsCurl*)’:
curl.cpp:1126:11: warning: comparison of integer expressions of different signedness: ‘int’ and ‘std::__cxx11::basic_string<char>::size_type’ {aka ‘unsigned int’} [-Wsign-compare]
   if (pos != std::string::npos) {
       ~~~~^~~~~~
curl.cpp: In member function ‘int S3fsCurl::UploadMultipartPostRequest(const char*, int, std::__cxx11::string&)’:
curl.cpp:3017:15: warning: comparison of integer expressions of different signedness: ‘int’ and ‘std::__cxx11::basic_string<char>::size_type’ {aka ‘unsigned int’} [-Wsign-compare]
       if (pos != std::string::npos) {
           ~~~~^~~~~~
curl.cpp: In member function ‘int S3fsCurl::GetObjectRequest(const char*, int, off_t, ssize_t)’:
curl.cpp:2551:40: warning: ‘ssetype’ may be used uninitialized in this function [-Wmaybe-uninitialized]
   if(0 != (result = PreGetObjectRequest(tpath, fd, start, size, ssetype, ssevalue))){
                     ~~~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
curl.cpp: In static member function ‘static int S3fsCurl::ParallelGetObjectRequest(const char*, int, off_t, ssize_t)’:
curl.cpp:1330:59: warning: ‘ssetype’ may be used uninitialized in this function [-Wmaybe-uninitialized]
       if(0 != (result = s3fscurl_para->PreGetObjectRequest(tpath, fd, (start + size - remaining_bytes), chunk, ssetype, ssevalue))){
                         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
mv -f .deps/curl.Tpo .deps/curl.Po
g++ -DHAVE_CONFIG_H -I. -I..  -D_FILE_OFFSET_BITS=64 -I/usr/include/fuse -I/usr/include/arm-linux-gnueabihf -I/usr/include/libxml2    -g -O2 -Wall -D_FILE_OFFSET_BITS=64 -MT cache.o -MD -MP -MF .deps/cache.Tpo -c -o cache.o cache.cpp
In file included from cache.h:23,
                 from cache.cpp:35:
cache.cpp: In member function ‘bool StatCache::IncSize(const string&, ssize_t)’:
common.h:81:28: warning: format ‘%ld’ expects argument of type ‘long int’, but argument 9 has type ‘__off64_t’ {aka ‘long long int’} [-Wformat=]
            fprintf(stdout, "%s%s%s:%s(%d): " fmt "%s\n", S3FS_LOG_LEVEL_STRING(level), S3FS_LOG_NEST(nest), __FILE__, __func__, __LINE__, __VA_ARGS__); \
                            ^~~~~~~~~~~~~~~~~~~~~~~~~~~~
common.h:107:35: note: in expansion of macro ‘S3FS_LOW_LOGPRN2’
 #define S3FS_PRN_INFO3(fmt, ...)  S3FS_LOW_LOGPRN2(S3FS_LOG_INFO, 3, fmt, ##__VA_ARGS__, "")
                                   ^~~~~~~~~~~~~~~~
cache.cpp:311:3: note: in expansion of macro ‘S3FS_PRN_INFO3’
   S3FS_PRN_INFO3(
   ^~~~~~~~~~~~~~
common.h:81:28: warning: format ‘%ld’ expects argument of type ‘long int’, but argument 10 has type ‘ssize_t’ {aka ‘int’} [-Wformat=]
            fprintf(stdout, "%s%s%s:%s(%d): " fmt "%s\n", S3FS_LOG_LEVEL_STRING(level), S3FS_LOG_NEST(nest), __FILE__, __func__, __LINE__, __VA_ARGS__); \
                            ^~~~~~~~~~~~~~~~~~~~~~~~~~~~
common.h:107:35: note: in expansion of macro ‘S3FS_LOW_LOGPRN2’
 #define S3FS_PRN_INFO3(fmt, ...)  S3FS_LOW_LOGPRN2(S3FS_LOG_INFO, 3, fmt, ##__VA_ARGS__, "")
                                   ^~~~~~~~~~~~~~~~
cache.cpp:311:3: note: in expansion of macro ‘S3FS_PRN_INFO3’
   S3FS_PRN_INFO3(
   ^~~~~~~~~~~~~~
common.h:83:52: warning: format ‘%ld’ expects argument of type ‘long int’, but argument 10 has type ‘__off64_’ {aka ‘long long int’} [-Wformat=]
            syslog(S3FS_LOG_LEVEL_TO_SYSLOG(level), "[tid:%ld]%s%s%s:%s(%d): " fmt "%s\n", syscall(SYS_gettid), S3FS_LOG_LEVEL_STRING(level), S3FS_LOG_NEST(nest), __FILE__, __func__, __LINE__, __VA_ARGS__); \
                                                    ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
common.h:107:35: note: in expansion of macro ‘S3FS_LOW_LOGPRN2’
 #define S3FS_PRN_INFO3(fmt, ...)  S3FS_LOW_LOGPRN2(S3FS_LOG_INFO, 3, fmt, ##__VA_ARGS__, "")
                                   ^~~~~~~~~~~~~~~~
cache.cpp:311:3: note: in expansion of macro ‘S3FS_PRN_INFO3’
   S3FS_PRN_INFO3(
   ^~~~~~~~~~~~~~
common.h:83:52: warning: format ‘%ld’ expects argument of type ‘long int’, but argument 11 has type ‘ssize_t’ {aka ‘int’} [-Wformat=]
            syslog(S3FS_LOG_LEVEL_TO_SYSLOG(level), "[tid:%ld]%s%s%s:%s(%d): " fmt "%s\n", syscall(SYS_gettid), S3FS_LOG_LEVEL_STRING(level), S3FS_LOG_NEST(nest), __FILE__, __func__, __LINE__, __VA_ARGS__); \
                                                    ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
common.h:107:35: note: in expansion of macro ‘S3FS_LOW_LOGPRN2’
 #define S3FS_PRN_INFO3(fmt, ...)  S3FS_LOW_LOGPRN2(S3FS_LOG_INFO, 3, fmt, ##__VA_ARGS__, "")
                                   ^~~~~~~~~~~~~~~~
cache.cpp:311:3: note: in expansion of macro ‘S3FS_PRN_INFO3’
   S3FS_PRN_INFO3(
   ^~~~~~~~~~~~~~
mv -f .deps/cache.Tpo .deps/cache.Po
g++ -DHAVE_CONFIG_H -I. -I..  -D_FILE_OFFSET_BITS=64 -I/usr/include/fuse -I/usr/include/arm-linux-gnueabihf -I/usr/include/libxml2    -g -O2 -Wall -D_FILE_OFFSET_BITS=64 -MT string_util.o -MD -MP -MF .deps/string_util.Tpo -c -o string_util.o string_util.cpp
mv -f .deps/string_util.Tpo .deps/string_util.Po
g++ -DHAVE_CONFIG_H -I. -I..  -D_FILE_OFFSET_BITS=64 -I/usr/include/fuse -I/usr/include/arm-linux-gnueabihf -I/usr/include/libxml2    -g -O2 -Wall -D_FILE_OFFSET_BITS=64 -MT s3fs_util.o -MD -MP -MF .deps/s3fs_util.Tpo -c -o s3fs_util.o s3fs_util.cpp
mv -f .deps/s3fs_util.Tpo .deps/s3fs_util.Po
g++ -DHAVE_CONFIG_H -I. -I..  -D_FILE_OFFSET_BITS=64 -I/usr/include/fuse -I/usr/include/arm-linux-gnueabihf -I/usr/include/libxml2    -g -O2 -Wall -D_FILE_OFFSET_BITS=64 -MT fdcache.o -MD -MP -MF .deps/fdcache.Tpo -c -o fdcache.o fdcache.cpp
In file included from fdcache.cpp:42:
fdcache.cpp: In member function ‘int FdEntity::NoCacheLoadAndPost(off_t, size_t)’:
common.h:72:28: warning: format ‘%zd’ expects argument of type ‘signed size_t’, but argument 7 has type ‘off_’ {aka ‘long long int’} [-Wformat=]
            fprintf(stdout, "%s%s:%s(%d): " fmt "%s\n", S3FS_LOG_LEVEL_STRING(level), __FILE__, __func__, __LINE__, __VA_ARGS__); \
                            ^~~~~~~~~~~~~~~~~~~~~~~~~~
common.h:100:35: note: in expansion of macro ‘S3FS_LOW_LOGPRN’
 #define S3FS_PRN_ERR(fmt, ...)    S3FS_LOW_LOGPRN(S3FS_LOG_ERR,  fmt, ##__VA_ARGS__, "")
                                   ^~~~~~~~~~~~~~~
fdcache.cpp:1181:13: note: in expansion of macro ‘S3FS_PRN_ERR’
             S3FS_PRN_ERR("failed to get object(start=%zd, size=%zu) for file(%d).", offset, oneread, tmpfd);
             ^~~~~~~~~~~~
In file included from fdcache.cpp:42:
common.h:74:52: warning: format ‘%zd’ expects argument of type ‘signed size_t’, but argument 7 has type ‘off_’ {aka ‘long long int’} [-Wformat=]
            syslog(S3FS_LOG_LEVEL_TO_SYSLOG(level), "[tid:%ld]%s:%s(%d): " fmt "%s", syscall(SYS_gettid), __FILE__, __func__, __LINE__, __VA_ARGS__); \
                                                    ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
common.h:100:35: note: in expansion of macro ‘S3FS_LOW_LOGPRN’
 #define S3FS_PRN_ERR(fmt, ...)    S3FS_LOW_LOGPRN(S3FS_LOG_ERR,  fmt, ##__VA_ARGS__, "")
                                   ^~~~~~~~~~~~~~~
fdcache.cpp:1181:13: note: in expansion of macro ‘S3FS_PRN_ERR’
             S3FS_PRN_ERR("failed to get object(start=%zd, size=%zu) for file(%d).", offset, oneread, tmpfd);
             ^~~~~~~~~~~~
In file included from fdcache.cpp:42:
common.h:72:28: warning: format ‘%zd’ expects argument of type ‘signed size_t’, but argument 7 has type ‘off_’ {aka ‘long long int’} [-Wformat=]
            fprintf(stdout, "%s%s:%s(%d): " fmt "%s\n", S3FS_LOG_LEVEL_STRING(level), __FILE__, __func__, __LINE__, __VA_ARGS__); \
                            ^~~~~~~~~~~~~~~~~~~~~~~~~~
common.h:100:35: note: in expansion of macro ‘S3FS_LOW_LOGPRN’
 #define S3FS_PRN_ERR(fmt, ...)    S3FS_LOW_LOGPRN(S3FS_LOG_ERR,  fmt, ##__VA_ARGS__, "")
                                   ^~~~~~~~~~~~~~~
fdcache.cpp:1201:9: note: in expansion of macro ‘S3FS_PRN_ERR’
         S3FS_PRN_ERR("failed to multipart post(start=%zd, size=%zu) for file(%d).", offset, oneread, upload_fd);
         ^~~~~~~~~~~~
In file included from fdcache.cpp:42:
common.h:74:52: warning: format ‘%zd’ expects argument of type ‘signed size_t’, but argument 7 has type ‘off_’ {aka ‘long long int’} [-Wformat=]
            syslog(S3FS_LOG_LEVEL_TO_SYSLOG(level), "[tid:%ld]%s:%s(%d): " fmt "%s", syscall(SYS_gettid), __FILE__, __func__, __LINE__, __VA_ARGS__); \
                                                    ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
common.h:100:35: note: in expansion of macro ‘S3FS_LOW_LOGPRN’
 #define S3FS_PRN_ERR(fmt, ...)    S3FS_LOW_LOGPRN(S3FS_LOG_ERR,  fmt, ##__VA_ARGS__, "")
                                   ^~~~~~~~~~~~~~~
fdcache.cpp:1201:9: note: in expansion of macro ‘S3FS_PRN_ERR’
         S3FS_PRN_ERR("failed to multipart post(start=%zd, size=%zu) for file(%d).", offset, oneread, upload_fd);
         ^~~~~~~~~~~~
In file included from fdcache.cpp:42:
fdcache.cpp: In member function ‘int FdEntity::RowFlush(const char*, bool)’:
common.h:72:28: warning: format ‘%zd’ expects argument of type ‘signed size_t’, but argument 7 has type ‘off_’ {aka ‘long long int’} [-Wformat=]
            fprintf(stdout, "%s%s:%s(%d): " fmt "%s\n", S3FS_LOG_LEVEL_STRING(level), __FILE__, __func__, __LINE__, __VA_ARGS__); \
                            ^~~~~~~~~~~~~~~~~~~~~~~~~~
common.h:100:35: note: in expansion of macro ‘S3FS_LOW_LOGPRN’
 #define S3FS_PRN_ERR(fmt, ...)    S3FS_LOW_LOGPRN(S3FS_LOG_ERR,  fmt, ##__VA_ARGS__, "")
                                   ^~~~~~~~~~~~~~~
fdcache.cpp:1397:9: note: in expansion of macro ‘S3FS_PRN_ERR’
         S3FS_PRN_ERR("failed to multipart post(start=%zd, size=%zu) for file(%d).", mp_start, mp_size, fd);
         ^~~~~~~~~~~~
In file included from fdcache.cpp:42:
common.h:74:52: warning: format ‘%zd’ expects argument of type ‘signed size_t’, but argument 7 has type ‘off_’ {aka ‘long long int’} [-Wformat=]
            syslog(S3FS_LOG_LEVEL_TO_SYSLOG(level), "[tid:%ld]%s:%s(%d): " fmt "%s", syscall(SYS_gettid), __FILE__, __func__, __LINE__, __VA_ARGS__); \
                                                    ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
common.h:100:35: note: in expansion of macro ‘S3FS_LOW_LOGPRN’
 #define S3FS_PRN_ERR(fmt, ...)    S3FS_LOW_LOGPRN(S3FS_LOG_ERR,  fmt, ##__VA_ARGS__, "")
                                   ^~~~~~~~~~~~~~~
fdcache.cpp:1397:9: note: in expansion of macro ‘S3FS_PRN_ERR’
         S3FS_PRN_ERR("failed to multipart post(start=%zd, size=%zu) for file(%d).", mp_start, mp_size, fd);
         ^~~~~~~~~~~~
In file included from fdcache.cpp:42:
fdcache.cpp: In member function ‘ssize_t FdEntity::Write(const char*, off_t, size_t)’:
common.h:72:28: warning: format ‘%zd’ expects argument of type ‘signed size_t’, but argument 7 has type ‘off_’ {aka ‘long long int’} [-Wformat=]
            fprintf(stdout, "%s%s:%s(%d): " fmt "%s\n", S3FS_LOG_LEVEL_STRING(level), __FILE__, __func__, __LINE__, __VA_ARGS__); \
                            ^~~~~~~~~~~~~~~~~~~~~~~~~~
common.h:100:35: note: in expansion of macro ‘S3FS_LOW_LOGPRN’
 #define S3FS_PRN_ERR(fmt, ...)    S3FS_LOW_LOGPRN(S3FS_LOG_ERR,  fmt, ##__VA_ARGS__, "")
                                   ^~~~~~~~~~~~~~~
fdcache.cpp:1540:9: note: in expansion of macro ‘S3FS_PRN_ERR’
         S3FS_PRN_ERR("failed to multipart post(start=%zd, size=%zu) for file(%d).", mp_start, mp_size, fd);
         ^~~~~~~~~~~~
In file included from fdcache.cpp:42:
common.h:74:52: warning: format ‘%zd’ expects argument of type ‘signed size_t’, but argument 7 has type ‘off_’ {aka ‘long long int’} [-Wformat=]
            syslog(S3FS_LOG_LEVEL_TO_SYSLOG(level), "[tid:%ld]%s:%s(%d): " fmt "%s", syscall(SYS_gettid), __FILE__, __func__, __LINE__, __VA_ARGS__); \
                                                    ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
common.h:100:35: note: in expansion of macro ‘S3FS_LOW_LOGPRN’
 #define S3FS_PRN_ERR(fmt, ...)    S3FS_LOW_LOGPRN(S3FS_LOG_ERR,  fmt, ##__VA_ARGS__, "")
                                   ^~~~~~~~~~~~~~~
fdcache.cpp:1540:9: note: in expansion of macro ‘S3FS_PRN_ERR’
         S3FS_PRN_ERR("failed to multipart post(start=%zd, size=%zu) for file(%d).", mp_start, mp_size, fd);
         ^~~~~~~~~~~~
In file included from fdcache.cpp:42:
common.h:72:28: warning: format ‘%ld’ expects argument of type ‘long int’, but argument 8 has type ‘ssize_t’ {aka ‘int’} [-Wformat=]
            fprintf(stdout, "%s%s:%s(%d): " fmt "%s\n", S3FS_LOG_LEVEL_STRING(level), __FILE__, __func__, __LINE__, __VA_ARGS__); \
                            ^~~~~~~~~~~~~~~~~~~~~~~~~~
common.h:100:35: note: in expansion of macro ‘S3FS_LOW_LOGPRN’
 #define S3FS_PRN_ERR(fmt, ...)    S3FS_LOW_LOGPRN(S3FS_LOG_ERR,  fmt, ##__VA_ARGS__, "")
                                   ^~~~~~~~~~~~~~~
fdcache.cpp:1559:4: note: in expansion of macro ‘S3FS_PRN_ERR’
    S3FS_PRN_ERR("failed to update file size in stat cache(path=%s, size=%ld).", path.c_str(), wsize);
    ^~~~~~~~~~~~
In file included from fdcache.cpp:42:
common.h:74:52: warning: format ‘%ld’ expects argument of type ‘long int’, but argument 8 has type ‘ssize_t’ {aka ‘int’} [-Wformat=]
            syslog(S3FS_LOG_LEVEL_TO_SYSLOG(level), "[tid:%ld]%s:%s(%d): " fmt "%s", syscall(SYS_gettid), __FILE__, __func__, __LINE__, __VA_ARGS__); \
                                                    ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
common.h:100:35: note: in expansion of macro ‘S3FS_LOW_LOGPRN’
 #define S3FS_PRN_ERR(fmt, ...)    S3FS_LOW_LOGPRN(S3FS_LOG_ERR,  fmt, ##__VA_ARGS__, "")
                                   ^~~~~~~~~~~~~~~
fdcache.cpp:1559:4: note: in expansion of macro ‘S3FS_PRN_ERR’
    S3FS_PRN_ERR("failed to update file size in stat cache(path=%s, size=%ld).", path.c_str(), wsize);
    ^~~~~~~~~~~~
mv -f .deps/fdcache.Tpo .deps/fdcache.Po
g++ -DHAVE_CONFIG_H -I. -I..  -D_FILE_OFFSET_BITS=64 -I/usr/include/fuse -I/usr/include/arm-linux-gnueabihf -I/usr/include/libxml2    -g -O2 -Wall -D_FILE_OFFSET_BITS=64 -MT common_auth.o -MD -MP -MF .deps/common_auth.Tpo -c -o common_auth.o common_auth.cpp
common_auth.cpp: In function ‘std::__cxx11::string s3fs_sha256sum(int, off_t, ssize_t)’:
common_auth.cpp:84:12: warning: ‘char* strncat(char*, const char*, size_t)’ output may be truncated copying 2 bytes from a string of length 2 [-Wstringop-truncation]
     strncat(sha256, hexbuf, 2);
     ~~~~~~~^~~~~~~~~~~~~~~~~~~
mv -f .deps/common_auth.Tpo .deps/common_auth.Po
g++ -DHAVE_CONFIG_H -I. -I..  -D_FILE_OFFSET_BITS=64 -I/usr/include/fuse -I/usr/include/arm-linux-gnueabihf -I/usr/include/libxml2    -g -O2 -Wall -D_FILE_OFFSET_BITS=64 -MT openssl_auth.o -MD -MP -MF .deps/openssl_auth.Tpo -c -o openssl_auth.o openssl_auth.cpp
openssl_auth.cpp:127:13: warning: ‘void s3fs_destroy_dyn_crypt_mutex(CRYPTO_dynlock_value*, const char*, int)’ defined but not used [-Wunused-function]
 static void s3fs_destroy_dyn_crypt_mutex(struct CRYPTO_dynlock_value* dyndata, const char* file, int line)
             ^~~~~~~~~~~~~~~~~~~~~~~~~~~~
openssl_auth.cpp:116:13: warning: ‘void s3fs_dyn_crypt_mutex_lock(int, CRYPTO_dynlock_value*, const char*, int)’ defined but not used [-Wunused-function]
 static void s3fs_dyn_crypt_mutex_lock(int mode, struct CRYPTO_dynlock_value* dyndata, const char* file, int line)
             ^~~~~~~~~~~~~~~~~~~~~~~~~
openssl_auth.cpp:104:37: warning: ‘CRYPTO_dynlock_value* s3fs_dyn_crypt_mutex(const char*, int)’ defined but not used [-Wunused-function]
 static struct CRYPTO_dynlock_value* s3fs_dyn_crypt_mutex(const char* file, int line)
                                     ^~~~~~~~~~~~~~~~~~~~
openssl_auth.cpp:97:22: warning: ‘long unsigned int s3fs_crypt_get_threadid()’ defined but not used [-Wunused-function]
 static unsigned long s3fs_crypt_get_threadid(void)
                      ^~~~~~~~~~~~~~~~~~~~~~~
openssl_auth.cpp:86:13: warning: ‘void s3fs_crypt_mutex_lock(int, int, const char*, int)’ defined but not used [-Wunused-function]
 static void s3fs_crypt_mutex_lock(int mode, int pos, const char* file, int line)
             ^~~~~~~~~~~~~~~~~~~~~
mv -f .deps/openssl_auth.Tpo .deps/openssl_auth.Po
g++  -g -O2 -Wall -D_FILE_OFFSET_BITS=64   -o cosfs s3fs.o curl.o cache.o string_util.o s3fs_util.o fdcache.o common_auth.o openssl_auth.o   -lfuse -pthread -lcurl -lxml2 -lcrypto 
g++ -DHAVE_CONFIG_H -I. -I..  -D_FILE_OFFSET_BITS=64 -I/usr/include/fuse -I/usr/include/arm-linux-gnueabihf -I/usr/include/libxml2    -g -O2 -Wall -D_FILE_OFFSET_BITS=64 -MT test_string_util.o -MD -MP -MF .deps/test_string_util.Tpo -c -o test_string_util.o test_string_util.cpp
mv -f .deps/test_string_util.Tpo .deps/test_string_util.Po
g++  -g -O2 -Wall -D_FILE_OFFSET_BITS=64   -o test_string_util string_util.o test_string_util.o  
make[2]: Leaving directory '/home/pi/Downloads/cosfs/src'
Making all in test
make[2]: Entering directory '/home/pi/Downloads/cosfs/test'
make[2]: Nothing to be done for 'all'.
make[2]: Leaving directory '/home/pi/Downloads/cosfs/test'
make[2]: Entering directory '/home/pi/Downloads/cosfs'
make[2]: Leaving directory '/home/pi/Downloads/cosfs'
make[1]: Leaving directory '/home/pi/Downloads/cosfs'
pi@rpi:~/Downloads/cosfs $ sudo make install
Making install in src
make[1]: Entering directory '/home/pi/Downloads/cosfs/src'
make[2]: Entering directory '/home/pi/Downloads/cosfs/src'
 /bin/mkdir -p '/usr/local/bin'
  /usr/bin/install -c cosfs '/usr/local/bin'
make[2]: Nothing to be done for 'install-data-am'.
make[2]: Leaving directory '/home/pi/Downloads/cosfs/src'
make[1]: Leaving directory '/home/pi/Downloads/cosfs/src'
Making install in test
make[1]: Entering directory '/home/pi/Downloads/cosfs/test'
make[2]: Entering directory '/home/pi/Downloads/cosfs/test'
make[2]: Nothing to be done for 'install-exec-am'.
make[2]: Nothing to be done for 'install-data-am'.
make[2]: Leaving directory '/home/pi/Downloads/cosfs/test'
make[1]: Leaving directory '/home/pi/Downloads/cosfs/test'
make[1]: Entering directory '/home/pi/Downloads/cosfs'
make[2]: Entering directory '/home/pi/Downloads/cosfs'
make[2]: Nothing to be done for 'install-exec-am'.
make[2]: Nothing to be done for 'install-data-am'.
make[2]: Leaving directory '/home/pi/Downloads/cosfs'
make[1]: Leaving directory '/home/pi/Downloads/cosfs'
pi@rpi:~/Downloads/cosfs $ 
```
</details>

新建配置文件
```
echo rpi-<rm>:<rm>:<rm> > passwd-cosfs
sudo mv passwd-cosfs /etc/passwd-cosfs
chmod 640 /etc/passwd-cosfs
```
挂载启动
```
mkdir /tmp/cosfs
cosfs rpi-<rm> /tmp/cosfs -ourl=http://cos.ap-beijing.myqcloud.com -odbglevel=info -ouse_cache=/path/to/local_cache
```
> `-ouse_cache`指定了使用本地`cache`来缓存临时文件，进一步提高性能，如果不需要本地`cache`或者本地磁盘容量有限，可不指定该选项

### 2.安装`SMB`
``` bash
sudo apt install samba
```

<details><summary>点击此处 ← 查看终端</summary>

```
pi@rpi:~ $ sudo apt install samba
Reading package lists... Done
Building dependency tree       
Reading state information... Done
The following additional packages will be installed:
  attr ibverbs-providers libboost-regex1.67.0 libcephfs2 libgfapi0 libgfrpc0 libgfxdr0 libglusterfs0
  libibverbs1 librados2 python-dnspython python-gpg python-ldb python-samba python-tdb samba-common
  samba-common-bin samba-dsdb-modules samba-vfs-modules tdb-tools
Suggested packages:
  bind9 bind9utils ctdb ldb-tools ntp | chrony smbldap-tools ufw winbind heimdal-clients
The following NEW packages will be installed:
  attr ibverbs-providers libboost-regex1.67.0 libcephfs2 libgfapi0 libgfrpc0 libgfxdr0 libglusterfs0
  libibverbs1 librados2 python-dnspython python-gpg python-ldb python-samba python-tdb samba samba-common
  samba-common-bin samba-dsdb-modules samba-vfs-modules tdb-tools
0 upgraded, 21 newly installed, 0 to remove and 56 not upgraded.
Need to get 18.2 MB of archives.
After this operation, 62.7 MB of additional disk space will be used.
Do you want to continue? [Y/n] y
Get:1 http://mirrors.ustc.edu.cn/raspbian/raspbian buster/main armhf python-dnspython all 1.16.0-1 [90.1 kB]
Get:2 http://mirrors.ustc.edu.cn/raspbian/raspbian buster/main armhf python-ldb armhf 2:1.5.1+really1.4.6-3 [33.1 kB]
Get:3 http://mirrors.ustc.edu.cn/raspbian/raspbian buster/main armhf python-tdb armhf 1.3.16-2+b1 [16.0 kB]  
Get:4 http://mirrors.ustc.edu.cn/raspbian/raspbian buster/main armhf python-samba armhf 2:4.9.5+dfsg-5+deb10u1+rpi1 [1,794 kB]
Get:5 http://mirrors.ustc.edu.cn/raspbian/raspbian buster/main armhf samba-common all 2:4.9.5+dfsg-5+deb10u1+rpi1 [170 kB]
Get:6 http://mirrors.ustc.edu.cn/raspbian/raspbian buster/main armhf samba-common-bin armhf 2:4.9.5+dfsg-5+deb10u1+rpi1 [570 kB]
Get:7 http://mirrors.ustc.edu.cn/raspbian/raspbian buster/main armhf tdb-tools armhf 1.3.16-2+b1 [26.9 kB]
Get:8 http://mirrors.ustc.edu.cn/raspbian/raspbian buster/main armhf samba armhf 2:4.9.5+dfsg-5+deb10u1+rpi1 [1,010 kB]
Get:9 http://mirrors.ustc.edu.cn/raspbian/raspbian buster/main armhf attr armhf 1:2.4.48-4 [39.4 kB]
Get:10 http://mirrors.ustc.edu.cn/raspbian/raspbian buster/main armhf libibverbs1 armhf 22.1-1 [43.5 kB]
Get:11 http://mirrors.ustc.edu.cn/raspbian/raspbian buster/main armhf ibverbs-providers armhf 22.1-1 [20.2 kB]
Get:12 http://mirrors.ustc.edu.cn/raspbian/raspbian buster/main armhf libboost-regex1.67.0 armhf 1.67.0-13 [430 kB]
Get:13 http://mirrors.ustc.edu.cn/raspbian/raspbian buster/main armhf librados2 armhf 12.2.11+dfsg1-2.1+rpi1 [2,337 kB]
Get:14 http://mirrors.ustc.edu.cn/raspbian/raspbian buster/main armhf libcephfs2 armhf 12.2.11+dfsg1-2.1+rpi1 [380 kB]
Get:15 http://mirrors.ustc.edu.cn/raspbian/raspbian buster/main armhf libglusterfs0 armhf 5.5-3 [2,724 kB]   
Get:16 http://mirrors.ustc.edu.cn/raspbian/raspbian buster/main armhf libgfxdr0 armhf 5.5-3 [2,488 kB]       
Get:17 http://mirrors.ustc.edu.cn/raspbian/raspbian buster/main armhf libgfrpc0 armhf 5.5-3 [2,506 kB]       
Get:18 http://mirrors.ustc.edu.cn/raspbian/raspbian buster/main armhf libgfapi0 armhf 5.5-3 [2,524 kB]       
Get:19 http://mirrors.ustc.edu.cn/raspbian/raspbian buster/main armhf python-gpg armhf 1.12.0-6 [275 kB]     
Get:20 http://mirrors.ustc.edu.cn/raspbian/raspbian buster/main armhf samba-dsdb-modules armhf 2:4.9.5+dfsg-5+deb10u1+rpi1 [345 kB]
Get:21 http://mirrors.ustc.edu.cn/raspbian/raspbian buster/main armhf samba-vfs-modules armhf 2:4.9.5+dfsg-5+deb10u1+rpi1 [400 kB]
Fetched 18.2 MB in 1min 10s (259 kB/s)                                                                       
Preconfiguring packages ...
Selecting previously unselected package python-dnspython.
(Reading database ... 160887 files and directories currently installed.)
Preparing to unpack .../00-python-dnspython_1.16.0-1_all.deb ...
Unpacking python-dnspython (1.16.0-1) ...
Selecting previously unselected package python-ldb.
Preparing to unpack .../01-python-ldb_2%3a1.5.1+really1.4.6-3_armhf.deb ...
Unpacking python-ldb (2:1.5.1+really1.4.6-3) ...
Selecting previously unselected package python-tdb.
Preparing to unpack .../02-python-tdb_1.3.16-2+b1_armhf.deb ...
Unpacking python-tdb (1.3.16-2+b1) ...
Selecting previously unselected package python-samba.
Preparing to unpack .../03-python-samba_2%3a4.9.5+dfsg-5+deb10u1+rpi1_armhf.deb ...
Unpacking python-samba (2:4.9.5+dfsg-5+deb10u1+rpi1) ...
Selecting previously unselected package samba-common.
Preparing to unpack .../04-samba-common_2%3a4.9.5+dfsg-5+deb10u1+rpi1_all.deb ...
Unpacking samba-common (2:4.9.5+dfsg-5+deb10u1+rpi1) ...
Selecting previously unselected package samba-common-bin.
Preparing to unpack .../05-samba-common-bin_2%3a4.9.5+dfsg-5+deb10u1+rpi1_armhf.deb ...
Unpacking samba-common-bin (2:4.9.5+dfsg-5+deb10u1+rpi1) ...
Selecting previously unselected package tdb-tools.
Preparing to unpack .../06-tdb-tools_1.3.16-2+b1_armhf.deb ...
Unpacking tdb-tools (1.3.16-2+b1) ...
Selecting previously unselected package samba.
Preparing to unpack .../07-samba_2%3a4.9.5+dfsg-5+deb10u1+rpi1_armhf.deb ...
Unpacking samba (2:4.9.5+dfsg-5+deb10u1+rpi1) ...
Selecting previously unselected package attr.
Preparing to unpack .../08-attr_1%3a2.4.48-4_armhf.deb ...
Unpacking attr (1:2.4.48-4) ...
Selecting previously unselected package libibverbs1:armhf.
Preparing to unpack .../09-libibverbs1_22.1-1_armhf.deb ...
Unpacking libibverbs1:armhf (22.1-1) ...
Selecting previously unselected package ibverbs-providers:armhf.
Preparing to unpack .../10-ibverbs-providers_22.1-1_armhf.deb ...
Unpacking ibverbs-providers:armhf (22.1-1) ...
Selecting previously unselected package libboost-regex1.67.0:armhf.
Preparing to unpack .../11-libboost-regex1.67.0_1.67.0-13_armhf.deb ...
Unpacking libboost-regex1.67.0:armhf (1.67.0-13) ...
Selecting previously unselected package librados2:armhf.
Preparing to unpack .../12-librados2_12.2.11+dfsg1-2.1+rpi1_armhf.deb ...
Unpacking librados2:armhf (12.2.11+dfsg1-2.1+rpi1) ...
Selecting previously unselected package libcephfs2:armhf.
Preparing to unpack .../13-libcephfs2_12.2.11+dfsg1-2.1+rpi1_armhf.deb ...
Unpacking libcephfs2:armhf (12.2.11+dfsg1-2.1+rpi1) ...
Selecting previously unselected package libglusterfs0:armhf.
Preparing to unpack .../14-libglusterfs0_5.5-3_armhf.deb ...
Unpacking libglusterfs0:armhf (5.5-3) ...
Selecting previously unselected package libgfxdr0:armhf.
Preparing to unpack .../15-libgfxdr0_5.5-3_armhf.deb ...
Unpacking libgfxdr0:armhf (5.5-3) ...
Selecting previously unselected package libgfrpc0:armhf.
Preparing to unpack .../16-libgfrpc0_5.5-3_armhf.deb ...
Unpacking libgfrpc0:armhf (5.5-3) ...
Selecting previously unselected package libgfapi0:armhf.
Preparing to unpack .../17-libgfapi0_5.5-3_armhf.deb ...
Unpacking libgfapi0:armhf (5.5-3) ...
Selecting previously unselected package python-gpg.
Preparing to unpack .../18-python-gpg_1.12.0-6_armhf.deb ...
Unpacking python-gpg (1.12.0-6) ...
Selecting previously unselected package samba-dsdb-modules:armhf.
Preparing to unpack .../19-samba-dsdb-modules_2%3a4.9.5+dfsg-5+deb10u1+rpi1_armhf.deb ...
Unpacking samba-dsdb-modules:armhf (2:4.9.5+dfsg-5+deb10u1+rpi1) ...
Selecting previously unselected package samba-vfs-modules:armhf.
Preparing to unpack .../20-samba-vfs-modules_2%3a4.9.5+dfsg-5+deb10u1+rpi1_armhf.deb ...
Unpacking samba-vfs-modules:armhf (2:4.9.5+dfsg-5+deb10u1+rpi1) ...
Setting up libibverbs1:armhf (22.1-1) ...
Setting up libboost-regex1.67.0:armhf (1.67.0-13) ...
Setting up ibverbs-providers:armhf (22.1-1) ...
Setting up attr (1:2.4.48-4) ...
Setting up samba-vfs-modules:armhf (2:4.9.5+dfsg-5+deb10u1+rpi1) ...
Setting up samba-common (2:4.9.5+dfsg-5+deb10u1+rpi1) ...

Creating config file /etc/samba/smb.conf with new version
Setting up libglusterfs0:armhf (5.5-3) ...
Setting up python-ldb (2:1.5.1+really1.4.6-3) ...
Setting up tdb-tools (1.3.16-2+b1) ...
update-alternatives: using /usr/bin/tdbbackup.tdbtools to provide /usr/bin/tdbbackup (tdbbackup) in auto mode
Setting up python-tdb (1.3.16-2+b1) ...
Setting up samba-dsdb-modules:armhf (2:4.9.5+dfsg-5+deb10u1+rpi1) ...
Setting up python-dnspython (1.16.0-1) ...
Setting up python-gpg (1.12.0-6) ...
Setting up libgfxdr0:armhf (5.5-3) ...
Setting up librados2:armhf (12.2.11+dfsg1-2.1+rpi1) ...
Setting up python-samba (2:4.9.5+dfsg-5+deb10u1+rpi1) ...
Setting up libcephfs2:armhf (12.2.11+dfsg1-2.1+rpi1) ...
Setting up samba-common-bin (2:4.9.5+dfsg-5+deb10u1+rpi1) ...
Checking smb.conf with testparm
Load smb config files from /etc/samba/smb.conf
Loaded services file OK.
Server role: ROLE_STANDALONE

Done
Setting up libgfrpc0:armhf (5.5-3) ...
Setting up samba (2:4.9.5+dfsg-5+deb10u1+rpi1) ...
Adding group `sambashare' (GID 116) ...
Done.
Samba is not being run as an AD Domain Controller: Masking samba-ad-dc.service
Please ignore the following error about deb-systemd-helper not finding those services.
(samba-ad-dc.service masked)
Created symlink /etc/systemd/system/multi-user.target.wants/nmbd.service → /lib/systemd/system/nmbd.service.
Failed to preset unit: Unit file /etc/systemd/system/samba-ad-dc.service is masked.
/usr/bin/deb-systemd-helper: error: systemctl preset failed on samba-ad-dc.service: No such file or directory
Created symlink /etc/systemd/system/multi-user.target.wants/smbd.service → /lib/systemd/system/smbd.service.
Setting up libgfapi0:armhf (5.5-3) ...
Processing triggers for systemd (241-7~deb10u2+rpi1) ...
Processing triggers for man-db (2.8.5-2) ...
Processing triggers for libc-bin (2.28-10+rpi1) ...
pi@rpi:~ $ 
```
</details>

安装过程中会弹框
![这里选是](https://i1.yuangezhizao.cn/Win-10/20200122185805.jpg!webp)

修改配置文件`sudo vim /etc/samba/smb.conf`如下
``` bash
#======================= Share Definitions =======================

[rpi]
   path = /tmp/cosfs
   comment = COSFS
   browseable = yes

# By default, the home directories are exported read-only. Change the
# next parameter to 'no' if you want to be able to write to them.
#   read only = no
   writeable = yes

# File creation mask is set to 0700 for security reasons. If you want to
# create files with group=rw permissions, set next parameter to 0775.
   create mask = 0700

# Directory creation mask is set to 0700 for security reasons. If you want to
# create dirs. with group=rw permissions, set next parameter to 0775.
   directory mask = 0700

# By default, \\server\username shares can be connected to by anyone
# with access to the samba server.
# The following parameter makes sure that only "username" can connect
# to \\server\username
# This might need tweaking when using external authentication schemes
   valid users = pi
   public = yes

```
添加`pi`用户
``` bash
pi@rpi:~ $ sudo smbpasswd -a pi
New SMB password:
Retype new SMB password:
Added user pi.
```
重启服务
```
sudo samba restart
```

### 3.远程访问
这里的构想是远程连接`rpi`的`SMB`，然后`SMB`指向的是`COS`，这样就不占用本地的任何空间了
结果并不能这么搞，草死（原因之后再调查`(╯°Д°)╯︵┻━┻`
没办法只能`/home/pi/Videos/Mi`
![选设备](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-22-20-43-48-689_com.xiaomi.sma.jpg!webp)
![选文件夹](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-22-20-44-07-472_com.xiaomi.sma.jpg!webp)
![同步设置](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-22-21-09-12-674_com.xiaomi.sma.jpg!webp)
![传输正常](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-22-22-58-56-173_com.xiaomi.sma.jpg!webp)

这里的显示有问题……亲测选择实时之后就会立即传输了（大概每次传输`7M`进行分割
然后更改设置之后，需要手动关闭再开启`视频存储`开关
![Windows 挂载](https://i1.yuangezhizao.cn/Win-10/20200122211129.jpg!webp)

因此，现在只能`cp -r xiaomi_camera_videos/ /tmp/cosfs/`之后清空视频文件了
![COS](https://i1.yuangezhizao.cn/Win-10/20200122213122.png!webp)

设置`1h`的频率然后写个脚本扔`cron`里就`ok`了
> 至此本文使命完成

![去 tm 的云存储 VIP](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-22-21-18-02-533_com.xiaomi.sma.jpg!webp)

## 0x03.后记
姿势不对，后期探索`ヽ(^_−)ﾉ`
初见竟然`2.5h`就写完了全文，「五星好评，下次还来」
`2020-3-31 21:27:16`：
去翻了下现在的文件夹列表
![5ce50c592cb6](https://i1.yuangezhizao.cn/Win-10/20200331212901.png!webp)

因为去年白嫖的资源包明天到期。。。
![200.00 GB](https://i1.yuangezhizao.cn/Win-10/20200331213606.jpg!webp)

其实也只用到了`163 GB`而已，而`rpi`就占了`55 GB`
![数据监控](https://i1.yuangezhizao.cn/Win-10/20200331213649.jpg!webp)
![存储桶数据概览](https://i1.yuangezhizao.cn/Win-10/20200331213757.jpg!webp)

于是去看看氪金的价格，**归档存储**倒是不贵
![产品定价](https://i1.yuangezhizao.cn/Win-10/20200331213450.jpg!webp)
![COS资源包](https://i1.yuangezhizao.cn/Win-10/20200331215954.jpg!webp)
![COS资源包](https://i1.yuangezhizao.cn/Win-10/20200331214520.jpg!webp)

然后去翻活动页面，氪了个`1`元`50 GB`的`6`个月时长的标准存储包（自然就没有买归档包
![好活动](https://i1.yuangezhizao.cn/Win-10/20200331215032.jpg!webp)
![还不错](https://i1.yuangezhizao.cn/Win-10/20200331214854.jpg!webp)
![1](https://i1.yuangezhizao.cn/Win-10/20200331214929.jpg!webp)
![50.00GB](https://i1.yuangezhizao.cn/Win-10/20200331215302.jpg!webp)
![25](https://i1.yuangezhizao.cn/Win-10/20200331221325.jpg!webp)

在加上之前的`50 GB`额度就正好凑足`100 GB`了，然后前天莫名提示`90%`？？？
![老用户福利](https://i1.yuangezhizao.cn/Win-10/20200331220448.jpg!webp)
![？](https://i1.yuangezhizao.cn/Win-10/20200331220705.jpg!webp)

于是现在的任务就变成了干掉`63.56 GB`……先从`81.15GB`的`video`存储桶下手吧，为什么是它呢？因为之前测试转存的时候屯了一个超多分`P`的`maimai`手元视频
屯完之后懒得管，不过现在是时候处理下了……
![刷屏草](https://i1.yuangezhizao.cn/Win-10/20200331221714.jpg!webp)
![前缀搜索](https://i1.yuangezhizao.cn/Win-10/20200331221819.png!webp)
![搞定](https://i1.yuangezhizao.cn/Win-10/20200331222705.jpg!webp)
