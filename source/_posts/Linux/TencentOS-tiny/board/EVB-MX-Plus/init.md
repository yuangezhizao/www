---
title: 腾讯 TencentOS tiny 官方定制 IoT 开发板 EVB_MX_Plus
date: 2020-1-18 14:42:35
tags:
  - TencentOS-tiny
  - EVB_MX_Plus
  - STM32L4
count: 1
os: 0
os_1: 10.0.17763.973 2019-LTSC
browser: 0
browser_1: 74.0.3729.169 Stable
place: 新家
key: 69
---
    顺丰空运，终于到手
    写完发现这文章也太水了，全是图草（
<!-- more -->
## 0x00.前言
前一阵子[云 + 社区](https://cloud.tencent.com/developer)发布了[比赛公告](https://web.archive.org/web/20200118065621/https://cloud.tencent.com/developer/article/1562607)`!!!∑(ﾟДﾟノ)ノ`
![开发板免费领！](https://i1.yuangezhizao.cn/Win-10/20200118145153.jpg!webp)

于是就填好了表单等待[入围名单公布！腾讯云IoT应用创新大赛火爆进行中！](https://web.archive.org/web/20200118071548/https://mp.weixin.qq.com/s/tmTsMzXBZlxZWROxyLzlwA)，最终有`330`名用户入选（包括本人`(｡･ω･｡)`

> 1. 腾讯`TencentOS tiny`官方定制`IoT`开发板`EVB_MX`
基于`STM32L4`低功耗主控，支持`WiFi`、`NB-IoT`、`2G`、`LoRaWAN`等多种通信方式扩展，同时支持`E53`传感器扩展，可应用于多场景`IoT`方案验证![1](https://i1.yuangezhizao.cn/Win-10/xshm1wvc4m.png!webp)
2. 腾讯`TencentOS tiny`官方定制`IoT`开发板`EVB_LX`
由兆易创新`（GD32）`赞助，业界首款基于`RISC-V`的`IoT`开发板，可支持`WiFi`、`NB-IoT`、`2G`、`LoRaWAN`等多种通信方式扩展，同时支持`E53`传感器扩展，可应用于多场景`IoT`方案验证![2](https://i1.yuangezhizao.cn/Win-10/n88n26papf.png!webp)
3. `P-NUCLEO-LRWAN3`开发套件
由意法半导体赞助，包含`LoRaWAN`节点和网关，节点集成多种传感器，可帮助开发者熟悉`LoRaWAN`网络，学习如何将`LoRaWAN`应用到自己的产品中![3](https://i1.yuangezhizao.cn/Win-10/01hk6wdb11.png!webp)
4. `RAK`室内网关
由深圳瑞科慧联赞助，高性能成品室内`LoRaWAN`网关，支持`8`信道的上行数据接收能力。![1](https://i1.yuangezhizao.cn/Win-10/yplplb83ai.png!webp)

## 0x01.收货
这里自己选择的是`1`，毕竟只熟悉`32`，后来在`wx`群中才陆续了解到`2`的`RISC-V`芯片以及`3`是价值`$99`的原厂板`Σ(っ°Д°;)っ`
最后发货到手发现`1`的配件还是比较多的`(｀・ω・´)`
![发货清单](https://i1.yuangezhizao.cn/Win-10/20200115211506.png!webp)
![还有 Lora 模组](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-16-23-24-13-927_com.tencent.mm.jpg!webp)
![顺丰好评](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20200116_231635.jpg!webp)
![空运巨快](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20200118_130306.jpg!webp)
![配送巨慢](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20200118_130243.jpg!webp)
![果然南山](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20200118_124942.jpg!webp)
![开箱](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20200118_125058.jpg!view)
![配件](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20200118_125742.jpg!view)
![上电](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20200118_130011.jpg!view)

## 0x02.[Keil](https://www.keil.com/download/product/)
![版本对比](https://i1.yuangezhizao.cn/Win-10/20200118161815.jpg!webp)
![MDK-Arm](https://i1.yuangezhizao.cn/Win-10/20200118155449.jpg!webp)
![MDK529.EXE](https://i1.yuangezhizao.cn/Win-10/20200118155854.jpg!webp)
![果断取消](https://i1.yuangezhizao.cn/Win-10/20200118160031.jpg!webp)
![代理启动！](https://i1.yuangezhizao.cn/Win-10/20200118160857.jpg!webp)

官网：http://www.keil.com/fid/13wqr0wyie9j1wprs3w11xsq6mxyr1a99ijw11/files/eval/mdk529.exe
~~CloudFlare：https://v2.yuangezhizao.cn/dl/mdk529.exe~~
~~Skysilk：http://proxy.yuangezhizao.cn/dl/mdk529.exe~~

![安装](https://i1.yuangezhizao.cn/Win-10/20200118161335.jpg!webp)
![这里取消勾选备份](https://i1.yuangezhizao.cn/Win-10/20200118161414.jpg!webp)
![安装完成会自动运行包管理](https://i1.yuangezhizao.cn/Win-10/20200118161943.jpg!webp)
![STM32L431RCTx，完全下不动](https://i1.yuangezhizao.cn/Win-10/20200118162324.jpg!webp)

[STMicroelectronics STM32L431RCTx](https://www.keil.com/dd2/stmicroelectronics/stm32l431rctx/)
![于是去官网下载](https://i1.yuangezhizao.cn/Win-10/20200118162644.jpg!webp)
![芯片信息](https://i1.yuangezhizao.cn/Win-10/20200118171146.jpg!webp)

官网：https://keilpack.azureedge.net/pack/Keil.STM32L4xx_DFP.2.3.0.pack
~~CloudFlare：https://v2.yuangezhizao.cn/dl/Keil.STM32L4xx_DFP.2.3.0.pack~~
~~Skysilk：http://proxy.yuangezhizao.cn/dl/Keil.STM32L4xx_DFP.2.3.0.pack~~
![运行 .pack 文件导入支持包](https://i1.yuangezhizao.cn/Win-10/20200118164029.jpg!webp)

## 0x03.[ST-LINK](https://jsproxy.yuangezhizao.workers.dev/-----https://www.st.com/content/st_com/zh/products/development-tools/software-development-tools/stm32-software-development-tools/stm32-utilities/stsw-link009.html)
![下载](https://i1.yuangezhizao.cn/Win-10/20200118170906.jpg!webp)
![dpinst_amd64.exe](https://i1.yuangezhizao.cn/Win-10/20200118171709.jpg!webp)
![安装](https://i1.yuangezhizao.cn/Win-10/20200118171636.jpg!webp)

## 0x04.[串口调试助手](https://web.archive.org/web/20200118092643/http://www.daxia.com/ss.htm)
下载[sscom5.13.1](http://www.daxia.com/download/sscom.rar)解压即用
![安装](https://i1.yuangezhizao.cn/Win-10/20200118172451.jpg!webp)

## 0x05.[TencentOS-tiny](https://github.com/Tencent/TencentOS-tiny)
https://github.com/Tencent/TencentOS-tiny/tree/master/board/TencentOS_tiny_EVB_MX_Plus
![只需要这一个文件夹](https://i1.yuangezhizao.cn/Win-10/20200118173748.jpg!webp)
![KEIL](https://i1.yuangezhizao.cn/Win-10/20200118211950.jpg!webp)
![于是采用部分下载法](https://i1.yuangezhizao.cn/Win-10/20200118173652.jpg!webp)

结果`api`请求超出限制直接`403`，于是拿代理下载`(*･ω< ) `
![机子磁盘空间不足](https://i1.yuangezhizao.cn/Win-10/20200118174538.jpg!webp)
![把之前的安装包删了](https://i1.yuangezhizao.cn/Win-10/20200118175200.jpg!webp)
![速度爽爆](https://i1.yuangezhizao.cn/Win-10/20200118175340.jpg!webp)

## 0x06.后记
然后就开始动手下载探索了，于是并没有时间来码字（
结果持续`Debug`到现在基本看出问题来了，就是例程与平台对不上，不仅限于数据格式，比如平台是`enum`而例程为`int`，平台是`int`而例程是`float`……
除夕前只放周六的周末就这样结束了，时间全用来`Trouble Shooting`了草
![草](https://i1.yuangezhizao.cn/Win-10/20191016005155.jpg!webp)

> 至此本文使命完成
