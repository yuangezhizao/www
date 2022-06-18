---
title: 记一次 Kafka 未增大文件描述符限制的翻车经历
date: 2022-04-29 22:51:24
tags:
  - Kafka
  - Log4j
count: 2
os: 1
os_1: Monterry 12.3.1 (21E258)
browser: 0
browser_1: 101.0.4951.41 Stable
place: 新家
key: 140
---
    记一次翻车经历系列，第二篇新鲜出炉
<!-- more -->
## 0x00.`TL;DR`
https://mastodon.yuangezhizao.cn/@yuangezhizao/108214813032210497

## 0x01.前言
周二早上起床睁开朦胧的睡眼，打开手机发现`wx`群里有新消息，说一节点的硬盘满了……并且已经引发其他组件的异常
瞬间清醒起来，大脑高速运转猜想到底是哪里出的问题，不到一个小时客户就已经准备好环境，我们这边可以进行远程连接了

## 0x02.问题确认
好在`SSH`还是可以正常连接上的，操作起来也没有卡顿之类的异样感，`df -h`看硬盘确实满了，然后`dh -h --max-depth=1`排查到底是哪个文件夹惹的祸
好家伙找到了，`/kafka`占用`327G`草……继续深入`logs`文件夹，发现二十多个每个占用`12G`的`server.log`日志文件，自`2022-04-23-12`至`2022-04-24-20`
迫不及待的等着看里面到底写了啥，结果全是`Too many open files`的报错信息，心里的一块石头落地了
``` log
[2022-04-24 20:59:58,804] ERROR Error while accepting connection (kafka.network.Acceptor)
java.io.IOException: Too many open files
        at sun.nio.ch.ServerSocketChannelImpl.accept0(Native Method)
        at sun.nio.ch.ServerSocketChannelImpl.accept(ServerSocketChannelImpl.java:421)
        at sun.nio.ch.ServerSocketChannelImpl.accept(ServerSocketChannelImpl.java:249)
        at kafka.network.Acceptor.accept(SocketServer.scala:460)
        at kafka.network.Acceptor.run(SocketServer.scala:403)
        at java.lang.Thread.run(Thread.java:748)
```
再追溯到前面一点儿的日志文件内容，前辈说是在`commit`偏移量的时候产生的报错
``` log
[2022-04-23 16:06:59,117] ERROR Error while writing to checkpoint file /usr/local/kafka/log/kafka/log-start-offset-checkpoint (kafka.server.LogDirFailureChannel)
java.io.FileNotFoundException: /usr/local/kafka/log/kafka/log-start-offset-checkpoint.tmp (Too many open files)
```

## 0x03.恢复服务
首先释放硬盘空间，删除这两天内过大的日志文件
``` bash
rm -rf server.log.2022-04-23*
rm -rf server.log.2022-04-24*
```

## 0x04.增大文件描述符限制
1. 参照官方文档：[OS](https://web.archive.org/web/20220429161854/https://kafka.apache.org/documentation/#os)
> File descriptor limits: Kafka uses file descriptors for log segments and open connections. If a broker hosts many partitions, consider that the broker needs at least (number_of_partitions)*(partition_size/segment_size) to track all log segments in addition to the number of connections the broker makes. We recommend at least 100000 allowed file descriptors for the broker processes as a starting point. Note: The mmap() function adds an extra reference to the file associated with the file descriptor fildes which is not removed by a subsequent close() on that file descriptor. This reference is removed when there are no more mappings to the file.

2. 参照：[kafka 中遇到的问题](https://web.archive.org/web/20220429160053/https://noby.in/kafkaq/)
> 对于一个高并发高性能的应用来说，`1024`或者`4096`的**文件描述符**限制未免太少，可以适当的调大这个参数。比如使用`ulimit -n 65535`命令将上限提高到`65535`，这样足以应对大多数的应用情况

因为是`Kafka`是用`systemd`来启动的，所以修改`/etc/sysctl.conf`或者`/etc/security/limits.conf`对其是不生效的，因为它仅对`PAM`登录的用户生效
1. 首先`systemctl status kafka`定位到单元文件的位置
2. 然后`vim kafka.service`增加`LimitNOFILE=65535`一行
3. 最后`systemctl daemon-reload`
4. 再次`systemctl start kafka`看到启动成功了，松了一口气

当然，重启之后还是要看一下文件描述符的限制是否变大了
1. 首先`ps -ef | grep kafka`可以过滤到两个`PID`，其中一个是`Kakfa`，另一个是`Zookeeper`
2. 然后`cat /proc/<Kakfa_PID>/limits`查看`Max Open Files`值是`65535`就没有问题啦

最后，也可以通过`lsof -p <Kakfa_PID> | wc -l`查看占用了多少个文件描述符

## 0x05.限制日志文件大小
万万没想到的是，谷歌`Kafka 日志`出来的结果全是针对于**数据**的设置，而不是**日志**的设置……
经过不懈努力终于找到一篇`medium`的看上去还算靠谱的文章：[Kafka Limit Server Logs](https://web.archive.org/web/20220429161138/https://medium.com/@abdullahtrmn/kafka-limit-server-logs-c00784a4038f)，需要修改`Kafka`路径下`config`文件夹中的`log4j.properties`配置文件
1. 把`log4j.appender.kafkaAppender=org.apache.log4j.RollingFileAppender`改成`log4j.appender.kafkaAppender=org.apache.log4j.DailyRollingFileAppender`
这样就不是按日切分，而是可以按照大小和个数切分
2. 追加`MaxFileSize`和`MaxBackupIndex`限制
``` conf
log4j.appender.kafkaAppender.MaxFileSize=500MB
log4j.appender.kafkaAppender.MaxBackupIndex=10
```
3. 最后`systemctl restart kafka`重启生效

备注：`kafkaAppender`默认输出的是`server.log`，其他`log`暂未修改？

## 0x06.后记
1. <span title="你知道的太多了" class="heimu">部署文档没写好，现网翻车火葬场</span>
2. 其实恢复`Kafka`很快就搞完了，但是果不其然`systemctl start mariadb`又`failed`了淦，直到晚上八点多才恢复正常（中途远程设备电量不足提前倒下，被迫暂停了一段时间
<span title="你知道的太多了" class="heimu">自己好心疼前辈刚集中隔离结束回家但晚上还在远程</span>，不过关于`MariaDB Galera Cluster`的话题，还是再单拎出一篇文章来讲吧（继续挖坑

## 0x07.引用
[Kafka too many open files解决](https://web.archive.org/web/20220429155307/https://blog.51cto.com/u_15072910/3961649)
[kafka too many open files的解决方法](https://web.archive.org/web/20220615072645/https://www.jianshu.com/p/1a48a4920088)
