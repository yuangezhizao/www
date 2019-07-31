---
title: 基于 NodeMCU + DHT11 搭建物联网温湿度监控系统
date: 2019-7-31 21:41:34
tags:
  - NodeMCU
  - DHT11
count: 1
os: 0
os_1: 10.0.17763.652 2019-LTSC
browser: 0
browser_1: 74.0.3729.169 Stable
place: 新家
key: 54
---
    祭出 ESP8266 神器
<!-- more -->
## 0x00.前言
去翻从家带来的硬件小玩楞，突然发现`DHT11`，只可惜拿`DHN`的`STM32`连上并不是很好用，于是自己又网购了一波，顺便终于淘了个`8266`留给自己用。当初大三比赛用的是`51`+`DS18B20`再加`pc`的组合，后来比赛结束变成了加`rpi`的组合，结果到现在彻底换成了`NodeMCU`+`DHT11`的组合，`8266nb！`
![tb 并不是很贵的说](https://i1.yuangezhizao.cn/Win-10/20190731215649.jpg!webp)

这里说明一点，`NodeMCU`中的`Node`与我们所熟知的`Node.js`并没有关系，没想到吧`hhh`，骚年……
但是是基于`Lua`语言的（写到这里想到了貌似也有基于`Python`的开发板，`py`大法好！

## 0x01.[NodeMCU](http://www.nodemcu.com/index_cn.html)
> 超简单的物联网开发平台

一款开源快速硬件原型平台，包括固件和开发板，用几行简单的`Lua`脚本就能开发物联网应用
一、特点：
1. 像`Arduino`一样操作硬件`IO`
提供硬件的高级接口，可以将应用开发者从繁复的硬件配置、寄存器操作中解放出来。用交互式`Lua`脚本，像`arduino`一样编写硬件代码！
2. 用`Nodejs`类似语法写网络应用
事件驱动型`API`极大的方便了用户进行网络应用开发，使用类似`Nodejs`的方式编写网络代码，并运行于`5mm*5mm`大小的`MCU`之上，加快您的物联网开发进度。
3. 超低成本的`WI-FI`模块
用于快速原型的开发板，集成了售价低于`10`人民币`WIFI`芯片`ESP8266`。我们为您提供性价比最高的物联网应用开发平台。

二、开发板
1. 基于乐鑫`esp8266`的`NodeMcu`开发板，具有`GPIO`、`PWM`、`I2C`、`1-Wire`、`ADC`等功能，结合`NodeMcu`固件为您的原型开发提供最快速的途径。
2. 包含`usb`串口，即插即用
3. `10 GPIO`, 每个都能配置为`PWM`，`I2C`，`1-wire`
4. `FCC`认证的`WI-FI`模块，内置`PCB`天线

## 0x02.[官方文档](https://nodemcu.readthedocs.io/en/master/)
看到`Basics`里面的`Getting started`了吗？三部曲走起
> Getting Started aka NodeMCU Quick Start
The basic process to get started with NodeMCU consists of the following three steps.
1. Build the firmware with the modules you need
2. Flash the firmware to the chip
3. Upload code to the device.

#### 编译
上云：https://nodemcu-build.com/
云端定制固件，你值得拥有！
![要用谷歌邮箱，腾讯邮箱可不行](https://i1.yuangezhizao.cn/Win-10/20190731221604.jpg!webp)
![勾选模块，注意红框](https://i1.yuangezhizao.cn/Win-10/20190731221503.jpg!webp)

`DHT`和`HTTP`不是默认自带的，
![TLS 可以勾上](https://i1.yuangezhizao.cn/Win-10/20190731221846.jpg!webp)

#### 烧录
[NodeMCU PyFlasher](https://github.com/marcelstoer/nodemcu-pyflasher)：其实这玩楞就是个`esptool.py`的图形化封装
![Flash NodeMCU](https://i1.yuangezhizao.cn/Win-10/20190731222322.png!webp)

#### 连接
[ESPlorer](https://github.com/4refr0nt/ESPlorer)
`pc`需要`CH340`的驱动，这里是`COM18`，第一次连接可以按一下板子上的`RST`复位键，并且下载完成应该会提示`init.lua is not found`
我这里之前传过了所以不会有这个提示。现在懒得截图，之后再补吧……
![Communication](https://i1.yuangezhizao.cn/Win-10/20190731222651.jpg!webp)

未完待续……