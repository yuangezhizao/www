---
title: 用 Pytesseract 识别验证码
date: 2018-1-16 14:12:36
tags:
  - Pytesseract
count: 2
os: 0
os_1: 10.0.17046.1000 Pro
browser: 0
browser_1: Chromium 62.0.3202.94
place: 家
key: 27
---
    2018，Happy New Year！
<!-- more -->
## 0x00.缘由
> 算是旧站存档原文，原文发布时间：2016-11-13 12:34:50

好久没在这个站写东西，是我忘记了吗？不是，是一直没有时间写点什么，~~大三的上学期确实很忙（废话划掉）~~我一直在看新东西，没有时间来写些什么……那为什么突然想起来回来看看呢？因为遇到了它，这个东西追溯起来最早是大一下学期，不过那时候是真·小白，`C`、`python`都没学，纯凭兴趣搭的，不过居然好使了，大概磨磨蹭蹭能有一周的时间，可以实现自动打码登录教务在线并查询成绩。它就是：`Pytesseract`！
> 存档原文：
首先说说为啥又要搞这个了呢？！
原因之一就是~~要叙叙旧~~换Mac系统了……
再者就是昨晚看了一眼自己以前写过的源码，实在是太烂了……于是乎下定决心要重写之……
另，网上的教程大多比较老（提供的链接地址还是`code.google.com`,现在项目已经移到`GitHub`上了）。


## 0x01.环境
a. Microsoft Windows [版本 10.0.17046.1000]（Win 10 x64 Pro Insider Preview 1709 17046.1000）
b. Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:53:40) [MSC v.1500 64 bit (AMD64)] on win32
c. JetBrains Pycharm 2017.3.2 x64 Professional
> 存档原文：
因为`pytesser`需要`Tesseract—OCR`（`pytesser`实际上只是一个方便`Python`调用`Tesseract—OCR`引擎的库）
和`PIL（Python Imaginary Library）`的支持，所以要先安装这两个包。

## 0x02.安装
#### 1. 安装[PIL](http://www.pythonware.com/products/pil/)
不要用上面那个链接，那个`PIL`官方提供的`PIL`二进制安装库包都是`32`位的，我们需要`64`位的。或者直接使用`Pillow`来代替，使用方法基本没有什么区别，我选择后者。
地址：[http://www.lfd.uci.edu/~gohlke/pythonlibs/#pillow](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pillow)
下载：`Pillow‑5.0.0‑cp27‑cp27m‑win_amd64.whl`，然后`pip`安装之。

> 存档原文：
tesseract本身不支持png，jpg这样图片格式，pytesser需要利用PIL将这种图片转换成tif格式，这是安装PIL的目的之一。sudo pip install PIL

#### 2. 安装[tesseract-ocr](https://github.com/tesseract-ocr/tesseract/wiki)
`Win`下，需要在[Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)下载，我选择`tesseract-ocr-setup-3.05.01.exe`，因为`tesseract-ocr-setup-4.0.0-alpha.20180109.exe(experimental)`没好使。

> 存档原文：
在`Mac`下安装方法极其简单，`brew install tesseract`，附：语言包在`/usr/local/share/tessdata`,这样子就安装好了，可以在终端输入`tesseract`试试

#### 3. 安装[pytesseract](https://code.google.com/archive/p/pytesser/downloads)
只有`pytesser_v0.0.1.zip`的版本，不过我好像是`pip`安装的，有点记不清了。

> 存档原文：
下载，解压，重命名，拷贝到`/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages`，
`/usr/local/lib/python2.7/site-packages/pytesser`，https://stackoverflow.com/questions/15567141/installing-pytesser ，`sudo pip install pytesseract`

## 0x03.测试
``` python
# -*- coding: utf-8 -*-
tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'

from PIL import Image
import pytesseract

image = Image.open('vcode.png!webp')
vcode = pytesseract.image_to_string(image, config=tessdata_dir_config)

print vcode
```
## 0x04.后记
成文匆忙，遇到`bug`可留言
几天前（`2018 年 1 月 19日`）因为`Win 10`预览版字体导致各种`IDE`乱码所以重装了`LTSB 2016`，到目前为止用的还是很舒服的，当然`8102`年了，也该切到`py 3`环境了，于是根本没装`py 2`的环境，直接装了`3.7.0a4`，次日换成了`3.6.4`。因此，在此重新说明一下配置方法，鉴于我现在也不知道这个站到底应该怎么去写，从百度搜了下`robots.txt`也早就生效了，想想能看到这个站的也都不是一般人，所以我就简写吧（以写给自己看的程度去写，讲真我是很少回头看自己站的内容的，这点后期可以调整一下）
![](https://i1.yuangezhizao.cn/Win-10/20180129135329.jpg!webp)


## 0x05.参考
[Python处理验证码第一篇（pytesser初探及报错处理）](http://blog.csdn.net/Bone_ACE/article/details/50436587)



