---
title: 希捷 Seagate 机械 ST500LT012-1DG142 翻车记
date: 2022-02-16 23:18:24
tags:
  - Seagate
  - HDD
count: 1
os: 1
os_1: Monterry 12.2.1 (21D62)
browser: 0
browser_1: 98.0.4758.102 Stable
place: 新家
key: 131
---
    难忘的端午节：不仅（第一次）没在家过，ESXi 的硬盘还逼了草
<!-- more -->
## 0x00.`TL;DR`
https://twitter.com/yuangezhizao/status/1493640040802504706

## 0x01.前言
`storage`怎么变成专门用来放翻车经历的文件夹了草？`(╯°□°）╯︵┻━┻`既然硬盘已经炸了，那还是来记录下是怎么炸的吧

## 0x02.回顾
几天前[#107774340715434959](https://mastodon.yuangezhizao.cn/@yuangezhizao/107774340715434959)看到树莓派官方终于推出了`64-bit`的系统，<span title="你知道的太多了" class="heimu">升级一时爽，翻车火葬场（</span>
本来的计划[#107802168869021564](https://mastodon.yuangezhizao.cn/@yuangezhizao/107802168869021564)也是把`rpi-slave`升级到`Raspberry Pi OS (64-bit)`，而`rpi-master`保持`Raspberry Pi OS`
于是光速把`rpi-slave`下电，并取下`SD`卡烧录镜像一顿操作猛如虎，然后在折腾的`setup`时候发现代理炸了
本地访问不到`windows server`的`PAC`文件了，并且连`ping`都`ping`不通？
登录`ESXi`发现虚拟机都在执行关机操作，有几个没装`vm-tools`的虚拟机自然是操作无效就没关上（现在回想应该还是没有给这几个虚拟机真正关机上，指没有执行**关闭电源**），然后过了一会`ESXi`主机就`shutdown`了
去客厅果然异常安静，`ESXi`还得用不能停于是又给开机了，开机之后再登录发现有几个虚拟机报错~~说是磁盘有问题~~（也确实没仔细看
![这 tm 是找不到文件啊淦](https://i1.yuangezhizao.cn/macOS/6EB0C1E76206217B22A5E95539E89A5E.jpg!webp)

以为都是像之前`HA`的硬盘执行一次修复操作就能恢复（还寻思怎么这么多
``` bash
vmkfstools -x repair /vmfs/volumes/DHG的磁盘/HA/hassos_ova-5.12.vmdk
```
![一片红](https://i1.yuangezhizao.cn/macOS/8A5C2F9E6FB0C7B3ACEB9F942557D7B0.jpg!webp)

就没太在意于是继续折腾`setup`了：[#107802498430000851](https://mastodon.yuangezhizao.cn/@yuangezhizao/107802498430000851)&[#107802613391102079](https://mastodon.yuangezhizao.cn/@yuangezhizao/107802613391102079)，直到俩小时差不多搞定后，再回过头来看`ESXi`，发现出大事情，是磁盘找不到了而不是磁盘有错误
在`WZ`的提醒下才发现少了一块`500G`的盘……并且`500G`只识别出了`3.86 GB`：[#107802717830824989](https://mastodon.yuangezhizao.cn/@yuangezhizao/107802717830824989)
本来想着`U`盘启动去`PE`里看看能不能修，结果`BIOS`里就看不到，直接入土（这可不是拿个软件修修坏道那么简单的事情了
![500G 不见了](https://i1.yuangezhizao.cn/macOS/A6DBA93BC5DFA0313FCD8A5F323FE195.jpg!webp)
![寄](https://i1.yuangezhizao.cn/macOS/1B8F8F9A032F92FAE0FF9AFAAACFA5E1.jpg!webp)

事已至此，只能掏钱买新盘了，当晚就众筹下单了（`2T+4T`），大佬们的赞助还是很给力的，还加购了条内存到总`128G`和`PCI-E 转 6 口 SATA3.0 *4`的转接卡，属于被迫提前升级了一波

## 0x03.坏
今晚回家后，把那块盘从机箱里拿出来了[#107807952048112891](https://mastodon.yuangezhizao.cn/@yuangezhizao/107807952048112891)，也没抱太大希望，果然「这盘上电转都不转，只亮蓝灯嘟嘟响，等到不响了红灯闪烁也没转草」：[#107808112968448154](https://mastodon.yuangezhizao.cn/@yuangezhizao/107808112968448154)
`v2`搜了下这种情况多半是驱动板/固件坏了：[#107808253285378695](https://mastodon.yuangezhizao.cn/@yuangezhizao/107808253285378695)能开盘恢复但是得`1000+`，告辞（

## 0x04.ups.sh
罪魁祸首：[UPS与ESXI联动实现断电自动关机](https://web.archive.org/web/20220216171348/https://cloud.tencent.com/developer/article/1855904)，不能因为是`腾讯公司网络技术服务专家`写的文章就完全相信，甚至还翻到了自己留的到现在也没有被回复的评论（注：对方文章照常更新
![草](https://i1.yuangezhizao.cn/macOS/20220217011434.png!webp)

心情复杂，抛开一直等着别人评论不说，当初开始用山特的`UPS`软件`Winpower`的时候，就应该把这个最开始的`ups.sh`的方案删掉就好了，明明只用前者就够了（

## 0x05.后记
事实再一次证明了笔记本盘不能用于`7*24h`，包括台式机里的普通家用硬盘（如希捷酷鱼），还是一分价钱一分货得上企业级的（`tb`灵车它不香吗？）或者说是`NAS`硬盘（如希捷酷狼）
当然，这个笔记本硬盘也不是自己的，创建虚拟机的时候也压根没有把数据放在了随时都可能被点爆的笔记本硬盘上的意识（根本不知道这是一块笔记本硬盘
最后看下损失，这些全部木大（自己的主要是`HA`和`cn-py-dl-c8`）[#107807854876297870](https://mastodon.yuangezhizao.cn/@yuangezhizao/107807854876297870)
虽然没啥极其重要的东西，但是那里面随着时间一点点积累的东西一下子就都木大了还是挺心疼的（不仅限于`cn-py-dl-c8`上的`mongo`里就存着爬虫的千万级破站视频`api`信息），呜呜呜~`(ಥ_ಥ)`
