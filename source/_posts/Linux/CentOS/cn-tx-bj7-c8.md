---
title: 新购 cn-tx-bj7-c8 轻量应用服务器
date: 2021-12-21 14:38:31
tags:
  - CentOS
  - server
count: 1
os: 1
os_1: Monterry 12.1 (21C52)
browser: 1
browser_1: 96.0.4664.110 Stable
place: 新家
key: 127
---
    终于还是用上了你云的轻量应用服务器草
<!-- more -->
## 0x00.前言
怀疑是临时工，反正买到了就闷声发大财嘛，之前还苦恼`cn-tx-bj1-c8`这台好用的`CentOS`来年夏天就要过期了（`2019-05-09 00:27:53`～`2022-05-09 00:27:54`）
然而现在又有新的机子实在是太开心了（`2021-12-20 22:07:24`～`2024-12-20 22:07:24`），假装自己还是学生党`2333`

## 0x01.修改主机名
还是万年不变的套路，毕竟是`SSH`连进去第一件要做的事情
``` bash
[root@cn-tx-bj7-c8 ~]# hostnamectl set-hostname cn-tx-bj7-c8
[root@cn-tx-bj7-c8 ~]# hostnamectl status
   Static hostname: cn-tx-bj7-c8
         Icon name: computer-vm
           Chassis: vm
        Machine ID: 24955ebe6f454781b4db8ea70343d7eb
           Boot ID: 2db66f2ce668440ea196c276e13866d8
    Virtualization: kvm
  Operating System: CentOS Linux 8
       CPE OS Name: cpe:/o:centos:centos:8
            Kernel: Linux 4.18.0-305.3.1.el8.x86_64
      Architecture: x86-64
[root@cn-tx-bj7-c8 ~]# cat /etc/hosts
127.0.0.1 cn-tx-bj7-c8 cn-tx-bj7-c8
127.0.0.1 localhost.localdomain localhost
127.0.0.1 localhost4.localdomain4 localhost4

::1 cn-tx-bj7-c8 cn-tx-bj7-c8
::1 localhost.localdomain localhost
::1 localhost6.localdomain6 localhost6

[root@cn-tx-bj7-c8 ~]# reboot
```

## 0x02.修改`SSH`端口
感叹昨晚十点创建的机子，今天下午两点登录就看到爆破记录草
``` bash
Activate the web console with: systemctl enable --now cockpit.socket

Last failed login: Tue Dec 21 09:53:50 CST 2021 from 45.141.84.10 on ssh:notty
There were 1917 failed login attempts since the last successful login.
Last login: Mon Dec 20 22:48:55 2021 from 123.185.64.217
[root@cn-tx-bj7-c8 ~]#
```
改成非`22`端口防止爆破，并且在你云的防火墙放行新的端口，阻断默认`22`端口
```
[root@cn-tx-bj7-c8 ~]# vim /etc/ssh/sshd_config
……
# If you want to change the port on a SELinux system, you have to tell
# SELinux about this change.
# semanage port -a -t ssh_port_t -p tcp #PORTNUMBER
#
Port <rm>
#AddressFamily any
#ListenAddress 0.0.0.0
#ListenAddress ::
……
[root@cn-tx-bj7-c8 ~]# systemctl restart sshd
```
注意一定要新开个`shell`测试新端口是否生效，生效则可关闭旧`shell`，否则需重新配置（其实也还好吧，大不了就`VNC`救场呗

