---
title: bilibili 播放量爬虫
date: 2017-02-08 18:00:00
tags:
  - python
  - crawler
  - bilibili
count: 2
os: 0
os_1: 10.0.14393 Pro
browser: 0
browser_1: 56.0.2924.87 Stable
place: 家
key: 02
---
    以前看过别人做的一个展示番剧播放数据的站点，自己也想模仿一下
<!-- more -->
## 0x00.起因
 [【测试】番剧数据中心](https://www.biliplus.com/data/)

## 0x01.经过
### 取数据
首先，要想做统计你得拿到数据。用 Google 搜了一圈最后在知乎上找到了结果 。我
采用这个 Api（Application Programming Interface，应用程序编程接口）：

    http://api.bilibili.com/archive_stat/stat?aid=<aid>

以 AV8614334 例，请求`http://api.bilibili.com/archive_stat/stat?aid=8614334`会得到如下`json`格式的结果。
```
// 20170217155559
// http://api.bilibili.com/archive_stat/stat?aid=8614334

{
  "code": 0,
  "data": {
    "view": 199648,
    "danmaku": 5132,
    "reply": 1164,
    "favorite": 124,
    "coin": 958,
    "share": 125,
    "now_rank": 0,
    "his_rank": 0
  },
  "message": ""
}
```
`py`代码：
``` python
import requests

api_url = "http://api.bilibili.com/archive_stat/stat?aid=8614334"
response = requests.get(api_url).content
```
周期的话一小时足矣，大可不必一分钟，其一文件太大没必要，其二在数据处理的时候你会发现会舍弃部分点。`Windows`平台可以用`计划任务`，`Linux`平台可以用`Cron`。前者用`批处理`的话，创建如下内容的`.bat`文件来运行`bilibili.py`：
``` bat
@echo off
cd C:\task
start python bilibili.py
exit
```
后者用`shell`的话，创建如下内容的`.sh`文件来运行`bilibili.py`：
``` bash
#!/bin/bash
export TZ='Asia/Shanghai'
# 需要考虑国外服务器的时区，否则时间会对不上，上一行有异议
python 10.py
```
### 存数据
然后就要存储这些数据了，你可以简单地直接存储到`json`文件里，也可以存到数据库里。对于前者，可以这样实现
``` python
import json

with open('data.json', 'a') as a:
    a.write(json.dumps(response) + '\n')
```
而后者略显麻烦，先将`json`对象转换成`python`对象，这里得到的是`dict`。
``` python
import json

jsDict = json.loads(response)
code = jsDict['code']
view = jsDict['data']['view']
danmaku = jsDict['data']['danmaku']
reply = jsDict['data']['reply']
favorite = jsDict['data']['favorite']
coin = jsDict['data']['coin']
share = jsDict['data']['share']
now_rank = jsDict['data']['now_rank']
his_rank = jsDict['data']['his_rank']
message = jsDict['message']
```
然后存到数据库里，采用`SQlite`。在`bilibili.db`文件中创建表并执行插入操作。
``` python
import sqlite3

conn = sqlite3.connect("bilibili.db")
c = conn.cursor()
# bilibili.db 不存在时会自动创建

c.execute('''CREATE TABLE IF NOT EXISTS{0} (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    DATE TEXT,
    TIME TEXT,
    code INT,
    view INT,
    danmaku INT,
    reply INT,
    favorite INT,
    coin INT,
    share INT,
    now_rank INT,
    his_rank INT,
    message TEXT);
    '''.format("`AV" + aid + "`"))
# 表名不能为纯数字

c.execute("INSERT INTO "+ "`AV" + aid + "`" + " (DATE, TIME, code, view, danmaku, reply, favorite, coin, share, now_rank, his_rank, message) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (DATE, TIME, code, view, danmaku, reply, favorite, coin, share, now_rank, his_rank, message));

conn.commit()
conn.close()
```
上述代码里的`DATE`，`TIME`是调用了当前的时间，可以这样实现：
``` python
from datetime import datetime

DATE = str(datetime.now().strftime("%Y-%m-%d"))
TIME = str(datetime.now().strftime("%H:%M:%S"))
```
### 用数据
等我数据屯足了再说吧
`2017-7-1 20:09:24 更新`：懒得爬了，放假再说吧……

## 0x02.结果
[源码](https://github.com/yuangezhizao/python/blob/master/crawler/bilibili/analysis-bilibili-views.py)
