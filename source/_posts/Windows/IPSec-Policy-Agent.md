---
title: Windows 准实时封禁 RDP 登录失败的 IP 地址
date: 2020-11-14 12:32:28
tags:
  - IPSec Policy Agent
  - Windows  
count: 1
os: 0
os_1: 10.0.17763.1577 2019-LTSC
browser: 0
browser_1: 80.0.3987.163 Stable
place: 新家
key: 103
---
     制裁！
<!-- more -->
## 0x00.前言
翻**事件查看器**看到又有实时（几秒一个）的爆破记录了草……虽然本着安全基准原则已经禁用了`Administrator`账户，所以大概率用户名都碰不上
但是，事情不能就这么早早结束了，早在许多年前就知道`Linux`平台大名鼎鼎的`Fail2ban`，现在也一直在用，并且使用体验极佳
不过，到了`Windows`平台，想找到类似的这种软件可就不是那么轻松的一件事情了，而是根本就找不到

## 0x01.查询
根据`404 Team`安全大佬们的[RDP 登录日志取证与清除](https://web.archive.org/web/20201114044007/https://paper.seebug.org/1043/)文章，可以通过`LogParser`或`wevtutil`写查询语句
奈何自己太菜，顺手就搜到了[Log Parser Lizard](https://lizard-labs.com/log_parser_lizard.aspx)图形化工具，即`Log parser Lizard: read system and application logs with SQL`
并且内置了许多例子，毕竟`SQL`语句都是共通的，于是照葫芦画瓢：
``` SQL
SELECT EXTRACT_TOKEN(Strings, 19, '|') AS SourceIP from Security WHERE EventID = '4625'
```
这样就获取到了全部**登录失败**的`IP`地址，总计`35616`条（全部才`35786`条
![Query](https://i1.yuangezhizao.cn/Win-10/20201114121822.jpg!webp)

至于导出方法，**开发不易，有能力请支持正版！**即使处于`60`天的无料试用期内，`Excel`导出也不可
![Buy](https://i1.yuangezhizao.cn/Win-10/20201114121600.jpg!webp)

不过全选复制就拿到了`(｀・ω・´)`，至此目的达成
> 其实，也可以使用`Kibana`中`security`模块来查询（这其实可以单独拆成一篇文章来讲

## 0x02.封禁
说来话长，从开始搞`Linux`时算起就有听说过各种面板，但是处于天生的排斥性并没有去尝试安装，前几个月苦于纯命令行的管理在某些特殊场景下还是不太方便
于是就去尝鲜了`bt`面板，最终在自己所有的`Linux`机子上全都部署上了，更换默认端口并开了`Basic Auth`认证应该还算安全吧。。。
看到有`Windows`版本的于是也尝鲜了一次，觉着里面的`Windows 工具箱`、`Windows 系统防火墙`功能还算实用就暂且留着用了
说来也不复杂，其实都是`GUI`界面对应的`cmd`调用实现罢了
> 有看过源码是基于`Python`的`Flask`框架实现的，这对于自己再熟悉不过了（也就是说有能力的话可以提取出对应功能的`py`脚本单独使用

![导入](https://i1.yuangezhizao.cn/Win-10/20201114121804.jpg!webp)

因为没有去重，导入花费了巨巨巨巨巨长的时间
![IPSec Policy Agent](https://i1.yuangezhizao.cn/Win-10/20201114125450.jpg!webp)

## 0x03.准实时
挂一个定时任务去查询然后封禁，关于封禁阈值还不知道怎么去写（现在是只要**曾经**登录失败过一次就会被封禁）
再提一句，万一封错了自己直接更换`IP`进入`BT`面板手动解封就好了
未完待续……

## 0x04.修改存储大小
默认日志存储大小`20M`，这里给修改成了`100M`，不怕空间不够`.jpG`
![Application.evtx](https://i1.yuangezhizao.cn/Win-10/20201114114316.jpg!webp)
![Security.evtx](https://i1.yuangezhizao.cn/Win-10/20201114114402.jpg!webp)
![Setup.evtx](https://i1.yuangezhizao.cn/Win-10/20201114114551.jpg!webp)
![System.evtx](https://i1.yuangezhizao.cn/Win-10/20201114114635.jpg!webp)

## 0x05.后记
总算了结了当初非常想实现的一件事情`ヽ(￣▽￣)ﾉ`
