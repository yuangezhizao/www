---
title: 记一次基于 Flutter 的安卓应用 HTTPS 抓包实现
date: 2021-08-27 22:33:57
tags:
  - Flutter
  - HTTPS
  - Frida
count: 2
os: 1
os_1: Monterry 12.0 Beta (21A5304g)
browser: 1
browser_1: 92.0.4515.159 Stable
place: 新家
key: 119
---
    IDA nb，Frida nb！
<!-- more -->
## 0x00.前言
这是第二次在这里提到`Frida`这个`Hook`工具了，但是这次的背景却更加简单，只是为了挂签到脚本而已
本文根据时间顺序从前至后回顾编写，章节无比跳跃，大佬轻（`rao`）喷（`ming`）
> 第一次前情回顾：[Frida 初体验](./init.html)

## 0x01.`Fiddler`抓包
`HomeAssistant`局域网唤醒台式机，远程桌面连进去之后先开启热点让手机连上，然后打开`Fiddler`（海鲜市场以十五折售出，手里现在没有显卡。。。
~~但是这个时候自己并不知道这个应用是基于`Flutter`构建的，自然是有用的`api`啥都没抓到~~

![假装是 Fiddler](https://i1.yuangezhizao.cn/macOS/20210826232700.png!webp)

注：此时安卓的基础抓包环境是没有问题的（狗东和你`b`的客户端请求都能看到）

<details><summary>点击此处 ← 查看折叠</summary>

![Move Cert……](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2021-08-27-23-50-07-403_com.topjohnwu..jpg!webp)
![TrustMeAlready](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2021-08-27-23-50-24-535_org.meowcat.ed.jpg!webp)

</details>

## 0x02.`WireShark`抓包
一气之下打开`WireShark`瞅瞅（请无视客户端为`macOS`版本
![TLSv1.2](https://i1.yuangezhizao.cn/macOS/20210826232801.png!webp)

注：这里`WireShark`解析的结果，是已经配置过`TLS`协议的`(Pre)-Master-Secret`文件

<details><summary>点击此处 ← 查看折叠</summary>

![.ssl-key.log](https://i1.yuangezhizao.cn/macOS/20210827225706.png!webp)

</details>

但是显然`Application Data`仍然是加密的，那么有没有方法把这一层再解开呢？答案是肯定的，毕竟已经是`Mitm`环境了啥证书都能拿到或者伪造（吧）

## 0x03.`Fiddler`抓包再放送
参照[利用Fiddler和Wireshark解密SSL加密流量](https://web.archive.org/web/20210827150219/https://www.cnblogs.com/alonesword/p/4567380.html)，只需对应网站的私钥即可，在`Fiddler`中需要把证书生成器修改为`CertMaker`（注：默认选项是另外一个）
于是只好被迫删掉当前证书，然后切换到`CertMaker`，接下来把证书安装到安卓手机上，此时的自己并不知道一个巨坑已经挖下了
由于`K20Pro`几个月之前从`Android 10`升级到了`11`版本，出于安全性考虑不再能通过直接点击`.crt`文件来安装证书了
![F*ck](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2021-08-27-23-08-57-219_com.android.ce.jpg!webp)

于是只能按照弹框所提示的方法进行操作了，进入到`设置`-`密码与安全`-`系统安全`，点击`高级`下的`加密与凭据`

<details><summary>点击此处 ← 查看折叠</summary>

![加密与凭据](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2021-08-27-23-13-27-354_com.android.se.jpg!webp)

</details>

网上有说法选择第一个`CA`证书并忽视报错，但是总感觉类型其实是第二种

<details><summary>点击此处 ← 查看折叠</summary>

![选择困难症](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2021-08-27-23-13-30-009_com.android.se.jpg!webp)

</details>

安装完成之后总得试一下是否生效，结果突然陷入僵局，因为更新完新的`Fiddler`证书之后狗东和你`b`的客户端请求都看不到，这是自己没想到的
![不太合理](https://i1.yuangezhizao.cn/macOS/QQ20210827-234006@2x.png!webp)

折腾了好多次一气之下狠心删掉全部证书，重启，安装证书，再重启也无果，包括上述的第二种选项也尝试了，可就是抓包不能

<details><summary>点击此处 ← 查看折叠</summary>

![全部木大？](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2021-08-26-18-33-31-422_com.android.se.jpg!webp)
![全部木大了](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2021-08-26-19-10-55-186_com.android.se.jpg!webp)

</details>

并且其实`信任的凭据`中已经能看到新证书位于`系统`中了，而`用户`证书是空的

<details><summary>点击此处 ← 查看折叠</summary>

![系统](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2021-08-27-23-19-14-257_com.android.se.jpg!webp)
![2021-08-25](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2021-08-27-23-19-16-886_com.android.se.jpg!webp)
![用户](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2021-08-27-23-19-20-109_com.android.se.jpg!webp)

</details>

这时候已经接近七点钟天都黑了，还没吃晚饭于是果断停止了思考，不（`chi`）搞（`fan`）了

## 0x04.静态分析
やだよ，`静态分析`相比（轻车熟路的）`分析通信`实在是太痛苦了，でも仕方がないです（从来就没有`动态分析`过.jpG
在`lib`的`arm64-v8a`目录下，看到有`libflutter.so`和`libapp.so`，その通りです，这个应用是基于`Flutter`构建的
![libflutter.so](https://i1.yuangezhizao.cn/macOS/QQ20210828-000757@2x.png!webp)

这就一下子点明了方向，只需要去查找`Flutter`应用的抓包方法即可
![和善的笑容](https://i1.yuangezhizao.cn/macOS/QQ20210828-001319@2x.png!webp)

注 ①：其实最开始是直接扔到了`JEB`里，然后在那里看到是`Flutter`应用，后来才去解压的`apk`（当时显然后者更简单`2333`

<details><summary>点击此处 ← 查看折叠</summary>

![又有新版本了好评](https://i1.yuangezhizao.cn/macOS/20210827000800.png!webp)
![FlutterApplication](https://i1.yuangezhizao.cn/macOS/20210827002100.png!webp)
![开幕雷击，彩蛋草](https://i1.yuangezhizao.cn/macOS/20210827002300.png!webp)

</details>

注 ②：额外吐槽下`Flutter`构建的应用加密是真`nb`，`libapp.so`啥函数都看不着

<details><summary>点击此处 ← 查看折叠</summary>

![？](https://i1.yuangezhizao.cn/macOS/20210827003500.png!webp)

</details>

## 0x05.`Charles`抓包
因为安卓证书炸了，`Fiddler`抓包不能，被迫回到`macOS`生产力平台，打开`Charles`一顿操作猛如虎，光速配置完成

<details><summary>点击此处 ← 查看折叠</summary>

![HTTP PROXY](https://i1.yuangezhizao.cn/macOS/QQ20210827-120744@2x.png!webp)
![SSL PROXY](https://i1.yuangezhizao.cn/macOS/QQ20210827-120733@2x.png!webp)

</details>

并且看到了[Flutter iOS App https抓包](https://web.archive.org/web/20210827162752/https://www.jianshu.com/p/53b53993a7f4)这篇文章，直接暴力替换`TCP`连接的`IP`地址有被震惊到，思路清奇开了个`反向代理`也真是骚操作（`Σ(oﾟдﾟoﾉ)`
这里贴一下修改好的`Frida`注入脚本
> 「Talk is cheap. Show your the code」

<details><summary>点击此处 ← 查看折叠</summary>

``` javascript
/*
*
* @creantan
*
* Example usage:
* # frida -U -f com.mrnew.door -l flutter_connect_.js --no-pause
*
*/

var sIP = '47.91.165.221' // 目标 IP 地址
var xIP = '192.168.2.1' // 代理电脑 IP 地址

// IP 字符串转 int
function ipToInt(ip){
    var  result = ip.split('.');
    return (parseInt(result[3]) << 24 
        | parseInt(result[2]) << 16
        | parseInt(result[1]) << 8
        | parseInt(result[0]));
}

// int 转 IP 字符串
function parseIp (number) {
  var ip = ''
  if (number <= 0) {
    return ip
  }
  const ip3 = (number << 0) >>> 24
  const ip2 = (number << 8) >>> 24
  const ip1 = (number << 16) >>> 24
  const ip0 = (number << 24) >>> 24
  ip += ip0 + '.' + ip1 + '.' + ip2 + '.' + ip3
  return ip
}

function parsePort(number) {
    return ((number & 0xFF) << 8) | ((number & 0xFF00) >> 8);
}

Interceptor.attach(Module.findExportByName(null, "connect"), {
    onEnter: function(args) {
        var fd = args[0].toInt32()
        if (Socket.type(fd) !== 'tcp')
          return;

        var ipAddr = args[1].add(4)
        var ip = parseIp(Memory.readU32(ipAddr))
        var portAddr = args[1].add(2)
        var port = parsePort(Memory.readUShort(portAddr));
        
        // 判断是否为目标地址
        if (ip === sIP) {
            console.log("[+] connect: " +ip+ ':'+ port);

            // 替换 IP 地址为代理主机
            Memory.writeU32(ipAddr,ipToInt(xIP))

            // 打印替换后地址
            console.log(hexdump(ptr(args[1]), {
                length: 32,
                header: true,
                ansi: true
            }))
        }
    }
})
```

</details>

开启反向代理然后`Hook`，生效了吗？并没有（`(╯°□°）╯︵┻━┻`
![Reverse Proxies](https://i1.yuangezhizao.cn/macOS/QQ20210827-120707@2x.png!webp)
![](https://i1.yuangezhizao.cn/macOS/QQ20210827-234402@2x.png!webp)

注 ①：`macOS`开启热点不是在`网络`而是在`共享`设置里草（差点以为`mini`不能开热点……

<details><summary>点击此处 ← 查看折叠</summary>

![互联网共享](https://i1.yuangezhizao.cn/macOS/20210826232800.png!webp)

</details>

注 ②：到现在`Magisk`里的`Frida-Server`仍然是用不了的状态，只能手动切换到`su`用户来运行

<details><summary>点击此处 ← 查看折叠</summary>

![根本就连不上](https://i1.yuangezhizao.cn/macOS/20210827014300.png!webp)
![这样才能连上](https://i1.yuangezhizao.cn/macOS/20210827015000.png!webp)
![确认生效](https://i1.yuangezhizao.cn/macOS/20210827015001.png!webp)

</details>

## 0x05.`Flutter`抓包
言归正传，参照[安卓 flutter app证书绑定校验抓包绕过](https://web.archive.org/web/20210827172655/https://blog.csdn.net/yhsnihao/article/details/110477720)
![内容很长，你忍一忍](https://i1.yuangezhizao.cn/macOS/QQ20210827-234133@2x.png!webp)

`macOS`上也下了`AS`，这样就能`USB`调试了，顺带必需的`ADB`工具就也有了，点开`Logcat`，过滤只看`flutter`，有一个报错出自`handshake.cc:354`
![Logcat](https://i1.yuangezhizao.cn/macOS/20210827104800.png!webp)

因为`Flutter`是开源的，于是去`gh`找一下对应的位置，请无视行号因为版本不一致，但是函数是对的
![handshake.cc](https://i1.yuangezhizao.cn/macOS/20210828011239.png!webp)

根据大佬的文章，更好的`Hook`位置在`ssl_crypto_x509_session_verify_cert_chain()`
![ssl_x509.cc](https://i1.yuangezhizao.cn/macOS/20210828011533.png!webp)

打开`IDA`，把`libflutter.so`拽进去，**稍等片刻等分析得差不多了的时候再开始**
1. 搜索字符串`ssl_server`
![ssl_server](https://i1.yuangezhizao.cn/macOS/20210827022000.png!webp)

2. 双击跳到字符串定义
![IDA View-A](https://i1.yuangezhizao.cn/macOS/20210827022100.png!webp)

3. 反查`交叉引用`，得到偏移量`5873D4`
![好在也只有一个](https://i1.yuangezhizao.cn/macOS/20210827030100.png!webp)
![点错（x）](https://i1.yuangezhizao.cn/macOS/20210827022300.png!webp)

4. 光速`Hook`
![](https://i1.yuangezhizao.cn/macOS/20210827031300.png!webp)

しかし，`Hook`之后应用确实可以正常访问网络了，但是抓包的结果却是空白，此时已是半夜三点多了，无奈只能关电脑睡觉了
![](https://i1.yuangezhizao.cn/macOS/QQ20210827-234320@2x.png!webp)

注：不分析完得到的地址是不正确的草，又多走弯路了

<details><summary>点击此处 ← 查看折叠</summary>

![0x3C925A](https://i1.yuangezhizao.cn/macOS/20210827022900.png!webp)
![0x3C91EC](https://i1.yuangezhizao.cn/macOS/20210827023100.png!webp)
![](https://i1.yuangezhizao.cn/macOS/QQ20210827-234436@2x.png!webp)

</details>

## 0x06.引用
本文表情包出自：[震惊！耗时还能这么优化？？](https://web.archive.org/web/20210825021942/https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzAwNDY1ODY2OQ%253D%253D%26mid%3D2649288229%26idx%3D1%26sn%3Dab95815670a0f2b833dbaadfeedc8b44)
[MacOS 下 Wireshark 抓取 Chrome HTTPS](https://web.archive.org/web/20210904144220/https://segmentfault.com/a/1190000021142289)
[安卓11安装Burp证书](https://web.archive.org/web/20210827161535/https://blog.csdn.net/change518/article/details/118159132)
[移动应用安全基础篇：APP抓包姿势总结](https://www.freebuf.com/articles/web/207041.html)

未完待续……