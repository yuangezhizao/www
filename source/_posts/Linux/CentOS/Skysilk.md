---
title: 重装系统之 Skysilk CentOS 7 安装 v2ray 代理等
date: 2019-5-12 20:53:55
tags:
  - CentOS
  - server
count: 1
os: 0
os_1: 10.0.17763.437 2019-LTSC
browser: 0
browser_1: 72.0.3626.121 Stable
place: 家
key: 51
---
    用了四个月的说，这几天 v2 突然挂了……
<!-- more -->

## 0x00.前言
一直以为被墙了，今晚才反应过来很奇怪啊，能`ping`，但是`nginx`外网页面看不了（还不是`80`端口），`ssh`连不上……直到我打开了`Graphs`，woc
![CPU爆了](https://i1.yuangezhizao.cn/Win-10/20190512205532.jpg!webp)

重启之后终于登录进去了，提示距离上次成功登录有十万次错误，绝了，`htop`也没看出来是哪个进程，并不是弱密码，奇怪的是那上面自带的`fail2ban`进程在但是貌似没生效，我也没去看相关日志，只是把`/var/log/nginx`和`/var/log/v2ray`这俩文件夹下下来了，等后期再分析……然后就直接重装新系统并传了密钥

## 0x01.`ssh`关闭密码登录
新系统刚进去就看到了两次失败登录尝试，于是直接关了密码登录`/etc/ssh/sshd_config`：`PasswordAuthentication no`，`systemctl restart sshd.service`，注销之后果然密码登录不行，密钥`ok`
![我关了](https://i1.yuangezhizao.cn/Win-10/20190512214356.jpg!webp)

## 0x02.[V2ray.Fun](https://github.com/FunctionClub/V2ray.Fun)
一键安装脚本有的是，特意看了内容有的真的会保存你的信息……安装原版的又不顺手，最终选了这个，带图形化管理界面不错`hhh`，是用`Flask`写的。
![修改连接](https://i1.yuangezhizao.cn/Win-10/20190512214632.png!webp)

还能直接看运行日志，也是十分爽到了
![运行日志](https://i1.yuangezhizao.cn/Win-10/20190512214900.png!webp)

## 0x03.服务器版本
``` bash
[root@CentOS ~]# cat /etc/redhat-release
CentOS Linux release 7.3.1611 (Core)
```
## 0x04.修改时区
``` bash
[root@CentOS ~]# timedatectl status
      Local time: Sun 2019-05-12 13:51:57 UTC
  Universal time: Sun 2019-05-12 13:51:57 UTC
        RTC time: n/a
       Time zone: UTC (UTC, +0000)
     NTP enabled: n/a
NTP synchronized: yes
 RTC in local TZ: no
      DST active: n/a
[root@CentOS ~]# timedatectl set-timezone Asia/Shanghai
[root@CentOS ~]# timedatectl status
      Local time: Sun 2019-05-12 21:52:18 CST
  Universal time: Sun 2019-05-12 13:52:18 UTC
        RTC time: n/a
       Time zone: Asia/Shanghai (CST, +0800)
     NTP enabled: n/a
NTP synchronized: yes
 RTC in local TZ: no
      DST active: n/a
```

## 0x05.常用工具
`yum install vim htop axel -y`

## 0x05.后记
本来还想着放到路由器上，后来想想还是算了吧，毕竟性能（其实`K2`还可以的）
