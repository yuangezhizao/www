---
title: 卧室贴遍蓝牙温湿度计是一种什么体验
date: 2021-12-30 23:12:14
tags:
  - Home Assistant
  - HA
  - LYWSD03MMC
count: 1
os: 1
os_1: Monterry 12.1 (21C52)
browser: 0
browser_1: 96.0.4664.110 Stable
place: 新家
key: 129
---
    没想到吧，年终总结之后还有亿篇文章
<!-- more -->
## 0x00.前言
又是想标题就纠结了半天的文章，虽说贴遍也只买了`5`个肯定不是贴满的那种场景`2333`

## 0x01.成果
![仪表盘](https://i1.yuangezhizao.cn/macOS/20211230231939.png!webp)

## 0x02.[LYWSD03MMC](https://esphome.io/components/sensor/xiaomi_ble.html#lywsd03mmc)
没错，就是米家蓝牙温湿度计`2`，超级便宜不得不佩服米家的成本控制，而且温湿度传感器精度应该是要比`DHT11`要好得多的辣
想接入`HA`有多种方法，一种方法是用原生固件，这样每次都得蓝牙连接到温湿度计上，然后才能读取到温度，频繁的进行连接会导致耗电量的增加
那么，难不成还有无需配对就能获取到温湿度数据的方法？没错，温湿度数据也是可以放在蓝牙的广播包里的，这样无需配对就也能读取到了，省电效果极佳
而这就是另一种方法，去刷[Aaron Christophel](https://www.youtube.com/watch?v=NXKzFG61lNs)的第三方固件，也就是[atc1441@ATC_MiThermometer](https://github.com/atc1441/ATC_MiThermometer)，并且它的`Fork`分支[pvvx@ATC_MiThermometer](https://github.com/pvvx/ATC_MiThermometer)也被原作者所推荐
在省电上还要更进一步（警觉！

> Victor @pvvx did some very nice refinings of this custom firmare so i really suggest on cheking it out and even use his version as it offers many more functions including non-volatile storage and a better low power management

综上所述，自己选择了最最省电的`PVVX MiThermometer`

## 0x03.[TelinkMiFlasher](https://pvvx.github.io/ATC_MiThermometer/TelinkMiFlasher.html)
首先记得在米家里绑定一次，如果一次没绑定过的话，直接刷第三方固件就不能直接绑定回米家了（需要多进行一次刷固件的操作来复位`ID`），反之则无需多进行一次刷固件的操作了
<span title="你知道的太多了" class="heimu">这都是踩过的坑……</span>然后，在谷歌浏览器里与蓝牙温湿度计配对（可以用手机也可以用电脑，只要能调用蓝牙就行
1. 激活`Do activation`
2. 选择`Custom Firmware ver 3.5`
3. 执行`OTA`升级

这样等蓝牙温湿度计自动重启后就算是刷入自定义固件了，下图是摆在桌面可以肉眼可见的一枚，这枚有亿点特殊
1. 一点是开启了`Comfort`显示，而其他贴在墙壁上的为了省电并未开启
2. 另一点是更改了`Humidity offset`，因为自定义固件会影响湿度的正确计算，这点是已知的，可以和其他枚摆在一起，以得到大致的偏移量
![TelinkMiFlasher](https://i1.yuangezhizao.cn/macOS/20211230233654.png!webp)

> Vbat: 2905 mV , Temp: 26.10°C, Humi: 49.58%, Count: 17257, flg: 0x05:r1/t0

而其他枚远在身边的，均统一修改如下
1. `Advertising type`：广播类型，选择`Custom`
2. `Advertising interval`：广播间隔，选择最大值`5000ms`
3. `Connect latency`：`2500ms`
4. `RF TX Power`：辐射强度，选择`VANT+0.04dbm`（远离致死量
5. `Minimum LCD refresh rate`：屏幕刷新间隔，选择`12.75s`

这样一来，该对蓝牙温湿度计做的事情就都做完了

## 0x04.`ESP32`
嗯？为什么不是`ESP8266`，`ESP32`可是要贵上不到一倍的价格……是因为只有`ESP32`才开始有蓝牙，而十几块钱的`ESP8266`并木有
这里还是一如既往地使用`ESPHome`完成一体式开发、编译和下载的工作，创建一个新的设备，然后写配置文件去吧，`yaml`工程师欢迎你！

<details><summary>点击此处 ← 查看折叠</summary>

```yaml
esphome:
  name: esp32
  platform: ESP32
  board: esp32doit-devkit-v1

# Enable logging
logger:

# Enable Home Assistant API
api:

ota:
  password: "<rm>"

wifi:
  ssid: "8266_Only"
  password: "<rm>"

  # Enable fallback hotspot (captive portal) in case wifi connection fails
  ap:
    ssid: "Esp32 Fallback Hotspot"
    password: "<rm>"

captive_portal:

# Example configuration entry
web_server:
  port: 80
  auth:
    username: yuangezhizao
    password: <rm>

esp32_ble_tracker:
#  scan_parameters:
#    duration: 60s

xiaomi_ble:

# Example configuration entry
sensor:
  - platform: wifi_signal
    name: "ESP32 WiFi Signal"
    update_interval: 10s

  - platform: pvvx_mithermometer
    #B1.9
    mac_address: "<rm>"
    temperature:
      name: "PVVX Temperature"
    humidity:
      name: "PVVX Humidity"
    battery_level:
      name: "PVVX Battery-Level"
    battery_voltage:
      name: "PVVX Battery-Voltage"

  - platform: pvvx_mithermometer
    #B1.4
    mac_address: "<rm>"
    temperature:
      name: "Windowsill Temperature"
    humidity:
      name: "Windowsill Humidity"
    battery_level:
      name: "Windowsill Battery-Level"
    battery_voltage:
      name: "Windowsill Battery-Voltage"

  - platform: pvvx_mithermometer
    #B1.9
    mac_address: "<rm>"
    temperature:
      name: "Window Temperature"
    humidity:
      name: "Window Humidity"
    battery_level:
      name: "Window Battery-Level"
    battery_voltage:
      name: "Window Battery-Voltage"

  - platform: pvvx_mithermometer
    #B1.4
    mac_address: "<rm>"
    temperature:
      name: "Doorway Temperature"
    humidity:
      name: "Doorway Humidity"
    battery_level:
      name: "Doorway Battery-Level"
    battery_voltage:
      name: "Doorway Battery-Voltage"
```
</details>

关键部分自然是`platform: pvvx_mithermometer`这一部分了，注意必须开启`esp32_ble_tracker`方可配置`pvvx_mithermometer`，注意`ESPHome`的版本不能过于旧，<span title="你知道的太多了" class="heimu">这都是有被坑过的经历</span>
```yaml
- platform: pvvx_mithermometer
  #B1.9
  mac_address: "<rm>"
  temperature:
    name: "PVVX Temperature"
  humidity:
    name: "PVVX Humidity"
  battery_level:
    name: "PVVX Battery-Level"
  battery_voltage:
    name: "PVVX Battery-Voltage"
```
初次编译后需要下载到本地使用`ESPHome-Flasher.app`应用程序以`USB`线连接的方式刷入，想用命令行什么的也是可以的
然后第二次开始就可以空中升级了，`OTA`是真的方便，不出意外的话，第一次刷入之后`ESP32`就会从蓝牙温湿度计的广播报文中读取到各种数据，然后保存至`HA`

## 0x05.`HA`
最后，是不是想问文章开头的面板是怎么搞的？首先，背景图是自己去[floorplanner](https://floorplanner.com)画的，并手动截图（因为导出的画质太低了，高画质害得有料）
然后在`HA`的仪表盘添加一个`picture-elements`，把截图并设为背景图，最后添加多个`elements`，其中每一个实体（`entity`）对应一个物理量
可以通过`style.top`和`style.left`等属性再逐一调整坐标以及样式就搞定全部了
``` yaml
elements:
  - type: state-label
    entity: sensor.pvvx_temperature
    title: 桌面温度
    style:
      top: 8%
      left: 30%
      font-weight: bold
```

## 0x06.后记
`2021-12-31 00:42:56`：去年今日还在参考百度、知乎写跑路信，差不多正好是这个时间点写完并且已经`送信`了
而今年这个时间点，害在抓紧时间写早就该写完发出来的文章，咕咕咕咕咕……不知不觉中又一年就要过去了，而自己又老了一岁

> 小时候，特别期盼过年；长大了，特别害怕过年
