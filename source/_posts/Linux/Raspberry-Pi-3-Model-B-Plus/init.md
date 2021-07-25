---
title: 树莓派 3B+ 初始化
date: 2021-03-11 23:22:23
tags:
  - RaspberryPi
count: 2
os: 1
os_1: Big Sur 11.2.3 (20D91)
browser: 1
browser_1: 89.0.4389.82 Stable
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
搬家之后`rpi-master`和`rpi-slave`均不再使用无线连接（分别是`5G`和`2.4G`的`WiFi`），全部以菊花插网线的方式上网
修改`/etc/dhcpcd.conf`，末尾追加
``` bash
# Example static IP configuration:

interface eth0
static routers=192.168.25.254
static domain_name_servers=192.168.25.246 192.168.25.238
static ip_address=192.168.25.129/24
static domain_search=
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

## 0x03.摄像头以[mjpeg](https://www.home-assistant.io/integrations/mjpeg/)方式接入`HomeAssistant`
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

## 0x02.后记
`2021-05-27 23:06:06`：这篇文章再不扔出来就要长毛了`2333`

## 0x04.引用
[树莓派设置静态 IP 地址](https://web.archive.org/web/20210725093638/https://www.jianshu.com/p/f9cb0f85a4e6)
[树莓派自带的网卡的带宽是多少](https://web.archive.org/web/20210725094423/https://www.icxbk.com/ask/detail/21847.html)

未完待续……