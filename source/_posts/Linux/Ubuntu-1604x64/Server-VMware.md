---
title: VMware 安装 Ubuntu Server 16.04 x64
date: 2018-2-23 11:22:26
tags:
  - Ubuntu
  - VMware
count: 1
os: 0
os_1: 10.0.14393 2016-LTSB
browser: 0
browser_1: 64.0.3282.140 Stable
place: 家
key: 32
---
    多图预警
<!-- more -->
## 0x00.安装

![](https://i1.yuangezhizao.cn/Win-10/20180223112530.png!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223112632.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223112651.jpg!webp)

![](https://i1.yuangezhizao.cn/Win-10/20180223112900.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223112934.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223113007.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223113030.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223113046.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223113100.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223113111.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223113134.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223113147.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223113215.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223113227.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223113245.jpg!webp)

![](https://i1.yuangezhizao.cn/Win-10/20180223113304.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223113349.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223113538.jpg!webp)

![](https://i1.yuangezhizao.cn/Win-10/20180223113636.jpg!webp)

![](https://i1.yuangezhizao.cn/Win-10/20180223113717.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223113752.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223113815.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223113831.jpg!webp)

![](https://i1.yuangezhizao.cn/Win-10/20180223113959.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223114045.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223114100.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223114113.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223114420.jpg!webp)

![](https://i1.yuangezhizao.cn/Win-10/20180223114503.jpg!webp)

![](https://i1.yuangezhizao.cn/Win-10/20180223114546.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223114605.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223114644.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223114704.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223114724.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223114747.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223114859.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223115112.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223115125.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223115219.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223115256.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223115325.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223115531.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223115559.jpg!webp)

![](https://i1.yuangezhizao.cn/Win-10/20180223115624.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223115705.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223115854.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223120103.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223120147.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223120211.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20180223120258.jpg!webp)

## 0x02.配置
`free -m`
一会再改这个
`sudo apt-get update`
`sudo apt-get upgrade`

## 0x03.修改时区
``` shell
yuangezhizao@Ubuntu:~$ tzselect
Please identify a location so that time zone rules can be set correctly.
Please select a continent, ocean, "coord", or "TZ".
 1) Africa
 2) Americas
 3) Antarctica
 4) Asia
 5) Atlantic Ocean
 6) Australia
 7) Europe
 8) Indian Ocean
 9) Pacific Ocean
10) coord - I want to use geographical coordinates.
11) TZ - I want to specify the time zone using the Posix TZ format.
#? 4
Please select a country whose clocks agree with yours.
 1) Afghanistan		  18) Israel		    35) Palestine
 2) Armenia		  19) Japan		    36) Philippines
 3) Azerbaijan		  20) Jordan		    37) Qatar
 4) Bahrain		  21) Kazakhstan	    38) Russia
 5) Bangladesh		  22) Korea (North)	    39) Saudi Arabia
 6) Bhutan		  23) Korea (South)	    40) Singapore
 7) Brunei		  24) Kuwait		    41) Sri Lanka
 8) Cambodia		  25) Kyrgyzstan	    42) Syria
 9) China		  26) Laos		    43) Taiwan
10) Cyprus		  27) Lebanon		    44) Tajikistan
11) East Timor		  28) Macau		    45) Thailand
12) Georgia		  29) Malaysia		    46) Turkmenistan
13) Hong Kong		  30) Mongolia		    47) United Arab Emirates
14) India		  31) Myanmar (Burma)	    48) Uzbekistan
15) Indonesia		  32) Nepal		    49) Vietnam
16) Iran		  33) Oman		    50) Yemen
17) Iraq		  34) Pakistan
#? 9
Please select one of the following time zone regions.
1) Beijing Time
2) Xinjiang Time
#? 1

The following information has been given:

	China
	Beijing Time

Therefore TZ='Asia/Shanghai' will be used.
Local time is now:	Fri Feb 23 18:32:22 CST 2018.
Universal Time is now:	Fri Feb 23 10:32:22 UTC 2018.
Is the above information OK?
1) Yes
2) No
#? 1

You can make this change permanent for yourself by appending the line
	TZ='Asia/Shanghai'; export TZ
to the file '.profile' in your home directory; then log out and log in again.

Here is that TZ value again, this time on standard output so that you
can use the /usr/bin/tzselect command in shell scripts:
Asia/Shanghai
yuangezhizao@Ubuntu:~$ sudo hwclock -w
```


## 0x04.安装 & 配置`MySQL`
`apt-get install mysql-server`
![设置密码](https://i1.yuangezhizao.cn/Win-10/20180223195017.png!webp)
![再次确认](https://i1.yuangezhizao.cn/Win-10/20180223195101.png!webp)

测试是否安装成功：
`netstat -tap | grep mysql`
设置外网访问：
`vim /etc/mysql/mysql.conf.d/mysqld.cnf`
注释`# bind-address = 127.0.0.1`
修改字符集
```
[mysqld]
character_set_server=utf8
```
进入`MySQL`：
```
mysql -uroot -p密码
grant all on *.* to root@'%' identified by '密码' with grant option;
flush privileges;
quit
```
重启`MySQL`：`service mysql restart`


## 0x05.安装`Redis`
`sudo apt install redis-server`
设置密码以及外网访问
`sudo vim /etc/redis/redis.conf`
`# requirepass foobared`去掉`#`号注释，把`foobared`替换为密码。
`#bind 127.0.0.1`注释
`databases 5`
重启服务：`sudo systemctl restart redis`
