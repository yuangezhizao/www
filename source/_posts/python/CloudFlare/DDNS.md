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

安装`pip3`，首先下载或者`wget https://bootstrap.pypa.io/get-pip.py`扔到自己的`NAS`分区中，然后`sudo python3 get-pip.py`，
会有大概率`ReadTimeoutError`，多次重试之后终于安装成功……
![一片红](https://i1.yuangezhizao.cn/Win-10/20190824132144.jpg!webp)
``` bash
yuangezhizao@NAS:/volume1/ygzz$ sudo python3 get-pip.py 
Password: 
Collecting pip
  Downloading https://files.pythonhosted.org/packages/8d/07/f7d7ced2f97ca3098c16565efbe6b15fafcba53e8d9bdb431e09140514b0/pip-19.2.2-py2.py3-none-any.whl (1.4MB)
     |████████████████████████████████| 1.4MB 8.2kB/s 
Collecting setuptools
  Downloading https://files.pythonhosted.org/packages/b2/86/095d2f7829badc207c893dd4ac767e871f6cd547145df797ea26baea4e2e/setuptools-41.2.0-py2.py3-none-any.whl (576kB)
     |████████████████████████████████| 583kB 9.5kB/s 
Collecting wheel
  Downloading https://files.pythonhosted.org/packages/00/83/b4a77d044e78ad1a45610eb88f745be2fd2c6d658f9798a15e384b7d57c9/wheel-0.33.6-py2.py3-none-any.whl
Installing collected packages: pip, setuptools, wheel
  WARNING: The script wheel is installed in '/volume1/@appstore/py3k/usr/local/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
Successfully installed pip-19.2.2 setuptools-41.2.0 wheel-0.33.6
```
安上了之后赶紧配置镜像源（如下是一顿骚操作，可见注释
``` bash
yuangezhizao@NAS:/volume1/ygzz$ sudo pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U
Password: 
sudo: pip3: command not found # 没在 PATH 里诶
yuangezhizao@NAS:/volume1/ygzz$ sudo cat /etc/profile
#/etc/profile: system-wide .profile file for ash.

umask 022

PATH=/sbin:/bin:/usr/sbin:/usr/bin:/usr/syno/sbin:/usr/syno/bin:/usr/local/sbin:/usr/local/bin
export PATH

PGDATA=/var/services/pgsql
export PGDATA

TERMINFO=/usr/share/terminfo
export TERMINFO

TERM=${TERM:-cons25}
export TERM

PAGER=more
export PAGER

export LC_ALL=en_US.utf8
export LANG=en_US.utf8

PS1="`hostname`> "

alias dir="ls -al"
alias ll="ls -la"

ulimit -c unlimited

if [ -f /etc.defaults/.bashrc_profile ]; then
	source /etc.defaults/.bashrc_profile
fi
yuangezhizao@NAS:/volume1/ygzz$ sudo vim /etc/profile # 永久生效法
yuangezhizao@NAS:/volume1/ygzz$ sudo source /etc/profile
sudo: source: command not found  # 永久生效不能？
yuangezhizao@NAS:/volume1/ygzz$ echo $PATH 
/sbin:/bin:/usr/sbin:/usr/bin:/usr/syno/sbin:/usr/syno/bin:/usr/local/sbin:/usr/local/bin
yuangezhizao@NAS:/volume1/ygzz$ export PATH=/sbin:/bin:/usr/sbin:/usr/bin:/usr/syno/sbin:/usr/syno/bin:/usr/local/sbin:/usr/local/bin:/volume1/@appstore/py3k/usr/local/bin
yuangezhizao@NAS:/volume1/ygzz$ echo $PATH # 那就临时生效吧……
/sbin:/bin:/usr/sbin:/usr/bin:/usr/syno/sbin:/usr/syno/bin:/usr/local/sbin:/usr/local/bin:/volume1/@appstore/py3k/usr/local/bin
yuangezhizao@NAS:/volume1/ygzz$ sudo pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U # 最新 ok
Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple
Requirement already up-to-date: pip in /volume1/@appstore/py3k/usr/local/lib/python3.5/site-packages (19.2.2)
yuangezhizao@NAS:/volume1/ygzz$ sudo pip3 install requests # 终于可以安装了
Collecting requests
  Downloading https://files.pythonhosted.org/packages/51/bd/23c926cd341ea6b7dd0b2a00aba99ae0f828be89d72b2190f27c11d4b7fb/requests-2.22.0-py2.py3-none-any.whl (57kB)
     |████████████████████████████████| 61kB 18kB/s 
Collecting urllib3!=1.25.0,!=1.25.1,<1.26,>=1.21.1 (from requests)
  Downloading https://files.pythonhosted.org/packages/e6/60/247f23a7121ae632d62811ba7f273d0e58972d75e58a94d329d51550a47d/urllib3-1.25.3-py2.py3-none-any.whl (150kB)
     |████████████████████████████████| 153kB 14kB/s 
Collecting idna<2.9,>=2.5 (from requests)
  Downloading https://files.pythonhosted.org/packages/14/2c/cd551d81dbe15200be1cf41cd03869a46fe7226e7450af7a6545bfc474c9/idna-2.8-py2.py3-none-any.whl (58kB)
     |████████████████████████████████| 61kB 13kB/s 
Collecting chardet<3.1.0,>=3.0.2 (from requests)
  Downloading https://files.pythonhosted.org/packages/bc/a9/01ffebfb562e4274b6487b4bb1ddec7ca55ec7510b22e4c51f14098443b8/chardet-3.0.4-py2.py3-none-any.whl (133kB)
     |████████████████████████████████| 143kB 13kB/s 
Collecting certifi>=2017.4.17 (from requests)
  Downloading https://files.pythonhosted.org/packages/69/1b/b853c7a9d4f6a6d00749e94eb6f3a041e342a885b87340b79c1ef73e3a78/certifi-2019.6.16-py2.py3-none-any.whl (157kB)
     |████████████████████████████████| 163kB 12kB/s 
Installing collected packages: urllib3, idna, chardet, certifi, requests
Successfully installed certifi-2019.6.16 chardet-3.0.4 idna-2.8 requests-2.22.0 urllib3-1.25.3
```
![运行成功](https://i1.yuangezhizao.cn/Win-10/20190812015053.png!webp)

未完待续……