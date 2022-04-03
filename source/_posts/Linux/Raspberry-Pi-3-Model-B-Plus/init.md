---
title: 树莓派 3B+ 初始化
date: 2021-03-11 23:22:23
tags:
  - RaspberryPi
count: 4
os: 1
os_1: Big Sur 11.2.3 (20D91)
browser: 0
browser_0: 89.0.4389.82 Stable
place: 新家
key: 110
---
    似曾相识的标题 2333
<!-- more -->
## 0x00.前言
上次写还是`18`年的这篇文章：[树莓派 3B 初始化](../Raspberry-Pi-3-Model-B/init.html)，但是这次变成了`树莓派 3B+ 初始化`草

## 0x01.[Raspberry Pi Imager.app](https://www.raspberrypi.org/software/)烧录[镜像](https://www.raspberrypi.org/software/operating-systems/)

<details><summary>点击此处 ← 查看折叠</summary>

![v1.5](https://i1.yuangezhizao.cn/macOS/QQ20210306-150222@2x.png!webp)
![系统](https://i1.yuangezhizao.cn/macOS/QQ20210306-150410@2x.png!webp)
![存储卡](https://i1.yuangezhizao.cn/macOS/QQ20210306-150511@2x.png!webp)
![烧录](https://i1.yuangezhizao.cn/macOS/QQ20210306-150519@2x.png!webp)
![确认](https://i1.yuangezhizao.cn/macOS/QQ20210306-150528@2x.png!webp)
![验证](https://i1.yuangezhizao.cn/macOS/QQ20210306-151043@2x.png!webp)
![弹出](https://i1.yuangezhizao.cn/macOS/QQ20210306-151317@2x.png!webp)

</details>

创建空白`ssh`文件扔到`/boot`路径下
![ssh](https://i1.yuangezhizao.cn/macOS/QQ20210306-152131@2x.png!webp)

## 0x02.设置静态`IP`地址
搬家之后`rpi-master`和`rpi-slave`均不再使用无线连接（分别是`5G`和`2.4G`的`WiFi`），全部以菊花插网线的方式上网，因此需要修改`/etc/dhcpcd.conf`，末尾追加
``` bash
# Example static IP configuration:

interface enxb827ebe7f863
static routers=192.168.25.254
static domain_name_servers=192.168.25.246 240e:30f:1e76:7300:40b0:9b2d:4ad2:3f9d
inform 192.168.25.129/24
```
``` bash
# Example static IP configuration:

interface eth0
static routers=192.168.25.254
static domain_name_servers=192.168.25.246 192.168.25.238
static ip_address=192.168.25.130/24
static domain_search=
```
注：`eth0`代表`本地网卡`，`wlan0`代表`无线网卡`

## 0x03.下行带宽上限测试
先在`cn-py-dl-w2d`上开启服务端
``` bash
D:\iperf-3.1.3-win64>iperf3 -s
-----------------------------------------------------------
Server listening on 5201
-----------------------------------------------------------
```
`3B+`实测不到`300M`，有线连接
``` bash
pi@rpi-master:~ $ iperf3 -c 192.168.25.248
Connecting to host 192.168.25.248, port 5201
[  5] local 192.168.25.129 port 42604 connected to 192.168.25.248 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  33.8 MBytes   284 Mbits/sec    0    218 KBytes       
[  5]   1.00-2.00   sec  32.4 MBytes   272 Mbits/sec    0    218 KBytes       
[  5]   2.00-3.01   sec  33.2 MBytes   277 Mbits/sec    0    218 KBytes       
[  5]   3.01-4.00   sec  32.5 MBytes   274 Mbits/sec    0    218 KBytes       
[  5]   4.00-5.00   sec  32.7 MBytes   274 Mbits/sec    0    218 KBytes       
[  5]   5.00-6.00   sec  32.6 MBytes   273 Mbits/sec    0    218 KBytes       
[  5]   6.00-7.01   sec  33.0 MBytes   275 Mbits/sec    0    218 KBytes       
[  5]   7.01-8.00   sec  32.7 MBytes   274 Mbits/sec    0    218 KBytes       
[  5]   8.00-9.00   sec  32.4 MBytes   273 Mbits/sec    0    218 KBytes       
[  5]   9.00-10.00  sec  32.7 MBytes   274 Mbits/sec    0    218 KBytes       
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec   328 MBytes   275 Mbits/sec    0             sender
[  5]   0.00-10.00  sec   327 MBytes   274 Mbits/sec                  receiver

iperf Done.
```
而`3B`则实测不到`100M`，同样也是有线连接
``` bash
pi@rpi-slave:~ $ iperf3 -c 192.168.25.248
Connecting to host 192.168.25.248, port 5201
[  5] local 192.168.25.130 port 50936 connected to 192.168.25.248 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  11.8 MBytes  98.8 Mbits/sec    0   98.4 KBytes       
[  5]   1.00-2.00   sec  11.3 MBytes  94.6 Mbits/sec    0   98.4 KBytes       
[  5]   2.00-3.00   sec  11.3 MBytes  94.5 Mbits/sec    0   98.4 KBytes       
[  5]   3.00-4.00   sec  11.3 MBytes  95.1 Mbits/sec    0    103 KBytes       
[  5]   4.00-5.00   sec  11.3 MBytes  94.5 Mbits/sec    0    103 KBytes       
[  5]   5.00-6.00   sec  11.3 MBytes  94.6 Mbits/sec    0    103 KBytes       
[  5]   6.00-7.00   sec  11.5 MBytes  96.6 Mbits/sec    0    103 KBytes       
[  5]   7.00-8.00   sec  11.3 MBytes  94.6 Mbits/sec    0    103 KBytes       
[  5]   8.00-9.00   sec  11.2 MBytes  93.5 Mbits/sec    0    103 KBytes       
[  5]   9.00-10.00  sec  11.3 MBytes  94.5 Mbits/sec    0    103 KBytes       
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec   113 MBytes  95.1 Mbits/sec    0             sender
[  5]   0.00-10.00  sec   113 MBytes  94.8 Mbits/sec                  receiver

iperf Done.
```

## 0x04.摄像头以[mjpeg](https://www.home-assistant.io/integrations/mjpeg/)方式接入`HomeAssistant`
修改`configuration.yaml`
``` yaml
camera:
  - platform: mjpeg
    name: Raspberry Pi Camera Module v2
    still_image_url: https://www.raspberrypi.org/homepage-9df4b/static/621b26de7977c5b8d765b3003b341a49/8924f/68fe7e4cb53767ad6c033bf3b46da3452188a24a_pi-camera-front-1-1426x1080.jpg
    username: yuangezhizao
    password: <rm>
    mjpeg_url: http://192.168.25.129:8081
    authentication: basic
```

## 0x05.安装[SmokePing](https://oss.oetiker.ch/smokeping/)
参照[How to install SmokePing](https://web.archive.org/web/20210817144328/https://oss.oetiker.ch/smokeping/doc/smokeping_install.en.html)全部得编译安装，看完直接劝退完全折腾不动，还是算了吧，真的需要一键安装脚本……
然后谷歌看到树莓派上有编译好的包，于是立即从`cn-py-dl-c8`切换到`rpi-master`来安装了
后来发现也可以用`docker`：https://github.com/linuxserver/docker-smokeping
``` bash
pi@rpi-master:~ $ apt show smokeping
Package: smokeping
Version: 2.7.3-3
Priority: optional
Section: net
Maintainer: Gabriel Filion <gabriel@koumbit.org>
Installed-Size: 1,179 kB
Depends: perl:any, libwww-perl, libsnmp-session-perl (>= 0.86), librrds-perl (>= 1.2), liburi-perl, fping (>= 2.4b2-to-ipv6-2), libcgi-fast-perl, debianutils (>= 1.7), adduser, lsb-base (>= 3.0-6), libdigest-hmac-perl, ucf (>= 0.28), libconfig-grammar-perl, libjs-cropper, libjs-scriptaculous, libjs-prototype, default-mta | mail-transport-agent
Recommends: apache2 | httpd-cgi, libsocket6-perl, dnsutils, echoping, apache2 (>= 2.4.6-4~) | apache2 | httpd
Suggests: curl, libauthen-radius-perl, libnet-ldap-perl, libnet-dns-perl, openssh-client, libio-socket-ssl-perl, libnet-telnet-perl
Homepage: https://smokeping.org/
Tag: admin::logging, admin::monitoring, implemented-in::perl,
 interface::commandline, interface::daemon, interface::web,
 network::server, protocol::ipv6, protocol::snmp, role::program,
 scope::utility, use::monitor, use::scanning, web::cgi, works-with::db,
 works-with::image, works-with::image:vector, works-with::logfile
Download-Size: 495 kB
APT-Sources: http://raspbian.raspberrypi.org/raspbian bullseye/main armhf Packages
Description: latency logging and graphing system
 SmokePing consists of a daemon process which organizes the
 latency measurements and a CGI which presents the graphs.
 .
 With SmokePing you can measure latency and packet loss in your network.
 SmokePing uses RRDtool to maintain a longterm datastore and to draw pretty
 graphs giving up to the minute information on the state of each
 network connection.
```
开始安装
``` bash
pi@rpi-master:~ $ sudo apt install smokeping -y
pi@rpi-master:~ $ a2enmod cgi
Your MPM seems to be threaded. Selecting cgid instead of cgi.
Module cgid already enabled
```
修改配置文件

<details><summary>点击此处 ← 查看折叠</summary>

``` bash
pi@rpi-master:~ $ sudo vim /etc/smokeping/config.d/Probes
pi@rpi-master:~ $ cat /etc/smokeping/config.d/Probes
*** Probes ***

+ FPing

binary = /usr/bin/fping

+ DNS
binary = /usr/bin/dig
lookup = example.com
pings = 5
step = 180

+ Curl

binary = /usr/bin/curl
step = 60
urlformat = https://%host%/
pi@rpi-master:~ $ sudo vim /etc/smokeping/config.d/Targets
pi@rpi-master:~ $ sudo cp /etc/smokeping/config.d/Targets /etc/smokeping/config.d/Targets.bak
pi@rpi-master:~ $ ll /etc/smokeping/config.d/
total 36
-rw-r--r-- 1 root root 177 Jul 11  2020 Alerts
-rw-r--r-- 1 root root 237 Jul 11  2020 Database
-rw-r--r-- 1 root root 489 Jul 11  2020 General
-rw-r--r-- 1 root root 255 Jul 11  2020 pathnames
-rw-r--r-- 1 root root 909 Jul 11  2020 Presentation
-rw-r--r-- 1 root root 191 Jan  1 11:59 Probes
-rw-r--r-- 1 root root 147 Jul 11  2020 Slaves
-rw-r--r-- 1 root root 380 Jul 11  2020 Targets
-rw-r--r-- 1 root root 380 Jan  1 12:01 Targets.bak
pi@rpi-master:~ $ sudo vim /etc/smokeping/config.d/Targets
pi@rpi-master:~ $ cat /etc/smokeping/config.d/Targets
*** Targets ***

probe = FPing
menu  = Top
title = Network Latency Grapher

+ ICMP

probe = FPing
menu  = ICMP
title = ICMP

++ ICMP_lab

menu  = lab
title = lab.yuangezhizao.cn
host  = lab.yuangezhizao.cn

++ ICMP_txy

menu  = txy
title = txy.yuangezhizao.cn
host  = txy.yuangezhizao.cn

++ ICMP_proxy

menu  = proxy
title = proxy.yuangezhizao.cn
host  = proxy.yuangezhizao.cn

++ ICMP_proxy-cf

menu  = proxy-cf
title = proxy-cf.yuangezhizao.cn
host  = proxy-cf.yuangezhizao.cn

++ ICMP_proxy_v6

menu  = proxy_v6
title = proxyv6.yuangezhizao.cn
host  = proxyv6.yuangezhizao.cn

++ ICMP_GCP-JP

menu  = GCP-JP
title = 35.190.226.17
host  = 35.190.226.17

++ ICMP_GCP-TW

menu  = GCP-TW
title = 35.194.225.73
host  = 35.194.225.73

+ DNS

probe = DNS
menu  = DNS
title = DNS

++ Cloudflare_Teams_DNS

menu  = 172.64.36.1
title = 172.64.36.1
host  = 172.64.36.1

++ Cloudflare_DNS

menu  = 1.1.1.1
title = 1.1.1.1
host  = 1.1.1.1

++ Google_DNS

menu  = 8.8.8.8
title = 8.8.8.8
host  = 8.8.8.8

++ 219_149_6_99

menu  = 219.149.6.99
title = 219.149.6.99
host  = 219.149.6.99

++ 120_53_53_11

menu  = 120.53.53.11
title = 120.53.53.11
host  = 120.53.53.11

++ Cloudflare_Teams_DNS-v6

menu  = 2402:4e00:0::d2ad:6392
title = 2402:4e00:0::d2ad:6392
host  = 2402:4e00:0::d2ad:6392

++ 2a06_98c1_54__1802

menu  = 2a06:98c1:54::1802
title = 2a06:98c1:54::1802
host  = 2a06:98c1:54::1802

+ HTTP

probe = Curl
menu  = HTTP
title = HTTP

++ HTTP_www-vercel

menu  = yuangezhizao.vercel.app
title = yuangezhizao.vercel.app
host  = yuangezhizao.vercel.app

++ HTTP_www-cf

menu  = www-cf.yuangezhizao.cn
title = www-cf.yuangezhizao.cn
host  = www-cf.yuangezhizao.cn

++ HTTP_proxy

menu  = proxy
title = proxy.yuangezhizao.cn
host  = proxy.yuangezhizao.cn

++ HTTP_proxy-cf

menu  = proxy-cf
title = proxy-cf.yuangezhizao.cn
host  = proxy-cf.yuangezhizao.cn

++ HTTP_proxy_v6

menu  = proxy_v6
title = proxyv6.yuangezhizao.cn
host  = proxyv6.yuangezhizao.cn

++ HTTP_proxy_v6-cf

menu  = proxy_v6-cf
title = proxyv6-cf.yuangezhizao.cn
host  = proxyv6-cf.yuangezhizao.cn
```

</details>

最后重启
``` bash
pi@rpi-master:~ $ sudo service smokeping restart
pi@rpi-master:~ $ service smokeping status
● smokeping.service - Latency Logging and Graphing System
     Loaded: loaded (/lib/systemd/system/smokeping.service; enabled; vendor preset: enabled)
     Active: active (running) since Sat 2022-01-01 12:21:35 CST; 2s ago
       Docs: man:smokeping(1)
             file:/usr/share/doc/smokeping/examples/systemd/slave_mode.conf
    Process: 19356 ExecStart=/usr/sbin/smokeping --pid-dir=/run/smokeping (code=exited, status=0/SUCCE>
   Main PID: 19367 (smokeping)
      Tasks: 4 (limit: 948)
     Memory: 67.7M
        CPU: 2.833s
     CGroup: /system.slice/smokeping.service
             ├─19367 /usr/bin/perl /usr/sbin/smokeping --pid-dir=/run/smokeping
             ├─19368 /usr/sbin/smokeping [DNS]
             ├─19369 /usr/sbin/smokeping [FPing]
             └─19370 /usr/sbin/smokeping [Curl]

Jan 01 12:21:35 rpi-master smokeping[19356]: Daemonizing /usr/sbin/smokeping ...
Jan 01 12:21:31 rpi-master smokeping[19367]: Entering multiprocess mode.
Jan 01 12:21:31 rpi-master smokeping[19367]: Child process 19368 started for probe DNS.
Jan 01 12:21:31 rpi-master smokeping[19368]: DNS: probing 7 targets with step 180 s and offset 150 s.
Jan 01 12:21:31 rpi-master smokeping[19367]: Child process 19369 started for probe FPing.
Jan 01 12:21:31 rpi-master smokeping[19369]: FPing: probing 7 targets with step 300 s and offset 70 s.
Jan 01 12:21:35 rpi-master systemd[1]: Started Latency Logging and Graphing System.
Jan 01 12:21:31 rpi-master smokeping[19367]: Child process 19370 started for probe Curl.
Jan 01 12:21:31 rpi-master smokeping[19367]: All probe processes started successfully.
Jan 01 12:21:31 rpi-master smokeping[19370]: Curl: probing 6 targets with step 60 s and offset 29 s.
```

## 0x06.后记
`2021-05-27 23:06:06`：这篇文章再不扔出来就要长毛了`2333`

## 0x07.引用
[树莓派设置静态 IP 地址](https://web.archive.org/web/20210725093638/https://www.jianshu.com/p/f9cb0f85a4e6)
[树莓派自带的网卡的带宽是多少](https://web.archive.org/web/20210725094423/https://www.icxbk.com/ask/detail/21847.html)
[Raspberry Pi に Smokeping をインストールしてスループットをモニタする](https://web.archive.org/web/20220101035221/https://sig9.hatenablog.com/entry/2020/01/13/000000)

[How to Upgrade Raspberry Pi OS to the Latest Version?](https://raspberrytips.com/update-raspberry-pi-latest-version)
[Raspberry Pi OS upgraded to Debian 11 “Bullseye”](https://www.cnx-software.com/2021/11/08/raspberry-pi-os-upgraded-to-debian-11-bullseye)
[raspberrypi/picamera2](https://github.com/raspberrypi/picamera2/tree/main/examples/tensorflow)

未完待续……