---
title: SUT 自动推送期末成绩系统
date: 2017-7-19 18:48:50
tags:
  - python
count: 2
os: 0
os_1: 10.0.14393 Pro
browser: 0
browser_1: 61.0.3153.0 Dev
place: 家
key: 09
---
    成绩先出的，挂了！
    公告：本文不再更新……
    完结撒花
<!-- more -->
## 0x00.小序
1. 刚才敲`hexo`，居然提示我`command not found`，看了下`node`&`npm`都在，那就是`环境变量`的问题了，因为前几天还好使来着……
果然，解决完`bug`可以步入正题了……
2. 本文仍旧是关于`python`里的`requests`库（俗称“瑞士军刀”）的基础使用……
3. 有个麻烦的问题就是需要识别附加码（因为无法绕过……），不过是最简单的那种类型（纯 4 位数字），给你们一张图片体会下
![附加码](https://i1.yuangezhizao.cn/Win-10/fjm.jpg!webp)
2333是拿爬虫爬到的……


## 0x01.缘由
1. 虽然是最后一科考完的，但是成绩迟迟没有出（截至 20 日已经 9 天了），有点慌了（还好没犯那种天天查一遍的强迫症似的毛病）……

## 0x02.套路
识别附加码登陆后间隔设定的时间重复查询成绩页面是否含有设定学科的序号，如有则触发向微信推送消息，反之 pass……

## 0x03.环境
其实页头有写，这里复述一遍：
a. Microsoft Windows [版本 10.0.14393]（Win 10 x64 Pro 1607 14393.1480）
b. Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:53:40) [MSC v.1500 64 bit (AMD64)] on win32
c. JetBrains Pycharm 2017.1.5 x64 Professional

以下安装顺序不要改变，因为`pytesseract`依赖`tesseract-ocr`及`PIL`。

#### 1. [Tesseract](https://github.com/tesseract-ocr/tesseract)——`google`的`ocr`识别引擎

参考官方[WiKi](https://github.com/tesseract-ocr/tesseract/wiki)页对于`Windows`下的介绍

> An unofficial installer for windows for Tesseract 3.05-dev and Tesseract 4.00-dev is available from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki). This includes the training tools.

