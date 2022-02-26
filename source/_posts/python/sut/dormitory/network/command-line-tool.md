---
title: SUTDN 命令行工具
date: 2017-9-15 15:29:31
tags:
  - SUTDN
count: 3
os: 0
os_1: 10.0.15063 Pro
browser: 0
browser_0: 61.0.3163.91 Dev
place: 宿舍
key: 25
gitment: true
---
    这是最近在写的个人在用一个小工具，感冒终于好转的说～
<!-- more -->
## 0x00.前言
    SUTDN（SUT Dormitory Network）
宿舍网络的运营商有且只有一种：`联通`，并且与校园网（总出口是`移动、电信和教育网`）没有任何关系，使用的是`锐捷`的产品，登陆操作在网页就能完成（`e-Protal`）且无需下载任何客户端，说到这里你可能就要问我就一个网页就能登录还写什么命令行工具？emmm……问题在于`PC`端的网页不能关（后抓包发现关闭会发送下线数据包，虽然有方法可破比如任务管理器暴力结束进程或者用`The Great Suspender`插件先`Suspende this tab`再关闭，但是还是很不舒服），所以干脆写个小工具出来好了，一劳永逸，顺便补一补基础……

## 0x01.开工
打开`Fiddler`，只监听浏览器的进程，进行一系列抓包操作并保存，随后就可以根据规律写出对应的脚本了，问题并不难，只是情况比较多，就拿用户登录的返回结果来说，我发现的足足有`8`种。具体的请求细节没啥好说的，没有意义的说……

## 0x02.经验
用户状态信息是根据`cookies`中的`jsessionid`鉴别的，用`requests`库写的时候最好把`session`放到类的初始化中去，免得`3`次登录失败就谈验证码（此法可破），即`self.session = requests.Session()`
![黑历史](https://i1.yuangezhizao.cn/macOS/20211106165626.png!webp)
![存档](https://i1.yuangezhizao.cn/Win-10/20171108214951.jpg!webp)
![开源](https://i1.yuangezhizao.cn/macOS/20211106170406.png!webp)

## 0x03.源码
https://github.com/yuangezhizao/SUTDN

## 0x04.参考
> https://github.com/j178/ipgw
