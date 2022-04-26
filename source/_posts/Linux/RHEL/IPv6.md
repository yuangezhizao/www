---
title: IPv6 + V2Ray 实现在外回无公网 IP 的家
date: 2022-04-26 22:18:34
tags:
  - IPv6
  - V2Ray
count: 1
os: 1
os_1: Monterry 12.3.1 (21E258)
browser: 0
browser_1: 100.0.4896.127 Stable
place: 新家
key: 139
---
    没错，22 年终于计划升至千兆宽带了
<!-- more -->
## 0x00.前言
因为公网`IP`的紧缺性以及政策的收紧，得知电信家宽在付费升级提速后大概率会丢失公网`IP`并且再也申请不到了
需要找到一个靠谱的回家方法，来实现自己在外能访问家中服务，以及别人访问家中`WZ`的`Minecraft`服务器

## 0x01.[frp](https://github.com/fatedier/frp)
提及无公网`IP`，脑海中第一个闪过的自然是**内网穿透**了，虽然自己在良心云上有`8M`带宽的轻量云主机，也搭了`frp`但还是当成备选方案

<details><summary>点击此处 ← 查看折叠</summary>

![8Mbps](https://i1.yuangezhizao.cn/macOS/20220426224947.png!webp)
![frp](https://i1.yuangezhizao.cn/macOS/20220426225235.png!webp)

</details>

毕竟谁都不想为分散在不同虚拟机上的各个服务挨个映射端口吧……自己觉得`frp`还是更适合于单个服务的内网穿透，比如访问老家的路由器
`emmm`，只可惜过年回家时发现家中的培训`K2`跑个新版`frpc`都`OOM`：[#107613862616668802](https://mastodon.yuangezhizao.cn/web/@yuangezhizao/107613862616668802)

## 0x01.方案
首先是可行性分析，在`v2`上找到了与本文标题思路完全一致的帖子：[由于公网 IP 没了，再次入软路由坑，被迫使用 ipv6](https://www.v2ex.com/t/844222)
![844222](https://i1.yuangezhizao.cn/macOS/20220426223110.png!webp)

当然在评论区还翻到了其他的几种方法：
1. `WireGuard`组网
2. [Tailscale](https://tailscale.com)服务或与其兼容的开源实现[headscale](https://github.com/juanfont/headscale)

## 0x02.[IPv6](https://zh.wikipedia.org/zh/IPv6)
1. 时至今日，三大运营商均已提供`IPv6`地址，电信家宽自然也不例外，通过路由器`PPPoE`拨号就能得到**公网**`IPv6`地址（严格来讲`IPv6`没有公不公网的概念
才疏学浅，除非路由器不支持`IPv6`拨号（此处是伏笔）只能得到路由器自己下发的**局域网**`IPv6`地址……比如`TP-Link`都能：[#108186344984859598](https://mastodon.yuangezhizao.cn/web/@yuangezhizao/108186344984859598)
2. 再看移动数据网络，自己手里的腾讯大王卡开启流量也是可以获取到联通的`IPv6`地址
3. 最后只剩在外蹭`WiFi`的情况了，实测在麦当劳是木有的，这点只能随缘

不过和公网`IP`相同，从运营商获取的`IPv6`地址也是会变的，所以仍然需要一个域名，然后挂上`DDNS`脚本定时更新其`AAAA`解析（这都不是难事儿
毕竟`IPv6`地址不是让人去用脑子记的，更何况自己连`IPv4`地址都记不住，也没必要去记忆这玩楞

## 0x03.[Project V](https://github.com/v2fly/v2ray-core)
> `Project V`：助你打造专属基础通信网络

为了方便使用不碰命令行，在`cn-py-dl-r8`上搭建[x-ui](https://github.com/vaxilu/x-ui)面板，或者使用`v2-ui`面板也行，后者时至今日自己也一直在用
毕竟实际`AAAA`解析指向的`cn-py-dl-r8`而不是`NAS`等其他虚机，就相当于对全网公开，还是得注意一下安全性，这也是用红帽企业操作系统的原因之一（白嫖

![x-ui](https://i1.yuangezhizao.cn/macOS/20220426234333.png!webp)

当然了，现在使用的内核是仍在活跃维护的[Xray-core](https://github.com/XTLS/Xray-core)，属于[Project X Community](https://github.com/XTLS)组织，起源于`Project V`，即此章节标题
> `Project X`：不畏浮云遮望眼 · 金睛如炬耀苍穹

关于区别，下文引用自[Project X](https://xtls.github.io)官网，反正用新协议就好啦
> `XTLS`？`Xray`？`V2Ray`？
> `Xray-core`是`v2ray-core`的超集，含更好的整体性能和`XTLS`等一系列增强，且完全兼容`v2ray-core`的功能及配置。

如果想访问家中服务，那么就得删除`routing`中`rules`里默认配置的`防止服务器本地流转问题：如内网被攻击或滥用、错误的本地回环等`
``` json
{
    "ip": [
        "geoip:private"
    ],
    "outboundTag": "blocked",
    "type": "field"
}
```
备注：这里还用到了`v2ray`实现的`IPv6`转换`IPv4`功能

## 0x04.实测
首先关掉`WiFi`，然后打开流量，最后运行`v2rayNG`，终于成功了：[#108199273350760962](https://mastodon.yuangezhizao.cn/web/@yuangezhizao/108199273350760962)
![kcp-dlv6](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2022-04-24-18-44-36-243_com.android.ch.jpg!webp)
![NAS](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2022-04-24-18-44-32-254_com.android.ch.jpg!webp)

未完待续……