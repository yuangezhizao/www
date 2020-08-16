---
title: DigitalOcean 搭建 Kubernetes
date: 2020-8-16 10:01:54
tags:
  - DigitalOcean
  - Kubernetes
count: 1
os: 0
os_1: 10.0.17763.1397 2019-LTSC
browser: 0
browser_1: 80.0.3987.163 Stable
place: 新家
key: 97
---
    100 刀只有 58 天的使用期太草了
<!-- more -->
## 0x00.前言
尝试`bypass abema`失败就莫名想起来了这个，结果还以为是有日本节点的……

## 0x01.注册
![100](https://i1.yuangezhizao.cn/Win-10/20200816100401.jpg!webp)
![绑卡](https://i1.yuangezhizao.cn/Win-10/20200815233717.jpg!webp)
![100](https://i1.yuangezhizao.cn/Win-10/20200816001121.jpg!webp)

竟然早在`2016`年就注册了，只不过一直没验证支付方式
![2016](https://i1.yuangezhizao.cn/Win-10/20200816001342.png!webp)

## 0x02.创建
![Droplets](https://i1.yuangezhizao.cn/Win-10/20200816100701.jpg!webp)

然后傻眼了，发现没有`日本`节点……于是随便选了个`新加坡`节点（
![Singapore](https://i1.yuangezhizao.cn/Win-10/20200816100802.jpg!webp)
![Create](https://i1.yuangezhizao.cn/Win-10/20200816100850.jpg!webp)
![graphs](https://i1.yuangezhizao.cn/Win-10/20200816101155.png!webp)
![Billing](https://i1.yuangezhizao.cn/Win-10/20200816103441.jpg!webp)

## 0x3.路由追踪
`北京`→`日本`→`新加坡`
![Best Trace](https://i1.yuangezhizao.cn/Win-10/20200816102634.png!webp)

## 0x04.云主机版本
``` bash
[root@do ~]# rpm -q centos-release
centos-release-8.2-2.2004.0.1.el8.x86_64
```

## 0x05.安装
``` bash
Connecting to <rm>:22...
Connection established.
To escape to local shell, press 'Ctrl+Alt+]'.

Activate the web console with: systemctl enable --now cockpit.socket

[root@do ~]# systemctl enable --now cockpit.socket
Created symlink /etc/systemd/system/sockets.target.wants/cockpit.socket → /usr/lib/systemd/system/cockpit.socket.
```

<details><summary>点击此处 ← 查看折叠</summary>

``` bash
[root@do ~]# bash <(curl -Ls https://blog.sprov.xyz/v2-ui.sh)
v2-ui 正在开发支持最新版 v2ray，暂无法更新与安装，如有需要，请使用测试版（仅临时测试，此脚本会尽快恢复）
测试版安装命令：
bash <(curl -Ls https://raw.githubusercontent.com/sprov065/v2-ui/master/install_new.sh) 5.3.0
[root@do ~]# bash <(curl -Ls https://raw.githubusercontent.com/sprov065/v2-ui/master/install_new.sh) 5.3.0

……

Created symlink /etc/systemd/system/multi-user.target.wants/v2-ui.service → /etc/systemd/system/v2-ui.service.
v2-ui v5.3.0 安装完成，面板已启动，

如果是全新安装，默认网页端口为 65432，用户名和密码默认都是 admin
请自行确保此端口没有被其他程序占用，并且确保 65432 端口已放行
若想将 65432 修改为其它端口，输入 v2-ui 命令进行修改，同样也要确保你修改的端口也是放行的

如果是更新面板，则按你之前的方式访问面板

v2-ui 管理脚本使用方法: 
----------------------------------------------
v2-ui              - 显示管理菜单 (功能更多)
v2-ui start        - 启动 v2-ui 面板
v2-ui stop         - 停止 v2-ui 面板
v2-ui restart      - 重启 v2-ui 面板
v2-ui status       - 查看 v2-ui 状态
v2-ui enable       - 设置 v2-ui 开机自启
v2-ui disable      - 取消 v2-ui 开机自启
v2-ui log          - 查看 v2-ui 日志
v2-ui update       - 更新 v2-ui 面板
v2-ui install      - 安装 v2-ui 面板
v2-ui uninstall    - 卸载 v2-ui 面板
----------------------------------------------
[root@do ~]# v2-ui

  v2-ui 面板管理脚本
--- https://blog.sprov.xyz/v2-ui ---
  0. 退出脚本
————————————————
  1. 安装 v2-ui
  2. 更新 v2-ui
  3. 卸载 v2-ui
————————————————
  4. 重置用户名密码
  5. 重置面板设置
  6. 设置面板端口
————————————————
  7. 启动 v2-ui
  8. 停止 v2-ui
  9. 重启 v2-ui
 10. 查看 v2-ui 状态
 11. 查看 v2-ui 日志
————————————————
 12. 设置 v2-ui 开机自启
 13. 取消 v2-ui 开机自启
————————————————
 14. 一键安装 bbr (最新内核)
 15. 更新 v2ray
 
面板状态: 已运行
是否开机自启: 是

请输入选择 [0-14]: 14
---------- System Information ----------
 OS      : CentOS 8.2.2004
 Arch    : x86_64 (64 Bit)
 Kernel  : 4.18.0-193.6.3.el8_2.x86_64
----------------------------------------
 Auto install latest kernel for TCP BBR

 URL: https://teddysun.com/489.html
----------------------------------------

Press any key to start...or Press Ctrl+C to cancel

Info: Your kernel version is greater than 4.9, directly setting TCP BBR...
Info: Setting TCP BBR completed...

安装 bbr 成功

按回车返回主菜单:
```

</details>

安装`htop`需要自行添加`EPEL`源

``` bash
[root@do ~]# yum install htop
DigitalOcean Agent                                                      85 kB/s | 3.3 kB     00:00    
No match for argument: htop
Error: Unable to find a match: htop
[root@do ~]# yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
Last metadata expiration check: 0:00:33 ago on Sun 16 Aug 2020 02:29:32 AM UTC.
epel-release-latest-8.noarch.rpm                                        14 kB/s |  22 kB     00:01    
Dependencies resolved.
=======================================================================================================
 Package                   Architecture        Version                 Repository                 Size
=======================================================================================================
Installing:
 epel-release              noarch              8-8.el8                 @commandline               22 k

Transaction Summary
=======================================================================================================
Install  1 Package

Total size: 22 k
Installed size: 32 k
Is this ok [y/N]: y
Is this ok [y/N]: y
Downloading Packages:
Running transaction check
Transaction check succeeded.
Running transaction test
Transaction test succeeded.
Running transaction
  Preparing        :                                                                               1/1 
  Installing       : epel-release-8-8.el8.noarch                                                   1/1 
  Running scriptlet: epel-release-8-8.el8.noarch                                                   1/1 
  Verifying        : epel-release-8-8.el8.noarch                                                   1/1 

Installed:
  epel-release-8-8.el8.noarch                                                                          

Complete!
[root@do ~]# 
```

## 0x06.测速
![1080 无压力](https://i1.yuangezhizao.cn/Win-10/20200816104650.jpg!webp)
![4K60 略卡](https://i1.yuangezhizao.cn/Win-10/20200816105135.jpg!webp)

## 0x07.Kubernetes
后续补充（

## 0x08.后记
用起来还是不错的，不过怎么一直没有扣费？？？

未完待续……