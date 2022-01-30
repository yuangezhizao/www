---
title: 上古神船也要物尽其用之安装 VMware ESXi 6.7
date: 2022-01-30 09:56:33
tags:
  - Z7M
  - VM
  - VMware
  - ESXi
count: 2
os: 1
os_1: Monterry 12.2 (21D49)
browser: 1
browser_1: 97.0.4692.99 Stable
place: 宽甸
key: 130
---
    除夕夜前一天终于想起一月份不能就这么鸽了
<!-- more -->
## 0x00.前言
算是上古？是六年前的[神舟 HASEE 战神 Z7M-i78172D1 笔记本](../../Windows/laptop.html)，每年回家都会被坑一次`.jpG`，没错昨晚一晚上就是这么过去的
反正已经炸了，在换装`Ubuntu Desktop`之前（珍爱生命，远离`Windows`），准备折腾下一直没有尝试的想法——在本子上装`ESXi`

## 0x01.封装自定义镜像
~~因为已经轻车熟路，~~本文只列出关键步骤，详细步骤可参考之前的相关文章

### 1.下载离线包
参照[VMware ESXi Release and Build Number History](https://web.archive.org/web/20220130020311/https://www.virten.net/vmware/esxi-release-build-number-history/)中关于`vSphere ESXi 6.7`的版本号，下载最新发布的`ESXi 6.7 January 2022 Patch`即应该是`ESXi670-202201001.zip`

Name | Patch | Date | Build
:---: | :---: | :---: | :---:
`ESXi 6.7 January 2022 Patch` | `ESXi670-202201001` | `2022-01-25` | `19195723`

结果官网找了一刻钟，发现`All Products`页面里有`7`版本的下载链接，但是木有`6.7`的只有`6.5`草，并且自己`7`的试用已经过期

<details><summary>点击此处 ← 查看折叠</summary>

![文档](https://i1.yuangezhizao.cn/macOS/20220130102242.png!webp)
![下载](https://i1.yuangezhizao.cn/macOS/20220130155740.png!webp)
![我的试用](https://i1.yuangezhizao.cn/macOS/20220130103034.png!webp)

</details>

然后发现原来`6.7`是在`Product Patches`里，[VMware ESXi 6.7, Patch Release ESXi670-202201001](https://web.archive.org/web/20220130023953/https://docs.vmware.com/en/VMware-vSphere/6.7/rn/esxi670-202201001.html)草

<details><summary>点击此处 ← 查看折叠</summary>

![产品补丁](https://i1.yuangezhizao.cn/macOS/20220130103225.png!webp)

</details>

> Release Date: 25 JAN 2022
Download Filename:	ESXi670-202201001.zip
Build:	19195723
Download Size:	478.2 MB
md5sum:	eb8ffccf1066ff84c56d959ced227e84
sha256checksum:	30d313abb16ac2ea742629dbd3eb31862a50d530f2cc5a505d60aff350a84b53
Host Reboot Required:	Yes
Virtual Machine Migration or Shutdown Required:	Yes

绝了，文件大小（`328M`）都对不上，反正哈希值是对的
![30d313abb16ac2ea742629dbd3eb31862a50d530f2cc5a505d60aff350a84b53](https://i1.yuangezhizao.cn/macOS/20220130104641.png!webp)

### 2.下载[ESXi-Customizer-PS](https://github.com/VFrontDe/ESXi-Customizer-PS)
最新版已经更新到`2.8.1`

### 3.下载`net55-r8168`驱动
嗯，仍然不支持`ESXi 7`（这就是为什么要装`ESXi 6.7`的根本原因

### 4.一句话封装
然后得到封装产物：`ESXi-6.7.0-20220104001-standard-customized.iso`

<details><summary>点击此处 ← 查看折叠</summary>

``` powershell
Microsoft Windows [版本 10.0.19044.1503]
(c) Microsoft Corporation。保留所有权利。

D:\yuangezhizao\Documents\ESXI\ESXi-Customizer-PS>powershell
Windows PowerShell
版权所有 (C) Microsoft Corporation。保留所有权利。

尝试新的跨平台 PowerShell https://aka.ms/pscore6

PS D:\yuangezhizao\Documents\ESXI\ESXi-Customizer-PS> .\ESXi-Customizer-PS.ps1 -izip .\ESXi670-202201001.zip -dpt .\net55-r8168-8.045a-napi-offline_bundle.zip -load net55-r8168

This is ESXi-Customizer-PS Version 2.8.1 (visit https://ESXi-Customizer-PS.v-front.de for more information!)
(Call with -help for instructions)

Logging to C:\Users\YUANGE~1\AppData\Local\Temp\ESXi-Customizer-PS-4628.log ...

Running with PowerShell version 5.1 and VMware PowerCLI version .. build

Adding base Offline bundle .\ESXi670-202201001.zip ... [OK]

Connecting additional depot .\net55-r8168-8.045a-napi-offline_bundle.zip ... [OK]

Getting Imageprofiles, please wait ... [OK]

Using Imageprofile ESXi-6.7.0-20220104001-standard ...
(Dated 01/12/2022 08:53:55, AcceptanceLevel: PartnerSupported,
Updates ESXi 6.7 Image Profile-ESXi-6.7.0-20220104001-standard)

Load additional VIBs from Online depots ...
   Add VIB net55-r8168 8.045a-napi [New AcceptanceLevel: CommunitySupported] [OK, added]

Exporting the Imageprofile to 'D:\yuangezhizao\Documents\ESXI\ESXi-Customizer-PS\ESXi-6.7.0-20220104001-standard-customized.iso'. Please be patient ...


All done.

PS D:\yuangezhizao\Documents\ESXI\ESXi-Customizer-PS>
```

</details>

## 0x02.放入`U`盘`LiveCD`
呜呜呜，`macOS`下木有[Rufus](https://rufus.ie/zh/)，之前试过`balenaEtcher`启动不能，这次再试一次好了（这块`USB 2.0`的`U`盘好慢

<details><summary>点击此处 ← 查看折叠</summary>

![提示缺少分区表](https://i1.yuangezhizao.cn/macOS/20220130112014.png!webp)
![辣鸡 U 盘](https://i1.yuangezhizao.cn/macOS/20220130112043.png!webp)
![烧录验证](https://i1.yuangezhizao.cn/macOS/20220130112203.png!webp)

</details>

果然还是启动不能，那么只能放弃`macOS`下折腾，去启动个`PE`运行`Rufus`进行烧录吗？
不，作为`macOS`的常驻玩家，怎么能轻易放弃呢？参照：[MAC 如何制作 Windows 启动盘给 PC 重装系统](https://web.archive.org/web/20220130071017/https://www.v2ex.com/t/800419)有两种方案
1. 一种是在`macOS`上启动`Windows for ARM`的虚拟机，这样就有`Rufus`可以用了；
2. 另一种则比较有意思了，在神船支持`UEFI`的情况下通过[Ventoy](https://github.com/ventoy/Ventoy)的[LiveCD](https://web.archive.org/web/20220130071523/https://www.ventoy.net/cn/doc_livecd.html)来启动自定义镜像

这里实际采用的是后者，因为现在手上没有能白嫖的`Parallels Desktop`（草
1. 首先用`磁盘工具`将`U`盘抹掉成`MS-DOS（FAT）`的格式，其实就是`FAT32`，然后把`ventoy-1.0.64-livecd.iso`的内容即一个`EFI`文件夹解压到`U`盘的根目录中，这样`LiveCD`就做好了
![目录结构](https://i1.yuangezhizao.cn/macOS/20220130154410.png!webp)

2. 然后通过`U`盘启动，并在选择在`U`盘上安装`Ventoy`，这样它就再也不是`LiveCD`了（

<details><summary>点击此处 ← 查看折叠</summary>

![此时还是 LiveCD](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20220130_115744.jpg!view)
![此时已是 Ventoy](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20220130_115852.jpg!view)

</details>

3. 最后再通过`U`盘启动自定义镜像，甚至可以安装`ESXi`到`U`盘，这样它就再也不是`Ventoy`了（（

> 至此`U`盘经历了：`LiveCD`→`Ventoy`→`ESXi`

## 0x03.安装`ESXi`
首先跟着安装向导一步一步的操作

<details><summary>点击此处 ← 查看折叠</summary>

![启动自定义镜像](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20220130_120241.jpg!view)
![选择磁盘](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20220130_123708.jpg!view)
![磁盘信息](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20220130_123741.jpg!view)
![确认](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20220130_123810.jpg!view)
![最终确认](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20220130_123924.jpg!view)
![安装后卡 75%](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20220130_124440.jpg!view)
![然后就 100%](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20220130_124708.jpg!view)

</details>

## 0x04.启动`ESXi`
然后重启就会进入到`ESXi`里辣

<details><summary>点击此处 ← 查看折叠</summary>

![启动中](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20220130_124928.jpg!view)
![启动完成](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20220130_125438.jpg!view)
![进入菜单](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20220130_125415.jpg!view)
![设置静态 IP](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20220130_125211.jpg!view)

</details>

## 0x05.登录`ESXi`
![登录](https://i1.yuangezhizao.cn/macOS/20220130125749.png!webp)
![0A65P-00HD0-3Z5M1-M097M-22P7H](https://i1.yuangezhizao.cn/macOS/20220130130130.png!webp)
![开幕 CVE 雷击](https://i1.yuangezhizao.cn/macOS/20220130130334.png!webp)
![独显可以切换直通](https://i1.yuangezhizao.cn/macOS/20220130130535.png!webp)
![虚拟网卡](https://i1.yuangezhizao.cn/macOS/20220130131159.png!webp)
![虚拟交换机](https://i1.yuangezhizao.cn/macOS/20220130131217.png!webp)
![ESXi 用不到 4G 空间](https://i1.yuangezhizao.cn/macOS/20220130131459.png!webp)
![并未使用的 SSD](https://i1.yuangezhizao.cn/macOS/20220130131541.png!webp)

## 0x06.后记
早上起来十点前就开始搞了，结果没想到搞了一白天都到下午四点半了草

## 0x07.引用

[VMware Overview of ‘L1 Terminal Fault’ (L1TF) Speculative-Execution vulnerabilities in Intel processors: CVE-2018-3646, CVE-2018-3620, and CVE-2018-3615 (55636)](https://kb.vmware.com/s/article/55636)
[老笔记本安装ESXI和群晖，不再吃灰](https://web.archive.org/web/20220130122630/https://blog.csdn.net/hahofe/article/details/117519109)

> 至此本文使命完成
