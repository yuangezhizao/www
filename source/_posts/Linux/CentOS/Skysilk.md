---
title: 重装系统之 Skysilk CentOS 7 安装 v2ray 代理等
date: 2019-5-12 20:53:55
tags:
  - CentOS
  - server
count: 5
os: 0
os_1: 10.0.17763.475 2019-LTSC
browser: 0
browser_1: 72.0.3626.121 Stable
place: 家
key: 51
---
    国庆过后甚久，近期终于恢复
<!-- more -->

## 0x00.前言
~~![隔一阵子就炸一次的面板]~~(https://i1.yuangezhizao.cn/Win-10/20191011215155.jpg!webp)
~~一直以为被墙了，今晚才反应过来很奇怪啊，能`ping`，但是`nginx`外网页面看不了（还不是`80`端口），`ssh`连不上……直到我打开了`Graphs`，woc~~
~~![CPU爆了]~~(https://i1.yuangezhizao.cn/Win-10/20190512205532.jpg!webp)
~~重启之后终于登录进去了，提示距离上次成功登录有十万次错误，绝了，`htop`也没看出来是哪个进程，并不是弱密码，奇怪的是那上面自带的`fail2ban`进程在但是貌似没生效，我也没去看相关日志，只是把`/var/log/nginx`和`/var/log/v2ray`这俩文件夹下下来了，等后期再分析……然后就直接重装新系统并传了密钥~~

## 0x01.`ssh`关闭密码登录
新系统刚进去就看到了两次失败登录尝试，于是直接关了密码登录`/etc/ssh/sshd_config`：`PasswordAuthentication no`，`systemctl restart sshd.service`，注销之后果然密码登录不行，密钥`ok`
![修改配置文件不会显示在这里](https://i1.yuangezhizao.cn/Win-10/20190512214356.jpg!webp)
![或在重装系统时选好](https://i1.yuangezhizao.cn/Win-10/20191120185105.jpg!webp)

## 0x02. `v2ray`合集
### 1. [v2-ui](https://github.com/sprov065/v2-ui/)
作者博客：[v2-ui，一个全新的多协议多用户 v2ray 面板](https://web.archive.org/web/20191123055128/https://blog.sprov.xyz/2019/08/03/v2-ui/)
又搜罗到好的面板了，用了数月看起来还不错
![登录](https://i1.yuangezhizao.cn/Win-10/20191123141115.jpg!webp)
![主界面](https://i1.yuangezhizao.cn/Win-10/20191123141157.jpg!webp)

### 2. [v2ray](https://github.com/v2ray/v2ray-core)
使用官方原版安装，其实只需要配置文件提前写好就`ok`
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

### ~~3. [V2ray.Fun](https://github.com/FunctionClub/V2ray.Fun)~~
~~一键安装脚本有的是，特意看了内容有的真的会保存你的信息……安装原版的又不顺手，最终选了这个，带图形化管理界面不错`hhh`，是用`Flask`写的。
`wget -N --no-check-certificate https://raw.githubusercontent.com/FunctionClub/V2ray.Fun/master/install.sh && bash install.sh`~~
~~![修改连接]~~(https://i1.yuangezhizao.cn/Win-10/20190512214632.png!webp)
~~还能直接看运行日志，也是十分爽到了~~
~~![运行日志]~~(https://i1.yuangezhizao.cn/Win-10/20190512214900.png!webp)
~~然后第二天就又炸了，正好遇到~~
~~![我们仍未知道那天就炸了的原因.jpG]~~(https://i1.yuangezhizao.cn/Win-10/20190513125106.jpg!webp)

## 0x03.服务器版本
``` bash
[root@CentOS ~]# rpm -q centos-release
centos-release-7-7.1908.0.el7.centos.x86_64
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
yum install vim htop axel ffmpeg -y
```

## 0x06.挂载第三方存储
1. `COSFS`挂载不能
```
fuse: device not found, try 'modprobe fuse' first
```
2. [gdrive](https://github.com/gdrive-org/gdrive)~~完美~~挂载不能
![过草.jpG](https://i1.yuangezhizao.cn/Win-10/20191204185510.jpg!webp)
去看`Issues`果然，[Application is not verified](https://github.com/gdrive-org/gdrive/issues/514)
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
这台白嫖一年的国外机子上完全**没有**必要开这玩楞，每次端口开放不能真是太烦了（`flag`草
关闭：`systemctl stop firewalld`
开机禁用：`systemctl disable firewalld`
状态：`systemctl status firewalld`
于是依赖于`firewalld`的`fail2ban`就变成摆设了……

## 0x08. 编译安装[python380](https://www.python.org/downloads/release/python-380/)环境
https://www.yuangezhizao.cn/articles/Linux/CentOS/server.html#0x04-编译安装python380环境

## 0x09. 测速工具[SPEEDTEST CLI](https://speedtest.net/apps/cli#fedora)
![然后竟然出了官方版](https://i1.yuangezhizao.cn/Win-10/20191120191325.jpg!webp)
```
sudo yum install wget
wget https://bintray.com/ookla/rhel/rpm -O bintray-ookla-rhel.repo
sudo mv bintray-ookla-rhel.repo /etc/yum.repos.d/
# Other non-official binaries will conflict with Speedtest CLI
# Example how to remove using yum
# rpm -qa | grep speedtest | xargs -I {} sudo yum -y remove {}
sudo yum install speedtest
```
测速结果
```
[root@CentOS ~]# speedtest
==============================================================================

You may only use this Speedtest software and information generated
from it for personal, non-commercial use, through a command line
interface on a personal computer. Your use of this software is subject
to the End User License Agreement, Terms of Use and Privacy Policy at
these URLs:

	https://www.speedtest.net/about/eula
	https://www.speedtest.net/about/terms
	https://www.speedtest.net/about/privacy

==============================================================================

Do you accept the license? [type YES to accept]: YES
License acceptance recorded. Continuing.


   Speedtest by Ookla

     Server: Xfernet - Los Angeles, CA (id = 13516)
        ISP: QuadraNet
    Latency:    41.88 ms   (1.92 ms jitter)
   Download:    99.61 Mbps (data used: 123.0 MB)                               
     Upload:   102.78 Mbps (data used: 132.7 MB)                               
Packet Loss:     0.0%
 Result URL: https://www.speedtest.net/result/c/<rm>
```
基于`py`的上古`speedtest-cli`已成为历史
~~`pip3 install speedtest-cli`~~
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

## 0x10.安装[宝塔面板](https://www.bt.cn/)
经过多次试验，不管是选择`源码编译安装`还是`二进制极速安装`都会失败，想了下原因应该是机子配置太低……
即使安装完成，但是会自动启动应用程序，而且默认配置已经吃满了性能，所以内存直接就爆掉了，过草
因此，想安装软件只能自己手动安装，再修改配置文件，最后启动（生草，比如 `ng` 就是这么搞的
比较搞笑的一点是，即使`Web Server`使用的是`ng`而不是`Apache24`，仍然会遇到进程莫名没了的情况
最近数次梯子炸了的时候都是发现反代`v2`的`ng`进程没了，只能使用备用的`tcp`版`v2`替代使用
猜测是内存不足，毕竟只有`512 MB`，白嫖的月一刀套餐能用就不错了`hhh`，`Docker`可是想都不用想的了
之后准备试试基于`Go`的`Caddy`，配置文件的编写看起来很精简……
![每次进来都会弹出安装提示](https://i1.yuangezhizao.cn/Win-10/20191123152243.jpg!webp)
![主界面](https://i1.yuangezhizao.cn/Win-10/20191123152444.jpg!webp)

比较实用的是`Web Shell`和`文件管理`，~~这样在使用公司网络这种含有特殊防火墙无法连接`22`端口的环境下也可以顺利操作了`hhh`~~
~~顺便一提，十月份特殊时期靠着公司代理能连上`proxy.yuangezhizao.cn`，然后`bt`面板主界面一直开着没关，导致访问量爆炸~~
~~到了`191114`突然被`SC`课电话查水表了，“这个域名是你自己的吧……你这个是干什么的？”~~
~~上午巨困……内部电话也听不太清……后来想想解释的也不对（Doge~~
~~`网 络 审 计 大 草`~~

## 0x11.[Netdata](https://github.com/netdata/netdata)
它是本人所见过的最高大上的监控？系统了，于是立即把手头上的全部`Linux`服务器都安装上这玩楞
界面吊炸天，比如梯子服务器监控地址：[https://proxy.yuangezhizao.cn:19999](https://proxy.yuangezhizao.cn:19999)

## 0x12.后记
本来还想着放到路由器上，后来想想还是算了吧，毕竟性能（其实`K2`还可以的）
`2019.10`翻车了。。。后借用大佬的`Cisco AnyConnect`才够到了失恋的国外机子（骚操作
连上之后`CloudFlare`反代`ws`协议的`v2ray`才能勉强持续使用……
然而都`10.11`也不见恢复的样子，过草过草……
所以就干脆一步到位直接重装系统了……

## 0x13.附注：已安装包（同步更新）
应该是最小化版本（因为`vim`都没有……）
![htop 看了眼进程列表](https://i1.yuangezhizao.cn/Win-10/20191120182547.jpg!webp)

其实也就是多安了个`bt`面板而已，顺便把`v2ray`和`v2-ui`都拿`ng`反代上（正是因为梯子炸了`ng`进程没了才发现`4`天前机子竟然被重启过……
`= =`
``` bash
[root@CentOS ~]# yum list installed
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
 * base: mirror.hostduplex.com
 * epel: d2lzkl7pfhq30w.cloudfront.net
 * extras: mirror.fileplanet.com
 * nux-dextop: mirror.li.nux.ro
 * updates: repos.lax.quadranet.com
Installed Packages
GeoIP.x86_64                                1.5.0-14.el7                                  @base               
Judy.x86_64                                 1.0.5-8.el7                                   @epel               
Judy-devel.x86_64                           1.0.5-8.el7                                   @epel               
SDL.x86_64                                  1.2.15-14.el7                                 @base               
acl.x86_64                                  2.2.51-14.el7                                 @base               
alsa-lib.x86_64                             1.1.8-1.el7                                   @base               
apr.x86_64                                  1.4.8-5.el7                                   @base               
apr-util.x86_64                             1.5.2-6.el7                                   @base               
aria2.x86_64                                1.34.0-5.el7                                  @epel               
audit-libs.x86_64                           2.8.5-4.el7                                   @base               
autoconf.noarch                             2.69-11.el7                                   @base               
autoconf-archive.noarch                     2017.03.21-1.el7                              @base               
autogen.x86_64                              5.18-5.el7                                    @base               
autogen-libopts.x86_64                      5.18-5.el7                                    @base               
automake.noarch                             1.13.4-3.el7                                  @base               
axel.x86_64                                 2.4-9.el7                                     @epel               
basesystem.noarch                           10.0-7.el7.centos                             @base               
bash.x86_64                                 4.2.46-33.el7                                 @base               
bind-export-libs.x86_64                     32:9.11.4-9.P2.el7                            @base               
bind-libs.x86_64                            32:9.11.4-9.P2.el7                            @base               
bind-libs-lite.x86_64                       32:9.11.4-9.P2.el7                            @base               
bind-license.noarch                         32:9.11.4-9.P2.el7                            @base               
bind-utils.x86_64                           32:9.11.4-9.P2.el7                            @base               
binutils.x86_64                             2.27-41.base.el7_7.1                          @updates            
bison.x86_64                                3.0.4-2.el7                                   installed           
bzip2-devel.x86_64                          1.0.6-13.el7                                  @base               
bzip2-libs.x86_64                           1.0.6-13.el7                                  @base               
c-ares.x86_64                               1.10.0-3.el7                                  @base               
ca-certificates.noarch                      2019.2.32-76.el7_7                            @updates            
centos-release.x86_64                       7-7.1908.0.el7.centos                         @base               
chkconfig.x86_64                            1.7.4-1.el7                                   @base               
coreutils.x86_64                            8.22-24.el7                                   @base               
cpio.x86_64                                 2.11-27.el7                                   @base               
cpp.x86_64                                  4.8.5-39.el7                                  @base               
cracklib.x86_64                             2.9.0-11.el7                                  @base               
cracklib-dicts.x86_64                       2.9.0-11.el7                                  @base               
cronie.x86_64                               1.4.11-23.el7                                 @base               
cronie-anacron.x86_64                       1.4.11-23.el7                                 @base               
crontabs.noarch                             1.11-6.20121102git.el7                        @base               
cryptsetup-libs.x86_64                      2.0.3-5.el7                                   @base               
curl.x86_64                                 7.29.0-54.el7_7.1                             @updates            
cyrus-sasl-lib.x86_64                       2.1.26-23.el7                                 @base               
dbus.x86_64                                 1:1.10.24-13.el7_6                            @base               
dbus-glib.x86_64                            0.100-7.el7                                   @base               
dbus-libs.x86_64                            1:1.10.24-13.el7_6                            @base               
dbus-python.x86_64                          1.1.1-9.el7                                   @base               
dejavu-fonts-common.noarch                  2.33-6.el7                                    @base               
dejavu-sans-fonts.noarch                    2.33-6.el7                                    @base               
device-mapper.x86_64                        7:1.02.158-2.el7_7.2                          @updates            
device-mapper-libs.x86_64                   7:1.02.158-2.el7_7.2                          @updates            
dhclient.x86_64                             12:4.2.5-77.el7.centos                        @base               
dhcp-common.x86_64                          12:4.2.5-77.el7.centos                        @base               
dhcp-libs.x86_64                            12:4.2.5-77.el7.centos                        @base               
diffutils.x86_64                            3.3-5.el7                                     @base               
dmidecode.x86_64                            1:3.2-3.el7                                   @base               
dos2unix.x86_64                             6.0.3-7.el7                                   @base               
dracut.x86_64                               033-564.el7                                   @base               
ebtables.x86_64                             2.0.10-16.el7                                 @base               
elfutils-default-yama-scope.noarch          0.176-2.el7                                   @base               
elfutils-libelf.x86_64                      0.176-2.el7                                   @base               
elfutils-libs.x86_64                        0.176-2.el7                                   @base               
epel-release.noarch                         7-12                                          @epel               
expat.x86_64                                2.1.0-10.el7_3                                @updates            
expat-devel.x86_64                          2.1.0-10.el7_3                                @base               
fail2ban.noarch                             0.9.7-1.el7                                   @epel               
fail2ban-firewalld.noarch                   0.9.7-1.el7                                   @epel               
fail2ban-sendmail.noarch                    0.9.7-1.el7                                   @epel               
fail2ban-server.noarch                      0.9.7-1.el7                                   @epel               
fdk-aac.x86_64                              0.1.4-1                                       @nux-dextop         
ffmpeg.x86_64                               2.8.15-2.el7.nux                              @nux-dextop         
ffmpeg-devel.x86_64                         2.8.15-2.el7.nux                              @nux-dextop         
ffmpeg-libs.x86_64                          2.8.15-2.el7.nux                              @nux-dextop         
file-libs.x86_64                            5.11-35.el7                                   @base               
filesystem.x86_64                           3.2-25.el7                                    @base               
findutils.x86_64                            1:4.5.11-6.el7                                @base               
fipscheck.x86_64                            1.4.1-6.el7                                   @base               
fipscheck-devel.x86_64                      1.4.1-6.el7                                   @base               
fipscheck-lib.x86_64                        1.4.1-6.el7                                   @base               
firewalld.noarch                            0.6.3-2.el7_7.2                               @updates            
firewalld-filesystem.noarch                 0.6.3-2.el7_7.2                               @updates            
flac-libs.x86_64                            1.3.0-5.el7_1                                 @base               
flex.x86_64                                 2.5.37-6.el7                                  installed           
fontconfig.x86_64                           2.13.0-4.3.el7                                @base               
fontconfig-devel.x86_64                     2.13.0-4.3.el7                                @base               
fontpackages-filesystem.noarch              1.44-8.el7                                    @base               
freetype.x86_64                             2.8-14.el7                                    @base               
freetype-devel.x86_64                       2.8-14.el7                                    @base               
fribidi.x86_64                              1.0.2-1.el7                                   @base               
gawk.x86_64                                 4.0.2-4.el7_3.1                               @updates            
gc.x86_64                                   7.2d-7.el7                                    @base               
gcc.x86_64                                  4.8.5-39.el7                                  @base               
gcc-c++.x86_64                              4.8.5-39.el7                                  @base               
gdbm.x86_64                                 1.10-8.el7                                    @base               
gdbm-devel.x86_64                           1.10-8.el7                                    @base               
geoipupdate.x86_64                          2.5.0-1.el7                                   @base               
gettext.x86_64                              0.19.8.1-2.el7                                @base               
gettext-libs.x86_64                         0.19.8.1-2.el7                                @base               
git.x86_64                                  1.8.3.1-20.el7                                @base               
glib2.x86_64                                2.56.1-5.el7                                  @base               
glibc.x86_64                                2.17-292.el7                                  @base               
glibc-common.x86_64                         2.17-292.el7                                  @base               
glibc-devel.x86_64                          2.17-292.el7                                  @base               
glibc-headers.x86_64                        2.17-292.el7                                  @base               
gmp.x86_64                                  1:6.0.0-15.el7                                @base               
gnupg2.x86_64                               2.0.22-5.el7_5                                @base               
gnutls.x86_64                               3.3.29-9.el7_6                                @base               
gobject-introspection.x86_64                1.56.1-1.el7                                  @base               
golang.x86_64                               1.13.3-1.el7                                  @epel               
golang-bin.x86_64                           1.13.3-1.el7                                  @epel               
golang-src.noarch                           1.13.3-1.el7                                  @epel               
gpgme.x86_64                                1.3.2-5.el7                                   @base               
gpm-libs.x86_64                             1.20.7-6.el7                                  @base               
graphite2.x86_64                            1.3.10-1.el7_3                                @base               
grep.x86_64                                 2.20-3.el7                                    @base               
groff-base.x86_64                           1.22.2-8.el7                                  @base               
gsm.x86_64                                  1.0.13-11.el7                                 @base               
guile.x86_64                                5:2.0.9-5.el7                                 @base               
gzip.x86_64                                 1.5-10.el7                                    @base               
hardlink.x86_64                             1:1.0-19.el7                                  @base               
harfbuzz.x86_64                             1.7.5-2.el7                                   @base               
hostname.x86_64                             3.13-3.el7_7.1                                @updates            
htop.x86_64                                 2.2.0-3.el7                                   @epel               
hwdata.x86_64                               0.252-9.3.el7                                 @base               
icu.x86_64                                  50.2-3.el7                                    @base               
iftop.x86_64                                1.0-0.21.pre4.el7                             @epel               
info.x86_64                                 5.1-5.el7                                     @base               
initscripts.x86_64                          9.49.47-1.el7                                 @base               
iproute.x86_64                              4.11.0-25.el7_7.2                             @updates            
ipset.x86_64                                7.1-1.el7                                     @base               
ipset-libs.x86_64                           7.1-1.el7                                     @base               
iptables.x86_64                             1.4.21-33.el7                                 @base               
iptables-services.x86_64                    1.4.21-33.el7                                 @base               
iputils.x86_64                              20160308-10.el7                               @base               
jbigkit-libs.x86_64                         2.0-11.el7                                    @base               
json-c.x86_64                               0.11-4.el7_0                                  @base               
kernel-headers.x86_64                       3.10.0-1062.7.1.el7                           @updates            
keyutils-libs.x86_64                        1.5.8-3.el7                                   @base               
keyutils-libs-devel.x86_64                  1.5.8-3.el7                                   @base               
kmod.x86_64                                 20-25.el7                                     @base               
kmod-libs.x86_64                            20-25.el7                                     @base               
kpartx.x86_64                               0.4.9-127.el7                                 @base               
krb5-devel.x86_64                           1.15.1-37.el7_7.2                             @updates            
krb5-libs.x86_64                            1.15.1-37.el7_7.2                             @updates            
lame-libs.x86_64                            3.100-1.el7                                   @epel               
less.x86_64                                 458-9.el7                                     @base               
libICE.x86_64                               1.0.9-9.el7                                   @base               
libSM.x86_64                                1.2.2-2.el7                                   @base               
libX11.x86_64                               1.6.7-2.el7                                   @base               
libX11-common.noarch                        1.6.7-2.el7                                   @base               
libX11-devel.x86_64                         1.6.7-2.el7                                   @base               
libXau.x86_64                               1.0.8-2.1.el7                                 @base               
libXau-devel.x86_64                         1.0.8-2.1.el7                                 @base               
libXdamage.x86_64                           1.1.4-4.1.el7                                 @base               
libXext.x86_64                              1.3.3-3.el7                                   @base               
libXfixes.x86_64                            5.0.3-1.el7                                   @base               
libXft.x86_64                               2.3.2-2.el7                                   @base               
libXft-devel.x86_64                         2.3.2-2.el7                                   @base               
libXi.x86_64                                1.7.9-1.el7                                   @base               
libXmu.x86_64                               1.1.2-2.el7                                   @base               
libXrender.x86_64                           0.9.10-1.el7                                  @base               
libXrender-devel.x86_64                     0.9.10-1.el7                                  @base               
libXt.x86_64                                1.1.5-3.el7                                   @base               
libXtst.x86_64                              1.2.3-1.el7                                   @base               
libXv.x86_64                                1.0.11-1.el7                                  @base               
libXxf86vm.x86_64                           1.1.4-1.el7                                   @base               
libacl.x86_64                               2.2.51-14.el7                                 @base               
libass.x86_64                               0.13.4-6.el7                                  @epel               
libassuan.x86_64                            2.1.0-3.el7                                   @base               
libasyncns.x86_64                           0.8-7.el7                                     @base               
libattr.x86_64                              2.4.46-13.el7                                 @base               
libavdevice.x86_64                          2.8.15-2.el7.nux                              @nux-dextop         
libblkid.x86_64                             2.23.2-61.el7_7.1                             @updates            
libcap.x86_64                               2.22-10.el7                                   @base               
libcap-ng.x86_64                            0.7.5-4.el7                                   @base               
libcap-ng-devel.x86_64                      0.7.5-4.el7                                   installed           
libcdio.x86_64                              0.92-3.el7                                    @base               
libcdio-paranoia.x86_64                     10.2+0.90-11.el7                              @base               
libcom_err.x86_64                           1.42.9-16.el7                                 @base               
libcom_err-devel.x86_64                     1.42.9-16.el7                                 @base               
libcroco.x86_64                             0.6.12-4.el7                                  @base               
libcurl.x86_64                              7.29.0-54.el7_7.1                             @updates            
libcurl-devel.x86_64                        7.29.0-54.el7_7.1                             @updates            
libdb.x86_64                                5.3.21-25.el7                                 @base               
libdb-utils.x86_64                          5.3.21-25.el7                                 @base               
libdb4.x86_64                               4.8.30-13.el7                                 @epel               
libdb4-devel.x86_64                         4.8.30-13.el7                                 @epel               
libdc1394.x86_64                            2.2.2-3.el7                                   @epel               
libdrm.x86_64                               2.4.97-2.el7                                  @base               
libedit.x86_64                              3.0-12.20121213cvs.el7                        @base               
libestr.x86_64                              0.1.9-2.el7                                   @base               
libev.x86_64                                4.15-7.el7                                    @extras             
libevent.x86_64                             2.0.21-4.el7                                  @base               
libevent-devel.x86_64                       2.0.21-4.el7                                  @base               
libfastjson.x86_64                          0.99.4-3.el7                                  @base               
libffi.x86_64                               3.0.13-18.el7                                 @base               
libffi-devel.x86_64                         3.0.13-18.el7                                 @base               
libgcc.x86_64                               4.8.5-39.el7                                  @base               
libgcrypt.x86_64                            1.5.3-14.el7                                  @base               
libgcrypt-devel.x86_64                      1.5.3-14.el7                                  @base               
libglvnd.x86_64                             1:1.0.1-0.8.git5baa1e5.el7                    @base               
libglvnd-egl.x86_64                         1:1.0.1-0.8.git5baa1e5.el7                    @base               
libglvnd-glx.x86_64                         1:1.0.1-0.8.git5baa1e5.el7                    @base               
libgomp.x86_64                              4.8.5-39.el7                                  @base               
libgpg-error.x86_64                         1.12-3.el7                                    @base               
libgpg-error-devel.x86_64                   1.12-3.el7                                    @base               
libicu.x86_64                               50.2-3.el7                                    @base               
libicu-devel.x86_64                         50.2-3.el7                                    @base               
libidn.x86_64                               1.28-4.el7                                    @base               
libjpeg-turbo.x86_64                        1.2.90-8.el7                                  @base               
libjpeg-turbo-devel.x86_64                  1.2.90-8.el7                                  @base               
libkadm5.x86_64                             1.15.1-37.el7_7.2                             @updates            
libmnl.x86_64                               1.0.3-7.el7                                   @base               
libmnl-devel.x86_64                         1.0.3-7.el7                                   @base               
libmodman.x86_64                            2.0.1-8.el7                                   @base               
libmount.x86_64                             2.23.2-61.el7_7.1                             @updates            
libmpc.x86_64                               1.0.1-3.el7                                   @base               
libnetfilter_conntrack.x86_64               1.0.6-1.el7_3                                 @updates            
libnfnetlink.x86_64                         1.0.1-4.el7                                   @base               
libogg.x86_64                               2:1.3.0-7.el7                                 @base               
libpcap.x86_64                              14:1.5.3-11.el7                               @base               
libpcap-devel.x86_64                        14:1.5.3-11.el7                               @base               
libpciaccess.x86_64                         0.14-1.el7                                    @base               
libpng.x86_64                               2:1.5.13-7.el7_2                              @base               
libpng-devel.x86_64                         2:1.5.13-7.el7_2                              @base               
libproxy.x86_64                             0.4.11-11.el7                                 @base               
libpwquality.x86_64                         1.2.3-5.el7                                   @base               
libraw1394.x86_64                           2.1.0-2.el7                                   @base               
libselinux.x86_64                           2.5-14.1.el7                                  @base               
libselinux-devel.x86_64                     2.5-14.1.el7                                  @base               
libselinux-python.x86_64                    2.5-14.1.el7                                  @base               
libselinux-utils.x86_64                     2.5-14.1.el7                                  @base               
libsemanage.x86_64                          2.5-14.el7                                    @base               
libsepol.x86_64                             2.5-10.el7                                    @base               
libsepol-devel.x86_64                       2.5-10.el7                                    @base               
libsmartcols.x86_64                         2.23.2-61.el7_7.1                             @updates            
libsndfile.x86_64                           1.0.25-10.el7                                 @base               
libssh2.x86_64                              1.8.0-3.el7                                   @base               
libstdc++.x86_64                            4.8.5-39.el7                                  @base               
libstdc++-devel.x86_64                      4.8.5-39.el7                                  @base               
libtasn1.x86_64                             4.10-1.el7                                    @base               
libtheora.x86_64                            1:1.1.1-8.el7                                 @base               
libtiff.x86_64                              4.0.3-32.el7                                  @base               
libtirpc.x86_64                             0.2.4-0.16.el7                                @base               
libtool-ltdl.x86_64                         2.4.2-22.el7_3                                @base               
libunistring.x86_64                         0.9.3-9.el7                                   @base               
libusbx.x86_64                              1.0.21-1.el7                                  @base               
libuser.x86_64                              0.60-9.el7                                    @base               
libutempter.x86_64                          1.1.6-4.el7                                   @base               
libuuid.x86_64                              2.23.2-61.el7_7.1                             @updates            
libuuid-devel.x86_64                        2.23.2-61.el7_7.1                             @updates            
libuv.x86_64                                1:1.33.0-2.el7                                @epel               
libuv-devel.x86_64                          1:1.33.0-2.el7                                @epel               
libv4l.x86_64                               0.9.5-4.el7                                   @base               
libva.x86_64                                1.8.3-1.el7                                   @base               
libvdpau.x86_64                             1.1.1-3.el7                                   @base               
libverto.x86_64                             0.2.5-4.el7                                   @base               
libverto-devel.x86_64                       0.2.5-4.el7                                   @base               
libvorbis.x86_64                            1:1.3.3-8.el7.1                               @base               
libwayland-client.x86_64                    1.15.0-1.el7                                  @base               
libwayland-server.x86_64                    1.15.0-1.el7                                  @base               
libwebp.x86_64                              0.3.0-7.el7                                   @base               
libwebp-devel.x86_64                        0.3.0-7.el7                                   @base               
libxcb.x86_64                               1.13-1.el7                                    @base               
libxcb-devel.x86_64                         1.13-1.el7                                    @base               
libxml2.x86_64                              2.9.1-6.el7_2.3                               @base               
libxml2-devel.x86_64                        2.9.1-6.el7_2.3                               @base               
libxml2-python.x86_64                       2.9.1-6.el7_2.3                               @base               
libxshmfence.x86_64                         1.2-1.el7                                     @base               
libxslt.x86_64                              1.1.28-5.el7                                  @base               
libxslt-devel.x86_64                        1.1.28-5.el7                                  @base               
libxslt-python.x86_64                       1.1.28-5.el7                                  @base               
logrotate.x86_64                            3.8.6-17.el7                                  @base               
lsof.x86_64                                 4.87-6.el7                                    @base               
lua.x86_64                                  5.1.4-15.el7                                  @base               
lz4.x86_64                                  1.7.5-3.el7                                   @base               
lz4-devel.x86_64                            1.7.5-3.el7                                   @base               
m4.x86_64                                   1.4.16-10.el7                                 installed           
make.x86_64                                 1:3.82-24.el7                                 @base               
mercurial.x86_64                            2.6.2-10.el7                                  @base               
mesa-libEGL.x86_64                          18.3.4-5.el7                                  @base               
mesa-libGL.x86_64                           18.3.4-5.el7                                  @base               
mesa-libgbm.x86_64                          18.3.4-5.el7                                  @base               
mesa-libglapi.x86_64                        18.3.4-5.el7                                  @base               
mpfr.x86_64                                 3.1.1-4.el7                                   @base               
nano.x86_64                                 2.3.1-10.el7                                  @base               
ncurses.x86_64                              5.9-14.20130511.el7_4                         @base               
ncurses-base.noarch                         5.9-14.20130511.el7_4                         @base               
ncurses-devel.x86_64                        5.9-14.20130511.el7_4                         @base               
ncurses-libs.x86_64                         5.9-14.20130511.el7_4                         @base               
neon.x86_64                                 0.30.0-4.el7                                  @base               
net-tools.x86_64                            2.0-0.25.20131004git.el7                      @base               
nettle.x86_64                               2.7.1-8.el7                                   @base               
nmap-ncat.x86_64                            2:6.40-19.el7                                 @base               
nspr.x86_64                                 4.21.0-1.el7                                  @base               
nspr-devel.x86_64                           4.21.0-1.el7                                  installed           
nss.x86_64                                  3.44.0-4.el7                                  @base               
nss-devel.x86_64                            3.44.0-4.el7                                  installed           
nss-pem.x86_64                              1.0.3-7.el7                                   @base               
nss-softokn.x86_64                          3.44.0-5.el7                                  @base               
nss-softokn-devel.x86_64                    3.44.0-5.el7                                  installed           
nss-softokn-freebl.x86_64                   3.44.0-5.el7                                  @base               
nss-softokn-freebl-devel.x86_64             3.44.0-5.el7                                  installed           
nss-sysinit.x86_64                          3.44.0-4.el7                                  @base               
nss-tools.x86_64                            3.44.0-4.el7                                  @base               
nss-util.x86_64                             3.44.0-3.el7                                  @base               
nss-util-devel.x86_64                       3.44.0-3.el7                                  installed           
ntp.x86_64                                  4.2.6p5-29.el7.centos                         @base               
ntpdate.x86_64                              4.2.6p5-29.el7.centos                         @base               
numactl-libs.x86_64                         2.0.12-3.el7_7.1                              @updates            
nux-dextop-release.noarch                   0-5.el7.nux                                   installed           
openal-soft.x86_64                          1.16.0-3.el7                                  @epel               
opencore-amr.x86_64                         0.1.3-3.el7.nux                               @nux-dextop         
openjpeg-libs.x86_64                        1.5.1-18.el7                                  @base               
openldap.x86_64                             2.4.44-21.el7_6                               @base               
openssh.x86_64                              7.4p1-21.el7                                  @base               
openssh-clients.x86_64                      7.4p1-21.el7                                  @base               
openssh-server.x86_64                       7.4p1-21.el7                                  @base               
openssl.x86_64                              1:1.0.2k-19.el7                               @base               
openssl-devel.x86_64                        1:1.0.2k-19.el7                               @base               
openssl-libs.x86_64                         1:1.0.2k-19.el7                               @base               
opus.x86_64                                 1.0.2-6.el7                                   @base               
orc.x86_64                                  0.4.26-1.el7                                  @base               
p11-kit.x86_64                              0.23.5-3.el7                                  @base               
p11-kit-trust.x86_64                        0.23.5-3.el7                                  @base               
pakchois.x86_64                             0.4-10.el7                                    @base               
pam.x86_64                                  1.1.8-22.el7                                  @base               
pam-devel.x86_64                            1.1.8-22.el7                                  @base               
passwd.x86_64                               0.79-5.el7                                    @base               
pcre.x86_64                                 8.32-17.el7                                   @base               
pcre-devel.x86_64                           8.32-17.el7                                   @base               
perl.x86_64                                 4:5.16.3-294.el7_6                            @base               
perl-Carp.noarch                            1.26-244.el7                                  @base               
perl-Data-Dumper.x86_64                     2.145-3.el7                                   @base               
perl-Encode.x86_64                          2.51-7.el7                                    @base               
perl-Error.noarch                           1:0.17020-2.el7                               @base               
perl-Exporter.noarch                        5.68-3.el7                                    @base               
perl-File-Path.noarch                       2.09-2.el7                                    @base               
perl-File-Temp.noarch                       0.23.01-3.el7                                 @base               
perl-Filter.x86_64                          1.49-3.el7                                    @base               
perl-Getopt-Long.noarch                     2.40-3.el7                                    @base               
perl-Git.noarch                             1.8.3.1-20.el7                                @base               
perl-HTTP-Tiny.noarch                       0.033-3.el7                                   @base               
perl-PathTools.x86_64                       3.40-5.el7                                    @base               
perl-Pod-Escapes.noarch                     1:1.04-294.el7_6                              @base               
perl-Pod-Perldoc.noarch                     3.20-4.el7                                    @base               
perl-Pod-Simple.noarch                      1:3.28-4.el7                                  @base               
perl-Pod-Usage.noarch                       1.63-3.el7                                    @base               
perl-Scalar-List-Utils.x86_64               1.27-248.el7                                  @base               
perl-Socket.x86_64                          2.010-4.el7                                   @base               
perl-Storable.x86_64                        2.45-3.el7                                    @base               
perl-TermReadKey.x86_64                     2.30-20.el7                                   @base               
perl-Test-Harness.noarch                    3.28-3.el7                                    @base               
perl-Text-ParseWords.noarch                 3.29-4.el7                                    @base               
perl-Thread-Queue.noarch                    3.02-2.el7                                    @base               
perl-Time-HiRes.x86_64                      4:1.9725-3.el7                                @base               
perl-Time-Local.noarch                      1.2300-2.el7                                  @base               
perl-constant.noarch                        1.27-2.el7                                    @base               
perl-libs.x86_64                            4:5.16.3-294.el7_6                            @base               
perl-macros.x86_64                          4:5.16.3-294.el7_6                            @base               
perl-parent.noarch                          1:0.225-244.el7                               @base               
perl-podlators.noarch                       2.5.1-3.el7                                   @base               
perl-threads.x86_64                         1.87-4.el7                                    @base               
perl-threads-shared.x86_64                  1.43-6.el7                                    @base               
pinentry.x86_64                             0.8.1-17.el7                                  @base               
pkgconfig.x86_64                            1:0.27.1-4.el7                                @base               
policycoreutils.x86_64                      2.5-33.el7                                    @base               
popt.x86_64                                 1.13-16.el7                                   @base               
ppp.x86_64                                  2.4.5-33.el7                                  installed           
procps-ng.x86_64                            3.3.10-26.el7_7.1                             @updates            
pth.x86_64                                  2.0.7-23.el7                                  @base               
pulseaudio-libs.x86_64                      10.0-5.el7                                    @base               
pygpgme.x86_64                              0.3-9.el7                                     @base               
pyliblzma.x86_64                            0.5.3-11.el7                                  @base               
python.x86_64                               2.7.5-86.el7                                  @base               
python-chardet.noarch                       2.2.1-3.el7                                   @base               
python-decorator.noarch                     3.4.0-3.el7                                   @base               
python-devel.x86_64                         2.7.5-86.el7                                  @base               
python-firewall.noarch                      0.6.3-2.el7_7.2                               @updates            
python-gevent.x86_64                        1.0-3.el7                                     @extras             
python-gobject-base.x86_64                  3.22.0-1.el7_4.1                              @base               
python-greenlet.x86_64                      0.4.2-4.el7                                   @extras             
python-iniparse.noarch                      0.4-9.el7                                     @base               
python-kitchen.noarch                       1.1.1-5.el7                                   @base               
python-libs.x86_64                          2.7.5-86.el7                                  @base               
python-pillow.x86_64                        2.0.0-19.gitd1c6db8.el7                       @base               
python-pycurl.x86_64                        7.19.0-19.el7                                 @base               
python-rpm-macros.noarch                    3-32.el7                                      @base               
python-slip.noarch                          0.4.0-4.el7                                   @base               
python-slip-dbus.noarch                     0.4.0-4.el7                                   @base               
python-srpm-macros.noarch                   3-32.el7                                      @base               
python-urlgrabber.noarch                    3.10-9.el7                                    @base               
python2-rpm-macros.noarch                   3-32.el7                                      @base               
python3.x86_64                              3.6.8-10.el7                                  @base               
python3-libs.x86_64                         3.6.8-10.el7                                  @base               
python3-pip.noarch                          9.0.3-5.el7                                   @base               
python3-setuptools.noarch                   39.2.0-10.el7                                 @base               
pyxattr.x86_64                              0.5.1-5.el7                                   @base               
qrencode-libs.x86_64                        3.4.1-3.el7                                   @base               
readline.x86_64                             6.2-11.el7                                    @base               
readline-devel.x86_64                       6.2-11.el7                                    @base               
rootfiles.noarch                            8.1-11.el7                                    @base               
rpm.x86_64                                  4.11.3-40.el7                                 @base               
rpm-build-libs.x86_64                       4.11.3-40.el7                                 @base               
rpm-libs.x86_64                             4.11.3-40.el7                                 @base               
rpm-python.x86_64                           4.11.3-40.el7                                 @base               
rsync.x86_64                                3.1.2-6.el7_6.1                               @base               
rsyslog.x86_64                              8.24.0-41.el7_7.2                             @updates            
schroedinger.x86_64                         1.0.11-4.el7                                  @epel               
screen.x86_64                               4.1.0-0.25.20120314git3c2946.el7              @base               
sed.x86_64                                  4.2.2-5.el7                                   @base               
setup.noarch                                2.8.71-10.el7                                 @base               
shadow-utils.x86_64                         2:4.6-5.el7                                   @base               
shared-mime-info.x86_64                     1.8-4.el7                                     @base               
soxr.x86_64                                 0.1.2-1.el7                                   @epel               
speedtest.x86_64                            1.0.0.2_1.5ae238b-1                           @bintray--ookla-rhel
speex.x86_64                                1.2-0.19.rc1.el7                              @base               
sqlite.x86_64                               3.7.17-8.el7                                  @base               
sqlite-devel.x86_64                         3.7.17-8.el7                                  @base               
ssmtp.x86_64                                2.64-14.el7                                   @epel               
subversion.x86_64                           1.7.14-14.el7                                 @base               
subversion-libs.x86_64                      1.7.14-14.el7                                 @base               
systemd.x86_64                              219-67.el7_7.2                                @updates            
systemd-devel.x86_64                        219-67.el7_7.2                                @updates            
systemd-libs.x86_64                         219-67.el7_7.2                                @updates            
systemd-python.x86_64                       219-67.el7_7.2                                @updates            
systemd-sysv.x86_64                         219-67.el7_7.2                                @updates            
sysvinit-tools.x86_64                       2.88-14.dsf.el7                               @base               
tar.x86_64                                  2:1.26-35.el7                                 @base               
tcl.x86_64                                  1:8.5.13-8.el7                                @base               
tcl-devel.x86_64                            1:8.5.13-8.el7                                @base               
tcp_wrappers-libs.x86_64                    7.6-77.el7                                    @base               
tk.x86_64                                   1:8.5.13-6.el7                                @base               
tk-devel.x86_64                             1:8.5.13-6.el7                                @base               
trousers.x86_64                             0.3.14-2.el7                                  @base               
tzdata.noarch                               2019c-1.el7                                   @updates            
unzip.x86_64                                6.0-20.el7                                    @base               
ustr.x86_64                                 1.0.4-16.el7                                  @base               
util-linux.x86_64                           2.23.2-61.el7_7.1                             @updates            
vim-common.x86_64                           2:7.4.629-6.el7                               @base               
vim-enhanced.x86_64                         2:7.4.629-6.el7                               @base               
vim-filesystem.x86_64                       2:7.4.629-6.el7                               @base               
vim-minimal.x86_64                          2:7.4.629-6.el7                               @base               
virt-what.x86_64                            1.18-4.el7                                    @base               
vo-amrwbenc.x86_64                          0.1.2-1.el7.nux                               @nux-dextop         
wget.x86_64                                 1.14-18.el7_6.1                               @base               
which.x86_64                                2.20-7.el7                                    @base               
x264-libs.x86_64                            0.142-11.20141221git6a301b6.el7.nux           @nux-dextop         
x265-libs.x86_64                            1.9-1.el7.nux                                 @nux-dextop         
xl2tpd.x86_64                               1.3.14-1.el7                                  @epel               
xorg-x11-proto-devel.noarch                 2018.4-1.el7                                  @base               
xvidcore.x86_64                             1.3.2-5.el7.nux                               @nux-dextop         
xz.x86_64                                   5.2.2-1.el7                                   @base               
xz-devel.x86_64                             5.2.2-1.el7                                   @base               
xz-libs.x86_64                              5.2.2-1.el7                                   @base               
yum.noarch                                  3.4.3-163.el7.centos                          @base               
yum-metadata-parser.x86_64                  1.1.4-10.el7                                  @base               
yum-plugin-fastestmirror.noarch             1.1.31-52.el7                                 @base               
yum-utils.noarch                            1.1.31-52.el7                                 @base               
zip.x86_64                                  3.0-11.el7                                    @base               
zlib.x86_64                                 1.2.7-18.el7                                  @base               
zlib-devel.x86_64                           1.2.7-18.el7                                  @base               
[root@CentOS ~]# 
```

## 0x14.引用
> [从零开始的 Rust 学习笔记(10) —— Breezin](https://web.archive.org/web/20191204110834/https://blog.0xbbc.com/2019/12/rust-learning-from-zero-10/)

未完待续……