---
title: 干炸里脊逆向
date: 2020-4-17 22:45:44
tags:
  - Il2Cpp
  - Il2CppDumper
count: 2
os: 0
os_1: 10.0.17763.1098 2019-LTSC
browser: 0
browser_1: 78.0.3904.108 Stable
place: 新家
key: 85
---
    只能跪着看大佬们的神操作了
<!-- more -->
## 0x00.前言
`b`（国）服今上午`11`点开了，同事都请假回家刷初始了，而本人却仍旧在社畜……
晚上回来甚至没管自己的初始号，毕竟并不能肝动这游戏，因为当初台服就是“三分钟热度”，然后就没怎么碰了
于是，直接谷歌搜索`公主连接 逆向`，那就从第一篇文章开始读起吧
[[Android 原创] [unity][超異域公主連結！Re:Dive ] 1.5.1解包(削弱敌方](https://web.archive.org/web/20200417144937/https://www.52pojie.cn/thread-999365-1-1.html)

## 0x01.解压`apk`
右键`7z`解压，可以看出与原文不同的是，国服提供了`SymbolMap-ARM64`、`SymbolMap-ARMv7`、`SymbolMap-x86`适配各种机型（甚至模拟器）
![解压](https://i1.yuangezhizao.cn/Win-10/20200417225108.jpg!webp)

可以肯定的是`Unity`[IL2CPP](https://web.archive.org/web/20200418113811/https://docs.unity3d.com/2017.4/Documentation/Manual/IL2CPP.html)打包的游戏，但是`global-metadata.dat`与原文不同**并未**隐藏
![IL2CPP](https://i1.yuangezhizao.cn/Win-10/20200418193352.jpg!webp)

原理可见[官方文档](https://web.archive.org/web/20200418114004/https://docs.unity3d.com/2017.4/Documentation/Manual/IL2CPP-HowItWorks.html)
![IL2CPP-HowItWorks.html](https://i1.yuangezhizao.cn/Win-10/20200418194050.jpg!webp)

然后就可以去拿`perfare`大的`Il2CppDumper v6.1.0`解析了，解压的时候看到了`lib`目录下有`libNetHTProtect.so`，草

## 0x02.[Il2CppDumper](https://github.com/Perfare/Il2CppDumper)
> Unity il2cpp reverse engineer

英文`README`一眼看到了命令行调用方式：`Il2CppDumper.exe <executable-file> <global-metadata>`
根据[中文说明](https://web.archive.org/web/20200417145911/https://github.com/Perfare/Il2CppDumper/blob/master/README.zh-CN.md)，运行`Il2CppDumper.exe`后先选择`\lib\armeabi-v7a\libil2cpp.so`后选择`\assets\bin\Data\Managed\Metadata\global-metadata.dat`即可，**然后根据提示输入相应信息**
果然提示可能受保护，需要手动输入`CodeRegistration`……
![解析](https://i1.yuangezhizao.cn/Win-10/20200417224035.jpg!webp)

再联想到之前看到的`libNetHTProtect`，果然
![枯了](https://i1.yuangezhizao.cn/Win-10/20191028224844.jpg!webp)

`libil2cpp.so`扔`IDA`也看到了大量的`nullsub_*`函数名，溜了溜了
![IDA](https://i1.yuangezhizao.cn/Win-10/20200417233305.jpg!webp)

不说了去上主号了，听天由命

## 0x03.[Gameguardian](https://web.archive.org/web/20200418100507/https://gameguardian.net/download)
`2020-4-18 18:04:16`：
`功能`和`常见问题`有说：
> 支持从内存`dump`的`libil2cpp.so`文件以绕过`99%`的保护<br>
`ERROR: This file may be protected.`
`Il2CppDumper`检测到可执行文件已被保护，使用`GameGuardian`从游戏内存中`dump libil2cpp.so`，然后使用`Il2CppDumper`载入按提示操作，即可绕过`99%`的保护

根据[Il2CppDumper使用Dump破解國内so加密手游](https://web.archive.org/web/20200418100450/https://www.xn--05v.jp/2020/01/29/3/)
去下载`GG`，模拟器用的是`Memu`，因为之前一直在用的就是这个，可以安装基于`Android 5.1`的`Xposed`
![介绍](https://i1.yuangezhizao.cn/Win-10/20200418181156.jpg!webp)
![Download](https://i1.yuangezhizao.cn/Win-10/20200418180958.jpg!webp)

使用`GG`从内存`dump`出`so`文件，把`GameGuardian.95.0.apk`和`公主连结R_2.4.6.apk`扔进模拟器，运行选择干炸里脊的进程（最大的那个就是），这里看到的全是零
注意需要开启`GG`隐藏（本人`1234`均选择了），否则导出中途游戏会闪退
![dump](https://i1.yuangezhizao.cn/Win-10/20200418140737.png!webp)

然后`dump`内存保存至`文件夹`
![文件夹](https://i1.yuangezhizao.cn/Win-10/20200418181810.jpg!webp)

地址范围默认即可
![保存](https://i1.yuangezhizao.cn/Win-10/20200418141513.png!webp)
![导出结束](https://i1.yuangezhizao.cn/Win-10/20200418141505.png!webp)

文件夹下全是`bin`以及一个`map`表文件
![dump](https://i1.yuangezhizao.cn/Win-10/20200418182803.jpg!webp)

打开`com.bilibili.priconne-maps.txt`文件，里面记录着内存中的文件位置

<details><summary>点击此处 ← 查看文件</summary>

``` bash
00008000-02bfb000 rw-p 00000000 00:00 0 
12c00000-12e01000 rw-p 00000000 00:01 7370       /dev/ashmem/dalvik-main space (deleted)
12e01000-139a7000 rw-p 00201000 00:01 7370       /dev/ashmem/dalvik-main space (deleted)
139a7000-22c00000 ---p 00da7000 00:01 7370       /dev/ashmem/dalvik-main space (deleted)
22c00000-22c01000 rw-p 00000000 00:01 7371       /dev/ashmem/dalvik-main space (deleted)
22c01000-32c00000 ---p 00001000 00:01 7371       /dev/ashmem/dalvik-main space (deleted)
6e000000-6f800000 rw-p 00000000 00:00 0 
6fafe000-70474000 rw-p 00000000 08:13 231        /data/dalvik-cache/x86/system@framework@boot.art
70474000-71f09000 r--p 00000000 08:13 51         /data/dalvik-cache/x86/system@framework@boot.oat
71f09000-73935000 r-xp 01a95000 08:13 51         /data/dalvik-cache/x86/system@framework@boot.oat
73935000-73936000 rw-p 034c1000 08:13 51         /data/dalvik-cache/x86/system@framework@boot.oat
73936000-7402e000 rw-p 00000000 00:01 7369       /dev/ashmem/dalvik-zygote space (deleted)
7402e000-7402f000 rw-p 00000000 00:01 7026       /dev/ashmem/dalvik-non moving space (deleted)
7402f000-74150000 rw-p 00001000 00:01 7026       /dev/ashmem/dalvik-non moving space (deleted)
74150000-76937000 ---p 00122000 00:01 7026       /dev/ashmem/dalvik-non moving space (deleted)
76937000-77936000 rw-p 02909000 00:01 7026       /dev/ashmem/dalvik-non moving space (deleted)
77c00000-78400000 rw-p 00000000 00:00 0 
78662000-787b4000 rw-s 00000000 00:01 404921     /dev/ashmem/gralloc-buffer (deleted)
787b4000-789b4000 rw-s 00000000 00:0d 9238       /dev/ttyS10
78a5e000-78bb0000 rw-s 00000000 00:01 404920     /dev/ashmem/gralloc-buffer (deleted)
78bb0000-78d02000 rw-s 00000000 00:01 404916     /dev/ashmem/gralloc-buffer (deleted)
78d02000-78f02000 rw-s 00000000 00:0d 9238       /dev/ttyS10
79000000-79800000 rw-p 00000000 00:00 0 
79817000-7a000000 rw-s 00000000 00:01 404273     /dev/ashmem/ACodec (deleted)
7a000000-7a800000 rw-s 00000000 00:01 404272     /dev/ashmem/ACodec (deleted)
7a800000-7cc00000 rw-p 00000000 00:00 0 
7cc17000-7d400000 rw-s 00000000 00:01 406056     /dev/ashmem/ACodec (deleted)
7d400000-7dc00000 rw-s 00000000 00:01 406055     /dev/ashmem/ACodec (deleted)
7dc00000-80000000 rw-p 00000000 00:00 0 
80017000-80800000 rw-s 00000000 00:01 406053     /dev/ashmem/ACodec (deleted)
80800000-81000000 rw-s 00000000 00:01 406052     /dev/ashmem/ACodec (deleted)
81000000-82c00000 rw-p 00000000 00:00 0 
82c17000-83400000 rw-s 00000000 00:01 404271     /dev/ashmem/ACodec (deleted)
83400000-84800000 rw-p 00000000 00:00 0 
84833000-84a33000 rw-s 00000000 00:0d 9238       /dev/ttyS10
84a33000-84b53000 rw-s 00000000 00:01 395423     /dev/ashmem/gralloc-buffer (deleted)
84b53000-84d53000 rw-s 00000000 00:0d 9238       /dev/ttyS10
84d53000-85553000 rw-s 00000000 00:01 404270     /dev/ashmem/ACodec (deleted)
85553000-85800000 r--p 00000000 00:16 149        /storage/emulated/0/Android/data/com.bilibili.priconne/files/il2cpp/SymbolMap-x86
85800000-87c00000 rw-p 00000000 00:00 0 
87c00000-88000000 rw-p 00000000 00:00 0 
88003000-88155000 rw-s 00000000 00:01 404919     /dev/ashmem/gralloc-buffer (deleted)
88155000-88176000 rw-p 00000000 00:01 394852     /dev/ashmem/dalvik-large object space allocation (deleted)
88176000-88197000 rw-p 00000000 00:01 394851     /dev/ashmem/dalvik-large object space allocation (deleted)
88197000-881b8000 rw-p 00000000 00:01 394850     /dev/ashmem/dalvik-large object space allocation (deleted)
881b8000-881d9000 rw-p 00000000 00:01 394849     /dev/ashmem/dalvik-large object space allocation (deleted)
881d9000-881fa000 rw-p 00000000 00:01 394837     /dev/ashmem/dalvik-large object space allocation (deleted)
881fa000-8821b000 rw-p 00000000 00:01 394836     /dev/ashmem/dalvik-large object space allocation (deleted)
8821b000-8823c000 rw-p 00000000 00:01 394835     /dev/ashmem/dalvik-large object space allocation (deleted)
8823c000-8825d000 rw-p 00000000 00:01 394834     /dev/ashmem/dalvik-large object space allocation (deleted)
8825d000-8827e000 rw-p 00000000 00:01 394833     /dev/ashmem/dalvik-large object space allocation (deleted)
8827e000-8829f000 rw-p 00000000 00:01 394832     /dev/ashmem/dalvik-large object space allocation (deleted)
8829f000-882c0000 rw-p 00000000 00:01 394831     /dev/ashmem/dalvik-large object space allocation (deleted)
882c0000-882e1000 rw-p 00000000 00:01 394830     /dev/ashmem/dalvik-large object space allocation (deleted)
882e1000-88302000 rw-p 00000000 00:01 394829     /dev/ashmem/dalvik-large object space allocation (deleted)
88400000-88800000 rw-p 00000000 00:00 0 
88804000-88825000 rw-p 00000000 00:01 394828     /dev/ashmem/dalvik-large object space allocation (deleted)
88825000-88846000 rw-p 00000000 00:01 394827     /dev/ashmem/dalvik-large object space allocation (deleted)
88846000-88867000 rw-p 00000000 00:01 394826     /dev/ashmem/dalvik-large object space allocation (deleted)
88867000-88888000 rw-p 00000000 00:01 394825     /dev/ashmem/dalvik-large object space allocation (deleted)
88888000-888a9000 rw-p 00000000 00:01 394824     /dev/ashmem/dalvik-large object space allocation (deleted)
888a9000-888ca000 rw-p 00000000 00:01 394823     /dev/ashmem/dalvik-large object space allocation (deleted)
888ca000-888eb000 rw-p 00000000 00:01 394822     /dev/ashmem/dalvik-large object space allocation (deleted)
888eb000-8890c000 rw-p 00000000 00:01 394751     /dev/ashmem/dalvik-large object space allocation (deleted)
8890c000-8892d000 rw-p 00000000 00:01 394821     /dev/ashmem/dalvik-large object space allocation (deleted)
8892d000-8894e000 rw-p 00000000 00:01 394820     /dev/ashmem/dalvik-large object space allocation (deleted)
8894e000-8896f000 rw-p 00000000 00:01 394819     /dev/ashmem/dalvik-large object space allocation (deleted)
8896f000-88990000 rw-p 00000000 00:01 394818     /dev/ashmem/dalvik-large object space allocation (deleted)
88990000-889b1000 rw-p 00000000 00:01 394817     /dev/ashmem/dalvik-large object space allocation (deleted)
889b1000-889d2000 rw-p 00000000 00:01 394816     /dev/ashmem/dalvik-large object space allocation (deleted)
889d2000-889f3000 rw-p 00000000 00:01 394815     /dev/ashmem/dalvik-large object space allocation (deleted)
889f3000-88a14000 rw-p 00000000 00:01 394814     /dev/ashmem/dalvik-large object space allocation (deleted)
88a14000-88a35000 rw-p 00000000 00:01 394813     /dev/ashmem/dalvik-large object space allocation (deleted)
88a35000-88a56000 rw-p 00000000 00:01 394812     /dev/ashmem/dalvik-large object space allocation (deleted)
88a56000-88a77000 rw-p 00000000 00:01 394811     /dev/ashmem/dalvik-large object space allocation (deleted)
88a77000-88a98000 rw-p 00000000 00:01 393967     /dev/ashmem/dalvik-large object space allocation (deleted)
88a98000-88ab9000 rw-p 00000000 00:01 394810     /dev/ashmem/dalvik-large object space allocation (deleted)
88ab9000-88ada000 rw-p 00000000 00:01 394809     /dev/ashmem/dalvik-large object space allocation (deleted)
88ada000-88adb000 ---p 00000000 00:00 0 
88adb000-88adc000 ---p 00000000 00:00 0 
88adc000-88bde000 rw-p 00000000 00:00 0          [stack:13180]
88bde000-88bff000 rw-p 00000000 00:01 394808     /dev/ashmem/dalvik-large object space allocation (deleted)
88bff000-88c20000 rw-p 00000000 00:01 394807     /dev/ashmem/dalvik-large object space allocation (deleted)
88c20000-88c41000 rw-p 00000000 00:01 394806     /dev/ashmem/dalvik-large object space allocation (deleted)
88c41000-88c62000 rw-p 00000000 00:01 394805     /dev/ashmem/dalvik-large object space allocation (deleted)
88c62000-88c83000 rw-p 00000000 00:01 394804     /dev/ashmem/dalvik-large object space allocation (deleted)
88c83000-88ca4000 rw-p 00000000 00:01 394803     /dev/ashmem/dalvik-large object space allocation (deleted)
88ca4000-88cc5000 rw-p 00000000 00:01 394802     /dev/ashmem/dalvik-large object space allocation (deleted)
88cc5000-88ce6000 rw-p 00000000 00:01 394801     /dev/ashmem/dalvik-large object space allocation (deleted)
88ce6000-88ce7000 ---p 00000000 00:00 0 
88ce7000-88ce8000 ---p 00000000 00:00 0 
88ce8000-88dea000 rw-p 00000000 00:00 0          [stack:13173]
88dea000-88deb000 ---p 00000000 00:00 0 
88deb000-88dec000 ---p 00000000 00:00 0 
88dec000-88eee000 rw-p 00000000 00:00 0          [stack:13172]
88eee000-88eef000 ---p 00000000 00:00 0 
88eef000-88ef0000 ---p 00000000 00:00 0 
88ef0000-88ff2000 rw-p 00000000 00:00 0          [stack:13168]
88ff8000-88ff9000 ---p 00000000 00:00 0 
88ff9000-890f6000 rw-p 00000000 00:00 0          [stack:15252]
890f6000-890f7000 ---p 00000000 00:00 0 
890f7000-890f8000 ---p 00000000 00:00 0 
890f8000-891fa000 rw-p 00000000 00:00 0          [stack:15203]
891fa000-891fb000 ---p 00000000 00:00 0 
891fb000-891fc000 ---p 00000000 00:00 0 
891fc000-892fe000 rw-p 00000000 00:00 0          [stack:13159]
892fe000-892ff000 ---p 00000000 00:00 0 
892ff000-89300000 ---p 00000000 00:00 0 
89300000-89402000 rw-p 00000000 00:00 0          [stack:13158]
89402000-89403000 ---p 00000000 00:00 0 
89403000-89404000 ---p 00000000 00:00 0 
89404000-89506000 rw-p 00000000 00:00 0          [stack:13157]
89517000-89538000 rw-p 00000000 00:01 394800     /dev/ashmem/dalvik-large object space allocation (deleted)
89538000-89559000 rw-p 00000000 00:01 394799     /dev/ashmem/dalvik-large object space allocation (deleted)
89559000-8957a000 rw-p 00000000 00:01 394798     /dev/ashmem/dalvik-large object space allocation (deleted)
8957a000-8959b000 rw-p 00000000 00:01 394797     /dev/ashmem/dalvik-large object space allocation (deleted)
8959b000-895bc000 rw-p 00000000 00:01 394796     /dev/ashmem/dalvik-large object space allocation (deleted)
895bc000-895dd000 rw-p 00000000 00:01 394795     /dev/ashmem/dalvik-large object space allocation (deleted)
895dd000-895fe000 rw-p 00000000 00:01 394794     /dev/ashmem/dalvik-large object space allocation (deleted)
895fe000-895ff000 ---p 00000000 00:00 0 
895ff000-89600000 ---p 00000000 00:00 0 
89600000-89702000 rw-p 00000000 00:00 0          [stack:13164]
89702000-89703000 ---p 00000000 00:00 0 
89703000-89800000 rw-p 00000000 00:00 0          [stack:13152]
89800000-89c00000 rw-p 00000000 00:00 0 
89c0d000-89c2e000 rw-p 00000000 00:01 394793     /dev/ashmem/dalvik-large object space allocation (deleted)
89c2e000-89c4f000 rw-p 00000000 00:01 394792     /dev/ashmem/dalvik-large object space allocation (deleted)
89c4f000-89c70000 rw-p 00000000 00:01 394791     /dev/ashmem/dalvik-large object space allocation (deleted)
89c70000-89c91000 rw-p 00000000 00:01 394790     /dev/ashmem/dalvik-large object space allocation (deleted)
89c91000-89cb2000 rw-p 00000000 00:01 392568     /dev/ashmem/dalvik-large object space allocation (deleted)
89cb2000-89cd3000 rw-p 00000000 00:01 394789     /dev/ashmem/dalvik-large object space allocation (deleted)
89cd3000-89cf4000 rw-p 00000000 00:01 394788     /dev/ashmem/dalvik-large object space allocation (deleted)
89cf4000-89cf5000 ---p 00000000 00:00 0 
89cf5000-89cf6000 ---p 00000000 00:00 0 
89cf6000-89df8000 rw-p 00000000 00:00 0          [stack:13148]
89df8000-89df9000 ---p 00000000 00:00 0 
89df9000-89dfa000 ---p 00000000 00:00 0 
89dfa000-89efc000 rw-p 00000000 00:00 0          [stack:13147]
89efc000-89efd000 ---p 00000000 00:00 0 
89efd000-89efe000 ---p 00000000 00:00 0 
89efe000-8a000000 rw-p 00000000 00:00 0          [stack:13144]
8a000000-8a400000 rw-p 00000000 00:00 0 
8a41e000-8a61e000 rw-s 00000000 00:0d 9238       /dev/ttyS10
8a61e000-8a61f000 ---p 00000000 00:00 0 
8a61f000-8a620000 ---p 00000000 00:00 0 
8a620000-8a71c000 rw-p 00000000 00:00 0          [stack:13087]
8a722000-8a723000 ---p 00000000 00:00 0 
8a723000-8a820000 rw-p 00000000 00:00 0          [stack:15265]
8a820000-8a940000 rw-s 00000000 00:01 391774     /dev/ashmem/gralloc-buffer (deleted)
8aa0c000-8aa0d000 ---p 00000000 00:00 0 
8aa0d000-8aa0e000 ---p 00000000 00:00 0 
8aa0e000-8ab0a000 rw-p 00000000 00:00 0          [stack:15042]
8ab0a000-8ab0b000 ---p 00000000 00:00 0 
8ab0b000-8ac08000 rw-p 00000000 00:00 0          [stack:15041]
8ac08000-8ac09000 ---p 00000000 00:00 0 
8ac09000-8ad06000 rw-p 00000000 00:00 0          [stack:15040]
8ad06000-8ad07000 ---p 00000000 00:00 0 
8ad07000-8ad08000 ---p 00000000 00:00 0 
8ad08000-8ae04000 rw-p 00000000 00:00 0          [stack:15039]
8ae04000-8ae05000 ---p 00000000 00:00 0 
8ae05000-8ae06000 ---p 00000000 00:00 0 
8ae06000-8af02000 rw-p 00000000 00:00 0          [stack:15038]
8af02000-8af03000 ---p 00000000 00:00 0 
8af03000-8b000000 rw-p 00000000 00:00 0          [stack:15037]
8b000000-8c400000 rw-p 00000000 00:00 0 
8c41d000-8c43e000 rw-p 00000000 00:01 394787     /dev/ashmem/dalvik-large object space allocation (deleted)
8c43e000-8c45f000 rw-p 00000000 00:01 394786     /dev/ashmem/dalvik-large object space allocation (deleted)
8c45f000-8c480000 rw-p 00000000 00:01 394785     /dev/ashmem/dalvik-large object space allocation (deleted)
8c480000-8c4a1000 rw-p 00000000 00:01 394784     /dev/ashmem/dalvik-large object space allocation (deleted)
8c4a1000-8c4aa000 rw-p 00000000 00:01 391798     /dev/ashmem/dalvik-large object space allocation (deleted)
8c4d9000-8c4da000 ---p 00000000 00:00 0 
8c4da000-8c5d7000 rw-p 00000000 00:00 0          [stack:15036]
8c5d7000-8c5f8000 rw-p 00000000 00:01 394783     /dev/ashmem/dalvik-large object space allocation (deleted)
8c5f8000-8c619000 rw-p 00000000 00:01 394782     /dev/ashmem/dalvik-large object space allocation (deleted)
8c619000-8c61e000 rw-p 00000000 00:01 391797     /dev/ashmem/dalvik-large object space allocation (deleted)
8c61e000-8c623000 rw-p 00000000 00:01 391796     /dev/ashmem/dalvik-large object space allocation (deleted)
8c628000-8c660000 rw-p 00000000 00:01 391778     /dev/ashmem/dalvik-large object space allocation (deleted)
8c660000-8c6f8000 r-xp 00000000 08:13 122886     /data/app/com.bilibili.priconne-1/lib/x86/libsqlite3android.so
8c6f8000-8c6f9000 ---p 00000000 00:00 0 
8c6f9000-8c6fa000 r--p 00098000 08:13 122886     /data/app/com.bilibili.priconne-1/lib/x86/libsqlite3android.so
8c6fa000-8c6fb000 rw-p 00099000 08:13 122886     /data/app/com.bilibili.priconne-1/lib/x86/libsqlite3android.so
8c6fb000-8c6fc000 rw-p 00000000 00:00 0 
8c6fc000-8c6fd000 ---p 00000000 00:00 0 
8c6fd000-8c6fe000 ---p 00000000 00:00 0 
8c6fe000-8c800000 rw-p 00000000 00:00 0          [stack:12918]
8c800000-8cc00000 rw-p 00000000 00:00 0 
8cc12000-8cc1b000 rw-p 00000000 00:01 391784     /dev/ashmem/dalvik-large object space allocation (deleted)
8cc1b000-8cc1f000 rw-p 00000000 00:01 391783     /dev/ashmem/dalvik-large object space allocation (deleted)
8cc1f000-8cc23000 rw-p 00000000 00:01 391782     /dev/ashmem/dalvik-large object space allocation (deleted)
8cc23000-8cc27000 rw-p 00000000 00:01 391781     /dev/ashmem/dalvik-large object space allocation (deleted)
8cc27000-8cc2b000 rw-p 00000000 00:01 391780     /dev/ashmem/dalvik-large object space allocation (deleted)
8cc2b000-8cc2f000 rw-p 00000000 00:01 391779     /dev/ashmem/dalvik-large object space allocation (deleted)
8cc2f000-8cc38000 rw-p 00000000 00:01 388050     /dev/ashmem/dalvik-large object space allocation (deleted)
8cc38000-8cc41000 rw-p 00000000 00:01 388049     /dev/ashmem/dalvik-large object space allocation (deleted)
8cc41000-8cc4a000 rw-p 00000000 00:01 388048     /dev/ashmem/dalvik-large object space allocation (deleted)
8cc4a000-8cc7d000 rw-p 00000000 00:01 388045     /dev/ashmem/dalvik-large object space allocation (deleted)
8cc7d000-8cc9e000 rw-p 00000000 00:01 394781     /dev/ashmem/dalvik-large object space allocation (deleted)
8cc9e000-8ccbf000 rw-p 00000000 00:01 394780     /dev/ashmem/dalvik-large object space allocation (deleted)
8ccbf000-8cce0000 rw-p 00000000 00:01 394779     /dev/ashmem/dalvik-large object space allocation (deleted)
8cce0000-8ce00000 rw-s 00000000 00:01 391769     /dev/ashmem/gralloc-buffer (deleted)
8ce7c000-8ce7d000 ---p 00000000 00:00 0 
8ce7d000-8ce7e000 ---p 00000000 00:00 0 
8ce7e000-8cf7a000 rw-p 00000000 00:00 0          [stack:15035]
8cf7a000-8cf7b000 ---p 00000000 00:00 0 
8cf7b000-8cf7c000 ---p 00000000 00:00 0 
8cf7c000-8d078000 rw-p 00000000 00:00 0          [stack:15034]
8d078000-8d079000 ---p 00000000 00:00 0 
8d079000-8d176000 rw-p 00000000 00:00 0          [stack:15033]
8d176000-8d177000 ---p 00000000 00:00 0 
8d177000-8d274000 rw-p 00000000 00:00 0          [stack:15032]
8d274000-8d275000 ---p 00000000 00:00 0 
8d275000-8d276000 ---p 00000000 00:00 0 
8d276000-8d372000 rw-p 00000000 00:00 0          [stack:15031]
8d372000-8d373000 ---p 00000000 00:00 0 
8d373000-8d374000 ---p 00000000 00:00 0 
8d374000-8d470000 rw-p 00000000 00:00 0          [stack:15030]
8d470000-8d471000 ---p 00000000 00:00 0 
8d471000-8d56e000 rw-p 00000000 00:00 0          [stack:15029]
8d56e000-8d6b7000 r--s 3d658000 08:13 227        /data/app/com.bilibili.priconne-1/base.apk
8d6b7000-8d800000 r--s 3d7a0000 08:13 227        /data/app/com.bilibili.priconne-1/base.apk
8d800000-8e400000 rw-p 00000000 00:00 0 
8e400000-8e408000 rw-p 00000000 00:01 391776     /dev/ashmem/dalvik-large object space allocation (deleted)
8e408000-8e429000 rw-p 00000000 00:01 394778     /dev/ashmem/dalvik-large object space allocation (deleted)
8e429000-8e449000 rw-s 00000000 00:01 390993     /dev/ashmem (deleted)
8e449000-8e44a000 ---p 00000000 00:00 0 
8e44a000-8e44b000 ---p 00000000 00:00 0 
8e44b000-8e54d000 rw-p 00000000 00:00 0          [stack:12917]
8e58b000-8e6ab000 rw-s 00000000 00:01 396085     /dev/ashmem/gralloc-buffer (deleted)
8e730000-8e87c000 r--s 3d3c6000 08:13 227        /data/app/com.bilibili.priconne-1/base.apk
8e87c000-8e9c7000 r--s 3d27c000 08:13 227        /data/app/com.bilibili.priconne-1/base.apk
8e9c7000-8e9c8000 ---p 00000000 00:00 0 
8e9c8000-8e9c9000 ---p 00000000 00:00 0 
8e9c9000-8eac5000 rw-p 00000000 00:00 0          [stack:12889]
8eac5000-8eac6000 ---p 00000000 00:00 0 
8eac6000-8eac7000 ---p 00000000 00:00 0 
8eac7000-8ebc9000 rw-p 00000000 00:00 0          [stack:12888]
8ebc9000-8ebca000 ---p 00000000 00:00 0 
8ebca000-8ebcb000 ---p 00000000 00:00 0 
8ebcb000-8ecc7000 rw-p 00000000 00:00 0          [stack:12886]
8ecc7000-8ecc8000 ---p 00000000 00:00 0 
8ecc8000-8edc5000 rw-p 00000000 00:00 0          [stack:12885]
8edc5000-8edc6000 ---p 00000000 00:00 0 
8edc6000-8edc7000 ---p 00000000 00:00 0 
8edc7000-8eec3000 rw-p 00000000 00:00 0          [stack:12884]
8eec3000-8eec4000 ---p 00000000 00:00 0 
8eec4000-8eec5000 ---p 00000000 00:00 0 
8eec5000-8efc1000 rw-p 00000000 00:00 0          [stack:12883]
8efc1000-8efc2000 ---p 00000000 00:00 0 
8efc2000-8efc3000 ---p 00000000 00:00 0 
8efc3000-8f0bf000 rw-p 00000000 00:00 0          [stack:12882]
8f0bf000-8f0c0000 ---p 00000000 00:00 0 
8f0c0000-8f0c1000 ---p 00000000 00:00 0 
8f0c1000-8f1bd000 rw-p 00000000 00:00 0          [stack:12881]
8f1bd000-8f800000 r--s 00000000 08:06 56         /system/app/webview/webview.apk
8f800000-8fc00000 rw-p 00000000 00:00 0 
8fc01000-8fc03000 rw-p 00000000 00:01 391810     /dev/ashmem/dalvik-indirect ref table (deleted)
8fc03000-8fc05000 rw-p 00000000 00:01 387601     /dev/ashmem/dalvik-indirect ref table (deleted)
8fc05000-8fc07000 rw-p 00000000 00:00 0 
8fc07000-8fc09000 rw-p 00000000 00:01 390992     /dev/ashmem/dalvik-indirect ref table (deleted)
8fc09000-8fc0b000 rw-p 00000000 00:00 0 
8fc0c000-8fc10000 rw-p 00000000 00:01 391777     /dev/ashmem/dalvik-large object space allocation (deleted)
8fc10000-8fc14000 rw-p 00000000 00:01 388047     /dev/ashmem/dalvik-large object space allocation (deleted)
8fc14000-8fc16000 rw-p 00000000 00:00 0 
8fc16000-8fc1b000 rw-p 00000000 00:01 388046     /dev/ashmem/dalvik-large object space allocation (deleted)
8fc20000-8fc41000 rw-p 00000000 00:01 394777     /dev/ashmem/dalvik-large object space allocation (deleted)
8fc41000-8fc62000 rw-p 00000000 00:01 394776     /dev/ashmem/dalvik-large object space allocation (deleted)
8fc62000-8fc6e000 r--s 00000000 08:13 131187     /data/data/com.bilibili.priconne/app_webview/Web Data
8fc8c000-8fc8e000 rw-p 00000000 00:01 391333     /dev/ashmem/dalvik-indirect ref table (deleted)
8fc8e000-8fc90000 rw-p 00000000 00:00 0 
8fc9a000-8fc9c000 rw-p 00000000 00:01 390990     /dev/ashmem/dalvik-indirect ref table (deleted)
8fc9c000-8fc9e000 rw-p 00000000 00:00 0 
8fc9e000-8fc9f000 ---p 00000000 00:00 0 
8fc9f000-8fca0000 ---p 00000000 00:00 0 
8fca0000-8fd9c000 rw-p 00000000 00:00 0          [stack:12880]
8fd9c000-8fe5e000 r--s 0073f000 08:06 56         /system/app/webview/webview.apk
8fe5e000-8fefc000 r--s 006a2000 08:06 56         /system/app/webview/webview.apk
8fefc000-8fefd000 ---p 00000000 00:00 0 
8fefd000-8fefe000 ---p 00000000 00:00 0 
8fefe000-90000000 rw-p 00000000 00:00 0          [stack:12877]
90000000-90400000 rw-p 00000000 00:00 0 
90400000-90402000 rw-p 00000000 00:01 390989     /dev/ashmem/dalvik-indirect ref table (deleted)
90402000-90403000 ---p 00000000 00:00 0 
90403000-90500000 rw-p 00000000 00:00 0          [stack:12876]
90500000-90501000 ---p 00000000 00:00 0 
90501000-905fe000 rw-p 00000000 00:00 0          [stack:12875]
905fe000-905ff000 ---p 00000000 00:00 0 
905ff000-906fc000 rw-p 00000000 00:00 0          [stack:12874]
906fc000-906fe000 rw-p 00000000 00:01 391283     /dev/ashmem/dalvik-indirect ref table (deleted)
906fe000-90700000 rw-p 00000000 00:01 389451     /dev/ashmem/dalvik-indirect ref table (deleted)
90700000-90702000 rw-p 00000000 00:01 391282     /dev/ashmem/dalvik-indirect ref table (deleted)
90702000-90703000 ---p 00000000 00:00 0 
90703000-90704000 ---p 00000000 00:00 0 
90704000-90800000 rw-p 00000000 00:00 0          [stack:12879]
90800000-90c04000 rw-p 00000000 00:00 0 
90c04000-90c06000 rw-p 00000000 00:01 390988     /dev/ashmem/dalvik-indirect ref table (deleted)
90c06000-90c08000 rw-p 00000000 00:01 390987     /dev/ashmem/dalvik-indirect ref table (deleted)
90c08000-90c0a000 rw-p 00000000 00:01 389450     /dev/ashmem/dalvik-indirect ref table (deleted)
90c0a000-90c0e000 rw-p 00000000 00:00 0 
90c0e000-90c11000 r--s 00878000 08:06 56         /system/app/webview/webview.apk
90c11000-90c72000 r--s 00642000 08:06 56         /system/app/webview/webview.apk
90c81000-90c83000 rw-p 00000000 00:00 0 
90c83000-90c86000 r-xp 00000000 08:06 965        /system/lib/libwebviewchromium_plat_support.so
90c86000-90c87000 r--p 00002000 08:06 965        /system/lib/libwebviewchromium_plat_support.so
90c87000-90c88000 rw-p 00003000 08:06 965        /system/lib/libwebviewchromium_plat_support.so
90c88000-90c89000 ---p 00000000 00:00 0 
90c89000-90d86000 rw-p 00000000 00:00 0          [stack:12873]
90d86000-90e8d000 r--p 00000000 00:01 391277     /dev/ashmem/dalvik-classes.dex extracted in memory from /system/app/webview/webview.apk (deleted)
90e8d000-90e8f000 rw-p 00000000 00:00 0 
90e8f000-90e91000 rw-p 00000000 00:01 390983     /dev/ashmem/dalvik-indirect ref table (deleted)
90e91000-90eb9000 r--s 0087c000 08:06 56         /system/app/webview/webview.apk
90eb9000-90ebd000 r--s 00951000 08:06 56         /system/app/webview/webview.apk
90ebd000-90ebe000 ---p 00000000 00:00 0 
90ebe000-90ebf000 ---p 00000000 00:00 0 
90ebf000-90fc1000 rw-p 00000000 00:00 0          [stack:12864]
90fc1000-90fea000 r-xp 00000000 08:13 122884     /data/app/com.bilibili.priconne-1/lib/x86/libBugly.so
90fea000-90feb000 r--p 00028000 08:13 122884     /data/app/com.bilibili.priconne-1/lib/x86/libBugly.so
90feb000-90fec000 rw-p 00029000 08:13 122884     /data/app/com.bilibili.priconne-1/lib/x86/libBugly.so
90fec000-90ff6000 rw-p 00000000 00:00 0 
90ff6000-90ff7000 ---p 00000000 00:00 0 
90ff7000-90ff8000 ---p 00000000 00:00 0 
90ff8000-910fa000 rw-p 00000000 00:00 0          [stack:12863]
910fa000-910fb000 ---p 00000000 00:00 0 
910fb000-910fc000 ---p 00000000 00:00 0 
910fc000-911fe000 rw-p 00000000 00:00 0          [stack:12862]
911fe000-911ff000 ---p 00000000 00:00 0 
911ff000-91200000 ---p 00000000 00:00 0 
91200000-91302000 rw-p 00000000 00:00 0          [stack:12861]
91319000-9133a000 rw-p 00000000 00:01 394775     /dev/ashmem/dalvik-large object space allocation (deleted)
9133a000-9135b000 rw-p 00000000 00:01 394774     /dev/ashmem/dalvik-large object space allocation (deleted)
9135b000-9137c000 rw-p 00000000 00:01 394773     /dev/ashmem/dalvik-large object space allocation (deleted)
9137c000-9139d000 rw-p 00000000 00:01 394772     /dev/ashmem/dalvik-large object space allocation (deleted)
9139d000-913be000 rw-p 00000000 00:01 394771     /dev/ashmem/dalvik-large object space allocation (deleted)
913be000-913df000 rw-p 00000000 00:01 394770     /dev/ashmem/dalvik-large object space allocation (deleted)
913df000-91400000 rw-p 00000000 00:01 394769     /dev/ashmem/dalvik-large object space allocation (deleted)
91400000-91c02000 rw-p 00000000 00:00 0 
91d00000-91d01000 ---p 00000000 00:00 0 
91d01000-91dfe000 rw-p 00000000 00:00 0          [stack:12851]
91dfe000-91dff000 ---p 00000000 00:00 0 
91dff000-91e00000 ---p 00000000 00:00 0 
91e00000-91f02000 rw-p 00000000 00:00 0          [stack:12848]
91f02000-91f03000 ---p 00000000 00:00 0 
91f03000-91f04000 ---p 00000000 00:00 0 
91f04000-92000000 rw-p 00000000 00:00 0          [stack:12847]
92000000-92804000 rw-p 00000000 00:00 0 
92822000-928e4000 r-xp 00000000 08:13 122887     /data/app/com.bilibili.priconne-1/lib/x86/libcri_mana_vpx.so
928e4000-928e6000 r--p 000c1000 08:13 122887     /data/app/com.bilibili.priconne-1/lib/x86/libcri_mana_vpx.so
928e6000-928e7000 rw-p 000c3000 08:13 122887     /data/app/com.bilibili.priconne-1/lib/x86/libcri_mana_vpx.so
928e7000-929e7000 rw-s 00000000 00:01 387576     /dev/ashmem/AudioFlinger::Client (deleted)
929e7000-929e8000 ---p 00000000 00:00 0 
929e8000-92ae5000 rw-p 00000000 00:00 0          [stack:12846]
92ae5000-92ae6000 ---p 00000000 00:00 0 
92ae6000-92ae7000 ---p 00000000 00:00 0 
92ae7000-92be3000 rw-p 00000000 00:00 0          [stack:12845]
92be3000-92be4000 ---p 00000000 00:00 0 
92be4000-92be5000 ---p 00000000 00:00 0 
92be5000-92ce1000 rw-p 00000000 00:00 0          [stack:12844]
92ce1000-92ce2000 ---p 00000000 00:00 0 
92ce2000-92ce3000 ---p 00000000 00:00 0 
92ce3000-92ddf000 rw-p 00000000 00:00 0          [stack:12843]
92ddf000-92de0000 ---p 00000000 00:00 0 
92de0000-92de1000 ---p 00000000 00:00 0 
92de1000-92edd000 rw-p 00000000 00:00 0          [stack:12842]
92edd000-92ede000 ---p 00000000 00:00 0 
92ede000-92edf000 ---p 00000000 00:00 0 
92edf000-92fdb000 rw-p 00000000 00:00 0          [stack:12841]
92fdb000-92fdc000 ---p 00000000 00:00 0 
92fdc000-92fdd000 ---p 00000000 00:00 0 
92fdd000-930d9000 rw-p 00000000 00:00 0          [stack:12840]
930d9000-930da000 ---p 00000000 00:00 0 
930da000-930db000 ---p 00000000 00:00 0 
930db000-931d7000 rw-p 00000000 00:00 0          [stack:12839]
931d7000-933b4000 r-xp 00000000 08:13 122891     /data/app/com.bilibili.priconne-1/lib/x86/libcri_ware_unity.so
933b4000-933b5000 ---p 00000000 00:00 0 
933b5000-933b8000 r--p 001dd000 08:13 122891     /data/app/com.bilibili.priconne-1/lib/x86/libcri_ware_unity.so
933b8000-933ba000 rw-p 001e0000 08:13 122891     /data/app/com.bilibili.priconne-1/lib/x86/libcri_ware_unity.so
933ba000-94c02000 rw-p 00000000 00:00 0 
94c07000-94c28000 rw-p 00000000 00:01 394768     /dev/ashmem/dalvik-large object space allocation (deleted)
94c28000-94c29000 ---p 00000000 00:00 0 
94c29000-94c2a000 ---p 00000000 00:00 0 
94c2a000-94d26000 rw-p 00000000 00:00 0          [stack:12838]
94d26000-94d27000 ---p 00000000 00:00 0 
94d27000-94e24000 rw-p 00000000 00:00 0          [stack:12837]
94e24000-94e25000 ---p 00000000 00:00 0 
94e25000-94f22000 rw-p 00000000 00:00 0          [stack:12836]
94f22000-94f23000 ---p 00000000 00:00 0 
94f23000-94f24000 ---p 00000000 00:00 0 
94f24000-95020000 rw-p 00000000 00:00 0          [stack:12834]
95020000-95021000 ---p 00000000 00:00 0 
95021000-95022000 ---p 00000000 00:00 0 
95022000-9511e000 rw-p 00000000 00:00 0          [stack:12833]
9511e000-9511f000 ---p 00000000 00:00 0 
9511f000-95120000 ---p 00000000 00:00 0 
95120000-9521c000 rw-p 00000000 00:00 0          [stack:12832]
9521c000-9521d000 ---p 00000000 00:00 0 
9521d000-9531a000 rw-p 00000000 00:00 0          [stack:12831]
9531a000-9531b000 ---p 00000000 00:00 0 
9531b000-95418000 rw-p 00000000 00:00 0          [stack:12830]
95418000-95419000 ---p 00000000 00:00 0 
95419000-95516000 rw-p 00000000 00:00 0          [stack:12829]
95516000-95517000 ---p 00000000 00:00 0 
95517000-95614000 rw-p 00000000 00:00 0          [stack:12828]
95614000-95615000 ---p 00000000 00:00 0 
95615000-95712000 rw-p 00000000 00:00 0          [stack:12827]
95712000-95713000 ---p 00000000 00:00 0 
95713000-95810000 rw-p 00000000 00:00 0          [stack:12826]
95810000-95811000 ---p 00000000 00:00 0 
95811000-9590e000 rw-p 00000000 00:00 0          [stack:12825]
9590e000-9590f000 ---p 00000000 00:00 0 
9590f000-95a0c000 rw-p 00000000 00:00 0          [stack:12824]
95a0c000-95a0d000 ---p 00000000 00:00 0 
95a0d000-95b0a000 rw-p 00000000 00:00 0          [stack:12823]
95b0a000-95b0b000 ---p 00000000 00:00 0 
95b0b000-95b0c000 ---p 00000000 00:00 0 
95b0c000-95c08000 rw-p 00000000 00:00 0          [stack:12822]
95c08000-95c09000 ---p 00000000 00:00 0 
95c09000-95c0a000 ---p 00000000 00:00 0 
95c0a000-95d06000 rw-p 00000000 00:00 0          [stack:12821]
95d06000-95d07000 ---p 00000000 00:00 0 
95d07000-95d08000 ---p 00000000 00:00 0 
95d08000-95e04000 rw-p 00000000 00:00 0          [stack:12820]
95e04000-95e05000 ---p 00000000 00:00 0 
95e05000-95e06000 ---p 00000000 00:00 0 
95e06000-95f02000 rw-p 00000000 00:00 0          [stack:12819]
95f02000-95f03000 ---p 00000000 00:00 0 
95f03000-96000000 rw-p 00000000 00:00 0          [stack:12818]
96000000-96404000 rw-p 00000000 00:00 0 
96404000-96405000 ---p 00000000 00:00 0 
96405000-96502000 rw-p 00000000 00:00 0          [stack:12817]
96502000-96503000 ---p 00000000 00:00 0 
96503000-96600000 rw-p 00000000 00:00 0          [stack:12816]
96600000-96800000 rw-s 00000000 00:0d 9238       /dev/ttyS10
96800000-97400000 rw-p 00000000 00:00 0 
97405000-97426000 rw-p 00000000 00:01 394767     /dev/ashmem/dalvik-large object space allocation (deleted)
97426000-97447000 rw-p 00000000 00:01 394766     /dev/ashmem/dalvik-large object space allocation (deleted)
97447000-9749a000 r--p 00000000 00:16 169        /storage/emulated/0/Android/data/com.bilibili.priconne/files/il2cpp/Resources/mscorlib.dll-resources.dat
9749a000-9749b000 ---p 00000000 00:00 0 
9749b000-97598000 rw-p 00000000 00:00 0          [stack:12814]
97598000-97599000 ---p 00000000 00:00 0 
97599000-97696000 rw-p 00000000 00:00 0          [stack:12813]
97696000-97697000 ---p 00000000 00:00 0 
97697000-97698000 ---p 00000000 00:00 0 
97698000-97794000 rw-p 00000000 00:00 0          [stack:12812]
97794000-98982000 r--p 00000000 00:16 148        /storage/emulated/0/Android/data/com.bilibili.priconne/files/il2cpp/Metadata/global-metadata.dat
98982000-98983000 ---p 00000000 00:00 0 
98983000-98984000 ---p 00000000 00:00 0 
98984000-98a80000 rw-p 00000000 00:00 0          [stack:12807]
98a80000-98a81000 ---p 00000000 00:00 0 
98a81000-98b7e000 rw-p 00000000 00:00 0          [stack:12805]
98b83000-98b85000 rw-p 00000000 00:01 394671     /dev/ashmem/dalvik-indirect ref table (deleted)
98b85000-98b87000 rw-p 00000000 00:00 0 
98b8b000-98b8d000 rw-p 00000000 00:01 392574     /dev/ashmem/dalvik-indirect ref table (deleted)
98b8d000-98b8f000 rw-p 00000000 00:00 0 
98b8f000-98b91000 rw-p 00000000 00:01 394666     /dev/ashmem/dalvik-indirect ref table (deleted)
98b91000-98b93000 rw-p 00000000 00:00 0 
98b95000-98bb6000 rw-p 00000000 00:01 394765     /dev/ashmem/dalvik-large object space allocation (deleted)
98bb6000-98bd7000 rw-p 00000000 00:01 394764     /dev/ashmem/dalvik-large object space allocation (deleted)
98bd7000-98bf8000 rw-p 00000000 00:01 394763     /dev/ashmem/dalvik-large object space allocation (deleted)
98bf8000-98c19000 rw-p 00000000 00:01 394762     /dev/ashmem/dalvik-large object space allocation (deleted)
98c19000-98c3a000 rw-p 00000000 00:01 394761     /dev/ashmem/dalvik-large object space allocation (deleted)
98c3a000-98c5b000 rw-p 00000000 00:01 394760     /dev/ashmem/dalvik-large object space allocation (deleted)
98c5b000-98c7c000 rw-p 00000000 00:01 394759     /dev/ashmem/dalvik-large object space allocation (deleted)
98c7c000-98c7d000 ---p 00000000 00:00 0 
98c7d000-98c7e000 ---p 00000000 00:00 0 
98c7e000-98d80000 rw-p 00000000 00:00 0          [stack:12801]
98d80000-98d82000 rw-p 00000000 00:00 0 
98d82000-98d84000 rw-p 00000000 00:01 390975     /dev/ashmem/dalvik-indirect ref table (deleted)
98d84000-98d86000 rw-p 00000000 00:00 0 
98d86000-98d87000 ---p 00000000 00:00 0 
98d87000-98d88000 ---p 00000000 00:00 0 
98d88000-98e84000 rw-p 00000000 00:00 0          [stack:12803]
98e84000-98e85000 ---p 00000000 00:00 0 
98e85000-98e86000 ---p 00000000 00:00 0 
98e86000-98f88000 rw-p 00000000 00:00 0          [stack:12798]
98f88000-98f89000 ---p 00000000 00:00 0 
98f89000-99086000 rw-p 00000000 00:00 0          [stack:12796]
99086000-99087000 ---p 00000000 00:00 0 
99087000-99088000 ---p 00000000 00:00 0 
99088000-9918a000 rw-p 00000000 00:00 0          [stack:12791]
9918a000-99f9b000 rw-p 00000000 00:01 385880     /dev/ashmem/dalvik-large object space allocation (deleted)
99f9b000-99f9c000 ---p 00000000 00:00 0 
99f9c000-99f9d000 ---p 00000000 00:00 0 
99f9d000-9a09f000 rw-p 00000000 00:00 0          [stack:12789]
9a10b000-9a116000 rw-p 00000000 00:01 404892     /dev/ashmem/dalvik-large object space allocation (deleted)
9a116000-9a121000 rw-p 00000000 00:01 404890     /dev/ashmem/dalvik-large object space allocation (deleted)
9a121000-9a1a1000 r-xp 00000000 08:06 919        /system/lib/libstagefright_soft_avcdec.so
9a1a1000-9a1a2000 r--p 0007f000 08:06 919        /system/lib/libstagefright_soft_avcdec.so
9a1a2000-9a1a3000 rw-p 00080000 08:06 919        /system/lib/libstagefright_soft_avcdec.so
9a1a3000-9a3a3000 rw-s 00000000 00:0d 9238       /dev/ttyS10
9a3a3000-9a3a4000 ---p 00000000 00:00 0 
9a3a4000-9a3a5000 ---p 00000000 00:00 0 
9a3a5000-9a4a7000 rw-p 00000000 00:00 0          [stack:12782]
9a4a7000-9a6a7000 rw-s 00000000 00:0d 9238       /dev/ttyS10
9a6a7000-9a6a8000 ---p 00000000 00:00 0 
9a6a8000-9a6a9000 ---p 00000000 00:00 0 
9a6a9000-9a7ab000 rw-p 00000000 00:00 0          [stack:12777]
9a7ab000-9a7ad000 rw-p 00000000 00:01 389417     /dev/ashmem/dalvik-indirect ref table (deleted)
9a7ad000-9a7af000 rw-p 00000000 00:01 387587     /dev/ashmem/dalvik-indirect ref table (deleted)
9a7af000-9a7b1000 rw-p 00000000 00:00 0 
9a7b1000-9a7b2000 ---p 00000000 00:00 0 
9a7b2000-9a7b3000 ---p 00000000 00:00 0 
9a7b3000-9a8af000 rw-p 00000000 00:00 0          [stack:12779]
9a8af000-9a8b0000 ---p 00000000 00:00 0 
9a8b0000-9a8b1000 ---p 00000000 00:00 0 
9a8b1000-9a9b3000 rw-p 00000000 00:00 0          [stack:12774]
9a9b3000-9a9b4000 ---p 00000000 00:00 0 
9a9b4000-9a9b5000 ---p 00000000 00:00 0 
9a9b5000-9aab7000 rw-p 00000000 00:00 0          [stack:12773]
9aab7000-9aab9000 rw-p 00000000 00:01 393930     /dev/ashmem/dalvik-indirect ref table (deleted)
9aab9000-9aabb000 rw-p 00000000 00:00 0 
9aac1000-9aac3000 rw-p 00000000 00:01 393928     /dev/ashmem/dalvik-indirect ref table (deleted)
9aac3000-9aac5000 rw-p 00000000 00:00 0 
9aac5000-9aac7000 rw-p 00000000 00:01 394665     /dev/ashmem/dalvik-indirect ref table (deleted)
9aac7000-9aac8000 ---p 00000000 00:00 0 
9aac8000-9aac9000 ---p 00000000 00:00 0 
9aac9000-9abcb000 rw-p 00000000 00:00 0          [stack:12771]
9abcb000-9abcd000 rw-p 00000000 00:00 0 
9abcd000-9abcf000 rw-p 00000000 00:01 389416     /dev/ashmem/dalvik-indirect ref table (deleted)
9abcf000-9abd1000 rw-p 00000000 00:00 0 
9abd1000-9abd3000 rw-p 00000000 00:01 415019     /dev/ashmem/dalvik-indirect ref table (deleted)
9abd3000-9abd7000 rw-p 00000000 00:00 0 
9abd7000-9abd9000 rw-p 00000000 00:01 389399     /dev/ashmem/dalvik-indirect ref table (deleted)
9abdb000-9abdd000 rw-p 00000000 00:01 406057     /dev/ashmem/dalvik-indirect ref table (deleted)
9abdd000-9abdf000 rw-p 00000000 00:00 0 
9abdf000-9abe0000 ---p 00000000 00:00 0 
9abe0000-9abe1000 ---p 00000000 00:00 0 
9abe1000-9acdd000 rw-p 00000000 00:00 0          [stack:12994]
9acdd000-9acdf000 rw-p 00000000 00:00 0 
9acdf000-9ace1000 rw-p 00000000 00:01 385927     /dev/ashmem/dalvik-indirect ref table (deleted)
9ace1000-9ace5000 rw-p 00000000 00:00 0 
9ace5000-9ace7000 rw-p 00000000 00:01 390367     /dev/ashmem/dalvik-indirect ref table (deleted)
9ace7000-9ace9000 rw-p 00000000 00:00 0 
9ace9000-9aceb000 rw-p 00000000 00:01 390366     /dev/ashmem/dalvik-indirect ref table (deleted)
9aceb000-9aced000 rw-p 00000000 00:00 0 
9aced000-9acef000 rw-p 00000000 00:01 390365     /dev/ashmem/dalvik-indirect ref table (deleted)
9acef000-9acf1000 rw-p 00000000 00:00 0 
9acf1000-9acf3000 rw-p 00000000 00:01 390364     /dev/ashmem/dalvik-indirect ref table (deleted)
9acf3000-9acf5000 rw-p 00000000 00:00 0 
9acf5000-9acf7000 rw-p 00000000 00:01 390363     /dev/ashmem/dalvik-indirect ref table (deleted)
9acf7000-9acf9000 rw-p 00000000 00:00 0 
9acf9000-9acfb000 rw-p 00000000 00:01 390362     /dev/ashmem/dalvik-indirect ref table (deleted)
9acfb000-9acfd000 rw-p 00000000 00:00 0 
9acfd000-9acff000 rw-p 00000000 00:01 390361     /dev/ashmem/dalvik-indirect ref table (deleted)
9acff000-9ad01000 rw-p 00000000 00:00 0 
9ad01000-9ad03000 rw-p 00000000 00:01 390360     /dev/ashmem/dalvik-indirect ref table (deleted)
9ad03000-9ad05000 rw-p 00000000 00:00 0 
9ad05000-9ad07000 r-xp 00000000 08:06 911        /system/lib/libstagefright_http_support.so
9ad07000-9ad08000 r--p 00001000 08:06 911        /system/lib/libstagefright_http_support.so
9ad08000-9ad09000 rw-p 00002000 08:06 911        /system/lib/libstagefright_http_support.so
9ad09000-9ad0c000 r-xp 00000000 08:06 804        /system/lib/libeffects.so
9ad0c000-9ad0d000 r--p 00002000 08:06 804        /system/lib/libeffects.so
9ad0d000-9ad0e000 rw-p 00003000 08:06 804        /system/lib/libeffects.so
9ad0e000-9ad55000 r-xp 00000000 08:06 967        /system/lib/libwilhelm.so
9ad55000-9ad59000 r--p 00046000 08:06 967        /system/lib/libwilhelm.so
9ad59000-9ad5a000 rw-p 0004a000 08:06 967        /system/lib/libwilhelm.so
9ad5a000-9ad5c000 r-xp 00000000 08:06 755        /system/lib/libOpenSLES.so
9ad5c000-9ad5d000 r--p 00001000 08:06 755        /system/lib/libOpenSLES.so
9ad5d000-9ad5e000 rw-p 00002000 08:06 755        /system/lib/libOpenSLES.so
9ad5f000-9ad61000 rw-p 00000000 00:00 0 
9ad61000-9ad63000 rw-p 00000000 00:01 394661     /dev/ashmem/dalvik-indirect ref table (deleted)
9ad63000-9ad65000 rw-p 00000000 00:00 0 
9ad66000-9ad92000 rw-p 00000000 00:00 0 
9ad93000-9ad95000 rw-p 00000000 00:01 395366     /dev/ashmem/dalvik-indirect ref table (deleted)
9ad95000-9ad97000 rw-p 00000000 00:00 0 
9ad97000-9ad99000 rw-p 00000000 00:01 385860     /dev/ashmem/dalvik-indirect ref table (deleted)
9ad99000-9ada5000 rw-p 00000000 00:00 0 
9ada5000-9ada7000 rw-p 00000000 00:01 385864     /dev/ashmem/dalvik-indirect ref table (deleted)
9ada7000-9ada9000 rw-p 00000000 00:00 0 
9ada9000-9adab000 rw-p 00000000 00:01 387548     /dev/ashmem/dalvik-indirect ref table (deleted)
9adab000-9adad000 rw-p 00000000 00:00 0 
9adae000-9adb0000 rw-p 00000000 00:00 0 
9adb0000-9adb2000 rw-p 00000000 00:01 404910     /dev/ashmem/dalvik-indirect ref table (deleted)
9adb2000-9adb4000 rw-p 00000000 00:01 387547     /dev/ashmem/dalvik-indirect ref table (deleted)
9adb4000-9adb6000 rw-p 00000000 00:00 0 
9adb6000-9adb8000 rw-p 00000000 00:01 392554     /dev/ashmem/dalvik-indirect ref table (deleted)
9adb8000-9adba000 rw-p 00000000 00:00 0 
9adbb000-9adbf000 rw-p 00000000 00:00 0 
9adbf000-9adc1000 rw-p 00000000 00:01 387567     /dev/ashmem/dalvik-indirect ref table (deleted)
9adc1000-9adc3000 rw-p 00000000 00:00 0 
9adc3000-9adc5000 rw-p 00000000 00:01 386848     /dev/ashmem/dalvik-indirect ref table (deleted)
9adc6000-9adc8000 rw-p 00000000 00:01 404909     /dev/ashmem/dalvik-indirect ref table (deleted)
9adc8000-9adca000 rw-p 00000000 00:00 0 
9adcb000-9adcf000 rw-p 00000000 00:00 0 
9adcf000-9add1000 rw-p 00000000 00:01 387546     /dev/ashmem/dalvik-indirect ref table (deleted)
9add1000-9add3000 rw-p 00000000 00:00 0 
9add3000-9add5000 rw-p 00000000 00:01 388499     /dev/ashmem/dalvik-indirect ref table (deleted)
9add5000-9add7000 rw-p 00000000 00:00 0 
9add7000-9add9000 rw-p 00000000 00:01 406054     /dev/ashmem/dalvik-indirect ref table (deleted)
9add9000-9addb000 rw-p 00000000 00:00 0 
9addb000-9ade1000 rw-p 00000000 00:01 404893     /dev/ashmem/dalvik-large object space allocation (deleted)
9ade1000-9ade2000 ---p 00000000 00:00 0 
9ade2000-9ade3000 ---p 00000000 00:00 0 
9ade3000-9aee5000 rw-p 00000000 00:00 0          [stack:12769]
9aee5000-9aee7000 rw-p 00000000 00:01 389896     /dev/ashmem/dalvik-indirect ref table (deleted)
9aee7000-9aeeb000 rw-p 00000000 00:00 0 
9aeeb000-9aeed000 rw-p 00000000 00:01 404908     /dev/ashmem/dalvik-indirect ref table (deleted)
9aeed000-9aef3000 rw-p 00000000 00:01 404891     /dev/ashmem/dalvik-large object space allocation (deleted)
9aef3000-9aef5000 rw-p 00000000 00:01 387536     /dev/ashmem/dalvik-indirect ref table (deleted)
9aef5000-9aef7000 rw-p 00000000 00:00 0 
9aef7000-9aef8000 ---p 00000000 00:00 0 
9aef8000-9aef9000 ---p 00000000 00:00 0 
9aef9000-9affb000 rw-p 00000000 00:00 0          [stack:12760]
9affb000-9affd000 rw-p 00000000 00:01 385800     /dev/ashmem/dalvik-indirect ref table (deleted)
9affd000-9afff000 rw-p 00000000 00:00 0 
9afff000-9b000000 ---p 00000000 00:00 0 
9b000000-9b001000 ---p 00000000 00:00 0 
9b001000-9b103000 rw-p 00000000 00:00 0          [stack:12759]
9b103000-9b107000 rw-p 00000000 00:00 0 
9b107000-9b117000 rw-p 00000000 00:01 404889     /dev/ashmem/dalvik-large object space allocation (deleted)
9b117000-9b118000 ---p 00000000 00:00 0 
9b118000-9b215000 rw-p 00000000 00:00 0          [stack:15028]
9b215000-9b217000 r-xp 00000000 08:13 122888     /data/app/com.bilibili.priconne-1/lib/x86/libbsutils.so
9b217000-9b218000 r--p 00001000 08:13 122888     /data/app/com.bilibili.priconne-1/lib/x86/libbsutils.so
9b218000-9b219000 rw-p 00002000 08:13 122888     /data/app/com.bilibili.priconne-1/lib/x86/libbsutils.so
9b219000-9b21b000 rw-p 00000000 00:01 406051     /dev/ashmem/dalvik-indirect ref table (deleted)
9b21b000-9b226000 rw-p 00000000 00:01 404888     /dev/ashmem/dalvik-large object space allocation (deleted)
9b226000-9b22d000 rw-p 00000000 00:01 404887     /dev/ashmem/dalvik-large object space allocation (deleted)
9b22d000-9b22f000 rw-p 00000000 00:01 387532     /dev/ashmem/dalvik-indirect ref table (deleted)
9b22f000-9b231000 rw-p 00000000 00:00 0 
9b231000-9b232000 ---p 00000000 00:00 0 
9b232000-9b233000 ---p 00000000 00:00 0 
9b233000-9b335000 rw-p 00000000 00:00 0          [stack:12757]
9b335000-9b336000 ---p 00000000 00:00 0 
9b336000-9b337000 ---p 00000000 00:00 0 
9b337000-9b439000 rw-p 00000000 00:00 0          [stack:12754]
9b43a000-9b43f000 rw-p 00000000 00:01 404886     /dev/ashmem/dalvik-large object space allocation (deleted)
9b43f000-9b440000 ---p 00000000 00:00 0 
9b440000-9b441000 ---p 00000000 00:00 0 
9b441000-9b53d000 rw-p 00000000 00:00 0          [stack:15027]
9b53d000-9b53e000 ---p 00000000 00:00 0 
9b53e000-9b53f000 ---p 00000000 00:00 0 
9b53f000-9b641000 rw-p 00000000 00:00 0          [stack:12750]
9b641000-9b642000 ---p 00000000 00:00 0 
9b642000-9b643000 ---p 00000000 00:00 0 
9b643000-9b745000 rw-p 00000000 00:00 0          [stack:12749]
9b745000-9b746000 ---p 00000000 00:00 0 
9b746000-9b747000 ---p 00000000 00:00 0 
9b747000-9b849000 rw-p 00000000 00:00 0          [stack:12747]
9b849000-9b84a000 ---p 00000000 00:00 0 
9b84a000-9b84b000 ---p 00000000 00:00 0 
9b84b000-9b94d000 rw-p 00000000 00:00 0          [stack:12746]
9b94d000-9b94e000 ---p 00000000 00:00 0 
9b94e000-9b94f000 ---p 00000000 00:00 0 
9b94f000-9ba51000 rw-p 00000000 00:00 0          [stack:12744]
9ba51000-9cb05000 r-xp 00000000 08:13 122893     /data/app/com.bilibili.priconne-1/lib/x86/libunity.so
9cb05000-9cb35000 rw-p 010b4000 08:13 122893     /data/app/com.bilibili.priconne-1/lib/x86/libunity.so
9cb35000-9e000000 rw-p 00000000 00:00 0 
9e001000-9e003000 rw-p 00000000 00:01 386820     /dev/ashmem/dalvik-indirect ref table (deleted)
9e003000-9e009000 rw-p 00000000 00:00 0 
9e009000-9e00b000 rw-p 00000000 00:01 388540     /dev/ashmem/dalvik-indirect ref table (deleted)
9e00b000-9e017000 r-xp 00000000 08:06 737        /system/lib/hw/gralloc.gmin.so
9e017000-9e018000 r--p 0000b000 08:06 737        /system/lib/hw/gralloc.gmin.so
9e018000-9e019000 rw-p 0000c000 08:06 737        /system/lib/hw/gralloc.gmin.so
9e019000-9e01d000 rw-p 00000000 00:01 404885     /dev/ashmem/dalvik-large object space allocation (deleted)
9e01d000-9e01f000 rw-p 00000000 00:01 388494     /dev/ashmem/dalvik-indirect ref table (deleted)
9e01f000-9e021000 rw-p 00000000 00:00 0 
9e021000-9e023000 rw-p 00000000 00:01 388492     /dev/ashmem/dalvik-indirect ref table (deleted)
9e023000-9e025000 rw-p 00000000 00:00 0 
9e025000-9e027000 rw-p 00000000 00:01 388487     /dev/ashmem/dalvik-indirect ref table (deleted)
9e027000-9e028000 r--p 00000000 00:00 0 
9e028000-9e02a000 rw-p 00000000 00:00 0 
9e02a000-9e02c000 rw-p 00000000 00:01 387558     /dev/ashmem/dalvik-indirect ref table (deleted)
9e02d000-9e02f000 rw-p 00000000 00:01 392587     /dev/ashmem/dalvik-indirect ref table (deleted)
9e02f000-9e031000 rw-p 00000000 00:00 0 
9e031000-9e032000 ---p 00000000 00:00 0 
9e032000-9e033000 ---p 00000000 00:00 0 
9e033000-9e135000 rw-p 00000000 00:00 0          [stack:12742]
9e135000-9e164000 rwxp 00000000 08:13 122897     /data/app/com.bilibili.priconne-1/lib/x86/libil2cpp.so
9e164000-9e16a000 r-xp 0002f000 08:13 122897     /data/app/com.bilibili.priconne-1/lib/x86/libil2cpp.so
9e16a000-9e16b000 r--p 00034000 08:13 122897     /data/app/com.bilibili.priconne-1/lib/x86/libil2cpp.so
9e16b000-9e16d000 rw-p 00035000 08:13 122897     /data/app/com.bilibili.priconne-1/lib/x86/libil2cpp.so
9e16d000-a2953000 rwxp 00037000 08:13 122897     /data/app/com.bilibili.priconne-1/lib/x86/libil2cpp.so
a2953000-a2c42000 rwxp 00000000 00:00 0 
a2c42000-a2c43000 ---p 00000000 00:00 0 
a2c43000-a2c44000 ---p 00000000 00:00 0 
a2c44000-a2d40000 rw-p 00000000 00:00 0          [stack:12739]
a2d40000-a2d48000 rw-p 00000000 00:00 0 
a2d48000-a2d4a000 rw-p 00000000 00:01 406050     /dev/ashmem/dalvik-indirect ref table (deleted)
a2d4a000-a2d4e000 rw-p 00000000 00:00 0 
a2d4e000-a2d53000 rw-p 00000000 00:01 395415     /dev/ashmem/dalvik-large object space allocation (deleted)
a2d53000-a2d55000 rw-p 00000000 00:01 406049     /dev/ashmem/dalvik-indirect ref table (deleted)
a2d55000-a2d57000 rw-p 00000000 00:01 393939     /dev/ashmem/dalvik-indirect ref table (deleted)
a2d57000-a2d78000 rw-p 00000000 00:01 394758     /dev/ashmem/dalvik-large object space allocation (deleted)
a2d78000-a2d99000 rw-p 00000000 00:01 394757     /dev/ashmem/dalvik-large object space allocation (deleted)
a2d99000-a2dba000 rw-p 00000000 00:01 394756     /dev/ashmem/dalvik-large object space allocation (deleted)
a2dba000-a2ddb000 rw-p 00000000 00:01 394755     /dev/ashmem/dalvik-large object space allocation (deleted)
a2ddb000-a2dfc000 rw-p 00000000 00:01 394754     /dev/ashmem/dalvik-large object space allocation (deleted)
a2dfc000-a2e1d000 rw-p 00000000 00:01 394753     /dev/ashmem/dalvik-large object space allocation (deleted)
a2e1d000-a2e3e000 rw-p 00000000 00:01 394752     /dev/ashmem/dalvik-large object space allocation (deleted)
a2e3e000-a31a5000 r-xp 00000000 08:13 122892     /data/app/com.bilibili.priconne-1/lib/x86/libNetHTProtect.so
a31a5000-a31a6000 ---p 00000000 00:00 0 
a31a6000-a31a9000 r--p 00367000 08:13 122892     /data/app/com.bilibili.priconne-1/lib/x86/libNetHTProtect.so
a31a9000-a321b000 rw-p 0036a000 08:13 122892     /data/app/com.bilibili.priconne-1/lib/x86/libNetHTProtect.so
a321b000-a3227000 rw-p 00000000 00:00 0 
a3227000-a324b000 rwxp 00000000 08:13 122885     /data/app/com.bilibili.priconne-1/lib/x86/libmain.so
a324b000-a324e000 r-xp 00024000 08:13 122885     /data/app/com.bilibili.priconne-1/lib/x86/libmain.so
a324e000-a324f000 r--p 00026000 08:13 122885     /data/app/com.bilibili.priconne-1/lib/x86/libmain.so
a324f000-a3250000 rw-p 00027000 08:13 122885     /data/app/com.bilibili.priconne-1/lib/x86/libmain.so
a3250000-a3253000 rwxp 00028000 08:13 122885     /data/app/com.bilibili.priconne-1/lib/x86/libmain.so
a3253000-a3254000 rwxp 00000000 00:00 0 
a3254000-a3814000 r--p 00000000 08:13 306        /data/dalvik-cache/x86/data@app@com.bilibili.priconne-1@base.apk@classes.dex
a3814000-a3e1d000 r-xp 005c0000 08:13 306        /data/dalvik-cache/x86/data@app@com.bilibili.priconne-1@base.apk@classes.dex
a3e1d000-a3e1e000 rw-p 00bc9000 08:13 306        /data/dalvik-cache/x86/data@app@com.bilibili.priconne-1@base.apk@classes.dex
a3e1e000-a3fb8000 r--s 5a0b3000 08:13 227        /data/app/com.bilibili.priconne-1/base.apk
a3fb8000-a3fb9000 ---p 00000000 00:00 0 
a3fb9000-a3fba000 ---p 00000000 00:00 0 
a3fba000-a40b6000 rw-p 00000000 00:00 0          [stack:12736]
a40b6000-a40b7000 ---p 00000000 00:00 0 
a40b7000-a40b8000 ---p 00000000 00:00 0 
a40b8000-a41b4000 rw-p 00000000 00:00 0          [stack:12735]
a41b4000-a41b5000 ---p 00000000 00:00 0 
a41b5000-a41b6000 ---p 00000000 00:00 0 
a41b6000-a42b8000 rw-p 00000000 00:00 0          [stack:12734]
a42b8000-a42b9000 ---p 00000000 00:00 0 
a42b9000-a42ba000 ---p 00000000 00:00 0 
a42ba000-a43bc000 rw-p 00000000 00:00 0          [stack:12733]
a43bc000-a43bd000 ---p 00000000 00:00 0 
a43bd000-a43be000 ---p 00000000 00:00 0 
a43be000-a44c0000 rw-p 00000000 00:00 0          [stack:12732]
a44c0000-a48c0000 rw-p 00000000 00:01 7025       /dev/ashmem/dalvik-allocspace main rosalloc space mark-bitmap 3 (deleted)
a48c0000-a7bbd000 r-xp 00000000 08:06 963        /system/lib/libwebviewchromium.so
a7bbd000-a7bbe000 ---p 00000000 00:00 0 
a7bbe000-a7d59000 r--p 00000000 08:13 44         /data/misc/shared_relro/libwebviewchromium32.relro
a7d59000-a7d74000 rw-p 03498000 08:06 963        /system/lib/libwebviewchromium.so
a7d74000-a7eea000 rw-p 00000000 00:00 0 
a7eea000-aacc0000 ---p 00000000 00:00 0 
aacc0000-aacc2000 r-xp 00000000 08:06 964        /system/lib/libwebviewchromium_loader.so
aacc2000-aacc3000 r--p 00001000 08:06 964        /system/lib/libwebviewchromium_loader.so
aacc3000-aacc4000 rw-p 00002000 08:06 964        /system/lib/libwebviewchromium_loader.so
aacc4000-aacc5000 r-xp 00000000 08:06 848        /system/lib/libjnigraphics.so
aacc5000-aacc6000 r--p 00000000 08:06 848        /system/lib/libjnigraphics.so
aacc6000-aacc7000 rw-p 00001000 08:06 848        /system/lib/libjnigraphics.so
aacc7000-aacd0000 r-xp 00000000 08:06 796        /system/lib/libcompiler_rt.so
aacd0000-aacd1000 r--p 00008000 08:06 796        /system/lib/libcompiler_rt.so
aacd1000-aacd2000 rw-p 00009000 08:06 796        /system/lib/libcompiler_rt.so
aacd2000-aacd3000 r--p 00000000 00:00 0 
aacd3000-aace8000 r-xp 00000000 08:06 764        /system/lib/libandroid.so
aace8000-aace9000 ---p 00000000 00:00 0 
aace9000-aaceb000 r--p 00015000 08:06 764        /system/lib/libandroid.so
aaceb000-aacec000 rw-p 00017000 08:06 764        /system/lib/libandroid.so
aacec000-aad05000 r-xp 00000000 08:06 729        /system/lib/egl/libGLESv2_adreno.so
aad05000-aad07000 r--p 00018000 08:06 729        /system/lib/egl/libGLESv2_adreno.so
aad07000-aad08000 rw-p 0001a000 08:06 729        /system/lib/egl/libGLESv2_adreno.so
aad08000-aad19000 r-xp 00000000 08:06 728        /system/lib/egl/libGLESv1_CM_adreno.so
aad19000-aad1a000 r--p 00010000 08:06 728        /system/lib/egl/libGLESv1_CM_adreno.so
aad1a000-aad1b000 rw-p 00011000 08:06 728        /system/lib/egl/libGLESv1_CM_adreno.so
aad1c000-aad24000 r-xp 00000000 08:06 763        /system/lib/lib_renderControl_enc.so
aad24000-aad25000 r--p 00007000 08:06 763        /system/lib/lib_renderControl_enc.so
aad25000-aad26000 rw-p 00008000 08:06 763        /system/lib/lib_renderControl_enc.so
aad26000-aad2f000 r-xp 00000000 08:06 757        /system/lib/libOpenglSystemCommon.so
aad2f000-aad30000 r--p 00008000 08:06 757        /system/lib/libOpenglSystemCommon.so
aad30000-aad31000 rw-p 00009000 08:06 757        /system/lib/libOpenglSystemCommon.so
aad31000-aad5e000 r-xp 00000000 08:06 756        /system/lib/libOpenglCodecCommon.so
aad5e000-aad5f000 r--p 0002c000 08:06 756        /system/lib/libOpenglCodecCommon.so
aad5f000-aad60000 rw-p 0002d000 08:06 756        /system/lib/libOpenglCodecCommon.so
aad60000-aadca000 r-xp 00000000 08:06 751        /system/lib/libGLESv2_enc.so
aadca000-aadcb000 ---p 00000000 00:00 0 
aadcb000-aadcc000 r--p 0006a000 08:06 751        /system/lib/libGLESv2_enc.so
aadcc000-aadcd000 rw-p 0006b000 08:06 751        /system/lib/libGLESv2_enc.so
aadcd000-aadfc000 r-xp 00000000 08:06 749        /system/lib/libGLESv1_enc.so
aadfc000-aadfd000 ---p 00000000 00:00 0 
aadfd000-aadfe000 r--p 0002f000 08:06 749        /system/lib/libGLESv1_enc.so
aadfe000-aadff000 rw-p 00030000 08:06 749        /system/lib/libGLESv1_enc.so
aadff000-aae1a000 r-xp 00000000 08:06 726        /system/lib/egl/libEGL_adreno.so
aae1a000-aae1b000 r--p 0001a000 08:06 726        /system/lib/egl/libEGL_adreno.so
aae1b000-aae1c000 rw-p 0001b000 08:06 726        /system/lib/egl/libEGL_adreno.so
aae1c000-aaf5c000 r--s 00323000 08:06 556        /system/framework/framework-res.apk
aaf5c000-aaf97000 r--s 00513000 08:06 556        /system/framework/framework-res.apk
aaf97000-ab010000 r--s 00000000 08:06 1120       /system/usr/share/zoneinfo/tzdata
ab010000-ab037000 r-xp 00000000 08:06 837        /system/lib/libjavacrypto.so
ab037000-ab038000 ---p 00000000 00:00 0 
ab038000-ab039000 r--p 00027000 08:06 837        /system/lib/libjavacrypto.so
ab039000-ab03a000 rw-p 00028000 08:06 837        /system/lib/libjavacrypto.so
ab03a000-ab045000 r-xp 00000000 08:06 887        /system/lib/librs_jni.so
ab045000-ab046000 ---p 00000000 00:00 0 
ab046000-ab047000 r--p 0000b000 08:06 887        /system/lib/librs_jni.so
ab047000-ab048000 rw-p 0000c000 08:06 887        /system/lib/librs_jni.so
ab048000-ab04e000 r-xp 00000000 08:06 771        /system/lib/libaudioeffect_jni.so
ab04e000-ab04f000 ---p 00000000 00:00 0 
ab04f000-ab050000 r--p 00006000 08:06 771        /system/lib/libaudioeffect_jni.so
ab050000-ab051000 rw-p 00007000 08:06 771        /system/lib/libaudioeffect_jni.so
ab051000-ab052000 r--p 00000000 00:00 0 
ab052000-ab055000 r-xp 00000000 08:06 897        /system/lib/libsoundpool.so
ab055000-ab056000 r--p 00002000 08:06 897        /system/lib/libsoundpool.so
ab056000-ab057000 rw-p 00003000 08:06 897        /system/lib/libsoundpool.so
ab057000-ab071000 r-xp 00000000 08:06 944        /system/lib/libswresample.so
ab071000-ab073000 r--p 00019000 08:06 944        /system/lib/libswresample.so
ab073000-ab074000 rw-p 0001b000 08:06 944        /system/lib/libswresample.so
ab074000-ab07c000 r-xp 00000000 08:06 817        /system/lib/libffmpeg_utils.so
ab07c000-ab07d000 r--p 00007000 08:06 817        /system/lib/libffmpeg_utils.so
ab07d000-ab07e000 rw-p 00008000 08:06 817        /system/lib/libffmpeg_utils.so
ab07e000-ab0db000 r-xp 00000000 08:06 780        /system/lib/libavutil.so
ab0db000-ab0df000 r--p 0005c000 08:06 780        /system/lib/libavutil.so
ab0df000-ab0e0000 rw-p 00060000 08:06 780        /system/lib/libavutil.so
ab0e0000-ab0f3000 rw-p 00000000 00:00 0 
ab0f3000-ab2fa000 r-xp 00000000 08:06 779        /system/lib/libavformat.so
ab2fa000-ab2fb000 ---p 00000000 00:00 0 
ab2fb000-ab309000 r--p 00207000 08:06 779        /system/lib/libavformat.so
ab309000-ab314000 rw-p 00215000 08:06 779        /system/lib/libavformat.so
ab314000-abd9f000 r-xp 00000000 08:06 778        /system/lib/libavcodec.so
abd9f000-abdb9000 r--p 00a8a000 08:06 778        /system/lib/libavcodec.so
abdb9000-abdcb000 rw-p 00aa4000 08:06 778        /system/lib/libavcodec.so
abdcb000-ac41a000 rw-p 00000000 00:00 0 
ac41a000-ac428000 r-xp 00000000 08:06 746        /system/lib/libFFmpegExtractor.so
ac428000-ac429000 r--p 0000d000 08:06 746        /system/lib/libFFmpegExtractor.so
ac429000-ac42a000 rw-p 0000e000 08:06 746        /system/lib/libFFmpegExtractor.so
ac42a000-ac44c000 r-xp 00000000 08:06 961        /system/lib/libvorbisidec.so
ac44c000-ac44d000 r--p 00021000 08:06 961        /system/lib/libvorbisidec.so
ac44d000-ac44e000 rw-p 00022000 08:06 961        /system/lib/libvorbisidec.so
ac44e000-ac451000 r-xp 00000000 08:06 938        /system/lib/libstagefright_yuv.so
ac451000-ac452000 r--p 00002000 08:06 938        /system/lib/libstagefright_yuv.so
ac452000-ac453000 rw-p 00003000 08:06 938        /system/lib/libstagefright_yuv.so
ac453000-ac487000 r-xp 00000000 08:06 913        /system/lib/libstagefright_omx.so
ac487000-ac48a000 r--p 00033000 08:06 913        /system/lib/libstagefright_omx.so
ac48a000-ac48b000 rw-p 00036000 08:06 913        /system/lib/libstagefright_omx.so
ac48b000-ac48c000 r-xp 00000000 08:06 909        /system/lib/libstagefright_enc_common.so
ac48c000-ac48d000 r--p 00000000 08:06 909        /system/lib/libstagefright_enc_common.so
ac48d000-ac48e000 rw-p 00001000 08:06 909        /system/lib/libstagefright_enc_common.so
ac48e000-ac496000 r-xp 00000000 08:06 908        /system/lib/libstagefright_avc_common.so
ac496000-ac497000 r--p 00007000 08:06 908        /system/lib/libstagefright_avc_common.so
ac497000-ac498000 rw-p 00008000 08:06 908        /system/lib/libstagefright_avc_common.so
ac498000-ac499000 r--p 00000000 00:00 0 
ac499000-ac4e7000 r-xp 00000000 08:06 873        /system/lib/libopus.so
ac4e7000-ac4e8000 ---p 00000000 00:00 0 
ac4e8000-ac4e9000 r--p 0004e000 08:06 873        /system/lib/libopus.so
ac4e9000-ac4ea000 rw-p 0004f000 08:06 873        /system/lib/libopus.so
ac4ea000-ac511000 r-xp 00000000 08:06 802        /system/lib/libdrmframework.so
ac511000-ac515000 r--p 00026000 08:06 802        /system/lib/libdrmframework.so
ac515000-ac516000 rw-p 0002a000 08:06 802        /system/lib/libdrmframework.so
ac516000-ac527000 r-xp 00000000 08:06 907        /system/lib/libstagefright_amrnb_common.so
ac527000-ac528000 r--p 00010000 08:06 907        /system/lib/libstagefright_amrnb_common.so
ac528000-ac529000 rw-p 00011000 08:06 907        /system/lib/libstagefright_amrnb_common.so
ac529000-ac6e1000 r-xp 00000000 08:06 906        /system/lib/libstagefright.so
ac6e1000-ac6eb000 r--p 001b7000 08:06 906        /system/lib/libstagefright.so
ac6eb000-ac6ec000 rw-p 001c1000 08:06 906        /system/lib/libstagefright.so
ac6ec000-ac709000 r-xp 00000000 08:06 863        /system/lib/libmtp.so
ac709000-ac70a000 ---p 00000000 00:00 0 
ac70a000-ac70c000 r--p 0001d000 08:06 863        /system/lib/libmtp.so
ac70c000-ac70d000 rw-p 0001f000 08:06 863        /system/lib/libmtp.so
ac70d000-ac71a000 r-xp 00000000 08:06 838        /system/lib/libjhead.so
ac71a000-ac71b000 ---p 00000000 00:00 0 
ac71b000-ac71c000 r--p 0000d000 08:06 838        /system/lib/libjhead.so
ac71c000-ac71d000 rw-p 0000e000 08:06 838        /system/lib/libjhead.so
ac71d000-ac71e000 rw-p 00000000 00:00 0 
ac71e000-ac745000 r-xp 00000000 08:06 806        /system/lib/libexif.so
ac745000-ac746000 ---p 00000000 00:00 0 
ac746000-ac752000 r--p 00027000 08:06 806        /system/lib/libexif.so
ac752000-ac753000 rw-p 00033000 08:06 806        /system/lib/libexif.so
ac753000-ac7bb000 r-xp 00000000 08:06 857        /system/lib/libmedia_jni.so
ac7bb000-ac7bc000 ---p 00000000 00:00 0 
ac7bc000-ac7bf000 r--p 00068000 08:06 857        /system/lib/libmedia_jni.so
ac7bf000-ac7c0000 rw-p 0006b000 08:06 857        /system/lib/libmedia_jni.so
ac7c0000-ac7c1000 r--p 00000000 00:00 0 
ac7c1000-ac7cb000 r--p 00000000 08:06 447        /system/fonts/CarroisGothicSC-Regular.ttf
ac7cb000-ac7e8000 r--p 00000000 08:06 451        /system/fonts/DancingScript-Bold.ttf
ac7e8000-ac805000 r--p 00000000 08:06 452        /system/fonts/DancingScript-Regular.ttf
ac805000-ac814000 r--p 00000000 08:06 449        /system/fonts/ComingSoon.ttf
ac814000-ac825000 r--p 00000000 08:06 450        /system/fonts/CutiveMono.ttf
ac825000-ac840000 r--p 00000000 08:06 456        /system/fonts/DroidSansMono.ttf
ac840000-ac880000 r--p 00000000 08:06 514        /system/fonts/NotoSerif-BoldItalic.ttf
ac880000-ac8bd000 r--p 00000000 08:06 515        /system/fonts/NotoSerif-Italic.ttf
ac8bd000-ac8fa000 r--p 00000000 08:06 513        /system/fonts/NotoSerif-Bold.ttf
ac8fa000-ac937000 r--p 00000000 08:06 516        /system/fonts/NotoSerif-Regular.ttf
ac937000-ac977000 r--p 00000000 08:06 530        /system/fonts/RobotoCondensed-BoldItalic.ttf
ac977000-ac9b2000 r--p 00000000 08:06 529        /system/fonts/RobotoCondensed-Bold.ttf
ac9b2000-ac9f2000 r--p 00000000 08:06 531        /system/fonts/RobotoCondensed-Italic.ttf
ac9f2000-aca2d000 r--p 00000000 08:06 534        /system/fonts/RobotoCondensed-Regular.ttf
aca2d000-aca6e000 r--p 00000000 08:06 533        /system/fonts/RobotoCondensed-LightItalic.ttf
aca6e000-acaa9000 r--p 00000000 08:06 532        /system/fonts/RobotoCondensed-Light.ttf
acaa9000-acd1a000 r--p 00000000 08:06 457        /system/fonts/MTLmr3m.ttf
acd1a000-ad0f3000 r--p 00000000 08:06 455        /system/fonts/DroidSansFallback.ttf
ad0f3000-ad248000 r--p 00000000 08:06 459        /system/fonts/NotoColorEmoji.ttf
ad248000-ad269000 r--p 00000000 08:06 500        /system/fonts/NotoSansSymbols-Regular-Subsetted.ttf
ad269000-ad3a4000 r--p 00000000 08:06 458        /system/fonts/NanumGothic.ttf
ad3a4000-ad3bc000 r--p 00000000 08:06 498        /system/fonts/NotoSansMyanmarUI-Bold.ttf
ad3bc000-ad3d3000 r--p 00000000 08:06 499        /system/fonts/NotoSansMyanmarUI-Regular.ttf
ad3d3000-ad3ed000 r--p 00000000 08:06 496        /system/fonts/NotoSansMyanmar-Bold.ttf
ad3ed000-ad408000 r--p 00000000 08:06 497        /system/fonts/NotoSansMyanmar-Regular.ttf
ad408000-ad410000 r--p 00000000 08:06 490        /system/fonts/NotoSansLaoUI-Bold.ttf
ad410000-ad418000 r--p 00000000 08:06 491        /system/fonts/NotoSansLaoUI-Regular.ttf
ad418000-ad420000 r--p 00000000 08:06 488        /system/fonts/NotoSansLao-Bold.ttf
ad420000-ad428000 r--p 00000000 08:06 489        /system/fonts/NotoSansLao-Regular.ttf
ad428000-ad431000 r--p 00000000 08:06 486        /system/fonts/NotoSansKhmerUI-Bold.ttf
ad431000-ad43b000 r--p 00000000 08:06 487        /system/fonts/NotoSansKhmerUI-Regular.ttf
ad43b000-ad444000 r--p 00000000 08:06 484        /system/fonts/NotoSansKhmer-Bold.ttf
ad444000-ad44d000 r--p 00000000 08:06 485        /system/fonts/NotoSansKhmer-Regular.ttf
ad44d000-ad461000 r--p 00000000 08:06 482        /system/fonts/NotoSansKannadaUI-Bold.ttf
ad461000-ad475000 r--p 00000000 08:06 483        /system/fonts/NotoSansKannadaUI-Regular.ttf
ad475000-ad489000 r--p 00000000 08:06 480        /system/fonts/NotoSansKannada-Bold.ttf
ad489000-ad49d000 r--p 00000000 08:06 481        /system/fonts/NotoSansKannada-Regular.ttf
ad49d000-ad4b8000 r--p 00000000 08:06 507        /system/fonts/NotoSansTeluguUI-Bold.ttf
ad4b8000-ad4d4000 r--p 00000000 08:06 508        /system/fonts/NotoSansTeluguUI-Regular.ttf
ad4d4000-ad4ef000 r--p 00000000 08:06 505        /system/fonts/NotoSansTelugu-Bold.ttf
ad4ef000-ad50a000 r--p 00000000 08:06 506        /system/fonts/NotoSansTelugu-Regular.ttf
ad50a000-ad524000 r--p 00000000 08:06 468        /system/fonts/NotoSansBengaliUI-Bold.ttf
ad524000-ad53f000 r--p 00000000 08:06 469        /system/fonts/NotoSansBengaliUI-Regular.ttf
ad53f000-ad557000 r--p 00000000 08:06 466        /system/fonts/NotoSansBengali-Bold.ttf
ad557000-ad570000 r--p 00000000 08:06 467        /system/fonts/NotoSansBengali-Regular.ttf
ad570000-ad57f000 r--p 00000000 08:06 494        /system/fonts/NotoSansMalayalamUI-Bold.ttf
ad57f000-ad58e000 r--p 00000000 08:06 495        /system/fonts/NotoSansMalayalamUI-Regular.ttf
ad58e000-ad59c000 r--p 00000000 08:06 492        /system/fonts/NotoSansMalayalam-Bold.ttf
ad59c000-ad5aa000 r--p 00000000 08:06 493        /system/fonts/NotoSansMalayalam-Regular.ttf
ad5aa000-ad5b3000 r--p 00000000 08:06 503        /system/fonts/NotoSansTamilUI-Bold.ttf
ad5b3000-ad5bc000 r--p 00000000 08:06 504        /system/fonts/NotoSansTamilUI-Regular.ttf
ad5bc000-ad5c5000 r--p 00000000 08:06 501        /system/fonts/NotoSansTamil-Bold.ttf
ad5c5000-ad5ce000 r--p 00000000 08:06 502        /system/fonts/NotoSansTamil-Regular.ttf
ad5ce000-ad5ea000 r--p 00000000 08:06 472        /system/fonts/NotoSansDevanagariUI-Bold.ttf
ad5ea000-ad608000 r--p 00000000 08:06 473        /system/fonts/NotoSansDevanagariUI-Regular.ttf
ad608000-ad626000 r--p 00000000 08:06 470        /system/fonts/NotoSansDevanagari-Bold.ttf
ad626000-ad645000 r--p 00000000 08:06 471        /system/fonts/NotoSansDevanagari-Regular.ttf
ad645000-ad64a000 r--p 00000000 08:06 476        /system/fonts/NotoSansGeorgian-Bold.ttf
ad64a000-ad64f000 r--p 00000000 08:06 477        /system/fonts/NotoSansGeorgian-Regular.ttf
ad64f000-ad653000 r--p 00000000 08:06 464        /system/fonts/NotoSansArmenian-Bold.ttf
ad653000-ad658000 r--p 00000000 08:06 511        /system/fonts/NotoSansThaiUI-Bold.ttf
ad658000-ad65e000 r--p 00000000 08:06 512        /system/fonts/NotoSansThaiUI-Regular.ttf
ad65e000-ad663000 r--p 00000000 08:06 509        /system/fonts/NotoSansThai-Bold.ttf
ad663000-ad669000 r--p 00000000 08:06 510        /system/fonts/NotoSansThai-Regular.ttf
ad669000-ad66e000 r--p 00000000 08:06 478        /system/fonts/NotoSansHebrew-Bold.ttf
ad66e000-ad691000 r--p 00000000 08:06 474        /system/fonts/NotoSansEthiopic-Bold.ttf
ad691000-ad6b4000 r--p 00000000 08:06 475        /system/fonts/NotoSansEthiopic-Regular.ttf
ad6b4000-ad6d0000 r--p 00000000 08:06 462        /system/fonts/NotoNaskhUI-Bold.ttf
ad6d0000-ad6ed000 r--p 00000000 08:06 463        /system/fonts/NotoNaskhUI-Regular.ttf
ad6ed000-ad709000 r--p 00000000 08:06 460        /system/fonts/NotoNaskh-Bold.ttf
ad709000-ad726000 r--p 00000000 08:06 461        /system/fonts/NotoNaskh-Regular.ttf
ad726000-ad767000 r--p 00000000 08:06 520        /system/fonts/Roboto-BoldItalic.ttf
ad767000-ad7a3000 r--p 00000000 08:06 519        /system/fonts/Roboto-Bold.ttf
ad7a3000-ad7e4000 r--p 00000000 08:06 518        /system/fonts/Roboto-BlackItalic.ttf
ad7e4000-ad820000 r--p 00000000 08:06 517        /system/fonts/Roboto-Black.ttf
ad820000-ad861000 r--p 00000000 08:06 525        /system/fonts/Roboto-MediumItalic.ttf
ad861000-ad89c000 r--p 00000000 08:06 524        /system/fonts/Roboto-Medium.ttf
ad89c000-ad8dd000 r--p 00000000 08:06 521        /system/fonts/Roboto-Italic.ttf
ad8dd000-ad918000 r--p 00000000 08:06 526        /system/fonts/Roboto-Regular.ttf
ad918000-ad959000 r--p 00000000 08:06 523        /system/fonts/Roboto-LightItalic.ttf
ad959000-ad995000 r--p 00000000 08:06 522        /system/fonts/Roboto-Light.ttf
ad995000-ad9d7000 r--p 00000000 08:06 528        /system/fonts/Roboto-ThinItalic.ttf
ad9d7000-ada14000 r--p 00000000 08:06 527        /system/fonts/Roboto-Thin.ttf
ada14000-aebf0000 r--s 00000000 08:06 1069       /system/usr/icu/icudt53l.dat
aebf0000-aebf2000 rw-p 00000000 00:00 0 
aebf2000-aebf4000 rw-p 00000000 00:01 388485     /dev/ashmem/dalvik-indirect ref table (deleted)
aebf4000-aebfc000 rw-p 00000000 00:00 0 
aebfc000-aebfe000 rw-p 00000000 00:01 385869     /dev/ashmem/dalvik-indirect ref table (deleted)
aebfe000-aec00000 rw-p 00000000 00:00 0 
aec00000-af000000 rw-p 00000000 00:01 7024       /dev/ashmem/dalvik-allocspace main rosalloc space live-bitmap 3 (deleted)
af000000-af400000 rw-p 00000000 00:00 0 
af400000-af404000 r--p 00000000 08:06 465        /system/fonts/NotoSansArmenian-Regular.ttf
af404000-af409000 r--p 00000000 08:06 479        /system/fonts/NotoSansHebrew-Regular.ttf
af409000-af507000 r--p 00000000 00:0d 9375       /dev/binder
af507000-af517000 rw-p 00000000 00:01 7023       /dev/ashmem/dalvik-rosalloc page map (deleted)
af517000-b06f3000 r--s 00000000 08:06 1069       /system/usr/icu/icudt53l.dat
b06f3000-b075c000 r-xp 00000000 08:06 836        /system/lib/libjavacore.so
b075c000-b075d000 ---p 00000000 00:00 0 
b075d000-b075e000 r--p 00069000 08:06 836        /system/lib/libjavacore.so
b075e000-b0760000 rw-p 0006a000 08:06 836        /system/lib/libjavacore.so
b0760000-b0828000 rw-p 00000000 00:01 7393       /dev/ashmem/dalvik-indirect ref table (deleted)
b0828000-b08f0000 rw-p 00000000 00:01 7392       /dev/ashmem/dalvik-indirect ref table (deleted)
b08f0000-b10f1000 rw-p 00000000 00:01 7385       /dev/ashmem/dalvik-live stack (deleted)
b10f1000-b18f2000 rw-p 00000000 00:01 7384       /dev/ashmem/dalvik-allocation stack (deleted)
b18f2000-b1932000 rw-p 00000000 00:01 7383       /dev/ashmem/dalvik-mark stack (deleted)
b1932000-b25cd000 rw-p 00000000 00:01 7382       /dev/ashmem/dalvik-card table (deleted)
b25cd000-b25ed000 rw-p 00000000 00:01 7381       /dev/ashmem/dalvik-large marked objects (deleted)
b25ed000-b29ed000 rw-p 00000000 00:01 7379       /dev/ashmem/dalvik-allocspace main rosalloc space 1 mark-bitmap 2 (deleted)
b29ed000-b2ded000 rw-p 00000000 00:01 7378       /dev/ashmem/dalvik-allocspace main rosalloc space 1 live-bitmap 2 (deleted)
b2ded000-b2def000 rw-p 00000000 00:01 386819     /dev/ashmem/dalvik-indirect ref table (deleted)
b2def000-b2df1000 rw-p 00000000 00:00 0 
b2df1000-b2df2000 rw-s 00000000 00:01 385920     /dev/zero (deleted)
b2df2000-b2df3000 r--p 00000000 00:00 0 
b2df3000-b2df5000 rw-p 00000000 00:01 386818     /dev/ashmem/dalvik-indirect ref table (deleted)
b2df5000-b2dfb000 rw-p 00000000 00:00 0 
b2dfb000-b2dfc000 r--p 00000000 08:13 306        /data/dalvik-cache/x86/data@app@com.bilibili.priconne-1@base.apk@classes.dex
b2dfc000-b2e0d000 r--s 579f2000 08:13 227        /data/app/com.bilibili.priconne-1/base.apk
b2e0d000-b2e0f000 rw-p 00000000 00:01 381925     /dev/ashmem/dalvik-indirect ref table (deleted)
b2e0f000-b2e11000 rw-p 00000000 00:00 0 
b2e11000-b2e13000 rw-p 00000000 00:01 386806     /dev/ashmem/dalvik-indirect ref table (deleted)
b2e13000-b2e15000 rw-p 00000000 00:00 0 
b2e15000-b2e17000 rw-p 00000000 00:01 386805     /dev/ashmem/dalvik-indirect ref table (deleted)
b2e17000-b2e19000 rw-p 00000000 00:00 0 
b2e19000-b2e1b000 rw-p 00000000 00:01 381924     /dev/ashmem/dalvik-indirect ref table (deleted)
b2e1b000-b2e1d000 rw-p 00000000 00:01 386804     /dev/ashmem/dalvik-indirect ref table (deleted)
b2e1d000-b2e1e000 ---p 00000000 00:00 0 
b2e1e000-b2e1f000 ---p 00000000 00:00 0 
b2e1f000-b2f21000 rw-p 00000000 00:00 0          [stack:12731]
b2f21000-b2f22000 ---p 00000000 00:00 0 
b2f22000-b2f23000 ---p 00000000 00:00 0 
b2f23000-b3025000 rw-p 00000000 00:00 0          [stack:12730]
b3025000-b3026000 ---p 00000000 00:00 0 
b3026000-b3027000 ---p 00000000 00:00 0 
b3027000-b3123000 rw-p 00000000 00:00 0          [stack:12729]
b3123000-b3124000 rw-p 00000000 00:01 385772     /dev/ashmem/dalvik-Heap thread pool worker thread 2 (deleted)
b3124000-b3125000 ---p 00001000 00:01 385772     /dev/ashmem/dalvik-Heap thread pool worker thread 2 (deleted)
b3125000-b3223000 rw-p 00002000 00:01 385772     /dev/ashmem/dalvik-Heap thread pool worker thread 2 (deleted)
b3223000-b3224000 rw-p 00000000 00:01 385771     /dev/ashmem/dalvik-Heap thread pool worker thread 1 (deleted)
b3224000-b3225000 ---p 00001000 00:01 385771     /dev/ashmem/dalvik-Heap thread pool worker thread 1 (deleted)
b3225000-b3323000 rw-p 00002000 00:01 385771     /dev/ashmem/dalvik-Heap thread pool worker thread 1 (deleted)
b3323000-b3324000 rw-p 00000000 00:01 385770     /dev/ashmem/dalvik-Heap thread pool worker thread 0 (deleted)
b3324000-b3325000 ---p 00001000 00:01 385770     /dev/ashmem/dalvik-Heap thread pool worker thread 0 (deleted)
b3325000-b3423000 rw-p 00002000 00:01 385770     /dev/ashmem/dalvik-Heap thread pool worker thread 0 (deleted)
b3423000-b3508000 rw-p 00000000 00:01 7028       /dev/ashmem/dalvik-allocspace non moving space mark-bitmap 4 (deleted)
b3508000-b35ed000 rw-p 00000000 00:01 7027       /dev/ashmem/dalvik-allocspace non moving space live-bitmap 4 (deleted)
b35ed000-b36ed000 rw-p 00000000 00:01 7373       /dev/ashmem/dalvik-allocspace zygote / non moving space mark-bitmap 0 (deleted)
b36ed000-b3bf4000 r-xp 00000000 08:06 770        /system/lib/libart.so
b3bf4000-b3bf5000 ---p 00000000 00:00 0 
b3bf5000-b3bfd000 r--p 00507000 08:06 770        /system/lib/libart.so
b3bfd000-b3bfe000 rw-p 0050f000 08:06 770        /system/lib/libart.so
b3bfe000-b4400000 rw-p 00000000 00:00 0 
b4400000-b4401000 r--p 00000000 00:00 0 
b4401000-b4405000 rw-p 00000000 00:00 0 
b4405000-b4407000 rw-p 00000000 00:01 386803     /dev/ashmem/dalvik-indirect ref table (deleted)
b4407000-b4409000 rw-p 00000000 00:00 0 
b4409000-b440b000 rw-p 00000000 00:01 386802     /dev/ashmem/dalvik-indirect ref table (deleted)
b440b000-b440d000 rw-p 00000000 00:00 0 
b440d000-b440e000 r--p 00000000 00:00 0 
b440e000-b4410000 rw-p 00000000 00:01 7395       /dev/ashmem/dalvik-indirect ref table (deleted)
b4410000-b4411000 rw-p 00000000 00:01 7391       /dev/ashmem/dalvik-mark sweep sweep array free buffer (deleted)
b4411000-b4412000 rw-p 00000000 00:01 7390       /dev/ashmem/dalvik-mark sweep sweep array free buffer (deleted)
b4412000-b4413000 rw-p 00000000 00:01 7389       /dev/ashmem/dalvik-mark sweep sweep array free buffer (deleted)
b4413000-b4414000 rw-p 00000000 00:01 7388       /dev/ashmem/dalvik-mark sweep sweep array free buffer (deleted)
b4414000-b4415000 rw-p 00000000 00:01 7387       /dev/ashmem/dalvik-mark sweep sweep array free buffer (deleted)
b4415000-b4435000 rw-p 00000000 00:01 7380       /dev/ashmem/dalvik-large live objects (deleted)
b4435000-b4445000 rw-p 00000000 00:01 7377       /dev/ashmem/dalvik-rosalloc page map (deleted)
b4445000-b4447000 rw-p 00000000 00:01 386801     /dev/ashmem/dalvik-indirect ref table (deleted)
b4447000-b4449000 rw-p 00000000 00:00 0 
b4449000-b444b000 rw-p 00000000 00:01 386800     /dev/ashmem/dalvik-indirect ref table (deleted)
b444b000-b444d000 rw-p 00000000 00:01 386799     /dev/ashmem/dalvik-indirect ref table (deleted)
b444d000-b444f000 rw-p 00000000 00:01 381923     /dev/ashmem/dalvik-indirect ref table (deleted)
b444f000-b4455000 rw-p 00000000 00:00 0 
b4455000-b4555000 rw-p 00000000 00:01 7372       /dev/ashmem/dalvik-allocspace zygote / non moving space live-bitmap 0 (deleted)
b4555000-b4556000 r--p 00000000 08:13 51         /data/dalvik-cache/x86/system@framework@boot.oat
b4556000-b457c000 r--p 00976000 08:13 231        /data/dalvik-cache/x86/system@framework@boot.art
b457c000-b457d000 r-xp 00000000 08:06 893        /system/lib/libsigchain.so
b457d000-b457e000 r--p 00000000 08:06 893        /system/lib/libsigchain.so
b457e000-b457f000 rw-p 00001000 08:06 893        /system/lib/libsigchain.so
b457f000-b4589000 r-xp 00000000 08:06 782        /system/lib/libbacktrace_libc++.so
b4589000-b458a000 r--p 00009000 08:06 782        /system/lib/libbacktrace_libc++.so
b458a000-b458b000 rw-p 0000a000 08:06 782        /system/lib/libbacktrace_libc++.so
b458b000-b458c000 r--p 00000000 00:00 0 
b458c000-b458d000 rw-p 00000000 00:01 7386       /dev/ashmem/dalvik-mark sweep sweep array free buffer (deleted)
b458d000-b45ad000 r--s 00000000 00:05 4026531993  /proc/version
b45ad000-b45ae000 r--p 00000000 00:00 0 
b45ae000-b45ce000 r--s 00000000 00:0d 7186       /dev/__properties__
b45ce000-b45d2000 r-xp 00000000 08:06 881        /system/lib/libpowermanager.so
b45d2000-b45d3000 r--p 00003000 08:06 881        /system/lib/libpowermanager.so
b45d3000-b45d4000 rw-p 00004000 08:06 881        /system/lib/libpowermanager.so
b45d4000-b45e6000 r-xp 00000000 08:06 795        /system/lib/libcommon_time_client.so
b45e6000-b45e7000 ---p 00000000 00:00 0 
b45e7000-b45eb000 r--p 00012000 08:06 795        /system/lib/libcommon_time_client.so
b45eb000-b45ec000 rw-p 00016000 08:06 795        /system/lib/libcommon_time_client.so
b45ec000-b4640000 r-xp 00000000 08:06 784        /system/lib/libbcinfo.so
b4640000-b4641000 r--p 00053000 08:06 784        /system/lib/libbcinfo.so
b4641000-b4642000 rw-p 00054000 08:06 784        /system/lib/libbcinfo.so
b4642000-b4674000 r-xp 00000000 08:06 783        /system/lib/libbcc.so
b4674000-b4676000 r--p 00031000 08:06 783        /system/lib/libbcc.so
b4676000-b4677000 rw-p 00033000 08:06 783        /system/lib/libbcc.so
b4677000-b4697000 rw-p 00000000 00:00 0 
b4697000-b5879000 r-xp 00000000 08:06 753        /system/lib/libLLVM.so
b5879000-b5906000 r--p 011e1000 08:06 753        /system/lib/libLLVM.so
b5906000-b5907000 rw-p 0126e000 08:06 753        /system/lib/libLLVM.so
b5907000-b590e000 rw-p 00000000 00:00 0 
b590e000-b5910000 r-xp 00000000 08:06 953        /system/lib/libunwind-ptrace.so
b5910000-b5911000 r--p 00001000 08:06 953        /system/lib/libunwind-ptrace.so
b5911000-b5912000 rw-p 00002000 08:06 953        /system/lib/libunwind-ptrace.so
b5912000-b592a000 r-xp 00000000 08:06 954        /system/lib/libunwind.so
b592a000-b592b000 r--p 00017000 08:06 954        /system/lib/libunwind.so
b592b000-b592c000 rw-p 00018000 08:06 954        /system/lib/libunwind.so
b592c000-b593b000 rw-p 00000000 00:00 0 
b593b000-b5948000 r-xp 00000000 08:06 822        /system/lib/libgccdemangle.so
b5948000-b5949000 r--p 0000c000 08:06 822        /system/lib/libgccdemangle.so
b5949000-b594a000 rw-p 0000d000 08:06 822        /system/lib/libgccdemangle.so
b594a000-b5969000 r-xp 00000000 08:06 875        /system/lib/libpcre.so
b5969000-b596a000 r--p 0001e000 08:06 875        /system/lib/libpcre.so
b596a000-b596b000 rw-p 0001f000 08:06 875        /system/lib/libpcre.so
b596b000-b5a73000 r-xp 00000000 08:06 787        /system/lib/libc++.so
b5a73000-b5a78000 r--p 00107000 08:06 787        /system/lib/libc++.so
b5a78000-b5a79000 rw-p 0010c000 08:06 787        /system/lib/libc++.so
b5a79000-b5a89000 rw-p 00000000 00:00 0 
b5a89000-b5a8b000 r--p 00000000 00:00 0 
b5a8b000-b5ac2000 r-xp 00000000 08:06 879        /system/lib/libpng.so
b5ac2000-b5ac3000 r--p 00036000 08:06 879        /system/lib/libpng.so
b5ac3000-b5ac4000 rw-p 00037000 08:06 879        /system/lib/libpng.so
b5ac4000-b5b46000 r-xp 00000000 08:06 820        /system/lib/libft2.so
b5b46000-b5b48000 r--p 00081000 08:06 820        /system/lib/libft2.so
b5b48000-b5b49000 rw-p 00083000 08:06 820        /system/lib/libft2.so
b5b49000-b5b6a000 r-xp 00000000 08:06 910        /system/lib/libstagefright_foundation.so
b5b6a000-b5b6b000 ---p 00000000 00:00 0 
b5b6b000-b5b6c000 r--p 00021000 08:06 910        /system/lib/libstagefright_foundation.so
b5b6c000-b5b6d000 rw-p 00022000 08:06 910        /system/lib/libstagefright_foundation.so
b5b6d000-b5b79000 r-xp 00000000 08:06 867        /system/lib/libnbaio.so
b5b79000-b5b7a000 r--p 0000b000 08:06 867        /system/lib/libnbaio.so
b5b7a000-b5b7b000 rw-p 0000c000 08:06 867        /system/lib/libnbaio.so
b5b7b000-b5b81000 r-xp 00000000 08:06 821        /system/lib/libgabi++.so
b5b81000-b5b82000 r--p 00005000 08:06 821        /system/lib/libgabi++.so
b5b82000-b5b83000 rw-p 00006000 08:06 821        /system/lib/libgabi++.so
b5b83000-b5ba6000 r-xp 00000000 08:06 762        /system/lib/libRScpp.so
b5ba6000-b5ba7000 r--p 00022000 08:06 762        /system/lib/libRScpp.so
b5ba7000-b5ba8000 rw-p 00023000 08:06 762        /system/lib/libRScpp.so
b5ba8000-b5bfd000 r-xp 00000000 08:06 758        /system/lib/libRS.so
b5bfd000-b5bfe000 ---p 00000000 00:00 0 
b5bfe000-b5c00000 r--p 00055000 08:06 758        /system/lib/libRS.so
b5c00000-b5c01000 rw-p 00057000 08:06 758        /system/lib/libRS.so
b5c01000-b5c05000 r-xp 00000000 08:06 969        /system/lib/libwpa_client.so
b5c05000-b5c06000 r--p 00003000 08:06 969        /system/lib/libwpa_client.so
b5c06000-b5c07000 rw-p 00004000 08:06 969        /system/lib/libwpa_client.so
b5c07000-b5c08000 r-xp 00000000 08:06 946        /system/lib/libsync.so
b5c08000-b5c09000 r--p 00000000 08:06 946        /system/lib/libsync.so
b5c09000-b5c0a000 rw-p 00001000 08:06 946        /system/lib/libsync.so
b5c0a000-b5c0e000 r-xp 00000000 08:06 901        /system/lib/libspeexresampler.so
b5c0e000-b5c0f000 r--p 00003000 08:06 901        /system/lib/libspeexresampler.so
b5c0f000-b5c10000 rw-p 00004000 08:06 901        /system/lib/libspeexresampler.so
b5c10000-b5cdc000 r-xp 00000000 08:06 747        /system/lib/libGLES_trace.so
b5cdc000-b5cdd000 ---p 00000000 00:00 0 
b5cdd000-b5cdf000 r--p 000cc000 08:06 747        /system/lib/libGLES_trace.so
b5cdf000-b5ce0000 rw-p 000ce000 08:06 747        /system/lib/libGLES_trace.so
b5ce0000-b5ced000 r-xp 00000000 08:06 781        /system/lib/libbacktrace.so
b5ced000-b5cee000 r--p 0000c000 08:06 781        /system/lib/libbacktrace.so
b5cee000-b5cef000 rw-p 0000d000 08:06 781        /system/lib/libbacktrace.so
b5cef000-b5cf0000 r--p 00000000 00:00 0 
b5cf0000-b5d0d000 r-xp 00000000 08:06 970        /system/lib/libz.so
b5d0d000-b5d0e000 r--p 0001c000 08:06 970        /system/lib/libz.so
b5d0e000-b5d0f000 rw-p 0001d000 08:06 970        /system/lib/libz.so
b5d0f000-b5d12000 r-xp 00000000 08:06 956        /system/lib/libusbhost.so
b5d12000-b5d13000 ---p 00000000 00:00 0 
b5d13000-b5d14000 r--p 00003000 08:06 956        /system/lib/libusbhost.so
b5d14000-b5d15000 rw-p 00004000 08:06 956        /system/lib/libusbhost.so
b5d15000-b5d27000 r-xp 00000000 08:06 951        /system/lib/libui.so
b5d27000-b5d28000 r--p 00011000 08:06 951        /system/lib/libui.so
b5d28000-b5d29000 rw-p 00012000 08:06 951        /system/lib/libui.so
b5d29000-b5d9e000 r-xp 00000000 08:06 940        /system/lib/libstlport.so
b5d9e000-b5da1000 r--p 00074000 08:06 940        /system/lib/libstlport.so
b5da1000-b5da2000 rw-p 00077000 08:06 940        /system/lib/libstlport.so
b5da2000-b5df9000 r-xp 00000000 08:06 905        /system/lib/libssl.so
b5df9000-b5dfc000 r--p 00056000 08:06 905        /system/lib/libssl.so
b5dfc000-b5dff000 rw-p 00059000 08:06 905        /system/lib/libssl.so
b5dff000-b5ee7000 r-xp 00000000 08:06 902        /system/lib/libsqlite.so
b5ee7000-b5ee9000 r--p 000e7000 08:06 902        /system/lib/libsqlite.so
b5ee9000-b5eea000 rw-p 000e9000 08:06 902        /system/lib/libsqlite.so
b5eea000-b5eeb000 rw-p 00000000 00:00 0 
b5eeb000-b5efc000 r-xp 00000000 08:06 898        /system/lib/libsoundtrigger.so
b5efc000-b5efd000 ---p 00000000 00:00 0 
b5efd000-b5f00000 r--p 00011000 08:06 898        /system/lib/libsoundtrigger.so
b5f00000-b5f01000 rw-p 00014000 08:06 898        /system/lib/libsoundtrigger.so
b5f01000-b5f5b000 r-xp 00000000 08:06 896        /system/lib/libsonivox.so
b5f5b000-b5f5c000 r--p 00059000 08:06 896        /system/lib/libsonivox.so
b5f5c000-b5f5d000 rw-p 0005a000 08:06 896        /system/lib/libsonivox.so
b5f5d000-b5f62000 rw-p 00000000 00:00 0 
b5f62000-b63d2000 r-xp 00000000 08:06 894        /system/lib/libskia.so
b63d2000-b63d3000 ---p 00000000 00:00 0 
b63d3000-b63ed000 r--p 00470000 08:06 894        /system/lib/libskia.so
b63ed000-b63f0000 rw-p 0048a000 08:06 894        /system/lib/libskia.so
b63f0000-b63f5000 rw-p 00000000 00:00 0 
b63f5000-b640d000 r-xp 00000000 08:06 890        /system/lib/libselinux.so
b640d000-b640e000 r--p 00017000 08:06 890        /system/lib/libselinux.so
b640e000-b640f000 rw-p 00018000 08:06 890        /system/lib/libselinux.so
b640f000-b6411000 r-xp 00000000 08:06 883        /system/lib/libprocessgroup.so
b6411000-b6412000 r--p 00001000 08:06 883        /system/lib/libprocessgroup.so
b6412000-b6413000 rw-p 00002000 08:06 883        /system/lib/libprocessgroup.so
b6413000-b6942000 r-xp 00000000 08:06 876        /system/lib/libpdfium.so
b6942000-b6943000 ---p 00000000 00:00 0 
b6943000-b6950000 r--p 0052f000 08:06 876        /system/lib/libpdfium.so
b6950000-b6955000 rw-p 0053c000 08:06 876        /system/lib/libpdfium.so
b6955000-b6959000 rw-p 00000000 00:00 0 
b6959000-b695a000 r--p 00000000 00:00 0 
b695a000-b6962000 r-xp 00000000 08:06 870        /system/lib/libnetutils.so
b6962000-b6963000 r--p 00007000 08:06 870        /system/lib/libnetutils.so
b6963000-b6964000 rw-p 00008000 08:06 870        /system/lib/libnetutils.so
b6964000-b6966000 r-xp 00000000 08:06 868        /system/lib/libnetd_client.so
b6966000-b6967000 r--p 00001000 08:06 868        /system/lib/libnetd_client.so
b6967000-b6968000 rw-p 00002000 08:06 868        /system/lib/libnetd_client.so
b6968000-b6969000 rw-p 00000000 00:00 0 
b6969000-b696f000 r-xp 00000000 08:06 865        /system/lib/libnativehelper.so
b696f000-b6970000 r--p 00005000 08:06 865        /system/lib/libnativehelper.so
b6970000-b6971000 rw-p 00006000 08:06 865        /system/lib/libnativehelper.so
b6971000-b6973000 r-xp 00000000 08:06 864        /system/lib/libnativebridge.so
b6973000-b6974000 ---p 00000000 00:00 0 
b6974000-b6975000 r--p 00002000 08:06 864        /system/lib/libnativebridge.so
b6975000-b6976000 rw-p 00003000 08:06 864        /system/lib/libnativebridge.so
b6976000-b6987000 r-xp 00000000 08:06 862        /system/lib/libminikin.so
b6987000-b6988000 r--p 00010000 08:06 862        /system/lib/libminikin.so
b6988000-b6989000 rw-p 00011000 08:06 862        /system/lib/libminikin.so
b6989000-b698a000 r-xp 00000000 08:06 861        /system/lib/libmemtrack.so
b698a000-b698b000 r--p 00000000 08:06 861        /system/lib/libmemtrack.so
b698b000-b698c000 rw-p 00001000 08:06 861        /system/lib/libmemtrack.so
b698c000-b6a75000 r-xp 00000000 08:06 856        /system/lib/libmedia.so
b6a75000-b6a92000 r--p 000e8000 08:06 856        /system/lib/libmedia.so
b6a92000-b6a93000 rw-p 00105000 08:06 856        /system/lib/libmedia.so
b6a93000-b6ad2000 r-xp 00000000 08:06 849        /system/lib/libjpeg.so
b6ad2000-b6ad3000 r--p 0003e000 08:06 849        /system/lib/libjpeg.so
b6ad3000-b6ad4000 rw-p 0003f000 08:06 849        /system/lib/libjpeg.so
b6ad4000-b6b2f000 r-xp 00000000 08:06 833        /system/lib/libinputflinger.so
b6b2f000-b6b32000 r--p 0005a000 08:06 833        /system/lib/libinputflinger.so
b6b32000-b6b33000 rw-p 0005d000 08:06 833        /system/lib/libinputflinger.so
b6b33000-b6b58000 r-xp 00000000 08:06 832        /system/lib/libinput.so
b6b58000-b6b59000 ---p 00000000 00:00 0 
b6b59000-b6b5c000 r--p 00025000 08:06 832        /system/lib/libinput.so
b6b5c000-b6b5d000 rw-p 00028000 08:06 832        /system/lib/libinput.so
b6b5d000-b6b6e000 r-xp 00000000 08:06 831        /system/lib/libimg_utils.so
b6b6e000-b6b70000 r--p 00010000 08:06 831        /system/lib/libimg_utils.so
b6b70000-b6b71000 rw-p 00012000 08:06 831        /system/lib/libimg_utils.so
b6b71000-b6d0f000 r-xp 00000000 08:06 830        /system/lib/libicuuc.so
b6d0f000-b6d10000 ---p 00000000 00:00 0 
b6d10000-b6d1b000 r--p 0019e000 08:06 830        /system/lib/libicuuc.so
b6d1b000-b6d1c000 rw-p 001a9000 08:06 830        /system/lib/libicuuc.so
b6d1c000-b6d20000 rw-p 00000000 00:00 0 
b6d20000-b6d21000 r--p 00000000 00:00 0 
b6d21000-b6f50000 r-xp 00000000 08:06 829        /system/lib/libicui18n.so
b6f50000-b6f5b000 r--p 0022e000 08:06 829        /system/lib/libicui18n.so
b6f5b000-b6f5c000 rw-p 00239000 08:06 829        /system/lib/libicui18n.so
b6f5c000-b7007000 r-xp 00000000 08:06 828        /system/lib/libhwui.so
b7007000-b700b000 r--p 000aa000 08:06 828        /system/lib/libhwui.so
b700b000-b700c000 rw-p 000ae000 08:06 828        /system/lib/libhwui.so
b700c000-b7062000 r-xp 00000000 08:06 826        /system/lib/libharfbuzz_ng.so
b7062000-b7063000 r--p 00055000 08:06 826        /system/lib/libharfbuzz_ng.so
b7063000-b7064000 rw-p 00056000 08:06 826        /system/lib/libharfbuzz_ng.so
b7064000-b706a000 r-xp 00000000 08:06 825        /system/lib/libhardware_legacy.so
b706a000-b706b000 r--p 00005000 08:06 825        /system/lib/libhardware_legacy.so
b706b000-b706c000 rw-p 00006000 08:06 825        /system/lib/libhardware_legacy.so
b706c000-b706d000 rw-p 00000000 00:00 0 
b706d000-b706e000 r-xp 00000000 08:06 824        /system/lib/libhardware.so
b706e000-b706f000 r--p 00000000 08:06 824        /system/lib/libhardware.so
b706f000-b7070000 rw-p 00001000 08:06 824        /system/lib/libhardware.so
b7070000-b70e3000 r-xp 00000000 08:06 823        /system/lib/libgui.so
b70e3000-b70e4000 ---p 00000000 00:00 0 
b70e4000-b70f1000 r--p 00073000 08:06 823        /system/lib/libgui.so
b70f1000-b70f2000 rw-p 00080000 08:06 823        /system/lib/libgui.so
b70f2000-b7121000 r-xp 00000000 08:06 807        /system/lib/libexpat.so
b7121000-b7122000 ---p 00000000 00:00 0 
b7122000-b7124000 r--p 0002f000 08:06 807        /system/lib/libexpat.so
b7124000-b7125000 rw-p 00031000 08:06 807        /system/lib/libexpat.so
b7125000-b7291000 r-xp 00000000 08:06 797        /system/lib/libcrypto.so
b7291000-b7292000 ---p 00000000 00:00 0 
b7292000-b72a1000 r--p 0016c000 08:06 797        /system/lib/libcrypto.so
b72a1000-b72a7000 rw-p 0017b000 08:06 797        /system/lib/libcrypto.so
b72a7000-b72a9000 rw-p 00000000 00:00 0 
b72a9000-b72b0000 r-xp 00000000 08:06 790        /system/lib/libcamera_metadata.so
b72b0000-b72b1000 r--p 00006000 08:06 790        /system/lib/libcamera_metadata.so
b72b1000-b72b2000 rw-p 00007000 08:06 790        /system/lib/libcamera_metadata.so
b72b2000-b7305000 r-xp 00000000 08:06 789        /system/lib/libcamera_client.so
b7305000-b7310000 r--p 00052000 08:06 789        /system/lib/libcamera_client.so
b7310000-b7311000 rw-p 0005d000 08:06 789        /system/lib/libcamera_client.so
b7311000-b7317000 r-xp 00000000 08:06 777        /system/lib/libaudioutils.so
b7317000-b7318000 r--p 00005000 08:06 777        /system/lib/libaudioutils.so
b7318000-b7319000 rw-p 00006000 08:06 777        /system/lib/libaudioutils.so
b7319000-b7357000 r-xp 00000000 08:06 767        /system/lib/libandroidfw.so
b7357000-b7359000 r--p 0003d000 08:06 767        /system/lib/libandroidfw.so
b7359000-b735a000 rw-p 0003f000 08:06 767        /system/lib/libandroidfw.so
b735a000-b735b000 r--p 00000000 00:00 0 
b735b000-b7369000 r-xp 00000000 08:06 750        /system/lib/libGLESv2.so
b7369000-b736a000 ---p 00000000 00:00 0 
b736a000-b736b000 r--p 0000e000 08:06 750        /system/lib/libGLESv2.so
b736b000-b736c000 rw-p 0000f000 08:06 750        /system/lib/libGLESv2.so
b736c000-b7374000 r-xp 00000000 08:06 748        /system/lib/libGLESv1_CM.so
b7374000-b7375000 r--p 00007000 08:06 748        /system/lib/libGLESv1_CM.so
b7375000-b7376000 rw-p 00008000 08:06 748        /system/lib/libGLESv1_CM.so
b7376000-b7379000 r-xp 00000000 08:06 744        /system/lib/libETC1.so
b7379000-b737a000 r--p 00002000 08:06 744        /system/lib/libETC1.so
b737a000-b737b000 rw-p 00003000 08:06 744        /system/lib/libETC1.so
b737b000-b737c000 r--p 00000000 00:00 0 
b737c000-b742f000 r-xp 00000000 08:06 743        /system/lib/libEGL.so
b742f000-b7431000 r--p 000b2000 08:06 743        /system/lib/libEGL.so
b7431000-b7438000 rw-p 000b4000 08:06 743        /system/lib/libEGL.so
b7438000-b743b000 rw-p 00000000 00:00 0 
b743b000-b7460000 r-xp 00000000 08:06 957        /system/lib/libutils.so
b7460000-b7461000 ---p 00000000 00:00 0 
b7461000-b7462000 r--p 00025000 08:06 957        /system/lib/libutils.so
b7462000-b7463000 rw-p 00026000 08:06 957        /system/lib/libutils.so
b7463000-b7466000 r-xp 00000000 08:06 939        /system/lib/libstdc++.so
b7466000-b7467000 r--p 00002000 08:06 939        /system/lib/libstdc++.so
b7467000-b7468000 rw-p 00003000 08:06 939        /system/lib/libstdc++.so
b7468000-b7488000 r-xp 00000000 08:06 854        /system/lib/libm.so
b7488000-b7489000 r--p 0001f000 08:06 854        /system/lib/libm.so
b7489000-b748a000 rw-p 00020000 08:06 854        /system/lib/libm.so
b748a000-b7492000 r-xp 00000000 08:06 852        /system/lib/liblog.so
b7492000-b7493000 ---p 00000000 00:00 0 
b7493000-b7494000 r--p 00008000 08:06 852        /system/lib/liblog.so
b7494000-b7495000 rw-p 00009000 08:06 852        /system/lib/liblog.so
b7495000-b74aa000 r-xp 00000000 08:06 798        /system/lib/libcutils.so
b74aa000-b74ab000 r--p 00014000 08:06 798        /system/lib/libcutils.so
b74ab000-b74ac000 rw-p 00015000 08:06 798        /system/lib/libcutils.so
b74ac000-b7586000 r-xp 00000000 08:06 788        /system/lib/libc.so
b7586000-b7587000 ---p 00000000 00:00 0 
b7587000-b758a000 r--p 000da000 08:06 788        /system/lib/libc.so
b758a000-b758d000 rw-p 000dd000 08:06 788        /system/lib/libc.so
b758d000-b7597000 rw-p 00000000 00:00 0 
b7597000-b75dc000 r-xp 00000000 08:06 785        /system/lib/libbinder.so
b75dc000-b75dd000 ---p 00000000 00:00 0 
b75dd000-b75e5000 r--p 00045000 08:06 785        /system/lib/libbinder.so
b75e5000-b75e6000 rw-p 0004d000 08:06 785        /system/lib/libbinder.so
b75e6000-b7768000 r-xp 00000000 08:06 765        /system/lib/libandroid_runtime.so
b7768000-b7769000 ---p 00000000 00:00 0 
b7769000-b7770000 r--p 00182000 08:06 765        /system/lib/libandroid_runtime.so
b7770000-b7778000 rw-p 00189000 08:06 765        /system/lib/libandroid_runtime.so
b7778000-b7779000 rw-p 00000000 00:00 0 
b7779000-b777a000 r--p 00000000 00:00 0 
b777a000-b777b000 rw-p 00000000 00:00 0 
b777b000-b777c000 r--p 00000000 00:00 0 
b777c000-b777e000 rw-p 00000000 00:00 0 
b777e000-b7780000 r--p 00000000 00:00 0          [vvar]
b7780000-b7781000 r-xp 00000000 00:00 0          [vdso]
b7781000-b7797000 r-xp 00000000 08:06 124        /system/bin/linker
b7797000-b7798000 r--p 00000000 00:00 0 
b7798000-b7799000 r--p 00016000 08:06 124        /system/bin/linker
b7799000-b779a000 rw-p 00017000 08:06 124        /system/bin/linker
b779a000-b779b000 rw-p 00000000 00:00 0 
b779b000-b779f000 r-xp 00000000 08:06 61         /system/bin/app_process32
b779f000-b77a0000 r--p 00003000 08:06 61         /system/bin/app_process32
b77a0000-b77a1000 rw-p 00000000 00:00 0 
bf505000-bf505000 rw-p 00000000 00:00 0 
bf505000-bf506000 ---p 00000000 00:00 0 
bf506000-bfd05000 rw-p 00000000 00:00 0          [stack]
```

</details>

需要找到`libil2cpp.so`的位置
``` bash
9e033000-9e135000 rw-p 00000000 00:00 0          [stack:12742]
9e135000-9e164000 rwxp 00000000 08:13 122897     /data/app/com.bilibili.priconne-1/lib/x86/libil2cpp.so
9e164000-9e16a000 r-xp 0002f000 08:13 122897     /data/app/com.bilibili.priconne-1/lib/x86/libil2cpp.so
9e16a000-9e16b000 r--p 00034000 08:13 122897     /data/app/com.bilibili.priconne-1/lib/x86/libil2cpp.so
9e16b000-9e16d000 rw-p 00035000 08:13 122897     /data/app/com.bilibili.priconne-1/lib/x86/libil2cpp.so
9e16d000-a2953000 rwxp 00037000 08:13 122897     /data/app/com.bilibili.priconne-1/lib/x86/libil2cpp.so
a2953000-a2c42000 rwxp 00000000 00:00 0 
a2c42000-a2c43000 ---p 00000000 00:00 0 
a2c43000-a2c44000 ---p 00000000 00:00 0 
a2c44000-a2d40000 rw-p 00000000 00:00 0          [stack:12739]
```
也就是说`9e135000`是起始位，但是`bin`文件并不是按照这个地址拆开保存的，直接按照文件大小逆向排序
![排序](https://i1.yuangezhizao.cn/Win-10/20200418183350.jpg!webp)

不难看出是在`com.bilibili.priconne-9e02d000-a48c0000.bin`该文件中，接下来就需要`010`编辑十六进制文件了
`so`文件是`9e135000`开始的，而`bin`文件是`9e02d000`开始的，因此位置为`9e135000`-`9e02d000`=`108000`
按快捷键<kbd>CTRL</kbd>+<kbd>G</kbd>，跳转到`108000`就能看到`ELF`文件头了
![45 4C 46](https://i1.yuangezhizao.cn/Win-10/20200418184345.jpg!webp)

接下来是文件尾部，同理用`a2953000`-`9e02d000`=`4926000`
![492:6000h](https://i1.yuangezhizao.cn/Win-10/20200418184547.jpg!webp)

然后先删除`4926000`后面的内容，再删除`108000`前面的内容，最后另存文件为`com.bilibili.priconne-9e02d000-a48c0000-dump.so`
然后直接从`4926000`开始拽到整个文件结束，删除（后来才想到应该从`4926010`开始吧
先拿`010`打开保存的`so`，可以去[sweetscape](https://web.archive.org/web/20200418105236/https://www.sweetscape.com/010editor/repository/files/ELF.bt)下解析模板`ELF.bt`来辅助阅读，然后就有`23`个警告草
``` bash
Executing template 'D:\yuangezhizao\Documents\SweetScape\010 Templates\ELF.bt' on 'D:\yuangezhizao\Downloads\逍遥安卓下载\dump\com.bilibili.priconne-9e02d000-a48c0000-dump.so'...
Segment data appears to either overlap with header, exist after the end of the file or overlap with the end of the file!
Section table either points outside or extends outside of the file
Section table either points outside or extends outside of the file
Section table either points outside or extends outside of the file
Section table either points outside or extends outside of the file
Section table either points outside or extends outside of the file
Section table either points outside or extends outside of the file
Section table either points outside or extends outside of the file
Section table either points outside or extends outside of the file
Section table either points outside or extends outside of the file
Section table either points outside or extends outside of the file
Section table either points outside or extends outside of the file
Section table either points outside or extends outside of the file
Section table either points outside or extends outside of the file
Section table either points outside or extends outside of the file
Section table either points outside or extends outside of the file
Section table either points outside or extends outside of the file
Section table either points outside or extends outside of the file
Section table either points outside or extends outside of the file
Section table either points outside or extends outside of the file
Section table either points outside or extends outside of the file
Section table either points outside or extends outside of the file
Section table either points outside or extends outside of the file
Result = 23 warnings found, template may not have run successfully!
```
但是并不知道该如何修复这个`so`文件，因为有看到别人修复过的：[[原创]内存dump 获得基于Unity3d的游戏相关代码](https://web.archive.org/web/20200418110501/https://bbs.pediy.com/thread-223649.htm)
![Template Results](https://i1.yuangezhizao.cn/Win-10/20200418185718.jpg!webp)
最后扔`IDA`，过两个警告
![1](https://i1.yuangezhizao.cn/Win-10/20200418185910.jpg!webp)
![2](https://i1.yuangezhizao.cn/Win-10/20200418185948.jpg!webp)

导出函数里就可以看到`il2cpp`相关操作了，但是并不是所有的函数都可以`F5`看源码
![1](https://i1.yuangezhizao.cn/Win-10/20200418190126.jpg!webp)

对比之前`dump`的`so`文件（同`x86`版本），`JNI_OnLoad`的内容并未发生改变，但是之前的导出函数只有`JNI_OnLoad`……
![char *__cdecl JNI_OnLoad(int a1)](https://i1.yuangezhizao.cn/Win-10/20200418190408.jpg!webp)

再去用`Il2CppDumper`，会提示输入地址：`9e135000`
![Il2CppDumper](https://i1.yuangezhizao.cn/Win-10/20200418143800.jpg!webp)
再次尝试并输入`0`，结果仍然提示可能受保护，并且需要输入`Code`地址，又联想到之前模板解析的结果中`Code`地址同样是`0`
![Il2CppDumper](https://i1.yuangezhizao.cn/Win-10/20200418192958.jpg!webp)

`2020-5-29 22:05:56`：挠头`.jpg`，才发现这篇文章已经鸽了……

## 0x05.引用
[记一次 Unity IL2CPP 游戏逆向](https://web.archive.org/web/20200418121727/https://dev.moe/1282)

## 0x06.免责声明
> 本文的目的只有一个就是学习更多的破解技巧和思路，如果有人利用本文技术去进行非法商业获取利益带来的法律责任都是操作者自己承担，和本文以及作者没关系

未完待续……