---
title: 【1024，Serverless】maimai_DX 查分器
date: 2020-10-20 20:21:59
tags:
  - Serverless
  - maimai_DX
count: 6
os: 1
os_1: High Sierra 10.13.6 (17G65)
browser: 0
browser_1: 86.0.4240.80 Stable
place: 新家
key: 101
---
    又到了一年一度的程序员节辣（提前的 1024
<!-- more -->
## 0x00.前言
社畜下班回到家楼下等电梯时刷微信时看到了[Serverless 有一百种玩法，比好玩更好玩](https://web.archive.org/web/20201020122345/https://mp.weixin.qq.com/s/jaCLx6gn3aHbLLptXvqsLQ)这篇推送文章，正巧自己最近几个月断断续续在写音游的历史记录存档，趁着这个机会决定参加这次应用开发

## 0x01.[Serverless Framework](https://web.archive.org/web/20201022123029/https://cloud.tencent.com/document/product/1154)
> `Serverless Framework`是业界非常受欢迎的无服务器应用框架，开发者无需关心底层资源即可部署完整可用的`Serverless`应用架构。`Serverless Framework`具有资源编排、自动伸缩、事件驱动等能力，覆盖编码、调试、测试、部署等全生命周期，帮助开发者通过联动云资源，迅速构建 `Serverless`应用

没错，就像几天前看到的《`Serverless`之歌》里面所说`I'm gonna reduce your ops`，它能大幅度减轻运维压力（也不得不佩服`aws`
那就开始动手吧！注意开发环境需`Node.js 10.0+`，一键全局安装：`npm install -g serverless`

<details><summary>点击此处 ← 查看终端</summary>

``` bash
Last login: Tue Oct 20 18:34:41 on ttys000
MacPro:maimai_DX_CN_probe yuangezhizao$ node -v
v14.14.0
MacPro:maimai_DX_CN_probe yuangezhizao$ npm -v
6.14.8
MacPro:~ yuangezhizao$ cd Documents/GitHub/maimai_DX_CN_probe/
MacPro:maimai_DX_CN_probe yuangezhizao$ npm install -g serverless
npm WARN deprecated request@2.88.2: request has been deprecated, see https://github.com/request/request/issues/3142
npm WARN deprecated request-promise-native@1.0.9: request-promise-native has been deprecated because it extends the now deprecated request package, see https://github.com/request/request/issues/3142
npm WARN deprecated har-validator@5.1.5: this library is no longer supported
/usr/local/bin/serverless -> /usr/local/lib/node_modules/serverless/bin/serverless.js
/usr/local/bin/sls -> /usr/local/lib/node_modules/serverless/bin/serverless.js

> snappy@6.3.5 install /usr/local/lib/node_modules/serverless/node_modules/snappy
> prebuild-install || node-gyp rebuild


> protobufjs@6.10.1 postinstall /usr/local/lib/node_modules/serverless/node_modules/protobufjs
> node scripts/postinstall


> serverless@2.8.0 postinstall /usr/local/lib/node_modules/serverless
> node ./scripts/postinstall.js


   ┌───────────────────────────────────────────────────┐
   │                                                   │
   │   Serverless Framework successfully installed!    │
   │                                                   │
   │   To start your first project run 'serverless'.   │
   │                                                   │
   └───────────────────────────────────────────────────┘

+ serverless@2.8.0
added 644 packages from 484 contributors in 522.774s
MacPro:maimai_DX_CN_probe yuangezhizao$ serverless -v
Framework Core: 2.8.0
Plugin: 4.1.1
SDK: 2.3.2
Components: 3.2.4
```

</details>

注：其中`Python`云函数运行环境仅仅支持`2.7`和`3.6`，本来想在本地安装一个`3.6`的最新版本`Python 3.6.12 - Aug. 17, 2020`
结果发现官网只提供源代码并没有`release`可执行文件，自己平日的开发环境是最新`Python 3.9.0 - Oct. 5, 2020`
~~后来想到其实只需要注意下大的语法变更就`ok`了，基本上应该问题不大~~

## 0x02.[腾讯云 Flask Serverless Component](https://github.com/serverless-components/tencent-flask)
> 腾讯云`Flask Serverless Component`，支持`Restful API`服务的部署，不支持`Flask Command`

本项目中并未实际使用`Flask Command`，故相当于没有任何限制，按照惯例首先来部署`demo`吧
1. 本地`PyCharm`创建一个新的`Flask`项目
![Flask](https://i1.yuangezhizao.cn/macOS/QQ20201020-212721@2x.png!webp)

2. 手动创建内容为`Flask`的`requirements.txt`
3. 按照[配置文档](https://github.com/serverless-components/tencent-flask/blob/master/docs/configure.md)创建`serverless.yml`，例如本项目实际使用的完整内容，初次使用可自行酌情简化

<details><summary>点击此处 ← 查看折叠</summary>

``` yml
component: flask # (必选) 组件名称，在该实例中为flask
name: maimai_DX_CN_probe # (必选) 组件实例名称.
org: yuangezhizao # (可选) 用于记录组织信息，默认值为您的腾讯云账户 appid，必须为字符串
app: yuangezhizao # (可选) 用于记录组织信息. 默认与name相同，必须为字符串
stage: dev # (可选) 用于区分环境信息，默认值是 dev

inputs:
  region: ap-beijing # 云函数所在区域
  functionName: maimai_DX_CN_probe # 云函数名称
  serviceName: maimai_DX_CN_probe # api网关服务名称
  runtime: Python3.6 # 运行环境
  #  src: ./src # 第一种为string时，会打包src对应目录下的代码上传到默认cos上。
  src:
    # TODO: 安装python项目依赖到项目当前目录
    hook: 'pip3 install -r ./src/requirements.txt -t ./src/requirements'
    dist: ./src
    include:
      - source: ./requirements
        prefix: ../ # prefix, can make ./requirements files/dir to ./
    exclude:
      - .env
      - 'src/requirements/**'
  # serviceId: service-np1uloxw # api网关服务ID
  # src:  # 第二种，部署src下的文件代码，并打包成zip上传到bucket上
  #   src: ./src  # 本地需要打包的文件目录
  #   bucket: bucket01 # bucket name，当前会默认在bucket name后增加 appid 后缀, 本例中为 bucket01-appid
  #   exclude:   # 被排除的文件或目录
  #     - .env
  #     - node_modules
  # src: # 第三种，在指定存储桶bucket中已经存在了object代码，直接部署
  #   bucket: bucket01 # bucket name，当前会默认在bucket name后增加 appid 后缀, 本例中为 bucket01-appid
  #   object: cos.zip  # bucket key 指定存储桶内的文件
  # layers:
  #   - name: layerName #  layer名称
  #     version: 1 #  版本
  functionConf: # 函数配置相关
    timeout: 10 # 超时时间，单位秒
    eip: true # 是否固定出口IP
    memorySize: 128 # 内存大小，单位MB
    environment: #  环境变量
      variables: #  环境变量数组
        DEBUG: false
    vpcConfig: # 私有网络配置
      vpcId: 'vpc-mrg5ak88' # 私有网络的Id
      subnetId: 'subnet-hqwa51dh' # 子网ID
  apigatewayConf: #  api网关配置
    isDisabled: false # 是否禁用自动创建 API 网关功能
    enableCORS: false #  允许跨域
    customDomains: # 自定义域名绑定
      - domain: maimai.yuangezhizao.cn # 待绑定的自定义的域名
        certificateId: hMMBPdz0 # 待绑定自定义域名的证书唯一 ID
          # 如要设置自定义路径映射，请设置为 false
        isDefaultMapping: false
          # 自定义路径映射的路径。使用自定义映射时，可一次仅映射一个 path 到一个环境，也可映射多个 path 到多个环境。并且一旦使用自定义映射，原本的默认映射规则不再生效，只有自定义映射路径生效。
        pathMappingSet:
          - path: /
            environment: release
          - path: /prepub
            environment: prepub
          - path: /test
            environment: test
        protocols: # 绑定自定义域名的协议类型，默认与服务的前端协议一致。
          #          - http # 支持http协议
          - https # 支持https协议
    protocols:
      #      - http
      - https
    environment: test
    serviceTimeout: 15
    # usagePlan: #  用户使用计划
    #   usagePlanId: 1111
    #   usagePlanName: slscmp
    #   usagePlanDesc: sls create
    #   maxRequestNum: 1000
    # auth: #  密钥
    #   secretName: secret
    #   secretIds:
    #     - xxx
```

</details>

4. 将密匙写入`.env`（这样就不用在部署时再拿起手机扫一扫了
``` bash
TENCENT_SECRET_ID=<rm>
TENCENT_SECRET_KEY=<rm>
```

<details><summary>点击此处 ← 查看终端</summary>

![成功部署](https://i1.yuangezhizao.cn/macOS/QQ20201020-225316@2x.png!webp)
![成功访问](https://i1.yuangezhizao.cn/macOS/QQ20201020-230006@2x.png!webp)

</details>

这样基于`Serverless`的`Flask`小`demo`就部署完成了，接下来继续按照自己的方式写剩下的代码

## 0x03.[舞萌查分器](https://maimai.yuangezhizao.cn/)
`gh`开源地址：[https://github.com/yuangezhizao/maimai_DX_CN_probe](https://github.com/yuangezhizao/maimai_DX_CN_probe)

## 0x04.遇到的问题以及解决思路
接下来将按照时间的顺序依次叙述一下开发过程中遇到的种种课题以及解决思路

### 1.`Serverless Framework Component`配置文件
纵观`Serverless Framework`，现在最新的是`V2`版本，也就是说不能沿袭之前版本的`serverless.yml`配置文件，需要重新对照文档修改
之前版本的配置文件可以参考这里：[实验室站迁移 TencentCloud Serverless 之路#0x03.部署 Python Flask 框架
](/init.html#2-配置Serverless)
也正是因为这个版本变化，导致配置文件有一处需要注意的地方
①之前版本会根据`requirements.txt`自动下载第三方库到项目目录下的`.serverless`文件夹下的`requirements`文件夹以参加最终的依赖打包，压缩成`zip`文件再最终上传至云函数运行环境
②最新版本不再自动下载，需要自行处理。不过官方示例已经给写了参考用法：[hook](https://github.com/serverless-components/tencent-flask/blob/49bc914fad091bad9202ac481042760509342b3d/example/serverless.yml#L8-L17)
``` yml
  src:
    # TODO: 安装python项目依赖到项目当前目录
    hook: 'pip3 install -r requirements.txt -t ./requirements'
    dist: ./
    include:
      - source: ./requirements
        prefix: ../ # prefix, can make ./requirements files/dir to ./
    exclude:
      - .env
      - 'requirements/**'
```
注释写的很清楚，使用`hook`去根据`requirements.txt`下载第三方库到项目目录下的`requirements`文件夹，避免第三方库导致本地文件夹管理混乱。然后`include`中指定了项目目录下的`requirements`文件夹在云端的`prefix`，即对于云端的云函数运行环境，`requirements`文件夹中的第三方库和项目目录是同级的，可以正常导入使用。当然了，本地运行使用的是全局的第三方库，并未用到项目目录下的`requirements`文件夹（

### 2.[层管理概述](https://web.archive.org/web/20201022122902/https://cloud.tencent.com/document/product/583/40159)
前者（指②）是一个很合理的设计，不过在实际环境中却发现了新的问题。完全一致的配置文件
``` yml
  src:
    hook: 'pip3 install -r ./src/requirements.txt -t ./src/requirements'
    dist: ./src
    include:
      - source: ./requirements
        prefix: ../
    exclude:
      - .env
```
在`macOS`下成功部署之后，云端的云函数编辑器中看到`requirements`文件夹不存在，第三方库和项目目录是同级的，的确没问题
不过在`Windows`下成功部署之后，云端的云函数编辑器中看到了`requirements`文件夹？也就是说第三方库和项目目录非同级，于是访问就会出现`no module found`的导入报错了……
反复尝试修改`prefix`等配置项到最后也没有调试成功，因此在这里提出两种解决方法
①修改配置文件如下，让本地的第三方库和项目目录同级存在
``` yml
  src:
    hook: 'pip3 install -r ./src/requirements.txt -t ./src'
    dist: ./src
    exclude:
      - .env
```
不过这样做自己是拒绝的，可想而知随着项目和第三方库的扩大文件夹会越来越多，非常不便于管理
②使用云函数提供的`层`
虽然`sls deploy`部署的速度很快，但是如果可以在部署时只上传项目代码而不去处理依赖不就更好了嘛，这样跨终协作端开发只需要关心项目代码就`ok`了
再也不需要管理依赖！并且还有一点，想在`SCF`控制台中在线编辑函数代码需要将部署程序包保持在`10MB`以下，不要以为十兆很大，很快就用光也是可能的
![仅显示入口文件](https://i1.yuangezhizao.cn/macOS/QQ20201022-210610@2x.png!webp)

具体如何操作呢？那就是要将第三方库文件夹直接打包并创建为层，则在函数代码中可直接通过`import`引用，毕竟有些特殊库比如`Brotli`，`windows`下没有`vc++`的话就只能去[https://lfd.uci.edu/~gohlke/pythonlibs](https://lfd.uci.edu/~gohlke/pythonlibs)下载`wheel`安装了
`macOS`下正常安装之后会得到`_brotli.cpython-39-darwin.so`，`brotli.py`中再以`import _brotli`的形式导入
不过又出新问题了，云端会导入报错`ModuleNotFoundError: No module named '_brotli'"`
> 当前`SCF`的执行环境建立在以下基础上：标准`CentOS 7.2`

为了解决问题尝试在`linux`环境下打包，拿起手头的`CentOS 8.2`云主机开始操作
``` bash
pip3 install -r requirements.txt -t ./layer --upgrade
zip -r layer.zip ./layer
```
然后就可以把打包的`layer.zip`下载到本地再传上去了，暂时可以一劳永逸了（
![层详细信息](https://i1.yuangezhizao.cn/macOS/QQ20201022-234808@2x.png!webp)

对了，配置文件可以移除`hook`并添加`layers`了
``` yml
  src:
    src: ./src
    exclude:
      - .env
      - '__pycache__/**'
  layers:
    - name: maimai_DX_CN_probe
      version: 3
```
> 已绑定层的函数被触发运行，启动并发实例时，将会解压加载函数的运行代码至`/var/user/`目录下，同时会将层内容解压加载至`/opt`目录下
若需使用或访问的文件`file`，放置在创建层时压缩文件的根目录下。则在解压加载后，可直接通过目录`/opt/file`访问到该文件。若在创建层时，通过文件夹进行压缩`dir/file`，则在函数运行时需通过`/opt/dir/file`访问具体文件

体验更快的部署速度吧！因为第三方库已经打包在“层”中了

<details><summary>点击此处 ← 查看终端</summary>

``` bash
MacPro:maimai_DX_CN_probe yuangezhizao$ sls deploy

serverless ⚡framework
Action: "deploy" - Stage: "dev" - App: "yuangezhizao" - Instance: "maimai_DX_CN_probe"

region: ap-beijing
apigw: 
  serviceId:     service-dn6wahj7
  subDomain:     service-dn6wahj7-1251901037.bj.apigw.tencentcs.com
  environment:   release
  url:           https://service-dn6wahj7-1251901037.bj.apigw.tencentcs.com/release/
  customDomains: 
    - 
      isBinded:  true
      created:   true
      subDomain: maimai.yuangezhizao.cn
      cname:     service-dn6wahj7-1251901037.bj.apigw.tencentcs.com
      url:       https://maimai.yuangezhizao.cn
scf: 
  functionName: maimai_DX_CN_probe
  runtime:      Python3.6
  namespace:    default
  lastVersion:  $LATEST
  traffic:      1

Full details: https://serverless.cloud.tencent.com/apps/yuangezhizao/maimai_DX_CN_probe/dev

15s › maimai_DX_CN_probe › Success
```

</details>

但是奇怪的是，在云端导入任意第三方库均会报错，于是调试着查看`path`
``` bash
for path in sys.path:
    print(path)

/var/runtime/python3
/var/user
/opt
/var/lang/python3/lib/python36.zip
/var/lang/python3/lib/python3.6
/var/lang/python3/lib/python3.6/lib-dynload
/var/lang/python3/lib/python3.6/site-packages
/var/lang/python3/lib/python3.6/site-packages/pip-18.0-py3.6.egg
```
再查看`opt`
``` bash
import os
dirs = os.listdir('/opt')

for file in dirs:
   print(file)

layer
```
这才恍然大悟，**打包时需要在当前路径直接打包**
上传之后“层”更新为版本`2`，但是`ModuleNotFoundError: No module named '_brotli'`报错依旧，并且确认`_brotli.cpython-38-x86_64-linux-gnu.so`文件实际存在
而在`CentOS`和`macOS`上本地导入均没有问题，这可就犯难了，又想到很有可能是`python`版本的问题，于是去寻找现成`3.6`的环境，比如这里
![3.6.8](https://i1.yuangezhizao.cn/macOS/QQ20201022-233709@2x.png!webp)

<details><summary>点击此处 ← 查看终端</summary>

``` bash
[root@txy ~]# rm -rf layer
[root@txy ~]# mkdir layer && cd layer
[root@txy layer]# vim requirements.txt
[root@txy layer]# cat requirements.txt 
Flask
Flask-SQLAlchemy
Flask-Zipper
brotli
python-dotenv
pymysql
[root@txy layer]# python -V
Python 3.8.6
[root@txy layer]# pip -V
pip 9.0.3 from /usr/lib/python3.6/site-packages (python 3.6)
[root@txy layer]# pip3 -V
pip 20.2.4 from /usr/local/python3/lib/python3.8/site-packages/pip (python 3.8)
[root@txy layer]# pip install -r requirements.txt -t . --upgrade
……
[root@txy layer]# zip -r layer.zip . -x requirements.txt
```

</details>

再再次上传之后“层”更新为版本`3`，访问成功！课题终于解决，原来是需要**相同版本**的`Python 3.6`运行环境

### 3.自定义入口文件
[components](https://github.com/serverless-components)源码[tencent-flask/src/_shims/](https://github.com/serverless-components/tencent-flask/tree/master/src/_shims)中的文件每次都会被原封不动地重新打包上传到云端云函数中，目前有两个文件
①`severless_wsgi.py`，作用是`converts an AWS API Gateway proxied request to a WSGI request.`
`WSGI`的全称是`Python Web Server Gateway Interface`即`Web 服务器网关接口`，它是为`Python`语言定义的`Web`服务器和`Web`应用程序或框架之间的一种简单而通用的接口
②`sl_handler.py`，就是默认的入口文件
``` python
import app  # Replace with your actual application
import severless_wsgi

# If you need to send additional content types as text, add then directly
# to the whitelist:
#
# serverless_wsgi.TEXT_MIME_TYPES.append("application/custom+json")

def handler(event, context):
    return severless_wsgi.handle_request(app.app, event, context)
```
针对于自己的项目，使用了`Flask`的`工厂函数`，为了避免每次都要在云端云函数编辑器中重新修改，最好的方法是自定义入口文件：
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
再指定`执行方法`为`serverless_handler.handler`，就`ok`了

### 4.`url_for`输出`http`而非`https`的`URL`
在视图函数中重定向到`url_for`所生成的链接都是`http`，而不是`https`……其实这个问题`Flask`的文档[Standalone WSGI Containers](https://flask.palletsprojects.com/en/1.1.x/deploying/wsgi-standalone/)有描述到
说到底这并不是`Flask`的问题，而是`WSGI`环境所导致的问题，推荐的方法是使用**中间件**，官方也给出了`ProxyFix`
``` python
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
```
但是是从`X-Forwarded-Proto`中取的值，`apigw`中其为`http`，因此并不能直接使用这个`ProxyFix`
因为`Flask`的社区还算完善，参考资料很多前人都铺好了路，所以直接去`Stack Overflow`搜解决方法，[Flask url_for generating http URL instead of https](https://stackoverflow.com/questions/14810795/flask-url-for-generating-http-url-instead-of-https)
问题出现的原因如图：`Browser ----- HTTPS ----> Reverse proxy（apigw） ----- HTTP ----> Flask`
因为自己在`apigw`设置了`前端类型`仅`https`，也就是说`Browser`端是不可能使用`http`访问到的，通过打印`environ`可知
``` json
{
  "CONTENT_LENGTH": "0",
  "CONTENT_TYPE": "",
  "PATH_INFO": "/",
  "QUERY_STRING": "",
  "REMOTE_ADDR": "",
  "REMOTE_USER": "",
  "REQUEST_METHOD": "GET",
  "SCRIPT_NAME": "",
  "SERVER_NAME": "maimai.yuangezhizao.cn",
  "SERVER_PORT": "80",
  "SERVER_PROTOCOL": "HTTP/1.1",
  "wsgi.errors": <__main__.CustomIO object at 0x7feda2224630>,
  "wsgi.input": <_io.BytesIO object at 0x7fed97093410>,
  "wsgi.multiprocess": False,
  "wsgi.multithread": False,
  "wsgi.run_once": False,
  "wsgi.url_scheme": "http",
  "wsgi.version": (1, 0),
  "serverless.authorizer": None,
  "serverless.event": "<rm>",
  "serverless.context": "<rm>",
  "API_GATEWAY_AUTHORIZER": None,
  "event": "<rm>",
  "context": "<rm>",
  "HTTP_ACCEPT": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
  "HTTP_ACCEPT_ENCODING": "gzip, deflate, br",
  "HTTP_ACCEPT_LANGUAGE": "zh-CN,zh;q=0.9,en;q=0.8",
  "HTTP_CONNECTION": "keep-alive",
  "HTTP_COOKIE": "<rm>",
  "HTTP_ENDPOINT_TIMEOUT": "15",
  "HTTP_HOST": "maimai.yuangezhizao.cn",
  "HTTP_SEC_FETCH_DEST": "document",
  "HTTP_SEC_FETCH_MODE": "navigate",
  "HTTP_SEC_FETCH_SITE": "none",
  "HTTP_SEC_FETCH_USER": "?1",
  "HTTP_UPGRADE_INSECURE_REQUESTS": "1",
  "HTTP_USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
  "HTTP_X_ANONYMOUS_CONSUMER": "true",
  "HTTP_X_API_REQUESTID": "5bcb29af2ca18c1e6d7b1ec5ff7b5427",
  "HTTP_X_API_SCHEME": "https",
  "HTTP_X_B3_TRACEID": "5bcb29af2ca18c1e6d7b1ec5ff7b5427",
  "HTTP_X_QUALIFIER": "$LATEST"
}
```
`HTTP_X_FORWARDED_PROTO`对应`apigw`里的变量是`HTTP_X_API_SCHEME`，故解决方法如下：[app.wsgi_app = ReverseProxied(app.wsgi_app)](`https://github.com/yuangezhizao/maimai_DX_CN_probe/blob/4600b3d8212777cb6184c796c1967b3ea9b05997/src/maimai_DX_CN_probe/__init__.py#L36`)
``` python
class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = environ.get('HTTP_X_FORWARDED_PROTO')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)

app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)
```

### 5.响应数据压缩
不论是`IIS`、`Apache`还是`Nginx`，都提供有压缩功能。毕竟自己在用的云主机外网上行只有`1M`带宽，压缩后对于缩短首屏时间的效果提升极为显著。对于`Serverless`，响应数据是通过`API Gateway`传输到客户端，那么压缩也应该是它所具备的能力（虽然外网速度大幅度提高，但是该压缩还是得压缩），然而并没有找到……看到某些`js`框架原生有提供压缩功能，于是打算添加`Flask`自行压缩的功能。简单来讲，通过订阅`@app.after_request`信号并调用第三方库`brotli`的`compress`方法即可（
在写之前去`gh`上看看有没有现成的轮子拓展，果然有……刚开始用的是`Flask-Zipper`，后来换成`Flask-Compress`解决了问题
实测`3.1 MB`的数据采用`brotli`压缩算法减至`76.1 kB`

<details><summary>点击此处 ← 查看折叠</summary>

![压缩前](https://i1.yuangezhizao.cn/macOS/QQ20201023-223613@2x.png!webp)
![压缩后](https://i1.yuangezhizao.cn/macOS/QQ20201023-224633@2x.png!webp)
![br](https://i1.yuangezhizao.cn/macOS/QQ20201023-224722@2x.png!webp)

</details>

### 6.`apigw`三种环境不同路径所产生的影响
默认的映射如下：

ID | 环境名 | 访问路径
:---: | :---: | :---:
1 | 发布 | release
2 | 预发布 | prepub	
3 | 测试 | test

因为配置的`static_url_path`为`""`，即`static`文件夹是映射到`/`路径下的，所以再加上`release`、`prepub`和`test`访问就自然`404`了
因此绑定了`自定义域名`，`使用自定义路径映射`，并将`发布`环境的访问路径设置成`/`，这样再访问`发布`环境就没有问题了

ID | 环境名 | 访问路径
:---: | :---: | :---:
1 | 发布 | /
2 | 预发布 | prepub	
3 | 测试 | test

### 7.同时访问`私有网络`和`外网`
`云函数`中可以利用到的云端数据库有如下几种
1. 云数据库`CDB`，需要`私有网络`访问，虽然可以通过外网访问但是能走内网就不走外网
2. `PostgreSQL for Serverless（ServerlessDB）`，这个是官方给`Serverless`配的`pg`数据库
3. 云开发`TCB`中的`MongoDB`，没记错的话需要开通内测权限访问

因为自己是从旧网站迁移过来的，数据暂时还没有迁移，因此直接访问原始云数据库`CDB`，在`云函数`配置`所属网络`和`所属子网`即可
但是此时会无法访问外网，一种解决方法是开启`公网访问`和`公网固定IP`，就可以同时访问内网和外网资源了

下列问题处于解决之中：
1. `http`强制跳转`https`
2. 测试环境推送至生产环境

## 0x05.后记

未完待续……
