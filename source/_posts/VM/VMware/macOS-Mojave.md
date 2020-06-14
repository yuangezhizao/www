---
title: VMware 导入 macOS Mojave
date: 2019-12-25 20:08:58
tags:
  - VM
  - VMware
  - macOS
count: 1
os: 0
os_1: 10.0.17763.914 2019-LTSC
browser: 0
browser_1: 74.0.3729.169 Stable
place: 新家
key: 64
---
    接着昨天继续搞（圣诞节警告
<!-- more -->
## 0x00.前言
大佬组的`ESXI`最近遇到了一个问题——硬盘炸了，其实印象里早在前一阵子就貌似在日志里看到过硬盘的警告……
但是并没有过于在意于是就暂时放下了，但是最近一次重启（为了给`ESXI`打上`unlocker`补丁）之后`wz`说他的虚拟机开机之后全？炸了（黑群晖、`Debian`、`EVE`）……
怀疑是某块`500 GB`硬盘的锅于是立即挂起全部虚拟机，把硬盘插到台式上进行磁盘检查（还拿走了本人的`U`盘被迫作成`PE`），扫描还没到`5 min`就看到了前面的**数十**个坏道点，过草……
![草](https://i1.yuangezhizao.cn/Win-10/20191016005155.jpg!webp)

近期，`tb`搞了块`60`块钱左右的硬盘先凑合用，年后准备把这套卖掉之后组建更高性能的（预计`5K`？
然后，趁着旧硬盘还没彻底报废赶紧在`web`端进行`导出`，这里导出了仨文件：`macOS.ovf`、`macOS.mf`、`disk-0.vmdk`
比较有意思的是`disk-0.vmdk`占用`33.3 GB`而实际存储的`macOS.vmdk`可是有`44.92 GB`……
然后，打了一份快照备用之后在`数据存储浏览器`中立即进行数据迁移，没错，`VMs`就是那块「一副要死的样子」的硬盘……
![VMs](https://i1.yuangezhizao.cn/Win-10/20191225202624.jpg!webp)

终于挪完地方了～

任务 | 目标 | 启动者 | 已排队时间 | 启动时间 | 结果 | 完成时间
:---: | :---: | :---: | :---: | :---: | :---: | :---:
Copy Datastore File | 无 | root | 2019/12/25 19:04:15 | 2019/12/25 19:04:15 | 成功完成 | 2019/12/25 20:31:21

## 0x01.Unlocker
`gh`上原版的`Unlocker`应该是找不到了，只找到了其他仓库，最开始接触这玩楞应该是大一大二那时候，连`py`还都不会呢
三四年后的今天，也能看个大概这个补丁的原理了，除了替换之外还去官网下载`com.vmware.fusion.tools.darwin.zip.tar`文件
这样`Unlocker`文件的作用也大概搞懂了（
![先结束这四个进程](https://i1.yuangezhizao.cn/Win-10/20191225203332.jpg!webp)

以管理员权限运行：
``` bash
C:\Windows\System32>"D:\yuangezhizao\Documents\Virtual Machines\unlocker-3.0.2\win-install.cmd"

Unlocker 3.0.2 for VMware Workstation
=====================================
(c) Dave Parsons 2011-18

Set encoding parameters...
Active code page: 850

VMware is installed at: C:\Program Files (x86)\VMware\VMware Workstation\
VMware product version: 15.1.0.13591040

Stopping VMware services...

Backing up files...
C:\Program Files (x86)\VMware\VMware Workstation\x64\vmware-vmx.exe -> D:\yuangezhizao\Documents\Virtual Machines\3.0\unlocker-3.0.2\backup\x64\vmware-vmx.exe
1 File(s) copied
C:\Program Files (x86)\VMware\VMware Workstation\x64\vmware-vmx-debug.exe -> D:\yuangezhizao\Documents\Virtual Machines\3.0\unlocker-3.0.2\backup\x64\vmware-vmx-debug.exe
1 File(s) copied
C:\Program Files (x86)\VMware\VMware Workstation\x64\vmware-vmx-stats.exe -> D:\yuangezhizao\Documents\Virtual Machines\3.0\unlocker-3.0.2\backup\x64\vmware-vmx-stats.exe
1 File(s) copied
C:\Program Files (x86)\VMware\VMware Workstation\vmwarebase.dll -> D:\yuangezhizao\Documents\Virtual Machines\3.0\unlocker-3.0.2\backup\vmwarebase.dll
1 File(s) copied

Patching...
File: C:\Program Files (x86)\VMware\VMware Workstation\x64\vmware-vmx.exe

appleSMCTableV0 (smc.version = "0")
appleSMCTableV0 Address      : 0xab4150
appleSMCTableV0 Private Key #: 0xF2/242
appleSMCTableV0 Public Key  #: 0xF0/240
appleSMCTableV0 Table        : 0xab4170
+LKS Key:
002 0xab41b8 +LKS 01 flag 0x90 0x140167c70L 07
OSK0 Key Before:
241 0xab84f0 OSK0 32 ch8* 0x80 0x140167cf0L 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
OSK0 Key After:
241 0xab84f0 OSK0 32 ch8* 0x80 0x140167c70L 6F 75 72 68 61 72 64 77 6F 72 6B 62 79 74 68 65 73 65 77 6F 72 64 73 67 75 61 72 64 65 64 70 6C
OSK1 Key Before:
242 0xab8538 OSK1 32 ch8* 0x80 0x140167cf0L 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
OSK1 Key After:
242 0xab8538 OSK1 32 ch8* 0x80 0x140167c70L 65 61 73 65 64 6F 6E 74 73 74 65 61 6C 28 63 29 41 70 70 6C 65 43 6F 6D 70 75 74 65 72 49 6E 63

appleSMCTableV1 (smc.version = "1")
appleSMCTableV1 Address      : 0xab8580
appleSMCTableV1 Private Key #: 0x01B4/436
appleSMCTableV1 Public Key  #: 0x01B0/432
appleSMCTableV1 Table        : 0xab85a0
+LKS Key:
004 0xab8678 +LKS 01 flag 0x90 0x140167c70L 01
OSK0 Key Before:
435 0xabffb0 OSK0 32 ch8* 0x90 0x140167cf0L 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
OSK0 Key After:
435 0xabffb0 OSK0 32 ch8* 0x90 0x140167c70L 6F 75 72 68 61 72 64 77 6F 72 6B 62 79 74 68 65 73 65 77 6F 72 64 73 67 75 61 72 64 65 64 70 6C
OSK1 Key Before:
436 0xabfff8 OSK1 32 ch8* 0x90 0x140167cf0L 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
OSK1 Key After:
436 0xabfff8 OSK1 32 ch8* 0x90 0x140167c70L 65 61 73 65 64 6F 6E 74 73 74 65 61 6C 28 63 29 41 70 70 6C 65 43 6F 6D 70 75 74 65 72 49 6E 63

File: C:\Program Files (x86)\VMware\VMware Workstation\x64\vmware-vmx-debug.exe

appleSMCTableV0 (smc.version = "0")
appleSMCTableV0 Address      : 0xcbda60
appleSMCTableV0 Private Key #: 0xF2/242
appleSMCTableV0 Public Key  #: 0xF0/240
appleSMCTableV0 Table        : 0xcbda80
+LKS Key:
002 0xcbdac8 +LKS 01 flag 0x90 0x14019fa20L 07
OSK0 Key Before:
241 0xcc1e00 OSK0 32 ch8* 0x80 0x14019fc00L 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
OSK0 Key After:
241 0xcc1e00 OSK0 32 ch8* 0x80 0x14019fa20L 6F 75 72 68 61 72 64 77 6F 72 6B 62 79 74 68 65 73 65 77 6F 72 64 73 67 75 61 72 64 65 64 70 6C
OSK1 Key Before:
242 0xcc1e48 OSK1 32 ch8* 0x80 0x14019fc00L 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
OSK1 Key After:
242 0xcc1e48 OSK1 32 ch8* 0x80 0x14019fa20L 65 61 73 65 64 6F 6E 74 73 74 65 61 6C 28 63 29 41 70 70 6C 65 43 6F 6D 70 75 74 65 72 49 6E 63

appleSMCTableV1 (smc.version = "1")
appleSMCTableV1 Address      : 0xcc1e90
appleSMCTableV1 Private Key #: 0x01B4/436
appleSMCTableV1 Public Key  #: 0x01B0/432
appleSMCTableV1 Table        : 0xcc1eb0
+LKS Key:
004 0xcc1f88 +LKS 01 flag 0x90 0x14019fa20L 01
OSK0 Key Before:
435 0xcc98c0 OSK0 32 ch8* 0x90 0x14019fc00L 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
OSK0 Key After:
435 0xcc98c0 OSK0 32 ch8* 0x90 0x14019fa20L 6F 75 72 68 61 72 64 77 6F 72 6B 62 79 74 68 65 73 65 77 6F 72 64 73 67 75 61 72 64 65 64 70 6C
OSK1 Key Before:
436 0xcc9908 OSK1 32 ch8* 0x90 0x14019fc00L 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
OSK1 Key After:
436 0xcc9908 OSK1 32 ch8* 0x90 0x14019fa20L 65 61 73 65 64 6F 6E 74 73 74 65 61 6C 28 63 29 41 70 70 6C 65 43 6F 6D 70 75 74 65 72 49 6E 63

File: C:\Program Files (x86)\VMware\VMware Workstation\x64\vmware-vmx-stats.exe

appleSMCTableV0 (smc.version = "0")
appleSMCTableV0 Address      : 0xaec4c0
appleSMCTableV0 Private Key #: 0xF2/242
appleSMCTableV0 Public Key  #: 0xF0/240
appleSMCTableV0 Table        : 0xaec4e0
+LKS Key:
002 0xaec528 +LKS 01 flag 0x90 0x1401718d0L 07
OSK0 Key Before:
241 0xaf0860 OSK0 32 ch8* 0x80 0x140171950L 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
OSK0 Key After:
241 0xaf0860 OSK0 32 ch8* 0x80 0x1401718d0L 6F 75 72 68 61 72 64 77 6F 72 6B 62 79 74 68 65 73 65 77 6F 72 64 73 67 75 61 72 64 65 64 70 6C
OSK1 Key Before:
242 0xaf08a8 OSK1 32 ch8* 0x80 0x140171950L 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
OSK1 Key After:
242 0xaf08a8 OSK1 32 ch8* 0x80 0x1401718d0L 65 61 73 65 64 6F 6E 74 73 74 65 61 6C 28 63 29 41 70 70 6C 65 43 6F 6D 70 75 74 65 72 49 6E 63

appleSMCTableV1 (smc.version = "1")
appleSMCTableV1 Address      : 0xaf08f0
appleSMCTableV1 Private Key #: 0x01B4/436
appleSMCTableV1 Public Key  #: 0x01B0/432
appleSMCTableV1 Table        : 0xaf0910
+LKS Key:
004 0xaf09e8 +LKS 01 flag 0x90 0x1401718d0L 01
OSK0 Key Before:
435 0xaf8320 OSK0 32 ch8* 0x90 0x140171950L 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
OSK0 Key After:
435 0xaf8320 OSK0 32 ch8* 0x90 0x1401718d0L 6F 75 72 68 61 72 64 77 6F 72 6B 62 79 74 68 65 73 65 77 6F 72 64 73 67 75 61 72 64 65 64 70 6C
OSK1 Key Before:
436 0xaf8368 OSK1 32 ch8* 0x90 0x140171950L 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
OSK1 Key After:
436 0xaf8368 OSK1 32 ch8* 0x90 0x1401718d0L 65 61 73 65 64 6F 6E 74 73 74 65 61 6C 28 63 29 41 70 70 6C 65 43 6F 6D 70 75 74 65 72 49 6E 63

GOS Patching: C:\Program Files (x86)\VMware\VMware Workstation\vmwarebase.dll
GOS Patched flag @: 0x4fa2e8
GOS Patched flag @: 0x4fa328
GOS Patched flag @: 0x4fa368
GOS Patched flag @: 0x4fa3a8
GOS Patched flag @: 0x4fa3e8
GOS Patched flag @: 0x4fa428
GOS Patched flag @: 0x4fa468
GOS Patched flag @: 0x4fa4a8
GOS Patched flag @: 0x4fa4e8
GOS Patched flag @: 0x4fa528
GOS Patched flag @: 0x4fa568
GOS Patched flag @: 0x4fa5a8
GOS Patched flag @: 0x4fa5e8
GOS Patched flag @: 0x590d28
GOS Patched flag @: 0x590d68
GOS Patched flag @: 0x590da8
GOS Patched flag @: 0x590de8
GOS Patched flag @: 0x590e28
GOS Patched flag @: 0x590e68
GOS Patched flag @: 0x590ea8
GOS Patched flag @: 0x590ee8
GOS Patched flag @: 0x590f28
GOS Patched flag @: 0x590f68
GOS Patched flag @: 0x590fa8
GOS Patched flag @: 0x590fe8
GOS Patched flag @: 0x591028
GOS Patched: C:\Program Files (x86)\VMware\VMware Workstation\vmwarebase.dll

Getting VMware Tools...
Retrieving Darwin tools from: http://softwareupdate.vmware.com/cds/vmw-desktop/fusion/11.5.1/15018442/packages/com.vmware.fusion.tools.darwin.zip.tar
Traceback (most recent call last):
  File "gettools.py", line 159, in <module>
    main()
  File "gettools.py", line 112, in main
    tar = tarfile.open(convertpath(dest + '/tools/com.vmware.fusion.tools.darwin.zip.tar'), 'r')
  File "tarfile.py", line 1680, in open
tarfile.ReadError: file could not be opened successfully
[2256] Failed to execute script gettools
File not found - darwin*.*
0 File(s) copied

Starting VMware services...

Finished!
```
比较遗憾的是，并没有从`fusion`中成功下载得到`com.vmware.fusion.tools.darwin.zip.tar`……

## 0x01.导入
![打开](https://i1.yuangezhizao.cn/Win-10/20191225203936.png!webp)
![果然恢复了大小](https://i1.yuangezhizao.cn/Win-10/20191225204056.jpg!webp)
![经过一段时间的等待就导入完成了](https://i1.yuangezhizao.cn/Win-10/20191225203908.jpg!webp)
![果然还是失败了](https://i1.yuangezhizao.cn/Win-10/20191225204144.jpg!webp)

顺便一提：本地更新不能，于是去官网下载结果发现还需要注册，过草……
![下载麻烦到爆](https://i1.yuangezhizao.cn/Win-10/20191225204519.jpg!webp)

未完待续……