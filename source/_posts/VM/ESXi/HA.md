---
title: VMware ESXi 安装 Home Assistant
date: 2020-4-5 19:13:00
tags:
  - VM
  - VMware
  - ESXi
count: 1
os: 0
os_1: 10.0.17763.1098 2019-LTSC
browser: 0
browser_1: 78.0.3904.108 Stable
place: 新家
key: 81
---
    老早就听说过 HA 了，昨天突然看到相关文章
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
`CPU`：`2`（第一次运行时分的单核，这次分的双核，看起来是够用的
`内存`：`2G`（第一次运行时分的`1G`结果跑满，这次`2G`同样跑满草，倒是可以再加
![虚拟硬件](https://i1.yuangezhizao.cn/Win-10/20200405192929.jpg!webp)

`引导选项`、`固件`：`EFI`，**关闭**`启用 UEFI 安全引导`（否则无法启动
![虚拟机选项](https://i1.yuangezhizao.cn/Win-10/20200405193613.jpg!webp)

最后`打开电源`，然后等上较长的一段时间才会就绪，直接睡觉去了
![vms](https://i1.yuangezhizao.cn/Win-10/20200405191808.png!webp)

## 0x02.配置
进入[http://homeassistant:8123](http://homeassistant:8123)，虽然官方说的是[http://homeassistant.local:8123](http://homeassistant.local:8123)，当然官方之前用的是`hassio.local`
![创建账户](https://i1.yuangezhizao.cn/Win-10/20200405184439.jpg!webp)

然而这个`自动检测`并不是很准确的样子，于是人工标点
![定位](https://i1.yuangezhizao.cn/Win-10/20200405185126.jpg!webp)

这里暂时没有配置，跳过
![集成](https://i1.yuangezhizao.cn/Win-10/20200405185157.jpg!webp)

终于来到了控制面板的首页了，空空如也`2333`
![首页](https://i1.yuangezhizao.cn/Win-10/20200405185306.jpg!webp)

然后去看一眼附加组件，竟然有`VSC`好评
![store](https://i1.yuangezhizao.cn/Win-10/20200405190040.jpg!webp)

目前版本：`Home Assistant 0.107.7`
![信息](https://i1.yuangezhizao.cn/Win-10/20200405195453.jpg!webp)

## 0x03.[ESPHome](https://esphome.io/)
`Supervisor`的`ADD-ON STORE`中的`Repositories`添加：`https://github.com/esphome/hassio`

![Repositories](https://i1.yuangezhizao.cn/Win-10/20200405200000.jpg!webp)
![ESPHome Hass.io Add-Ons](https://i1.yuangezhizao.cn/Win-10/20200405200153.jpg!webp)

来创建个设备玩玩看吧
![必须小写草](https://i1.yuangezhizao.cn/Win-10/20200405201014.jpg!webp)
![NodeMCU](https://i1.yuangezhizao.cn/Win-10/20200405201252.jpg!webp)

提供`WiFi`信息，而且说明了只需要一次`USB`烧录固件，之后的升级均通过`OTA`，并可在此处指定升级密匙
![WiFi](https://i1.yuangezhizao.cn/Win-10/20200405201444.jpg!webp)

然后才想到，虚拟机里并不能开启热点草
![Done](https://i1.yuangezhizao.cn/Win-10/20200405201649.jpg!webp)

然后就炸了
![草](https://i1.yuangezhizao.cn/Win-10/20200405201811.jpg!webp)
![刷新页面之后好了](https://i1.yuangezhizao.cn/Win-10/20200405202034.jpg!webp)

`UPLOAD`编译固件，结果编译炸了
![Compile And Upload](https://i1.yuangezhizao.cn/Win-10/20200405202131.jpg!webp)
![+1s](https://i1.yuangezhizao.cn/Win-10/20200405202145.jpg!webp)

## 0x04.后记
这个`HA`可以看做是一个平台，不过具体要干什么就要靠你的想象力了

## 0x05.引用
[如何在ESXI中安装Home Assistant](https://web.archive.org/web/20200405114005/https://lijie.org/2019/10/12/install-homeassistant-on-esxi/)

未完待续……