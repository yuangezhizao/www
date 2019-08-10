---
title: 重装系统之 Skysilk CentOS 7 安装 v2ray 代理等
date: 2019-5-12 20:53:55
tags:
  - CentOS
  - server
count: 1
os: 0
os_1: 10.0.17763.475 2019-LTSC
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

## 0x02.~~[V2ray.Fun](https://github.com/FunctionClub/V2ray.Fun)~~[V2ray](https://github.com/v2ray/v2ray-core)
看了下手册，其实只需要`bash <(curl -L -s https://install.direct/go.sh)`，之后记好`PORT`&`UUID`即可
``` bash
[root@CentOS ~]# bash <(curl -L -s https://install.direct/go.sh)
Installing V2Ray v4.19.1 on x86_64
Downloading V2Ray: https://github.com/v2ray/v2ray-core/releases/download/v4.19.1/v2ray-linux-64.zip
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   608    0   608    0     0   1720      0 --:--:-- --:--:-- --:--:--  1722
100 11.2M  100 11.2M    0     0  2729k      0  0:00:04  0:00:04 --:--:-- 3141k
Updating software repo
Installing unzip
Extracting V2Ray package to /tmp/v2ray.
Archive:  /tmp/v2ray/v2ray.zip
  inflating: /tmp/v2ray/config.json  
   creating: /tmp/v2ray/doc/
  inflating: /tmp/v2ray/doc/readme.md  
  inflating: /tmp/v2ray/geoip.dat    
  inflating: /tmp/v2ray/geosite.dat  
   creating: /tmp/v2ray/systemd/
  inflating: /tmp/v2ray/systemd/v2ray.service  
   creating: /tmp/v2ray/systemv/
  inflating: /tmp/v2ray/systemv/v2ray  
  inflating: /tmp/v2ray/v2ctl        
 extracting: /tmp/v2ray/v2ctl.sig    
  inflating: /tmp/v2ray/v2ray        
 extracting: /tmp/v2ray/v2ray.sig    
  inflating: /tmp/v2ray/vpoint_socks_vmess.json  
  inflating: /tmp/v2ray/vpoint_vmess_freedom.json  
PORT:<rm>
UUID:<rm>
Created symlink from /etc/systemd/system/multi-user.target.wants/v2ray.service to /etc/systemd/system/v2ray.service.
V2Ray v4.19.1 is installed.
[root@CentOS ~]# systemctl status v2ray
● v2ray.service - V2Ray Service
   Loaded: loaded (/etc/systemd/system/v2ray.service; enabled; vendor preset: disabled)
   Active: inactive (dead)
[root@CentOS ~]# systemctl stop firewalld
[root@CentOS ~]# systemctl disable firewalld
Removed symlink /etc/systemd/system/dbus-org.fedoraproject.FirewallD1.service.
Removed symlink /etc/systemd/system/basic.target.wants/firewalld.service.
[root@CentOS ~]# systemctl start v2ray
[root@CentOS ~]# systemctl status v2ray
● v2ray.service - V2Ray Service
   Loaded: loaded (/etc/systemd/system/v2ray.service; enabled; vendor preset: disabled)
   Active: active (running) since Tue 2019-06-25 22:18:58 CST; 3s ago
 Main PID: 2107 (v2ray)
   CGroup: /system.slice/v2ray.service
           └─2107 /usr/bin/v2ray/v2ray -config /etc/v2ray/config.json

Jun 25 22:18:58 CentOS systemd[1]: Started V2Ray Service.
Jun 25 22:18:58 CentOS v2ray[2107]: V2Ray 4.19.1 (Let\'s Fly) Custom
Jun 25 22:18:58 CentOS v2ray[2107]: A unified platform for anti-censorship.
Jun 25 22:18:58 CentOS v2ray[2107]: 2019/06/25 22:18:58 [Warning] v2ray.com/core: V2Ray...ted
Hint: Some lines were ellipsized, use -l to show in full.
[root@CentOS ~]# cat /etc/v2ray/config.json 
{
  "inbounds": [{
    "port": <rm>,
    "protocol": "vmess",
    "settings": {
      "clients": [
        {
          "id": "<rm>",
          "level": 1,
          "alterId": 64
        }
      ]
    }
  }],
  "outbounds": [{
    "protocol": "freedom",
    "settings": {}
  },{
    "protocol": "blackhole",
    "settings": {},
    "tag": "blocked"
  }],
  "routing": {
    "rules": [
      {
        "type": "field",
        "ip": ["geoip:private"],
        "outboundTag": "blocked"
      }
    ]
  }
}
```