> An installer for the old version 3.02 is available for Windows from our [download](https://github.com/tesseract-ocr/tesseract/wiki/Downloads) page. This includes the English training data. If you want to use another language, [download the appropriate training data](https://github.com/tesseract-ocr/tesseract/wiki/Data-Files), unpack it using [7-zip](http://www.7-zip.org/), and copy the .traineddata file into the 'tessdata' directory, probably C:\Program Files\Tesseract OCR\tessdata.

即`3.02`之前参考[sourceforge](https://sourceforge.net/projects/tesseract-ocr-alt/files/)上的，之后版本不提供安装包，但有个非官方`3.05-dev`|`4.00-dev`安装包可以使用，
我使用的是后者那个`tesseract-ocr-setup-4.00.00dev.exe	2017-05-10 16:46	40.5M	latest Tesseract 4`（图新鲜不要介意）……
安装时可选`Additional Language data（download）`，里面含简体中文——`Chinese（Simplified）`，安装完需要手动把`C:\Program Files (x86)\Tesseract-OCR`添加至`Path`环境变量里。

输入`tesseract -v`会得到如下信息才算搞定：
```
tesseract 4.00.00alpha
 leptonica-1.74.1
  libgif 4.1.6(?) : libjpeg 8d (libjpeg-turbo 1.5.0) : libpng 1.6.20 : libtiff 4.0.6 : zlib 1.2.8 : libwebp 0.4.3 : libopenjp2 2.1.0
```

#### 2. [pillow](https://github.com/python-pillow/Pillow)——`python`的图像处理库
> a replacement for PIL, the Python Image Library, which provides image processing functionality and supports many file formats.
Use `from PIL import Image` instead of `import Image`.

[.whl文件](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pillow)，根据版本选择`Pillow‑4.2.1‑cp27‑cp27m‑win_amd64.whl（[1.4 MB] [Jul 06, 2017]）`，然后`pip`安装之。

#### 3. [pytesseract](https://github.com/madmaze/pytesseract)——一个`python`库
> `pytesseract`是对`Tesseract-OCR`的一个封装，方便我们在`python`中调用`Tesseract-OCR`引擎

直接`pip install pytesseract`或者`easy_install pytesseract`就可以了，是安装过程最简单的……
备份：[pypi](https://pypi.python.org/pypi/pytesseract/0.1)

随便识别一张图片：
``` python
# -*- coding: utf-8 -*-
try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract

image = Image.open('vcode.jpg!webp')
vcode = pytesseract.image_to_string(image)

print vcode
```
报错：
```
Traceback (most recent call last):
  File "D:/yuangezhizao/Documents/Pycharm/pic.py", line 9, in <module>
    vcode = pytesseract.image_to_string(image)
  File "C:\Python27\lib\site-packages\pytesseract\pytesseract.py", line 125, in image_to_string
    raise TesseractError(status, errors)
pytesseract.pytesseract.TesseractError: (1, u'Error opening data file \\Program Files (x86)\\Tesseract-OCR\\eng.traineddata')
```
查[issue](https://github.com/madmaze/pytesseract/issues/50)，
看到[jtbr](https://github.com/jtbr)的解释：
> This occurs under windows (at least in tesseract version 3.05) when the current directory is on a different drive from where tesseract is installed.

> Something in tesseract is expecting data files to be in \Program Files... (rather than C:\Program Files, say). So if you're not on the same drive letter as tesseract, it will fail. It would be great if we could work around it by temporarily changing drives (under windows only) to the tesseract installation drive before executing tesseract, and changing back after.

看到[int3l](https://github.com/int3l)的解决方法：
> Finally managed to reproduce this error.

> Please try to use the config option with pytesseract like this:

> tessdata_dir_config = '--tessdata-dir "<replace_with_your_tessdata_dir_path>"'
 Example config: '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
 It's important to include double quotes around the dir path.

> pytesseract.image_to_string(image, lang='chi_sim', config=tessdata_dir_config)
If this workaround works for you, I will include the snippet to the README file.

后来发现其实`GitHub`首页就有写……

~~20 日写了一下午，未完待续……~~
`2017-7-24 16:04:12 更新`：

现在可以识别教务在线的附加码了：
``` python
# -*- coding: utf-8 -*-
tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'

try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract
import requests

fjm_url = 'http://jwc.sut.edu.cn/ACTIONVALIDATERANDOMPICTURE.APPPROCESS'
img = requests.get(fjm_url)
with open('fjm.jpg!webp', 'wb') as f:
    f.write(img.content)
image = Image.open('fjm.jpg!webp')

fjm = pytesseract.image_to_string(image, config=tessdata_dir_config)

print fjm
```

## 0x04.抓包
其实就是<kbd>F12</kbd>，切换到`Network`选项卡（懒得分析页面了）……
找到登陆的那个（Post）包：
```
▼ General
Request URL:http://jwc.sut.edu.cn/ACTIONLOGON.APPPROCESS?mode=4
Request Method:POST
Status Code:200 OK
Remote Address:202.199.96.30:80
Referrer Policy:no-referrer-when-downgrade

▼ Response Headers     view source
Content-Length:983
Content-Type:text/html;charset=gb2312
Date:Mon, 24 Jul 2017 11:21:17 GMT
Expires:Thu, 01 Jan 1970 00:00:00 GMT
Pragma:no-cache
Server:WebLogic Server 8.1 SP2 Fri Dec 5 15:01:51 PST 2003 316284

▼ Requests Headers     view source
Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding:gzip, deflate
Accept-Language:zh-CN,zh;q=0.8
Cache-Control:max-age=0
Connection:keep-alive
Content-Length:71
Content-Type:application/x-www-form-urlencoded
Cookie:UM_distinctid=**********d2f1-0b**********d7-396b4e08-144000-15c3**********; gsScrollPos-477=0; gsScrollPos-704=; CNZZDATA4785959=cnzz_eid%3D805060342-1495720475-http%253A%252F%252Fjwc.sut.edu.cn%252F%26ntime%3D1500893572; JSESSIONID=********************zL2UNl0tJdAt**********Ivuv5ltwfP!7548*****
Host:jwc.sut.edu.cn
Origin:http://jwc.sut.edu.cn
Referer:http://jwc.sut.edu.cn/ACTIONLOGON.APPPROCESS?mode=3
Upgrade-Insecure-Requests:1
User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36

▼ Query String Parameters     view source view URL encoded
mode:4

▼ Form Data     view source view URL encoded
WebUserNO:15*******
Password:******
Agnomen:1858
submit.x:29
submit.y:3
```
~~点击`Query String Parameters`&`Form Data`的`view source`，会分别变成`mode=4`&`WebUserNO=15*******&Password=******&Agnomen=1858&submit.x=29&submit.y=3`，这才是我们需要的。~~

## 0x05.模拟
拿出瑞士军刀（误），如下（没啥好说的了）：
``` python
import requests

s = requests.Session()
LoginUrl = "http://jwc.sut.edu.cn/ACTIONLOGON.APPPROCESS?mode=4"
username = "15*******"
password = "******"

LoginData = {
    'WebUserNO': username,
    'Password': password,
    'Agnomen': fjm
}

r = s.post(LoginUrl, data=LoginData)
```
哦，对了，你要是问为什么模拟提交的参数比抓包的少，我会说这是试验出来的最少参数的提交方式，再不能删减了……
接下来就是继续抓包然后模拟，思路已在`## 0x02.套路`澄清。

我忽然发现好像写过原理类似的文章（差点都忘了）[SUT 大学外语六级报名报警系统](https://www.yuangezhizao.cn/articles/python/sut/jwzx/college-foreign-language-six-level-sign-up-alarm-system.html)，就是附加码的处理方式不一样，那就不重复了（看着不及格的科目实在是没有欲望再写下去了~~谁来安慰我下受伤的心灵，第一次……~~）……

## 0x06.推送——[Server酱](https://sc.ftqq.com/3.version)
个人安利下这个，超好用的！

> Server酱
是什么
「Server酱」，英文名「ServerChan」，是一款「程序员」和「服务器」之间的通信软件。
说人话？就是从服务器推报警和日志到手机的工具。
开通并使用上它，只需要一分钟：
登入：用`GitHub`账号[登入网站](http://sc.ftqq.com/?c=github&a=login)，就能获得一个[SCKEY](http://sc.ftqq.com/?c=code)（在「[发送消息](http://sc.ftqq.com/?c=code)」页面）
绑定：点击「[微信推送](http://sc.ftqq.com/?c=wechat&a=bind)」，扫码关注同时即可完成绑定
发消息：往[http://sc.ftqq.com/SCKEY.send](http://sc.ftqq.com/SCKEY.send)发GET请求，就可以在微信里收到消息啦
来个示意图：
![示意图](https://i1.yuangezhizao.cn/Win-10/ServerChan.gif!raw)
调用代码
发送消息非常简单，只需要向以下URL发一个GET或者POST请求：
`https://sc.ftqq.com/< 此处填写 SCKEY >.send`
接受两个参数：
text：消息标题，最长为256，必填。
desp：消息内容，最长64Kb，可空，支持MarkDown。
最简单的消息发送方式是通过浏览器，在地址栏输入以下URL，回车后即可发送：
`https://sc.ftqq.com/< 此处填写 SCKEY >.send?text=主人服务器又挂掉啦~`
SCKEY是非常重要的，所以请妥善保存，不要随便告诉别人。另外同样内容的消息一分钟只能发送一次，服务器只保留一周的消息记录。

所以我们只需要定义一个推送函数，在成绩页面有标记的内容时执行此函数即可在微信收到推送，比如这样：
``` python
def send_wechat_message():
    send_url = 'http://sc.ftqq.com/< 此处填写 SCKEY >.send'

    Send_Data = {
        'text': '欧尼酱，新成绩要看么？'
        'desp': '喵喵喵'
    }

    r = s.post(send_url, data=Send_Data)
    return r.text
```
返回包正常情况下是这样的：`{"errno":0,"errmsg":"success","dataset":"done"}`，然后看手机微信：
![收到推送]('https://i1.yuangezhizao.cn/MX4-Pro/S70724-200624.jpg!webp')

## 0x07.看似没有用的后记
再次强调一遍不要在`py`里循环查询（会出意外的……），`Win`下善用`计划任务`，`Linux`下善用`Cron`

> 参考链接：https://www.polarxiong.com/archives/python-pytesser-tesseract.html

# 完结撒花
终于写完了，好累……