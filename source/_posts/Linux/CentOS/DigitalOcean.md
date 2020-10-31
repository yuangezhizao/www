---
title: DigitalOcean 搭建 Kubernetes
date: 2020-8-16 10:01:54
tags:
  - DigitalOcean
  - Kubernetes
count: 2
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
![Kubernetes in minutes](https://i1.yuangezhizao.cn/Win-10/20200816112833.jpg!webp)
![Create a cluster](https://i1.yuangezhizao.cn/Win-10/20200816113340.jpg!webp)
![30 刀月付](https://i1.yuangezhizao.cn/Win-10/20200816113619.jpg!webp)
![1](https://i1.yuangezhizao.cn/Win-10/20200816113757.jpg!webp)
![2](https://i1.yuangezhizao.cn/Win-10/20200816113926.jpg!webp)

[install-kubectl](https://kubernetes.io/zh/docs/tasks/tools/install-kubectl/)
``` bash
[root@py ~]# cat <<EOF > /etc/yum.repos.d/kubernetes.repo
> [kubernetes]
> name=Kubernetes
> baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
> enabled=1
> gpgcheck=1
> repo_gpgcheck=1
> gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
> EOF
[root@py ~]# yum install -y kubectl
Loaded plugins: fastestmirror
Determining fastest mirrors
epel/x86_64/metalink                                                            | 3.2 kB  00:00:00     
 * base: mirrors.neusoft.edu.cn
 * centos-sclo-rh: mirrors.neusoft.edu.cn
 * centos-sclo-sclo: mirrors.neusoft.edu.cn
 * epel: my.mirrors.thegigabit.com
 * extras: mirrors.neusoft.edu.cn
 * updates: mirrors.neusoft.edu.cn
base                                                                            | 3.6 kB  00:00:00     
centos-sclo-rh                                                                  | 3.0 kB  00:00:00     
centos-sclo-sclo                                                                | 3.0 kB  00:00:00     
docker-ce-stable                                                                | 3.5 kB  00:00:00     
epel                                                                            | 4.7 kB  00:00:00     
extras                                                                          | 2.9 kB  00:00:00     
https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64/repodata/repomd.xml: [Errno 12] Timeout on https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64/repodata/repomd.xml: (28, 'Connection timed out after 30000 milliseconds')
Trying other mirror.
https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64/repodata/repomd.xml: [Errno 12] Timeout on https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64/repodata/repomd.xml: (28, 'Connection timed out after 30000 milliseconds')
Trying other mirror.
https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64/repodata/repomd.xml: [Errno 12] Timeout on https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64/repodata/repomd.xml: (28, 'Connection timed out after 30000 milliseconds')
Trying other mirror.
https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64/repodata/repomd.xml: [Errno 14] curl#35 - "TCP connection reset by peer"
Trying other mirror.


 One of the configured repositories failed (Kubernetes),
 and yum doesn't have enough cached data to continue. At this point the only
 safe thing yum can do is fail. There are a few ways to work "fix" this:

     1. Contact the upstream for the repository and get them to fix the problem.

     2. Reconfigure the baseurl/etc. for the repository, to point to a working
        upstream. This is most often useful if you are using a newer
        distribution release than is supported by the repository (and the
        packages for the previous distribution release still work).

     3. Run the command with the repository temporarily disabled
            yum --disablerepo=kubernetes ...

     4. Disable the repository permanently, so yum won't use it by default. Yum
        will then just ignore the repository until you permanently enable it
        again or use --enablerepo for temporary usage:

            yum-config-manager --disable kubernetes
        or
            subscription-manager repos --disable=kubernetes

     5. Configure the failing repository to be skipped, if it is unavailable.
        Note that yum will try to contact the repo. when it runs most commands,
        so will have to try and fail each time (and thus. yum will be be much
        slower). If it is a very temporary problem though, this is often a nice
        compromise:

            yum-config-manager --save --setopt=kubernetes.skip_if_unavailable=true

failure: repodata/repomd.xml from kubernetes: [Errno 256] No more mirrors to try.
https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64/repodata/repomd.xml: [Errno 12] Timeout on https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64/repodata/repomd.xml: (28, 'Connection timed out after 30000 milliseconds')
https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64/repodata/repomd.xml: [Errno 12] Timeout on https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64/repodata/repomd.xml: (28, 'Connection timed out after 30000 milliseconds')
https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64/repodata/repomd.xml: [Errno 12] Timeout on https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64/repodata/repomd.xml: (28, 'Connection timed out after 30000 milliseconds')
https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64/repodata/repomd.xml: [Errno 14] curl#35 - "TCP connection reset by peer"
[root@py ~]# export http_proxy="http://cn-py-dl-w9d:1081"
```
只好手动安装，`v1.18.8`
![v1.18.8](https://i1.yuangezhizao.cn/Win-10/20200816115809.jpg!webp)

``` bash
wget https://dl.k8s.io/v1.18.8/kubernetes-client-linux-amd64.tar.gz
tar -zxvf kubernetes-client-linux-amd64.tar.gz
cd kubernetes/client/bin
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
```
草，需要相同版本，即`1.18.6`
``` bash
[root@py ~]# chmod +x ./kubectl
[root@py ~]# mv ./kubectl /usr/local/bin/kubectl
```
下载`doctl`
``` bash
[root@py ~]# tar -zxvf doctl-1.46.0-linux-amd64.tar.gz 
[root@py ~]# mv ./doctl /usr/local/bin/doctl
```
![3](https://i1.yuangezhizao.cn/Win-10/20200816121931.jpg!webp)

[生成 token](https://github.com/digitalocean/doctl#authenticating-with-digitalocean)
``` bash
[root@py ~]# doctl auth init
Please authenticate doctl for use with your DigitalOcean account. You can generate a token in the control panel at https://cloud.digitalocean.com/account/api/tokens

Enter your access token: 
Validating token... OK
```
[连接](https://www.digitalocean.com/docs/kubernetes/how-to/connect-to-cluster/)
``` bash
[root@py ~]# doctl kubernetes cluster kubeconfig save kubernetes
Notice: Adding cluster credentials to kubeconfig file found in "/root/.kube/config"
Notice: Setting current-context to do-sgp1-kubernetes
[root@py ~]# kubectl config current-context
do-sgp1-kubernetes
[root@py ~]# kubectl config get-contexts
CURRENT   NAME                 CLUSTER              AUTHINFO                   NAMESPACE
*         do-sgp1-kubernetes   do-sgp1-kubernetes   do-sgp1-kubernetes-admin  
```
![4](https://i1.yuangezhizao.cn/Win-10/20200816122624.jpg!webp)
![5](https://i1.yuangezhizao.cn/Win-10/20200816122640.jpg!webp)

## 0x08.后记
用起来还是不错的，~~不过怎么一直没有扣费？？？~~隔日扣（白）费（嫖）

未完待续……