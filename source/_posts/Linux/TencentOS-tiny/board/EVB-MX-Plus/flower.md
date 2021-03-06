---
title: 【IOT应用创新大赛】基于 EVB_MX_Plus 的盆栽土壤监测
date: 2020-4-20 22:38:46
tags:
  - TencentOS-tiny
  - EVB_MX_Plus
  - STM32L4
count: 6
os: 0
os_1: 10.0.17763.1158 2019-LTSC
browser: 0
browser_1: 78.0.3904.108 Stable
place: 新家
key: 86
---
    终于到 deadline 了草
<!-- more -->
## 0x00.前言
还记得推上的那张曲线图嘛，越临近`deadline`效率越高（雾
![RT](https://i1.yuangezhizao.cn/Win-10/20200420224201.jpg!webp)

`2020-4-23 23:35:25`：
<details><summary>点击此处 ← 查看折叠</summary>

本来想着直接在社区修改，结果预览的图片都`403`了……于是又转回来修改了
![RT](https://i1.yuangezhizao.cn/Win-10/20200423231853.jpg!webp)

又想起来`Coding Pages`今晚突然莫名炸了博客也进不来了……
![0%](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-04-23-22-05-27-855_com.taobao.tao.jpg!webp)

</details>

## 0x01.简介
其实这阵子一直盯着[专栏](https://cloud.tencent.com/developer/column/79816)看投稿文章的方向性，印象里上周直至昨天还只有`4`篇，今天突然就多了数十篇，看完大佬们已经提交的文章，感觉好多都是`LoRa`相关的
虽然当初比赛申请的时候并不知道`RoLa`是什么，但是看完大佬们的文章也算是明白了它的基本使用方法吧，传输距离比`WiFi`远多了可是印象里最深刻的一点了
最后说回自己申请的`32`板子，虽然是个半内行人但是拿到手也能看出这是一块好板子~~，拿到手之后真是爱不释手`hhh`~~
而且还能脱离数据线仅使用锂电池供电（毕竟主打的低功耗`MCU`），不过某天晚上测试过一次不到`8h`就没电了（~~推测主要原因是`OLED`的耗电量巨大……~~即使关闭`OLED`显示再等到早上起来同样会没电）

## 0x02.`EVB_MX_Plus`
配套的联网模块使用`ESP8266`模组，这个用的再熟悉不过了，也赠送了`RoLa`模组，但是在公开的覆盖图上并没有看到市内有覆盖，因此暂时仍旧使用前者
另外的拓展`E51`模块足够使用，也没有额外购买其他型号的（
板子拿到手的那个周末就照着例程成功对接上了，见[EVB_MX_Plus 对接腾讯云物联网开发平台](./qcloud-iot-explorer.html)，不得不说`物联网开发平台`是真的方便（除了因自己没看好烧错例程无法对接之外），`demo`程序可以实现云端控制灯的开关（顺便吐槽下这个灯真是巨亮无比）
~~然后去看板子上的其他传感器：`温、湿、光`应有尽有，~~另外在例程里也看到了`DHT11`的适配，~~估计~~已经找个`PIN`给接上~~就也能~~使用了
`2020-4-23 23:42:42`：
看到`DHT11_BUS.c`库还是忍不住把之前放在`NodeMCU`上的`DHT11`拔下来插到板子上了`hhh`

作为个人业余开发者，并没有接触过工业（商业）产品的经验。所以觉得应该致力于解决贴近自己现实生活中的需求
对于老生常谈的`温湿度监控`已经基于`NodeMCU`+`DHT11`实现，这里就围绕着另一个「课题」进行方案落地
> 去年`tb`上买了一盆文竹，但是因为种种原因（懒）要么是好几天没浇水，要么是一浇就浇多了……
本来刚拿到手的时候是绿绿的，到了现在已经变黄了，惨……

因此决定监测植物的湿度，于是立即去`tb`购买传感器等相关配件
虽然确实是用了`红包省钱卡`的`5`元无门槛红包，但是其实也不是很贵的样子
![6.94](https://i1.yuangezhizao.cn/Win-10/20200420225355.png!webp)

拿到手后首先来看`土壤湿度传感器`，这个传感器说到底还是国内的厂子自己生产的，引出的两根线接到另外一块比较器板子上
型号选的是`4 PIN`的，即除了输入的电源和地之外，输出既有`A`也有`D`，数字量`D`其实是依赖于`LM358`来比较电压大小，因此可以手动调节板子上的滑动变阻器来改变开始输出的阈值
同时板子上除了电源有`LED`指示之外，另一个`LED`正是和`D`口状态同步的，这里毕竟要看数值，因此选择`A`口怼到开发板的`ADC1`上来测量其实际电压
电压拿到手之后还需要映射到湿度范围上，虽然实际关系可能不是近似于线性，但是这里还是当做线性处理了
相对湿度的计算方法很简单，放空气中是`4V`（`0%`）左右，插水里面是`1V`（`100%`）左右
即：`soil_humi = (4000 - adValue) / 30;`（请无视混用了`下划线`和`驼峰`命名法

然后就是小水泵了，这玩楞直接插`5V`流速实在是太快了（主要还是花盆太小了），而且不清楚能不能加上负反馈调节（学过的《自动控制原理》还略有印象）
`1m`长的水管拿到手发现巨长，于是拿小刀割出`20cm`，足够使用了
回头去翻商品详情发现了这么一段话，没错`绝对湿度值`并不适用于`土壤`
![绝对湿度值](https://i1.yuangezhizao.cn/Win-10/20200421225320.jpg!webp)

这水泵电流`120mA`，直接拿单片机`GPIO`口是驱动不了的，可以选择外接一个**三极管**搞定，并且不能长时间工作因为会影响到板子的供电？实测不大一会`mqtt`通信就报错断开了，串口输出还能看到路径乱码？？？
目前的解决方法是，每次只接通`3s`之后就断开，这个水量也足够一次短暂的补充了（花盆小
![0.12](https://i1.yuangezhizao.cn/Win-10/20200423233914.jpg!webp)

`2020-4-22 21:30:23`：
<details><summary>点击此处 ← 查看折叠</summary>

晚上挖掘~~`E53_IA1.pdf`~~`E53_SC1.pdf`原理图
首先要引入`E51`的概念，从原理图提供的信息可以得知这是国内自定的一个接口标准
![E51](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20200422_214907.jpg!view)
![实物对照](https://i1.yuangezhizao.cn/Win-10/20200422221337.jpg!webp)

正面左侧`SHT30`中间`LED`右侧`PT4211E23E`~~`BH1750`~~，`D2`橙色？的二极管还是可以辨识出来的，光照传感器仔细看也能看见上面的采集框
![E53_SC1 正面](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20200422_212842.jpg!view)

背面`ERRPROM`，但是目前存储足够并没有需求使用
![E53_SC1 背面](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20200422_212736.jpg!view)

~~然后就发现了有电机（水泵）预留位……~~
~~因为图中标出了`motor sw`和`motor`，这不明显的拿前者控制后者嘛，并且猜测是拉低`motor sw`导致`motor`接地（实物中`D2`那么大的二极管搁那放着的呢……~~结果看错图草
![E53 Interface IA1](https://i1.yuangezhizao.cn/Win-10/20200422213252.jpg!webp)

~~另，之前的`基于TencentOS tiny开源项目的实践--从零开始快速打造IoT小应用.pdf`介绍中拓展板`E53_IA1`是实装有电机和`DHT11`的，这也解释了为什么源码中有`DHT11_BUS.c`但是并没有`SHT30`的设备驱动~~
![E53_SC1](https://i1.yuangezhizao.cn/Win-10/20200422220433.jpg!webp)

顺便吐槽下`DHT11`的湿度百分比竟然是个浮点数？？？之前一直都是只有整数位的……
![湿度](https://i1.yuangezhizao.cn/Win-10/20200422221143.jpg!webp)
</details>

最后的水位传感器，是准备放在储水容器之中来测量剩余可用水量，目前并未实装（原因不仅在于需要寻找空余的`GPIO`口，更在于又需要找`5V`供电……
虽然买了一堆传感器可以直接把状态数据推到云上，但是每多一个传感器就需要多一处供电啊（
当然了，这个同样是输出模拟值，需要从`GPIO`口进行`ADC`采集来读取其电压值来判定水位线，基本思路是一样的

## 0x03.代码
[gh](https://github.com/yuangezhizao/EVB_MX_Plus)
说到底还是`C51`的基础不够，搞一个编译`pass`都得排半天的错
![编译通过！](https://i1.yuangezhizao.cn/Win-10/20200420234447.jpg!webp)

## 0x04.[腾讯云物联网开发平台](https://web.archive.org/web/20200421114636/https://cloud.tencent.com/document/product/1081)
来上云吧，进入[控制台](https://console.cloud.tencent.com/iotexplorer)，印象里早在公测的时候就申请到了名额
![物联网开发平台](https://i1.yuangezhizao.cn/Win-10/20200421194538.jpg!webp)

这里有两个项目：`智能灯`那个是板子的示例项目，`flower`是自己新建的项目
![开发中心-产品开发](https://i1.yuangezhizao.cn/Win-10/20200421194743.jpg!webp)
![数据模板](https://i1.yuangezhizao.cn/Win-10/20200423235158.jpg!webp)
![设备开发](https://i1.yuangezhizao.cn/Win-10/20200423235245.jpg!webp)
![交互开发](https://i1.yuangezhizao.cn/Win-10/20200423235311.jpg!webp)
![面板配置](https://i1.yuangezhizao.cn/Win-10/20200423235343.png!webp)
![设备调试](https://i1.yuangezhizao.cn/Win-10/20200423235412.jpg!webp)
![设备信息](https://i1.yuangezhizao.cn/Win-10/20200423235517.png!webp)
![下发指令](https://i1.yuangezhizao.cn/Win-10/20200423235607.jpg!webp)

比较实用的还有`数据开发`功能，可以实现自己的逻辑
![画图](https://i1.yuangezhizao.cn/Win-10/20200423235803.jpg!webp)

`输出`部分的`APP 推送`暂时还用不上，因此选择`公众号推送`方式，即报警消息通过微信服务号推送给自己
`处理`部分的`数据过滤`其实就是判定条件，比如湿度低于`70%`触发等等
`输入`部分的`设备数据`即传感器读取的湿度数据，`设备事件`即通过`event`上报的`事件`，同理`设备状态`也是类似的（都是在读传感器嘛

`EVB_MX_Plus`出厂的开关位置控制了`USB`接口插到`PC`上为**串口**使用由`CH340`驱动，烧录是用了另外的接口因此互不影响（这板子设计的真是妙啊
另外，如果接上`ST-Link`的话，就无法使用物理开关控制断电了，它会强制供电，烧录完成之后可以按下板子上的复位键来重启，就不需要拔插`ST-Link`了
而只接`USB`线就可以使用物理开关，并且会给板子上的锂电池充电
![串口助手](https://i1.yuangezhizao.cn/Win-10/20200420233903.jpg!webp)

## 0x05.连线图
![完整图](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20200424_000415.jpg!view)

## 0x06.小程序
源码自带小程序端，照着模板不到半小时就能预览出来（顺便发现代码里明文`SECRET_ID`和`SECRET_KEY`……这个还是得拿`CAM`单独建个只读`API`密钥
![v0.2](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-04-23-23-27-24-879_com.tencent.mm.jpg!webp)

也可以使用`腾讯连连`，从官方控制台配好`UI`之后直接扫码就可以使用了，非常方便
![flower](https://i1.yuangezhizao.cn/Redmi-K20Pro/Screenshot_2020-04-24-00-14-46-415_com.tencent.mm.jpg!webp)

## 0x07.实验室站
这里的构想是通过`数据同步`将数据存储至私有库中，并使用`Grafana`之类的可视化工具查看
`数据同步`即将设备通过`MQTT`上报的数据以`HTTP`形式发送至自己的云主机上，通过`Flask`开一个接口接收并存储至`MySQL`就搞定了
此构想其他项目已实现，~~暂未~~此处已实装
![接收数据](https://i1.yuangezhizao.cn/Win-10/20200514232540.jpg!webp)

示例`Flask`代码，上传接口未做来源验证，后期可以自行加个`token`做双方校验
``` python
@api.route('/IOT/flower', methods=['GET', 'POST'])
def IOT_flower():
    if 'upload' in request.args:
        data = json.loads(request.get_data(as_text=True))
        seq = data.get('seq')
        timestamp = data.get('timestamp')
        topic = data.get('topic')
        productid = data.get('productid')
        devicename = data.get('devicename')
        brightness = data.get('payload').get('params').get('brightness')
        humidity = data.get('payload').get('params').get('humidity')
        temperature = data.get('payload').get('params').get('temperature')
        soil_humi = data.get('payload').get('params').get('soil_humi')
        light_switch = data.get('payload').get('params').get('light_switch')
        motor_switch = data.get('payload').get('params').get('motor_switch')
        return upload(seq, timestamp, topic, productid, devicename, brightness, humidity, temperature, soil_humi,
                      light_switch, motor_switch)
    elif 'devicename' in request.args:
        devicename = request.args['devicename']
        if devicename:
            return get_multidata_from_mysql(devicename)
        else:
            return bad_request('参数值为空')
    else:
        return bad_request('非法参数')
```
![数据预览](https://i1.yuangezhizao.cn/Win-10/20200514233151.jpg!webp)

即可用`https://lab.yuangezhizao.cn/api/v0.0.1/IOT/flower?devicename=dev001`接口进行访问
![api](https://i1.yuangezhizao.cn/Win-10/20200514231423.jpg!webp)

`Grafana`里选好数据源就也可以进行可视化了
![datasources](https://i1.yuangezhizao.cn/Win-10/20200514232901.jpg!webp)

## 0x08.HomeAssistant
这里的构想是接入`HomeAssistant`，可使用其进行查看，并配置`HomeKit`对接`IOS`家庭，即可用`Siri`语音控制
方案一：结合上面的`数据同步`，数据就触手可及了，自有源也不必担心消耗过多的请求量
`HomeAssistant`里有一种`sensor`平台是`command_line`，即把执行`shell`获取到的数据为数据来源，直接写个读`MySQL`的`shell`就`ok`了
有这个`command_line`就可以任意对接了，爽到（
~~方案二：连接到云上`MQTT`……~~
此构想其他项目已实现，~~暂未~~此处已实装
![文档](https://i1.yuangezhizao.cn/Win-10/20200514223316.jpg!webp)
``` bash
sensor:
  - platform: command_line
    name: soil_humi
    command: python3 -c "import requests; print(requests.get('https://lab.yuangezhizao.cn/api/v0.0.1/IOT/flower?devicename=dev001').json()['data']['soil_humi'])"
    unit_of_measurement: "%"

  - platform: command_line
    name: yuangezhizao's room temperature
    command: python3 -c "import requests; print(requests.get('https://lab.yuangezhizao.cn/api/v0.0.1/IOT/flower?devicename=dev001').json()['data']['temperature'])"
    unit_of_measurement: "°C"

  - platform: command_line
    name: yuangezhizao's room humidity
    command: python3 -c "import requests; print(requests.get('https://lab.yuangezhizao.cn/api/v0.0.1/IOT/flower?devicename=dev001').json()['data']['humidity'])"
    unit_of_measurement: "%"

  - platform: command_line
    name: brightness
    command: python3 -c "import requests; print(requests.get('https://lab.yuangezhizao.cn/api/v0.0.1/IOT/flower?devicename=dev001').json()['data']['brightness'])"
    unit_of_measurement: "lx"
```
![实际接入](https://i1.yuangezhizao.cn/iPad/img_2412.png!webp)

## 0x09.HomeKit
打开家庭可以同步看到传感器的状态，这里有个坑就是`温度`传感器可以显示，但是`湿度`不行，解决方法是自定义属性
```
sensor.soil_humi:
  friendly_name: 土壤湿度
  device_class: humidity

sensor.brightness:
  friendly_name: 光照强度

sensor.yuangezhizao_s_room_humidity_2:
  friendly_name: 房间湿度
  device_class: humidity

sensor.yuangezhizao_s_room_temperature_2:
  friendly_name: 房间温度
```
![配置文件](https://i1.yuangezhizao.cn/Win-10/20200514234621.jpg!webp)
![实际接入](https://i1.yuangezhizao.cn/iPad/img_2408.png!webp)

也可以召唤`Siri`
![实际接入](https://i1.yuangezhizao.cn/iPad/img_2410.png!webp)
![实际接入](https://i1.yuangezhizao.cn/iPad/img_2411.png!webp)

## 0x09.后记
总的来说收获还是巨大的（`wx`群里都是巨佬，瑟瑟发抖……
未完待续……