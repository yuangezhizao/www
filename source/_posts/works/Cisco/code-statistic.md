---
title: 一些关于代码量的统计方法
date: 2022-03-27 23:49:49
tags:
  - git
  - WakaTime
  - Wakapi
count: 2
os: 1
os_1: Monterry 12.3 (21E230)
browser: 0
browser_0: 99.0.4844.84 Stable
place: 新家
key: 136
---
    爆肝了一个月，从来没有这么累过（身体有点儿顶不住了，被迫体调不良请假
<!-- more -->
## 0x00.前言
现在只想每天晚上能睡个好觉，可谁能想到连这都变成一件奢侈的事情了
![心态炸裂](https://i1.yuangezhizao.cn/macOS/20220328011618.png!webp)

## 0x01.`GitHub Contributions`
没错，脑海里第一个浮现的就是那张「地铁站都比你努力」的推图，可惜原推找不到了

<details><summary>点击此处 ← 查看折叠</summary>

![害怕.jpG](https://i1.yuangezhizao.cn/macOS/20220328001517.png!webp)

</details>

参照[Learn how we count contributions](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/managing-contribution-graphs-on-your-profile/why-are-my-contributions-not-showing-up-on-my-profile)可知，如下类型会被计入
1. `Issues`、`pull requests`和`discussions`
2. `Commits`

也就是说，实际的统计量不只是`Commits`，还包括其他互动的一些方面，并且印象里当初创建一个新的空仓库也会被`+1`（注：有待考证
并且在`2022`年跨年时，自己为了恢复为原有的整`1000`数字折腾到半夜最终还是失败了（因为即使是`push -f`仍然会被计入
![2021-3D](https://i1.yuangezhizao.cn/macOS/20211231231706.png!webp)
![2021-2D](https://i1.yuangezhizao.cn/macOS/20211231231634.png!webp)

## 0x02.[Lakr233/myyearwithgit](https://github.com/Lakr233/myyearwithgit)
> 我和我的代码，还有这一年。

这是单独针对于`git`仓库进行分析的`app`，仅限`macOS`平台，不过从结果来看并不符合预期，明明自己写的最多的应该是`.py`才对，却因为创建过前端项目反倒是`HTML`变成第一了草

<details><summary>点击此处 ← 查看折叠</summary>

![1](https://i1.yuangezhizao.cn/macOS/QQ20211231-234713@2x.png!webp)
![2](https://i1.yuangezhizao.cn/macOS/QQ20211231-234729@2x.png!webp)
![3](https://i1.yuangezhizao.cn/macOS/QQ20211231-234747@2x.png!webp)
![4](https://i1.yuangezhizao.cn/macOS/QQ20211231-234755@2x.png!webp)
![5](https://i1.yuangezhizao.cn/macOS/QQ20211231-234804@2x.png!webp)
![6](https://i1.yuangezhizao.cn/macOS/QQ20211231-234814@2x.png!webp)
![7](https://i1.yuangezhizao.cn/macOS/QQ20211231-234825@2x.png!webp)
![8](https://i1.yuangezhizao.cn/macOS/QQ20211231-234839@2x.png!webp)

</details>

## 0x03.`Productivity Guide`
接下来是`JB`家的`IDE`，虽然是针针对于快捷键而不是代码量的统计，但还是列出来吧，也不一定有多少人知道
这里拿`PyCharm`举例子，在「帮助」里，中文翻译成了「我的工作效率」
![我的代码效率](https://i1.yuangezhizao.cn/macOS/20220328003359.png!webp)

嗯？第一名竟然不是自动补全
![](https://i1.yuangezhizao.cn/macOS/20220328003532.png!webp)

## 0x04.[WakaTime](https://wakatime.com/)
前面说了那么多，终于来到重头戏了，这是统计写代码时长的网站，是真正的那种只有打字才会统计的那种，干放着无操作不会被计入时长（应该是
常用的编辑器`VSCode`、`PyCharm`等都有插件可以安装

<details><summary>点击此处 ← 查看折叠</summary>

![上半月存档](https://mastodon-1251901037.cos.ap-beijing.myqcloud.com/media_attachments/files/107/967/025/333/423/985/original/57e03c2964ace0c0.png)
![上半月存档](https://mastodon-1251901037.cos.ap-beijing.myqcloud.com/media_attachments/files/107/967/026/900/389/236/original/03be27e1399b16d7.png)

</details>

![总览](https://i1.yuangezhizao.cn/macOS/20220328010509.png!webp)
![项目](https://i1.yuangezhizao.cn/macOS/20220328011204.png!webp)

上周
![周一](https://i1.yuangezhizao.cn/macOS/20220328010743.png!webp)
![周二](https://i1.yuangezhizao.cn/macOS/20220328010730.png!webp)
![周三](https://i1.yuangezhizao.cn/macOS/20220328010710.png!webp)
![周四，虽然白天请假](https://i1.yuangezhizao.cn/macOS/20220328010654.png!webp)
![周五](https://i1.yuangezhizao.cn/macOS/20220328010640.png!webp)
![周六](https://i1.yuangezhizao.cn/macOS/20220328010627.png!webp)
![周日](https://i1.yuangezhizao.cn/macOS/20220328010609.png!webp)

上上周
![周一](https://i1.yuangezhizao.cn/macOS/20220328010855.png!webp)
![周二](https://i1.yuangezhizao.cn/macOS/20220328010842.png!webp)
![周三](https://i1.yuangezhizao.cn/macOS/20220328010831.png!webp)
![周四](https://i1.yuangezhizao.cn/macOS/20220328010821.png!webp)
![周五](https://i1.yuangezhizao.cn/macOS/20220328010810.png!webp)
![周日](https://i1.yuangezhizao.cn/macOS/20220328010754.png!webp)

而配置文件只有一处，位于用户文件夹下的`.wakatime.cfg`，没错就是个`api_key`

<details><summary>点击此处 ← 查看折叠</summary>

``` bash
yuangezhizao@MacMini ~ % cat .wakatime.cfg
[settings]
api_key = <rm>

[internal]
backoff_at      =
backoff_retries = 0
```

</details>

官方免费版支持查看最近两周的记录，再久的需要花钱升级到`Premium`，但是这个价格属实劝退

<details><summary>点击此处 ← 查看折叠</summary>

![月 9 刀](https://i1.yuangezhizao.cn/macOS/20220328004524.png!webp)
![年 99 刀](https://i1.yuangezhizao.cn/macOS/20220328004457.png!webp)

</details>

那么有没有白嫖的方法呢？答案自然是肯定的
1. 一是可以定时导出每天的粗略统计，参照：https://gist.github.com/yuangezhizao/25d568c20912e81fdfe71d3a4d049b6d
2. 另外则是搭建开源的第三方兼容服务端，比如下面这个

## 0x05.[wakapi](https://github.com/muety/wakapi)
> A minimalist, self-hosted WakaTime-compatible backend for coding statistics.

比如这个月过去的四周，总`96 hrs 14 mins`，其中`73 hrs 57 mins`除以`16 days`（除去有例会的周一）约等于`4.625`小时每天，就算除以`20 days`也能得到`3.7`小时每天
这个数值可以用来精准衡量每天的撸码时长（确信
![summary](https://i1.yuangezhizao.cn/macOS/20220328005506.png!webp)
![Project](https://i1.yuangezhizao.cn/macOS/20220328005610.png!webp)

## 0x06.后记
在经历了[2 月](../../Linux/TencentOS-tiny/board/EVB_AIoT/init.html#0x00-前言)和[3 月](../../Linux/TencentOS-tiny/board/EVB_AIoT/eiq.html#0x01-前言)之后，希望自己能恢复到正常状态，总得好起来吧

未完待续……