## 0x03.安装[Fail2ban](https://www.fail2ban.org/)
针对爆破，祭出`Fail2ban`神器
``` bash
[root@cn-tx-bj7-c8 ~]# dnf install fail2ban -y
[root@cn-tx-bj7-c8 ~]# systemctl status fail2ban
● fail2ban.service - Fail2Ban Service
   Loaded: loaded (/usr/lib/systemd/system/fail2ban.service; disabled; vendor preset: disabled)
   Active: inactive (dead)
     Docs: man:fail2ban(1)
```
配置开机自启并启动
``` bash
[root@cn-tx-bj7-c8 ~]# systemctl enable --now fail2ban
Created symlink /etc/systemd/system/multi-user.target.wants/fail2ban.service → /usr/lib/systemd/system/fail2ban.service.
[root@cn-tx-bj7-c8 ~]# systemctl status fail2ban
● fail2ban.service - Fail2Ban Service
   Loaded: loaded (/usr/lib/systemd/system/fail2ban.service; enabled; vendor preset: disabled)
   Active: active (running) since Tue 2021-12-21 14:53:30 CST; 2s ago
     Docs: man:fail2ban(1)
  Process: 277792 ExecStartPre=/bin/mkdir -p /run/fail2ban (code=exited, status=0/SUCCESS)
 Main PID: 277794 (fail2ban-server)
    Tasks: 3 (limit: 23722)
   Memory: 10.7M
   CGroup: /system.slice/fail2ban.service
           └─277794 /usr/bin/python3.6 -s /usr/bin/fail2ban-server -xf start

Dec 21 14:53:30 cn-tx-bj7-c8 systemd[1]: Starting Fail2Ban Service...
Dec 21 14:53:30 cn-tx-bj7-c8 systemd[1]: Started Fail2Ban Service.
Dec 21 14:53:30 cn-tx-bj7-c8 fail2ban-server[277794]: Server ready
```
创建`.local`配置文件，防止更新时`.conf`可能被覆盖
``` bash
[root@cn-tx-bj7-c8 ~]# ll /etc/fail2ban/
total 56
drwxr-xr-x 2 root root  4096 Dec 21 14:52 action.d
-rw-r--r-- 1 root root  2816 Nov 24  2020 fail2ban.conf
drwxr-xr-x 2 root root  4096 Nov 24  2020 fail2ban.d
drwxr-xr-x 3 root root  4096 Dec 21 14:52 filter.d
-rw-r--r-- 1 root root 24996 Nov 24  2020 jail.conf
drwxr-xr-x 2 root root  4096 Dec 21 14:52 jail.d
-rw-r--r-- 1 root root  2827 Nov 24  2020 paths-common.conf
-rw-r--r-- 1 root root   930 Nov 24  2020 paths-fedora.conf
[root@cn-tx-bj7-c8 ~]# cp /etc/fail2ban/jail.{conf,local}
[root@cn-tx-bj7-c8 ~]# ll /etc/fail2ban/
total 84
drwxr-xr-x 2 root root  4096 Dec 21 14:52 action.d
-rw-r--r-- 1 root root  2816 Nov 24  2020 fail2ban.conf
drwxr-xr-x 2 root root  4096 Nov 24  2020 fail2ban.d
drwxr-xr-x 3 root root  4096 Dec 21 14:52 filter.d
-rw-r--r-- 1 root root 24996 Nov 24  2020 jail.conf
drwxr-xr-x 2 root root  4096 Dec 21 14:52 jail.d
-rw-r--r-- 1 root root 24996 Dec 21 14:54 jail.local
-rw-r--r-- 1 root root  2827 Nov 24  2020 paths-common.conf
-rw-r--r-- 1 root root   930 Nov 24  2020 paths-fedora.conf
```
修改配置文件`/etc/fail2ban/jail.local`，开启`SSH`防火墙
``` bash
……
# "bantime" is the number of seconds that a host is banned.
bantime  = 1d

# A host is banned if it has generated "maxretry" during the last "findtime"
# seconds.
findtime  = 10m

# "maxretry" is the number of failures before a host get banned.
maxretry = 5
……
[sshd]

# To use more aggressive sshd modes set filter parameter "mode" in jail.local:
# normal (default), ddos, extra or aggressive (combines all).
# See "tests/files/logs/sshd" or "filter.d/sshd.conf" for usage example and details.
enabled = true
#mode   = normal
port    = <rm>
logpath = %(sshd_log)s
backend = %(sshd_backend)s
```
最后就可以使用`Fail2ban客户端`查看状态了，是不是很简单？
```
[root@cn-tx-bj7-c8 ~]# fail2ban-client status
Status
|- Number of jail:      1
`- Jail list:   sshd
[root@cn-tx-bj7-c8 ~]# fail2ban-client status sshd
Status for the jail: sshd
|- Filter
|  |- Currently failed: 0
|  |- Total failed:     0
|  `- Journal matches:  _SYSTEMD_UNIT=sshd.service + _COMM=sshd
`- Actions
   |- Currently banned: 0
   |- Total banned:     0
   `- Banned IP list:
```

