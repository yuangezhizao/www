---
title: 【1024，Serverless】maimai_DX 查分器
date: 2020-10-20 20:21:59
tags:
  - Serverless
  - maimai_DX
count: 1
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
社畜下班回到家楼下等电梯时刷微信时看到了[Serverless 有一百种玩法，比好玩更好玩](https://web.archive.org/web/20201020122345/https://mp.weixin.qq.com/s/jaCLx6gn3aHbLLptXvqsLQ)这篇推送文章
正巧自己最近几个月一直在写音游的历史记录存档，趁着这个机会决定来玩儿这次应用开发

## 0x01.[Serverless Framework](https://cloud.tencent.com/document/product/1154)
> `Serverless Framework`是业界非常受欢迎的无服务器应用框架，开发者无需关心底层资源即可部署完整可用的`Serverless`应用架构。`Serverless Framework`具有资源编排、自动伸缩、事件驱动等能力，覆盖编码、调试、测试、部署等全生命周期，帮助开发者通过联动云资源，迅速构建 `Serverless`应用

注意开发环境需`Node.js 10.0+`，一键全局安装：`npm install -g serverless`

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

其中`Python`云函数运行环境仅仅支持`2.7`和`3.6`，本来想在本地安装一个`3.6`的最新版本`Python 3.6.12 - Aug. 17, 2020`
结果发现官网只提供有源代码而并没有`release`可执行文件，本地环境是最新的`Python 3.9.0 - Oct. 5, 2020`
后来想到其实只需要注意下大的语法变更就`ok`了，基本上应该问题不大

## 0x02.[部署 Python Flask](https://github.com/serverless-components/tencent-flask)
> 腾讯云`Flask Serverless Component`，支持`Restful API`服务的部署，不支持`Flask Command`

因为项目中并未实际使用`Flask Command`，因此相当于没有任何限制，惯例首先来部署`demo`吧
1. 本地`PyCharm`创建一个新的`Flask`项目
![Flask](https://i1.yuangezhizao.cn/macOS/QQ20201020-212721@2x.png!webp)

2. 手动创建内容为`Flask`的`requirements.txt`
3. 按照[配置文档](https://github.com/serverless-components/tencent-flask/blob/master/docs/configure.md)创建`serverless.yml`，这里贴出的是完整版，初次使用可以酌情简化

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

4. 将密匙写入`.env`（这样就不用每次部署时拿起手机扫一扫了
``` bash
TENCENT_SECRET_ID=<rm>
TENCENT_SECRET_KEY=<rm>
```

![成功部署](https://i1.yuangezhizao.cn/macOS/QQ20201020-225316@2x.png!webp)
![成功访问](https://i1.yuangezhizao.cn/macOS/QQ20201020-230006@2x.png!webp)

## 0x03.后记
![error](https://i1.yuangezhizao.cn/macOS/QQ20201020-223004@2x.png!webp)

果不其然，是没有添加`hook`的选项，于是重新修改，终于部署成功！

未完待续……
