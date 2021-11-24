---
title: Windows Server 2019 升级 2022
date: 2021-11-24 20:11:32
tags:
  - Windows
  - server
count: 1
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

4. 参照[密钥管理服务 (KMS) 客户端激活和产品密钥](https://docs.microsoft.com/zh-cn/windows-server/get-started/kms-client-activation-keys)，这里输入`Windows Server 2022 Datacenter`版本的产品密钥`WX4NM-KYWYW-QJJR4-XV3QB-6VM33`
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

未完待续……