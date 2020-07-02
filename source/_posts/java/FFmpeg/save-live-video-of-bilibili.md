---
title: 用 FFmpeg 保存 bilibili 直播视频
date: 2017-7-24 16:04:12
tags:
  - FFmpeg
  - java
count: 2
os: 0
os_1: 10.0.14393 Pro
browser: 0
browser_1: 61.0.3153.0 Dev
place: 家
key: 10
gitment: true
---
    这就是我 7.21～23 这三天忙的事情……
    内含视频福利……（7-31 updated）
<!-- more -->
## 0x00.先行版
### 【720P】拔剑神曲
<video controls="controls" poster="https://i1.yuangezhizao.cn/403.png!webp" src="https://v1.yuangezhizao.cn/av12421316.mp4" preload="none">
您的浏览器不支持 video 标签。
</video>

### 【1080P】夜舞
<video controls="controls" poster="https://i1.yuangezhizao.cn/Win-10/20170724112021.jpg!webp" src="https://v1.yuangezhizao.cn/av12524206.mp4" preload="none">
您的浏览器不支持 video 标签。
</video>

### 【1080P】追光使者
<video controls="controls" poster="https://i1.yuangezhizao.cn/Win-10/20170724112319.jpg!webp" src="https://v1.yuangezhizao.cn/av12524302.mp4" preload="none">
您的浏览器不支持 video 标签。
</video>

### 【1080P】CONNECT
<video controls="controls" poster="https://i1.yuangezhizao.cn/Win-10/20170802181613.jpg!webp" src="https://v1.yuangezhizao.cn/5086-2017-07-21-17-16-27_pr-1.mp4" preload="none">
您的浏览器不支持 video 标签。
</video>

### 【1080P】ONE WEEK
<video controls="controls" poster="https://i1.yuangezhizao.cn/Win-10/20170802181008.jpg!webp" src="https://v1.yuangezhizao.cn/5086-2017-07-21-17-16-27_pr-2.mp4" preload="none">
您的浏览器不支持 video 标签。
</video>

### 【1080P】Poker Face
<video controls="controls" poster="https://i1.yuangezhizao.cn/Win-10/20170802181423.jpg!webp" src="https://v1.yuangezhizao.cn/5086-2017-07-21-17-31-38_pr-2.mp4" preload="none">
您的浏览器不支持 video 标签。
</video>

### 【1080P】*（不会打日文）
<video controls="controls" src="https://v1.yuangezhizao.cn/5086-2017-07-21-17-31-38_pr-1.mp4" preload="none">
您的浏览器不支持 video 标签。
</video>

### 【720P】极乐净土
<video controls="controls" src="https://v1.yuangezhizao.cn/5086-2017-7-23-12-26-24_pr.mp4" preload="none">
您的浏览器不支持 video 标签。
</video>

### 【1080P】BML 开场
<video controls="controls" poster="https://i1.yuangezhizao.cn/Win-10/20170802181916.jpg!webp" src="https://v1.yuangezhizao.cn/5086-2017-07-23-16-51-54_pr.mp4" preload="none">
您的浏览器不支持 video 标签。
</video>

### 【720P】2233
<video controls="controls" poster="https://i1.yuangezhizao.cn/Win-10/20170802181756.jpg!webp" src="https://v1.yuangezhizao.cn/20006-2017-7-22-9-48-26_AVS.mp4" preload="none">
您的浏览器不支持 video 标签。
</video>

~~未完待续……~~
~~（感觉`HTTPS`的视频地址好卡……干脆去了）~~
## 0x01.缘由
`Bilibili World 2017`要开始了，然而并不能去现场（车费大于票费系列），但是看看直播总是可以的吧……21 号早发现直播是同时进行的且不止一个，这……于是乎想存下来慢慢享受（并挖了个新坑）……

## 0x02.三种方法

### 1. [liverecord.groovy](https://gist.github.com/sunny00123/4e69283b930f0f3a36244237797be9d0)
来自`av4568222`评论

关于如何在`Win`下配置`Groovy`环境请参考此文章：
> http://www.jianshu.com/p/777cc61a6202

### 2. [biliroku](https://github.com/zyzsdy/biliroku)——`bilibili`生放送（直播）录制
开源，地址如上所示

### 3. [B站录播机](http://live.weibo333.com)——不再错过每一场直播
闭源，录制两个以上房间 or 下载弹幕需要付费

## 0x03.优缺点
1优点：自动分时（其他两种无此）；自动检测直播开始
1缺点：手动结束进程时文件已损坏，只好等录完整小段再停止

2优点：可以暂停（其他两种无此）；自动检测直播开始；界面非常标准
2缺点：暂无！

3优点：自动检测直播开始；界面精致……
3缺点：比较消耗系统资源（放在服务器上`CPU`打满过）；不能暂停，单文件达到了`5G`

## 0x04.我的使用

本机：3
原因：尝鲜（测试稳定性）

服务器（阿里云）：2
原因：个人最推荐这个，可以打开多个窗口进行多录制

服务器（百度云）：1
原因：备份档，在稳定状况下需要保持稳定

##  0x05.文件概览
占位补图
```
主舞台
5086
脱口秀舞台
308892
……游戏舞台
……4891353
交友舞台
4891366
freestyle
20006
……主播
……5440
bilibili world 2233厨房直播间
4891387
bilibiliworld-黑白键
4891390
bilibiliworld-da'kao'c
4891394
Bilibili World天下第一麒麟臂的直播间
4891402
BiliBiliWorld-娃娃机
4891405
Bilibiliword-世界之海
4891412
Bilibili World 哔哩哔哩小屋生放送
4891419
bilibili world 直播用爱发电
4891426
nike react 缓震空间
1563089
```
