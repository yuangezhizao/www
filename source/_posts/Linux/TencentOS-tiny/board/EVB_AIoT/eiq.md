---
title: 【AIoT应用创新大赛】基于 EVB_AIoT 的 EIQ 学习笔记
date: 2022-03-12 13:23:09
tags:
  - TencentOS-tiny
  - EVB_AIoT
  - RT1062
count: 1
os: 1
os_1: Monterry 12.2.1 (21D62)
browser: 0
browser_0: 99.0.4844.51 Stable
place: 新家
key: 134
---
    比赛寄了，只能勉强交个作业
<!-- more -->
## 0x00.`TL;DR`
> 推荐阅读首发于云+社区的初赛超详细の长文：[AIoT应用创新大赛-基于 EVB_AIoT 的 EIQ 学习笔记](https://cloud.tencent.com/developer/article/1956609)

而下文仅为在折腾过程中的一些额外的琐碎片段补充，并无过多阅读价值

## 0x01.前言
<span title="你知道的太多了" class="heimu">接上文，转眼间快一个月就过去了
twitter.com/yuangezhizao/status/1503454256069677056
甚至这篇文章在十天前创建，今晚打开`VSCode`才想起还没给发出来，健忘越来越严重了
</span>

## 0x02.[eIQ® ML Software Development Environment](https://web.archive.org/web/20220312052511/https://www.nxp.com/design/software/development-software/eiq-ml-development-environment:EIQ)
奇怪的是页面上的`eIQ Toolkit`和`eIQ Portal`对应的是都是前者的链接，`eIQ Portal`是进不去了……
不过不像`MCUXpressoIDE_11.5.0`有`Linux`、`MAC`和`Windows`三个平台的版本，`eIQ Toolkit`的只有`windows`版本，而自己用的是`MAC`，于是打开台式机下载后安装
结果安装完`eIQ Toolkit`，显示`Launch eIQ Portal`，`emmm`，原来是整合到一起了

<details><summary>点击此处 ← 查看折叠</summary>

![eIQ_Toolkit_v1.2.5.375_b220118.exe](https://i1.yuangezhizao.cn/macOS/20220312133808.png!webp)
![主界面](https://i1.yuangezhizao.cn/macOS/20220312134058.png!webp)

</details>

最快的入门方法自然是导入官方例程了，`1060`的`SDK`里提供了非常多的五花八门的例程，毕竟不是官方开发板直接烧录后就能运行，这里可能需要修改引脚和其他配置才能运行

<details><summary>点击此处 ← 查看折叠</summary>

![1060](https://i1.yuangezhizao.cn/macOS/20220312135537.png!webp)
![eiq_examples](https://i1.yuangezhizao.cn/macOS/20220312140417.png!webp)

</details>

先直接编译，一般情况下肯定是成功的，毕竟是官方例程，可以看到`BOARD_SDRAM`的占用已经接近`30MB`了
``` bash
Finished building: ../board/pin_mux.c

Building target: evkmimxrt1060_deepviewrt_modelrunner.axf
Invoking: MCU Linker
arm-none-eabi-gcc -nostdlib -L"/Users/yuangezhizao/Documents/MCUXpressoIDE_11.5.0_7232/workspace/eiq_examples/evkmimxrt1060_deepviewrt_modelrunner/evkmimxrt1060/deepviewrt_modelrunner/eiq/deepviewrt/lib" -L"/Users/yuangezhizao/Documents/MCUXpressoIDE_11.5.0_7232/workspace/eiq_examples/evkmimxrt1060_deepviewrt_modelrunner/evkmimxrt1060/deepviewrt_modelrunner/CMSIS/DSP" -Xlinker --no-wchar-size-warning -Xlinker -Map="evkmimxrt1060_deepviewrt_modelrunner.map" -Xlinker --gc-sections -Xlinker -print-memory-usage -Xlinker --sort-section=alignment -Xlinker --cref -mcpu=cortex-m7 -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -T evkmimxrt1060_deepviewrt_modelrunner_Debug.ld -o "evkmimxrt1060_deepviewrt_modelrunner.axf"  ./xip/evkmimxrt1060_flexspi_nor_config.o ./xip/fsl_flexspi_nor_boot.o  ./utilities/fsl_assert.o ./utilities/fsl_debug_console.o ./utilities/fsl_str.o  ./startup/startup_mimxrt1062.o  ./source/lwip_dhcp_freertos.o ./source/modelrunner.o ./source/picohttp.o ./source/picohttpparser.o ./source/semihost_hardfault.o  ./phy/fsl_phyksz8081.o  ./mdio/fsl_enet_mdio.o  ./lwip/src/netif/ppp/auth.o ./lwip/src/netif/ppp/ccp.o ./lwip/src/netif/ppp/chap-md5.o ./lwip/src/netif/ppp/chap-new.o ./lwip/src/netif/ppp/chap_ms.o ./lwip/src/netif/ppp/demand.o ./lwip/src/netif/ppp/eap.o ./lwip/src/netif/ppp/eui64.o ./lwip/src/netif/ppp/fsm.o ./lwip/src/netif/ppp/ipcp.o ./lwip/src/netif/ppp/ipv6cp.o ./lwip/src/netif/ppp/lcp.o ./lwip/src/netif/ppp/lwip_ecp.o ./lwip/src/netif/ppp/magic.o ./lwip/src/netif/ppp/mppe.o ./lwip/src/netif/ppp/multilink.o ./lwip/src/netif/ppp/ppp.o ./lwip/src/netif/ppp/pppapi.o ./lwip/src/netif/ppp/pppcrypt.o ./lwip/src/netif/ppp/pppoe.o ./lwip/src/netif/ppp/pppol2tp.o ./lwip/src/netif/ppp/pppos.o ./lwip/src/netif/ppp/upap.o ./lwip/src/netif/ppp/utils.o ./lwip/src/netif/ppp/vj.o  ./lwip/src/netif/bridgeif.o ./lwip/src/netif/bridgeif_fdb.o ./lwip/src/netif/ethernet.o ./lwip/src/netif/lowpan6.o ./lwip/src/netif/lowpan6_ble.o ./lwip/src/netif/lowpan6_common.o ./lwip/src/netif/slipif.o ./lwip/src/netif/zepif.o  ./lwip/src/core/ipv6/dhcp6.o ./lwip/src/core/ipv6/ethip6.o ./lwip/src/core/ipv6/icmp6.o ./lwip/src/core/ipv6/inet6.o ./lwip/src/core/ipv6/ip6.o ./lwip/src/core/ipv6/ip6_addr.o ./lwip/src/core/ipv6/ip6_frag.o ./lwip/src/core/ipv6/mld6.o ./lwip/src/core/ipv6/nd6.o  ./lwip/src/core/ipv4/acd.o ./lwip/src/core/ipv4/autoip.o ./lwip/src/core/ipv4/dhcp.o ./lwip/src/core/ipv4/etharp.o ./lwip/src/core/ipv4/icmp.o ./lwip/src/core/ipv4/igmp.o ./lwip/src/core/ipv4/ip4.o ./lwip/src/core/ipv4/ip4_addr.o ./lwip/src/core/ipv4/ip4_frag.o  ./lwip/src/core/altcp.o ./lwip/src/core/altcp_alloc.o ./lwip/src/core/altcp_tcp.o ./lwip/src/core/def.o ./lwip/src/core/dns.o ./lwip/src/core/inet_chksum.o ./lwip/src/core/init.o ./lwip/src/core/ip.o ./lwip/src/core/mem.o ./lwip/src/core/memp.o ./lwip/src/core/netif.o ./lwip/src/core/pbuf.o ./lwip/src/core/raw.o ./lwip/src/core/stats.o ./lwip/src/core/sys.o ./lwip/src/core/tcp.o ./lwip/src/core/tcp_in.o ./lwip/src/core/tcp_out.o ./lwip/src/core/timeouts.o ./lwip/src/core/udp.o  ./lwip/src/apps/mdns/mdns.o ./lwip/src/apps/mdns/mdns_domain.o ./lwip/src/apps/mdns/mdns_out.o  ./lwip/src/apps/httpsrv/httpsrv.o ./lwip/src/apps/httpsrv/httpsrv_base64.o ./lwip/src/apps/httpsrv/httpsrv_fs.o ./lwip/src/apps/httpsrv/httpsrv_script.o ./lwip/src/apps/httpsrv/httpsrv_sha1.o ./lwip/src/apps/httpsrv/httpsrv_supp.o ./lwip/src/apps/httpsrv/httpsrv_task.o ./lwip/src/apps/httpsrv/httpsrv_tls.o ./lwip/src/apps/httpsrv/httpsrv_utf8.o ./lwip/src/apps/httpsrv/httpsrv_ws.o ./lwip/src/apps/httpsrv/httpsrv_ws_api.o  ./lwip/src/api/api_lib.o ./lwip/src/api/api_msg.o ./lwip/src/api/err.o ./lwip/src/api/if_api.o ./lwip/src/api/netbuf.o ./lwip/src/api/netdb.o ./lwip/src/api/netifapi.o ./lwip/src/api/sockets.o ./lwip/src/api/tcpip.o  ./lwip/port/enet_ethernetif.o ./lwip/port/enet_ethernetif_kinetis.o ./lwip/port/sys_arch.o  ./freertos/freertos_kernel/portable/MemMang/heap_3.o  ./freertos/freertos_kernel/portable/GCC/ARM_CM4F/port.o  ./freertos/freertos_kernel/croutine.o ./freertos/freertos_kernel/event_groups.o ./freertos/freertos_kernel/list.o ./freertos/freertos_kernel/queue.o ./freertos/freertos_kernel/stream_buffer.o ./freertos/freertos_kernel/tasks.o ./freertos/freertos_kernel/timers.o  ./drivers/fsl_cache.o ./drivers/fsl_clock.o ./drivers/fsl_common.o ./drivers/fsl_common_arm.o ./drivers/fsl_enet.o ./drivers/fsl_flexram.o ./drivers/fsl_flexram_allocate.o ./drivers/fsl_flexspi.o ./drivers/fsl_gpio.o ./drivers/fsl_gpt.o ./drivers/fsl_lpuart.o  ./device/system_MIMXRT1062.o  ./component/uart/fsl_adapter_lpuart.o  ./component/serial_manager/fsl_component_serial_manager.o ./component/serial_manager/fsl_component_serial_port_uart.o  ./component/lists/fsl_component_generic_list.o  ./board/board.o ./board/clock_config.o ./board/dcd.o ./board/pin_mux.o   -lmodelrunner-rt-flash -ldeepview-rt-cortex-m7f -larm_cortexM7lfdp_math
Memory region         Used Size  Region Size  %age Used
     BOARD_FLASH:      368624 B         8 MB      4.39%
     BOARD_SDRAM:    29496780 B        30 MB     93.77%
   NCACHE_REGION:         248 B         2 MB      0.01%
        SRAM_DTC:          0 GB       128 KB      0.00%
        SRAM_ITC:          0 GB       128 KB      0.00%
         SRAM_OC:          0 GB       768 KB      0.00%
Finished building target: evkmimxrt1060_deepviewrt_modelrunner.axf

Performing post-build steps
arm-none-eabi-size "evkmimxrt1060_deepviewrt_modelrunner.axf"; # arm-none-eabi-objcopy -v -O binary "evkmimxrt1060_deepviewrt_modelrunner.axf" "evkmimxrt1060_deepviewrt_modelrunner.bin" ; # checksum -p MIMXRT1062xxxxA -d "evkmimxrt1060_deepviewrt_modelrunner.bin";
   text	   data	    bss	    dec	    hex	filename
 365788	   2836	29494148	29862772	1c7ab74	evkmimxrt1060_deepviewrt_modelrunner.axf


14:26:33 Build Finished. 0 errors, 0 warnings. (took 11s.657ms)
```
结果发现需要依赖官网开发板的网线接口，才能让主机和开发板在同一网段内，并且官方例程是基于`FreeRTOS`的还依赖于`lwip`的`SOCKET`
而手上的开发板没有提供网线接口，用`ESP8266`虽然应该可以保证在同一网段内的，但是`SOCKET`好像还是得依赖于`lwip`
虽然手上有`LoRaWAN`模组，家里也有测试用网关，但感觉修改例程是个大活儿所以还是鸽了（

## 0x03.快速入门
使用示例脚本创建工程并导入数据集

<details><summary>点击此处 ← 查看折叠</summary>

``` bash
C:\nxp\eIQ_Toolkit_v1.2.5>cd workspace

C:\nxp\eIQ_Toolkit_v1.2.5\workspace>python CIFAR_uploader.py
2022-03-12 16:11:19.429964: I tensorflow/stream_executor/platform/default/dso_loader.cc:53] Successfully opened dynamic library cudart64_110.dll
Downloading data from https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
Traceback (most recent call last):
  File "urllib\request.py", line 1354, in do_open
  File "http\client.py", line 1252, in request
  File "http\client.py", line 1298, in _send_request
  File "http\client.py", line 1247, in endheaders
  File "http\client.py", line 1007, in _send_output
  File "http\client.py", line 947, in send
  File "http\client.py", line 1421, in connect
  File "ssl.py", line 500, in wrap_socket
  File "ssl.py", line 1040, in _create
  File "ssl.py", line 1309, in do_handshake
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: certificate has expired (_ssl.c:1131)

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\nxp\eIQ_Toolkit_v1.2.5\python\Lib\site-packages\tensorflow\python\keras\utils\data_utils.py", line 258, in get_file
    urlretrieve(origin, fpath, dl_progress)
  File "urllib\request.py", line 247, in urlretrieve
  File "urllib\request.py", line 222, in urlopen
  File "urllib\request.py", line 525, in open
  File "urllib\request.py", line 542, in _open
  File "urllib\request.py", line 502, in _call_chain
  File "urllib\request.py", line 1397, in https_open
  File "urllib\request.py", line 1357, in do_open
urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: certificate has expired (_ssl.c:1131)>

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "CIFAR_uploader.py", line 39, in <module>
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
  File "C:\nxp\eIQ_Toolkit_v1.2.5\python\Lib\site-packages\tensorflow\python\keras\datasets\cifar10.py", line 79, in load_data
    path = get_file(
  File "C:\nxp\eIQ_Toolkit_v1.2.5\python\Lib\site-packages\tensorflow\python\keras\utils\data_utils.py", line 262, in get_file
    raise Exception(error_msg.format(origin, e.errno, e.reason))
Exception: URL fetch failure on https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz: None -- [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: certificate has expired (_ssl.c:1131)
```

</details>

尝试配置代理`set HTTPS_PROXY=http://cn-py-dl-w2d:1081`结果还是不行，奇怪怎么还对于`urlretrieve`函数不生效
谷歌搜了一圈解决方法，直接下载`cifar-10-python.tar.gz`并重命名自`cifar-10-python.tar.gz`至`cifar-10-batches-py.tar.gz`
然后扔到用户文件夹`C:\Users\yuangezhizao\.keras\datasets`下，再次运行导入成功了，并且可以看到多了个`cifar-10-batches-py`的解压后的文件夹

## 0x04.后记
> 自己转行互联网写代码一年多了，没错脱离嵌入式行业也一年多了
感叹芯片的发展是真快，也感叹才一年没碰就已经有些许生疏了
虽说可以写比赛经历，但是看别人都搞出实际作品而自己寄了
觉得辜负了比赛举办方满满的诚意，愧对汪总（认真脸）
心里多少还是有亿点点失落呢
2022-03-15
远哥制造

## 0x05.引用
[Voice Intelligent Technology](https://www.nxp.com/design/software/embedded-software/voice-intelligent-technology:VOICE-INTELLIGENT-TECHNOLOGY)
[GUI Guider](https://www.nxp.com/design/software/development-software/gui-guider:GUI-GUIDER)
[TS-MACHINE-LEARNING-AND-AI](https://www.nxp.com/design/training/ai-and-machine-learning-training-academy:TS-MACHINE-LEARNING-AND-AI?cid=sp_pro506756_tac563550_avnt_1#community)
