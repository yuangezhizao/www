---
title: 腾讯云万象优图之人脸识别
date: 2017-03-04 21:00:00
tags:
  - python
  - QCloud
count: 2
os: 0
os_1: 10.0.14393 Pro
browser: 0
browser_1: 56.0.2924.87 Stable
place: 宿舍
key: 04
---
    一直想尝试这个，奈何水平不足（GitHub上也没有参考），故原计划在假期学，然而一直拖到了今天。
    校级 Watch Dogs
<!-- more -->
## 0x00.前言
这是一个很普通的[控制台界面](https://console.qcloud.com/image/imgguide)，以前总是感觉太简陋了，连图片列表都没有。当然现在没有那种感觉了，毕竟有`Api`就足够了。

## 0x01.开工
首先，阅读[产品文档](https://www.qcloud.com/document/product/275)，今天对我们有用的是[签名和鉴权文档](https://www.qcloud.com/document/product/275/3805)和[人脸识别接口文档](https://www.qcloud.com/document/product/275/6014)。
然后，先生成签名，这里我用了它给出的`php`的实例，所以需要一个`php`环境。`Windows`下可以用[PHPStudy](http://www.phpstudy.net/)，现在我在`Mac`下，方法就更简单了，`sudo apachectl start`即可。
签名有了，剩下的就简单了，直接看文档的例子就能明白。人脸识别有这么几个概念：
1. `group_id`：就是一个分组，个体都在组里，好比一个学校，数量限制为5000个。

> 个体(person)以组（group）的形式存储，一个组可以包含多个个体，一个个体也可以存在于多个组。group\_id即用来标识group。组(group)没有专门的创建接口，创建个体(person)时，指定group_id则会自动创建

2. `person_id`：个体，也就是每一个人，数量限制为10000个。

> 人脸以个体（person）的形式存储，一个个体下可以存储多张人脸。person_id即用来标识person

3. `face_id`：人脸，每一个人可以对应多张脸，数量限制为20个。

> 标识每张人脸的id

现在来创建个体：
``` python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests

url = "http://service.image.myqcloud.com/face/newperson"
id = <此处替换为学号>

headers = {
    "Authorization": "<此处替换为签名>",
    "Host": "service.image.myqcloud.com",
#   "Content-Length": "187",
    "Content-Type": "Application/json"
}

data = {
    "appid": "<此处替换为项目ID>",
    "bucket": "<此处替换为空间名称>",
    "group_ids": ["2015"],  #注意此处参数类型，我被摆了一道
    "person_id": str(id),
    "url": "<此处替换为人脸图片地址>"
}

jdata = json.dumps(data)
r = requests.post(url=url, data=jdata, headers=headers)

print r.text
```
运行结果如下所示：
``` json
{"code":0,"message":"OK","data":{"person_id":"手动打码","suc_group":1,"suc_face":1,"session_id":"","face_id":"手动打码","group_ids":["2015"]}}
```
这样就在`2015`组（就是`2015`级学生）里创建了一个包含一张人脸的个体。接下来就是继续创建个体了……

`2017-7-1 20:13:16`：
审查学校`教务在线`发现是`大连乾豪`开发的教务系统，此系统漏洞较多不过应该会有增量更新，`用户登陆`后（没账号你就不用想了……），进入`教务管理系统`的`查询中心`，切换到`学生园地`的`个人信息`，发现照片的链接是`http://***.***/***.APPPROCESS?ByStudentNO=null`，怀着试一试的态度，把`null`改成其他同学的学号，发现可以访问。可以写个爬虫爬下来……截至目前，试验所用照片已完全删除，`使用本方法获取属于非法行为，滥用此法本人不承担任何责任！`
~~1万年后……~~
个体足够了，可以进行人脸识别了，一共有三种：人脸验证、人脸检索、人脸比对。这里对我最有用的是人脸检索，其他的我就不详细介绍了。
``` python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests

url = "http://service.image.myqcloud.com/face/identify"

headers = {
    "Authorization": "<此处替换为签名>",
    "Host": "service.image.myqcloud.com",
#   "Content-Length": "187",
    "Content-Type": "Application/json"
}

data = {
    "appid": "<此处替换为项目ID>",
    "bucket": "<此处替换为空间名称>",
    "group_id": ["2015"],
    "url":
}

jdata = json.dumps(data)
r = requests.post(url=url, data=jdata, headers=headers)

print r.text
```

大体上就是这个样子……

## 0x02.更新

`2017-7-1 20:13:16`：
我记得当初还写了个前端页面对接到后端的接口上，用了`Flask`但是文件上传总是出错……
故意观察了一天再来写这段。总体上，可信率可观！
要是能识别的话基本上没有错的，不能识别的就是不能了……
