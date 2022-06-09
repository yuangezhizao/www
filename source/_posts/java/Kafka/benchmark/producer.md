---
title: Apache Kafka Producer Benchmark
date: 2022-06-09 14:52:50
tags:
  - Kafka
count: 1
os: 1
os_1: Monterry 12.4 (21F79)
browser: 0
browser_1: 102.0.5005.61 Stable
place: 新家
key: 144
---
    一小时水一篇文章，不愧是我
<!-- more -->
## 0x00.前言
众所周知，压测都是从单机测起的，然后再拓展到集群环境，这也是上一篇文章中提到的「不得不在各个平台上都装一份，以便进行横向对比」

## 0x01.测试环境
虚拟机从来都不缺，要多少有多少（`bushi`

Hostname | CPU | RAM | Disk | OS
:---: | :---: | :---: | :---: | :---:
`cn-tx-bj1-r8` | 单核 | `2G` | 普通云硬盘 | `RHEL 8`
`cn-tx-bj6-u0` | 双核 | `4G` | `SSD`云硬盘 | `Ubuntu Server 20.04 LTS`
`cn-py-dl-r8` | 八核 | `16G` | 希捷机械硬盘 | `RHEL 8`

## 0x02.[kafka-producer-perf-test.sh](https://github.com/apache/kafka/blob/3.2/bin/kafka-producer-perf-test.sh)
因前辈给了这篇文章[kafka性能测试](https://web.archive.org/web/20220609070713/https://www.cnblogs.com/arli/p/12574524.html)，其中针对生产者的测试点挺详细的，自己也准备抄作业，于是花了两天折腾官方提供的这个脚本，没想到最后得出的结论却是并不适合用它来压测
### 1.粗测磁盘写入性能
「普通云硬盘」，`120`左右
``` bash
[root@cn-tx-bj1-r8 kafka_2.13-3.2.0]# dd if=/dev/zero of=dd-test bs=1M count=10240 oflag=direct
10240+0 records in
10240+0 records out
10737418240 bytes (11 GB, 10 GiB) copied, 87.3094 s, 123 MB/s
[root@cn-tx-bj1-r8 kafka_2.13-3.2.0]# dd if=/dev/zero of=dd-test bs=1M count=10240 oflag=direct
10240+0 records in
10240+0 records out
10737418240 bytes (11 GB, 10 GiB) copied, 88.8004 s, 121 MB/s
```
`SSD`云硬盘，`140`左右，对比「普通云硬盘」也并没有快多少
``` bash
ubuntu@cn-tx-bj6-u0:~/kafka_2.13-3.2.0$ dd if=/dev/zero of=dd-test bs=1M count=10240 oflag=direct
10240+0 records in
10240+0 records out
10737418240 bytes (11 GB, 10 GiB) copied, 75.0504 s, 143 MB/s
ubuntu@cn-tx-bj6-u0:~/kafka_2.13-3.2.0$ dd if=/dev/zero of=dd-test bs=1M count=10240 oflag=direct
10240+0 records in
10240+0 records out
10737418240 bytes (11 GB, 10 GiB) copied, 78.0834 s, 138 MB/s
```
「希捷机械硬盘」竟然是最快的，`200`左右，这可是没想到的
``` bash
[root@cn-py-dl-r8 kafka_2.13-3.2.0]# dd if=/dev/zero of=dd-test bs=1M count=10240 oflag=direct
10240+0 records in
10240+0 records out
10737418240 bytes (11 GB, 10 GiB) copied, 53.753 s, 200 MB/s
[root@cn-py-dl-r8 kafka_2.13-3.2.0]# dd if=/dev/zero of=dd-test bs=1M count=10240 oflag=direct
10240+0 records in
10240+0 records out
10737418240 bytes (11 GB, 10 GiB) copied, 54.2146 s, 198 MB/s
```

### 2.创建`Kafka`单节点单分区的主题
`cn-tx-bj1-r8`
``` bash
[root@cn-tx-bj1-r8 kafka_2.13-3.2.0]# bin/kafka-topics.sh --describe --topic test --bootstrap-server localhost:9092
Topic: test     TopicId: hEm3koInQpaUn61qzF5xnA PartitionCount: 1       ReplicationFactor: 1    Configs: segment.bytes=1073741824
        Topic: test     Partition: 0    Leader: 0       Replicas: 0     Isr: 0
```
`cn-tx-bj6-u0`：[#108440595160620768](https://mastodon.yuangezhizao.cn/@yuangezhizao/108440595160620768)
``` bash
ubuntu@cn-tx-bj6-u0:~/kafka_2.13-3.2.0$ bin/kafka-topics.sh --describe --topic test --bootstrap-server localhost:9092
Topic: test     TopicId: at6ZMlLCQr256EbLyFuKdw PartitionCount: 1       ReplicationFactor: 1    Configs: segment.bytes=1073741824
        Topic: test     Partition: 0    Leader: 0       Replicas: 0     Isr: 0
```
`cn-py-dl-r8`：[#108440262738706509](https://mastodon.yuangezhizao.cn/@yuangezhizao/108440262738706509)
``` bash
[root@cn-py-dl-r8 kafka_2.13-3.2.0]# bin/kafka-topics.sh --describe --topic test --bootstrap-server localhost:9092
Topic: test     TopicId: FzMw9nyaQ6Kncgqmp1TBqw PartitionCount: 1       ReplicationFactor: 1    Configs: segment.bytes=1073741824
        Topic: test     Partition: 0    Leader: 0       Replicas: 0     Isr: 0
```

### 3.运行生产者性能测试
参数中指定的`config/producer.properties`配置文件保持了默认，其实也尝试过修改其中的`linger.ms`和`batch.size`等参数，虽然确实可能有效果提升[#108441932955929068](https://mastodon.yuangezhizao.cn/@yuangezhizao/108441932955929068)
但毕竟并不使用`Java`版本的生产者，所以就不浪费时间在这里调参了，之后还得去研究实际会用的`librdkafka`的调参呢，原始结果见[#108446732693126948](https://mastodon.yuangezhizao.cn/@yuangezhizao/108446732693126948)

<details><summary>点击此处 ← 查看折叠</summary>

``` bash
[root@cn-py-dl-r8 kafka_2.13-3.2.0]# cat config/producer.properties
############################# Producer Basics #############################

# list of brokers used for bootstrapping knowledge about the rest of the cluster
# format: host1:port1,host2:port2 ...
bootstrap.servers=localhost:9092

# specify the compression codec for all data generated: none, gzip, snappy, lz4, zstd
compression.type=none

# name of the partitioner class for partitioning records;
# The default uses "sticky" partitioning logic which spreads the load evenly between partitions, but improves throughput by attempting to fill the batches sent to each partition.
#partitioner.class=

# the maximum amount of time the client will wait for the response of a request
#request.timeout.ms=

# how long `KafkaProducer.send` and `KafkaProducer.partitionsFor` will block for
#max.block.ms=

# the producer will wait for up to the given delay to allow other records to be sent so that the sends can be batched together
#linger.ms=

# the maximum size of a request in bytes
#max.request.size=

# the default batch size in bytes when batching multiple records sent to a partition
#batch.size=

# the total bytes of memory the producer can use to buffer records waiting to be sent to the server
#buffer.memory=
```

</details>

`cn-tx-bj1-r8`毕竟是单核，测试时跑爆`CPU`，明显只有一个核是不够用的，限制了压测脚本的生产能力
``` bash
[root@cn-tx-bj1-r8 kafka_2.13-3.2.0]# free -h
              total        used        free      shared  buff/cache   available
Mem:          1.8Gi       935Mi       151Mi        97Mi       725Mi       616Mi
Swap:            0B          0B          0B
[root@cn-tx-bj1-r8 kafka_2.13-3.2.0]# bin/kafka-producer-perf-test.sh --topic test --num-records 5000000 --record-size 1024 --throughput -1 --producer.config config/producer.properties
8101 records sent, 1615.7 records/sec (1.58 MB/sec), 1776.0 ms avg latency, 3082.0 ms max latency.
23205 records sent, 4638.2 records/sec (4.53 MB/sec), 4635.7 ms avg latency, 5953.0 ms max latency.
41175 records sent, 8231.7 records/sec (8.04 MB/sec), 4726.7 ms avg latency, 6319.0 ms max latency.
26325 records sent, 5253.4 records/sec (5.13 MB/sec), 4324.2 ms avg latency, 5742.0 ms max latency.
33810 records sent, 6759.3 records/sec (6.60 MB/sec), 5495.2 ms avg latency, 6051.0 ms max latency.
65160 records sent, 13026.8 records/sec (12.72 MB/sec), 2984.7 ms avg latency, 5282.0 ms max latency.
101505 records sent, 20296.9 records/sec (19.82 MB/sec), 1509.4 ms avg latency, 1830.0 ms max latency.
123780 records sent, 24741.2 records/sec (24.16 MB/sec), 1256.6 ms avg latency, 1516.0 ms max latency.
108870 records sent, 21774.0 records/sec (21.26 MB/sec), 1293.2 ms avg latency, 1742.0 ms max latency.
115395 records sent, 23079.0 records/sec (22.54 MB/sec), 1451.8 ms avg latency, 1824.0 ms max latency.
86385 records sent, 17277.0 records/sec (16.87 MB/sec), 1506.9 ms avg latency, 2586.0 ms max latency.
94785 records sent, 18754.5 records/sec (18.31 MB/sec), 1872.2 ms avg latency, 3482.0 ms max latency.
124005 records sent, 24796.0 records/sec (24.21 MB/sec), 1239.6 ms avg latency, 1360.0 ms max latency.
118995 records sent, 23799.0 records/sec (23.24 MB/sec), 1275.7 ms avg latency, 1388.0 ms max latency.
116325 records sent, 23251.0 records/sec (22.71 MB/sec), 1349.5 ms avg latency, 1703.0 ms max latency.
121260 records sent, 24247.2 records/sec (23.68 MB/sec), 1261.7 ms avg latency, 1337.0 ms max latency.
125700 records sent, 25140.0 records/sec (24.55 MB/sec), 1246.4 ms avg latency, 1366.0 ms max latency.
132405 records sent, 26470.4 records/sec (25.85 MB/sec), 1159.3 ms avg latency, 1243.0 ms max latency.
133935 records sent, 26787.0 records/sec (26.16 MB/sec), 1137.2 ms avg latency, 1249.0 ms max latency.
123255 records sent, 24641.1 records/sec (24.06 MB/sec), 1233.4 ms avg latency, 1413.0 ms max latency.
125160 records sent, 25032.0 records/sec (24.45 MB/sec), 1232.0 ms avg latency, 1335.0 ms max latency.
113835 records sent, 22767.0 records/sec (22.23 MB/sec), 1337.3 ms avg latency, 1607.0 ms max latency.
126825 records sent, 25365.0 records/sec (24.77 MB/sec), 1225.8 ms avg latency, 1452.0 ms max latency.
123450 records sent, 19045.0 records/sec (18.60 MB/sec), 1218.1 ms avg latency, 2731.0 ms max latency.
109080 records sent, 21816.0 records/sec (21.30 MB/sec), 1840.8 ms avg latency, 3146.0 ms max latency.
120930 records sent, 24181.2 records/sec (23.61 MB/sec), 1265.0 ms avg latency, 1420.0 ms max latency.
114345 records sent, 22869.0 records/sec (22.33 MB/sec), 1357.0 ms avg latency, 1836.0 ms max latency.
112035 records sent, 22398.0 records/sec (21.87 MB/sec), 1237.7 ms avg latency, 1832.0 ms max latency.
119355 records sent, 23866.2 records/sec (23.31 MB/sec), 1406.4 ms avg latency, 1898.0 ms max latency.
124761 records sent, 24952.2 records/sec (24.37 MB/sec), 1200.6 ms avg latency, 1370.0 ms max latency.
126729 records sent, 25345.8 records/sec (24.75 MB/sec), 1251.2 ms avg latency, 1457.0 ms max latency.
126795 records sent, 25359.0 records/sec (24.76 MB/sec), 1207.9 ms avg latency, 1415.0 ms max latency.
125205 records sent, 24956.1 records/sec (24.37 MB/sec), 1200.3 ms avg latency, 1383.0 ms max latency.
117120 records sent, 23424.0 records/sec (22.88 MB/sec), 1323.5 ms avg latency, 1574.0 ms max latency.
86430 records sent, 17286.0 records/sec (16.88 MB/sec), 1795.1 ms avg latency, 2974.0 ms max latency.
104925 records sent, 20976.6 records/sec (20.48 MB/sec), 1427.8 ms avg latency, 1717.0 ms max latency.
120510 records sent, 23255.5 records/sec (22.71 MB/sec), 1273.5 ms avg latency, 1566.0 ms max latency.
117705 records sent, 23536.3 records/sec (22.98 MB/sec), 1361.8 ms avg latency, 1600.0 ms max latency.
122490 records sent, 24498.0 records/sec (23.92 MB/sec), 1203.2 ms avg latency, 1493.0 ms max latency.
128550 records sent, 25710.0 records/sec (25.11 MB/sec), 1269.7 ms avg latency, 1599.0 ms max latency.
125415 records sent, 25057.9 records/sec (24.47 MB/sec), 1215.9 ms avg latency, 1471.0 ms max latency.
117120 records sent, 23386.6 records/sec (22.84 MB/sec), 1235.4 ms avg latency, 1543.0 ms max latency.
126045 records sent, 25209.0 records/sec (24.62 MB/sec), 1295.3 ms avg latency, 1708.0 ms max latency.
124650 records sent, 24930.0 records/sec (24.35 MB/sec), 1233.4 ms avg latency, 1404.0 ms max latency.
127935 records sent, 25556.3 records/sec (24.96 MB/sec), 1174.9 ms avg latency, 1299.0 ms max latency.
114435 records sent, 22887.0 records/sec (22.35 MB/sec), 1363.9 ms avg latency, 1577.0 ms max latency.
5000000 records sent, 21335.336010 records/sec (20.84 MB/sec), 1418.58 ms avg latency, 6319.00 ms max latency, 1255 ms 50th, 2463 ms 95th, 5218 ms 99th, 6047 ms 99.9th.
[root@cn-tx-bj1-r8 kafka_2.13-3.2.0]# free -h
              total        used        free      shared  buff/cache   available
Mem:          1.8Gi       1.1Gi       239Mi        97Mi       492Mi       470Mi
Swap:            0B          0B          0B
```
`cn-tx-bj6-u0`多了一个核心变成了双核，测试时还是跑爆两个`CPU`，`65`左右的吞吐量看起来还行，压测脚本的生产能力并没有受到限制
``` bash
ubuntu@cn-tx-bj6-u0:~/kafka_2.13-3.2.0$ free -h
              total        used        free      shared  buff/cache   available
Mem:          3.3Gi       972Mi       2.1Gi       2.0Mi       316Mi       2.2Gi
Swap:            0B          0B          0B
ubuntu@cn-tx-bj6-u0:~/kafka_2.13-3.2.0$ bin/kafka-producer-perf-test.sh --topic test --num-records 5000000 --record-size 1024 --throughput -1 --producer.config config/producer.properties
85597 records sent, 17109.1 records/sec (16.71 MB/sec), 1071.9 ms avg latency, 1406.0 ms max latency.
160875 records sent, 32168.6 records/sec (31.41 MB/sec), 976.6 ms avg latency, 1318.0 ms max latency.
189705 records sent, 37918.2 records/sec (37.03 MB/sec), 827.8 ms avg latency, 1189.0 ms max latency.
300030 records sent, 60006.0 records/sec (58.60 MB/sec), 120.3 ms avg latency, 435.0 ms max latency.
329497 records sent, 65899.4 records/sec (64.35 MB/sec), 16.5 ms avg latency, 185.0 ms max latency.
389491 records sent, 77898.2 records/sec (76.07 MB/sec), 20.1 ms avg latency, 139.0 ms max latency.
418597 records sent, 83719.4 records/sec (81.76 MB/sec), 71.5 ms avg latency, 431.0 ms max latency.
392701 records sent, 78540.2 records/sec (76.70 MB/sec), 51.2 ms avg latency, 261.0 ms max latency.
429040 records sent, 85808.0 records/sec (83.80 MB/sec), 37.3 ms avg latency, 123.0 ms max latency.
354655 records sent, 70902.6 records/sec (69.24 MB/sec), 21.5 ms avg latency, 96.0 ms max latency.
390479 records sent, 78095.8 records/sec (76.27 MB/sec), 27.2 ms avg latency, 132.0 ms max latency.
417045 records sent, 83409.0 records/sec (81.45 MB/sec), 24.1 ms avg latency, 140.0 ms max latency.
325728 records sent, 65145.6 records/sec (63.62 MB/sec), 13.8 ms avg latency, 125.0 ms max latency.
415732 records sent, 83096.5 records/sec (81.15 MB/sec), 17.3 ms avg latency, 130.0 ms max latency.
397019 records sent, 79340.3 records/sec (77.48 MB/sec), 46.9 ms avg latency, 282.0 ms max latency.
5000000 records sent, 66320.913637 records/sec (64.77 MB/sec), 116.04 ms avg latency, 1406.00 ms max latency, 13 ms 50th, 856 ms 95th, 1198 ms 99th, 1379 ms 99.9th.
ubuntu@cn-tx-bj6-u0:~/kafka_2.13-3.2.0$ free -h
              total        used        free      shared  buff/cache   available
Mem:          3.3Gi       1.4Gi       396Mi       2.0Mi       1.6Gi       1.7Gi
Swap:            0B          0B          0B
```
`cn-py-dl-r8`快进到八核这下性能不成问题了，压测脚本的生产能力更不会受到限制了，不过仍然是`60`左右的吞吐量，不得不怀疑这就是单个压测脚本所能打到的上限了
```
[root@cn-py-dl-r8 kafka_2.13-3.2.0]# free -h
              total        used        free      shared  buff/cache   available
Mem:           15Gi       2.7Gi       4.0Gi       174Mi       8.7Gi        12Gi
Swap:            0B          0B          0B
[root@cn-py-dl-r8 kafka_2.13-3.2.0]# bin/kafka-producer-perf-test.sh --topic test --num-records 5000000 --record-size 1024 --throughput -1 --producer.config config/producer.properties
106876 records sent, 21375.2 records/sec (20.87 MB/sec), 1049.6 ms avg latency, 1697.0 ms max latency.
284445 records sent, 56889.0 records/sec (55.56 MB/sec), 469.6 ms avg latency, 999.0 ms max latency.
331323 records sent, 66264.6 records/sec (64.71 MB/sec), 22.6 ms avg latency, 213.0 ms max latency.
331586 records sent, 66317.2 records/sec (64.76 MB/sec), 2.0 ms avg latency, 30.0 ms max latency.
321614 records sent, 64322.8 records/sec (62.82 MB/sec), 4.1 ms avg latency, 45.0 ms max latency.
333204 records sent, 66640.8 records/sec (65.08 MB/sec), 2.0 ms avg latency, 29.0 ms max latency.
336222 records sent, 67244.4 records/sec (65.67 MB/sec), 1.1 ms avg latency, 17.0 ms max latency.
332382 records sent, 66476.4 records/sec (64.92 MB/sec), 1.4 ms avg latency, 22.0 ms max latency.
321589 records sent, 64317.8 records/sec (62.81 MB/sec), 5.0 ms avg latency, 69.0 ms max latency.
329435 records sent, 65887.0 records/sec (64.34 MB/sec), 2.1 ms avg latency, 29.0 ms max latency.
75963 records sent, 12877.3 records/sec (12.58 MB/sec), 9.7 ms avg latency, 4702.0 ms max latency.
344710 records sent, 68831.9 records/sec (67.22 MB/sec), 468.7 ms avg latency, 4711.0 ms max latency.
329002 records sent, 65800.4 records/sec (64.26 MB/sec), 2.8 ms avg latency, 29.0 ms max latency.
334619 records sent, 66923.8 records/sec (65.36 MB/sec), 2.0 ms avg latency, 26.0 ms max latency.
331480 records sent, 66296.0 records/sec (64.74 MB/sec), 4.1 ms avg latency, 48.0 ms max latency.
336836 records sent, 67367.2 records/sec (65.79 MB/sec), 2.3 ms avg latency, 32.0 ms max latency.
5000000 records sent, 59406.411140 records/sec (58.01 MB/sec), 85.10 ms avg latency, 4711.00 ms max latency, 1 ms 50th, 483 ms 95th, 1490 ms 99th, 4682 ms 99.9th.
[root@cn-py-dl-r8 kafka_2.13-3.2.0]# free -h
              total        used        free      shared  buff/cache   available
Mem:           15Gi       5.1Gi       2.5Gi       174Mi       7.8Gi       9.8Gi
Swap:            0B          0B          0B
```

### 4.结论
1. 个人观点，在吞吐量小于`50~60`的情况下[#108434169651624713](https://mastodon.yuangezhizao.cn/@yuangezhizao/108434169651624713)，可以使用`kafka-producer-perf-test.sh`来测试吞吐量，因为看起来还没到单个脚本所能打到的上限
比如这篇文章[How to optimize your Kafka producer for throughput](https://web.archive.org/web/20220609091801/https://developer.confluent.io/tutorials/optimize-producer-throughput/confluent.html)，通过修改`batch.size`、`linger.ms`、`compression.type=lz4`和`acks=1`
把吞吐量从`1.03 MB/sec`提高到了`5.65 MB/sec`，是可以使用这个脚本来验证的
2. 但是如果被压测的机器性能更好（指大于`50`）[#108431369549507049](https://mastodon.yuangezhizao.cn/@yuangezhizao/108431369549507049)，那么只运行这一个脚本显然是不够的，需要同时运行多个脚本才能打到较高的数值（亦或是多进程搞起来
3. 查看这个脚本的源码，发现实际调用的是`org.apache.kafka.tools.ProducerPerformance`这个类
``` bash
if [ "x$KAFKA_HEAP_OPTS" = "x" ]; then
    export KAFKA_HEAP_OPTS="-Xmx512M"
fi
exec $(dirname $0)/kafka-run-class.sh org.apache.kafka.tools.ProducerPerformance "$@"
```
再查看[ProducerPerformance.java](https://github.com/apache/kafka/blob/3.2/tools/src/main/java/org/apache/kafka/tools/ProducerPerformance.java)源码，节选其关键部分如下
里面只定义了一个`KafkaProducer<byte[], byte[]> producer = createKafkaProducer(props);`
当没达到总数`numRecords`时，随机生成每一条记录`payload = generateRandomPayload(recordSize, payloadByteList, payload, random);`，然后调用`producer.send(record, cb);`
``` bash
KafkaProducer<byte[], byte[]> producer = createKafkaProducer(props);

/* setup perf test */

for (long i = 0; i < numRecords; i++) {

    payload = generateRandomPayload(recordSize, payloadByteList, payload, random);

    record = new ProducerRecord<>(topicName, payload);

    Callback cb = stats.nextCompletion(sendStartMs, payload.length, stats);
    producer.send(record, cb);
}

if (!shouldPrintMetrics) {
    producer.close();

    /* print final results */
    stats.printTotal();
} else {
    // Make sure all messages are sent before printing out the stats and the metrics
    // We need to do this in a different branch for now since tests/kafkatest/sanity_checks/test_performance_services.py
    // expects this class to work with older versions of the client jar that don't support flush().
    producer.flush();

    /* print final results */
    stats.printTotal();

    /* print out metrics */
    ToolsUtils.printMetrics(producer.metrics());
    producer.close();
}
```
测试时也确实看到只有一个核心是打满的状态，这个脚本是单进程的
4. 那么问题只剩下[#108439423671562473](https://mastodon.yuangezhizao.cn/@yuangezhizao/108439423671562473)，为什么别人只用这一个脚本就能得到数百的吞吐量？难道是单个`CPU`足够强劲？
5. 最后，因运行多个脚本还得将所有的结果加和，也没找到能一次性获取所有生产者吞吐量总和的地方，被迫决定不再使用这个脚本进行测试了……

未完待续……