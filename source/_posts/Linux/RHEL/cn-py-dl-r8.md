---
title: PY 云新增 cn-py-dl-r8 虚拟机
date: 2022-04-02 22:00:56
tags:
  - RHEL
count: 1
os: 1
os_1: Monterry 12.3.1 (21E258)
browser: 0
browser_1: 100.0.4896.60 Stable
place: 新家
key: 137
---
    三月已经过去，四月会变好吗？
<!-- more -->
## 0x00.前言
红帽企业级`Linux`的操作体验实在是`tql`

## 0x01.`SELINUX`切换至`Permissive`模式
只能说对于家用`LAB`环境为了根本用不上的过分安全，去折腾这玩楞是大可不必的，又不是生产环境为啥要难为自己呢？节省掉的时间多补几部番它不香吗？
参照官方文档：[更改 SELINUX 状态和模式](https://access.redhat.com/documentation/zh-cn/red_hat_enterprise_linux/8/html/using_selinux/changing-selinux-states-and-modes_using-selinux)
``` bash
[root@cn-py-dl-r8 ~]# getenforce
Enforcing
[root@cn-py-dl-r8 ~]# sestatus
SELinux status:                 enabled
SELinuxfs mount:                /sys/fs/selinux
SELinux root directory:         /etc/selinux
Loaded policy name:             targeted
Current mode:                   enforcing
Mode from config file:          enforcing
Policy MLS status:              enabled
Policy deny_unknown status:     allowed
Memory protection checking:     actual (secure)
Max kernel policy version:      33
```
本来是准备直接关了了事，结果发现文档中说
> 在`/etc/selinux/config`中使用`SELINUX=disabled`选项禁用`SELinux`的结果是，内核在引导时首先启用`SELinux`，并在后续的引导过程后切换到禁用模式。因为内存泄漏和竞争条件会导致内核`panics`，如果您的情况确实需要完全禁用`SELinux`，则首选的方法是，在内核命令行中添加 `selinux=0`参数（如引导时更改`SELinux`模式）所述

好吧，那就先切换到`Permissive`模式吧
``` bash
[root@cn-py-dl-r8 ~]# cat /etc/selinux/config
# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#     enforcing - SELinux security policy is enforced.
#     permissive - SELinux prints warnings instead of enforcing.
#     disabled - No SELinux policy is loaded.
SELINUX=permissive
# SELINUXTYPE= can take one of these three values:
#     targeted - Targeted processes are protected,
#     minimum - Modification of targeted policy. Only selected processes are protected. 
#     mls - Multi Level Security protection.
SELINUXTYPE=targeted
[root@cn-py-dl-r8 ~]# reboot
```

## 0x02.安装[Uptime Kuma](https://github.com/louislam/uptime-kuma)
开幕就被智能提示惊艳到了，上一次类似的体验还是[thefuck](https://github.com/nvbn/thefuck)
``` bash
Activate the web console with: systemctl enable --now cockpit.socket

Last login: Sun Mar 27 17:54:05 2022 from 192.168.25.123
[root@cn-py-dl-r8 ~]# git clone https://github.com/louislam/uptime-kuma.git
bash: git: command not found...
Install package 'git-core' to provide command 'git'? [N/y] y


 * Waiting in queue... 
 * Loading list of packages.... 
The following packages have to be installed:
 git-core-2.27.0-1.el8.x86_64   Core package of git with minimal functionality
Proceed with changes? [N/y] y


 * Waiting in queue... 
 * Waiting for authentication... 
 * Waiting in queue... 
 * Downloading packages... 
 * Requesting data... 
 * Testing changes... 
 * Installing packages... 
Cloning into 'uptime-kuma'...
```
拉取镜像时发现可以选择多种源，但是显然只有`docker`的源是可用的
```
[root@cn-py-dl-r8 ~]# docker pull louislam/uptime-kuma
Emulate Docker CLI using podman. Create /etc/containers/nodocker to quiet msg.
? Please select an image: 
  ▸ registry.fedoraproject.org/louislam/uptime-kuma:1
    registry.access.redhat.com/louislam/uptime-kuma:1
    registry.centos.org/louislam/uptime-kuma:1
    docker.io/louislam/uptime-kuma:1
✔ registry.fedoraproject.org/louislam/uptime-kuma:1
Trying to pull registry.fedoraproject.org/louislam/uptime-kuma:1...
Error: initializing source docker://registry.fedoraproject.org/louislam/uptime-kuma:1: reading manifest 1 in registry.fedoraproject.org/louislam/uptime-kuma: manifest unknown: manifest unknown
✔ registry.access.redhat.com/louislam/uptime-kuma:1
Trying to pull registry.access.redhat.com/louislam/uptime-kuma:1...
Error: initializing source docker://registry.access.redhat.com/louislam/uptime-kuma:1: reading manifest 1 in registry.access.redhat.com/louislam/uptime-kuma: name unknown: Repo not found
✔ registry.centos.org/louislam/uptime-kuma:1
Trying to pull registry.centos.org/louislam/uptime-kuma:1...
Error: initializing source docker://registry.centos.org/louislam/uptime-kuma:1: reading manifest 1 in registry.centos.org/louislam/uptime-kuma: manifest unknown: manifest unknown
✔ docker.io/louislam/uptime-kuma:1
Trying to pull docker.io/louislam/uptime-kuma:1...
Getting image source signatures
Copying blob 59583c507ad2 done  
Copying blob c56d959776a3 done  
Copying blob 15115158dd02 done  
Copying blob 0a3670bd8e93 done  
Copying blob 579e31ff2961 done  
Copying blob 7581f704a9fb done  
Copying blob cda0f3030bcb done  
Copying blob bfd44b4f1180 done  
Copying config d25e979aca done  
Writing manifest to image destination
Storing signatures
a2bb93273f2035dfd513abf3fa0d9bfd38b7cc1cebd194e742bfceb01adf9aad
```
然后使用`docker-compose`进行部署，或者`docker run -d --restart=always -p 3001:3001 -v uptime-kuma:/app/data --name uptime-kuma louislam/uptime-kuma:1`
``` bash
[root@cn-py-dl-r8 docker]# cd /root/uptime-kuma/docker
[root@cn-py-dl-r8 docker]# cat docker-compose.yml 
# Simple docker-composer.yml
# You can change your port or volume location

version: '3.3'

services:
  uptime-kuma:
    image: louislam/uptime-kuma
    container_name: uptime-kuma
    volumes:
      - uptime-kuma:/app/data
    ports:
      - 3001:3001

volumes:
  uptime-kuma:
[root@cn-py-dl-r8 docker]# docker-compose  up -d
Creating uptime-kuma ... done
```
最后防火墙放通端口，可参照红帽官方文档：[使用 CLI 控制端口](https://access.redhat.com/documentation/zh-cn/red_hat_enterprise_linux/8/html/securing_networks/controlling-ports-using-cli_using-and-configuring-firewalld#opening-a-port_controlling-ports-using-cli)
```
[root@cn-py-dl-r8 ~]# systemctl status firewalld
● firewalld.service - firewalld - dynamic firewall daemon
   Loaded: loaded (/usr/lib/systemd/system/firewalld.service; enabled; vendor preset: enabled)
   Active: active (running) since Sun 2022-03-27 14:59:55 CST; 5 days ago
     Docs: man:firewalld(1)
 Main PID: 1107 (firewalld)
    Tasks: 2 (limit: 100784)
   Memory: 33.7M
   CGroup: /system.slice/firewalld.service
           └─1107 /usr/libexec/platform-python -s /usr/sbin/firewalld --nofork --nopid

Mar 27 14:59:54 cn-py-dl-r8 systemd[1]: Starting firewalld - dynamic firewall daemon...
Mar 27 14:59:55 cn-py-dl-r8 systemd[1]: Started firewalld - dynamic firewall daemon.
Mar 27 14:59:56 cn-py-dl-r8 firewalld[1107]: WARNING: AllowZoneDrifting is enabled. This is considered >
[root@cn-py-dl-r8 ~]# firewall-cmd --list-services
cockpit dhcpv6-client ssh
[root@cn-py-dl-r8 ~]# firewall-cmd --list-ports

[root@cn-py-dl-r8 ~]# firewall-cmd --add-port=3001/tcp
success
[root@cn-py-dl-r8 ~]# firewall-cmd --list-ports
3001/tcp
[root@cn-py-dl-r8 ~]# firewall-cmd --runtime-to-permanent
success
```

## 0x03.安装[Docker](https://docs.docker.com/install/linux/docker-ce/centos/)
不过`docker`并不是自带的，需要手动安装，`RHEL`下未安装时会提示安装`podman-docker`
``` bash
[root@cn-py-dl-r8 docker]# docker
bash: docker: command not found...
Install package 'podman-docker' to provide command 'docker'? [N/y] y


 * Waiting in queue... 
 * Loading list of packages.... 
The following packages have to be installed:
 podman-docker-1:3.4.2-9.module+el8.5.0+13852+150547f7.noarch   Emulate Docker CLI using podman
Proceed with changes? [N/y] y


 * Waiting in queue... 
 * Waiting for authentication... 
 * Waiting in queue... 
 * Downloading packages... 
 * Requesting data... 
 * Testing changes... 
 * Installing packages... 
Emulate Docker CLI using podman. Create /etc/containers/nodocker to quiet msg.
Error: missing command 'podman COMMAND'
Try 'podman --help' for more information.

[root@cn-py-dl-r8 docker]# docker ps
Emulate Docker CLI using podman. Create /etc/containers/nodocker to quiet msg.
CONTAINER ID  IMAGE       COMMAND     CREATED     STATUS      PORTS       NAMES
```
然后惯例安装`portainer`可视化
``` bash
[root@cn-py-dl-r8 ~]# docker pull portainer/portainer:latest
[root@cn-py-dl-r8 ~]# docker volume create portainer_data
[root@cn-py-dl-r8 ~]# docker run -d -p 9000:9000 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer
Emulate Docker CLI using podman. Create /etc/containers/nodocker to quiet msg.
Error: statfs /var/run/docker.sock: no such file or directory
```
不过在`RHEL`下`docker`并未默认开放`api`访问，并不能直接成功创建容器，需要手动开启，可参照：https://docs.podman.io/en/v3.2.3/_static/api.html
``` bash
[root@cn-py-dl-r8 ~]# podman system service -t 0 &
[1] 108648
[root@cn-py-dl-r8 ~]# ll /var/run | grep "docker.sock"
lrwxrwxrwx.  1 root           root             23 Mar 28 22:16 docker.sock -> /run/podman/podman.sock
[root@cn-py-dl-r8 ~]# docker run -d -p 9000:9000 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer
Emulate Docker CLI using podman. Create /etc/containers/nodocker to quiet msg.
123ced8912a5d1557531d2b9d645aa71061763b5f65d52cef6e5a204f3ad61fb
```
创建成功之后在防火墙中开放端口，结果报错`Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get http://%2Fvar%2Frun%2Fdocker.sock/_ping: dial unix /var/run/docker.sock: connect: permission denied`
![寄](https://i1.yuangezhizao.cn/macOS/20220402103137.png!webp)

于是又去谷歌搜了一圈，这里未尝试：https://github.com/dpw/selinux-dockersock
仅尝试在`-v`后添加小写的`:z`或者大写的`:Z`，结果还是不行
`docker run -d -p 9000:9000 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock:Z -v portainer_data:/data portainer/portainer`

一气之下加上`--privileged`，先凑合用吧`XD`
`docker run -d --privileged -p 9000:9000 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer`

## 0x04.安装[Docker-Compose](https://docs.docker.com/compose/install/)
接下来安装`docker-compose`，没配代理太慢了……
``` bash
[root@cn-py-dl-r8 ~]# wget "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)"
--2022-03-28 22:19:11--  https://github.com/docker/compose/releases/download/1.29.2/docker-compose-Linux-x86_64
Resolving github.com (github.com)... 192.30.255.113
Connecting to github.com (github.com)|192.30.255.113|:443... connected.
HTTP request sent, awaiting response... 302 Found
```
在`MacMini`上下载完，拿`sftp`传上去也比下载快`2333`
``` bash
sftp> put docker-compose-Linux-x86_64
Uploading docker-compose-Linux-x86_64 to /root/docker-compose-Linux-x86_64
  100% 12438KB  12438KB/s 00:00:00     
/Users/yuangezhizao/Downloads/docker-compose-Linux-x86_64: 12737304 bytes transferred in 0 seconds (12438 KB/s)
```
不过也得开启`docker`的`api`，否则运行也会报错

<details><summary>点击此处 ← 查看折叠</summary>

``` bash
[root@cn-py-dl-r8 ~]# mv docker-compose-Linux-x86_64 /usr/local/bin/docker-compose
mv: overwrite '/usr/local/bin/docker-compose'? y
[root@cn-py-dl-r8 ~]# chmod +x /usr/local/bin/docker-compose
[root@cn-py-dl-r8 ~]# docker-compose --version
docker-compose version 1.29.2, build 5becea4c
[root@cn-py-dl-r8 ~]# cd uptime-kuma/docker/
[root@cn-py-dl-r8 docker]# docker-compose up -d
Traceback (most recent call last):
  File "urllib3/connectionpool.py", line 677, in urlopen
  File "urllib3/connectionpool.py", line 392, in _make_request
  File "http/client.py", line 1277, in request
  File "http/client.py", line 1323, in _send_request
  File "http/client.py", line 1272, in endheaders
  File "http/client.py", line 1032, in _send_output
  File "http/client.py", line 972, in send
  File "docker/transport/unixconn.py", line 43, in connect
FileNotFoundError: [Errno 2] No such file or directory

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "requests/adapters.py", line 449, in send
  File "urllib3/connectionpool.py", line 727, in urlopen
  File "urllib3/util/retry.py", line 410, in increment
  File "urllib3/packages/six.py", line 734, in reraise
  File "urllib3/connectionpool.py", line 677, in urlopen
  File "urllib3/connectionpool.py", line 392, in _make_request
  File "http/client.py", line 1277, in request
  File "http/client.py", line 1323, in _send_request
  File "http/client.py", line 1272, in endheaders
  File "http/client.py", line 1032, in _send_output
  File "http/client.py", line 972, in send
  File "docker/transport/unixconn.py", line 43, in connect
urllib3.exceptions.ProtocolError: ('Connection aborted.', FileNotFoundError(2, 'No such file or directory'))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "docker/api/client.py", line 214, in _retrieve_server_version
  File "docker/api/daemon.py", line 181, in version
  File "docker/utils/decorators.py", line 46, in inner
  File "docker/api/client.py", line 237, in _get
  File "requests/sessions.py", line 543, in get
  File "requests/sessions.py", line 530, in request
  File "requests/sessions.py", line 643, in send
  File "requests/adapters.py", line 498, in send
requests.exceptions.ConnectionError: ('Connection aborted.', FileNotFoundError(2, 'No such file or directory'))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "docker-compose", line 3, in <module>
  File "compose/cli/main.py", line 81, in main
  File "compose/cli/main.py", line 200, in perform_command
  File "compose/cli/command.py", line 70, in project_from_options
  File "compose/cli/command.py", line 153, in get_project
  File "compose/cli/docker_client.py", line 43, in get_client
  File "compose/cli/docker_client.py", line 170, in docker_client
  File "docker/api/client.py", line 197, in __init__
  File "docker/api/client.py", line 222, in _retrieve_server_version
docker.errors.DockerException: Error while fetching server API version: ('Connection aborted.', FileNotFoundError(2, 'No such file or directory'))
[21676] Failed to execute script docker-compose
```

</details>

## 0x05.安装[SmokePing](https://oss.oetiker.ch/smokeping)
``` bash
[root@cn-py-dl-r8 ~]# git clone https://github.com/linuxserver/docker-smokeping
[root@cn-py-dl-r8 ~]# cd docker-smokeping/
[root@cn-py-dl-r8 docker-smokeping]# mkdir config data
[root@cn-py-dl-r8 docker-smokeping]# cat docker-compose.yml 
---
version: "2.1"
services:
  smokeping:
    image: lscr.io/linuxserver/smokeping
    container_name: smokeping
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/London
    volumes:
      - /root/docker-smokeping/config:/config
      - /root/docker-smokepingdata:/data
    ports:
      - 81:80
    restart: unless-stopped
[root@cn-py-dl-r8 docker-smokeping]# podman system service -t 0 &
[1] 2547
[root@cn-py-dl-r8 docker-smokeping]# docker-compose up -d
Creating network "docker-smokeping_default" with the default driver
Creating smokeping ... done
```
~~然后去日志里一看，全是报错草……~~在切换了`SELINUX`模式之后不再报错了，这就对了嘛
``` bash
ERROR: can't open /config/General: No such file or directory
httpd: Could not open configuration file /etc/apache2/httpd.conf: No such file or directory
```

## 0x06.安装[x-ui](https://github.com/vaxilu/x-ui)
``` bash
[root@cn-py-dl-r8 ~]# git clone https://github.com/vaxilu/x-ui.git
[root@cn-py-dl-r8 ~]# cd x-ui/
[root@cn-py-dl-r8 x-ui]# ./install.sh
```
代理有点问题所以手动修改脚本内容
1. `wget -N --no-check-certificate -O /usr/local/x-ui-linux-${arch}.tar.gz https://github.com/vaxilu/x-ui/releases/download/${last_version}/x-ui-linux-${arch}.tar.gz`修改为
`wget -N --no-check-certificate -O /usr/local/x-ui-linux-${arch}.tar.gz https://proxy-cf.yuangezhizao.cn/dl/x-ui-linux-amd64.tar.gz`
2. `wget --no-check-certificate -O /usr/bin/x-ui https://raw.githubusercontent.com/vaxilu/x-ui/main/x-ui.sh`修改为`mv /root/x-ui/x-ui.sh /usr/bin/x-ui`

``` bash
[root@cn-py-dl-r8 x-ui]# firewall-cmd --add-port=54321/tcp
success
[root@cn-py-dl-r8 x-ui]# firewall-cmd --runtime-to-permanent
success
```

## 0x07.安装`htop`
``` bash
[root@cn-py-dl-r8 ~]# yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
[root@cn-py-dl-r8 ~]# yum update -y
[root@cn-py-dl-r8 ~]# yum install htop -y
```

## 0x08.后记
唉，`cn-py-dl-c8`全部木大，`cn-py-dl-r8`又得个把月才能再搞起来，心累……

## 0x09.引用
[Centos8安装podman容器+portainerUI+podman API启用方法](https://www.92cto.com/blog/2509.html)
