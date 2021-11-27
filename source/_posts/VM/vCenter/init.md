---
title: VMware vCenter Server 7.0.0 安装
date: 2021-09-27 21:20:31
tags:
  - VM
  - VMware
  - vCenter
count: 2
os: 1
os_1: Monterry 12.0 Beta (21A5506j)
browser: 1
browser_1: 94.0.4606.61 Stable
place: 新家
key: 120
---
    鸽了半年的水（jie）文（tu）终于发出来了
<!-- more -->
## 0x00.前言
工作的时候发现大都在用`vCenter`，看到家里只安装了`ESXi`决定也搞一个好了

## 0x01.安装
> 多图预警

### 1. 第 1 阶段
![安装](https://i1.yuangezhizao.cn/Win-10/20210303123626.png!webp)
![下一步](https://i1.yuangezhizao.cn/Win-10/20210303123640.png!webp)
![下一步](https://i1.yuangezhizao.cn/Win-10/20210303123652.png!webp)
![微型](https://i1.yuangezhizao.cn/Win-10/20210303124747.png!webp)
![NASdata](https://i1.yuangezhizao.cn/Win-10/20210303124900.png!webp)
![192.168.25.230](https://i1.yuangezhizao.cn/Win-10/20210303125103.png!webp)
![完成](https://i1.yuangezhizao.cn/Win-10/20210303125121.png!webp)
![部署设备](https://i1.yuangezhizao.cn/Win-10/20210303125141.png!webp)
![继续](https://i1.yuangezhizao.cn/Win-10/20210303130407.png!webp)

### 2. 第 2 阶段
![下一步](https://i1.yuangezhizao.cn/Win-10/20210303130426.png!webp)
![设备配置](https://i1.yuangezhizao.cn/Win-10/20210303130523.png!webp)
![开启 SSH](https://i1.yuangezhizao.cn/Win-10/20210303130617.png!webp)
![这里搞错了，应该加入现有 SSO 域才对](https://i1.yuangezhizao.cn/Win-10/20210303130750.png!webp)
![CEIP 可以配置后续加入](https://i1.yuangezhizao.cn/Win-10/20210303130811.png!webp)
![完成](https://i1.yuangezhizao.cn/Win-10/20210303130832.png!webp)
![确定](https://i1.yuangezhizao.cn/Win-10/20210303130843.png!webp)
![完成](https://i1.yuangezhizao.cn/Win-10/20210303131141.png!webp)

## 0x02.后记
`45min`光速`xjb`写完草

> 至此本文使命完成
