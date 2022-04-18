---
title: 静态路由简析
date: 2022-04-16 21:42:29
tags:
  - CCNA
count: 2
os: 1
os_1: Monterry 12.3.1 (21E258)
browser: 0
browser_1: 100.0.4896.127 Stable
place: 新家
key: 138
---
    关键字选得好，直接一步到位
<!-- more -->
## 0x00.`TL;DR`
[11、路由基础及静态路由](https://web.archive.org/web/20220416140900/https://renyuan431.github.io/2020/05/04/11-route-basic)

## 0x01.前言
标题起得有点儿大，显然刚开始学`CCNA`的自己是不可能写出什么有价值的东西的，但是没想到的是用这个关键字搜到了一篇`2.68w`字的神文
![https://renyuan431.github.io/2020/05/04/11-route-basic](https://i1.yuangezhizao.cn/macOS/20220416220508.png!webp)

看了作者的转行网工学习经历，这也`tql`吧
![https://renyuan431.github.io/about](https://i1.yuangezhizao.cn/macOS/20220416221351.png!webp)

自己又成功水了一篇文章草……不过如果有时间的话，也可能再回来补充写下

## 0x02.后记
`4`月份的上半月已经过去，终于不再像`3`月份天天爆肝`jb`那么累了，总算是回归正轨了
![WakaTime](https://i1.yuangezhizao.cn/macOS/20220418202826.png!webp)

这周一晚上被上门核酸检测之后，开始了为期`7`天的居家隔离生活，现在已经过去`5`天，但是除了每天订外卖换成了室友们做饭，和平常没有任何的区别
趁着周末开始恶补`CCNA`，然后计划开始啃新买的`《Segment Routing 详解（第一卷）》`（`WZ`手里的第二卷实在是啃不动
那么到底是什么原因触发的呢？<span title="你知道的太多了" class="heimu">上个月爆肝`jb`受不了了</span>
说来话长，刚转行加入`Cisco`的时候其实对网络并没有太大的兴趣，所以精力一直在`Python`以及其他第三方组件上
加上开始着手的项目中（`NetFlow`、`SNMP`）所需的网络知识并不多，也并没有好好去学习
但是，欠的债迟早是要还的，只不过是自己误以为习以为常就没问题了……

## 0x03.引用
[Static routing](https://en.wikipedia.org/wiki/Static_routing)
