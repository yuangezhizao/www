---
title: 记多次云主机玄学被日跑满外网上传
date: 2020-8-5 19:45:10
tags:
  - PhpStudy
  - php_xmlrpc.dll
count: 2
os: 0
os_1: 10.0.17763.1369 2019-LTSC
browser: 0
browser_1: 80.0.3987.163 Stable
place: 新家
key: 94
---
    一直以为用的是没后门版本真是日了狗了，草
<!-- more -->
## 0x00.前言
`2020-10-31 11:41:38`：奇怪的是后来重装了`Windows Server 2019`但是进程`4`没过几天又被注入了，因为并没有安多余的软件，到底是谁的后门？？？

> [PhpStudy 后门分析](https://paper.seebug.org/1044/)

从昨天下午开始收到第一条短信开始，直到今早仍然处于告警状态，觉得莫名其妙，于是就立即排查去了
![云监控之告警策略](https://i1.yuangezhizao.cn/Win-10/20200805201059.jpg!webp)
![云服务器之监控](https://i1.yuangezhizao.cn/Win-10/20200805200722.jpg!webp)

## 0x01.排查
> [带宽占用高导致无法登录](https://cloud.tencent.com/document/product/213/10334)

毕竟是云主机，任务管理器“性能”中虽然能看到“以太网”，反映的是上行`1M`跑满，但不同于自己的台式机，“进程”中对应的每一条详情并没有提供“以太网”的筛选方式
![进程](https://i1.yuangezhizao.cn/Win-10/20200805201350.jpg!webp)

这就犯难了，于是在任务管理器中“打开资源监视器”，并展开“网络”选项卡，终于可以看到排序的进程了
![网络](https://i1.yuangezhizao.cn/Win-10/954078278_1596597819332_5676.png!webp)
![4](https://i1.yuangezhizao.cn/Win-10/954078278_1596598011677_7628.png!webp)

没错，就是这个`PID`为`4`名称为`System`的进程，与非常多的`IP`地址进行了连接，奇怪的是只有发送没有接收，随手查了几个排在前面的地域，都是“香港”草，越来越觉得得有端倪……
其实之前也有几次类似于这种的外网带宽被跑满的情况，但是并没有详细去调查（~~其实是不会~~，过几天好了就不了了之了
毕竟实验室站根本没多少人访问不可能有持续占满的情况存在，略有访问量的博客站是托管在腾讯云对象存储上并用`CDN`进行分发的，也并没有放在云主机上（

> [Windows 实例：CPU 或内存占用率高导致无法登录](https://cloud.tencent.com/document/product/213/10233)

从帮助文档中可以看到如下描述（不得不说你云的文档是越来越详细了，写的还比较有水平至少不是
> 常见的系统进程如下：
`System Idle Process`：系统空间进程，显示`CPU`空闲时间百分比
`system`：内存管理进程
`explorer`：桌面和文件管理
`iexplore`：微软的浏览器
`csrss`：微软客户端/服务端运行时子系统
`svchost`：系统进程，用于执行`DLL`
`Taskmgr`：任务管理器
`Isass`：本地安全权限服务

之后定位到了具体的文件位置，确实在`C:\Windows\System32`路径下
![ntoskrnl.exe](https://i1.yuangezhizao.cn/Win-10/20200805210203.jpg!webp)

并且带有微软的数字签名，`emmm……`
![版权](https://i1.yuangezhizao.cn/Win-10/20200805210239.jpg!webp)

另外再提一个“事件查看器”中的现象，`安全`选项卡中每几秒钟就会记录一次登录失败的日志
![事件查看器](https://i1.yuangezhizao.cn/Win-10/20200805210539.jpg!webp)

前一阵子还曾以为跑满带宽是因为`3389`被集中爆破导致的，因为自己在安全组中临时禁用`3389`仿佛就好了，现在看来其实并不是这样

## 0x02.工单
想了下还是决定发工单寻求帮助
![入侵警告](https://i1.yuangezhizao.cn/Win-10/20200805210746.jpg!webp)

火绒`nb`！中午吃完饭回到工位上立即进行了全盘杀毒，然后就去睡觉了……醒来一看，`woc`
![握草](https://i1.yuangezhizao.cn/Win-10/20200804210838.jpg!webp)

真·扫出来`6`个病毒，一眼就看到了`PHPStudy`后门草（
![6](https://i1.yuangezhizao.cn/Win-10/20200805211859.jpg!webp)

**当初自己绝对是在官网下载的（确信**，因此至于这个后门的来头并不知情
![草](https://i1.yuangezhizao.cn/Win-10/20191016005155.jpg!webp)

不信拿记事本打开去搜了下`eval`，还真`tm`有
![eval](https://i1.yuangezhizao.cn/Win-10/20200805211927.jpg!webp)

## 0x03.杀毒
点了下“立即处理”就完事了，然后发现还是在跑满带宽，只好立即重启云主机，再次重启之后终于好了

## 0x04.修复
等到了晚上下班回到家再次重启云主机之后发现`MongoDB`炸了，又得去修数据库，毕竟`collection-13--3881483226843500597.wt`这个接近`40MB`的文件被识别为含病毒文件而被干掉了
于是就去“隔离区”给恢复了回来，重启`MongoDB`服务无果，日（
`--repair`修复到一半才发现不仅`ping`不通，所有的端口服务都无法正常访问，才发现是安全狗端口的“严格模式”的锅，关了就好了，结果关了之后又跑满带宽了，草？一脸黑人问号……

## 0x05.后记
又去仔细看了眼工单里推荐的安全措施：
①端口一直懒得改，看到`安全狗`（遇到`3389`爆破于上周装的，结果狗并不好用）内置此功能，于是换掉了`3389`
②然后就去配置安全组（实时生效的云防火墙，真香！）了，**入站规则**白名单手动指定用到的全部服务，其余全部走默认规则“拒绝”掉就好了

这里比较奇怪的一点是，限制入站白名单其余默认拒绝的瞬间，外网带宽就不再跑满了……