## 0x04.开启[Cockpit](https://github.com/cockpit-project/cockpit)
还记得之前登录时看到的`Activate the web console with: systemctl enable --now cockpit.socket`嘛？搞定了`SSH`之后可以尝鲜开启它了，之前倒还真没用过……
``` bash
[root@cn-tx-bj7-c8 ~]# systemctl enable --now cockpit.socket
Created symlink /etc/systemd/system/sockets.target.wants/cockpit.socket → /usr/lib/systemd/system/cockpit.socket.
[root@cn-tx-bj7-c8 ~]# systemctl status cockpit.socket
● cockpit.socket - Cockpit Web Service Socket
   Loaded: loaded (/usr/lib/systemd/system/cockpit.socket; enabled; vendor preset: disabled)
   Active: active (listening) since Tue 2021-12-21 15:30:09 CST; 14s ago
     Docs: man:cockpit-ws(8)
   Listen: [::]:9090 (Stream)
  Process: 285185 ExecStartPost=/bin/ln -snf active.motd /run/cockpit/motd (code=exited, status=0/SUCCESS)
  Process: 285178 ExecStartPost=/usr/share/cockpit/motd/update-motd  localhost (code=exited, status=0/SUCCESS)
    Tasks: 0 (limit: 23722)
   Memory: 4.0K
   CGroup: /system.slice/cockpit.socket

Dec 21 15:30:09 cn-tx-bj7-c8 systemd[1]: Starting Cockpit Web Service Socket.
Dec 21 15:30:09 cn-tx-bj7-c8 systemd[1]: Listening on Cockpit Web Service Socket.
[root@cn-tx-bj7-c8 ~]# systemctl status cockpit
● cockpit.service - Cockpit Web Service
   Loaded: loaded (/usr/lib/systemd/system/cockpit.service; static; vendor preset: disabled)
   Active: inactive (dead)
     Docs: man:cockpit-ws(8)
```
然后访问`9090`端口，使用`SSH`的账户登录，哇哦界面针不戳，有那味儿了
![登录](https://i1.yuangezhizao.cn/macOS/20211221153308.png!webp)
![概览](https://i1.yuangezhizao.cn/macOS/20211221153544.png!webp)

从`账户`中还能看到有个已锁定的`lighthouse`用户草
![账户](https://i1.yuangezhizao.cn/macOS/20211221153940.png!webp)

也可以查看各服务的运行状态
![服务](https://i1.yuangezhizao.cn/macOS/20211221154246.png!webp)

当然最重要的终端自然也是有滴
![终端](https://i1.yuangezhizao.cn/macOS/20211221160249.png!webp)

## 0x05.导出`MongoDB`数据
`cn-tx-bj3-w9d`上`C`盘又告急了草，`spacesniffer`一扫发现`MongoDB`的数据有`7.4G`，相比其他小文件还算挺大的
![C](https://i1.yuangezhizao.cn/macOS/20211221204036.png!webp)
![data](https://i1.yuangezhizao.cn/macOS/20211221204146.png!webp)

因为`windows`上默认安装不含`mongodump`可执行程序，需要手动下载`mongodb-database-tools-windows-x86_64-100.5.1.zip`工具包并解压，然后执行`mongodump`
``` bash
E:\mongodb-database-tools-windows-x86_64-100.5.1\bin>mongodump -u<rm> -p<rm> -o "X:\\mongodb_data"
2021-12-21T21:04:12.503+0800    writing admin.system.users to X:\mongodb_data\admin\system.users.bson
2021-12-21T21:04:12.548+0800    done dumping admin.system.users (2 documents)
2021-12-21T21:04:12.548+0800    writing admin.system.version to X:\mongodb_data\admin\system.version.bson
2021-12-21T21:04:12.558+0800    done dumping admin.system.version (3 documents)
……
2021-12-21T21:16:42.272+0800    [#######################.]  bilibili.bilibili_all_3  4355003/4369494  (99.7%)
2021-12-21T21:16:43.128+0800    [########################]  bilibili.bilibili_all_3  4369494/4369494  (100.0%)
2021-12-21T21:16:45.550+0800    done dumping bilibili.bilibili_all_3 (4369494 documents)
```
并且迁移过程中`cn-tx-bj3-w9d`连文件复制的空间都木大了~~，又看了一圈占用空间较大的地方，把虚拟内存修改成了`256-512`重启后竟然报错说虚拟内存过低，又给调大到`512-1024`……~~
![data](https://i1.yuangezhizao.cn/macOS/20211221214344.png!webp)

<span title="你知道的太多了" class="heimu">调时一时爽，卡爆火葬场……</span>又被坑了数个小时，这个虚拟内存千万不能调小，调完之后系统巨卡无比（还是得设置成让系统自动管理才对
并且图形化挂载`S3`的工具频频报错也太不稳定了，只好`pip`安装`coscmd`，安装的时候发现`pip`也被设置成了你云的镜像源，`C:\>coscmd upload -r --skipmd5 X:/mongodb_data mongo_data_bak`这才算是终于把`mongodump`导出的数据拿出来了，耗时俩小时真是日了狗了
趣事：在`upload`某一个集合的时候，`CPU`会跑满，上行速度从几十兆每秒瞬间降低到几百`K`至一两兆，重启无果
后来看到集合的名称是`wooyun`突然恍然大悟，再结合占`CPU`高的进程是`windows defender`不难得出因为内容满是漏洞`POC`所以劲爆扫描草，于是就先跳过了这个集合
![100](https://i1.yuangezhizao.cn/macOS/20211221225103.png!webp)
![wooyun](https://i1.yuangezhizao.cn/macOS/20211221225212.png!webp)

## 0x06.安装[MongoDB](https://web.archive.org/web/20211221084419/https://docs.mongodb.com/manual/tutorial/install-mongodb-on-red-hat/)
这里需要手动创建一个`5.0`的源
``` bash
[root@cn-tx-bj7-c8 ~]# cat /etc/yum.repos.d/mongodb-org-5.0.repo
[mongodb-org-5.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/5.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-5.0.asc
[root@cn-tx-bj7-c8 ~]# dnf install mongodb-org -y
……
[root@cn-tx-bj7-c8 ~]# systemctl enable mongod --now
```
等到下一步[#0x07-导入MongoDB数据](#0x07-导入MongoDB数据)再执行完数据导入后，修改配置文件
``` bash
[root@cn-tx-bj7-c8 ~]# vim /etc/mongod.conf
# network interfaces
net:
  port: 27017
  bindIp: 0.0.0.0  # Enter 0.0.0.0,:: to bind to all IPv4 and IPv6 addresses or, alternatively, use the net.bindIpAll setting.


security:
  authorization: enabled
[root@cn-tx-bj7-c8 ~]# systemctl restart mongod
```
![终于搞定了](https://i1.yuangezhizao.cn/macOS/20211222005512.png!webp)

## 0x07.导入`MongoDB`数据
途中去挂载`cn-tx-bj3-w9d`导出数据所在的`CIFS`文件系统的时候，发现`文件存储`竟然不支持和`cn-tx-bj7-c8`内网互通，~~血贵的`云联网`简直劝退，~~云联网`同地域 5Gbps 及以下带宽免费`
弱小无助的自己费尽周折上传到了`COS`，毕竟文件存储是按时付费的淦，越快操作完越省钱啊，结果后来发现只要开通`云联网`之后内网就可以互通了草
``` bash
[root@cn-tx-bj7-c8 ~]# dnf install nfs-utils -y
[root@cn-tx-bj7-c8 ~]# mkdir localfolder
[root@cn-tx-bj7-c8 ~]# ls
localfolder
[root@cn-tx-bj7-c8 ~]# mount -t nfs -o vers=3,nolock,proto=tcp,noresvport 10.0.2.15:/<rm> localfolder
mount.nfs: Connection timed out
```
要从`COS`中转就也得安装`coscmd`，并且确认是内网域名，毕竟是大体积下载还是得确认一下，<span title="你知道的太多了" class="heimu">不能外网流量被反撸</span>（国内带宽`0.5/G`太贵了
``` bash
[root@cn-tx-bj7-c8 ~]# pip -V
pip 9.0.3 from /usr/lib/python3.6/site-packages (python 3.6)
[root@cn-tx-bj7-c8 ~]# pip3 -V
pip 9.0.3 from /usr/lib/python3.6/site-packages (python 3.6)
[root@cn-tx-bj7-c8 ~]# pip3 install coscmd
WARNING: Running pip install with root privileges is generally not a good idea. Try `pip3 install --user` instead.
Collecting coscmd
  Downloading http://mirrors.tencentyun.com/pypi/packages/7b/68/00f9ea072d29d3692ebfdb08111cdce828e9590a03dfc8bfcf7b608167d7/coscmd-1.8.6.24.tar.gz
……
[root@cn-tx-bj7-c8 ~]# coscmd config -a <rm> -s <rm> -b centos-<rm> -r ap-beijing
Created configuration file in b'/root/.cos.conf'
[root@cn-tx-bj7-c8 ~]# nslookup centos-<rm>.cos.ap-beijing.myqcloud.com
Server:         183.60.82.98
Address:        183.60.82.98#53

Name:   centos-<rm>.cos.ap-beijing.myqcloud.com
Address: 169.254.0.49
```
然后光速内网下载
``` bash
[root@cn-tx-bj7-c8 ~]# coscmd download -r /mongo_data_bak mongo_data_bak
……
Downloading mongo_data_bak/bilibili/2020AOY.bson
100%|██████████████████████████████████████| 47.0M/47.0M [00:00<00:00, 64.3MB/s]
Download cos://centos-<rm>/mongo_data_bak/bilibili/bilibili_all_2.bson   =>   mongo_data_bak/bilibili/bilibili_all_2.bson
Downloading mongo_data_bak/bilibili/bilibili_all_2.bson
1.57GB [00:20, 82.1MB/s]                                                        
Download cos://centos-<rm>/mongo_data_bak/bilibili/bilibili_all_3.bson   =>   mongo_data_bak/bilibili/bilibili_all_3.bson
Downloading mongo_data_bak/bilibili/bilibili_all_3.bson
11.3GB [02:09, 93.3MB/s]                                                        
Download cos://centos-<rm>/mongo_data_bak/bilibili/bilibili_all_4.bson   =>   mongo_data_bak/bilibili/bilibili_all_4.bson
Downloading mongo_data_bak/bilibili/bilibili_all_4.bson
6.46GB [01:09, 100MB/s]                                                         
Download cos://centos-<rm>/mongo_data_bak/biliplus/view.bson   =>   mongo_data_bak/biliplus/view.bson
Downloading mongo_data_bak/biliplus/view.bson
691MB [00:01, 380MB/s]                                                          
Download cos://centos-<rm>/mongo_data_bak/jd_campus/feeds.bson   =>   mongo_data_bak/jd_campus/feeds.bson
Downloading mongo_data_bak/jd_campus/feeds.bson
256MB [00:03, 79.4MB/s]                                                         
Download cos://centos-<rm>/mongo_data_bak/masadora/notes.bson   =>   mongo_data_bak/masadora/notes.bson
Downloading mongo_data_bak/masadora/notes.bson
577MB [00:06, 90.1MB/s]                                                         
Download cos://centos-<rm>/mongo_data_bak/rbc/attend_class.bson   =>   mongo_data_bak/rbc/attend_class.bson
Downloading mongo_data_bak/rbc/attend_class.bson
89.7MB [00:00, 120MB/s]                                                         
Download cos://centos-<rm>/mongo_data_bak/twitter/inoriminase.bson   =>   mongo_data_bak/twitter/inoriminase.bson
Downloading mongo_data_bak/twitter/inoriminase.bson
25.8MB [00:00, 55.2MB/s]                                                        
90 files downloaded, 0 files skipped, 0 files failed
……
```
最后终于可以导入了，这一刻真就等了一天草，因为是在本地新安装的`mongod`所以也不用特意指定地址和端口辣，简直太方便了
``` bash
[root@cn-tx-bj7-c8 ~]# mongorestore mongo_data_bak
2021-12-21T23:14:50.794+0800    preparing collections to restore from
……
2021-12-21T23:14:50.810+0800    reading metadata for bilibili.bilibili_all_3 from mongo_data_bak/bilibili/bilibili_all_3.metadata.json
……
2021-12-21T23:14:50.868+0800    restoring bilibili.bilibili_all_3 from mongo_data_bak/bilibili/bilibili_all_3.bson
……
2021-12-21T23:19:12.376+0800    [########################]  bilibili.bilibili_all_3  11.1GB/11.1GB  (100.0%)
2021-12-21T23:19:12.376+0800    finished restoring bilibili.bilibili_all_3 (4369494 documents, 0 failures)
……
2021-12-21T23:19:13.660+0800    restoring indexes for collection bilibili.bilibili_all_3 from metadata
2021-12-21T23:19:13.660+0800    index: &idx.IndexDocument{Options:primitive.M{"background":false, "name":"aid", "unique":true, "v":2}, Key:primitive.D{primitive.E{Key:"aid", Value:1}}, PartialFilterExpression:primitive.D(nil)}
……
2021-12-21T23:19:42.663+0800    7550066 document(s) restored successfully. 0 document(s) failed to restore.
```
备注：翻文档的时候还发现可以[标准输入导入](https://web.archive.org/web/20211221151924/https://docs.mongodb.com/database-tools/mongorestore/)，不过限于外网带宽只有`1m`还是算了：`mongodump --archive --db=test --port=27017 | mongorestore --archive --port=27018`
`2021-12-22 01:06:31`：在开通`云联网`之后，去搞定最后一个`wooyun`集合，一顿操作猛如虎
``` bash
E:\mongodb-database-tools-windows-x86_64-100.5.1\bin>mongodump -d wooyun -o "X:\\mongodb_data"
2021-12-21T23:53:20.157+0800    writing wooyun.wooyun_drops to X:\mongodb_data\wooyun\wooyun_drops.bson
2021-12-21T23:53:20.391+0800    writing wooyun.wooyun_list to X:\mongodb_data\wooyun\wooyun_list.bson
2021-12-21T23:53:22.095+0800    [#################.......]  wooyun.wooyun_drops    936/1269  (73.8%)
2021-12-21T23:53:22.101+0800    [........................]   wooyun.wooyun_list  1451/40293   (3.6%)
2021-12-21T23:53:22.103+0800
2021-12-21T23:53:22.742+0800    [########################]  wooyun.wooyun_drops  1269/1269  (100.0%)
2021-12-21T23:53:23.302+0800    done dumping wooyun.wooyun_drops (1269 documents)
2021-12-21T23:53:25.083+0800    [##......................]  wooyun.wooyun_list  4787/40293  (11.9%)
2021-12-21T23:53:28.159+0800    [#####...................]  wooyun.wooyun_list  8395/40293  (20.8%)
2021-12-21T23:53:31.083+0800    [######..................]  wooyun.wooyun_list  10725/40293  (26.6%)
2021-12-21T23:53:34.149+0800    [########................]  wooyun.wooyun_list  13840/40293  (34.3%)
2021-12-21T23:53:37.132+0800    [##########..............]  wooyun.wooyun_list  17739/40293  (44.0%)
2021-12-21T23:53:40.083+0800    [############............]  wooyun.wooyun_list  21036/40293  (52.2%)
2021-12-21T23:53:43.083+0800    [##############..........]  wooyun.wooyun_list  25147/40293  (62.4%)
2021-12-21T23:53:46.124+0800    [#################.......]  wooyun.wooyun_list  29754/40293  (73.8%)
2021-12-21T23:53:49.087+0800    [###################.....]  wooyun.wooyun_list  32785/40293  (81.4%)
2021-12-21T23:53:52.112+0800    [#####################...]  wooyun.wooyun_list  36894/40293  (91.6%)
2021-12-21T23:53:54.499+0800    [########################]  wooyun.wooyun_list  40293/40293  (100.0%)
2021-12-21T23:53:56.458+0800    done dumping wooyun.wooyun_list (40293 documents)
```
再还原
``` bash
[root@cn-tx-bj7-c8 test]# mongorestore mongodb_data
2021-12-21T23:54:39.134+0800    preparing collections to restore from
2021-12-21T23:54:39.139+0800    reading metadata for wooyun.wooyun_drops from mongodb_data/wooyun/wooyun_drops.metadata.json
2021-12-21T23:54:39.142+0800    reading metadata for wooyun.wooyun_list from mongodb_data/wooyun/wooyun_list.metadata.json
2021-12-21T23:54:39.167+0800    restoring wooyun.wooyun_drops from mongodb_data/wooyun/wooyun_drops.bson
2021-12-21T23:54:39.178+0800    restoring wooyun.wooyun_list from mongodb_data/wooyun/wooyun_list.bson
2021-12-21T23:54:40.796+0800    finished restoring wooyun.wooyun_drops (1269 documents, 0 failures)
2021-12-21T23:54:42.134+0800    [##......................]  wooyun.wooyun_list  182MB/1.63GB  (10.9%)
2021-12-21T23:54:45.134+0800    [#####...................]  wooyun.wooyun_list  369MB/1.63GB  (22.1%)
2021-12-21T23:54:48.134+0800    [#######.................]  wooyun.wooyun_list  554MB/1.63GB  (33.2%)
2021-12-21T23:54:51.134+0800    [##########..............]  wooyun.wooyun_list  729MB/1.63GB  (43.7%)
2021-12-21T23:54:54.134+0800    [#############...........]  wooyun.wooyun_list  925MB/1.63GB  (55.5%)
2021-12-21T23:54:57.134+0800    [###############.........]  wooyun.wooyun_list  1.07GB/1.63GB  (65.5%)
2021-12-21T23:55:00.134+0800    [##################......]  wooyun.wooyun_list  1.25GB/1.63GB  (76.9%)
2021-12-21T23:55:03.134+0800    [####################....]  wooyun.wooyun_list  1.41GB/1.63GB  (86.9%)
2021-12-21T23:55:06.135+0800    [#######################.]  wooyun.wooyun_list  1.60GB/1.63GB  (98.0%)
2021-12-21T23:55:06.799+0800    [########################]  wooyun.wooyun_list  1.63GB/1.63GB  (100.0%)
2021-12-21T23:55:06.799+0800    finished restoring wooyun.wooyun_list (40293 documents, 0 failures)
2021-12-21T23:55:06.799+0800    restoring indexes for collection wooyun.wooyun_drops from metadata
2021-12-21T23:55:06.799+0800    index: &idx.IndexDocument{Options:primitive.M{"name":"datetime_1", "v":1}, Key:primitive.D{primitive.E{Key:"datetime", Value:1}}, PartialFilterExpression:primitive.D(nil)}
2021-12-21T23:55:06.799+0800    index: &idx.IndexDocument{Options:primitive.M{"name":"url", "unique":true, "v":2}, Key:primitive.D{primitive.E{Key:"url", Value:1}}, PartialFilterExpression:primitive.D(nil)}
2021-12-21T23:55:06.799+0800    restoring indexes for collection wooyun.wooyun_list from metadata
2021-12-21T23:55:06.799+0800    index: &idx.IndexDocument{Options:primitive.M{"name":"datetime_1", "v":1}, Key:primitive.D{primitive.E{Key:"datetime", Value:1}}, PartialFilterExpression:primitive.D(nil)}
2021-12-21T23:55:06.799+0800    index: &idx.IndexDocument{Options:primitive.M{"name":"wooyun_id", "unique":true, "v":2}, Key:primitive.D{primitive.E{Key:"wooyun_id", Value:1}}, PartialFilterExpression:primitive.D(nil)}
2021-12-21T23:55:08.285+0800    41562 document(s) restored successfully. 0 document(s) failed to restore.
```
最后卸载`cn-tx-bj3-w9d`上的`MongoDB`，寿终正寝已完成使命（<span title="你知道的太多了" class="heimu">这内存大户就是个定时炸弹，尤其是作死全文搜索的时候<span>
![卸载](https://i1.yuangezhizao.cn/macOS/20211221235959.png!webp)

## 0x06.后记
折腾了一天好累，反正万事开头难

## 0x07.引用
[如何在CentOS 8上安装和配置Fail2ban](https://web.archive.org/web/20211221065719/https://www.myfreax.com/install-configure-fail2ban-on-centos-8/)
[如何在CentOS 8中安装Cockpit Web Console](https://web.archive.org/web/20211221074630/https://www.howtoing.com/install-cockpit-web-console-in-centos-8)
[Cockpit - 使用Web浏览器监视和管理多个Linux服务器的强大工具](https://web.archive.org/web/20211221074818/https://www.howtoing.com/cockpit-monitor-multiple-linux-servers-via-web-browser/)
[如何在CentOS 8上安装MongoDB](https://web.archive.org/web/20211221084731/https://www.myfreax.com/how-to-install-mongodb-on-centos-8/)
