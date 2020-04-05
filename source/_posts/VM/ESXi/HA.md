---
title: VMware ESXi 安装 Home Assistant
date: 2020-4-5 19:13:00
tags:
  - VM
  - VMware
  - ESXi
count: 1
os: 0
os_1: 10.0.17763.1098 2019-LTSC
browser: 0
browser_1: 78.0.3904.108 Stable
place: 新家
key: 81
---
    老早就听说过 HA 了，昨天突然看到相关文章
<!-- more -->
## 0x00.前言
既然出了`VMDK`适配给`VMWare Workstation`，那么`ESXi`就一定也可以
![VMDK](https://i1.yuangezhizao.cn/Win-10/20200405191835.jpg!webp)

## 0x01.[安装](https://web.archive.org/web/20200405112133/https://www.home-assistant.io/hassio/installation/)
![创建新虚拟机](https://i1.yuangezhizao.cn/Win-10/20200405192315.jpg!webp)

`兼容性`：`ESXi 7.0 虚拟机`
`客户机操作系统系列`：`Linux`
`客户机操作系统版本`：`其他 4.x 或更高版本的 Linux (64 位)`
![选择名称和客户机操作系统](https://i1.yuangezhizao.cn/Win-10/20200405194227.jpg!webp)

`自定义设置`，删除`硬盘 1`、`CD/DVD 驱动器 1`
`添加硬盘`、`现有硬盘`：包含`HassOS.vmdk`的文件夹`HassOS`，`IDE控制器0`，`主要`
`CPU`：`2`（第一次运行时分的单核，这次分的双核，看起来是够用的
`内存`：`2G`（第一次运行时分的`1G`结果跑满，这次`2G`同样跑满草，倒是可以再加
![虚拟硬件](https://i1.yuangezhizao.cn/Win-10/20200405192929.jpg!webp)

`引导选项`、`固件`：`EFI`，**关闭**`启用 UEFI 安全引导`（否则无法启动
![虚拟机选项](https://i1.yuangezhizao.cn/Win-10/20200405193613.jpg!webp)

最后`打开电源`，然后等上较长的一段时间才会就绪，直接睡觉去了
![vms](https://i1.yuangezhizao.cn/Win-10/20200405191808.png!webp)

## 0x02.配置
进入[http://homeassistant:8123](http://homeassistant:8123)，虽然官方说的是[http://homeassistant.local:8123](http://homeassistant.local:8123)，当然官方之前用的是`hassio.local`
![创建账户](https://i1.yuangezhizao.cn/Win-10/20200405184439.jpg!webp)

然而这个`自动检测`并不是很准确的样子，于是人工标点
![定位](https://i1.yuangezhizao.cn/Win-10/20200405185126.jpg!webp)

这里暂时没有配置，跳过
![集成](https://i1.yuangezhizao.cn/Win-10/20200405185157.jpg!webp)

终于来到了控制面板的首页了，空空如也`2333`
![首页](https://i1.yuangezhizao.cn/Win-10/20200405185306.jpg!webp)

然后去看一眼附加组件，竟然有`VSC`好评
![store](https://i1.yuangezhizao.cn/Win-10/20200405190040.jpg!webp)

目前版本：`Home Assistant 0.107.7`
![信息](https://i1.yuangezhizao.cn/Win-10/20200405195453.jpg!webp)

## 0x03.[ESPHome](https://esphome.io/)
`Supervisor`的`ADD-ON STORE`中的`Repositories`添加：`https://github.com/esphome/hassio`

![Repositories](https://i1.yuangezhizao.cn/Win-10/20200405200000.jpg!webp)
![ESPHome Hass.io Add-Ons](https://i1.yuangezhizao.cn/Win-10/20200405200153.jpg!webp)

来创建个设备玩玩看吧
![必须小写草](https://i1.yuangezhizao.cn/Win-10/20200405201014.jpg!webp)
![NodeMCU](https://i1.yuangezhizao.cn/Win-10/20200405201252.jpg!webp)

提供`WiFi`信息，而且说明了只需要一次`USB`烧录固件，之后的升级均通过`OTA`，并可在此处指定升级密匙
![WiFi](https://i1.yuangezhizao.cn/Win-10/20200405201444.jpg!webp)

然后才想到，虚拟机里并不能开启热点草
![Done](https://i1.yuangezhizao.cn/Win-10/20200405201649.jpg!webp)

然后就炸了
![草](https://i1.yuangezhizao.cn/Win-10/20200405201811.jpg!webp)
![刷新页面之后好了](https://i1.yuangezhizao.cn/Win-10/20200405202034.jpg!webp)

`UPLOAD`编译固件，结果编译炸了
![Compile And Upload](https://i1.yuangezhizao.cn/Win-10/20200405202131.jpg!webp)
![+1s](https://i1.yuangezhizao.cn/Win-10/20200405202145.jpg!webp)

确信是网络环境原因，重试了好几次`Compile And Upload nodemcu.yaml`，终于成功（指下载）一次（并没有成功烧录？

<details><summary>点击此处 ← 查看终端</summary>

``` bash
INFO Reading configuration /config/esphome/nodemcu.yaml...
INFO Generating C++ source...
INFO Compiling app...
INFO Running:  platformio run -d /config/esphome/nodemcu
Processing nodemcu (board: nodemcuv2; framework: arduino; platform: espressif8266@2.2.3)
--------------------------------------------------------------------------------
HARDWARE: ESP8266 80MHz, 80KB RAM, 4MB Flash
Looking for ESPAsyncTCP-esphome library in registry
LibraryManager: Installing id=6757 @ 1.2.2
ESPAsyncTCP-esphome @ 1.2.2 has been successfully installed!
Looking for ESPAsyncWebServer-esphome library in registry
LibraryManager: Installing id=6758 @ 1.2.6

Downloading  [####--------------------------------]   12%
Downloading  [####--------------------------------]   13%
Downloading  [#####-------------------------------]   13%
Downloading  [#####-------------------------------]   14%
Downloading  [#####-------------------------------]   15%
Downloading  [#####-------------------------------]   15%  00:00:05
Downloading  [#####-------------------------------]   16%  00:00:05
Downloading  [######------------------------------]   16%  00:00:05
Downloading  [######------------------------------]   17%  00:00:05
Downloading  [######------------------------------]   18%  00:00:05
Downloading  [######------------------------------]   19%  00:00:05
Downloading  [#######-----------------------------]   19%  00:00:05
Downloading  [#######-----------------------------]   20%  00:00:05
Downloading  [#######-----------------------------]   21%  00:00:05
Downloading  [#######-----------------------------]   22%  00:00:05
Downloading  [########----------------------------]   22%  00:00:05
Downloading  [########----------------------------]   23%  00:00:05
Downloading  [########----------------------------]   24%  00:00:05
Downloading  [#########---------------------------]   25%  00:00:05
Downloading  [#########---------------------------]   26%  00:00:05
Downloading  [#########---------------------------]   27%  00:00:05
Downloading  [#########---------------------------]   27%  00:00:04
Downloading  [##########--------------------------]   27%  00:00:04
Downloading  [##########--------------------------]   28%  00:00:04
Downloading  [##########--------------------------]   29%  00:00:04
Downloading  [##########--------------------------]   30%  00:00:04
Downloading  [###########-------------------------]   30%  00:00:04
Downloading  [###########-------------------------]   31%  00:00:04
Downloading  [###########-------------------------]   32%  00:00:04
Downloading  [############------------------------]   33%  00:00:04
Downloading  [############------------------------]   34%  00:00:04
Downloading  [############------------------------]   35%  00:00:04
Downloading  [############------------------------]   36%  00:00:04
Downloading  [#############-----------------------]   36%  00:00:04
Downloading  [#############-----------------------]   37%  00:00:04
Downloading  [#############-----------------------]   38%  00:00:04
Downloading  [##############----------------------]   39%  00:00:04
Downloading  [##############----------------------]   40%  00:00:04
Downloading  [##############----------------------]   41%  00:00:04
Downloading  [###############---------------------]   41%  00:00:04
Downloading  [###############---------------------]   42%  00:00:04
Downloading  [###############---------------------]   43%  00:00:04
Downloading  [###############---------------------]   44%  00:00:04
Downloading  [################--------------------]   44%  00:00:04
Downloading  [################--------------------]   45%  00:00:04
Downloading  [################--------------------]   46%  00:00:04
Downloading  [#################-------------------]   47%  00:00:04
Downloading  [#################-------------------]   48%  00:00:04
Downloading  [#################-------------------]   49%  00:00:04
Downloading  [##################------------------]   50%  00:00:04
Downloading  [##################------------------]   51%  00:00:04
Downloading  [##################------------------]   52%  00:00:03
Downloading  [###################-----------------]   53%  00:00:03
Downloading  [###################-----------------]   54%  00:00:03
Downloading  [###################-----------------]   55%  00:00:03
Downloading  [####################----------------]   55%  00:00:03
Downloading  [####################----------------]   56%  00:00:03
Downloading  [####################----------------]   57%  00:00:03
Downloading  [####################----------------]   58%  00:00:03
Downloading  [#####################---------------]   58%  00:00:03
Downloading  [#####################---------------]   59%  00:00:03
Downloading  [#####################---------------]   60%  00:00:03
Downloading  [######################--------------]   61%  00:00:03
Downloading  [######################--------------]   62%  00:00:03
Downloading  [######################--------------]   63%  00:00:03
Downloading  [#######################-------------]   63%  00:00:03
Downloading  [#######################-------------]   64%  00:00:03
Downloading  [#######################-------------]   65%  00:00:03
Downloading  [#######################-------------]   65%  00:00:02
Downloading  [#######################-------------]   66%  00:00:02
Downloading  [########################------------]   66%  00:00:02
Downloading  [########################------------]   67%  00:00:02
Downloading  [########################------------]   68%  00:00:02
Downloading  [########################------------]   69%  00:00:02
Downloading  [#########################-----------]   69%  00:00:02
Downloading  [#########################-----------]   70%  00:00:02
Downloading  [#########################-----------]   71%  00:00:02
Downloading  [#########################-----------]   72%  00:00:02
Downloading  [##########################----------]   72%  00:00:02
Downloading  [##########################----------]   73%  00:00:02
Downloading  [##########################----------]   74%  00:00:02
Downloading  [###########################---------]   75%  00:00:02
Downloading  [###########################---------]   76%  00:00:02
Downloading  [###########################---------]   77%  00:00:02
Downloading  [###########################---------]   77%  00:00:01
Downloading  [############################--------]   77%  00:00:01
Downloading  [############################--------]   78%  00:00:01
Downloading  [############################--------]   79%  00:00:01
Downloading  [############################--------]   80%  00:00:01
Downloading  [#############################-------]   80%  00:00:01
Downloading  [#############################-------]   81%  00:00:01
Downloading  [#############################-------]   82%  00:00:01
Downloading  [##############################------]   83%  00:00:01
Downloading  [##############################------]   84%  00:00:01
Downloading  [##############################------]   85%  00:00:01
Downloading  [##############################------]   86%  00:00:01
Downloading  [###############################-----]   86%  00:00:01
Downloading  [###############################-----]   87%  00:00:01
Downloading  [###############################-----]   88%  00:00:01
Downloading  [################################----]   89%  00:00:01
Downloading  [################################----]   89%  00:00:00
Downloading  [################################----]   90%  00:00:00
Downloading  [################################----]   91%  00:00:00
Downloading  [#################################---]   91%  00:00:00
Downloading  [#################################---]   92%  00:00:00
Downloading  [#################################---]   93%  00:00:00
Downloading  [#################################---]   94%  00:00:00
Downloading  [##################################--]   94%  00:00:00
Downloading  [##################################--]   95%  00:00:00
Downloading  [##################################--]   96%  00:00:00
Downloading  [###################################-]   97%  00:00:00
Downloading  [###################################-]   98%  00:00:00
Downloading  [###################################-]   99%  00:00:00
Downloading  [####################################]  100%          
ESPAsyncWebServer-esphome @ 1.2.6 has been successfully installed!
LibraryManager: Installing id=6757
Looking for AsyncTCP-esphome library in registry
LibraryManager: Installing id=6798
AsyncTCP-esphome @ 1.1.1 has been successfully installed!
Dependency Graph
|-- <ESPAsyncTCP-esphome> 1.2.2
|   |-- <ESP8266WiFi> 1.0
|-- <ESP8266WiFi> 1.0
|-- <ESP8266mDNS> 1.2
|   |-- <ESP8266WiFi> 1.0
|-- <ESPAsyncWebServer-esphome> 1.2.6
|   |-- <ESPAsyncTCP-esphome> 1.2.2
|   |   |-- <ESP8266WiFi> 1.0
|   |-- <Hash> 1.0
|   |-- <ESP8266WiFi> 1.0
|-- <DNSServer> 1.1.1
|   |-- <ESP8266WiFi> 1.0
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/api/api_connection.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/api/api_pb2.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/api/api_pb2_service.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/api/api_server.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/api/list_entities.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/api/proto.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/api/subscribe_state.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/api/user_services.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/api/util.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/captive_portal/captive_portal.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/logger/logger.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/ota/ota_component.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/web_server_base/web_server_base.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/wifi/wifi_component.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/wifi/wifi_component_esp32.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/wifi/wifi_component_esp8266.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/core/application.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/core/component.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/core/controller.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/core/esphal.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/core/helpers.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/core/log.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/core/preferences.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/core/scheduler.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/core/util.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/main.cpp.o
Generating LD script /data/nodemcu/.pioenvs/nodemcu/ld/local.eagle.app.v6.common.ld
Compiling /data/nodemcu/.pioenvs/nodemcu/lib4d9/ESP8266WiFi/BearSSLHelpers.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib4d9/ESP8266WiFi/CertStoreBearSSL.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib4d9/ESP8266WiFi/ESP8266WiFi.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib4d9/ESP8266WiFi/ESP8266WiFiAP.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib4d9/ESP8266WiFi/ESP8266WiFiGeneric.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib4d9/ESP8266WiFi/ESP8266WiFiMulti.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib4d9/ESP8266WiFi/ESP8266WiFiSTA-WPS.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib4d9/ESP8266WiFi/ESP8266WiFiSTA.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib4d9/ESP8266WiFi/ESP8266WiFiScan.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib4d9/ESP8266WiFi/WiFiClient.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib4d9/ESP8266WiFi/WiFiClientSecureAxTLS.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib4d9/ESP8266WiFi/WiFiClientSecureBearSSL.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib4d9/ESP8266WiFi/WiFiServer.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib4d9/ESP8266WiFi/WiFiServerSecureAxTLS.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib4d9/ESP8266WiFi/WiFiServerSecureBearSSL.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib4d9/ESP8266WiFi/WiFiUdp.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib5c2/ESPAsyncTCP-esphome_ID6757/AsyncPrinter.cpp.o
Archiving /data/nodemcu/.pioenvs/nodemcu/lib4d9/libESP8266WiFi.a
Compiling /data/nodemcu/.pioenvs/nodemcu/lib5c2/ESPAsyncTCP-esphome_ID6757/ESPAsyncTCP.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib5c2/ESPAsyncTCP-esphome_ID6757/ESPAsyncTCPbuffer.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib5c2/ESPAsyncTCP-esphome_ID6757/SyncClient.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib5c2/ESPAsyncTCP-esphome_ID6757/tcp_axtls.c.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib0d3/ESP8266mDNS/ESP8266mDNS.cpp.o
Archiving /data/nodemcu/.pioenvs/nodemcu/lib5c2/libESPAsyncTCP-esphome_ID6757.a
Compiling /data/nodemcu/.pioenvs/nodemcu/lib0d3/ESP8266mDNS/ESP8266mDNS_Legacy.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib0d3/ESP8266mDNS/LEAmDNS.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib0d3/ESP8266mDNS/LEAmDNS_Control.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib0d3/ESP8266mDNS/LEAmDNS_Helpers.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib0d3/ESP8266mDNS/LEAmDNS_Structs.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib0d3/ESP8266mDNS/LEAmDNS_Transfer.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib6f5/Hash/Hash.cpp.o
Archiving /data/nodemcu/.pioenvs/nodemcu/lib0d3/libESP8266mDNS.a
Compiling /data/nodemcu/.pioenvs/nodemcu/lib6f5/Hash/sha1/sha1.c.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib90c/ESPAsyncWebServer-esphome_ID6758/AsyncEventSource.cpp.o
Archiving /data/nodemcu/.pioenvs/nodemcu/lib6f5/libHash.a
Compiling /data/nodemcu/.pioenvs/nodemcu/lib90c/ESPAsyncWebServer-esphome_ID6758/AsyncWebSocket.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib90c/ESPAsyncWebServer-esphome_ID6758/SPIFFSEditor.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib90c/ESPAsyncWebServer-esphome_ID6758/WebAuthentication.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib90c/ESPAsyncWebServer-esphome_ID6758/WebHandlers.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib90c/ESPAsyncWebServer-esphome_ID6758/WebRequest.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib90c/ESPAsyncWebServer-esphome_ID6758/WebResponses.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib90c/ESPAsyncWebServer-esphome_ID6758/WebServer.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/lib760/DNSServer/DNSServer.cpp.o
Archiving /data/nodemcu/.pioenvs/nodemcu/lib90c/libESPAsyncWebServer-esphome_ID6758.a
Archiving /data/nodemcu/.pioenvs/nodemcu/libFrameworkArduinoVariant.a
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/Esp-frag.cpp.o
Archiving /data/nodemcu/.pioenvs/nodemcu/lib760/libDNSServer.a
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/Esp-version.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/Esp.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/FS.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/FunctionalInterrupt.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/HardwareSerial.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/IPAddress.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/MD5Builder.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/Print.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/Schedule.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/ScheduledFunctions.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/StackThunk.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/Stream.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/StreamString.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/Tone.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/Updater.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/WMath.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/WString.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/abi.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/base64.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/cbuf.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/cont.S.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/cont_util.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/core_esp8266_app_entry_noextra4k.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/core_esp8266_eboot_command.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/core_esp8266_flash_utils.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/core_esp8266_i2s.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/core_esp8266_main.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/core_esp8266_noniso.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/core_esp8266_phy.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/core_esp8266_postmortem.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/core_esp8266_si2c.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/core_esp8266_sigma_delta.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/core_esp8266_timer.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/core_esp8266_waveform.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/core_esp8266_wiring.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/core_esp8266_wiring_analog.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/core_esp8266_wiring_digital.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/core_esp8266_wiring_pulse.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/core_esp8266_wiring_pwm.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/core_esp8266_wiring_shift.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/debug.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/gdb_hooks.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/heap.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/libb64/cdecode.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/libb64/cencode.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/libc_replacements.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/sntp-lwip2.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/spiffs/spiffs_cache.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/spiffs/spiffs_check.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/spiffs/spiffs_gc.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/spiffs/spiffs_hydrogen.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/spiffs/spiffs_nucleus.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/spiffs_api.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/spiffs_hal.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/sqrt32.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/time.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/uart.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/FrameworkArduino/umm_malloc/umm_malloc.cpp.o
Archiving /data/nodemcu/.pioenvs/nodemcu/libFrameworkArduino.a
Linking /data/nodemcu/.pioenvs/nodemcu/firmware.elf
Building /data/nodemcu/.pioenvs/nodemcu/firmware.bin
Retrieving maximum program size /data/nodemcu/.pioenvs/nodemcu/firmware.elf
Checking size /data/nodemcu/.pioenvs/nodemcu/firmware.elf
DATA:    [====      ]  43.9% (used 35928 bytes from 81920 bytes)
PROGRAM: [====      ]  37.7% (used 393512 bytes from 1044464 bytes)
Creating BIN file "/data/nodemcu/.pioenvs/nodemcu/firmware.bin" using "/data/nodemcu/.pioenvs/nodemcu/firmware.elf"
========================= [SUCCESS] Took 54.97 seconds =========================
INFO Successfully compiled program.
INFO Resolving IP address of nodemcu.local
ERROR Error resolving IP address of nodemcu.local. Is it connected to WiFi?
ERROR (If this error persists, please set a static IP address: https://esphome.io/components/wifi.html#manual-ips)
ERROR Error resolving IP address: Error resolving address with mDNS: Did not respond. Maybe the device is offline., [Errno -5] No address associated with hostname
```

</details>

然后去找编译产物
![只编译](https://i1.yuangezhizao.cn/Win-10/20200405210250.jpg!webp)

非常奇怪，`/data/nodemcu/.pioenvs/nodemcu/firmware.bin`并不存在……因为`/data/`目录下就没有`nodemcu`这个文件夹草
``` bash
➜  / cd /data         
➜  /data ll
total 12K
drwx------ 2 root root 4.0K Apr  5 19:04 git
-rw-r--r-- 1 root root   43 Apr  5 19:04 options.json
drwxr-xr-x 6 root root 4.0K Apr  5 19:04 vscode
```

没办法只好修改`nodemcu.yaml.json`配置文件中的`firmware_bin_path`，然后重新编译
![修改](https://i1.yuangezhizao.cn/Win-10/20200405210758.jpg!webp)
![重新编译](https://i1.yuangezhizao.cn/Win-10/20200405211032.jpg!webp)

也不知道是不是改动的关系，反正是可以下载固件了……
![只编译](https://i1.yuangezhizao.cn/Win-10/20200405211126.jpg!webp)

那么如何烧录固件呢，之前`Ardunio`用习惯了，这次看来得拿回`NodeMCU PyFlasher`
![烧录](https://i1.yuangezhizao.cn/Win-10/20200405211909.jpg!webp)
![Online](https://i1.yuangezhizao.cn/Win-10/20200405212220.jpg!webp)

然后添加传感器
``` bash
# Example configuration entry
sensor:
  - platform: dht
    pin: D1
    temperature:
      name: "Temperature"
    humidity:
      name: "Humidity"
    update_interval: 60s
```
然后`UPLOAD`编译固件，`OTA`成功升级巨爽啊，但是并不能获取到传感器的值，一看`Auto-detected model: DHT22`，草

<details><summary>点击此处 ← 查看终端</summary>

``` bash
INFO Reading configuration /config/esphome/nodemcu.yaml...
INFO Generating C++ source...
INFO Compiling app...
INFO Running:  platformio run -d /config/esphome/nodemcu
Processing nodemcu (board: nodemcuv2; framework: arduino; platform: espressif8266@2.2.3)
--------------------------------------------------------------------------------
HARDWARE: ESP8266 80MHz, 80KB RAM, 4MB Flash
Dependency Graph
|-- <ESPAsyncTCP-esphome> 1.2.2
|   |-- <ESP8266WiFi> 1.0
|-- <ESP8266WiFi> 1.0
|-- <ESP8266mDNS> 1.2
|   |-- <ESP8266WiFi> 1.0
|-- <ESPAsyncWebServer-esphome> 1.2.6
|   |-- <ESPAsyncTCP-esphome> 1.2.2
|   |   |-- <ESP8266WiFi> 1.0
|   |-- <Hash> 1.0
|   |-- <ESP8266WiFi> 1.0
|-- <DNSServer> 1.1.1
|   |-- <ESP8266WiFi> 1.0
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/api/api_connection.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/api/api_pb2_service.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/api/api_server.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/api/list_entities.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/api/proto.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/api/subscribe_state.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/api/user_services.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/api/util.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/captive_portal/captive_portal.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/dht/dht.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/logger/logger.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/ota/ota_component.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/sensor/automation.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/sensor/filter.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/sensor/sensor.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/web_server_base/web_server_base.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/wifi/wifi_component.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/wifi/wifi_component_esp32.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/components/wifi/wifi_component_esp8266.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/core/application.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/core/component.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/core/controller.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/core/esphal.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/core/log.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/core/preferences.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/esphome/core/util.cpp.o
Compiling /data/nodemcu/.pioenvs/nodemcu/src/main.cpp.o
Linking /data/nodemcu/.pioenvs/nodemcu/firmware.elf
Building /data/nodemcu/.pioenvs/nodemcu/firmware.bin
Retrieving maximum program size /data/nodemcu/.pioenvs/nodemcu/firmware.elf
Checking size /data/nodemcu/.pioenvs/nodemcu/firmware.elf
DATA:    [====      ]  44.3% (used 36328 bytes from 81920 bytes)
PROGRAM: [====      ]  38.5% (used 402532 bytes from 1044464 bytes)
Creating BIN file "/data/nodemcu/.pioenvs/nodemcu/firmware.bin" using "/data/nodemcu/.pioenvs/nodemcu/firmware.elf"
========================= [SUCCESS] Took 12.22 seconds =========================
INFO Successfully compiled program.
INFO Resolving IP address of nodemcu.local
INFO  -> 192.168.25.96
INFO Uploading /data/nodemcu/.pioenvs/nodemcu/firmware.bin (406688 bytes)
Uploading: [============================================================] 100% Done...

INFO Waiting for result...
INFO OTA successful
INFO Successfully uploaded program.
INFO Starting log output from nodemcu.local using esphome API
WARNING Error resolving IP address of nodemcu.local. Is it connected to WiFi?
WARNING (If this error persists, please set a static IP address: https://esphome.io/components/wifi.html#manual-ips)
WARNING Initial connection failed. The ESP might not be connected to WiFi yet (Error resolving IP address: Error resolving address with mDNS: Did not respond. Maybe the device is offline., [Errno -5] No address associated with hostname). Re-Trying in 1 seconds
WARNING Error resolving IP address of nodemcu.local. Is it connected to WiFi?
WARNING (If this error persists, please set a static IP address: https://esphome.io/components/wifi.html#manual-ips)
WARNING Initial connection failed. The ESP might not be connected to WiFi yet (Error resolving IP address: Error resolving address with mDNS: Did not respond. Maybe the device is offline., [Errno -5] No address associated with hostname). Re-Trying in 1 seconds
INFO Connecting to nodemcu.local:6053 (192.168.25.96)
INFO Successfully connected to nodemcu.local
[21:28:01][I][app:100]: ESPHome version 1.14.3 compiled on Apr  5 2020, 21:27:25
[21:28:01][C][wifi:415]: WiFi:
[21:28:01][C][wifi:283]:   SSID: [redacted]
[21:28:01][C][wifi:284]:   IP Address: 192.168.25.96
[21:28:01][C][wifi:286]:   BSSID: [redacted]
[21:28:01][C][wifi:287]:   Hostname: 'nodemcu'
[21:28:01][C][wifi:291]:   Signal strength: -48 dB ▂▄▆█
[21:28:01][C][wifi:295]:   Channel: 6
[21:28:01][C][wifi:296]:   Subnet: 255.255.255.0
[21:28:01][C][wifi:297]:   Gateway: 192.168.25.254
[21:28:01][C][wifi:298]:   DNS1: 192.168.25.254
[21:28:01][C][wifi:299]:   DNS2: (IP unset)
[21:28:01][C][logger:175]: Logger:
[21:28:01][C][logger:176]:   Level: DEBUG
[21:28:01][C][logger:177]:   Log Baud Rate: 115200
[21:28:01][C][logger:178]:   Hardware UART: UART0
[21:28:01][C][dht:017]: DHT:
[21:28:01][C][dht:018]:   Pin: GPIO5 (Mode: INPUT)
[21:28:01][C][dht:020]:   Auto-detected model: DHT22
[21:28:01][C][dht:027]:   Update Interval: 60.0s
[21:28:01][C][dht:029]:   Temperature 'Temperature'
[21:28:01][C][dht:029]:     Unit of Measurement: '°C'
[21:28:01][C][dht:029]:     Accuracy Decimals: 1
[21:28:01][C][dht:029]:     Icon: 'mdi:thermometer'
[21:28:01][C][dht:030]:   Humidity 'Humidity'
[21:28:01][C][dht:030]:     Unit of Measurement: '%'
[21:28:01][C][dht:030]:     Accuracy Decimals: 0
[21:28:01][C][dht:030]:     Icon: 'mdi:water-percent'
[21:28:01][C][captive_portal:169]: Captive Portal:
[21:28:01][C][ota:029]: Over-The-Air Updates:
[21:28:01][C][ota:030]:   Address: nodemcu.local:8266
[21:28:01][C][api:095]: API Server:
[21:28:01][C][api:096]:   Address: nodemcu.local:6053
[21:28:15][W][dht:126]: Requesting data from DHT failed!
[21:28:15][W][dht:060]: Invalid readings! Please check your wiring (pull-up resistor, pin number) and consider manually specifying the DHT model using the model option.
[21:28:15][D][sensor:092]: 'Temperature': Sending state nan °C with 1 decimals of accuracy
[21:28:15][D][sensor:092]: 'Humidity': Sending state nan % with 0 decimals of accuracy
```

</details>

于是手动指定是`DHT11`
``` bash
# Example configuration entry
sensor:
  - platform: dht
    pin: D1
    temperature:
      name: "Temperature"
    humidity:
      name: "Humidity"
    model: DHT11
    update_interval: 60s
```
再次`UPLOAD`编译固件，这次能获取到传感器的值了

<details><summary>点击此处 ← 查看终端</summary>

``` bash
INFO Reading configuration /config/esphome/nodemcu.yaml...
INFO Generating C++ source...
INFO Compiling app...
INFO Running:  platformio run -d /config/esphome/nodemcu
Processing nodemcu (board: nodemcuv2; framework: arduino; platform: espressif8266@2.2.3)
--------------------------------------------------------------------------------
HARDWARE: ESP8266 80MHz, 80KB RAM, 4MB Flash
Dependency Graph
|-- <ESPAsyncTCP-esphome> 1.2.2
|   |-- <ESP8266WiFi> 1.0
|-- <ESP8266WiFi> 1.0
|-- <ESP8266mDNS> 1.2
|   |-- <ESP8266WiFi> 1.0
|-- <ESPAsyncWebServer-esphome> 1.2.6
|   |-- <ESPAsyncTCP-esphome> 1.2.2
|   |   |-- <ESP8266WiFi> 1.0
|   |-- <Hash> 1.0
|   |-- <ESP8266WiFi> 1.0
|-- <DNSServer> 1.1.1
|   |-- <ESP8266WiFi> 1.0
Compiling /data/nodemcu/.pioenvs/nodemcu/src/main.cpp.o
Linking /data/nodemcu/.pioenvs/nodemcu/firmware.elf
Retrieving maximum program size /data/nodemcu/.pioenvs/nodemcu/firmware.elf
Checking size /data/nodemcu/.pioenvs/nodemcu/firmware.elf
Building /data/nodemcu/.pioenvs/nodemcu/firmware.bin
DATA:    [====      ]  44.3% (used 36328 bytes from 81920 bytes)
PROGRAM: [====      ]  38.5% (used 402532 bytes from 1044464 bytes)
Creating BIN file "/data/nodemcu/.pioenvs/nodemcu/firmware.bin" using "/data/nodemcu/.pioenvs/nodemcu/firmware.elf"
========================= [SUCCESS] Took 3.72 seconds =========================
INFO Successfully compiled program.
INFO Resolving IP address of nodemcu.local
INFO  -> 192.168.25.96
INFO Uploading /data/nodemcu/.pioenvs/nodemcu/firmware.bin (406688 bytes)
Uploading: [============================================================] 100% Done...

INFO Waiting for result...
INFO OTA successful
INFO Successfully uploaded program.
INFO Starting log output from nodemcu.local using esphome API
WARNING Error resolving IP address of nodemcu.local. Is it connected to WiFi?
WARNING (If this error persists, please set a static IP address: https://esphome.io/components/wifi.html#manual-ips)
WARNING Initial connection failed. The ESP might not be connected to WiFi yet (Error resolving IP address: Error resolving address with mDNS: Did not respond. Maybe the device is offline., [Errno -5] No address associated with hostname). Re-Trying in 1 seconds
WARNING Error resolving IP address of nodemcu.local. Is it connected to WiFi?
WARNING (If this error persists, please set a static IP address: https://esphome.io/components/wifi.html#manual-ips)
WARNING Initial connection failed. The ESP might not be connected to WiFi yet (Error resolving IP address: Error resolving address with mDNS: Did not respond. Maybe the device is offline., [Errno -5] No address associated with hostname). Re-Trying in 1 seconds
INFO Connecting to nodemcu.local:6053 (192.168.25.96)
INFO Successfully connected to nodemcu.local
[21:30:37][I][app:100]: ESPHome version 1.14.3 compiled on Apr  5 2020, 21:30:01
[21:30:37][C][wifi:415]: WiFi:
[21:30:37][C][wifi:283]:   SSID: [redacted]
[21:30:37][C][wifi:284]:   IP Address: 192.168.25.96
[21:30:37][C][wifi:286]:   BSSID: [redacted]
[21:30:37][C][wifi:287]:   Hostname: 'nodemcu'
[21:30:37][C][wifi:291]:   Signal strength: -49 dB ▂▄▆█
[21:30:37][C][wifi:295]:   Channel: 6
[21:30:37][C][wifi:296]:   Subnet: 255.255.255.0
[21:30:37][C][wifi:297]:   Gateway: 192.168.25.254
[21:30:37][C][wifi:298]:   DNS1: 192.168.25.254
[21:30:37][C][wifi:299]:   DNS2: (IP unset)
[21:30:37][C][logger:175]: Logger:
[21:30:37][C][logger:176]:   Level: DEBUG
[21:30:37][C][logger:177]:   Log Baud Rate: 115200
[21:30:37][C][logger:178]:   Hardware UART: UART0
[21:30:37][C][dht:017]: DHT:
[21:30:37][C][dht:018]:   Pin: GPIO5 (Mode: INPUT)
[21:30:37][C][dht:022]:   Model: DHT11
[21:30:37][C][dht:027]:   Update Interval: 60.0s
[21:30:37][C][dht:029]:   Temperature 'Temperature'
[21:30:37][C][dht:029]:     Unit of Measurement: '°C'
[21:30:37][C][dht:029]:     Accuracy Decimals: 1
[21:30:37][C][dht:029]:     Icon: 'mdi:thermometer'
[21:30:37][C][dht:030]:   Humidity 'Humidity'
[21:30:37][C][dht:030]:     Unit of Measurement: '%'
[21:30:37][C][dht:030]:     Accuracy Decimals: 0
[21:30:37][C][dht:030]:     Icon: 'mdi:water-percent'
[21:30:37][C][captive_portal:169]: Captive Portal:
[21:30:37][C][ota:029]: Over-The-Air Updates:
[21:30:37][C][ota:030]:   Address: nodemcu.local:8266
[21:30:37][C][api:095]: API Server:
[21:30:37][C][api:096]:   Address: nodemcu.local:6053
[21:30:54][D][dht:048]: Got Temperature=27.0°C Humidity=49.0%
[21:30:54][D][sensor:092]: 'Temperature': Sending state 27.00000 °C with 1 decimals of accuracy
[21:30:54][D][sensor:092]: 'Humidity': Sending state 49.00000 % with 0 decimals of accuracy
[21:31:54][D][dht:048]: Got Temperature=27.0°C Humidity=49.0%
[21:31:54][D][sensor:092]: 'Temperature': Sending state 27.00000 °C with 1 decimals of accuracy
[21:31:54][D][sensor:092]: 'Humidity': Sending state 49.00000 % with 0 decimals of accuracy
[21:32:19][I][ota:046]: Boot seems successful, resetting boot loop counter.
[21:32:54][D][dht:048]: Got Temperature=27.0°C Humidity=49.0%
[21:32:54][D][sensor:092]: 'Temperature': Sending state 27.00000 °C with 1 decimals of accuracy
[21:32:54][D][sensor:092]: 'Humidity': Sending state 49.00000 % with 0 decimals of accuracy
```

</details>

最后上两张图
![debug](https://i1.yuangezhizao.cn/Win-10/20200405215020.png!webp)
![首页](https://i1.yuangezhizao.cn/Win-10/20200405214906.png!webp)

## 0x04.后记
这个传感器取值，温度的**一位**小数点精度一直**是零**啊，也就是说只剩下整数位了草……
这个`HA`可以看做是一个平台，具体能发挥到什么程度就要靠你的想象力了

## 0x05.引用
[如何在ESXI中安装Home Assistant](https://web.archive.org/web/20200405114005/https://lijie.org/2019/10/12/install-homeassistant-on-esxi/)
[智能家居 篇一：Homeassistant系列：ESPEasy转战ESPHome，更加便捷高效，告别频繁重启hass](https://web.archive.org/web/20200405134417/https://post.smzdm.com/p/a3gzw7xk/)

未完待续……