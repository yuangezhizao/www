---
title: iPadOS 13.5 17F75 unc0ver 越狱
date: 2020-6-16 17:03:06
tags:
  - unc0ver
count: 1
os: 0
os_1: 10.0.18363.720 Pro 1909
browser: 0
browser_1: 83.0.4103.61 Stable
place: 软件园
key: 92
---
    又是在 Co. 写的草稿，真正的原始创建时间：‎2020‎-‎6‎-‎1 14:19:20
<!-- more -->
## 0x01.[AltStore](https://altstore.io/)
`13.5`有个`bug`，需要提前关闭`pad`中「卸载未使用的`App`」选项并重新安装或删除被卸载的`App`来绕过，否则会报超出`3`个`App`的限制的错误。因为`unc0ver`的`ipa`不能通过正常方法直接安装，所以需要在`pc`上安装`AltStore`和非`UWP`版的`iTunes`，登录`Apple ID`，验证密码正确之后会大概率报错，此时抓包会发现请求了`oscp`，而这个网站在国内连接不能，于是打开了全局代理保存了返回包，因为即使挂上全局代理也仍然报错，所以只能开启`Fiddler`的`AutoResponder`功能进行请求拦截，指定到之前保存的返回包的本地文件上，最终才得以成功安装（
之前的`AltStore`还不能直接安装`ipa`包，但是现在的版本是可以的

## 0x02.[unc0ver](https://unc0ver.dev/)
> The most advanced jail​break tool.<br>iOS 11.0 - 13.5

目前最新版是`2020/5/25`发布的`v5.0.1`版本，`Full-fledged support for all devices on iOS 11.0-13.5 with Cydia and tweak injection`即适配`13.5`
这也是越狱史上的一大进步，首次利用零日漏洞而并非系统安全性漏洞，目前官方已经关闭了降级到`13.4.1`的通道
~~`pc`上右键下载到的`ipa`包，用`AltStore`打开，即可通过`WiFi`或者`USB`安装到手机上~~
`pad`上使用`AltStore`打开文件，选择到`ipa`文件，这里图省事`ipa`文件是在`NAS`的共享目录里，也就省去了传到`iCloud`的愚蠢方法（因为并不知道如何传文件到`pad`里

## 0x03.`jail​break`
打开`unc0ver`，点击下方的蓝色按钮，等待第一进度走完之后重启，重启之后再次进入`unc0ver`等待第二进度走完之后重启，
重启之后就完成了
之后如果重启的话会丢失越狱，但是重新越狱的话只需重启一次就`ok`了，可以非常方便地控制系统状态（对比安卓想卸载`Root`权限可就不是简单地重启就能搞定的？
未完待续……