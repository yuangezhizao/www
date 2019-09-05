---
title: 百度云人脸识别
date: 2018-4-1 11:21:25
tags:
  - python
count: 1
os: 0
os_1: 10.0.14393 2016-LTSB
browser: 0
browser_1: 64.0.3282.140 Stable
place: 宿舍
key: 35
---
    还是想测试一下效果，腾讯的早开始收费了……
<!-- more -->
## 0x00.前言
有`SDK`包实在是在方便了，也不用自己去请求`api`了……
![](https://i1.yuangezhizao.cn/Win-10/20180401113130.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180401113152.jpg!webp)

## 0x01.开工
[地址](https://console.bce.baidu.com/ai/#/ai/face/overview/index)，创建应用，应用名称我设的“人脸识别”，记录`AppID`、`API Key`、`Secret Key`之后`SDK`包初始化需要用到
`pip3 install baidu-aip`
![](https://i1.yuangezhizao.cn/Win-10/20180401112606.jpg!webp)

人脸库为了方便管理写的“年级名”
![](https://i1.yuangezhizao.cn/Win-10/20180401113358.jpg!webp)

## 0x02.新建`AipFace`
详见[文档](http://ai.baidu.com/docs#/Face-Python-SDK/top)
``` python
from aip import AipFace

""" 你的 APPID AK SK """
APP_ID = '你的 App ID'
API_KEY = '你的 Api Key'
SECRET_KEY = '你的 Secret Key'

client = AipFace(APP_ID, API_KEY, SECRET_KEY)
```
人脸检测的返回数据倒是可以存一下，虽然以后也不一定会用上，接口有限制的话就`sleep(1)`一下即可，代码不详细贴了。

## 0.03.人脸注册
真正意义上的人脸识别需要先人脸注册
``` python
import os
dir = '***'

from aip import AipFace
""" 你的 APPID AK SK """
APP_ID = '***'
API_KEY = '***'
SECRET_KEY = '***'
client = AipFace(APP_ID, API_KEY, SECRET_KEY)
groupId = '2015'

""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

""" 如果有可选参数 """
options = {}
options['action_type'] = 'replace'

if os.path.exists(dir):
    dirs = os.listdir(dir)
    for dirc in dirs:
        if 'py' not in dirc:
            print(dirc)
            uid = dirc[:-4]
            userInfo = ''
            image = get_file_content()
            client.addUser(uid, userInfo, groupId, image, options)
else :
    print('dir not exists')
```

## 0.04.人脸识别
``` python
groupId = "group1,group2"

""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

image = get_file_content('example.jpg')

""" 调用人脸识别 """
client.identifyUser(groupId, image);

""" 如果有可选参数 """
options = {}
options["ext_fields"] = "faceliveness"
options["user_top_num"] = 3

""" 带参数调用人脸识别 """
client.identifyUser(groupId, image, options)
```
