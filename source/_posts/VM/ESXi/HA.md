---
title: VMware ESXi 安装 Home Assistant
date: 2020-4-5 19:13:00
tags:
  - VM
  - VMware
  - ESXi
  - Home Assistant
  - HA
count: 4
os: 0
os_1: 10.0.17763.1098 2019-LTSC
browser: 0
browser_0: 78.0.3904.108 Stable
place: 新家
key: 81
---
    老早就听说过 HA 了，昨天突然看到相关文章于是开搞
<!-- more -->
## 0x00.前言
既然出了`VMDK`适配给`VMWare Workstation`，那么`ESXi`就一定也可以
![VMDK](https://i1.yuangezhizao.cn/Win-10/20200405191835.jpg!webp)

## 0x01.[安装](https://web.archive.org/web/20200405112133/https://www.home-assistant.io/hassio/installation/)
![创建新虚拟机](https://i1.yuangezhizao.cn/Win-10/20200405192315.jpg!webp)

`兼容性`：`ESXi 7.0 虚拟机`
`客户机操作系统系列`：`Linux`
`客户机操作系统版本`：`其他 4.x 或更高版本的 Linux (64 位)`
![选择名称和客户机操作系统](https://i1.yuangezhizao.cn/Win-10/20200405194227.jpg!webp)

`自定义设置`，删除`硬盘 1`、`CD/DVD 驱动器 1`
`添加硬盘`、`现有硬盘`：包含`HassOS.vmdk`的文件夹`HassOS`，`IDE控制器0`，`主要`
`CPU`：`2`（第一次运行时分的单核，这次分的双核，看起来是够用的，最终分配单核节省资源
`内存`：`2G`（第一次运行时分的`1G`结果跑满，这次`2G`同样跑满草，最终分配`2G`保持不变
![虚拟硬件](https://i1.yuangezhizao.cn/Win-10/20200405192929.jpg!webp)

然后等给它分`4G`内存的时候，竟然只占用`1.85 GB`？？？
![4G](https://i1.yuangezhizao.cn/Win-10/20200406202926.jpg!webp)

`引导选项`、`固件`：`EFI`，**关闭**`启用 UEFI 安全引导`（否则无法启动
![虚拟机选项](https://i1.yuangezhizao.cn/Win-10/20200405193613.jpg!webp)

最后`打开电源`，然后等上较长的一段时间才会就绪，直接睡觉去了
![vms](https://i1.yuangezhizao.cn/Win-10/20200406204750.png!webp)

## 0x02.后记
这次其实是`VMDK`的下载花费了较长的时间
按照格式还是把文章拆分开了，具体的`Home Assistant`就挪到下篇文章再来介绍了

## 0x03.引用
[如何在ESXI中安装Home Assistant](https://web.archive.org/web/20200405114005/https://lijie.org/2019/10/12/install-homeassistant-on-esxi/)
[智能家居篇-3：ESP-01/01S 接入HomeAssistant，实现Siri控制](https://web.archive.org/web/20200614133438/https://codess.cc/archives/277.html)
[ESPHome入门指引（伪）](https://web.archive.org/web/20200614133443/https://ljr.im/articles/esphome-getting-started-guide-pseudo/)
[乐鑫ESP8266烧录固件、升级最新固件、刷MQTT固件](https://web.archive.org/web/20200614133452/http://www.piaoyi.org/iot/espressif-ESP8266-MQTT-AT.html)

> 至此本文使命完成
