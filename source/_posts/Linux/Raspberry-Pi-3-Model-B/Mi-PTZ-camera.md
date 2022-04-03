---
title: 米家摄像机云台版同步腾讯云 COS
date: 2020-1-22 19:07:58
tags:
  - Mi
count: 3
os: 0
os_1: 10.0.17763.973 2019-LTSC
browser: 0
browser_1: 74.0.3729.169 Stable
place: 新家
key: 71
---
    狗东 110-100 白条券使用完毕
    然后 19 年的社畜终于结束了草
<!-- more -->
## 0x00.前言
前阵子“非你莫鼠”领到了`110-100`白条优惠券，家里暂时也不需要米、面、油了，想着过年回家一周还得看着这面的情况（`7x24h`不断电的`rpi`以及`远程唤醒`台式机`(〃'▽'〃)`
所以就种草了个这玩楞，然鹅`199`草，看了下价格变化曲线感觉有戏，今天凌晨果然降价，于是立即购买！`(๑*◡*๑)`
![真·标准矩形价格曲线](https://i1.yuangezhizao.cn/Win-10/20200122191606.jpg!webp)
![于是等到凌晨果然降价](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-22-00-07-30-633_com.jingdong.a.jpg!webp)
![-100](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-22-00-12-20-406_com.jingdong.a.jpg!webp)
![一折？](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-22-00-12-48-503_com.jingdong.a.jpg!webp)
![赶紧把快过期的红包勾上](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-22-00-13-12-025_com.jingdong.a.jpg!webp)

预计下午配送，结果早上起来就发现到配送站了，于是立即`wx`联系说家里白天不会有人就扔蜂巢吧……晚上回来就拿到了`(￣▽￣)~*`
![你米外包装](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20200122_180749.jpg!view)

## 0x01.上电
`5V 1A`插菊花，然后这玩楞就突然发出响（语）声（音）草，倒是可海星没有太沙雕，掏出手机扫码再把屏幕上的码给摄像头扫（互扫嘛）就`ok`了`(＾＿－)`
其中还不支持`5G WiFi`还是有点儿遗憾（~~都上`H.265`视频编码了就不能支持下`5G`么草~~，后来才想到`5G`穿墙硬伤

![no 5G](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-22-18-15-38-682_com.xiaomi.sma.jpg!webp)

然后就日常升级固件到最新（毕竟新电子产品拿到手的第一步基本上都是更到最新，即使这并不一定是一个好习惯
![3.5.8_0415](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-22-18-23-01-189_com.xiaomi.sma.jpg!webp)

~~`0415`警觉，区号？~~然后就摸索`App`发现没插存储卡，然后……没找着插槽（一脸黑人问号`⊙▃⊙`
翻了半天开始怀疑人生自己是不是买错了，结果后来搜索到了结果（`(╯°Д°)╯︵┻━┻`

![这个 SD 卡槽的位置真是绝了](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20200122_183010.jpg!view)
![草](https://i1.yuangezhizao.cn/Win-10/20191016005155.jpg!webp)

（忘记先断电就直接）插……入……，之后提示异常，格式化之后就能使了（之前这张卡是给`rpi`做`OSMC`系统的
虽然已经是买的能力范围内最好的卡了，但是限于`3b`的硬件性能（不限于`GPU`）自第一次验证可行性之后就再也没用过了
当然，现在`rpi`装的是最新的官方系统，优化吊炸天异常丝滑，虽然是`32`位系统罢了`(￣.￣)`
于是这张闲置的卡就拿来做摄像头的本地存储了，好歹是`U1`的卡（应该是`Class 10`

![28.8G](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-22-18-32-00-328_com.xiaomi.sma.jpg!webp)

## 0x02.私有云存储
看了下`rpi`的剩余空间，结果还没有存储卡大（废话，毕竟都是`32G`的
``` bash
pi@rpi:~ $ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/root        29G   11G   16G  41% /
devtmpfs        370M     0  370M   0% /dev
tmpfs           374M     0  374M   0% /dev/shm
tmpfs           374M   39M  336M  11% /run
tmpfs           5.0M  4.0K  5.0M   1% /run/lock
tmpfs           374M     0  374M   0% /sys/fs/cgroup
/dev/mmcblk0p1  253M   52M  201M  21% /boot
tmpfs            75M     0   75M   0% /run/user/1000
```
于是准备干脆扔到`COS`上算了，立即开通存储桶
![私有读写 + 服务端加密](https://i1.yuangezhizao.cn/Win-10/20200122201740.png!webp)

### 1.安装[COSFS](https://github.com/tencentyun/cosfs)
先安装编译工具
``` bash
sudo apt install automake autotools-dev g++ git libcurl4-gnutls-dev libfuse-dev libssl-dev libxml2-dev make pkg-config fuse -y
```
然后下载源码编译安装，一气呵成（笑
<details><summary>点击此处 ← 查看终端</summary>

``` bash
pi@rpi:~/Downloads $ git clone https://github.com/tencentyun/cosfs.git
<rm>
pi@rpi:~/Downloads $ cd cosfs/
pi@rpi:~/Downloads/cosfs $ ./autogen.sh
<rm>
pi@rpi:~/Downloads/cosfs $ ./configure
<rm>
pi@rpi:~/Downloads/cosfs $ make
<rm>
pi@rpi:~/Downloads/cosfs $ sudo make install
<rm>
```
</details>

新建配置文件
```
echo rpi-<rm>:<rm>:<rm> > passwd-cosfs
sudo mv passwd-cosfs /etc/passwd-cosfs
chmod 640 /etc/passwd-cosfs
```
挂载启动
```
mkdir /tmp/cosfs
cosfs rpi-<rm> /tmp/cosfs -ourl=http://cos.ap-beijing.myqcloud.com -odbglevel=info -ouse_cache=/path/to/local_cache
```
> `-ouse_cache`指定了使用本地`cache`来缓存临时文件，进一步提高性能，如果不需要本地`cache`或者本地磁盘容量有限，可不指定该选项

### 2.安装`SMB`
``` bash
sudo apt install samba
```
安装过程中会弹框
![这里选是](https://i1.yuangezhizao.cn/Win-10/20200122185805.jpg!webp)

修改配置文件`sudo vim /etc/samba/smb.conf`如下
``` bash
#======================= Share Definitions =======================

[rpi]
   path = /tmp/cosfs
   comment = COSFS
   browseable = yes

# By default, the home directories are exported read-only. Change the
# next parameter to 'no' if you want to be able to write to them.
#   read only = no
   writeable = yes

# File creation mask is set to 0700 for security reasons. If you want to
# create files with group=rw permissions, set next parameter to 0775.
   create mask = 0700

# Directory creation mask is set to 0700 for security reasons. If you want to
# create dirs. with group=rw permissions, set next parameter to 0775.
   directory mask = 0700

# By default, \\server\username shares can be connected to by anyone
# with access to the samba server.
# The following parameter makes sure that only "username" can connect
# to \\server\username
# This might need tweaking when using external authentication schemes
   valid users = pi
   public = yes

```
添加`pi`用户
``` bash
pi@rpi:~ $ sudo smbpasswd -a pi
New SMB password:
Retype new SMB password:
Added user pi.
```
重启服务
```
sudo samba restart
```

### 3.远程访问
这里的构想是远程连接`rpi`的`SMB`，然后`SMB`指向的是`COS`，这样就不占用本地的任何空间了
结果并不能这么搞，草死（原因之后再调查`(╯°Д°)╯︵┻━┻`
没办法只能`/home/pi/Videos/Mi`
![选设备](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-22-20-43-48-689_com.xiaomi.sma.jpg!webp)
![选文件夹](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-22-20-44-07-472_com.xiaomi.sma.jpg!webp)
![同步设置](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-22-21-09-12-674_com.xiaomi.sma.jpg!webp)
![传输正常](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-22-22-58-56-173_com.xiaomi.sma.jpg!webp)

这里的显示有问题……亲测选择实时之后就会立即传输了（大概每次传输`7M`进行分割
然后更改设置之后，需要手动关闭再开启`视频存储`开关
![Windows 挂载](https://i1.yuangezhizao.cn/Win-10/20200122211129.jpg!webp)

因此，现在只能`cp -r xiaomi_camera_videos/ /tmp/cosfs/`之后清空视频文件了
![COS](https://i1.yuangezhizao.cn/Win-10/20200122213122.png!webp)

设置`1h`的频率然后写个脚本扔`cron`里就`ok`了
> 至此本文使命完成

![去 tm 的云存储 VIP](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-01-22-21-18-02-533_com.xiaomi.sma.jpg!webp)

## 0x03.后记
姿势不对，后期探索`ヽ(^_−)ﾉ`
初见竟然`2.5h`就写完了全文，「五星好评，下次还来」
`2020-3-31 21:27:16`：
去翻了下现在的文件夹列表
![5ce50c592cb6](https://i1.yuangezhizao.cn/Win-10/20200331212901.png!webp)

因为去年白嫖的资源包明天到期。。。
![200.00 GB](https://i1.yuangezhizao.cn/Win-10/20200331213606.jpg!webp)

其实也只用到了`163 GB`而已，而`rpi`就占了`55 GB`
![数据监控](https://i1.yuangezhizao.cn/Win-10/20200331213649.jpg!webp)
![存储桶数据概览](https://i1.yuangezhizao.cn/Win-10/20200331213757.jpg!webp)

于是去看看氪金的价格，**归档存储**倒是不贵
![产品定价](https://i1.yuangezhizao.cn/Win-10/20200331213450.jpg!webp)
![COS资源包](https://i1.yuangezhizao.cn/Win-10/20200331215954.jpg!webp)
![COS资源包](https://i1.yuangezhizao.cn/Win-10/20200331214520.jpg!webp)

然后去翻活动页面，氪了个`1`元`50 GB`的`6`个月时长的标准存储包（自然就没有买归档包
![好活动](https://i1.yuangezhizao.cn/Win-10/20200331215032.jpg!webp)
![还不错](https://i1.yuangezhizao.cn/Win-10/20200331214854.jpg!webp)
![1](https://i1.yuangezhizao.cn/Win-10/20200331214929.jpg!webp)
![50.00GB](https://i1.yuangezhizao.cn/Win-10/20200331215302.jpg!webp)
![25](https://i1.yuangezhizao.cn/Win-10/20200331221325.jpg!webp)

在加上之前的`50 GB`额度就正好凑足`100 GB`了，然后前天莫名提示`90%`？？？
![老用户福利](https://i1.yuangezhizao.cn/Win-10/20200331220448.jpg!webp)
![？](https://i1.yuangezhizao.cn/Win-10/20200331220705.jpg!webp)

于是现在的任务就变成了干掉`63.56 GB`……先从`81.15GB`的`video`存储桶下手吧，为什么是它呢？因为之前测试转存的时候屯了一个超多分`P`的`maimai`手元视频
屯完之后懒得管，不过现在是时候处理下了……
![刷屏草](https://i1.yuangezhizao.cn/Win-10/20200331221714.jpg!webp)
![前缀搜索](https://i1.yuangezhizao.cn/Win-10/20200331221819.png!webp)
![搞定](https://i1.yuangezhizao.cn/Win-10/20200331222705.jpg!webp)
