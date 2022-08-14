---
title: 腾讯 TencentOS tiny 官方定制 IoT 开发板 EVB_AIoT
date: 2022-02-26 21:33:48
tags:
  - TencentOS-tiny
  - EVB_AIoT
  - RT1062
count: 4
os: 1
os_1: Monterry 12.2.1 (21D62)
browser: 0
browser_1: 98.0.4758.109 Stable
place: 新家
key: 133
---
    #StandWithUkriane 🇺🇦
<!-- more -->
## 0x00.前言
<span title="你知道的太多了" class="heimu">最近过于浮躁，啥都想干又啥都没干（心情不好
回连后才不到两周（`13`天），刷推就经历了三波大新闻，一个比一个劲爆
要么是因为作息不规律，放飞自我晚睡晚起也没人管；要么是一直想去刷推看现在怎么样了，比如前晚凌晨三点「睡不着起来上了趟厕所，又去看了眼现在怎么样了」
明明有很多正经的事情要做（鹅厂比赛，录的网课，新买的书），却一直还像春节假期那样只想着先看番度日，总之还是得回归正轨，不然心里的石头一直落不下负担太大了</span>
时隔两年，二期[2021 TencentOS Tiny AIoT应用创新大赛](https://web.archive.org/web/20220307120534/https://cloud.tencent.com/developer/competition/introduction/10032)终于来了，这次的开发板核心板芯片从`STM32L4`换成了`i.MX RT1062`
`i.MX RT`系列`MCU`是`NXP`的**跨界处理器**，既具备高频率（最高主频`600M`）、高处理性能，又具备中断响应迅速、实时性高的特点（而非传统的微控制器或微处理器
> 一期关联文章：[腾讯 TencentOS tiny 官方定制 IoT 开发板 EVB_MX_Plus](../EVB-MX-Plus/init.html)，[EVB_MX_Plus 对接腾讯云物联网开发平台](../EVB-MX-Plus/qcloud-iot-explorer.html)，[【IOT应用创新大赛】基于 EVB_MX_Plus 的盆栽土壤监测](../EVB-MX-Plus/flower.html)

## 0x01.快速入门
首先，把`6`个比赛直播视频给看完

序号 | 标题 | 备注
:---: | :---: | :---:
`1` | `1.汪礼超-TencentOS Tiny物联网操作系统简介及AIoT开发板软硬件开发环境入门简介.mp4` | 鹅厂大佬（`tql`
`2` | `2.王世伟-TencentOS Tiny内核移植与腾讯云物联网平台对接入门指南.mp4` | 鹅厂大佬（直播演示上云
`3` | `3.衡杰nxp RT106x芯片开发快速指南.mp4` | `NXP`大佬
`4` | `4.洪晓峦-基于腾讯连连、TencentOS Tiny 快速建立AloT小程序应用` | 声音可爱的鹅厂妹子
`5` | `5.杨瑞-ARM CMSIS NN加速库在TencentOS Tiny上的应用介绍.mp4` | 是大佬
`6` | `6.张岩 基于i.MXRT1062的AIoT应用解决方案.mp4` | 是大佬

然后，把微信公众号文章通读一遍，主要来自`wx`群里分享的链接

序号 | 标题 | 来源
:---: | :---: | :---:
`1` | [i.MX RT1062助力TencentOS Tiny AIoT应用创新大赛](https://web.archive.org/web/20220307123217/https://mp.weixin.qq.com/s?__biz=MzI3NDYwOTQ5Mg%3D%3D&mid=2247489403&idx=2&sn=c2c5580e26e62d7785f222de1a715640) | 恩智浦MCU加油站
`2` | [移植i.MX RT1062 SDK工程至腾讯EVB_AIOT开发板](https://web.archive.org/web/20220307123104/https://mp.weixin.qq.com/s?__biz=MzI3NDYwOTQ5Mg%3D%3D&mid=2247489703&idx=1&sn=e15d47d588f08d6c2492bd1f4e0f3182) | 恩智浦MCU加油站
`3` | [TencentOS Tiny EVB_AIoT开发板环境搭建与点灯](https://web.archive.org/web/20220307123653/https://mp.weixin.qq.com/s?__biz=MzU0MzQzMzc5Nw%3D%3D&mid=2247488772&idx=1&sn=f7324446713f32c212ee6f332ada1359) | 痞子衡嵌入式
`4` | [TencentOS Tiny EVB_AIoT开发板在Flash调试与离线启动](https://web.archive.org/web/20220307123818/https://mp.weixin.qq.com/s?__biz=MzU0MzQzMzc5Nw%3D%3D&mid=2247488788&idx=1&sn=8dbfee385ad3215633c3e225b772ef45) | 痞子衡嵌入式
`5` | [i.MXRT1062 & 使用 IOMUXC 和 GPIO 点亮LED](https://web.archive.org/web/20220307124919/https://mp.weixin.qq.com/s?__biz=MzUyMTE0NTA2Ng%3D%3D&mid=2247487157&idx=1&sn=0e5beb407a96f0441620f823b502e607) | mculover666
`6` | [i.MX RT1062 嵌套中断向量控制器NVIC](https://web.archive.org/web/20220307125512/https://mp.weixin.qq.com/s?__biz=MzUyMTE0NTA2Ng%3D%3D&mid=2247487192&idx=1&sn=8251c5b9663525e4be0fd98a056545fa) | mculover666
`7` | [#恩智浦开发工具](https://web.archive.org/web/20220307123420/https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzU0MzQzMzc5Nw%3D%3D&action=getalbum&album_id=1522554051819864065) | 痞子衡嵌入式

最后，看一篇大佬的比赛作品，基本上就差不多可以做到心中有数了

序号 | 标题 | 备注
:---: | :---: | :---:
`3` | [AIoT应用创新大赛-基于TencentOS Tiny 的会议室使用小助手](https://web.archive.org/web/20220307125656/https://cloud.tencent.com/developer/article/1940558) | 
`2` | [AIoT应用创新大赛-keil开发--(2)移植TencentOS tiny与对接腾讯云IoT](https://web.archive.org/web/20220307130140/https://cloud.tencent.com/developer/article/1931085) | 
`1` | [AIoT应用创新大赛-keil开发--(1)前期准备与Hello World](https://web.archive.org/web/20220307125911/https://cloud.tencent.com/developer/article/1925881) | 

> 感谢上述大佬们的参考资料，让「一个小白」也可以快速入门

## 0x02.移植上云
这里说的移植是指移植[TencentOS-tiny](https://github.com/OpenAtomFoundation/TencentOS-tiny)，没错现在代码仓库已经迁移到`OpenAtomFoundation`而不是`Tencent`组织下了，上云自然指的是`腾讯云物联网开发平台`了
先跟着直播视频搭建过一遍之后，自己又从零把`Camera_ov5640`下的`evkmimxrt1060_csi_rgb565`例程成功移植并上云（可以同时跑多个任务），确信自己搞定是没啥问题了
其实主要的操作就是复制需要的文件夹，然后修改`IDE`的宏和头文件配置，并补充`include`语句，最后调试（烧录）个几十次就行了（<span title="你知道的太多了" class="heimu">是不是听起来很简单？</span>
> 这里[#107905771053979130](https://mastodon.yuangezhizao.cn/web/statuses/107905771053979130)是前天**周日凌晨**搞到**四点半**的自己（<span title="你知道的太多了" class="heimu">猝死倒计时</span>
下午睡醒才想起去`wx`群里求助，在汪总的帮助下才给解决掉：`APPLICATION_TASK_STK_SIZE`太小`512`不够用，试了下`4096`不报错了

## 0x03.选题恐惧症
毕竟是比赛，再整一个烂大街的温湿度传感器实在是太`low`了，毕竟一期选题中已经用到过，不能比赛芯片都换了，参赛的传感器还不换草
也确实选题足够折磨人，直到现在脑海中也想不出更好的现实场景，预想的选题是控制舵机操作远程主机的开关机，有点像`SWITCH`那个意思
但后来又仔细想了一想，这就一个开关上云好像比温湿度传感器害`low`草，不能辜负了比赛举办方满满的诚意，免费的开发板还附赠`4.3`寸`800*480`显示屏
在最近一周突击比赛直播视频和微信公众号文章之后，发现这芯片可以跑机器学习，这不得搞一个玩玩，光速拿`wx`群里的人脸识别例程抄作业，烧录后看到实际效果还不错
同时最近几天看到`wx`群里有人也在讨论`eip`，决定先搞个`eip`做做看吧……

## 0x04.资源利用计划
序号 | 资源 | 备注
:---: | :---: | :---:
`1` | 摄像头 | ✔️
`2` | 显示屏 | ✔️
`3` | 触摸屏 | ❌（无现成驱动）
`4` | 语音采集 | ❌（板上硬件需修改，`Clara`需商业授权）
`5` | 语音播放 | ❌（`3.5mm`耳机孔输出）

## 0x05.后记
`deadline`临近，可惜最近工作有亿点忙，工作日实在是抽不出太多的时间，只能周末爆肝重操（嵌入式老本行）旧业了……
<span title="你知道的太多了" class="heimu">因为是凌晨三点睡的，睡醒就下午一点，吃完煮的水饺就困了，结果又睡着了这次醒来是五点，周六这一天就只剩晚上了，心塞（并且睡多了现在脑袋开始迷糊了草</span>
