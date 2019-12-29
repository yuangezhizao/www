---
title: ESXi 安装 macOS Mojave
date: 2019-12-24 20:11:21
tags:
  - VM
  - VMware
  - ESXi
  - macOS
count: 1
os: 0
os_1: 10.0.17763.914 2019-LTSC
browser: 0
browser_1: 74.0.3729.169 Stable
place: 新家
key: 63
---
    黑苹果？启动！
<!-- more -->
## 0x00.前言
由于新台式硬盘已经分配好了，所以不想再进行切割操作……况且年底也不想再去买硬盘，所以就尝试在`ESXi`上安装`macOS`试试看好了……
前一阵子的某个周末折腾了下，照着`Google`来的教程就开始搞，只不过自己手头并没有实体`macOS`系统的机子（笔记本黑苹果已带回家
所以只能去官网`iTunes`？下载`dmg`镜像，然后现下了个`Ultra ISO`用来把`dmg`格式转化为`iso`格式，启动！
结果启动不能过草，直接就进`BIOS`让我去选启动项？？？然后又翻到了有人对比过的和能正常启动的`ISO`镜像的内容差异的帖子
![草](https://i1.yuangezhizao.cn/Win-10/20191215031908.jpg!webp)
![草 * 2](https://i1.yuangezhizao.cn/Win-10/20191215031922.jpg!webp)

发现目录结构完全不一样`hhh`……看了下本人的`ISO`貌似`Ultra ISO`给转换成一个整体包了，过草……
到最后也没能找到除了在实体`macOS`系统的机子上转换格式的方法……

## 0x01.创建
![典型](https://i1.yuangezhizao.cn/Win-10/20191215030804.jpg!webp)
![VMs](https://i1.yuangezhizao.cn/Win-10/20191215030826.jpg!webp)
![苹果系统！](https://i1.yuangezhizao.cn/Win-10/20191215030849.jpg!webp)

注：`unlocker`补丁（使非`ESXi`支持非`Apple`硬件等）记得最开始打上（之后重启`ESXi`
![sudo sh](https://i1.yuangezhizao.cn/Win-10/20191215030222.jpg!webp)
![命名](https://i1.yuangezhizao.cn/Win-10/20191215030916.jpg!webp)
![150 GB](https://i1.yuangezhizao.cn/Win-10/20191215031120.jpg!webp)
![完成](https://i1.yuangezhizao.cn/Win-10/20191215031825.jpg!webp)

## 0x02.开机
今天社畜回家突然想起这个，吃完饭直接去搜了个支持`EXSI`的`macOS 10.14`谷歌网盘镜像
`macOS Mojave 10.14 by SYSNETTECH Solutions Full Version.iso`，下好之后`web`传到`EXSI`上
更换下虚拟机挂载的`ISO`，开机！
看到`Apple`的图标之后，`我真是兴奋到不行.jpG`
![妙](https://i1.yuangezhizao.cn/Win-10/20191224195302.jpg!webp)
![语言](https://i1.yuangezhizao.cn/Win-10/20191224194248.jpg!webp)
![磁盘工具](https://i1.yuangezhizao.cn/Win-10/20191224194454.jpg!webp)
![虚拟磁盘](https://i1.yuangezhizao.cn/Win-10/20191224194330.jpg!webp)
![没选 APFS](https://i1.yuangezhizao.cn/Win-10/20191224194346.jpg!webp)
![抹掉](https://i1.yuangezhizao.cn/Win-10/20191224194441.jpg!webp)
![Mac OS 拓展（日志式）](https://i1.yuangezhizao.cn/Win-10/20191224195441.jpg!webp)
![嗯？](https://i1.yuangezhizao.cn/Win-10/20191224194512.jpg!webp)

出现这个错误之后立即去搜索，想到是时间的问题，`date`更改时间重启无解，继续尝试发现还需要断网
`ESXi`倒是很好操作，右键网络图标选择`断开连接`再开机，之后再修改时间
![断网大法](https://i1.yuangezhizao.cn/Win-10/20191224195505.jpg!webp)
![修改时间](https://i1.yuangezhizao.cn/Win-10/20191224195650.jpg!webp)
![退出终端](https://i1.yuangezhizao.cn/Win-10/20191224194749.jpg!webp)
![安装 macOS](https://i1.yuangezhizao.cn/Win-10/20191224194300.jpg!webp)
![继续](https://i1.yuangezhizao.cn/Win-10/20191224195712.jpg!webp)
![同意](https://i1.yuangezhizao.cn/Win-10/20191224195738.jpg!webp)
![macOS](https://i1.yuangezhizao.cn/Win-10/20191224195748.jpg!webp)
![神 tm 5 min](https://i1.yuangezhizao.cn/Win-10/20191224195809.jpg!webp)

看到日志也确信了它会联网更新时间，过草
![时间更新不能](https://i1.yuangezhizao.cn/Win-10/20191224201439.jpg!webp)

然后就是漫长的等待了
![TWO THOUSANDS YEARS LATER](https://i1.yuangezhizao.cn/Win-10/20191224205755.jpg!webp)

其实进安装之后本人就给恢复网络连接了，然后`tm`貌似卡住了？
![看日志发现果然在下载更新](https://i1.yuangezhizao.cn/Win-10/20191224202130.jpg!webp)
![终于熬出头了](https://i1.yuangezhizao.cn/Win-10/20191224205641.jpg)

## 0x03.配置
突然巨大的一阵杂音，吓死我了（即使开着`QQ 音乐`
![鼠标滚轮没反向好评](https://i1.yuangezhizao.cn/Win-10/20191224211517.jpg)
![简体拼音](https://i1.yuangezhizao.cn/Win-10/20191224211632.jpg)
![pass](https://i1.yuangezhizao.cn/Win-10/20191224211703.jpg)

草，又被吓了一跳
![立即静音](https://i1.yuangezhizao.cn/Win-10/20191224211805.jpg)
![不传输](https://i1.yuangezhizao.cn/Win-10/20191224211935.jpg)
![登录](https://i1.yuangezhizao.cn/Win-10/20191224212018.jpg)
![二次验证好评](https://i1.yuangezhizao.cn/Win-10/20191224212136.jpg)

竟然卡在这里一直转圈圈……
![那就先跳过好了](https://i1.yuangezhizao.cn/Win-10/20191224213040.jpg)
![同意](https://i1.yuangezhizao.cn/Win-10/20191224213127.jpg)
![创建账户](https://i1.yuangezhizao.cn/Win-10/20191224213409.jpg)
![定位](https://i1.yuangezhizao.cn/Win-10/20191224213514.jpg)
![但是，我拒绝](https://i1.yuangezhizao.cn/Win-10/20191224213544.jpg)
![外观设置卡了下没截到，选的白色（毕竟虚拟机](https://i1.yuangezhizao.cn/Win-10/20191224213701.jpg)

## 0x04.运行
![3 MB 显存，爆炸啊](https://i1.yuangezhizao.cn/Win-10/20191224214137.jpg)
![安装不能](https://i1.yuangezhizao.cn/Win-10/20191224225344.jpg)
![然后只能去下了个 darwin10_1.iso 手动安装](https://i1.yuangezhizao.cn/Win-10/20191224215147.jpg)
![草](https://i1.yuangezhizao.cn/Win-10/20191224215402.jpg)
![只敢更 10.14](https://i1.yuangezhizao.cn/Win-10/20191224221201.jpg)
![再更](https://i1.yuangezhizao.cn/Win-10/20191224225429.jpg)
![允许](https://i1.yuangezhizao.cn/Win-10/20191224215432.jpg)
![重启见奇迹](https://i1.yuangezhizao.cn/Win-10/20191224215615.jpg)
![128 MB 显存！](https://i1.yuangezhizao.cn/Win-10/20191224220032.jpg)
![高分辨率全屏实在是太奇怪了](https://i1.yuangezhizao.cn/Win-10/20191224220245.png)
![2h 警告](https://i1.yuangezhizao.cn/Win-10/20191224221228.jpg)

`2019-12-25 22:40:34`：
`10.15`还是不可使用，因此只能`10.14`……
![打完快照尝试 10.15](https://i1.yuangezhizao.cn/Win-10/20191225215552.jpg)
![屏幕分辨率受限点不到继续](https://i1.yuangezhizao.cn/Win-10/20191225220128.jpg)
![去 tm HIDPI](https://i1.yuangezhizao.cn/Win-10/20191225221031.jpg)
![继续](https://i1.yuangezhizao.cn/Win-10/20191225221444.jpg)
![同意](https://i1.yuangezhizao.cn/Win-10/20191225221550.jpg)
![安装](https://i1.yuangezhizao.cn/Win-10/20191225221621.jpg)
![继续](https://i1.yuangezhizao.cn/Win-10/20191225222246.jpg)
![突然完成](https://i1.yuangezhizao.cn/Win-10/20191225222513.jpg)
![果然已炸](https://i1.yuangezhizao.cn/Win-10/20191225223700.jpg)
![日志](https://i1.yuangezhizao.cn/Win-10/20191225223743.jpg)
![转到](https://i1.yuangezhizao.cn/Win-10/20191225223857.jpg)

## 0x05.引用
> [求助，安装VM苹果，全屏分辨率自动变HiDPI](https://web.archive.org/web/20191225141257/http://tieba.baidu.com/p/5460378749?red_tag=c0777425807)

未完待续……
