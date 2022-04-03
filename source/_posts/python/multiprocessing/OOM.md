---
title: 记一次多进程使用不当的 OOM 翻车经历
date: 2021-10-28 01:00:00
tags:
  - OOM
  - multiprocessing
  - Elasticsearch
count: 2
os: 1
os_1: Monterry 12.0.1 (21A559)
browser: 0
browser_1: 95.0.4638.69 Stable
place: 福州
key: 122
---
    可遇不可求的经历，月更素材不请自来
<!-- more -->
## 0x00.前言
早上被前辈敲门叫醒，一看手机客户在`wx`群里说服务器`SSH`登不上去，叫我们赶紧过去

## 0x01.问题确认
去了一看`SSH`是可以登录的，只不过服务端回显特别慢，凭经验看有点像内存或硬盘爆满的现象
因为速度实在是太慢了于是放弃`SSH`，登录到`CIMC`（相当于`VNC`）的界面，一看一整页的`OOM Killer`已经开始制裁（第一个是`java`，后面的都是`python3`
那么问题已经确认，是系统发生了`OOM`，路上还在各种猜测比如是硬盘炸了之类的……
`emmm`，想了一下可能是自己昨天从多线程切换到了多进程所导致的，进入`top`再按<kbd>C</kbd>键，然后一整屏的`python3 collector.py`，粗略估算首屏就有二三十个了
而且所占内存巨大，物理机`128G`内存，平常基本浮动在`64G`左右，这时候`free -m`的整机内存所剩无几
> 下注：现网真实复现数据

``` bash
[root@node1 ]# free -m
        total   used    free    shared  buff/cache  available
Mem:    128406  127181  396     59      828         370
Swap:   51199   8086    43113
[root@node1 ]# ps -ef | grep collector
root 16065  113930  3   15:09   ?   00:00:18    -venv/bin/python3 collector.py
首屏非全部，省略后续`49+`行……
```
## 0x02.恢复服务
也很纳闷，早在前一天下午就讨论到了使用多进程有`OOM`风险~~，也只开了`max_workers`为`4`的进程池，怎么就会爆内存了呢？~~
但是首先还是要恢复服务，把`ps -ef`出的`collector`进程全都`kill`掉，并且用`supervisorctl`把对应的子服务关闭，内存算是回到了正常水平
然后就是各种第三方组件的恢复，最后`Kafka`一直启动不能，`messages`里也一直有`error`报错，临时删掉`data`再启动也终于恢复了

## 0x03.等待复现
这时候还没换回多线程，准备先跑着看看会不会还有问题……结果果不其然，下午做完核酸检测回来的时候前辈说复现了，现场还在，正准备开始`kill`
操作巨卡无比已是在意料之中，上来就`free -m`一看果然内存又基本跑满，再通过`top`看有非常多的`python3`，都得翻到第二页才能看完
虽然没来得及手动`kill`，不过赶巧等了一会儿这些进程都结束了，翻日志发现刚刚写入了一个含`7850484`条记录的索引，耗时`490.36`秒
先不说其他的，`7850484`应该是遇到的每小时级别最大的键了，其实这个键的写入操作本来是应该在半夜`3`点后的定时任务里去完成的
结果半夜直接`OOM`一直没有完成，拖到了下午`3`点又开始跑定时任务的时候就复现了

## 0x04.溯源分析
是时候贴一下关键函数的源码了，这一个函数里就写了俩`bug`简直了
``` python
def bulk_load_to_es_by_pool_executor(df_content, timestamp, index_name_type):
    """
    Refer to
    https://web.archive.org/web/20210323141917/https://discuss.elastic.co/t/helpers-parallel-bulk-in-python-not-working/39498
    https://web.archive.org/web/20210720072749/https://www.jianshu.com/p/b9b3d66aa0be
    """
    try:
        s_t = time.time()

        flows_split_size = CFG.config.get('flows_split_size')
        use_thread_pool = CFG.config.get('use_thread_pool')
        thread_pool_max_workers = CFG.config.get('thread_pool_max_workers')

        content = generate_all_content(df_content, timestamp, index_name_type)
        LOG.debug(f'generate_all_content completed in {str(time.time() - s_t)}s')

        content_list = split_all_content(content, flows_split_size)
        # LOG.debug(f'content_list completed in {str(time.time() - s_t)}s')

        # 210803 change from ThreadPoolExecutor to ProcessPoolExecutor, bypass GIL
        # https://docs.python.org/zh-cn/3/library/concurrent.futures.html#processpoolexecutor
        if use_thread_pool:
            executor = ThreadPoolExecutor(max_workers=int(thread_pool_max_workers))
        else:
            executor = ProcessPoolExecutor()
        all_task = [executor.submit(bulk_in_thread, (each)) for each in content_list]

        wait(all_task, return_when=ALL_COMPLETED)

        LOG.info(f'bulk_load_to_es count {len(content)} completed in {str(time.time() - s_t)}s')
    except Exception as err:
        raise CollectorException('error occured when post raw flows to es, %s' % str(err))
```
### 1.`content`过大
没错，`content`就是那个含有`7850484`条记录的`bulk`的请求体，粗略估测不超过`15MB * 66 = 990MB`，也就是接近`1G`的大小
而创建`ProcessPoolExecutor()`时`content`变量已经存在，`multiprocessing`启动进程的方法在`Unix`中的默认值是`fork`
也就是说`fork`出来的每一个进程都会拷贝一份`content`变量，造成不必要的内存开销

### 2.未限制`max_workers`
翻阅了一下`gitlab`的历史，可以看出最开始用的`ThreadPoolExecutor`是有显式设定`max_workers`的，但是`ProcessPoolExecutor`却没有传入`max_workers`
想了下原因是，当初看到文档`max_workers`默认是机器的处理器个数，想着应该不需要手动设定数量吧，所以到头来代码里就一直没有给多进程设置`max_workers`的地方……
`lab`里测试环境的`CPU`是`16`再不就是`32`，而现网环境是直接把`CentOS`装到了物理机上，也没有`ESXi`之类的虚拟化平台，`CPU`就是`64`……

以上两个原因，导致在处理`7850484`条记录时占用接近`64G`的内存，加上平常基本浮动在`64G`左右，合计就接近`128G`
半夜的时候超过`128G`导致`OOM`，而次日下午是刚恢复完其他服务没有占用过多内存才勉强运行完成

## 0x05.代码重构
### 1.`content`过大
未完待续……

### 2.限制`max_workers`
`executor = ProcessPoolExecutor(max_workers=int(thread_pool_max_workers))`

## 0x06.后记
现网`OOM`有被吓到，本来都订了当晚回来的机票，被迫取消留用晚了一天才回来（

## 0x07.引用
[Python 调用 elasticsearch 的 bulk 接口批量插入数据出现内存泄露，导致 OOM](https://web.archive.org/web/20211030114138/https://www.v2ex.com/t/329311)
