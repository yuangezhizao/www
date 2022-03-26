---
title: VMware vCenter 安装 RHEL 8
date: 2022-03-27 00:01:45
tags:
  - VM
  - VMware
  - vCenter
  - RHEL
count: 2
os: 1
os_1: Monterry 12.3 (21E230)
browser: 0
browser_0: 99.0.4844.84 Stable
place: 新家
key: 135
---
    cn-py-dl-a8 销毁，cn-py-dl-r8 真香
<!-- more -->
## 0x00.前言
上个月新安装的`AlmaLinux`一直没抽出时间来部署软件，昨晚看到`RHEL`红帽开发者个人订阅有`16`台的额度，立即尝鲜

## 0x01.安装
![下载](https://i1.yuangezhizao.cn/macOS/20220326232509.png!webp)
![rhel-8.5-x86_64-dvd.iso](https://i1.yuangezhizao.cn/macOS/20220327000926.png!webp)
![新建虚拟机](https://i1.yuangezhizao.cn/macOS/20220327001044.png!webp)
![创建新虚拟机](https://i1.yuangezhizao.cn/macOS/20220327001138.png!webp)
![cn-py-dl-r8](https://i1.yuangezhizao.cn/macOS/20220327001222.png!webp)
![PYDL](https://i1.yuangezhizao.cn/macOS/20220327001241.png!webp)
![4T@2022-2-22](https://i1.yuangezhizao.cn/macOS/20220327001828.png!webp)
![ESXi 7.0 U2](https://i1.yuangezhizao.cn/macOS/20220327001418.png!webp)
![RHEL 8](https://i1.yuangezhizao.cn/macOS/20220327001503.png!webp)
![ISO](https://i1.yuangezhizao.cn/macOS/20220327002026.png!webp)
![2C](https://i1.yuangezhizao.cn/macOS/20220327001616.png!webp)
![50G](https://i1.yuangezhizao.cn/macOS/20220327001925.png!webp)
![即将完成](https://i1.yuangezhizao.cn/macOS/20220327002149.png!webp)
![创建完成](https://i1.yuangezhizao.cn/macOS/20220327002240.png!webp)
![打开电源](https://i1.yuangezhizao.cn/macOS/20220327002619.png!webp)
![开机](https://i1.yuangezhizao.cn/macOS/20220327002730.png!webp)
![保持默认英文](https://i1.yuangezhizao.cn/macOS/20220327002829.png!webp)
![安装配置](https://i1.yuangezhizao.cn/macOS/20220327002902.png!webp)
![静态 IP](https://i1.yuangezhizao.cn/macOS/20220327003036.png!webp)
![PAC 代理](https://i1.yuangezhizao.cn/macOS/20220327003129.png!webp)
![联网](https://i1.yuangezhizao.cn/macOS/20220327003255.png!webp)
![NTP](https://i1.yuangezhizao.cn/macOS/20220327003433.png!webp)
![网络时间](https://i1.yuangezhizao.cn/macOS/20220327003527.png!webp)
![默认安装](https://i1.yuangezhizao.cn/macOS/20220327003725.png!webp)
![本地源](https://i1.yuangezhizao.cn/macOS/20220327003755.png!webp)
![默认硬盘](https://i1.yuangezhizao.cn/macOS/20220327003845.png!webp)
![KDUMP 160MB](https://i1.yuangezhizao.cn/macOS/20220327003919.png!webp)
![保持默认](https://i1.yuangezhizao.cn/macOS/20220327004006.png!webp)
![连接账户](https://i1.yuangezhizao.cn/macOS/20220327004145.png!webp)
![注册中](https://i1.yuangezhizao.cn/macOS/20220327004212.png!webp)
![附加订阅](https://i1.yuangezhizao.cn/macOS/20220327004217.png!webp)
![1/16](https://i1.yuangezhizao.cn/macOS/20220327004312.png!webp)
![然后就突然卡住草，部分选项还得重设](https://i1.yuangezhizao.cn/macOS/20220327004645.png!webp)
![配置密码](https://i1.yuangezhizao.cn/macOS/20220327005212.png!webp)
![不知道红帽 CDN 速度如何](https://i1.yuangezhizao.cn/macOS/20220327012045.png!webp)
![终于开始安装](https://i1.yuangezhizao.cn/macOS/20220327012258.png!webp)
![先睡觉去了，估计白天就完成了](https://i1.yuangezhizao.cn/macOS/20220327012425.png!webp)

## 0x02.红帽门户
![1/16](https://i1.yuangezhizao.cn/macOS/20220327005443.png!webp)
![虚拟系统](https://i1.yuangezhizao.cn/macOS/20220327005811.png!webp)

> 至此本文使命完成
