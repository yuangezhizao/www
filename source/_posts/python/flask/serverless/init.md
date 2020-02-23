---
title: 实验室站迁移 TencentCloud Serverless 之路
date: 2020-2-23 19:46:43
tags:
  - Flask
  - TencentCloud
  - Serverless
count: 1
os: 0
os_1: 10.0.17763.1039 2019-LTSC
browser: 0
browser_1: 78.0.3904.108 Stable
place: 新家
key: 75
---
    这周在家 996 终于抽出时间了，然而今晚就要截稿了……
<!-- more -->
## 0x00.前言
到现在`Serverless`举行了`4`次线上直播，每次都参加并提交了作业，一路下来感觉还不错~~（并收割了`3`个公仔等待发货）~~`(｀・ω・´)`
然后看到[Serverless 粉丝，腾讯云喊你领取“专属”T恤！](https://web.archive.org/web/20200223123443/https://mp.weixin.qq.com/s/2z83fjYsJteEQTcv3f4oig)，觉得还是有必要写一下感想之类的，其实也确实想把自己的[实验室](https://lab.yuangezhizao.cn)站迁移到`Serverless`试试看

## 0x01.[TencentCloud Serverless](https://serverless.com/cn)
不得不感叹互联网时代科技的进步，之前[实验室站 Python 3.7.2 + Flask 1.0.2 + mod_wsgi 4.6.5 + Apache 2.4.38 + HTTP/2 + TLSv1.3 + brotli](../lab.html)这篇文章里写过传统方法发布网站的环境部署，虽然现在熟悉了操作并不觉得很麻烦，但是对于从来没接触过这块的人来说就比较难懂了`o(ﾟДﾟ)っ！`
而现在有了`Serverless`，就可以完全无视上面的操作步骤了，这里引用官网的两段话：
> `Serverless Framework`可以帮您以更少的成本和开销, 快速构建`Serverless`应用。它能够完美支持无服务器应用的开发，部署，测试，监控等环节。

> 关于`Serverless`：`Serverless`面向未来的运维方式
网络应用正在慢慢改变世界，但是大多数互联网企业仍然无法顺畅交付工程，更不用说敏捷开发和快速迭代了。**所以我们必须从根本上简化应用工程的交付和操作。**<br>
这就是**无服务器架构**所提供的`serverless`建立在下一代公共云服务之上，该服务仅在使用时自动扩容和收费。当规模， 所用容量和成本管理实现自动化时，可节省`99%`的成本管理。<br>
无服务器架构是全新的，因此我们需要改变先前对老架构和工作流的看法。`serverless`的目标是以一种简单，强大而优雅的使用体验为开发者，团队提供开发和运行`serverless`应用程序所需的所有工具。

是不是很方便`2333`，本人现在倒是觉得对于**个人**开发者来说，如果想构建轻量应用的话，用`Serverless`应该会节省非常多的时间
当然了，`Serverless`对比传统型应用还是有区别的，目前它并不能完美支持，举一个例子：`Flask CLI`就不支持（不过这倒是小事情了
对于**企业**开发者来说也是同理的，想快速上线一套网站的话，部署在一个服务器上倒是好说（就好比本人现在的[实验室](https://lab.yuangezhizao.cn)站，日`pv`两位数。。。），可是当访问量上升之后，需要扩容的时候就比较麻烦了，这时候你得在多个服务器上部署并且配置负载均衡等等
说了这么多，对本人来说，可能觉得最大的优点在于运维部署方面吧……

## 0x02.[安装](https://serverless.com/cn/framework/docs/getting-started/)
`Serverless Framework`是基于`Node.js`的开源`CLI`，注：需`Node 8+`
全局安装：
```
npm install serverless -g
```
这里没有使用`cnpm`的原因是因为网络还算`ok`没有特别耗时，另外忘记了之前在哪里看到过`cnpm`不会更新`package-lock.json`也就没有再去用第三方源
之后更新的话就：
```
npm update serverless -g
```
官网的`快速开始`教程之后快速部署了个`demo`，即：
```
serverless create -t tencent-nodejs
```
命令里的`tencent-nodejs`是众多组件中的一个，组件列表：[https://github.com/serverless/components](https://github.com/serverless/components)

## 0x03.[部署 Python Flask 框架](https://serverless.com/cn/framework/docs/providers/tencent/components/high-level-components/tencent-flask/)
因为本人对`Flask`还算熟悉，所以干脆把部署这个`Component`当成`Hello World`好了
其中官网简介里写道：
> 注 ：任何支持`WSGI（Web Server Gateway Interface）`的`Python`服务端框架都可以通过该组件进行部署，例如 `Falcon`框架等。

### 1. 创建新项目
#### 1. 基于模板
通过`sls`直接根据模板创建服务，`gh`上有很多模板
比如`https://github.com/serverless/components/tree/master/templates/tencent-flask`
```
serverless create --template-url https://github.com/serverless/components/tree/master/templates/tencent-flask
```
<details><summary>点击此处 ← 查看源码</summary>

``` python
# -*- coding: utf8 -*-

import json
from flask import Flask, jsonify, request
app = Flask(__name__)


@app.route("/")
def index():
    return "Hello Flash"

@app.route('/user', methods = ['POST'])
def addUser():
    # we must get request body from clound function event;
    event = request.environ['event']
    user = json.loads(event['body'])
    return jsonify(data=user)


@app.route("/user", methods = ['GET'])
def listUser():
    users = [{'name': 'test1'}, {'name': 'test2'}]
    return jsonify(data=users)


@app.route("/user/<id>", methods = ['GET'])
def getUser(id):
    return jsonify(data={'name': 'test1'})
```
</details>

#### 2. 不基于模板
在`Pycharm`创建一个新的`Flask`项目：`LAB_Serverless`以区别之前的`LAB`
![New Project](https://i1.yuangezhizao.cn/Win-10/20200223204026.jpg!webp)
![app.py](https://i1.yuangezhizao.cn/Win-10/20200223204236.jpg!webp)

真的是无比熟悉的经典代码`2333`
<details><summary>点击此处 ← 查看源码</summary>

``` python
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
```
</details>

`requirements.txt`？别急，先往下看

### 2. 配置`Serverless`
1. 创建`serverless.yml`，这里更改了几处配置
``` yml
MyComponent:
  component: '@serverless/tencent-flask'
  inputs:
    region: ap-beijing
    functionName: LAB_Serverless
    code: ./
    functionConf:
      timeout: 10
      memorySize: 128
      environment:
        variables:
          TEST: value
          Version: 2020-2-23_21:01:44
      vpcConfig:
        subnetId: ''
        vpcId: ''
    apigatewayConf:
      protocol: https
      environment: test
```
2. 创建`.env`，写入密匙（因为懒得每次部署都得拿起手机扫一扫授权`(^_−)☆`
``` env
TENCENT_SECRET_ID=<rm>
TENCENT_SECRET_KEY=<rm>
```

### 3. 部署
`serverless`的缩写是`sls`，因此也可以用`sls`简化命令
但是这里报错了……报错的原因是`requirements`文件夹不存在`(╯°Д°)╯`

<details><summary>点击此处 ← 查看终端</summary>

``` bash
Microsoft Windows [版本 10.0.17763.1039]
(c) 2018 Microsoft Corporation。保留所有权利。

D:\yuangezhizao\Documents\PycharmProjects\LAB_Serverless>sls --debug

  DEBUG ─ Resolving the template's static variables.
  DEBUG ─ Collecting components from the template.
  DEBUG ─ Downloading any NPM components found in the template.
  DEBUG ─ Analyzing the template's components dependencies.
  DEBUG ─ Creating the template's components graph.
  DEBUG ─ Syncing template state.
  DEBUG ─ Executing the template's components graph.
  DEBUG ─ Compressing function LAB_Serverless file to D:\yuangezhizao\Documents\PycharmProjects\LAB_Serverless\.serverless/LAB_Serverless.zip.
(node:22500) UnhandledPromiseRejectionWarning: Error: ENOENT: no such file or directory, stat 'D:\yuangezhizao\Documents\PycharmProjects\LAB_Serverless\.
serverless\requirements'eploying
    at Object.statSync (fs.js:946:3)
    at Object.statSync (C:\Users\yuangezhizao\AppData\Roaming\npm\node_modules\serverless\node_modules\_graceful-fs@4.2.3@graceful-fs\polyfills.js:308:16
)
    at WriteStream.<anonymous> (C:\Users\yuangezhizao\.serverless\components\registry\npm\@serverless\tencent-flask@0.2.0\node_modules\@serverless\tencen
t-flask\node_modules\@serverless\tencent-scf\library\utils.js:124:20)
    at WriteStream.emit (events.js:304:20)
    at C:\Users\yuangezhizao\.serverless\components\registry\npm\@serverless\tencent-flask@0.2.0\node_modules\@serverless\tencent-flask\node_modules\grac
eful-fs\graceful-fs.js:298:14
    at C:\Users\yuangezhizao\.serverless\components\registry\npm\@serverless\tencent-flask@0.2.0\node_modules\@serverless\tencent-flask\node_modules\grac
eful-fs\graceful-fs.js:325:16
    at C:\Users\yuangezhizao\AppData\Roaming\npm\node_modules\serverless\node_modules\_graceful-fs@4.2.3@graceful-fs\graceful-fs.js:325:16
    at FSReqCallback.oncomplete (fs.js:152:23)
(node:22500) UnhandledPromiseRejectionWarning: Unhandled promise rejection. This error originated either by throwing inside of an async function without
a catch block, or by rejecting a promise which was not handled with .catch(). (rejection id: 1)
(node:22500) [DEP0018] DeprecationWarning: Unhandled promise rejections are deprecated. In the future, promise rejections that are not handled will termi
nate the Node.js process with a non-zero exit code.

  194s » MyComponent » canceled

终止批处理操作吗(Y/N)? Y

D:\yuangezhizao\Documents\PycharmProjects\LAB_Serverless>
```
</details>

然后去`.serverless`文件下的`Template.MyComponent.pyRequirements.json`文件中看到了`requirements.txt`
这里其实是故意操作的（特意没添加`requirements.txt`），说明`requirements.txt`必须存在`(｡･ω･｡)`
![requirements](https://i1.yuangezhizao.cn/Win-10/20200223212104.jpg!webp)

因此，去创建文件内容为`Flask`的`requirements.txt`
<details><summary>点击此处 ← 查看终端</summary>

``` bash
D:\yuangezhizao\Documents\PycharmProjects\LAB_Serverless>sls --debug

  DEBUG ─ Resolving the template's static variables.
  DEBUG ─ Collecting components from the template.
  DEBUG ─ Downloading any NPM components found in the template.
  DEBUG ─ Analyzing the template's components dependencies.
  DEBUG ─ Creating the template's components graph.
  DEBUG ─ Syncing template state.
  DEBUG ─ Executing the template's components graph.
  DEBUG ─ Generated requirements from D:\yuangezhizao\Documents\PycharmProjects\LAB_Serverless\requirements.txt in D:\yuangezhizao\Documents\PycharmProje
cts\LAB_Serverless\.serverless\requirements.txt...
  DEBUG ─ Installing requirements from C:\Users\yuangezhizao\AppData\Local\Yugasun\serverless-python-requirements\Cache\2a1a661c4e3e6faadab5d001bc10cc3ac
ccf648921aad7c279d94f138eaaf833_slspyc\requirements.txt ...
  DEBUG ─ Using download cache directory C:\Users\yuangezhizao\AppData\Local\Yugasun\serverless-python-requirements\Cache\downloadCacheslspyc
  DEBUG ─ Running ...
  DEBUG ─ Compressing function LAB_Serverless file to D:\yuangezhizao\Documents\PycharmProjects\LAB_Serverless\.serverless/LAB_Serverless.zip.
  DEBUG ─ Compressed function LAB_Serverless file successful
  DEBUG ─ Uploading service package to cos[sls-cloudfunction-ap-beijing-code]. sls-cloudfunction-default-LAB_Serverless-1582464464.zip
  DEBUG ─ Uploaded package successful D:\yuangezhizao\Documents\PycharmProjects\LAB_Serverless\.serverless/LAB_Serverless.zip
  DEBUG ─ Creating function LAB_Serverless
  DEBUG ─ Created function LAB_Serverless successful
  DEBUG ─ Setting tags for function LAB_Serverless
  DEBUG ─ Creating trigger for function LAB_Serverless
  DEBUG ─ Deployed function LAB_Serverless successful
  DEBUG ─ Starting API-Gateway deployment with name MyComponent.TencentApiGateway in the ap-beijing region
  DEBUG ─ Service with ID service-0ok85tqh created.
  DEBUG ─ API with id api-ivk6tk0y created.
  DEBUG ─ Deploying service with id service-0ok85tqh.
  DEBUG ─ Deployment successful for the api named MyComponent.TencentApiGateway in the ap-beijing region.

  MyComponent: 
    region:              ap-beijing
    functionName:        LAB_Serverless
    apiGatewayServiceId: service-0ok85tqh
    url:                 http://service-0ok85tqh-1251901037.bj.apigw.tencentcs.com/test/

  44s » MyComponent » done


D:\yuangezhizao\Documents\PycharmProjects\LAB_Serverless>
```
</details>

趁机看下部署成功之后的`.serverless`文件夹：
![.serverless](https://i1.yuangezhizao.cn/Win-10/20200223212917.jpg!webp)

`Template.MyComponent.TencentCloudFunction.json`即`云函数`：
``` json
{
  "deployed": {
    "Name": "LAB_Serverless",
    "Runtime": "Python3.6",
    "Handler": "api_service.handler",
    "MemorySize": 128,
    "Timeout": 10,
    "Region": "ap-beijing",
    "Description": "This is a template function"
  }
}
```
第三方包全在这里：
![requirements](https://i1.yuangezhizao.cn/Win-10/20200223213223.jpg!webp)

`Template.MyComponent.TencentApiGateway.json`即`API 网关`
``` json
{
  "protocols": [
    "http"
  ],
  "subDomain": "service-0ok85tqh-1251901037.bj.apigw.tencentcs.com",
  "environment": "test",
  "region": "ap-beijing",
  "service": {
    "value": "service-0ok85tqh",
    "created": true
  },
  "apis": [
    {
      "path": "/",
      "method": "ANY",
      "apiId": {
        "value": "api-ivk6tk0y",
        "created": true
      }
    }
  ]
}
```
也就是说`CLI`自动帮我们创建`SCF`并将运行环境一并上传，再创建`API 网关`配置到`SCF`的触发器上
这里比较奇怪的一点是，怎么是`http`？？？明明配置的`https`呀，难道测试环境只有`http`？`(╯°Д°)╯︵┻━┻`
``` yml
apigatewayConf:
    protocol: https
    environment: test
```
到这里`demo`就搞定了，已经可以正常访问了
![api_service.py](https://i1.yuangezhizao.cn/Win-10/20200223220344.jpg!webp)

## 0x04.原理深入
这里说的`深入`其实有点儿夸大其词了，本人也就个业余的开发者而已……
去云函数看实际运行环境，发现把`.idea`文件夹也给上传了`2333`
另外，多了如下俩本地没有的文件：
![api_service.py](https://i1.yuangezhizao.cn/Win-10/20200223214149.jpg!webp)
![serverless.wsgi](https://i1.yuangezhizao.cn/Win-10/20200223214408.jpg!webp)

其实这就是`serverless`的核心了，`serverless`配置静态页面的原理自己是清楚的
比如`Hexo`那玩楞，就是生成页面之后扔到`COS`上就能访问了
但是，对于动态页面就比较好奇了，这是怎么实现的呢，其实就是靠着`serverless.wsgi`这个文件等等
自然能看到这个模块描述：`此模块将 AWS API Gateway 代理请求转换为 WSGI 请求。`
``` python
"""
This module converts an AWS API Gateway proxied request to a WSGI request.

Inspired by: https://github.com/miserlou/zappa

Author: Logan Raarup <logan@logan.dk>
"""
```
还是相当有意思的`(｀・ω・´)`

## 0x05.迁移`LAB`
接下来就得一点儿一点儿进行迁移了，不难想到应该有非常多的坑的，比如如何访问自己的`MySQL`、`Redis`、
`MongoDB`，再比如`Celery`计划任务，自己是用`RabbitMQ`的消息队列，这东西要怎么上云？这些问题都是自己需要后期去解决的……
毕竟上大学就开始写的网站，有非常非常多的依赖……
[更新日志](https://lab.yuangezhizao.cn/update)：
> 当前 git 版本：7a65018，总提交 824 次

## 0x06.后记
迁移注定是一个大工程，写了俩个半小时仿佛也没写出多少精华的东西来，就又得准备睡觉了，明早迎接新一周`8.5 8.5 6`生活
写到最后倒是觉得可以当成一个系列来写，从下一篇开始写起迁移的各种填坑……

未完待续……