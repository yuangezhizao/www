---
title: 总日漫表迁移 Next.js 的重构之路
date: 2021-11-07 00:23:29
tags:
  - Next.js
  - React
count: 1
os: 1
os_1: Monterry 12.0.1 (21A559)
browser: 1
browser_1: 95.0.4638.69 Stable
place: 新家
key: 124
---
    也算是历史性的重构，终于用上前端框架了
<!-- more -->
## 0x00.前言
本来前天晚上在写的是这篇文章，结果故事太长昨天又花了一整天，凌晨前总算是差不多给搞定了，于是终于可以来填这篇的坑了

## 0x01.缘由
最直接的原因是谷歌搜索`远哥制造的实验室`搜索不到`https://lab.yuangezhizao.cn/`了，通过`inurl`搜索语法发现被索引的只有`6`条

<details><summary>点击此处 ← 查看折叠</summary>

![inurl](https://i1.yuangezhizao.cn/macOS/20211107003123.png!webp)

</details>

翻`QZone`又想起这个站点其实最开始是叫**远哥应用**（~~`https://app.yuangezhizao.cn/`~~），后来觉得自己专业接触不到像计算机专业的实验室，于是自己就采用了**实验室**这个名字……
里面放着自己基于`Flask`折腾出的各种小应用，不过随着时间的流逝，不具时效性的玩楞越来越多，而有意义的相对独立的应用比如[maimai_DX 查分器](https://maimai.yuangezhizao.cn/)是被单独分配了子域名
趁着这次搜索翻车，再加上出于对`SEO`的考虑决定给**总日漫表**也单独分配`bgmlist`子域，然后将从**实验室**迁移出去
就像`查分器`一样在**实验室**中仅留存一条指向的链接以备留念，也算是在**实验室**完成了自己的使命`2333`

## 0x02.历史
虽然前一篇文章已经花费了大量的笔墨进行了描述，这里针对**总日漫表**部分还是再回顾一下吧
最初版的页面是在`180523`提出的，而`180530`才使用`git`管理**实验室**整个项目

<details><summary>点击此处 ← 查看折叠</summary>

![最初版](https://i1.yuangezhizao.cn/macOS/20211106222500.png!webp)

</details>

最初版页面字段非常有限，直到`190407`才修改数据库模型丰富字段，并类似于现在使用的页面

<details><summary>点击此处 ← 查看折叠</summary>

![190407](https://i1.yuangezhizao.cn/macOS/QQ20211107-005749@2x.png!webp)

</details>

而下一次修改则鸽到了`200310`，主要是追加了`制作公司`字段，并且真正意义上的开始对外公开
![200310](https://i1.yuangezhizao.cn/macOS/20211106225742.png!webp)

接下来，来看一下`200310`后针对`bangumi_200310.html`的所有改动

<details><summary>点击此处 ← 查看折叠</summary>

![bangumi_200310.html](https://i1.yuangezhizao.cn/macOS/20211107011431.png!webp)

</details>

最后，贴一下在`git`中搜索`bangumi`得到的全部提交记录

<details><summary>点击此处 ← 查看折叠</summary>

![1](https://i1.yuangezhizao.cn/macOS/20211107010940.png!webp)
![2](https://i1.yuangezhizao.cn/macOS/20211107011039.png!webp)

</details>

真的是经过无数次重构，最终演变成现在看到的页面

<details><summary>点击此处 ← 查看折叠</summary>

![201004](https://i1.yuangezhizao.cn/macOS/20211106231042.png!webp)

</details>

未完待续……