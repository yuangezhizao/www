---
title: 基于 NodeMCU + DHT11 搭建物联网温湿度监控系统
date: 2019-7-31 21:41:34
tags:
  - NodeMCU
  - DHT11
count: 1
os: 0
os_1: 10.0.17763.652 2019-LTSC
browser: 0
browser_1: 74.0.3729.169 Stable
place: 新家
key: 54
---
    祭出 ESP8266 神器
<!-- more -->
## 0x00.前言
去翻从家带来的硬件小玩楞，突然发现`DHT11`，只可惜拿`DHN`的`STM32`连上并不是很好用，于是自己又网购了一波，顺便终于淘了个`8266`留给自己用。当初大三比赛用的是`51`+`DS18B20`再加`pc`的组合，后来比赛结束变成了加`rpi`的组合，结果到现在彻底换成了`NodeMCU`+`DHT11`的组合，`8266nb！`
![tb 并不是很贵的说](https://i1.yuangezhizao.cn/Win-10/20190731215649.jpg!webp)

这里说明一点，`NodeMCU`中的`Node`与我们所熟知的`Node.js`并没有关系，没想到吧`hhh`，骚年……
但是是基于`Lua`语言的（写到这里想到了貌似也有基于`Python`的开发板，`py`大法好！
`2019-8-18 20:54:41`又买了一套扔`WZ`屋里用
![19.4 一套](https://i1.yuangezhizao.cn/Win-10/20190818205558.jpg!webp)
![未拆](https://i1.yuangezhizao.cn/Lenovo-Z5/IMG_20190818_205754.jpg!webp)
![正面](https://i1.yuangezhizao.cn/Lenovo-Z5/IMG_20190818_205826.jpg!webp)
![背面](https://i1.yuangezhizao.cn/Lenovo-Z5/IMG_20190818_205905.jpg!webp)

`2019-9-21 23:15:41`由于中秋节自己带回去的那套扔家里了所以就又又买了一套给自己玩
![终于买继电器了](https://i1.yuangezhizao.cn/Win-10/20190921230857.jpg!webp)
![正面](https://i1.yuangezhizao.cn/Lenovo-Z5/IMG_20190921_234033.jpg!webp)
![背面](https://i1.yuangezhizao.cn/Lenovo-Z5/IMG_20190921_234051.jpg!webp)

## 0x01.[NodeMCU](http://www.nodemcu.com/index_cn.html)
> 超简单的物联网开发平台

一款开源快速硬件原型平台，包括固件和开发板，用几行简单的`Lua`脚本就能开发物联网应用
一、特点：
1. 像`Arduino`一样操作硬件`IO`
提供硬件的高级接口，可以将应用开发者从繁复的硬件配置、寄存器操作中解放出来。用交互式`Lua`脚本，像`arduino`一样编写硬件代码！
2. 用`Nodejs`类似语法写网络应用
事件驱动型`API`极大的方便了用户进行网络应用开发，使用类似`Nodejs`的方式编写网络代码，并运行于`5mm*5mm`大小的`MCU`之上，加快您的物联网开发进度。
3. 超低成本的`WI-FI`模块
用于快速原型的开发板，集成了售价低于`10`人民币`WIFI`芯片`ESP8266`。我们为您提供性价比最高的物联网应用开发平台。

二、开发板
1. 基于乐鑫`esp8266`的`NodeMcu`开发板，具有`GPIO`、`PWM`、`I2C`、`1-Wire`、`ADC`等功能，结合`NodeMcu`固件为您的原型开发提供最快速的途径。
2. 包含`usb`串口，即插即用
3. `10 GPIO`, 每个都能配置为`PWM`，`I2C`，`1-wire`
4. `FCC`认证的`WI-FI`模块，内置`PCB`天线

## 0x02.[官方文档](https://nodemcu.readthedocs.io/en/master/)
看到`Basics`里面的`Getting started`了吗？三部曲走起
> Getting Started aka NodeMCU Quick Start
The basic process to get started with NodeMCU consists of the following three steps.
1. Build the firmware with the modules you need
2. Flash the firmware to the chip
3. Upload code to the device.

#### [上云编译](https://nodemcu-build.com/)
云端定制固件，你值得拥有！
![要用谷歌邮箱，腾讯邮箱可不行](https://i1.yuangezhizao.cn/Win-10/20190818212200.jpg!webp)

注意`master`和`dev`与`gh`上的代码库是同步的，因此随着时间的推移会有部分语法的差别（基本上网上的例程直接跑都会报错需要小修小改尤其是带`tmr`的），在这里暂时选择`1.5.4.1-final (frozen, for 512KB flash)`
以上是花了半下午的时间~~（公司摸鱼）~~远程连接到家里的电脑之后反复编译，下载试出来的（到最后谷歌邮箱接收的固件直接`404`不让下载也是绝了`2333`
![勾选模块，注意红框](https://i1.yuangezhizao.cn/Win-10/20190818212437.jpg!webp)

`DHT`和`HTTP`不是默认自带的，
![TLS 可以勾上](https://i1.yuangezhizao.cn/Win-10/20190818212620.jpg!webp)

编译开始与完成之时会分别收到邮件：
![finished](https://i1.yuangezhizao.cn/Win-10/20190813200048.jpg!webp)

```
Strike!
You successfully commissioned a NodeMCU custom build from the dev branch. You selected the following 15 modules: cron crypto dht encoder enduser_setup file gpio http mqtt net node tmr uart websocket wifi.

We'll keep you posted by email about the progress of your build.

In the meantime I suggest you take a look at the build stats to find out how your firmware configuration compares to others in the community.
```
> This was built against the dev branch and includes the following modules: cron, crypto, dht, encoder, enduser_setup, file, gpio, http, mqtt, net, node, tmr, uart, websocket, wifi, tls.

`float`与`integer`具体选哪个好？在这里我选了前者，在`print`的时候字符串格式化会有差异

#### [NodeMCU PyFlasher](https://github.com/marcelstoer/nodemcu-pyflasher)烧录
其实这玩楞就是个`esptool.py`的图形化封装
![Flash NodeMCU](https://i1.yuangezhizao.cn/Win-10/20190813200545.jpg!webp)

#### [ESPlorer](https://github.com/4refr0nt/ESPlorer)连接
`pc`需要`CH340`的驱动，这里是`COM4`，波特率`115200`
首次连接可以按一下板子上的`RST`复位键，并且下载完成应该会提示`lua: cannot open init.lua`
~~我这里之前传过了所以不会有这个提示。现在懒得截图，之后再补吧……~~
![Communication](https://i1.yuangezhizao.cn/Win-10/20190813200956.jpg!webp)

## 0x03.代码
> 注：本文所有代码均经过测试并已通过运行验证
#### [连接`WiFi`](https://nodemcu.readthedocs.io/en/master/modules/wifi/)
法一、初级：先定义函数，后在参数中引用
``` lua
print('[WiFi]Setting...')
wifi.setmode(wifi.STATION)
wifi.sta.config{ssid="SUT", pwd="<rm>"}
print('[WiFi]Connecting...')
wifi.sta.connect()

function getip()
    if wifi.sta.getip() == nil then
        print('[WiFi]Waiting（2s）...')
    else
        print('[WiFi]Connected at：' .. wifi.sta.getip())
        tmr.stop(1)
    end
end

tmr.alarm(1, 2000, tmr.ALARM_AUTO, getip)
```
法二、高级：匿名函数直接写入参数
``` lua
print('[WiFi]Setting...')
wifi.setmode(wifi.STATION)
wifi.sta.config{ssid="SUT", pwd="<rm>"}
print('[WiFi]Connecting...')
wifi.sta.connect()

tmr.alarm(1, 2000, tmr.ALARM_AUTO, function()
    if wifi.sta.getip() == nil then
        print('[WiFi]Waiting（2s）...')
    else
        print('[WiFi]Connected at：' .. wifi.sta.getip())
    tmr.stop(1)
    end
end)
```
然后你就可以活学活用下了：
``` lua
print("[WiFi]Scanning...")

function connect(t)
    for k, v in pairs(t) do
        print(k.."："..v)
        if k == "SUT" then
            print("[WiFi]Setting...")
            wifi.sta.config{ssid="SUT", pwd="<rm>"}
            print("[WiFi]Connecting...")
            wifi.sta.connect()
            tmr.alarm(1, 2000, tmr.ALARM_AUTO, get_ip)
            break
        else
            print("[WiFi]Unavailable AP...")
        end
    end
end


function get_ip()
    if wifi.sta.getip() == nil then
        print("[WiFi]Waiting（2s）...")
    else
        print("[WiFi]Connected："..wifi.sta.getip())
        tmr.stop(1)
    end
end

wifi.setmode(wifi.STATION)
wifi.sta.getap(connect)
```
#### [温湿度传感器](https://nodemcu.readthedocs.io/en/master/modules/dht/)
``` lua
pin = 1

function measure()
    status, temp, humi, temp_dec, humi_dec = dht.read11(pin)
    if status == dht.OK then
        -- Integer firmware using this example
        --[[
        print(string.format("DHT Temperature:%d.%03d;Humidity:%d.%03d\r\n",
              math.floor(temp),
              temp_dec,
              math.floor(humi),
              humi_dec
        ))
        ]]--

        -- Float firmware using this example
        print("[DHT11][SUCCESS]T："..temp..";H："..humi)
    elseif status == dht.ERROR_CHECKSUM then
        print("[DHT11][ERROR_CHECKSUM]T："..temp.."；H："..humi)
    elseif status == dht.ERROR_TIMEOUT then
        print("[DHT11][ERROR_TIMEOUT]")
    end
end


tmr.alarm(1, 1000, tmr.ALARM_AUTO, measure)
```

## 0x03.引用
> [NodeMCU--学习笔记(二)连接wifi](https://web.archive.org/web/20190905061225/https://blog.csdn.net/qq_28877125/article/details/78680743)

未完待续……