---
title: 良心云 CentOS 学生机切换 RHEL
date: 2022-05-08 10:37:00
tags:
  - RHEL
  - server
count: 2
os: 1
os_1: Monterry 12.3.1 (21E258)
browser: 0
browser_1: 101.0.4951.54 Stable
place: 新家
key: 141
---
    毕业三年已经过去，光速又续费了三年
<!-- more -->
## 0x00.前言
还不是因为`CentOS 8`提前停止支持，虽然良心云的公共镜像中含有`AlmaLinux 8.5`亦或是`Rocky Linux 8.5`
但自己还是选择折腾封装红帽的自定义镜像，`Self-Support`它不香吗？就翻红帽文档呗
![2019~2025](https://i1.yuangezhizao.cn/macOS/20220510230335.png!webp)

## 0x01.自定义镜像
其实国外的公有云大都提供了`RHEL`的镜像，而国内则只看到福报云和红帽有`PY`交易：[Red Hat云接入计划](https://web.archive.org/web/20220510132949/https://help.aliyun.com/document_detail/88267.html)
出于安全性的考量，决定自己动手丰衣足食，坚决不用第三方提供的`RHEL`镜像，良心云也提供了[制作 Linux 镜像](https://web.archive.org/web/20220510133801/https://cloud.tencent.com/document/product/213/17814)的文档
并且谷歌还搜索到了[一步一步导入RHEL镜像到腾讯云](https://web.archive.org/web/20220510133611/https://cloud.tencent.com/developer/article/1820786)，这下更有自信心了`2333`

## 0x02.`cn-py-dl-r8`
入口在`云服务器`控制台的`服务迁移`下，不管是[在线迁移](https://web.archive.org/web/20220510134231/https://cloud.tencent.com/document/product/213/32961)还是[离线迁移](https://web.archive.org/web/20220510134039/https://cloud.tencent.com/document/product/213/19233)都需要先在本地安装好系统，然后进行迁移
本着节省传输和迁移的时间决定使用`离线迁移`的方法，并且目前`在线迁移`处于公测期间，害得加群申请开通服务……
没有新版镜像就还是用`rhel-8.5-x86_64-dvd.iso`，一顿操作猛如虎，很快就在`vCenter`新装好了一台，毕竟之前已经装过一次了（
> [VMware vCenter 安装 RHEL 8](../../VM/vCenter/RHEL-8.html)

需要注意的是不需要默认勾选的`GUI`类型，图形化桌面内存占用还是太高了[#108271669063819198](https://mastodon.yuangezhizao.cn/@yuangezhizao/108271669063819198)，安装完成之后照着良心云文档一步一步的检查

### 1. 确认`OS`分区为`MBR`分区，而非`GPT`
``` bash
[root@UPS-PC home]# parted -l /dev/sda | grep 'Partition Table'
Partition Table: msdos
```

### 2. 确认操作系统以`BIOS`方式启动，而非`EFI`
``` bash
[root@UPS-PC home]# ls /sys/firmware/efi
ls: cannot access '/sys/firmware/efi': No such file or directory
```

### 3. 确认`GRUB`使用硬盘`UUID`挂载
首先查询到`/root`的文件系统名称为`/dev/sda1`，然后查询`UUID`，最后检查`/etc/fstab`发现已经是`UUID`，并且未挂载其它硬盘
``` bash
[root@UPS-PC home]# df -TH
Filesystem            Type      Size  Used Avail Use% Mounted on
devtmpfs              devtmpfs  4.1G     0  4.1G   0% /dev
tmpfs                 tmpfs     4.1G     0  4.1G   0% /dev/shm
tmpfs                 tmpfs     4.1G  9.1M  4.1G   1% /run
tmpfs                 tmpfs     4.1G     0  4.1G   0% /sys/fs/cgroup
/dev/mapper/rhel-root xfs       8.6G  1.7G  7.0G  20% /
/dev/sda1             xfs       1.1G  222M  842M  21% /boot
tmpfs                 tmpfs     815M     0  815M   0% /run/user/0
[root@UPS-PC home]# blkid /dev/sda1
/dev/sda1: UUID="633c5f10-f4c5-4766-b17b-82d7b3cd7ff7" BLOCK_SIZE="512" TYPE="xfs" PARTUUID="0d2cab79-01"
[root@UPS-PC home]# cat /etc/fstab
#
# /etc/fstab
# Created by anaconda on Sun May  8 13:02:32 2022
#
# Accessible filesystems, by reference, are maintained under '/dev/disk/'.
# See man pages fstab(5), findfs(8), mount(8) and/or blkid(8) for more info.
#
# After editing this file, run 'systemctl daemon-reload' to update systemd
# units generated from this file.
#
/dev/mapper/rhel-root   /                       xfs     defaults        0 0
UUID=633c5f10-f4c5-4766-b17b-82d7b3cd7ff7 /boot                   xfs     defaults        0 0
/dev/mapper/rhel-swap   none                    swap    defaults        0 0
```

### 4. 确认`/etc/shadow`权限`可以读写`
``` bash
[root@UPS-PC home]# ll /etc/shadow
----------. 1 root root 634 May  8 21:06 /etc/shadow
```

### 5. 确认内核支持`Virtio`驱动
很不幸`RHEL 8.5`默认不支持，需要重新配置临时文件系统`initramfs`
``` bash
[root@UPS-PC home]# grep -i virtio /boot/config-$(uname -r)
CONFIG_BLK_MQ_VIRTIO=y
CONFIG_VIRTIO_VSOCKETS=m
CONFIG_VIRTIO_VSOCKETS_COMMON=m
CONFIG_VIRTIO_BLK=m
# CONFIG_VIRTIO_BLK_SCSI is not set
CONFIG_SCSI_VIRTIO=m
CONFIG_VIRTIO_NET=m
CONFIG_VIRTIO_CONSOLE=m
CONFIG_HW_RANDOM_VIRTIO=y
CONFIG_DRM_VIRTIO_GPU=m
CONFIG_VIRTIO=y
CONFIG_VIRTIO_PCI_LIB=y
CONFIG_VIRTIO_MENU=y
CONFIG_VIRTIO_PCI=y
CONFIG_VIRTIO_PCI_LEGACY=y
CONFIG_VIRTIO_VDPA=m
CONFIG_VIRTIO_BALLOON=m
CONFIG_VIRTIO_INPUT=m
# CONFIG_VIRTIO_MMIO is not set
# CONFIG_RPMSG_VIRTIO is not set
CONFIG_VIRTIO_FS=m
# CONFIG_CRYPTO_DEV_VIRTIO is not set
[root@UPS-PC home]# lsinitrd /boot/initramfs-$(uname -r).img | grep virtio
[root@UPS-PC home]# ll /etc/dracut.conf.d/
total 0
[root@UPS-PC home]# mkinitrd -f --allow-missing --with=virtio_blk --preload=virtio_blk --with=virtio_net --preload=virtio_net --with=virtio_console --preload=virtio_console /boot/initramfs-$(uname -r).img $(uname -r)
Creating: target|kernel|dracut args|basicmodules 
[root@UPS-PC home]# ll /etc/dracut.conf.d/
total 0
[root@UPS-PC home]# lsinitrd /boot/initramfs-$(uname -r).img | grep virtio
Arguments: -f --add-drivers ' virtio_blk virtio_blk virtio_net virtio_net virtio_console virtio_console'
-rw-r--r--   1 root     root         8996 Sep 20  2021 usr/lib/modules/4.18.0-348.el8.x86_64/kernel/drivers/block/virtio_blk.ko.xz
-rw-r--r--   1 root     root        14856 Sep 20  2021 usr/lib/modules/4.18.0-348.el8.x86_64/kernel/drivers/char/virtio_console.ko.xz
-rw-r--r--   1 root     root        25644 Sep 20  2021 usr/lib/modules/4.18.0-348.el8.x86_64/kernel/drivers/net/virtio_net.ko.xz
```

### 6. 安装`cloud-init`
使用`RHEL`标准仓库自带源，毕竟都用红帽了果断拒绝良心云文档中的手动编译
``` bash
[root@UPS-PC home]# yum install cloud-init -y
Updating Subscription Management repositories.
Unable to read consumer identity

This system is not registered with an entitlement server. You can use subscription-manager to register.

Error: There are no enabled repositories in "/etc/yum.repos.d", "/etc/yum/repos.d", "/etc/distro.repos.d".
```
看来在`cn-py-dl-r8`不注册是绕不过去了，`subscription-manager`一条`register --auto-attach`搞定，在执行这条命令之后还是一如既往的需要等待很久……
``` bash
[root@UPS-PC home]# subscription-manager register --username <rm> --password <rm> --auto-attach
Registering to: subscription.rhsm.redhat.com:443/subscription
The system has been registered with ID: <rm>
The registered system name is: UPS-PC.py.local
Installed Product Current Status:
Product Name: Red Hat Enterprise Linux for x86_64
Status:       Subscribed
```
然后执行结束正准备安装`cloud-init`的时候，发现害没完事儿`(╯°□°）╯︵┻━┻`
``` bash
[root@UPS-PC home]# yum install cloud-init -y
Updating Subscription Management repositories.
Waiting for process with pid 15203 to finish.
^CKeyboardInterrupt: Terminated.
[root@UPS-PC home]# ps aux | grep 15203
root       15203  0.4  1.3 675056 105852 ?       SNs  21:36   0:03 /usr/libexec/platform-python /usr/bin/dnf makecache --timer
root       15259  0.0  0.0  12136  1100 pts/0    S+   21:48   0:00 grep --color=auto 15203
```
> 2000 years later

<details><summary>点击此处 ← 查看折叠</summary>

``` bash
[root@UPS-PC home]# yum install cloud-init -y
Updating Subscription Management repositories.
Last metadata expiration check: 0:01:04 ago on Sun 08 May 2022 09:49:17 PM CST.
Dependencies resolved.
========================================================================================================
 Package                 Arch   Version                          Repository                        Size
========================================================================================================
Installing:
 cloud-init              noarch 21.1-7.el8_5.5                   rhel-8-for-x86_64-appstream-rpms 1.1 M
Installing dependencies:
 bind-export-libs        x86_64 32:9.11.26-6.el8                 rhel-8-for-x86_64-baseos-rpms    1.1 M
 checkpolicy             x86_64 2.9-1.el8                        rhel-8-for-x86_64-baseos-rpms    346 k
 dhcp-client             x86_64 12:4.3.6-45.el8                  rhel-8-for-x86_64-baseos-rpms    318 k
 dhcp-common             noarch 12:4.3.6-45.el8                  rhel-8-for-x86_64-baseos-rpms    207 k
 dhcp-libs               x86_64 12:4.3.6-45.el8                  rhel-8-for-x86_64-baseos-rpms    148 k
 gdisk                   x86_64 1.0.3-6.el8                      rhel-8-for-x86_64-baseos-rpms    239 k
 ipcalc                  x86_64 0.2.4-4.el8                      rhel-8-for-x86_64-baseos-rpms     38 k
 python3-audit           x86_64 3.0-0.17.20191104git1c2f876.el8  rhel-8-for-x86_64-baseos-rpms     86 k
 python3-babel           noarch 2.5.1-7.el8                      rhel-8-for-x86_64-appstream-rpms 4.8 M
 python3-cffi            x86_64 1.11.5-5.el8                     rhel-8-for-x86_64-baseos-rpms    238 k
 python3-cryptography    x86_64 3.2.1-5.el8                      rhel-8-for-x86_64-baseos-rpms    559 k
 python3-jinja2          noarch 2.10.1-3.el8                     rhel-8-for-x86_64-appstream-rpms 538 k
 python3-jsonpatch       noarch 1.21-2.el8                       rhel-8-for-x86_64-appstream-rpms  27 k
 python3-jsonpointer     noarch 1.10-11.el8                      rhel-8-for-x86_64-appstream-rpms  20 k
 python3-jsonschema      noarch 2.6.0-4.el8                      rhel-8-for-x86_64-appstream-rpms  82 k
 python3-jwt             noarch 1.6.1-2.el8                      rhel-8-for-x86_64-baseos-rpms     43 k
 python3-libsemanage     x86_64 2.9-6.el8                        rhel-8-for-x86_64-baseos-rpms    127 k
 python3-markupsafe      x86_64 0.23-19.el8                      rhel-8-for-x86_64-appstream-rpms  39 k
 python3-netifaces       x86_64 0.10.6-4.el8                     rhel-8-for-x86_64-appstream-rpms  25 k
 python3-oauthlib        noarch 2.1.0-1.el8                      rhel-8-for-x86_64-baseos-rpms    155 k
 python3-ply             noarch 3.9-9.el8                        rhel-8-for-x86_64-baseos-rpms    111 k
 python3-policycoreutils noarch 2.9-16.el8                       rhel-8-for-x86_64-baseos-rpms    2.2 M
 python3-prettytable     noarch 0.7.2-14.el8                     rhel-8-for-x86_64-appstream-rpms  44 k
 python3-pycparser       noarch 2.14-14.el8                      rhel-8-for-x86_64-baseos-rpms    109 k
 python3-pyserial        noarch 3.1.1-8.el8                      rhel-8-for-x86_64-appstream-rpms 169 k
 python3-pytz            noarch 2017.2-9.el8                     rhel-8-for-x86_64-appstream-rpms  54 k
 python3-pyyaml          x86_64 3.12-12.el8                      rhel-8-for-x86_64-baseos-rpms    193 k
 python3-setools         x86_64 4.3.0-2.el8                      rhel-8-for-x86_64-baseos-rpms    626 k
Installing weak dependencies:
 geolite2-city           noarch 20180605-1.el8                   rhel-8-for-x86_64-appstream-rpms  19 M
 geolite2-country        noarch 20180605-1.el8                   rhel-8-for-x86_64-appstream-rpms 1.0 M
 libmaxminddb            x86_64 1.2.0-10.el8                     rhel-8-for-x86_64-appstream-rpms  33 k

Transaction Summary
========================================================================================================
Install  32 Packages

Total download size: 34 M
Installed size: 106 M
Downloading Packages:
(1/32): python3-prettytable-0.7.2-14.el8.noarch.rpm                      14 kB/s |  44 kB     00:03    
(2/32): python3-jsonpointer-1.10-11.el8.noarch.rpm                       32 kB/s |  20 kB     00:00    
(3/32): python3-pyserial-3.1.1-8.el8.noarch.rpm                          31 kB/s | 169 kB     00:05    
(4/32): python3-jsonschema-2.6.0-4.el8.noarch.rpm                        60 kB/s |  82 kB     00:01    
(5/32): geolite2-country-20180605-1.el8.noarch.rpm                      287 kB/s | 1.0 MB     00:03    
(6/32): python3-jsonpatch-1.21-2.el8.noarch.rpm                          28 kB/s |  27 kB     00:00    
(7/32): python3-netifaces-0.10.6-4.el8.x86_64.rpm                        20 kB/s |  25 kB     00:01    
(8/32): python3-pytz-2017.2-9.el8.noarch.rpm                             15 kB/s |  54 kB     00:03    
(9/32): python3-markupsafe-0.23-19.el8.x86_64.rpm                        41 kB/s |  39 kB     00:00    
(10/32): libmaxminddb-1.2.0-10.el8.x86_64.rpm                            22 kB/s |  33 kB     00:01    
(11/32): python3-jinja2-2.10.1-3.el8.noarch.rpm                         158 kB/s | 538 kB     00:03    
(12/32): python3-babel-2.5.1-7.el8.noarch.rpm                           867 kB/s | 4.8 MB     00:05    
(13/32): gdisk-1.0.3-6.el8.x86_64.rpm                                   178 kB/s | 239 kB     00:01    
(14/32): cloud-init-21.1-7.el8_5.5.noarch.rpm                           310 kB/s | 1.1 MB     00:03    
(15/32): python3-cffi-1.11.5-5.el8.x86_64.rpm                           146 kB/s | 238 kB     00:01    
(16/32): python3-pyyaml-3.12-12.el8.x86_64.rpm                           50 kB/s | 193 kB     00:03    
(17/32): python3-pycparser-2.14-14.el8.noarch.rpm                        57 kB/s | 109 kB     00:01    
(18/32): python3-oauthlib-2.1.0-1.el8.noarch.rpm                         87 kB/s | 155 kB     00:01    
(19/32): python3-jwt-1.6.1-2.el8.noarch.rpm                              32 kB/s |  43 kB     00:01    
(20/32): checkpolicy-2.9-1.el8.x86_64.rpm                               131 kB/s | 346 kB     00:02    
(21/32): ipcalc-0.2.4-4.el8.x86_64.rpm                                   14 kB/s |  38 kB     00:02    
(22/32): python3-audit-3.0-0.17.20191104git1c2f876.el8.x86_64.rpm        55 kB/s |  86 kB     00:01    
(23/32): python3-setools-4.3.0-2.el8.x86_64.rpm                         291 kB/s | 626 kB     00:02    
(24/32): python3-libsemanage-2.9-6.el8.x86_64.rpm                        82 kB/s | 127 kB     00:01    
(25/32): python3-ply-3.9-9.el8.noarch.rpm                                62 kB/s | 111 kB     00:01    
(26/32): dhcp-libs-4.3.6-45.el8.x86_64.rpm                               82 kB/s | 148 kB     00:01    
(27/32): dhcp-client-4.3.6-45.el8.x86_64.rpm                            164 kB/s | 318 kB     00:01    
(28/32): python3-cryptography-3.2.1-5.el8.x86_64.rpm                    267 kB/s | 559 kB     00:02    
(29/32): dhcp-common-4.3.6-45.el8.noarch.rpm                            119 kB/s | 207 kB     00:01    
(30/32): bind-export-libs-9.11.26-6.el8.x86_64.rpm                      321 kB/s | 1.1 MB     00:03    
(31/32): python3-policycoreutils-2.9-16.el8.noarch.rpm                  405 kB/s | 2.2 MB     00:05    
(32/32): geolite2-city-20180605-1.el8.noarch.rpm                        184 kB/s |  19 MB     01:45    
--------------------------------------------------------------------------------------------------------
Total                                                                   327 kB/s |  34 MB     01:45     
Red Hat Enterprise Linux 8 for x86_64 - AppStream (RPMs)                447 kB/s | 5.0 kB     00:00    
Importing GPG key 0xFD431D51:
 Userid     : "Red Hat, Inc. (release key 2) <security@redhat.com>"
 Fingerprint: 567E 347A D004 4ADE 55BA 8A5F 199E 2F91 FD43 1D51
 From       : /etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
Key imported successfully
Importing GPG key 0xD4082792:
 Userid     : "Red Hat, Inc. (auxiliary key) <security@redhat.com>"
 Fingerprint: 6A6A A7C9 7C88 90AE C6AE BFE2 F76F 66C3 D408 2792
 From       : /etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
Key imported successfully
Running transaction check
Transaction check succeeded.
Running transaction test
Transaction test succeeded.
Running transaction
  Preparing        :                                                                                1/1 
  Installing       : geolite2-country-20180605-1.el8.noarch                                        1/32 
  Installing       : geolite2-city-20180605-1.el8.noarch                                           2/32 
  Installing       : libmaxminddb-1.2.0-10.el8.x86_64                                              3/32 
  Running scriptlet: libmaxminddb-1.2.0-10.el8.x86_64                                              3/32 
  Installing       : ipcalc-0.2.4-4.el8.x86_64                                                     4/32 
  Installing       : bind-export-libs-32:9.11.26-6.el8.x86_64                                      5/32 
  Running scriptlet: bind-export-libs-32:9.11.26-6.el8.x86_64                                      5/32 
  Installing       : dhcp-common-12:4.3.6-45.el8.noarch                                            6/32 
  Installing       : dhcp-libs-12:4.3.6-45.el8.x86_64                                              7/32 
  Installing       : dhcp-client-12:4.3.6-45.el8.x86_64                                            8/32 
  Installing       : python3-ply-3.9-9.el8.noarch                                                  9/32 
  Installing       : python3-pycparser-2.14-14.el8.noarch                                         10/32 
  Installing       : python3-cffi-1.11.5-5.el8.x86_64                                             11/32 
  Installing       : python3-cryptography-3.2.1-5.el8.x86_64                                      12/32 
  Installing       : python3-jwt-1.6.1-2.el8.noarch                                               13/32 
  Installing       : python3-oauthlib-2.1.0-1.el8.noarch                                          14/32 
  Installing       : python3-libsemanage-2.9-6.el8.x86_64                                         15/32 
  Installing       : python3-setools-4.3.0-2.el8.x86_64                                           16/32 
  Installing       : python3-audit-3.0-0.17.20191104git1c2f876.el8.x86_64                         17/32 
  Installing       : checkpolicy-2.9-1.el8.x86_64                                                 18/32 
  Installing       : python3-policycoreutils-2.9-16.el8.noarch                                    19/32 
  Installing       : python3-pyyaml-3.12-12.el8.x86_64                                            20/32 
  Installing       : gdisk-1.0.3-6.el8.x86_64                                                     21/32 
  Installing       : python3-markupsafe-0.23-19.el8.x86_64                                        22/32 
  Installing       : python3-netifaces-0.10.6-4.el8.x86_64                                        23/32 
  Installing       : python3-pytz-2017.2-9.el8.noarch                                             24/32 
  Installing       : python3-babel-2.5.1-7.el8.noarch                                             25/32 
  Installing       : python3-jinja2-2.10.1-3.el8.noarch                                           26/32 
  Installing       : python3-jsonschema-2.6.0-4.el8.noarch                                        27/32 
  Installing       : python3-jsonpointer-1.10-11.el8.noarch                                       28/32 
  Installing       : python3-jsonpatch-1.21-2.el8.noarch                                          29/32 
  Installing       : python3-pyserial-3.1.1-8.el8.noarch                                          30/32 
  Installing       : python3-prettytable-0.7.2-14.el8.noarch                                      31/32 
  Installing       : cloud-init-21.1-7.el8_5.5.noarch                                             32/32 
  Running scriptlet: cloud-init-21.1-7.el8_5.5.noarch                                             32/32 
  Verifying        : python3-prettytable-0.7.2-14.el8.noarch                                       1/32 
  Verifying        : geolite2-city-20180605-1.el8.noarch                                           2/32 
  Verifying        : python3-pyserial-3.1.1-8.el8.noarch                                           3/32 
  Verifying        : python3-jsonpointer-1.10-11.el8.noarch                                        4/32 
  Verifying        : geolite2-country-20180605-1.el8.noarch                                        5/32 
  Verifying        : python3-jsonschema-2.6.0-4.el8.noarch                                         6/32 
  Verifying        : python3-pytz-2017.2-9.el8.noarch                                              7/32 
  Verifying        : python3-jsonpatch-1.21-2.el8.noarch                                           8/32 
  Verifying        : python3-netifaces-0.10.6-4.el8.x86_64                                         9/32 
  Verifying        : python3-markupsafe-0.23-19.el8.x86_64                                        10/32 
  Verifying        : libmaxminddb-1.2.0-10.el8.x86_64                                             11/32 
  Verifying        : python3-babel-2.5.1-7.el8.noarch                                             12/32 
  Verifying        : python3-jinja2-2.10.1-3.el8.noarch                                           13/32 
  Verifying        : cloud-init-21.1-7.el8_5.5.noarch                                             14/32 
  Verifying        : gdisk-1.0.3-6.el8.x86_64                                                     15/32 
  Verifying        : python3-pyyaml-3.12-12.el8.x86_64                                            16/32 
  Verifying        : python3-cffi-1.11.5-5.el8.x86_64                                             17/32 
  Verifying        : python3-pycparser-2.14-14.el8.noarch                                         18/32 
  Verifying        : python3-oauthlib-2.1.0-1.el8.noarch                                          19/32 
  Verifying        : python3-jwt-1.6.1-2.el8.noarch                                               20/32 
  Verifying        : checkpolicy-2.9-1.el8.x86_64                                                 21/32 
  Verifying        : ipcalc-0.2.4-4.el8.x86_64                                                    22/32 
  Verifying        : python3-audit-3.0-0.17.20191104git1c2f876.el8.x86_64                         23/32 
  Verifying        : python3-setools-4.3.0-2.el8.x86_64                                           24/32 
  Verifying        : python3-libsemanage-2.9-6.el8.x86_64                                         25/32 
  Verifying        : python3-ply-3.9-9.el8.noarch                                                 26/32 
  Verifying        : dhcp-libs-12:4.3.6-45.el8.x86_64                                             27/32 
  Verifying        : dhcp-client-12:4.3.6-45.el8.x86_64                                           28/32 
  Verifying        : python3-cryptography-3.2.1-5.el8.x86_64                                      29/32 
  Verifying        : dhcp-common-12:4.3.6-45.el8.noarch                                           30/32 
  Verifying        : bind-export-libs-32:9.11.26-6.el8.x86_64                                     31/32 
  Verifying        : python3-policycoreutils-2.9-16.el8.noarch                                    32/32 
Installed products updated.

Installed:
  bind-export-libs-32:9.11.26-6.el8.x86_64     checkpolicy-2.9-1.el8.x86_64                            
  cloud-init-21.1-7.el8_5.5.noarch             dhcp-client-12:4.3.6-45.el8.x86_64                      
  dhcp-common-12:4.3.6-45.el8.noarch           dhcp-libs-12:4.3.6-45.el8.x86_64                        
  gdisk-1.0.3-6.el8.x86_64                     geolite2-city-20180605-1.el8.noarch                     
  geolite2-country-20180605-1.el8.noarch       ipcalc-0.2.4-4.el8.x86_64                               
  libmaxminddb-1.2.0-10.el8.x86_64             python3-audit-3.0-0.17.20191104git1c2f876.el8.x86_64    
  python3-babel-2.5.1-7.el8.noarch             python3-cffi-1.11.5-5.el8.x86_64                        
  python3-cryptography-3.2.1-5.el8.x86_64      python3-jinja2-2.10.1-3.el8.noarch                      
  python3-jsonpatch-1.21-2.el8.noarch          python3-jsonpointer-1.10-11.el8.noarch                  
  python3-jsonschema-2.6.0-4.el8.noarch        python3-jwt-1.6.1-2.el8.noarch                          
  python3-libsemanage-2.9-6.el8.x86_64         python3-markupsafe-0.23-19.el8.x86_64                   
  python3-netifaces-0.10.6-4.el8.x86_64        python3-oauthlib-2.1.0-1.el8.noarch                     
  python3-ply-3.9-9.el8.noarch                 python3-policycoreutils-2.9-16.el8.noarch               
  python3-prettytable-0.7.2-14.el8.noarch      python3-pycparser-2.14-14.el8.noarch                    
  python3-pyserial-3.1.1-8.el8.noarch          python3-pytz-2017.2-9.el8.noarch                        
  python3-pyyaml-3.12-12.el8.x86_64            python3-setools-4.3.0-2.el8.x86_64                      

Complete!
```

</details>

然后使用良心云提供的`cloud.cfg`替代原有的

<details><summary>点击此处 ← 查看折叠</summary>

``` bash
[root@UPS-PC home]# cat /etc/cloud/cloud.cfg
users:
 - default

disable_root: 1
ssh_pwauth:   0

mount_default_fields: [~, ~, 'auto', 'defaults,nofail,x-systemd.requires=cloud-init.service', '0', '2']
resize_rootfs_tmp: /dev
ssh_deletekeys:   1
ssh_genkeytypes:  ['rsa', 'ecdsa', 'ed25519']
syslog_fix_perms: ~
disable_vmware_customization: false

cloud_init_modules:
 - disk_setup
 - migrator
 - bootcmd
 - write-files
 - growpart
 - resizefs
 - set_hostname
 - update_hostname
 - update_etc_hosts
 - rsyslog
 - users-groups
 - ssh

cloud_config_modules:
 - mounts
 - locale
 - set-passwords
 - rh_subscription
 - yum-add-repo
 - package-update-upgrade-install
 - timezone
 - puppet
 - chef
 - salt-minion
 - mcollective
 - disable-ec2-metadata
 - runcmd

cloud_final_modules:
 - rightscale_userdata
 - scripts-per-once
 - scripts-per-boot
 - scripts-per-instance
 - scripts-user
 - ssh-authkey-fingerprints
 - keys-to-console
 - phone-home
 - final-message
 - power-state-change

system_info:
  default_user:
    name: cloud-user
    lock_passwd: true
    gecos: Cloud User
    groups: [adm, systemd-journal]
    sudo: ["ALL=(ALL) NOPASSWD:ALL"]
    shell: /bin/bash
  distro: rhel
  paths:
    cloud_dir: /var/lib/cloud
    templates_dir: /etc/cloud/templates
  ssh_svcname: sshd
```

</details>

<details><summary>点击此处 ← 查看折叠</summary>

``` bash
[root@UPS-PC home]# echo '' > /etc/cloud/cloud.cfg
[root@UPS-PC home]# vi /etc/cloud/cloud.cfg
[root@UPS-PC home]# cat /etc/cloud/cloud.cfg
users:
 - default

disable_root: 0
ssh_pwauth:   1

datasource_list: [ ConfigDrive, TencentCloud ]
datasource:
  ConfigDrive:
    dsmode: local
  TencentCloud:
    metadata_urls: ['http://metadata.tencentyun.com']

cloud_init_modules:
 - migrator
 - bootcmd
 - write-files
 - growpart
 - resizefs
 - set_hostname
 - update_hostname
 - ['update_etc_hosts', 'once-per-instance']
 - rsyslog
 - users-groups
 - ssh

cloud_config_modules:
 - mounts
 - locale
 - set-passwords
 - rh_subscription
 - yum-add-repo
 - package-update-upgrade-install
 - ntp
 - timezone
 - resolv_conf
 - puppet
 - chef
 - salt-minion
 - mcollective
 - disable-ec2-metadata
 - runcmd

unverified_modules: ['resolv_conf']

cloud_final_modules:
 - rightscale_userdata
 - scripts-per-once
 - scripts-per-boot
 - scripts-per-instance
 - scripts-user
 - ssh-authkey-fingerprints
 - keys-to-console
 - phone-home
 - final-message
 - power-state-change

system_info:
  default_user:
    name: root
    lock_passwd: false
    gecos: Cloud User
    groups: [wheel, adm, systemd-journal]
    sudo: ["ALL=(ALL) NOPASSWD:ALL"]
    shell: /bin/bash
  distro: rhel
  paths:
    cloud_dir: /var/lib/cloud
    templates_dir: /etc/cloud/templates
  ssh_svcname: sshd
```

</details>

执行`init`检查相关配置是否成功，然后删掉缓存记录
``` bash
[root@UPS-PC ~]# cloud-init init --local
Cloud-init v. 21.1-7.el8_5.5 running 'init-local' at Sun, 08 May 2022 16:25:49 +0000. Up 11883.54 seconds.
[root@UPS-PC ~]# rm -rf /var/lib/cloud
```

**得益于良心云文档的排版错误，差点儿错过三个步骤草**
- 首先是添加`syslog`用户：`useradd syslog`
- 然后是修改服务单元文件

<details><summary>点击此处 ← 查看折叠</summary>

``` bash
[root@UPS-PC home]# cat /lib/systemd/system/cloud-init-local.service
[Unit]
Description=Initial cloud-init job (pre-networking)
DefaultDependencies=no
Wants=network-pre.target
After=systemd-remount-fs.service
Requires=dbus.socket
After=dbus.socket
Before=NetworkManager.service network.service
Before=network-pre.target
Before=shutdown.target
Before=firewalld.target
Conflicts=shutdown.target
RequiresMountsFor=/var/lib/cloud
ConditionPathExists=!/etc/cloud/cloud-init.disabled
ConditionKernelCommandLine=!cloud-init=disabled

[Service]
Type=oneshot
ExecStartPre=/bin/mkdir -p /run/cloud-init
ExecStartPre=/sbin/restorecon /run/cloud-init
ExecStartPre=/usr/bin/touch /run/cloud-init/enabled
ExecStart=/usr/bin/cloud-init init --local
ExecStart=/bin/touch /run/cloud-init/network-config-ready
RemainAfterExit=yes
TimeoutSec=0

# Output needs to appear in instance console output
StandardOutput=journal+console

[Install]
WantedBy=cloud-init.target
[root@UPS-PC home]# cat /lib/systemd/system/cloud-init.service
[Unit]
Description=Initial cloud-init job (metadata service crawler)
Wants=cloud-init-local.service
Wants=sshd-keygen.service
Wants=sshd.service
After=cloud-init-local.service
After=NetworkManager.service network.service
After=NetworkManager-wait-online.service
Before=network-online.target
Before=sshd-keygen.service
Before=sshd.service
Before=systemd-user-sessions.service
ConditionPathExists=!/etc/cloud/cloud-init.disabled
ConditionKernelCommandLine=!cloud-init=disabled

[Service]
Type=oneshot
ExecStart=/usr/bin/cloud-init init
RemainAfterExit=yes
TimeoutSec=0

# Output needs to appear in instance console output
StandardOutput=journal+console

[Install]
WantedBy=cloud-init.target
[root@UPS-PC ~]# cp /lib/systemd/system/cloud-init-local.service /lib/systemd/system/cloud-init-local.service.bak
[root@UPS-PC ~]# echo '' > /lib/systemd/system/cloud-init-local.service
[root@UPS-PC ~]# vi /lib/systemd/system/cloud-init-local.service
[root@UPS-PC ~]# cat /lib/systemd/system/cloud-init-local.service
[Unit]
Description=Initial cloud-init job (pre-networking)
Wants=network-pre.target
After=systemd-remount-fs.service
Before=NetworkManager.service
Before=network-pre.target
Before=shutdown.target
Conflicts=shutdown.target
RequiresMountsFor=/var/lib/cloud
[Service]
Type=oneshot
ExecStart=/usr/bin/cloud-init init --local
ExecStart=/bin/touch /run/cloud-init/network-config-ready
RemainAfterExit=yes
TimeoutSec=0
# Output needs to appear in instance console output
StandardOutput=journal+console
[Install]
WantedBy=cloud-init.target
[root@UPS-PC ~]# cp /lib/systemd/system/cloud-init.service /lib/systemd/system/cloud-init.service.bak
[root@UPS-PC ~]# vi /lib/systemd/system/cloud-init.service
[root@UPS-PC ~]# echo '' > /lib/systemd/system/cloud-init.service
[root@UPS-PC ~]# vi /lib/systemd/system/cloud-init.service
[root@UPS-PC ~]# cat /lib/systemd/system/cloud-init.service
[Unit]
Description=Initial cloud-init job (metadata service crawler)
Wants=cloud-init-local.service
Wants=sshd-keygen.service
Wants=sshd.service
After=cloud-init-local.service
After=systemd-networkd-wait-online.service
After=networking.service
After=systemd-hostnamed.service
Before=network-online.target
Before=sshd-keygen.service
Before=sshd.service
Before=systemd-user-sessions.service
Conflicts=shutdown.target
[Service]
Type=oneshot
ExecStart=/usr/bin/cloud-init init
RemainAfterExit=yes
TimeoutSec=0
# Output needs to appear in instance console output
StandardOutput=journal+console
[Install]
WantedBy=cloud-init.target
```

</details>

- 最后配置服务自启动

<details><summary>点击此处 ← 查看折叠</summary>

``` bash
[root@UPS-PC home]# systemctl status cloud-init-local
● cloud-init-local.service - Initial cloud-init job (pre-networking)
   Loaded: loaded (/usr/lib/systemd/system/cloud-init-local.service; enabled; vendor preset: disabled)
   Active: inactive (dead)
[root@UPS-PC home]# systemctl status cloud-init
● cloud-init.service - Initial cloud-init job (metadata service crawler)
   Loaded: loaded (/usr/lib/systemd/system/cloud-init.service; enabled; vendor preset: disabled)
   Active: inactive (dead)
[root@UPS-PC home]# systemctl status cloud-config
● cloud-config.service - Apply the settings specified in cloud-config
   Loaded: loaded (/usr/lib/systemd/system/cloud-config.service; enabled; vendor preset: disabled)
   Active: inactive (dead)
[root@UPS-PC home]# systemctl status cloud-final
● cloud-final.service - Execute cloud user/final scripts
   Loaded: loaded (/usr/lib/systemd/system/cloud-final.service; enabled; vendor preset: disabled)
   Active: inactive (dead)
[root@UPS-PC home]# systemctl enable cloud-init-local.service 
[root@UPS-PC home]# systemctl start cloud-init-local.service
[root@UPS-PC home]# systemctl enable cloud-init.service
[root@UPS-PC home]# systemctl start cloud-init.service
[root@UPS-PC home]# systemctl enable cloud-config.service
[root@UPS-PC home]# systemctl start cloud-config.service
[root@UPS-PC home]# systemctl enable cloud-final.service
[root@UPS-PC home]# systemctl start cloud-final.service
```

</details>

### 7. 确认木有`VMware tools`
结果发现还真有，`vCenter`这么快就给装上了……
``` bash
[root@UPS-PC home]# ps aux | grep vmtool
root        1073  0.0  0.1 278356 10792 ?        Ssl  21:07   0:02 /usr/bin/vmtoolsd
root       24041  0.0  0.0  12136  1160 pts/0    S+   21:57   0:00 grep --color=auto vmtool
```
不过是`open-vm-tools`而不是通过`.pl`脚本安装的

<details><summary>点击此处 ← 查看折叠</summary>

``` bash
[root@UPS-PC home]# find / -name 'vmware-uninstall-tools.p'
[root@UPS-PC home]# ./vmware-uninstall-tools.pl
-bash: ./vmware-uninstall-tools.pl: No such file or directory
[root@UPS-PC home]# rpm -qa | grep vm
lvm2-libs-2.03.12-10.el8.x86_64
ima-evm-utils-1.3.2-12.el8.x86_64
open-vm-tools-11.2.5-2.el8.x86_64
lvm2-2.03.12-10.el8.x86_64
[root@UPS-PC home]# yum remove open-vm-tools -y
Updating Subscription Management repositories.
Dependencies resolved.
========================================================================================================
 Package                   Architecture     Version                          Repository            Size
========================================================================================================
Removing:
 open-vm-tools             x86_64           11.2.5-2.el8                     @AppStream           2.6 M
Removing unused dependencies:
 fuse                      x86_64           2.9.7-12.el8                     @anaconda            206 k
 fuse-common               x86_64           3.2.1-12.el8                     @anaconda            4.7 k
 libdrm                    x86_64           2.4.106-2.el8                    @AppStream           385 k
 libmspack                 x86_64           0.7-0.3.alpha.el8.4              @AppStream           132 k
 libpciaccess              x86_64           0.14-1.el8                       @anaconda             48 k
 libtool-ltdl              x86_64           2.4.6-25.el8                     @anaconda             69 k
 libxslt                   x86_64           1.1.32-6.el8                     @anaconda            734 k
 tar                       x86_64           2:1.30-5.el8                     @anaconda            2.7 M
 xmlsec1                   x86_64           1.2.25-4.el8                     @AppStream           595 k
 xmlsec1-openssl           x86_64           1.2.25-4.el8                     @AppStream           286 k

Transaction Summary
========================================================================================================
Remove  11 Packages

Freed space: 7.8 M
Running transaction check
Transaction check succeeded.
Running transaction test
Transaction test succeeded.
Running transaction
  Preparing        :                                                                                1/1 
  Running scriptlet: open-vm-tools-11.2.5-2.el8.x86_64                                              1/1 
  Running scriptlet: open-vm-tools-11.2.5-2.el8.x86_64                                             1/11 
  Erasing          : open-vm-tools-11.2.5-2.el8.x86_64                                             1/11 
  Running scriptlet: open-vm-tools-11.2.5-2.el8.x86_64                                             1/11 
  Erasing          : xmlsec1-openssl-1.2.25-4.el8.x86_64                                           2/11 
  Erasing          : xmlsec1-1.2.25-4.el8.x86_64                                                   3/11 
  Erasing          : fuse-2.9.7-12.el8.x86_64                                                      4/11 
  Erasing          : libdrm-2.4.106-2.el8.x86_64                                                   5/11 
  Erasing          : fuse-common-3.2.1-12.el8.x86_64                                               6/11 
  Erasing          : libpciaccess-0.14-1.el8.x86_64                                                7/11 
  Erasing          : libtool-ltdl-2.4.6-25.el8.x86_64                                              8/11 
  Running scriptlet: libtool-ltdl-2.4.6-25.el8.x86_64                                              8/11 
  Erasing          : libxslt-1.1.32-6.el8.x86_64                                                   9/11 
  Erasing          : libmspack-0.7-0.3.alpha.el8.4.x86_64                                         10/11 
  Running scriptlet: tar-2:1.30-5.el8.x86_64                                                      11/11 
  Erasing          : tar-2:1.30-5.el8.x86_64                                                      11/11 
  Running scriptlet: tar-2:1.30-5.el8.x86_64                                                      11/11 
  Verifying        : fuse-2.9.7-12.el8.x86_64                                                      1/11 
  Verifying        : fuse-common-3.2.1-12.el8.x86_64                                               2/11 
  Verifying        : libdrm-2.4.106-2.el8.x86_64                                                   3/11 
  Verifying        : libmspack-0.7-0.3.alpha.el8.4.x86_64                                          4/11 
  Verifying        : libpciaccess-0.14-1.el8.x86_64                                                5/11 
  Verifying        : libtool-ltdl-2.4.6-25.el8.x86_64                                              6/11 
  Verifying        : libxslt-1.1.32-6.el8.x86_64                                                   7/11 
  Verifying        : open-vm-tools-11.2.5-2.el8.x86_64                                             8/11 
  Verifying        : tar-2:1.30-5.el8.x86_64                                                       9/11 
  Verifying        : xmlsec1-1.2.25-4.el8.x86_64                                                  10/11 
  Verifying        : xmlsec1-openssl-1.2.25-4.el8.x86_64                                          11/11 
Installed products updated.

Removed:
  fuse-2.9.7-12.el8.x86_64                           fuse-common-3.2.1-12.el8.x86_64                    
  libdrm-2.4.106-2.el8.x86_64                        libmspack-0.7-0.3.alpha.el8.4.x86_64               
  libpciaccess-0.14-1.el8.x86_64                     libtool-ltdl-2.4.6-25.el8.x86_64                   
  libxslt-1.1.32-6.el8.x86_64                        open-vm-tools-11.2.5-2.el8.x86_64                  
  tar-2:1.30-5.el8.x86_64                            xmlsec1-1.2.25-4.el8.x86_64                        
  xmlsec1-openssl-1.2.25-4.el8.x86_64               

Complete!
```

</details>

### 8. 确认分区和大小
``` bash
[root@UPS-PC home]# mount
sysfs on /sys type sysfs (rw,nosuid,nodev,noexec,relatime,seclabel)
proc on /proc type proc (rw,nosuid,nodev,noexec,relatime)
devtmpfs on /dev type devtmpfs (rw,nosuid,seclabel,size=3957708k,nr_inodes=989427,mode=755)
securityfs on /sys/kernel/security type securityfs (rw,nosuid,nodev,noexec,relatime)
tmpfs on /dev/shm type tmpfs (rw,nosuid,nodev,seclabel)
devpts on /dev/pts type devpts (rw,nosuid,noexec,relatime,seclabel,gid=5,mode=620,ptmxmode=000)
tmpfs on /run type tmpfs (rw,nosuid,nodev,seclabel,mode=755)
tmpfs on /sys/fs/cgroup type tmpfs (ro,nosuid,nodev,noexec,seclabel,mode=755)
cgroup on /sys/fs/cgroup/systemd type cgroup (rw,nosuid,nodev,noexec,relatime,seclabel,xattr,release_agent=/usr/lib/systemd/systemd-cgroups-agent,name=systemd)
pstore on /sys/fs/pstore type pstore (rw,nosuid,nodev,noexec,relatime,seclabel)
bpf on /sys/fs/bpf type bpf (rw,nosuid,nodev,noexec,relatime,mode=700)
cgroup on /sys/fs/cgroup/net_cls,net_prio type cgroup (rw,nosuid,nodev,noexec,relatime,seclabel,net_cls,net_prio)
cgroup on /sys/fs/cgroup/memory type cgroup (rw,nosuid,nodev,noexec,relatime,seclabel,memory)
cgroup on /sys/fs/cgroup/pids type cgroup (rw,nosuid,nodev,noexec,relatime,seclabel,pids)
cgroup on /sys/fs/cgroup/perf_event type cgroup (rw,nosuid,nodev,noexec,relatime,seclabel,perf_event)
cgroup on /sys/fs/cgroup/cpuset type cgroup (rw,nosuid,nodev,noexec,relatime,seclabel,cpuset)
cgroup on /sys/fs/cgroup/blkio type cgroup (rw,nosuid,nodev,noexec,relatime,seclabel,blkio)
cgroup on /sys/fs/cgroup/cpu,cpuacct type cgroup (rw,nosuid,nodev,noexec,relatime,seclabel,cpu,cpuacct)
cgroup on /sys/fs/cgroup/rdma type cgroup (rw,nosuid,nodev,noexec,relatime,seclabel,rdma)
cgroup on /sys/fs/cgroup/freezer type cgroup (rw,nosuid,nodev,noexec,relatime,seclabel,freezer)
cgroup on /sys/fs/cgroup/hugetlb type cgroup (rw,nosuid,nodev,noexec,relatime,seclabel,hugetlb)
cgroup on /sys/fs/cgroup/devices type cgroup (rw,nosuid,nodev,noexec,relatime,seclabel,devices)
none on /sys/kernel/tracing type tracefs (rw,relatime,seclabel)
configfs on /sys/kernel/config type configfs (rw,relatime)
/dev/mapper/rhel-root on / type xfs (rw,relatime,seclabel,attr2,inode64,logbufs=8,logbsize=32k,noquota)
selinuxfs on /sys/fs/selinux type selinuxfs (rw,relatime)
mqueue on /dev/mqueue type mqueue (rw,relatime,seclabel)
hugetlbfs on /dev/hugepages type hugetlbfs (rw,relatime,seclabel,pagesize=2M)
debugfs on /sys/kernel/debug type debugfs (rw,relatime,seclabel)
systemd-1 on /proc/sys/fs/binfmt_misc type autofs (rw,relatime,fd=40,pgrp=1,timeout=0,minproto=5,maxproto=5,direct,pipe_ino=14728)
fusectl on /sys/fs/fuse/connections type fusectl (rw,relatime)
/dev/sda1 on /boot type xfs (rw,relatime,seclabel,attr2,inode64,logbufs=8,logbsize=32k,noquota)
tmpfs on /run/user/0 type tmpfs (rw,nosuid,nodev,relatime,seclabel,size=795364k,mode=700)
binfmt_misc on /proc/sys/fs/binfmt_misc type binfmt_misc (rw,relatime)
tracefs on /sys/kernel/debug/tracing type tracefs (rw,relatime,seclabel)
```

### 9. 更改网络端口到`eth0`
> 网卡更换为`Virtio Nic`，默认只提供`eth0`

良心云文档中并没有写，参考前人在`GRUB_CMDLINE_LINUX`追加`net.ifnames=0 biosdevname=0`
``` bash
[root@UPS-PC home]# cat /etc/default/grub
GRUB_TIMEOUT=5
GRUB_DISTRIBUTOR="$(sed 's, release .*$,,g' /etc/system-release)"
GRUB_DEFAULT=saved
GRUB_DISABLE_SUBMENU=true
GRUB_TERMINAL_OUTPUT="console"
GRUB_CMDLINE_LINUX="crashkernel=auto resume=/dev/mapper/rhel-swap rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap rhgb quiet"
GRUB_DISABLE_RECOVERY="true"
GRUB_ENABLE_BLSCFG=true
[root@UPS-PC home]# vi /etc/default/grub
[root@UPS-PC home]# cat /etc/default/grub
GRUB_TIMEOUT=5
GRUB_DISTRIBUTOR="$(sed 's, release .*$,,g' /etc/system-release)"
GRUB_DEFAULT=saved
GRUB_DISABLE_SUBMENU=true
GRUB_TERMINAL_OUTPUT="console"
GRUB_CMDLINE_LINUX="crashkernel=auto resume=/dev/mapper/rhel-swap rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap rhgb quiet net.ifnames=0 biosdevname=0"
GRUB_DISABLE_RECOVERY="true"
GRUB_ENABLE_BLSCFG=true
```
然后重新编译`GRUB`启动配置
``` bash
[root@UPS-PC home]# grub2-mkconfig -o /boot/grub2/grub.cfg
Generating grub configuration file ...
done
```
最后修改网卡配置文件，并重命名`ifcfg-ens192`至`ifcfg-eth0`
``` bash
[root@UPS-PC home]# cat /etc/sysconfig/network-scripts/ifcfg-ens192 
# Created by cloud-init on instance boot automatically, do not edit.
#
BOOTPROTO=dhcp
DEVICE=ens192
HWADDR=00:50:56:ba:56:32
ONBOOT=yes
TYPE=Ethernet
USERCTL=no
[root@UPS-PC home]# vi /etc/sysconfig/network-scripts/ifcfg-ens192 
[root@UPS-PC home]# mv /etc/sysconfig/network-scripts/ifcfg-ens192 /etc/sysconfig/network-scripts/ifcfg-eth0
[root@UPS-PC home]# cat /etc/sysconfig/network-scripts/ifcfg-eth0 
# Created by cloud-init on instance boot automatically, do not edit.
#
BOOTPROTO=dhcp
DEVICE=eth0
HWADDR=00:50:56:ba:56:32
ONBOOT=yes
TYPE=Ethernet
USERCTL=no
```
至此终于搞完一半了，然后关机，导出`OVF`模板，上传`VMDK`至`COS`，最后导入自定义镜像
本来以为不需要等待多久，结果过了一会儿还没完成不打算等了，没想到的是电脑关机后刚上床就导入完成了草[#108267441787923547](https://mastodon.yuangezhizao.cn/@yuangezhizao/108267441787923547)，只能白天继续来搞了……
> 此章节时间线[#108266452237726140](https://mastodon.yuangezhizao.cn/@yuangezhizao/108266452237726140)

## 0x03.`cn-tx-bj1-r8`
另一半则是开始着手重装`cn-tx-bj1-c8`的系统，终于可以使用自己制作的`rhel-85-x86-64-minimal`自定义镜像来安装了，成功启动！
![Ootpa](https://mastodon-1251901037.cos.ap-beijing.myqcloud.com/media_attachments/files/108/271/392/389/124/755/original/de5a5469a0b2d090.png)

虽然看到`cloud-init`还是报了`DNS`解析失败等错误，但是毕竟系统起来了可以后期慢慢修，并不知道会有多少坑等着呢……
然后的`Linux`云主机初始化操作就异常娴熟了，简单列几点吧~

1. 修改`hostname`等待重启
``` bash
[root@VM-32-113-centos ~]# vi /etc/hosts
[root@VM-32-113-centos ~]# cat /etc/hosts
# Your system has configured 'manage_etc_hosts' as True.
# As a result, if you wish for changes to this file to persist
# then you will need to either
# a.) make changes to the master file in /etc/cloud/templates/hosts.redhat.tmpl
# b.) change or remove the value of 'manage_etc_hosts' in
#     /etc/cloud/cloud.cfg or cloud-config from user-data
# 
# The following lines are desirable for IPv4 capable hosts
127.0.0.1 cn-tx-bj1-r8 cn-tx-bj1-r8
127.0.0.1 localhost.localdomain localhost
127.0.0.1 localhost4.localdomain4 localhost4

# The following lines are desirable for IPv6 capable hosts
::1 cn-tx-bj1-r8 cn-tx-bj1-r8
::1 localhost.localdomain localhost
::1 localhost6.localdomain6 localhost6
[root@VM-32-113-centos ~]# hostnamectl set-hostname cn-tx-bj1-r8
[root@VM-32-113-centos ~]# hostnamectl status
   Static hostname: cn-tx-bj1-r8
         Icon name: computer-vm
           Chassis: vm
        Machine ID: 0ba7a84d83404f9db63783a17f5fb6b1
           Boot ID: b4668c56ec7a486b9d0992f03d795309
    Virtualization: kvm
  Operating System: Red Hat Enterprise Linux 8.5 (Ootpa)
       CPE OS Name: cpe:/o:redhat:enterprise_linux:8::baseos
            Kernel: Linux 4.18.0-348.el8.x86_64
      Architecture: x86-64
```

2. 配置`SELINUX`为`permissive`模式，执行重启
``` bash
[root@VM-32-113-centos ~]# vi /etc/selinux/config
[root@VM-32-113-centos ~]# cat /etc/selinux/config

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
```

3. 修改`SSH`端口非`22`，并放通防火墙，配置`fail2ban`保护`sshd`服务
``` bash
[root@cn-tx-bj1-r8 ~]# firewall-cmd --add-port=<rm>/tcp
success
[root@cn-tx-bj1-r8 ~]# firewall-cmd --runtime-to-permanent
success
[root@cn-tx-bj1-r8 ~]# firewall-cmd --list-ports
<rm>/tcp
```

4. 试了一下可以直接访问红帽的源，但毕竟更换了环境还是重新注册下吧，可以看出系统`UUID`没有变化，暂时不需要重新生成
``` bash
[root@cn-tx-bj1-r8 ~]# subscription-manager register --username <rm> --password <rm> 
This system is already registered. Use --force to override
[root@cn-tx-bj1-r8 ~]# subscription-manager register --username <rm> --password <rm> --force
Unregistering from: subscription.rhsm.redhat.com:443/subscription
The system with UUID 5ad1c54f-024a-4445-b670-4be086022637 has been unregistered
All local data removed
Registering to: subscription.rhsm.redhat.com:443/subscription
The system has been registered with ID: 82cad6a2-54c5-427b-8df5-ea230fec0ca4
The registered system name is: cn-tx-bj1-r8
[root@cn-tx-bj1-r8 ~]# subscription-manager attach --auto
```

5. 最后查看内存占用，`used`部分并没有比`Debain`更省内存？
``` bash
[root@cn-tx-bj1-r8 ~]# free -h
              total        used        free      shared  buff/cache   available
Mem:          1.8Gi       152Mi       1.2Gi       9.0Mi       383Mi       1.5Gi
Swap:         1.0Gi          0B       1.0Gi
```

6. 扩充磁盘空间，可以看到是`xfs`而不是`ext4`的格式，且`/`挂载点只占用了`8.6G`，加上`/boot`挂载点的`1.1G`接近当初分配的`10G`大小
``` bash
[root@cn-tx-bj1-r8 ~]# fdisk -l
Disk /dev/vda: 50 GiB, 53687091200 bytes, 104857600 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x0d2cab79

Device     Boot   Start      End  Sectors Size Id Type
/dev/vda1  *       2048  2099199  2097152   1G 83 Linux
/dev/vda2       2099200 20971519 18872320   9G 8e Linux LVM


Disk /dev/mapper/rhel-root: 8 GiB, 8585740288 bytes, 16769024 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes


Disk /dev/mapper/rhel-swap: 1 GiB, 1073741824 bytes, 2097152 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
[root@cn-tx-bj1-r8 ~]# df -TH
Filesystem            Type      Size  Used Avail Use% Mounted on
devtmpfs              devtmpfs  935M     0  935M   0% /dev
tmpfs                 tmpfs     953M   25k  953M   1% /dev/shm
tmpfs                 tmpfs     953M   68M  886M   8% /run
tmpfs                 tmpfs     953M     0  953M   0% /sys/fs/cgroup
/dev/mapper/rhel-root xfs       8.6G  2.4G  6.3G  28% /
/dev/vda1             xfs       1.1G  220M  845M  21% /boot
tmpfs                 tmpfs     191M     0  191M   0% /run/user/0
```
可以看出`/`挂载点在`vda2`下，再分成了`rhel-root`和`rhel-swap`，也就是说需要扩充的是`vda2`
``` bash
[root@cn-tx-bj1-r8 ~]# dnf install -y cloud-utils-growpart
[root@cn-tx-bj1-r8 ~]# lsblk
NAME          MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sr0            11:0    1 154.5M  0 rom  
vda           252:0    0    50G  0 disk 
├─vda1        252:1    0     1G  0 part /boot
└─vda2        252:2    0     9G  0 part 
  ├─rhel-root 253:0    0     8G  0 lvm  /
  └─rhel-swap 253:1    0     1G  0 lvm  [SWAP]
```
尝试使用`growpart`和`resize2fs`，果不其然`resize2fs`报错了
``` bash
[root@cn-tx-bj1-r8 ~]# growpart /dev/vda 2
CHANGED: partition=2 start=2099200 old: size=18872320 end=20971520 new: size=102758367 end=104857567
[root@cn-tx-bj1-r8 ~]# resize2fs /dev/vda2
resize2fs 1.45.6 (20-Mar-2020)
resize2fs: Device or resource busy while trying to open /dev/vda2
Couldn\'t find valid filesystem superblock.
```
切换成针对`xfs`的命令`xfs_growfs`
``` bash
[root@cn-tx-bj1-r8 ~]# xfs_growfs /dev/mapper/rhel-root
meta-data=/dev/mapper/rhel-root  isize=512    agcount=4, agsize=524032 blks
         =                       sectsz=512   attr=2, projid32bit=1
         =                       crc=1        finobt=1, sparse=1, rmapbt=0
         =                       reflink=1
data     =                       bsize=4096   blocks=2096128, imaxpct=25
         =                       sunit=0      swidth=0 blks
naming   =version 2              bsize=4096   ascii-ci=0, ftype=1
log      =internal log           bsize=4096   blocks=2560, version=2
         =                       sectsz=512   sunit=0 blks, lazy-count=1
realtime =none                   extsz=4096   blocks=0, rtextents=0
[root@cn-tx-bj1-r8 ~]# growpart /dev/vda 2
NOCHANGE: partition 2 is size 102758367. it cannot be grown
[root@cn-tx-bj1-r8 ~]# pvresize /dev/vda2
  Physical volume "/dev/vda2" changed
  1 physical volume(s) resized or updated / 0 physical volume(s) not resized
[root@cn-tx-bj1-r8 ~]# pvdisplay
  --- Physical volume ---
  PV Name               /dev/vda2
  VG Name               rhel
  PV Size               <49.00 GiB / not usable 1.98 MiB
  Allocatable           yes 
  PE Size               4.00 MiB
  Total PE              12543
  Free PE               10240
  Allocated PE          2303
  PV UUID               qX1P1B-rFi8-BEIf-heEk-KJj6-iGfD-8TBntG
[root@cn-tx-bj1-r8 ~]# vgdisplay
  --- Volume group ---
  VG Name               rhel
  System ID             
  Format                lvm2
  Metadata Areas        1
  Metadata Sequence No  5
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                2
  Open LV               2
  Max PV                0
  Cur PV                1
  Act PV                1
  VG Size               <49.00 GiB
  PE Size               4.00 MiB
  Total PE              12543
  Alloc PE / Size       2303 / <9.00 GiB
  Free  PE / Size       10240 / 40.00 GiB
  VG UUID               XJ5ttD-HFOy-M01d-pJKw-CqK0-tkFL-nSSPKv
[root@cn-tx-bj1-r8 ~]# lvextend -l +100%FREE /dev/mapper/rhel-root
  Size of logical volume rhel/root changed from <8.00 GiB (2047 extents) to <48.00 GiB (12287 extents).
  Logical volume rhel/root successfully resized.
[root@cn-tx-bj1-r8 ~]# xfs_growfs /dev/mapper/rhel-root
meta-data=/dev/mapper/rhel-root  isize=512    agcount=4, agsize=524032 blks
         =                       sectsz=512   attr=2, projid32bit=1
         =                       crc=1        finobt=1, sparse=1, rmapbt=0
         =                       reflink=1
data     =                       bsize=4096   blocks=2096128, imaxpct=25
         =                       sunit=0      swidth=0 blks
naming   =version 2              bsize=4096   ascii-ci=0, ftype=1
log      =internal log           bsize=4096   blocks=2560, version=2
         =                       sectsz=512   sunit=0 blks, lazy-count=1
realtime =none                   extsz=4096   blocks=0, rtextents=0
data blocks changed from 2096128 to 12581888
```
再次查看大小，已经成功了，变成`52G`了
``` bash
[root@cn-tx-bj1-r8 ~]# df -TH
Filesystem            Type      Size  Used Avail Use% Mounted on
devtmpfs              devtmpfs  935M     0  935M   0% /dev
tmpfs                 tmpfs     953M   25k  953M   1% /dev/shm
tmpfs                 tmpfs     953M   68M  886M   8% /run
tmpfs                 tmpfs     953M     0  953M   0% /sys/fs/cgroup
/dev/mapper/rhel-root xfs        52G  2.7G   49G   6% /
/dev/vda1             xfs       1.1G  220M  845M  21% /boot
tmpfs                 tmpfs     191M     0  191M   0% /run/user/0
```

> 此章节时间线[#108271381980874897](https://mastodon.yuangezhizao.cn/@yuangezhizao/108271381980874897)

## 0x04.后记
`cn-py-dl-r8`→`cn-tx-bj1-r8`终于搞定了，最后删除`cn-py-dl-r8`[#108271667122964721](https://mastodon.yuangezhizao.cn/@yuangezhizao/108271667122964721)，完结撒花🎉🎉🎉

## 0x05.引用
[使用growpart扩容CentOS虚拟机磁盘](https://web.archive.org/web/20220513075449/https://www.cnblogs.com/sanduzxcvbnm/p/13998085.html)
[安装云服务器监控组件](https://cloud.tencent.com/document/product/248/6211)
[云服务器无监控数据](https://cloud.tencent.com/document/product/248/44702)
[获取内网 IP 地址和设置 DNS](https://cloud.tencent.com/document/product/213/17941)

> 至此本文使命完成
