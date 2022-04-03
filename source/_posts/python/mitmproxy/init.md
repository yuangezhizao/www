---
title: mitmproxy 安装踩坑简记
date: 2021-08-02 23:40:05
tags:
  - mitmproxy
count: 1
os: 1
os_1: Monterry 12.0 Beta (21A5294g)
browser: 0
browser_1: 92.0.4515.107 Stable
place: 新家
key: 118
---
    总算给安装上了
<!-- more -->
## 0x00.前言
为了存储`maimai_DX`的成绩，每次都得开抓包工具，偶然间发现`py`有`mitmproxy`，可以借助于它获取`cookies`

## 0x01.安装
参照官方文档[mitmproxy](https://web.archive.org/web/20210803125024/https://docs.mitmproxy.org/stable/overview-installation/)，可以看到`macOS`下推荐的方法是使用`brew`来安装
``` bash
brew install mitmproxy
```
安装完成之后发现毕竟要拿`py`写逻辑，所以还是得安装`pip`的包
``` bash
pip3 install mitmproxy
```

## 0x02.运行
首先，执行的是`brew`的`mitmproxy`，一切正常，但是`pip`的`mitmproxy`报错了
``` bash
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/cryptography/hazmat/bindings/openssl/binding.py", line 14, in <module>
    from cryptography.hazmat.bindings._openssl import ffi, lib
ImportError: dlopen(/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/_cffi_backend.cpython-39-darwin.so, 0x0002): tried: '/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/_cffi_backend.cpython-39-darwin.so' (mach-o file, but is an incompatible architecture (have 'x86_64', need 'arm64e')), '/usr/lib/_cffi_backend.cpython-39-darwin.so' (no such file)
```
于是就开始了漫长的排查过程……
首先发现，`brew`是有`X86_64`和`arm64`两个版本的，而实际生效的只有前者（因为当初从黑苹果迁移到白苹果之后并没有重新安装`brew`，是个上古遗留问题
所以决定首先卸载`brew`，然后重新安装，这样就可以确定本地只有`arm64`版本的了，然后谷歌搜到了[Installation on an M1 Mac - Not in Rosetta Mode](https://web.archive.org/web/20210802155015/https://github.com/pyca/cryptography/issues/5742)，发现是`cffi`的问题
``` bash
pip3 uninstall cffi
pip3 install cffi
```
终于解决了问题

## 0x03.使用
``` bash
yuangezhizao@MacMini ~ % mitmdump --version
Mitmproxy: 7.0.0
Python:    3.9.6
OpenSSL:   OpenSSL 1.1.1k  25 Mar 2021
Platform:  macOS-12.0-arm64-arm-64bit
```

## 0x04.引用
[使用 mitmproxy + python 做拦截代理](https://blog.wolfogre.com/posts/usage-of-mitmproxy/)
[Installing Cryptography on an Apple Silicon M1 Mac](https://web.archive.org/web/20210802160245/https://stackoverflow.com/questions/66035003/installing-cryptography-on-an-apple-silicon-m1-mac)
[Runtime error on import on M1 Mac](https://web.archive.org/web/20210803125234/https://github.com/pyca/cryptography/issues/5843)
