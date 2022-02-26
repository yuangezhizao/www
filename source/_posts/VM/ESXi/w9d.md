---
title: VMware ESXi 安装 Microsoft Windows Server 2019（64 位）
date: 2020-4-4 13:46:56
tags:
  - VM
  - VMware
  - ESXi
count: 2
os: 0
os_1: 10.0.17763.1098 2019-LTSC
browser: 0
browser_0: 78.0.3904.108 Stable
place: 新家
key: 80
---
    自建机子巨爽啊
<!-- more -->
## 0x00.前言
此文章拆分自[VMware ESXi 7.0.0 服务器虚拟化](./init.html)

## 0x02.配置
![vms](https://i1.yuangezhizao.cn/Win-10/20200404135648.png!webp)

关机之后，`编辑设置`、`虚拟机选项`、`常规选项`、`客户机操作系统版本`是没有`19`的选项的
![客户机操作系统版本](https://i1.yuangezhizao.cn/Win-10/20200404140113.jpg!webp)

是因为需要提前进行升级操作
![升级虚拟机兼容性](https://i1.yuangezhizao.cn/Win-10/20200404140413.jpg!webp)
![ESXi 7.0 虚拟机](https://i1.yuangezhizao.cn/Win-10/20200404140434.jpg!webp)
![是](https://i1.yuangezhizao.cn/Win-10/20200404140526.jpg!webp)

然后就果然可以了
![2019](https://i1.yuangezhizao.cn/Win-10/20200404140726.jpg!webp)

还顺手把`VBS`开启了，然而好像这是针对于虚机的，所以应该并没有什么卵用（又不在虚机里再安虚机，禁止套娃）
![vSphere 6.7 新特性 — 基于虚拟化的安全 (VBS)](https://i1.yuangezhizao.cn/Win-10/20200404141911.jpg!webp)
![VBS](https://i1.yuangezhizao.cn/Win-10/20200404141509.jpg!webp)
![完工](https://i1.yuangezhizao.cn/Win-10/20200404142024.jpg!webp)

## 0x03.登录
`AD`域控登录大法
![logon](https://i1.yuangezhizao.cn/Win-10/20200404132729.jpg!webp)

`12C12G`爽到
![关于](https://i1.yuangezhizao.cn/Win-10/20200404133022.png!webp)
![系统信息](https://i1.yuangezhizao.cn/Win-10/20200404133413.jpg!webp)

~~先给自己分配了一个虚拟机`hhh`~~`2019-12-28 00:51:40`该机子由于存储在坏掉的硬盘无法成功完全导出，最终只能重装……
![vms](https://i1.yuangezhizao.cn/Win-10/20190728003657.png!webp)
![cn-py-dl-w9d](https://i1.yuangezhizao.cn/Win-10/20190728015602.png!webp)

## 0x04.对比
讲个笑话
![1080](https://i1.yuangezhizao.cn/Win-10/20200404150251.jpg!webp)

## 0x05.引用
[vSphere 6.7 新特性 — 基于虚拟化的安全 (VBS)](https://web.archive.org/web/20200404062111/https://blogs.vmware.com/china/2018/07/27/vsphere-6-7-%E6%96%B0%E7%89%B9%E6%80%A7-%E5%9F%BA%E4%BA%8E%E8%99%9A%E6%8B%9F%E5%8C%96%E7%9A%84%E5%AE%89%E5%85%A8-vbs/)

未完待续……