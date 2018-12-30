---
title: 树莓派 3B 初始化
date: 2018-3-6 19:03:35
tags:
  - Raspberry-pi
count: 2
os: 0
os_1: 10.0.14393 2016-LTSB
browser: 0
browser_1: 64.0.3282.140 Stable
place: 宿舍
key: 34
---
    寒假剁手买了板子，每天都在折腾中……
<!-- more -->
## 0x00.前言
> 成文时间仓促也不想细写，所以**不适合**无基础人士阅读！（请善用`Gitment`评论区

## 0x01.`Etcher`烧录[镜像](https://www.raspberrypi.org/downloads/raspbian/)
> 版本：RASPBIAN STRETCH WITH DESKTOP，2018-03-13-raspbian-stretch.img

升级系统虽然`sudo apt-get update`，`sudo apt-get dist-upgrade`这两步就能解决，~~然而我是后看到的~~但是如果以前没安装某软件，就不能在更新中下载到它。所以还是重新烧录了最新版本的镜像。烧录完成创建一个可以是空的`ssh`文件放在`/boot`分区下以开启`ssh`服务（我没有显示器但是有网线）。所以，要记得插根网线。

## 0x02.善于使用`raspi-config`
以`sudo`权限运行
![你并不会看到这个图形化界面](https://i1.yuangezhizao.cn/Win-10/20180316232443.jpg!webp)

不全说了，只挑几个。`5`里的`VNC`就是`RealVNC`的，打开之后才能用`VNC`图形化连接，进去先连个`WiFi`，毕竟不是什么时候都有网线支持的，`7`中`A3 Memory Split`调到`256`，`A7 GL Griver`我选的第二项`G2 GL（Fake KMS）`，第一项`VNC`分辨率一直保持默认的小窗口，更改不生效，窗口文字渲染部分会加重，感觉是个`Bug`。
![在这里也可以进](https://i1.yuangezhizao.cn/Win-10/20180317004332.jpg!webp)

## 0x03.更换阿里源
修改`/etc/apt/sources.list`
```
#科大源
deb http://mirrors.ustc.edu.cn/raspbian/raspbian/ jessie main contrib non-free rpi
```
修改`/etc/apt/sources.list.d/raspi.list`
```
#科大源
deb http://mirrors.ustc.edu.cn/archive.raspberrypi.org/debian/ jessie main ui
```
更新软件索引清单：`sudo apt-get update`
比较索引清单更新依赖关系：`sudo apt-get upgrade -y`

## 0x04.更换`pip`源
编辑`/.pip/pip.conf`，内容为
```
[global]
trusted-host = mirrors.aliyun.com
index-url = http://mirrors.aliyun.com/pypi/simple
```

## 0x05.修改交换分区大小
因为默认`100M`编译`FFmpeg`会不够用，分他个`500M`应该够了，当然`2G`是最好的了……
先看一眼，`free -h`
`sudo vi /etc/dphys-swapfile`
修改`CONF_SWAPSIZE`即可。
`sudo /etc/init.d/dphys-swapfile restart`
再看一眼，`free -h`

## 0x06.挂载 NTFS 硬盘支持读写
`sudo apt-get install ntfs-3g`

## 0x07.安装`Aria2`以备远程下载
安装：`sudo apt-get install aria2`
创建配置文件夹：`sudo mkdir /etc/aria2`
创建`session`和配置文件：`sudo touch /etc/aria2/aria2.session`，`sudo touch /etc/aria2/aria2.conf`
修改配置文件`sudo vim /etc/aria2/aria2.conf`：
```shell
## 文件保存相关 ##

# 文件保存目录
dir=/media/pi/Swap
# 启用磁盘缓存, 0为禁用缓存, 需1.16以上版本, 默认:16M
disk-cache=32M
# 断点续传
continue=true
#同服务器连接数
max-connection-per-server=1

# 文件预分配方式, 能有效降低磁盘碎片, 默认:prealloc
# 预分配所需时间: none < falloc ? trunc < prealloc
# falloc和trunc则需要文件系统和内核支持
# NTFS建议使用falloc, EXT3/4建议trunc, MAC 下需要注释此项
file-allocation=prealloc
check-certificate=false

## 下载连接相关 ##

# 最大同时下载任务数, 运行时可修改, 默认:5
max-concurrent-downloads=5
# 同一服务器连接数, 添加时可指定, 默认:1
max-connection-per-server=1
# 整体下载速度限制, 运行时可修改, 默认:0（不限制）
max-overall-download-limit=0
# 单个任务下载速度限制, 默认:0（不限制）
max-download-limit=0
# 整体上传速度限制, 运行时可修改, 默认:0（不限制）
max-overall-upload-limit=0
# 单个任务上传速度限制, 默认:0（不限制）
max-upload-limit=0
# 禁用IPv6, 默认:false
disable-ipv6=true

# 最小文件分片大小, 添加时可指定, 取值范围1M -1024M, 默认:20M
# 假定size=10M, 文件为20MiB 则使用两个来源下载; 文件为15MiB 则使用一个来源下载
min-split-size=10M
# 单个任务最大线程数, 添加时可指定, 默认:5
split=5

## 进度保存相关 ##

# 从会话文件中读取下载任务
input-file=/etc/aria2/aria2.session
# 在Aria2退出时保存错误的、未完成的下载任务到会话文件
save-session=/etc/aria2/aria2.session
# 定时保存会话, 0为退出时才保存, 需1.16.1以上版本, 默认:0
save-session-interval=60

## RPC相关设置 ##

# 启用RPC, 默认:false
enable-rpc=true
# 允许所有来源, 默认:false
rpc-allow-origin-all=true
# 允许外部访问, 默认:false
rpc-listen-all=true
# RPC端口, 仅当默认端口被占用时修改
# rpc-listen-port=6800
# 设置的RPC授权令牌, v1.18.4新增功能, 取代 --rpc-user 和 --rpc-passwd 选项
rpc-secret=pandownload

## BT/PT下载相关 ##

# 当下载的是一个种子(以.torrent结尾)时, 自动开始BT任务, 默认:true
#follow-torrent=true
# 客户端伪装, PT需要
peer-id-prefix=-TR2770-
user-agent=Transmission/2.77
# 强制保存会话, 即使任务已经完成, 默认:false
# 较新的版本开启后会在任务完成后依然保留.aria2文件
#force-save=false
# 继续之前的BT任务时, 无需再次校验, 默认:false
bt-seed-unverified=true
# 保存磁力链接元数据为种子文件(.torrent文件), 默认:false
bt-save-metadata=true
```
后台运行：`aria2c --conf-path=/etc/aria2/aria2.conf -D`
添加开机自启：`touch /etc/init.d/aria2c`
```sh
#!/bin/sh
### BEGIN INIT INFO
# Provides: aria2c
# Required-Start:    $network $local_fs $remote_fs
# Required-Stop:     $network $local_fs $remote_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: aria2c RPC init script.
# Description: Starts and stops aria2 RPC services.
### END INIT INFO

USER=root
RETVAL=0

case "$1" in  
    start)  
        echo "Starting service Aria2..."
        aria2c --conf-path=/etc/aria2/aria2.conf -D
        echo "Start service done."  
    ;;  
    stop)  
        echo "Stoping service Aria2..."  
        killall aria2c   
        echo "Stop service done."  
    ;;  
esac  
  
exit $RETVAL
```
赋予可执行权限：`chmod +x /etc/init.d/aria2c`
添加`/etc/init.d/aria2c start`到`/etc/rc.local`的`exit 0`之前
~~`apt-get -y install chkconfig`，`chkconfig --add aria2c`~~

## 0x08.安装`Nginx`
源于习惯本来想用`Apache`的，但是翻了翻感觉还是换个轻量级的较好，于是换成`Nginx`了。可以在上面放`webui-aria2`这种纯静态页面，但是后来被我移到腾讯云的`Apache`上了……（看到某人说的也就能支撑`100`用户在线……
`sudo apt-get -y install nginx`
`rm -rf /var/www/html`
`git clone https://github.com/ziahamza/webui-aria2.git /var/www/html`
`/etc/init.d/nginx start`
~~开机自启：编辑`/etc/rc.local`添加`/etc/init.d/nginx start`~~

## 0x09.手动编译支持硬解的[FFmpeg](http://ffmpeg.org/)
参考[引用第三条](#引用)
上个版本系统可以编译出`ffplay`、`ffprobe`、`ffserver`。但是最新版本的系统编译`ffplay`的依赖处理关系又问题，暂时先搁置一段时间

## 0x10.`GPIO`驱动`JLX12864G-086-PC`
这显示屏原本是`51`单片机课设所用，官方有驱动文件，所以就移（复）植（制）过来了，后续还会单独发相关内容，所以就简单写了。
我只用到了`wiringPiSetup()`、`pinMode`、`digitalWrite`和`digitalRead`这四个库函数。
编译：`gcc -Wall -o 12864g-86-pc.c 12864g-86-pc -lwiringPi`
运行：`sudo ./test`（控制`GPIO`需要用到`sudo`权限）
在这里叙述个开机执行二进制内容的方法：
1.制作`sh`脚本，同级目录创建`start.sh`，内容（按需更改）：
```shell
#!/bin/sh
cd 路径
sudo ./12864g-86-pc
```
2.修改`start.sh`权限：
`sudo chmod 777 start.sh`

3.向`rc.local`添加我们制作的这个脚本，用于开机启动：
`sudo vim /etc/rc.local`
在`exit 0`之前添加如下内容：`路径/start.sh start`

## 0x11.播放音频杂音问题
最新版本镜像该问题已不存在，参考[引用第十条](#引用)
`sudo vim /boot/config.txt`
`audio_pwm_mode = 2`
重启生效，在之前的镜像中改变还是很明显的。


## 0x12.【暂不推荐】安装`Docker`
```shell
pi@raspberrypi:~/Downloads $ curl -fsSL get.docker.com -o get-docker.sh
pi@raspberrypi:~/Downloads $ ls
get-docker.sh
pi@raspberrypi:~/Downloads $ sudo sh get-docker.sh
# Executing docker install script, commit: fc04d2c
+ sh -c apt-get update -qq >/dev/null
+ sh -c apt-get install -y -qq apt-transport-https ca-certificates curl >/dev/null
+ sh -c curl -fsSL "https://download.docker.com/linux/raspbian/gpg" | apt-key add -qq - >/dev/null
Warning: apt-key output should not be parsed (stdout is not a terminal)
+ sh -c echo "deb [arch=armhf] https://download.docker.com/linux/raspbian stretch edge" > /etc/apt/sources.list.d/docker.list
+ [ raspbian = debian ]
+ sh -c apt-get update -qq >/dev/null
+ sh -c apt-get install -y -qq --no-install-recommends docker-ce >/dev/null
+ sh -c docker version
Client:
 Version:	18.02.0-ce
 API version:	1.36
 Go version:	go1.9.3
 Git commit:	fc4de44
 Built:	Wed Feb  7 21:24:08 2018
 OS/Arch:	linux/arm
 Experimental:	false
 Orchestrator:	swarm

Server:
 Engine:
  Version:	18.02.0-ce
  API version:	1.36 (minimum version 1.12)
  Go version:	go1.9.3
  Git commit:	fc4de44~
  Built:	Wed Feb  7 21:20:13 2018
  OS/Arch:	linux/arm
  Experimental:	false
If you would like to use Docker as a non-root user, you should now consider
adding your user to the "docker" group with something like:

  sudo usermod -aG docker your-user

Remember that you will have to log out and back in for this to take effect!

WARNING: Adding a user to the "docker" group will grant the ability to run
         containers which can be used to obtain root privileges on the
         docker host.
         Refer to https://docs.docker.com/engine/security/security/#docker-daemon-attack-surface
         for more information.
pi@raspberrypi:~/Downloads $ sudo usermod -aG docker pi
pi@raspberrypi:~/Downloads $ docker search raspbian
Warning: failed to get default registry endpoint from daemon (Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get http://%2Fvar%2Frun%2Fdocker.sock/v1.36/info: dial unix /var/run/docker.sock: connect: permission denied). Using system default: https://index.docker.io/v1/
Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get http://%2Fvar%2Frun%2Fdocker.sock/v1.36/images/search?limit=25&term=raspbian: dial unix /var/run/docker.sock: connect: permission denied
```
## 引用
> [树莓派3B新版raspbian系统换国内源](http://www.cnblogs.com/wangchuanyang/p/6434323.html)
> [修改树莓派交换分区 SWAP 的正确姿势](http://shumeipai.nxez.com/2017/12/18/how-to-modify-raspberry-pi-swap-partition.html)
> [玩转树莓派02——搭建下载机](https://www.jianshu.com/p/4cf37177fc62)
> [树莓派驱动的b站直播弹幕点播台](https://github.com/chenxuuu/24h-raspberry-live-on-bilibili)
> [ffmpeg源码编译安装（Compile ffmpeg with source） Part 2 ： 扩展安装](http://www.cnblogs.com/yaoz/p/6944942.html)
> [树莓派编译安装FFmpeg(添加H.264硬件编解码器支持)](http://blog.csdn.net/sbdx/article/details/75110126)
> [树莓派 GPIO 控制](http://wiki.jikexueyuan.com/project/raspberry-pi/gpio.html)
> [树莓派开机自动运行某程序.md](http://blog.csdn.net/qq_17242837/article/details/53931738)
> [【教程】树莓派程序开机自启动方法总结](https://www.jianshu.com/p/86adb6d5347b)
> [树莓派音频口底噪太大的解决办法](http://blog.csdn.net/SmallSquare/article/details/79506097)

> [树莓派 b 站直播相关](https://www.chenxublog.com/)


> [三步在树莓派上部署nginx+uWSGI+flask](https://www.jianshu.com/p/14123b6b74c0)


> [Raspbian镜像使用帮助](https://lug.ustc.edu.cn/wiki/mirrors/help/raspbian)


https://github.com/markondej/fm_transmitter
