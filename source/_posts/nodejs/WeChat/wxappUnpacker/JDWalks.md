---
title: 微信小程序“奔跑吧少东家”解包
date: 2019-5-8 16:47:52
tags:
  - WeChat
  - JDWalks
count: 1
os: 0
os_1: 10.0.17763.475 2019-LTSC
browser: 0
browser_1: 72.0.3626.121 Stable
place: 家
key: 48
---
    https://github.com/qwerty472123/wxappUnpacker
<!-- more -->

## 0x00.获取`wxapkg`包
安卓已`root`手机进入到`/data/data/com.tencent.mm/MicroMsg/<rm>/appbrand/pkg/`目录下，一看`_1268812133_73.wxapkg`这个就是了。`1268812133`是不变的，`73`会随着小程序的版本而变化，我手里最早有`29`的版本。

## 0x01.`wxappUnpacker`解包
解包巨占版面，https://gist.github.com/yuangezhizao/84786987b4a4456f56e782d6c8addcf6
报错，去`gh`的`issues`搜`__vd_version_info__ is not defined`，有俩结果，第一个[#237](https://github.com/qwerty472123/wxappUnpacker/issues/237)里有一种解决方法：https://github.com/qwerty472123/wxappUnpacker/issues/237#issuecomment-483921630
重新运行，问题解决，https://gist.github.com/yuangezhizao/2529a086e1d222e8abf37f21e423bb97
![更多资料](https://i1.yuangezhizao.cn/Lenovo-Z5/Screenshot_2019-05-08-17-11-39-1005645939.png!webp)

这里能直接看到`AppID`，并不需要网上所说的繁琐的抓包操作，然而并没有什么卵用……
或者`referer: https://servicewechat.com/wxe0520fb14cfac990/73/page-frame.html`这里也能知道
![设置](https://i1.yuangezhizao.cn/Lenovo-Z5/Screenshot_2019-05-08-17-15-58-1639594540.png!webp)

hhh，毕竟依赖于步数的小程序

## 0x02.微信开发者工具
![导入项目翻车](https://i1.yuangezhizao.cn/Win-10/20190508174224.jpg!webp)

没办法只能用自己的了或者测试号，这里我选择测试号导入。
![然后就能看见熟悉的授权界面了](https://i1.yuangezhizao.cn/Win-10/20190508174815.jpg!webp)
![设置界面这俩选项勾好](https://i1.yuangezhizao.cn/Win-10/20190508175025.jpg!webp)
![并不能成功登录](https://i1.yuangezhizao.cn/Win-10/20190508175853.jpg!webp)
![真实登录抓包](https://i1.yuangezhizao.cn/Win-10/20190508180406.png!webp)

原来是缺少了地理位置信息，当然`Headers`也不一样
```
POST https://jdwalksapi.g100.org.cn/user/login HTTP/1.1
charset: utf-8
Accept-Encoding: gzip
referer: https://servicewechat.com/wxe0520fb14cfac990/73/page-frame.html
content-type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Linux; Android 8.1.0; Lenovo L78011 Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/73.0.3683.90 Mobile Safari/537.36 MicroMessenger/7.0.4.1420(0x27000437) Process/appbrand0 NetType/WIFI Language/zh_CN
Content-Length: 1250
Host: jdwalksapi.g100.org.cn
Connection: Keep-Alive
```
![更新了也不行](https://i1.yuangezhizao.cn/Win-10/20190508180747.jpg!webp)

## 0x03.WebStorm
扔进去就可以享受`JB`家的`IDE`体验了，慢慢品味码农们辛辛苦苦写的代码了（雾
![](https://i1.yuangezhizao.cn/Win-10/20190508183725.jpg!webp)

## 0x04.源码下载
https://github.com/yuangezhizao/JDWalks
