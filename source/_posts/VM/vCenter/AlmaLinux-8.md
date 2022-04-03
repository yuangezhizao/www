---
title: VMware vCenter 安装 AlmaLinux 8
date: 2022-02-20 15:44:18
tags:
  - VM
  - VMware
  - vCenter
  - AlmaLinux
count: 1
os: 1
os_1: Monterry 12.2.1 (21D62)
browser: 0
browser_1: 98.0.4758.102 Stable
place: 新家
key: 132
---
    因为端午节 cn-py-dl-c8 炸了，被迫折腾安装 cn-py-dl-a8
<!-- more -->
## 0x00.前言
毕竟`CentOS`已经停止支持，生产环境都迁移到[AlmaLinux OS](https://github.com/AlmaLinux/)上了，所以家里也不例外（<span title="你知道的太多了" class="heimu">继续白嫖</span>

## 0x01.安装
![官网](https://i1.yuangezhizao.cn/macOS/QQ20220220-153957@2x.png!webp)
![这里选择最小镜像](https://i1.yuangezhizao.cn/macOS/QQ20220220-154105@2x.png!webp)
![新建虚拟机](https://i1.yuangezhizao.cn/macOS/QQ20220220-160009@2x.png!webp)
![创建新虚拟机](https://i1.yuangezhizao.cn/macOS/QQ20220220-160050@2x.png!webp)
![cn-py-dl-a8](https://i1.yuangezhizao.cn/macOS/QQ20220220-160141@2x.png!webp)
![PYDL](https://i1.yuangezhizao.cn/macOS/QQ20220220-160157@2x.png!webp)
![2T@2021-4-18](https://i1.yuangezhizao.cn/macOS/QQ20220220-160213@2x.png!webp)
![ESXi 7.0 U2](https://i1.yuangezhizao.cn/macOS/QQ20220220-160301@2x.png!webp)
![CentOS 8](https://i1.yuangezhizao.cn/macOS/QQ20220220-160511@2x.png!webp)
![ISO](https://i1.yuangezhizao.cn/macOS/QQ20220220-161811@2x.png!webp)
![2C](https://i1.yuangezhizao.cn/macOS/QQ20220220-161843@2x.png!webp)
![50G](https://i1.yuangezhizao.cn/macOS/QQ20220220-161905@2x.png!webp)
![即将完成](https://i1.yuangezhizao.cn/macOS/QQ20220220-162024@2x.png!webp)
![创建完成](https://i1.yuangezhizao.cn/macOS/QQ20220220-162311@2x.png!webp)
![开机](https://i1.yuangezhizao.cn/macOS/QQ20220220-162454@2x.png!webp)
![保持默认英文](https://i1.yuangezhizao.cn/macOS/QQ20220220-162610@2x.png!webp)
![安装配置](https://i1.yuangezhizao.cn/macOS/QQ20220220-162741@2x.png!webp)
![静态 IP](https://i1.yuangezhizao.cn/macOS/QQ20220220-163206@2x.png!webp)
![PAC 代理](https://i1.yuangezhizao.cn/macOS/QQ20220220-163122@2x.png!webp)
![联网](https://i1.yuangezhizao.cn/macOS/QQ20220220-163402@2x.png!webp)
![NTP](https://i1.yuangezhizao.cn/macOS/QQ20220220-163610@2x.png!webp)
![网络时间](https://i1.yuangezhizao.cn/macOS/QQ20220220-163651@2x.png!webp)
![默认安装](https://i1.yuangezhizao.cn/macOS/QQ20220220-163757@2x.png!webp)
![不用输入网络源了](https://i1.yuangezhizao.cn/macOS/QQ20220220-163856@2x.png!webp)
![默认硬盘](https://i1.yuangezhizao.cn/macOS/QQ20220220-163913@2x.png!webp)
![配置密码](https://i1.yuangezhizao.cn/macOS/QQ20220220-163944@2x.png!webp)
![安装完成](https://i1.yuangezhizao.cn/macOS/QQ20220220-164450@2x.png!webp)
![重启](https://i1.yuangezhizao.cn/macOS/QQ20220220-164511@2x.png!webp)
![搞定](https://i1.yuangezhizao.cn/macOS/QQ20220220-164559@2x.png!webp)

> 至此本文使命完成
