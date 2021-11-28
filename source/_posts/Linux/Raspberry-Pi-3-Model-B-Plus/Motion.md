---
title: 树莓派基于 Motion 搭建监控系统
date: 2021-03-01 19:08:04
tags:
  - Motion
count: 2
os: 1
os_1: Big Sur 11.2.2 (20D80)
browser: 1
browser_1: 88.0.4324.192 Stable
place: 新家
key: 108
---
    假期结束了.jpG
<!-- more -->
## 0x00.前言
假期随手一翻理线包竟然找到了失恋多年的[Camera Module V2](https://www.raspberrypi.org/products/camera-module-v2/)，从`19`年到`21`年一直没有竟然还是好使的（
虽然这玩楞是`16`年首发的，但计划至少会发行至`24`年
想了一圈用途还是按照之前的套路安装`Motion`好了，至于其他的方案之后再进行探索吧`2333`

## 0x01.[Motion](https://github.com/Motion-Project/motion)
参照[官方文档](https://motion-project.github.io/)
### 1.安装
图省事安装预编译包：`sudo apt install motion`
### 2.配置
``` bash
sudo vim /etc/motion/motion.conf

daemon on
videodevice /dev/video0
width 640
height 480
framerate 60
ffmpeg_out_movies off
ffmpeg_video_codec flv
netcam_keepalive on
stream_maxrate 60
stream_localhost off
stream_auth_method 1
stream_authentication <rm>:<rm>
webcontrol_localhost off
webcontrol_authentication <rm>:<rm>
webcontrol_param 3
```
``` bash
sudo vim /etc/default/motion

start_motion_daemon=yes
```
### 3.运行
`sudo motion -m`~~，修改配置文件后需`sudo killall -SIGHUP motion`~~

## 0x01.后记
好耶，`Chrome`书签总数`-1`（`2`月份毕竟过年就没更新，三月份第一天这就恢复上了
码字码不动了，先这样吧……

## 0x16.引用
> [继续监控！使用树莓派+Motion实现实时视频监控并通过浏览器查看](https://web.archive.org/web/20210301111736/https://kenvix.com/post/rpi-monitor-2/)
[树莓派摄像头 + motion 实现视频监控系统](https://web.archive.org/web/20210301113652/https://bun.plus/posts/monitoring-with-raspberry-pi-and-motion)
