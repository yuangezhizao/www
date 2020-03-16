---
title: Frida 初体验
date: 2020-3-16 21:53:05
tags:
  - frida
count: 1
os: 0
os_1: 10.0.17763.1098 2019-LTSC
browser: 0
browser_1: 78.0.3904.108 Stable
place: 新家
key: 79
---
    Frida 大法好！
    标题起成荤段子了草？！
<!-- more -->
## 0x00.前言
> `cf6dbca95b470bd7392dfef9060adaeaa154f3603b857028c4f1c92c174563d9`，你懂得
（并不是密钥，谁敢公开放那玩楞？

`Xposed`动态注入是太平常不过的事情了，但是毕竟需要手写`Android`再编译下发到实机安装，还经常碰到其`class not found`的玄学错误……
折腾起来并不是最好的选择，但是也可以用……那么有没有一种更加省事情的方法了，答案是肯定的——`Frida`

## 0x01.[Frida](https://github.com/frida)
为什么突然就提及这玩楞了呢，因为最近`<rm>`东开始推广旗下的**校园`APP`**，其实早在之前就有这方面的发展，但是那次并没有？推广开来就不了了之了……
但是这次直接发布正式版安装包并且不限于举行`21`天打卡活动（奖品巨丰厚）等等，于是就去下载了个安装上看看（

## 0x02.网络
直接就连上电脑的热点并默认开启了代理，连新用户登录的请求都不想放过。。。结果这玩楞和`Magisk Hide`放到一起会产生黑魔法，具体表现如下：
①不开启`Magisk Hide`，直接提示**非法应用**之后大约`5`秒后闪退，但是在这个阶段抓包可能
![Hide](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20200316_220332.jpg!webp)
![闪退草](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-03-16-22-07-00-078_com.jd.campus.jpg!webp)

②开启`Magisk Hide`，不闪退了但是抓包不能草
![1550000](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20200316_220941.jpg!webp)

`(╯°Д°)╯︵┻━┻`绝了，没办法现在只能选择方法①，并在其有限时间内尽可能快速地完成点击操作，不难发现`Host`自然是`api.m.<rm>.com`
毕竟是客户端，和`PC`、`M`版的都没法比，猜测也可能是业务要求，必须走加密接口（这是很显然的，反正都是现成的技术，加一个`jar`包依赖也不是困难
于是，就自然看到了`64`位的签名`sign`，显然不是数出来的`hhh`
``` python
>>> len('<rm>')
64
```
并且基本上所有有用的请求都有`sign`，所以刨根问底势在必行！

## 0x03.静态分析
> 写到这里突然发现小标题和标题越来越没关系了草……

直接把整个`apk`扔进去反编译（这时候就体现出`AMD 3700X`的作用了），切换到**字符串**选项卡，直接搜索`sign`，等了一小会就出结果了，排除掉不相关的文件
矛头逐渐指向了`com.<rm>.sdk.gatewaysign.GatewaySignatureHelper`，这个实在是太眼熟了，因为之前看过`<rm>`东客户端里也有类似代码段
里面的`signature`函数简直太明显，反正没被混淆是好事情，毕竟本人也是个菜鸡，给源码都不一定看得懂
再来看加密方法，是`<rm>`但是并不知道密钥，后来才知道**交叉引用**就是搜索命令，于是注意力被引到了调用此函数的另一个文件中
看到了是`v4.add("sign", GatewaySignatureHelper.signature(v5, JDMobiSec.n1("<rm>")));`
没错，`JDMobiSec.n1("<rm>")`就是所需密钥了，然后就去翻引用`import android.content.res.JDMobiSec;`，这里不是很懂，还能这么写？引用素材资源？
但是之后乱翻在`lib/armeabi-v7a`文件夹下找到了同名的`so`库文件，那肯定就是这个了
`IDA Pro (32-bit)`启动，之所以没用`IDA Pro (64-bit)`这个是因为没法<kbd>F5</kbd>看源码哈
找到`JNI_OnLoad`，顺便看到了大面积的`sub_xxxx`那自然是混淆了，然后还没按<kbd>F5</kbd>就没调用图吓到了
![调用图](https://i1.yuangezhizao.cn/Win-10/20200315195859.png!webp)

瑟瑟发抖`.jpg`，然后再看内部
![JNI_OnLoad](https://i1.yuangezhizao.cn/Win-10/20200315200004.png!webp)

这`tm`是`JNI_OnLoad`？？？吓得直接关机……哦不，立即右上角并扔回收站
于是由于技术太菜，这条路就走到死胡同了……
卒

## 0x04.动态分析
终于可以步入主题了

### 1. 再谈[Frida](https://frida.re/)
> Inject JavaScript to explore native apps on Windows, Mac, Linux, iOS, Android, and QNX.

> `Frida`是一款基于`Python + JavaScript`的`Hook`框架，可运行在各个平台，主要使用的动态二进制插桩技术

反正就知道它可以用来`注入`就`ok`了，这个`Xposed`的原理都是差不多的，但实际实现肯定是不一样的（又想到了孵化进程）……

### 2. （客户端）[安装](https://frida.re/docs/installation/)
``` bash
C:\Users\yuangezhizao>pip install frida frida-tools
Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple
Requirement already satisfied: frida in c:\python38\lib\site-packages (12.8.14)
Requirement already satisfied: frida-tools in c:\python38\lib\site-packages (7.1.0)
Requirement already satisfied: colorama<1.0.0,>=0.2.7 in c:\python38\lib\site-packages (from frida-tools) (0.4.3)
Requirement already satisfied: prompt-toolkit<4.0.0,>=3.0.3 in c:\python38\lib\site-packages (from frida-tools) (3.0.4)
Requirement already satisfied: pygments<3.0.0,>=2.0.2 in c:\python38\lib\site-packages (from frida-tools) (2.6.1)
Requirement already satisfied: wcwidth in c:\python38\lib\site-packages (from prompt-toolkit<4.0.0,>=3.0.3->frida-tools) (0.1.8)

C:\Users\yuangezhizao>frida --version
12.8.14

C:\Users\yuangezhizao>
```

### 2. （服务端）[安装](https://frida.re/docs/android/)
这里指的服务端自然是**安卓**端了，查看手机`CPU`版本
``` bash
~$ getprop ro.product.cpu.abi
arm64-v8a
~$ 
```
然后去下载对应版本：`frida-server-12.8.14-android-arm64.xz`，解压后将**二进制文件**重命名为`frida-server`并扔到手机里
``` bash
adb push frida-server /data/local/tmp/frida-server
```
之后挂在后台运行就`ok`，设备自然是具有`Root`权限的（

## 0x05.引用
[Frida教程](https://blog.csdn.net/qingemengyue/article/details/80061491)
[Frida.Android.Practice (ssl unpinning)](https://sec.xiaomi.com/article/43)

昨天肝了一晚上肝猛了，结果还没睡好觉……刚刚写了一小时就快到十一点半了，略困（~~想要抱抱~~
今天周一破例争取零点前睡觉吧，未完待续……