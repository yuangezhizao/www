---
title: 基于 Cloudflare Gateway + SmartDNS + AdGuard 的家用 DNS 方案
date: 2021-10-09 20:07:22
tags:
  - Cloudflare
  - SmartDNS
  - AdGuard
count: 1
os: 1
os_1: Monterry 12.0 Beta (21A5506j)
browser: 1
browser_1: 94.0.4606.81 Stable
place: 新家
key: 121
---
    这套方案也快用一年了，还算稳定于是分享出来
<!-- more -->
## 0x00.前言
`DNS`套娃（bushi

## 0x01.[Cloudflare Gateway](https://www.cloudflare.com/zh-cn/teams/gateway/)
最上游使用的是`Cloudflare for Teams`中的`Gateway`，在`Locations`加一个位置就可以获得独一无二的`DNS`服务器地址，目前包含如下四种
1. `IPv4`
2. `IPv6`
3. `DNS over HTTPS`
4. `DNS over TLS`

![PY](https://i1.yuangezhizao.cn/macOS/20211009202011.png!webp)

当然使用他家的`1.1.1.1`或者谷歌的`8.8.8.8`也是没有问题的，`Gateway`的优点之一在于所有查询都是有记录的
![Gateway Activity Log](https://i1.yuangezhizao.cn/macOS/20211009202355.png!webp)

`Teams`的`Free`版本订阅可追溯至最近`24h`，对于家用足够了，方便进行后期二次审计
![Free](https://i1.yuangezhizao.cn/macOS/20211009202814.png!webp)

同时也有自带的分析页面，可以看到最近一季度的解析量是`55M`
![Analytics](https://i1.yuangezhizao.cn/macOS/20211009203351.png!webp)

分类占比一半多（`50.3%`）的是`Technology`
![Requests by category](https://i1.yuangezhizao.cn/macOS/20211009203659.png!webp)

## 0x02.[SmartDNS](https://github.com/pymumu/smartdns)
> 前情回顾：[PY 云新增 CentOS 7.7 64 位#0x06-SmartDNS](../../Linux/CentOS/cn-py-dl-c7.html#0x06-SmartDNS)

> `SmartDNS`是一个运行在本地的`DNS`服务器，`SmartDNS`接受本地客户端的`DNS`查询请求，从多个上游`DNS`服务器获取`DNS`查询结果，并将访问速度最快的结果返回给客户端，提高网络访问速度。
同时支持指定特定域名`IP`地址，并高性匹配，达到过滤广告的效果。与`dnsmasq`的`all-servers`不同，`smartdns`返回的是访问速度最快的解析结果![架构](https://github.com/pymumu/test/releases/download/blob/architecture.png)

那么是直接将`Cloudflare Gateway`的`DNS`服务器填入网关？然而并不是，这里是填入到了`SmartDNS`的配置项之中
实测直接使用的话浏览器访问网页的加载速度比较慢，猜测是服务器位于国外，发起解析请求的速度肯定是赶不上国内的机子了，单独使用并不推荐除非可以忍受巨慢的解析
那么如何解决这个问题呢？从`/etc/smartdns/smartdns.conf`中的`server`配置项可以看出实际上还写入了其他的`DNS`提供商，然后利用`SmartDNS`的主打？功能测速后返回访问速度最快的解析结果
`SmartDNS`也推荐配置多个上游服务器，反正测速交给他就好了嘛（不过要是说因为写入了其他提供商而失去了`Cloudflare Gateway`的意义自己也无力反驳草，算了不管了
![如何配置上游服务器最佳](https://i1.yuangezhizao.cn/macOS/20211009205840.png!webp)

测速模式配置`speed-check-mode ping,tcp:80,tcp:443`，顾名思义就不做解释了
同时，在这一环节也可以开启审计日志
![如何启用审计日志](https://i1.yuangezhizao.cn/macOS/20211009210926.png!webp)
![内容示例](https://i1.yuangezhizao.cn/macOS/20211009210829.png!webp)

## 0x03.[AdGuard](https://adguard.com/zh_cn/welcome.html)
从上述审计日志的内容可以发现请求来自`192.168.25.246`的地址，而这个地址对应的服务是`HomeAssistant`，而`AdGuard Home`是以加载项的方式引入的
![AdGuard Home](https://i1.yuangezhizao.cn/macOS/20211009211708.png!webp)

`AdGuard`主要用来进行自定义拦截过滤（广告`+`追踪），`AdGuard`的上游服务器只有`SmartDNS`这一个来源
![仪表盘](https://i1.yuangezhizao.cn/macOS/20211009211923.png!webp)

可以按需订阅第三方整理好的列表，当然有误封风险了，可以核实后再加到白名单里取消拦截
![DNS 封锁清单](https://i1.yuangezhizao.cn/macOS/20211009212449.png!webp)

平时有需要封禁的域名只需填入到`自定义过滤规则`的列表即可，前两个环节可以开启审计日志，最后的这个环境自然也是可以的，并且是最便于查看的
![查询日志](https://i1.yuangezhizao.cn/macOS/20211009214135.png!webp)

`AdGuard Home`本身是支持`IPv4`和`IPv6`两种方式访问的，但可能由于在`HomeAssistant`中`Docker`网络配置的原因，目前只支持`IPv4`
![IPv4](https://i1.yuangezhizao.cn/macOS/20211009213056.png!webp)

把这个`IPv4`地址填到各种设备的网络`DNS`设置项中就算完成了整个流程，`DNS`套娃（bushi

## 0x04.后记
总结一句话：`Cloudflare Gateway`用于获得纯净的`DNS`解析结果，`SmartDNS`用于测速后返回访问速度最快的解析结果，`AdGuard`用于自定义拦截过滤
虽然看起来每个环节的部分功能都有重复之处，但是实践却发现每个环节都各自其职，必不可缺
最后再说下`Cloudflare for Teams`，最开始只有`Gateway`功能，而现在实装的功能越来越多，并且无料享受
这两天实际体验了下新出的`Access`和`Devices`等功能，后者~~当成备用梯子~~是真香`2333`

![Teams yes！](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2021-10-09-21-54-27-542_com.cloudflare.jpg!webp)
![WARP yes！](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2021-10-09-21-55-05-335_com.cloudflare.jpg!webp)

> 至此本文使命完成
