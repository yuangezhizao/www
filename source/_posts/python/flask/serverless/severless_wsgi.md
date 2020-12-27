---
title: 【云+社区年度征文】浅析基于 Serverless 的 maimai_DX 查分器
date: 2020-12-24 23:24:04
tags:
  - Serverless
count: 2
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
整个上文，见[【1024，Serverless】maimai_DX 查分器](./maimai_DX_CN_probe.html)，本文针对部分内容进行再补充

## 0x01.[WSGI](https://wsgi.readthedocs.io/en/latest/index.html)
说起`WSGI`，只要是写过`Python Web`的人多多少少都应该会听说过[Web服务器网关接口](https://zh.wikipedia.org/wiki/Web服务器网关接口)，先来看看维基的解释
> Web服务器网关接口（`Python Web Server Gateway Interface`，缩写为`WSGI`）是为`Python`语言定义的`Web`服务器和`Web`应用程序或框架之间的一种简单而通用的接口。自从`WSGI`被开发出来以后，许多其它语言中也出现了类似接口

再来看官方文档，没错是在[PEP 3333](https://web.archive.org/web/20201224153638/https://www.python.org/dev/peps/pep-3333/)中引入的，这个在`2010`年创建的`PEP`详细描述了什么是`Python Web Server Gateway Interface`
> WSGI[1] is not a server, a python module, a framework, an API or any kind of software. It is just an interface specification by which server and application communicate. Both server and application interface sides are specified in the PEP 3333. If an application (or framework or toolkit) is written to the WSGI spec then it will run on any server written to that spec.

简单来说，`WSGI`包含两个部分，**服务器或网关端**以及**应用程序或框架端**
### 1. 应用程序或框架端
- 它仅仅是一个接收两个参数的可调用（`callable`）`对象`，函数、方法、类等具有`__call__`方法的`object`都属于前句话中`对象`的范畴内，并且这个`对象`必须可以多次调用
虽然名字叫做`应用程序`，但写`web app`的开发人员并不会直接拿`WSGI`作为`api`使用，而是会去用上层更高级的框架（比如`Flask`等），写框架和服务器开发者才会面对`WSGI`编程（
- 从[The Application/Framework Side](https://www.python.org/dev/peps/pep-3333/#id20)的示例代码中可以看到接收的两个对象分别是：`environ`和`start_response`。这俩**位置**参数是必须的，虽然命名可以不这么命
`environ`参数是一个字典对象，必须包含某些`WSGI`所需的变量（除非值为空时可省略），如下面的`CGI`变量：
1. `REQUEST_METHOD`
2. `SCRIPT_NAME`
3. `PATH_INFO`
4. `QUERY_STRING`
5. `CONTENT_TYPE`
6. `CONTENT_LENGTH`
7. `SERVER_NAME, SERVER_PORT`
8. `SERVER_PROTOCOL`
9. `HTTP_` `Variables`

另外，还必须包含以下`WSGI`定义的变量
1. `wsgi.version`
2. `wsgi.url_scheme`
3. `wsgi.input`
4. `wsgi.errors`
5. `wsgi.multithread`
6. `wsgi.multiprocess`
7. `wsgi.run_once`

- 通过调用`start_response(status, response_headers, exc_info = None)`发送状态码（`HTTP Status Code`）和头部信息（`HTTP Header`）
整个函数的返回值为响应内容（`HTTP Body`）是一个`write（body_data）`可调用对象

### 2. 服务器或网关端
客户端发起了一个请求之后，它就会去调一次前文中的可调用对象。参照[The Server/Gateway Side](https://www.python.org/dev/peps/pep-3333/#id21)示例代码即`result = application（environ，start_response）`
正好对应上前文中的接收的两个对象

### 3.中间件
本来仅有`1`和`2`就足够了，这里的中间件是可选功能（

## 0x02.传统`Web`服务与`Serverless`
> `Serverless`通常翻译为「无服务架构」，是一种软件系统设计架构思想和方法，并不是一个开发框架或者工具。它的出现是为了让开发者更加关注业务的开发，而将繁杂的运维和部署交给云厂商。`Serverless`由`Faas`和`Baas`组成，`Faas`为开发者提供业务运算环境，然后与`Baas`提供的数据和存储服务，进行交互，从而提供与传统服务一致的体验。但是由于`Faas`是无状态的，并且其运行环境是有读写限制的，最重要的是它是基于事件触发的。因此如果传统`Web`服务想迁移到`Serverless`上，是需要进行相关改造和特殊处理的，为此迁移成本是必不可少的

1. 传统`Web`服务：日常生活中接触最多的就是`HTTP`服务，客户端发起请求，服务端接受请求后进行处理最后返回响应。部署流程是需要将项目代码扔到云主机上
根据不用的语言启用不同的`Web`服务器常驻进程，并监听云主机相关接口，等待客户端的到来（
2. 而`Serverless`：客户端发起请求至`网关`，网关触发事件至`云函数`，`云函数`返回响应至网关最终到达客户端

云函数基于网关触发事件被调用，传统`Web`服务`Serverless`化的核心就是可以将`Event`对象转化为`HTTP`请求，也就是`Adapter`
[Serverless Components](https://github.com/serverless/components)中的高阶组件包含了开发者针对各框架的适配，整个工具是基于`node`写的，参照它的逻辑实际部署时会将`src`下的`_shims`文件原封不动地传到云函数根路径下
参考[tencent-flask](https://github.com/serverless-components/tencent-flask)这个`component`，会将`sl_handler.py`和`serverless_wsgi.py`这两个文件上传
1. [sl_handler.py](https://github.com/serverless-components/tencent-flask/blob/master/src/_shims/sl_handler.py)，这个文件的`handler`函数就是云函数的入口，自己项目可以自定义入口文件，因为使用了`工厂模式`故进行改写：
``` python
import severless_wsgi

from maimai_DX_CN_probe import create_app  # Replace with your actual application


# If you need to send additional content types as text, add then directly
# to the whitelist:
#
# serverless_wsgi.TEXT_MIME_TYPES.append("application/custom+json")

def handler(event, context):
    return severless_wsgi.handle_request(create_app(), event, context)
```
最后指定云函数的入口为`severless_handle.py`的`handler`函数即可
2. [severless_wsgi.py](https://github.com/serverless-components/tencent-flask/blob/master/src/_shims/severless_wsgi.py)，这个文件中的`handle_request(app, event, context)`函数则会将来自网关的`event`和`context`会转换为`environ`并调用`app`生成`response`，并可根据`网关`的需要进行`base64`编码

`Serverless Framework`的基础组件不仅包含`SCF 组件`目前还包含：`Website 组件`、`API 网关组件`、`VPC 组件`、`COS 组件`、`PostgreSQL 组件`、`CynosDB 组件`、`CDN 组件`、`Layer 组件`调度其他云上资源

## 0x03.再谈查分器
- 毕竟数据都是来自于爬虫，半年前基本写完的[maimai_DX_CN_saver](https://github.com/yuangezhizao/maimai_DX_CN_saver)也一直处于停滞状态中。
页面适配中大方面的排行榜是不打算去做了，实时性太强的数据存到本地基本上没有太大意义，参考[MuseDash](https://github.com/yuangezhizao/MuseDash)空间过大被发邮件，然后现在放到了[MuseDash-backup](https://yuangezhizao.coding.net/public/MuseDash/MuseDash-backup/git/files)，排行榜数据是以`json`格式存储的，后来用转化为`LFS`对象另存了一份[MuseDash](https://yuangezhizao.coding.net/public/MuseDash/MuseDash/git/files)
- 针对于查分器公开使用？目前已经实装了`Web`端手动存储，不过是提交一个含有原页面`html`的表单到后台再进行提取数据存入数据库的。因为`华立`封禁了云主机的`ip`也就是说爬虫云端肯定是做不了了，这在写完自动存储功能之后测试时才注意到……所以自动存储的功能只能在本地跑了（
- 趣事：使用`API 网关`时不支持响应内容压缩，于是自己去找了个`Flask`的库实装上，其实这本来是网关应该支持的功能，然后最近发现`API 网关`现在支持了（

## 0x04.后记
有了这次的开发经验，针对`wacca`音游可以写出一个类似的查分器了（

## 0x05.引用
[如何将 Web 框架迁移到 Serverless](https://my.oschina.net/u/4390465/blog/4355518)
[如何为Serverless架构做了一个Django的Component](https://zhuanlan.zhihu.com/p/109926704)

`2020-12-28 00:44:07`：晚上再来更新……