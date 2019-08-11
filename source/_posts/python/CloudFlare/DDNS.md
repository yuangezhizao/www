---
title: CloudFlare DDNS 脚本
date: 2019-8-12 01:26:59
tags:
  - CloudFlare
  - DDNS
count: 1
os: 0
os_1: 10.0.17763.652 2019-LTSC
browser: 0
browser_1: 74.0.3729.169 Stable
place: 新家
key: 56
---
    手写 DDNS 实现，爽到！
<!-- more -->
## 0x00.前言
因为电信宽带提供公网`ip`地址，`wz`打了个电话就申请到了，然而每次获取到的公网`ip`并不是固定的，感觉极低的概率能获取到上次的拨号的地址
又需要访问家里的一些服务，开始时是干脆记住`ip`地址，后来越来越懒了决定干脆用域名的`A`记录解析好了，于是就有了本文的内容

## 0x01.代码
![核心接口](https://i1.yuangezhizao.cn/Win-10/20190812013626.jpg!webp)

`CloudFlare_DDNS.py`
``` python
#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/7/18 0018 19:40
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
import time

import requests

headers = {
    'X-Auth-Email': '<rm>',
    'X-Auth-Key': '<rm>',
    'Content-Type': 'application/json',
}


def update_dns_record():
    ip = requests.get('https://lab.yuangezhizao.cn/ip').json()['IP']

    data = '{"type":"A","name":"home.yuangezhizao.cn","content":"' + ip + '"}'

    response = requests.put(
        'https://api.cloudflare.com/client/v4/zones/<zone_identifier>/dns_records/<identifier>/',
        headers=headers, data=data)

    print(response.json())


try:
    update_dns_record()
except Exception as e:
    print(e)

```
`zone_identifier`和`identifier`不方便确定的话，可以<key>F12</key>来下官方页面，那个页面走的接口数据也是一样的

## 0x02.定时运行
~~`Windows`计划任务请！~~群辉大法好！
套件中心里可以安装`Python3`，再开启`SSH`服务，连进去之后安装`pip3`就可以下载`requests`包了`hhh`
![Python3](https://i1.yuangezhizao.cn/Win-10/20190812014512.jpg!webp)
![任务计划](https://i1.yuangezhizao.cn/Win-10/20190812014216.jpg!webp)
![常规](https://i1.yuangezhizao.cn/Win-10/20190812014353.jpg!webp)
![计划](https://i1.yuangezhizao.cn/Win-10/20190812014406.jpg!webp)
![任务设置](https://i1.yuangezhizao.cn/Win-10/20190812014422.jpg!webp)

![未安装包](https://i1.yuangezhizao.cn/Win-10/20190812015002.jpg!webp)
![运行成功](https://i1.yuangezhizao.cn/Win-10/20190812015053.png!webp)

未完待续……
