---
title: 【云+社区年度征文】浅析基于 Serverless 的 maimai_DX 查分器
date: 2020-12-24 23:24:04
tags:
  - Serverless
count: 1
os: 1
os_1: Big Sur 11.1 (20C69)
browser: 0
browser_1: 87.0.4280.88 Stable
place: 新家
key: 106
---
    Happy Xmas！
<!-- more -->
## 0x00.前言
整个上文，见[【1024，Serverless】maimai_DX 查分器](./maimai_DX_CN_probe.html)

## 0x01.[WSGI](https://wsgi.readthedocs.io/en/latest/index.html)
说起`WSGI`，只要是写过`Python Web`的人多多少少都应该会听说过[Web服务器网关接口](https://zh.wikipedia.org/wiki/Web服务器网关接口)，先来看看维基的解释
> Web服务器网关接口（`Python Web Server Gateway Interface`，缩写为`WSGI`）是为`Python`语言定义的`Web`服务器和`Web`应用程序或框架之间的一种简单而通用的接口。自从`WSGI`被开发出来以后，许多其它语言中也出现了类似接口

再来看官方文档，没错是在[PEP 3333](https://web.archive.org/web/20201224153638/https://www.python.org/dev/peps/pep-3333/)中引入的，这个在`2010`年创建的`PEP`详细描述了什么是`Python Web Server Gateway Interface`
> WSGI[1] is not a server, a python module, a framework, an API or any kind of software. It is just an interface specification by which server and application communicate. Both server and application interface sides are specified in the PEP 3333. If an application (or framework or toolkit) is written to the WSGI spec then it will run on any server written to that spec.

简单来说，`WSGI`包含两个部分，**服务器或网关端**以及**应用程序或框架端**
### 1. 应用程序或框架端
- 它仅仅是一个接收两个参数的可调用（`callable`）`对象`，函数、方法、类等具有`__call__`方法的`object`都属于前句话中`对象`的范畴内，并且这个`对象`必须可以多次调用。虽然名字叫做`应用程序`，但写`web app`的开发人员并不会直接拿`WSGI`作为`api`使用，而是会去用上层更高级的框架（比如`Flask`等），写框架和服务器开发者才会面对`WSGI`编程（
- 从[The Application/Framework Side](https://www.python.org/dev/peps/pep-3333/#id20)的示例代码中可以看到接收的两个对象分别是：`environ`和`start_response`
- 通过调用`start_response(status, response_headers)`发送状态码（`HTTP Status Code`）和头部信息（`HTTP Header`），整个函数的返回值为响应内容（`HTTP Body`）

### 2. 服务器或网关端
客户端发起了一个请求之后，它就会去调一次前文中的可调用对象，参照[The Server/Gateway Side](https://www.python.org/dev/peps/pep-3333/#id21)示例代码即`result = application（environ，start_response）`正好对应上前文中的接收的两个对象

### 3.中间件
`2020-12-25 00:47:02`：受时间关系影响去睡觉了，晚上再来更新