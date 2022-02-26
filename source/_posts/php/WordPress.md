---
title: 【玩转腾讯云】WordPress 建站实战分享
date: 2021-05-07 00:00:00
tags:
  - Serverless
count: 1
os: 1
os_1: Monterey 12.0 Beta (21A5268h)
browser: 0
browser_0: 91.0.4472.114 Stable
place: 新家
key: 116
---
    到头来还是得从云加社区同步过来草
<!-- more -->
## 0x01.公测活动
从[云函数](https://cloud.tencent.com/product/scf)和[API网关](https://cloud.tencent.com/product/apigw)控制台的`banner`可以看到，`Serverless WordPress`建站提供了公测期间免费体验的活动！
![云函数](https://i1.yuangezhizao.cn/ask-qcloudimg-com/http-save/yehe-226318/5f4096bipn.png!view)
![API 网关](https://i1.yuangezhizao.cn/ask-qcloudimg-com/http-save/yehe-226318/l0rmf5hss.png!view)
![公测活动](https://i1.yuangezhizao.cn/ask-qcloudimg-com/http-save/yehe-226318/8f00brycwa.png!view)
![五种云产品均有优惠券赠送](https://i1.yuangezhizao.cn/ask-qcloudimg-com/http-save/yehe-226318/1ihautxqjr.png!view)
![就算是公测结束之后，也有预付费包可以购买](https://i1.yuangezhizao.cn/ask-qcloudimg-com/http-save/yehe-226318/0ew8p0wfo9.png!view)

## 0x02.部署应用
点击 [https://console.cloud.tencent.com/sls/create?t=wordpress&from=gw](https://console.cloud.tencent.com/sls/create?t=wordpress&from=gw) 此链接通过模板创建应用，如下图
![快速部署一个 Wordpress 框架](https://i1.yuangezhizao.cn/ask-qcloudimg-com/http-save/yehe-226318/zhc315fbia.png!view)

输入自定义的应用名称：`wordpress`
环境选择默认的：开发环境
地域修改为：北京
![新建应用](https://i1.yuangezhizao.cn/ask-qcloudimg-com/http-save/yehe-226318/faypup12ki.png!view)

点击完成，开始部署，可以在部署日志中看到进度，这里需要稍等一段时间（自己部署时卡在`Downloading code`一段时间……
![开始部署](https://i1.yuangezhizao.cn/ask-qcloudimg-com/http-save/yehe-226318/7kj4yunwyi.png!view)
![大约需要一分半钟的时间](https://i1.yuangezhizao.cn/ask-qcloudimg-com/http-save/yehe-226318/s7jo4ukz6p.png!view)
![然而光下载等了接近 20 分钟，后面部署倒是很快](https://i1.yuangezhizao.cn/ask-qcloudimg-com/http-save/yehe-226318/414g1e9gs1.png!view)

可以看到这里报错了，是因为没有授权`CFS`，因为之前是需要付费开通的，所以就一直没有授权
```js
[2021-05-06 17:57:07]  Error: 获取cfs信息错误。({"Error": {"Code": "AuthFailure.UnauthorizedOperation", "Message": "CAM signature/authentication error: request unauthorized([request id:663878175]you are not authorized to perform operation (cfs:DescribeCfsFileSystems)\nresource (qcs::cfs:ap-beijing:uin/954078278:filesystem/*) has no permission\n)"}, "RequestId": "2105555b-e5a8-4af0-a992-4fd7c144d26b"}) (reqId: d5c8a801-34c9-4bd4-950b-4077f1ad8034)
```
![注销应用](https://i1.yuangezhizao.cn/ask-qcloudimg-com/http-save/yehe-226318/52a6vsmzuz.png!view)

部署失败的同时收到了邮件，是代金券到账的消息（好像少了两种服务的优惠券？
![收到代金券](https://i1.yuangezhizao.cn/ask-qcloudimg-com/http-save/yehe-226318/zjtaiej8tg.png!view)

随便点到一个云函数里，可以看到关联的文件系统资源
![申请](https://i1.yuangezhizao.cn/ask-qcloudimg-com/http-save/yehe-226318/r66wvdwfq6.png!view)

参照[https://cloud.tencent.com/document/product/583/46199](https://cloud.tencent.com/document/product/583/46199)进行权限追加
在访问管理[https://console.cloud.tencent.com/cam/role](https://console.cloud.tencent.com/cam/role)，的角色中找到`SCF_QcsRole`，点击关联策略
![角色](https://i1.yuangezhizao.cn/ask-qcloudimg-com/http-save/yehe-226318/1bskm26ga9.png!view)

添加`QcloudCFSReadOnlyAccess`的策略
![关联策略](https://i1.yuangezhizao.cn/ask-qcloudimg-com/http-save/yehe-226318/gx4sj0a0hn.png!view)
![关联完成](https://i1.yuangezhizao.cn/ask-qcloudimg-com/http-save/yehe-226318/gu5gmubonh.png!view)

然后重新部署，第二次部署的时候速度变得很快
```js
Downloading code
Initializing node.js environment
Installing plugins
Processing serverless config files
Deploying serverless project
```
耗时四分钟不到，从日志中可以看到创建了`VPC`、`CFS`、`CynosDB cluster`、`apigw`、云函数`wpInitFaas`和`wpServerFaas`，云函数关联了`layer`
![操作成功](https://i1.yuangezhizao.cn/ask-qcloudimg-com/http-save/yehe-226318/db7xwnreh1.png!view)

## 0x03.初始化应用
进入管理登录地址
![资源列表](https://i1.yuangezhizao.cn/ask-qcloudimg-com/http-save/yehe-226318/ldm37ndpft.png!view)

填写信息后，点击安装
![初始化](https://i1.yuangezhizao.cn/ask-qcloudimg-com/http-save/yehe-226318/t0zlex7dns.png!view)

安装完成之后，即可进入后台管理页面，就可以写文章进行发布了
![成功](https://i1.yuangezhizao.cn/ask-qcloudimg-com/http-save/yehe-226318/j0c0t3qhsz.png!view)
![仪表盘](https://i1.yuangezhizao.cn/ask-qcloudimg-com/http-save/yehe-226318/fjprwjflo9.png!view)
![首页](https://i1.yuangezhizao.cn/ask-qcloudimg-com/http-save/yehe-226318/i6av5z4oqy.png!view)

## 0x04.后记
趁着这次机会体会到了`serverless`和腾讯云其他产品的结合，`CFS`和`TDSQL-C Serverless`实现了远程挂载和数据存储的需求，因此`wordpress`部署在`serverless`上才得以实现，对传统服务的流程进行了替换
![架构图](https://i1.yuangezhizao.cn/ask-qcloudimg-com/http-save/yehe-226318/xa4bg63ey3.png!view)
