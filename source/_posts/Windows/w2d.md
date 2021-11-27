---
title: Windows Server 2019 升级 2022
date: 2021-11-24 20:11:32
tags:
  - Windows
  - server
count: 3
os: 1
os_1: Monterry 12.0.1 (21A559)
browser: 1
browser_1: 96.0.4664.55 Stable
place: 新家
key: 125
---
    连 LTSC 2022 终于也出了
<!-- more -->
## 0x00.前言
升级前版本：`17763.2300`，是基于`1809`的`Windows Server 2019 数据中心版 64 位中文版`
![2019](https://i1.yuangezhizao.cn/macOS/20211124200537.png!webp)

虽然官方说可以从`2019`直升`2022`，无需全新安装，但保险起见还是打了个快照以防万一，`生成虚拟机内存快照`，即连带着内存一起打进去了
![223.53 GB](https://i1.yuangezhizao.cn/macOS/20211124201717.png!webp)

## 0x01.升级
1. 首先把`zh-cn_windows_server_2022_x64_dvd_6c73507d.iso`从`NAS`的下载路劲移动至虚拟机的本地磁盘，右键使用`Windows`自带的`装载`进行挂载操作
2. 然后进入新挂载出来的的文件里，双击`setup.exe`开始搞起
![装载](https://i1.yuangezhizao.cn/macOS/20211124200142.png!webp)

3. `更改安装程序下载更新的方式`，选择`不是现在`，以加快安装速度
![更改安装程序下载更新的方式](https://i1.yuangezhizao.cn/macOS/20211124200153.png!webp)
![不是现在](https://i1.yuangezhizao.cn/macOS/20211124200210.png!webp)

4. 参照[密钥管理服务 (KMS) 客户端激活和产品密钥](https://web.archive.org/web/20211125025910/https://docs.microsoft.com/zh-cn/windows-server/get-started/kms-client-activation-keys)，这里输入`Windows Server 2022 Datacenter`版本的产品密钥`WX4NM-KYWYW-QJJR4-XV3QB-6VM33`
如果想要`Windows Server 2022 Standard`版本则输入`VDYBN-27WPP-V4HQT-9VMD4-VMK7H`
![WX4NM-KYWYW-QJJR4-XV3QB-6VM33](https://i1.yuangezhizao.cn/macOS/20211124200322.png!webp)

5. 选择包含`Desktop Experience`的操作系统，毕竟这`tm`是`Windows`系统啊淦，没有界面那还不如装`Linux`了草
![Desktop Experience](https://i1.yuangezhizao.cn/macOS/20211124200338.png!webp)

6. 接受许可，保留全部内容
![莫得选择](https://i1.yuangezhizao.cn/macOS/20211124200349.png!webp)

7. 开始安装
![安装](https://i1.yuangezhizao.cn/macOS/20211124200655.png!webp)

众所周知此时的蓝色背景只是全屏了而已，仍然可以在应用间切换，因为还没有重启，所以暂时还不会影响正在运行的服务
![Desktop Experience](https://i1.yuangezhizao.cn/macOS/20211124202738.png!webp)

机械硬盘等了`20min`突然开始重启，于是去`ESXi`看后续
![安装](https://i1.yuangezhizao.cn/macOS/20211124205137.png!webp)

然后就一直等到了`23:40`，也就是接近`3h`草……终于下一次重启转圈圈了
![安装](https://i1.yuangezhizao.cn/macOS/20211124233946.png!webp)

8. 等到了第二天上午，睡醒后终于更新完成了，远程桌面登录发现黑屏草，召唤任务管理器运行`explorer.exe`就可以显示桌面了，不知道是不是为了节省资源来这么设计的
然后`v2rayN`打不开了草，等了好久终于不再是`无响应`了

![无响应](https://i1.yuangezhizao.cn/macOS/20211125104722.png!webp)

9. 升级后版本：`20348.169`，是基于`21H2`的`Windows Server 2022 数据中心版 64 位中文版`
![21H2](https://i1.yuangezhizao.cn/macOS/20211125105254.png!webp)

## 0X02.后记
~~没重启直接登录后感觉变卡了，反向升级？~~不过内存占用似乎变少了
`2021-11-27 19:37:12`：早上起来发现家里内网`PAC`访问不了了，一看`cn-py-dl-w2d`的远程桌面也连不上，于是赶紧登录到`ESXi`上去看看是怎么回事
![硬盘告急](https://i1.yuangezhizao.cn/macOS/20211127103416.png!webp)

开幕雷击，原来是硬盘满了……还是在`VC`上操作吧，当然开幕还是同样的提示语
![+1](https://i1.yuangezhizao.cn/macOS/20211127103945.png!webp)

去看了存储占用又想到在升级之前打了一个快照，果断删除之后终于可以登录了，其实之前虚拟机的状态相当于`挂起`，因此恢复之后各种服务的状态也都保持着
![删除全部快照](https://i1.yuangezhizao.cn/macOS/20211127103810.png!webp)


## 0x03.引用
[远程进入服务器界面黑屏如何处理](https://web.archive.org/web/20211125025713/https://social.technet.microsoft.com/Forums/msonline/fr-FR/8ac9305c-f89b-4843-88fd-1ed5c53fb0a4/36828312433682720837263812115322120300283875440657236312291420)

> 至此本文使命完成
