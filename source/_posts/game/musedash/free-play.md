---
title: 使用 Fiddler 白嫖 MuseDash 付费曲包
date: 2019-1-12 23:26:46
tags:
  - MuseDash
  - Fiddler
count: 1
os: 0
os_1: 10.0.17763.107 2019-LTSC
browser: 0
browser_1: 70.0.3538.110 Stable
place: 宿舍
key: 40
---
    『你可否谛听我的呢喃？』
<!-- more -->
## 0x00.前言
    毕竟是学生党，付费曲包 18 元一个……

## 0x01.工具
1. 一台安卓手机，我的是`MX4 Pro`，安卓`5.1.0`系统，已`root`（非必需）
2. [Fiddler - Free Web Debugging Proxy - Telerik](http://www.baidu.com/link?url=qDvwKqJLWy-_nV-tc45vsGr2Ci9eDKIlrL1-EuHFi4aUMOlCDoNI-ARQk3q3Azfk)![Fiddler](https://i1.yuangezhizao.cn/Win-10/20190112233023.jpg!webp)

## 0x02.方法
配好安卓手机的网络代理以及`Fiddler`的`HTTPS`抓包功能，进入游戏，遇到包含`check_xd_purchase`的请求时，在`AutoResponder`标签页中`Add Rule`，`Rule Editor`处理方式选择`Find a file...`，选择到一个内容为`{"result": "purchased"}`文本文档，点击`Save`保存规则，点击`Enable rules`使规则生效。最后，在游戏拓展包处点击`恢复购买`，弹框`恢复购买成功`，到此结束。


## 0x03.原理
首先修改购买时的金额，付款成功，曲包未发~~（浪费我一块钱）~~，确认服务端有校验支付金额；
其次，未购买时曲包返回：
![未购买](https://i1.yuangezhizao.cn/Win-10/20190112235144.png!webp)

瞎蒙判定字符，`True`，`true`，`Bought`，`bought`均无果，我是想不出来了……
最后，花`18`块钱购买，付费成功，返回：
![已购买](https://i1.yuangezhizao.cn/Win-10/20190112234733.png!webp)

得到客户端判定字符，`purchased`，`9`个字母值`18`块钱……
真贵，倒是只要知道了这个就能无限用下去了，你曲包尽管出（

## 0x04.后记
忘了是从哪个版本开始（空间里有记录懒得去翻），每次打完歌上传排行榜数据之后都会请求曲包购买检测，我以为重视起来校验了，就一直开着`AR`，结果一次意外没开，发现也能玩。好样的，合着你还是在用`恢复购买`之后本地缓存的校验，这样就又和以前一样了，可以在外面开网打歌了……

## 0x05.免责声明
> 本文的目的只有一个就是学习更多的破解技巧和思路，如果有人利用本文技术去进行非法商业获取利益带来的法律责任都是操作者自己承担，和本文以及作者没关系

未完待续……