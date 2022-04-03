---
title: 从零开始的 Redmi K20Pro 生活
date: 2020-1-14 18:24:59
tags:
  - Android
count: 1
os: 0
os_1: 10.0.17763.914 2019-LTSC
browser: 0
browser_1: 74.0.3729.169 Stable
place: 新家
key: 67
---
    解 BL 锁竟然是格式化草
    解锁一时爽，重启火葬场
    本文加入了大量颜文字哦
<!-- more -->
## 0x00.前言
昨天~~摸鱼~~的时候看到了[我家 Android 初养成](https://web.archive.org/web/20200114105238/https://diygod.me/android/)，意外发现是同型号，于是就有了这篇文章`(*•ω•)`
去年双十一意外领到了`¥500`无门槛全品白条券而购买的`Lenovo Z5`逐渐脱离时代了，于是今年准备继续领券之后立即购买，结果没领着
但是`K20Pro`还是走预售购买了草`(〃'▽'〃)`

![Lenovo Z5](https://i1.yuangezhizao.cn/Win-10/20200114183728.png!webp)
![¥649.64](https://i1.yuangezhizao.cn/Win-10/20200114184104.jpg!webp)
![-500](https://cors.yuangezhizao.workers.dev/?url=https://b290.photo.store.qq.com/psb?/V142qzsq49uFaJ/NXvLYPUPtZyvSwtoqWKDkDT84U4GvIqZ83.3h*i8tjM!/b/dCIBAAAAAAAA&bo=AAYACgAGAAoRECc!)
![Redmi K20Pro](https://i1.yuangezhizao.cn/Win-10/20200114183332.png!webp)
![¥2499.00](https://i1.yuangezhizao.cn/Win-10/20200114183650.jpg!webp)

突然感觉好贵啊，但是想着好歹是`855 Plus`+`8`+`512`，嗯，还是物有所值的`(；´д｀)ゞ`

## 0x01.解锁`Bootloader`
没错就是那个`BL`，其实之前`Z5`只需在`开发者选项`中点开`OEM 解锁`再重启就`ok`了`(^_−)☆`
![OEM 解锁](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-14-18-55-53-111_com.android.se.jpg!webp)

结果`K20`这里倒是可以直接点开，然而好像并没有什么卵用`(艹皿艹)`
所以「我们仍未知道这个开关点开的作用」，于是去[走流程](https://web.archive.org/web/20200114120513/http://www.miui.com/unlock/index.html)`(o°ω°o)`，结果也不知道`Cent Browser`到底是怎么了，死活进不去`(T＿T)`

![草](https://i1.yuangezhizao.cn/Win-10/20200114195312.jpg!webp)
![立即解锁](https://i1.yuangezhizao.cn/Win-10/20200114195725.jpg!webp)
![502 草](https://i1.yuangezhizao.cn/Win-10/20200114195844.jpg!webp)

解锁之前虽然看到了提示，但想到**可能**只是`清除数据`而不是`格式化内置存储`，怀着侥幸的心理只备份了`wx`到`pc`以及微软桌面云同步
顺手拿自带小米同步工具同步了下通讯录、短信等就一心想着赶紧解锁而没管其他东西了……（其实也就少个`DCIM`和`QQfile_recv`等

![运行解锁工具](https://i1.yuangezhizao.cn/Win-10/20200113204732.jpg!webp)
![免责声明](https://i1.yuangezhizao.cn/Win-10/20200113204648.jpg!webp)
![连接不能](https://i1.yuangezhizao.cn/Win-10/20200113204822.jpg!webp)
![安装驱动](https://i1.yuangezhizao.cn/Win-10/20200113205200.jpg!webp)
![解锁确认](https://i1.yuangezhizao.cn/Win-10/20200113205336.jpg!webp)
![解锁再确认](https://i1.yuangezhizao.cn/Win-10/20200113205347.jpg!webp)
![解锁成功](https://i1.yuangezhizao.cn/Win-10/20200113205404.jpg!webp)

结果重启之后就懵逼了，非常淡定地打开图库：`无图片`，又去自带`文件管理`看了眼，这才确信确实是格式化了草
当场翻车，原地爆炸
![草](https://i1.yuangezhizao.cn/Win-10/20191016005155.jpg!webp)
![草 * 2](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-13-21-05-59-693_com.android.se.jpg!webp)

然后次日也就是今天想了下昨晚还是太着急了，从旧`Z5`迁移过来的一年数据和`K20`俩月使用痕迹消失匿迹
虽然大部分扯淡的东西都扔在空间里了，但还是有不少照片（冬天去东港威尼斯水城那次）就这么一瞬间没了。。。`(ಥ﹏ಥ)`
倒是以另外的方式整理了一直没去整理的内置存储不限于`QQfile_recv`，虽没意识到有什么很重要的东西，不过也可能永远也想不起来了`(｀・ω・´)`
话说都`512 GB`存储了还整理个`p`啊，喂！
经验：之后的话相册还是定期迁移到`pc`上吧`(￣.￣)`

## 0x02.刷入[TWRP](https://twrp.me/)
直接扔出大佬微博：[wzsx150](https://weibo.com/u/6033736159)，以及[LR.Team定制版TWRP下载地址集合](https://weibo.com/ttarticle/p/show?id=2309404160776561631202)

![运行](https://i1.yuangezhizao.cn/Win-10/20200113210645.jpg!webp)
![1](https://i1.yuangezhizao.cn/Win-10/20200113210657.jpg!webp)
![下一步](https://i1.yuangezhizao.cn/Win-10/20200113210711.jpg!webp)
![等待](https://i1.yuangezhizao.cn/Win-10/20200113210735.jpg!webp)
![等待](https://i1.yuangezhizao.cn/Win-10/20200113210749.jpg!webp)
![完成](https://i1.yuangezhizao.cn/Win-10/20200113210806.jpg!webp)

首先要解密`data`分区，小米的解密密码就是锁屏密码，然后`TWRP`竟然提供了图形化解锁，好评！
（之前`Z5`只能输入密码于是就只能线刷了草
![滑动](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-13-21-08-54.png!webp)
![高级](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-13-21-09-07.png!webp)
![Root](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-13-21-09-50.png!webp)

## 0x03.刷入[Magisk](https://github.com/topjohnwu/Magisk)
> `Magisk`是一个兼具稳定性和可玩性的神器：作为一个`Root`方案，它能不破坏系统实现无痛`OTA`，作为一个插件扩展平台，它又能提供丰富的自定义模块来满足多样化的定制需求

重启之后就会发现`Magisk Manager`已经安好了，这里升级到最新`ヾ(✿ﾟ▽ﾟ)ノ`
![更新](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-13-21-48-50-354_com.topjohnwu..jpg!webp)
![最新](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-13-21-50-25-124_com.topjohnwu..jpg!webp)

## 0x04.太极
然后就可以安装模块了`hhh`，比如这里安装的`太极`，主要还是`xp`框架暂未支持安卓十过草

![安装](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-14-20-50-16-168_com.topjohnwu..jpg!webp)
![太极](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-14-20-54-51-953_me.weishu.exp.jpg!webp)

## 0x05.谷歌相机
> `Redmi K20 Pro`支持`Camera2 API`，所以不需要额外折腾就可以安装`Google`相机<br>
国内开发者阿狗酱有分享专门为`Redmi K20 Pro`调教的谷歌相机

继续扔大佬微博，[阿狗酱](https://weibo.com/u/5213532617)
`HDR+`拍夜景很强
![吊炸天](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-14-21-00-01-611_org.codeaurora.jpg!webp)

支持`RAW`格式惊了，拓展名是`.dng`
![RAW](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-14-21-01-34-548_org.codeaurora.jpg!webp)

未完待续……