~~一键安装脚本有的是，特意看了内容有的真的会保存你的信息……安装原版的又不顺手，最终选了这个，带图形化管理界面不错`hhh`，是用`Flask`写的。
`wget -N --no-check-certificate https://raw.githubusercontent.com/FunctionClub/V2ray.Fun/master/install.sh && bash install.sh`~~
![修改连接](https://i1.yuangezhizao.cn/Win-10/20190512214632.png!webp)

~~还能直接看运行日志，也是十分爽到了~~
![运行日志](https://i1.yuangezhizao.cn/Win-10/20190512214900.png!webp)

~~然后第二天就又炸了，正好遇到~~
![htop](https://i1.yuangezhizao.cn/Win-10/20190513125106.jpg!webp)

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
``` bash
yum update
yum install vim htop axel -y
```

## 0x06.挂载第三方存储
1. `COSFS`
```
fuse: device not found, try 'modprobe fuse' first
```
2. `gdrive`：https://github.com/gdrive-org/gdrive
```
[root@CentOS ~]# gdrive about
Authentication needed
Go to the following url in your browser:
https://accounts.google.com/o/oauth2/auth?access_type=offline&client_id=<rm>.apps.googleusercontent.com&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&response_type=code&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive&state=state

Enter verification code: <rm>
User: 远哥制造, yuangezhizao@gmail.com
Used: 1.8 GB
Free: 14.3 GB
Total: 16.1 GB
Max upload size: 5.2 TB
```

## 0x07.关闭防火墙
关闭：`systemctl stop firewalld`
开机禁用：`systemctl disable firewalld`
状态：`systemctl status firewalld`

## 0x08. 编译安装[python373](https://www.python.org/downloads/release/python-373/)环境
https://www.yuangezhizao.cn/articles/Linux/CentOS/server.html#0x04-编译安装python373环境

## 0x09. 测速工具`speedtest-cli`
`pip3 install speedtest-cli`
``` bash
[root@CentOS ~]# speedtest-cli
Retrieving speedtest.net configuration...
Testing from QuadraNet (<rm>)...
Retrieving speedtest.net server list...
Selecting best server based on ping...
Hosted by Kansas Research and Education Network (Wichita, KS) [43.14 km]: 46.056 ms
Testing download speed................................................................................
Download: 96.85 Mbit/s
Testing upload speed......................................................................................................
Upload: 95.07 Mbit/s
```

## 0x10.后记
本来还想着放到路由器上，后来想想还是算了吧，毕竟性能（其实`K2`还可以的）

## 0x11.附注：已安装包（同步更新）
应该是最小化版本（因为`vim`都没有……）
``` bash
[root@CentOS ~]# yum list installed
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
 * base: centos.mirror.lax.us.hostlink.com.au
 * epel: mirror.layeronline.com
 * extras: linux.mirrors.es.net
 * updates: mirrors.syringanetworks.net
Installed Packages
GeoIP.x86_64                                       1.5.0-13.el7                      @base   
acl.x86_64                                         2.2.51-14.el7                     @base   
audit-libs.x86_64                                  2.8.4-4.el7                       @base   
autoconf.noarch                                    2.69-11.el7                       @base   
automake.noarch                                    1.13.4-3.el7                      @base   
axel.x86_64                                        2.4-9.el7                         @epel   
basesystem.noarch                                  10.0-7.el7.centos                 @base   
bash.x86_64                                        4.2.46-31.el7                     @base   
bind-libs-lite.x86_64                              32:9.9.4-73.el7_6                 @updates
bind-license.noarch                                32:9.9.4-73.el7_6                 @updates
binutils.x86_64                                    2.27-34.base.el7                  @base   
bzip2-devel.x86_64                                 1.0.6-13.el7                      @base   
bzip2-libs.x86_64                                  1.0.6-13.el7                      @base   
ca-certificates.noarch                             2018.2.22-70.0.el7_5              @base   
centos-release.x86_64                              7-6.1810.2.el7.centos             @base   
chkconfig.x86_64                                   1.7.4-1.el7                       @base   
cmake.x86_64                                       2.8.12.2-2.el7                    @base   
coreutils.x86_64                                   8.22-23.el7                       @base   
cpio.x86_64                                        2.11-27.el7                       @base   
cpp.x86_64                                         4.8.5-36.el7_6.2                  @updates
cracklib.x86_64                                    2.9.0-11.el7                      @base   
cracklib-dicts.x86_64                              2.9.0-11.el7                      @base   
cronie.x86_64                                      1.4.11-20.el7_6                   @updates
cronie-anacron.x86_64                              1.4.11-20.el7_6                   @updates
crontabs.noarch                                    1.11-6.20121102git.el7            @base   
cryptsetup-libs.x86_64                             2.0.3-3.el7                       @base   
curl.x86_64                                        7.29.0-51.el7                     @base   
cyrus-sasl-lib.x86_64                              2.1.26-23.el7                     @base   
dbus.x86_64                                        1:1.10.24-13.el7_6                @updates
dbus-glib.x86_64                                   0.100-7.el7                       @base   
dbus-libs.x86_64                                   1:1.10.24-13.el7_6                @updates
dbus-python.x86_64                                 1.1.1-9.el7                       @base   
dejavu-fonts-common.noarch                         2.33-6.el7                        @base   
dejavu-sans-fonts.noarch                           2.33-6.el7                        @base   
device-mapper.x86_64                               7:1.02.149-10.el7_6.7             @updates
device-mapper-libs.x86_64                          7:1.02.149-10.el7_6.7             @updates
dhclient.x86_64                                    12:4.2.5-68.el7.centos.1          @base   
dhcp-common.x86_64                                 12:4.2.5-68.el7.centos.1          @base   
dhcp-libs.x86_64                                   12:4.2.5-68.el7.centos.1          @base   
diffutils.x86_64                                   3.3-4.el7                         @base   
dracut.x86_64                                      033-554.el7                       @base   
ebtables.x86_64                                    2.0.10-16.el7                     @base   
elfutils-default-yama-scope.noarch                 0.172-2.el7                       @base   
elfutils-libelf.x86_64                             0.172-2.el7                       @base   
elfutils-libs.x86_64                               0.172-2.el7                       @base   
epel-release.noarch                                7-11                              @epel   
expat.x86_64                                       2.1.0-10.el7_3                    @updates
expat-devel.x86_64                                 2.1.0-10.el7_3                    @base   
fail2ban.noarch                                    0.9.7-1.el7                       @epel   
fail2ban-firewalld.noarch                          0.9.7-1.el7                       @epel   
fail2ban-sendmail.noarch                           0.9.7-1.el7                       @epel   
fail2ban-server.noarch                             0.9.7-1.el7                       @epel   
file-libs.x86_64                                   5.11-35.el7                       @base   
filesystem.x86_64                                  3.2-25.el7                        @base   
findutils.x86_64                                   1:4.5.11-6.el7                    @base   
fipscheck.x86_64                                   1.4.1-6.el7                       @base   
fipscheck-lib.x86_64                               1.4.1-6.el7                       @base   
firewalld.noarch                                   0.5.3-5.el7                       @base   
firewalld-filesystem.noarch                        0.5.3-5.el7                       @base   
fontconfig.x86_64                                  2.13.0-4.3.el7                    @base   
fontconfig-devel.x86_64                            2.13.0-4.3.el7                    @base   
fontpackages-filesystem.noarch                     1.44-8.el7                        @base   
freetype.x86_64                                    2.8-12.el7_6.1                    @updates
freetype-devel.x86_64                              2.8-12.el7_6.1                    @updates
gawk.x86_64                                        4.0.2-4.el7_3.1                   @updates
gcc.x86_64                                         4.8.5-36.el7_6.2                  @updates
gcc-c++.x86_64                                     4.8.5-36.el7_6.2                  @updates
gdbm.x86_64                                        1.10-8.el7                        @base   
gettext.x86_64                                     0.19.8.1-2.el7                    @base   
gettext-libs.x86_64                                0.19.8.1-2.el7                    @base   
git.x86_64                                         1.8.3.1-20.el7                    @updates
glib2.x86_64                                       2.56.1-2.el7                      @base   
glibc.x86_64                                       2.17-260.el7_6.5                  @updates
glibc-common.x86_64                                2.17-260.el7_6.5                  @updates
glibc-devel.x86_64                                 2.17-260.el7_6.5                  @updates
glibc-headers.x86_64                               2.17-260.el7_6.5                  @updates
gmp.x86_64                                         1:6.0.0-15.el7                    @base   
gnupg2.x86_64                                      2.0.22-5.el7_5                    @base   
gobject-introspection.x86_64                       1.56.1-1.el7                      @base   
gpgme.x86_64                                       1.3.2-5.el7                       @base   
gpm-libs.x86_64                                    1.20.7-5.el7                      @base   
grep.x86_64                                        2.20-3.el7                        @base   
groff-base.x86_64                                  1.22.2-8.el7                      @base   
gzip.x86_64                                        1.5-10.el7                        @base   
hardlink.x86_64                                    1:1.0-19.el7                      @base   
hostname.x86_64                                    3.13-3.el7                        @base   
htop.x86_64                                        2.2.0-3.el7                       @epel   
info.x86_64                                        5.1-5.el7                         @base   
initscripts.x86_64                                 9.49.46-1.el7                     @base   
iproute.x86_64                                     4.11.0-14.el7_6.2                 @updates
ipset.x86_64                                       6.38-3.el7_6                      @updates
ipset-libs.x86_64                                  6.38-3.el7_6                      @updates
iptables.x86_64                                    1.4.21-28.el7                     @base   
iputils.x86_64                                     20160308-10.el7                   @base   
json-c.x86_64                                      0.11-4.el7_0                      @base   
kernel-headers.x86_64                              3.10.0-957.12.2.el7               @updates
keyutils-libs.x86_64                               1.5.8-3.el7                       @base   
keyutils-libs-devel.x86_64                         1.5.8-3.el7                       @base   
kmod.x86_64                                        20-23.el7                         @base   
kmod-libs.x86_64                                   20-23.el7                         @base   
kpartx.x86_64                                      0.4.9-123.el7                     @base   
krb5-devel.x86_64                                  1.15.1-37.el7_6                   @updates
krb5-libs.x86_64                                   1.15.1-37.el7_6                   @updates
less.x86_64                                        458-9.el7                         @base   
libX11.x86_64                                      1.6.5-2.el7                       @base   
libX11-common.noarch                               1.6.5-2.el7                       @base   
libX11-devel.x86_64                                1.6.5-2.el7                       @base   
libXau.x86_64                                      1.0.8-2.1.el7                     @base   
libXau-devel.x86_64                                1.0.8-2.1.el7                     @base   
libXft.x86_64                                      2.3.2-2.el7                       @base   
libXft-devel.x86_64                                2.3.2-2.el7                       @base   
libXrender.x86_64                                  0.9.10-1.el7                      @base   
libXrender-devel.x86_64                            0.9.10-1.el7                      @base   
libacl.x86_64                                      2.2.51-14.el7                     @base   
libarchive.x86_64                                  3.1.2-10.el7_2                    @base   
libassuan.x86_64                                   2.1.0-3.el7                       @base   
libattr.x86_64                                     2.4.46-13.el7                     @base   
libblkid.x86_64                                    2.23.2-59.el7_6.1                 @updates
libcap.x86_64                                      2.22-9.el7                        @base   
libcap-ng.x86_64                                   0.7.5-4.el7                       @base   
libcom_err.x86_64                                  1.42.9-13.el7                     @base   
libcom_err-devel.x86_64                            1.42.9-13.el7                     @base   
libcroco.x86_64                                    0.6.12-4.el7                      @base   
libcurl.x86_64                                     7.29.0-51.el7                     @base   
libdb.x86_64                                       5.3.21-24.el7                     @base   
libdb-utils.x86_64                                 5.3.21-24.el7                     @base   
libedit.x86_64                                     3.0-12.20121213cvs.el7            @base   
libestr.x86_64                                     0.1.9-2.el7                       @base   
libfastjson.x86_64                                 0.99.4-3.el7                      @base   
libffi.x86_64                                      3.0.13-18.el7                     @base   
libffi-devel.x86_64                                3.0.13-18.el7                     @base   
libgcc.x86_64                                      4.8.5-36.el7_6.2                  @updates
libgcrypt.x86_64                                   1.5.3-14.el7                      @base   
libgomp.x86_64                                     4.8.5-36.el7_6.2                  @updates
libgpg-error.x86_64                                1.12-3.el7                        @base   
libidn.x86_64                                      1.28-4.el7                        @base   
libkadm5.x86_64                                    1.15.1-37.el7_6                   @updates
libmnl.x86_64                                      1.0.3-7.el7                       @base   
libmount.x86_64                                    2.23.2-59.el7_6.1                 @updates
libmpc.x86_64                                      1.0.1-3.el7                       @base   
libnetfilter_conntrack.x86_64                      1.0.6-1.el7_3                     @updates
libnfnetlink.x86_64                                1.0.1-4.el7                       @base   
libpng.x86_64                                      2:1.5.13-7.el7_2                  @base   
libpng-devel.x86_64                                2:1.5.13-7.el7_2                  @base   
libpwquality.x86_64                                1.2.3-5.el7                       @base   
libselinux.x86_64                                  2.5-14.1.el7                      @base   
libselinux-devel.x86_64                            2.5-14.1.el7                      @base   
libselinux-python.x86_64                           2.5-14.1.el7                      @base   
libselinux-utils.x86_64                            2.5-14.1.el7                      @base   
libsemanage.x86_64                                 2.5-14.el7                        @base   
libsepol.x86_64                                    2.5-10.el7                        @base   
libsepol-devel.x86_64                              2.5-10.el7                        @base   
libsmartcols.x86_64                                2.23.2-59.el7_6.1                 @updates
libssh2.x86_64                                     1.4.3-12.el7_6.2                  @updates
libstdc++.x86_64                                   4.8.5-36.el7_6.2                  @updates
libstdc++-devel.x86_64                             4.8.5-36.el7_6.2                  @updates
libtasn1.x86_64                                    4.10-1.el7                        @base   
libunistring.x86_64                                0.9.3-9.el7                       @base   
libuser.x86_64                                     0.60-9.el7                        @base   
libutempter.x86_64                                 1.1.6-4.el7                       @base   
libuuid.x86_64                                     2.23.2-59.el7_6.1                 @updates
libuuid-devel.x86_64                               2.23.2-59.el7_6.1                 @updates
libverto.x86_64                                    0.2.5-4.el7                       @base   
libverto-devel.x86_64                              0.2.5-4.el7                       @base   
libxcb.x86_64                                      1.13-1.el7                        @base   
libxcb-devel.x86_64                                1.13-1.el7                        @base   
libxml2.x86_64                                     2.9.1-6.el7_2.3                   @base   
logrotate.x86_64                                   3.8.6-17.el7                      @base   
lua.x86_64                                         5.1.4-15.el7                      @base   
lz4.x86_64                                         1.7.5-2.el7                       @base   
lzo.x86_64                                         2.06-8.el7                        @base   
m4.x86_64                                          1.4.16-10.el7                     @base   
make.x86_64                                        1:3.82-23.el7                     @base   
mpfr.x86_64                                        3.1.1-4.el7                       @base   
nano.x86_64                                        2.3.1-10.el7                      @base   
ncurses.x86_64                                     5.9-14.20130511.el7_4             @base   
ncurses-base.noarch                                5.9-14.20130511.el7_4             @base   
ncurses-devel.x86_64                               5.9-14.20130511.el7_4             @base   
ncurses-libs.x86_64                                5.9-14.20130511.el7_4             @base   
nspr.x86_64                                        4.19.0-1.el7_5                    @base   
nss.x86_64                                         3.36.0-7.1.el7_6                  @updates
nss-pem.x86_64                                     1.0.3-5.el7_6.1                   @updates
nss-softokn.x86_64                                 3.36.0-5.el7_5                    @base   
nss-softokn-freebl.x86_64                          3.36.0-5.el7_5                    @base   
nss-sysinit.x86_64                                 3.36.0-7.1.el7_6                  @updates
nss-tools.x86_64                                   3.36.0-7.1.el7_6                  @updates
nss-util.x86_64                                    3.36.0-1.1.el7_6                  @updates
openldap.x86_64                                    2.4.44-21.el7_6                   @updates
openssh.x86_64                                     7.4p1-16.el7                      @base   
openssh-clients.x86_64                             7.4p1-16.el7                      @base   
openssh-server.x86_64                              7.4p1-16.el7                      @base   
openssl.x86_64                                     1:1.0.2k-16.el7_6.1               @updates
openssl-devel.x86_64                               1:1.0.2k-16.el7_6.1               @updates
openssl-libs.x86_64                                1:1.0.2k-16.el7_6.1               @updates
p11-kit.x86_64                                     0.23.5-3.el7                      @base   
p11-kit-trust.x86_64                               0.23.5-3.el7                      @base   
pam.x86_64                                         1.1.8-22.el7                      @base   
passwd.x86_64                                      0.79-4.el7                        @base   
pcre.x86_64                                        8.32-17.el7                       @base   
pcre-devel.x86_64                                  8.32-17.el7                       @base   
perl.x86_64                                        4:5.16.3-294.el7_6                @updates
perl-Carp.noarch                                   1.26-244.el7                      @base   
perl-Data-Dumper.x86_64                            2.145-3.el7                       @base   
perl-Encode.x86_64                                 2.51-7.el7                        @base   
perl-Error.noarch                                  1:0.17020-2.el7                   @base   
perl-Exporter.noarch                               5.68-3.el7                        @base   
perl-File-Path.noarch                              2.09-2.el7                        @base   
perl-File-Temp.noarch                              0.23.01-3.el7                     @base   
perl-Filter.x86_64                                 1.49-3.el7                        @base   
perl-Getopt-Long.noarch                            2.40-3.el7                        @base   
perl-Git.noarch                                    1.8.3.1-20.el7                    @updates
perl-HTTP-Tiny.noarch                              0.033-3.el7                       @base   
perl-PathTools.x86_64                              3.40-5.el7                        @base   
perl-Pod-Escapes.noarch                            1:1.04-294.el7_6                  @updates
perl-Pod-Perldoc.noarch                            3.20-4.el7                        @base   
perl-Pod-Simple.noarch                             1:3.28-4.el7                      @base   
perl-Pod-Usage.noarch                              1.63-3.el7                        @base   
perl-Scalar-List-Utils.x86_64                      1.27-248.el7                      @base   
perl-Socket.x86_64                                 2.010-4.el7                       @base   
perl-Storable.x86_64                               2.45-3.el7                        @base   
perl-TermReadKey.x86_64                            2.30-20.el7                       @base   
perl-Test-Harness.noarch                           3.28-3.el7                        @base   
perl-Text-ParseWords.noarch                        3.29-4.el7                        @base   
perl-Thread-Queue.noarch                           3.02-2.el7                        @base   
perl-Time-HiRes.x86_64                             4:1.9725-3.el7                    @base   
perl-Time-Local.noarch                             1.2300-2.el7                      @base   
perl-constant.noarch                               1.27-2.el7                        @base   
perl-libs.x86_64                                   4:5.16.3-294.el7_6                @updates
perl-macros.x86_64                                 4:5.16.3-294.el7_6                @updates
perl-parent.noarch                                 1:0.225-244.el7                   @base   
perl-podlators.noarch                              2.5.1-3.el7                       @base   
perl-threads.x86_64                                1.87-4.el7                        @base   
perl-threads-shared.x86_64                         1.43-6.el7                        @base   
pinentry.x86_64                                    0.8.1-17.el7                      @base   
pkgconfig.x86_64                                   1:0.27.1-4.el7                    @base   
policycoreutils.x86_64                             2.5-29.el7_6.1                    @updates
popt.x86_64                                        1.13-16.el7                       @base   
procps-ng.x86_64                                   3.3.10-23.el7                     @base   
pth.x86_64                                         2.0.7-23.el7                      @base   
pygpgme.x86_64                                     0.3-9.el7                         @base   
pyliblzma.x86_64                                   0.5.3-11.el7                      @base   
python.x86_64                                      2.7.5-77.el7_6                    @updates
python-backports.x86_64                            1.0-8.el7                         @base   
python-backports-ssl_match_hostname.noarch         3.5.0.1-1.el7                     @base   
python-decorator.noarch                            3.4.0-3.el7                       @base   
python-devel.x86_64                                2.7.5-77.el7_6                    @updates
python-firewall.noarch                             0.5.3-5.el7                       @base   
python-gobject-base.x86_64                         3.22.0-1.el7_4.1                  @base   
python-iniparse.noarch                             0.4-9.el7                         @base   
python-ipaddress.noarch                            1.0.16-2.el7                      @base   
python-libs.x86_64                                 2.7.5-77.el7_6                    @updates
python-pycurl.x86_64                               7.19.0-19.el7                     @base   
python-setuptools.noarch                           0.9.8-7.el7                       @base   
python-slip.noarch                                 0.4.0-4.el7                       @base   
python-slip-dbus.noarch                            0.4.0-4.el7                       @base   
python-urlgrabber.noarch                           3.10-9.el7                        @base   
python2-pip.noarch                                 8.1.2-8.el7                       @epel   
pyxattr.x86_64                                     0.5.1-5.el7                       @base   
qrencode-libs.x86_64                               3.4.1-3.el7                       @base   
readline.x86_64                                    6.2-10.el7                        @base   
readline-devel.x86_64                              6.2-10.el7                        @base   
rootfiles.noarch                                   8.1-11.el7                        @base   
rpm.x86_64                                         4.11.3-35.el7                     @base   
rpm-build-libs.x86_64                              4.11.3-35.el7                     @base   
rpm-libs.x86_64                                    4.11.3-35.el7                     @base   
rpm-python.x86_64                                  4.11.3-35.el7                     @base   
rsync.x86_64                                       3.1.2-6.el7_6.1                   @updates
rsyslog.x86_64                                     8.24.0-34.el7                     @base   
sed.x86_64                                         4.2.2-5.el7                       @base   
setup.noarch                                       2.8.71-10.el7                     @base   
shadow-utils.x86_64                                2:4.1.5.1-25.el7_6.1              @updates
shared-mime-info.x86_64                            1.8-4.el7                         @base   
socat.x86_64                                       1.7.3.2-2.el7                     @base   
sqlite.x86_64                                      3.7.17-8.el7                      @base   
sqlite-devel.x86_64                                3.7.17-8.el7                      @base   
ssmtp.x86_64                                       2.64-14.el7                       @epel   
systemd.x86_64                                     219-62.el7_6.6                    @updates
systemd-libs.x86_64                                219-62.el7_6.6                    @updates
systemd-python.x86_64                              219-62.el7_6.6                    @updates
sysvinit-tools.x86_64                              2.88-14.dsf.el7                   @base   
tar.x86_64                                         2:1.26-35.el7                     @base   
tcl.x86_64                                         1:8.5.13-8.el7                    @base   
tcl-devel.x86_64                                   1:8.5.13-8.el7                    @base   
tcp_wrappers-libs.x86_64                           7.6-77.el7                        @base   
tk.x86_64                                          1:8.5.13-6.el7                    @base   
tk-devel.x86_64                                    1:8.5.13-6.el7                    @base   
tzdata.noarch                                      2019a-1.el7                       @updates
unzip.x86_64                                       6.0-19.el7                        @base   
ustr.x86_64                                        1.0.4-16.el7                      @base   
util-linux.x86_64                                  2.23.2-59.el7_6.1                 @updates
vim-common.x86_64                                  2:7.4.160-5.el7                   @base   
vim-enhanced.x86_64                                2:7.4.160-5.el7                   @base   
vim-filesystem.x86_64                              2:7.4.160-5.el7                   @base   
vim-minimal.x86_64                                 2:7.4.160-5.el7                   @base   
wget.x86_64                                        1.14-18.el7                       @base   
which.x86_64                                       2.20-7.el7                        @base   
xorg-x11-proto-devel.noarch                        2018.4-1.el7                      @base   
xz.x86_64                                          5.2.2-1.el7                       @base   
xz-libs.x86_64                                     5.2.2-1.el7                       @base   
yum.noarch                                         3.4.3-161.el7.centos              @base   
yum-metadata-parser.x86_64                         1.1.4-10.el7                      @base   
yum-plugin-fastestmirror.noarch                    1.1.31-50.el7                     @base   
zlib.x86_64                                        1.2.7-18.el7                      @base   
zlib-devel.x86_64                                  1.2.7-18.el7                      @base   
[root@CentOS ~]# 
```