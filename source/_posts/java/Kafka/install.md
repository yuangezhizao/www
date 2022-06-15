---
title: Apache Kafka 单机版安装（RHEL 8 / Ubuntu 20.04）
date: 2022-06-09 13:50:01
tags:
  - RHEL
  - Ubuntu
  - Kafka
count: 2
os: 1
os_1: Monterry 12.4 (21F79)
browser: 0
browser_1: 102.0.5005.61 Stable
place: 新家
key: 143
---
    没想到最后把手里内存足够的机子都装了个遍.jpG
<!-- more -->
## 0x00.前言
为了之后的性能测试，不得不在各个平台上都装一份，以便进行横向对比

## 0x01.安装`Java`
`Kafka`的运行依赖于`Java`虚拟机，后者可以直接从各大包管理工具安装，非常方便，并不需要手动下载，再解压配置环境变量之类的……
### 1.基于`RHEL 8`系统
自`Kafka 3.0.0`版本起，`The deprecation of support for Java 8 and Scala 2.12`，于是选择安装`openjdk 11`
``` bash
[root@cn-py-dl-r8 ~]# dnf install java-11-openjdk -y
[root@cn-py-dl-r8 ~]# java -version
openjdk version "11.0.15" 2022-04-19 LTS
OpenJDK Runtime Environment 18.9 (build 11.0.15+10-LTS)
OpenJDK 64-Bit Server VM 18.9 (build 11.0.15+10-LTS, mixed mode, sharing)
```
### 2.基于`Ubuntu 20.04`系统
这里只列出命令，就不再赘述了
``` bash
ubuntu@cn-tx-bj6-u0:~$ sudo apt install openjdk-11-jdk
ubuntu@cn-tx-bj6-u0:~$ java -version
openjdk version "11.0.15" 2022-04-19
OpenJDK Runtime Environment (build 11.0.15+10-Ubuntu-0ubuntu0.20.04.1)
OpenJDK 64-Bit Server VM (build 11.0.15+10-Ubuntu-0ubuntu0.20.04.1, mixed mode, sharing)
```

## 0x02.安装[Kafka](https://kafka.apache.org/downloads)
截至目前，最新版本是`3.2.0`，然后`Scala`有`2.12`和`2.13`的，这里选择官方推荐的后者，即`kafka_2.13-3.2.0.tgz`
### 1.基于`RHEL 8`系统
和安装`Java`不同，需要手动下载预编译包，再解压并创建单元文件
``` bash
[root@cn-py-dl-r8 ~]# wget https://dlcdn.apache.org/kafka/3.2.0/kafka_2.13-3.2.0.tgz
[root@cn-py-dl-r8 ~]# tar -zxvf kafka_2.13-3.2.0.tgz
```
创建`Kafka`和`Zookeeper`的自定义数据目录，虽然本文并未实际使用到这些目录
``` bash
[root@cn-py-dl-r8 ~]# mkdir kafka
[root@cn-py-dl-r8 ~]# cd kafka
[root@cn-py-dl-r8 kafka]# mkdir kafka-logs
[root@cn-py-dl-r8 kafka]# mkdir -p zookeeper/data
[root@cn-py-dl-r8 kafka]# echo 0 > zookeeper/data/myid
[root@cn-py-dl-r8 kafka]# mkdir -p zookeeper/logs
[root@cn-py-dl-r8 kafka]# tree
.
├── kafka-logs
└── zookeeper
    ├── data
    │   └── myid
    └── logs

4 directories, 1 file
```
创建`Zookeeper`的单元文件，虽然官方计划后续去掉`Zookeeper`，但现在还是得用到它
``` bash
[root@cn-py-dl-r8 ~]# cat /usr/lib/systemd/system/zookeeper.service
[Unit]
Description=Zookeeper service
After=network.target

[Service]
Type=simple
User=root
Group=root
ExecStart=/bin/bash /root/kafka_2.13-3.2.0/bin/zookeeper-server-start.sh /root/kafka_2.13-3.2.0/config/zookeeper.properties
ExecStop=/bin/bash /root/kafka_2.13-3.2.0/bin/zookeeper-server-stop.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
创建`Kafka`的单元文件，在环境变量中设定了`JMX_PORT=9988`，并增大`LimitNOFILE=65535`
> `LimitNOFILE=65535`的原因见：[记一次 Kafka 未增大文件描述符限制的翻车经历](./server-logs.html)

``` bash
[root@cn-py-dl-r8 ~]# cat /usr/lib/systemd/system/kafka.service
[Unit]
Description=Apache Kafka server (broker)
After=network.target zookeeper.service

[Service]
Type=simple
User=root
Group=root
Environment=JMX_PORT=9988
ExecStart=/bin/bash /root/kafka_2.13-3.2.0/bin/kafka-server-start.sh /root/kafka_2.13-3.2.0/config/server.properties
ExecStop=/bin/bash /root/kafka_2.13-3.2.0/bin/kafka-server-stop.sh
Restart=on-failure
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
```
### 2.基于`Ubuntu 20.04`系统

<details><summary>点击此处 ← 查看折叠</summary>

``` bash
ubuntu@cn-tx-bj6-u0:~$ wget https://dlcdn.apache.org/kafka/3.2.0/kafka_2.13-3.2.0.tgz
ubuntu@cn-tx-bj6-u0:~$ tar -zxvf kafka_2.13-3.2.0.tgz
ubuntu@cn-tx-bj6-u0:~$ mkdir kafka
ubuntu@cn-tx-bj6-u0:~$ cd kafka
ubuntu@cn-tx-bj6-u0:~/kafka$ mkdir kafka-logs
ubuntu@cn-tx-bj6-u0:~/kafka$ mkdir -p zookeeper/data
ubuntu@cn-tx-bj6-u0:~/kafka$ echo 0 > zookeeper/data/myid
ubuntu@cn-tx-bj6-u0:~/kafka$ mkdir -p zookeeper/logs
ubuntu@cn-tx-bj6-u0:~$ sudo vim /etc/systemd/system/zookeeper.service
ubuntu@cn-tx-bj6-u0:~$ cat /etc/systemd/system/zookeeper.service
[Unit]
Description=Zookeeper service
After=network.target

[Service]
Type=simple
User=root
Group=root
ExecStart=/bin/bash /home/ubuntu/kafka_2.13-3.2.0/bin/zookeeper-server-start.sh /home/ubuntu/kafka_2.13-3.2.0/config/zookeeper.properties
ExecStop=/bin/bash /home/ubuntu/kafka_2.13-3.2.0/bin/zookeeper-server-stop.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
ubuntu@cn-tx-bj6-u0:~$ sudo vim /usr/lib/systemd/system/kafka.service
ubuntu@cn-tx-bj6-u0:~$ cat /usr/lib/systemd/system/kafka.service
[Unit]
Description=Apache Kafka server (broker)
After=network.target zookeeper.service

[Service]
Type=simple
User=root
Group=root
Environment=JMX_PORT=9988
ExecStart=/bin/bash /home/ubuntu/kafka_2.13-3.2.0/bin/kafka-server-start.sh /home/ubuntu/kafka_2.13-3.2.0/config/server.properties
ExecStop=/bin/bash /home/ubuntu/kafka_2.13-3.2.0/bin/kafka-server-stop.sh
Restart=on-failure
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
```

</details>

## 0x03.安装[CMAK](https://github.com/yahoo/CMAK)
`CMAK`是一款雅虎开源的非常好用的`Kafka`图形化管理工具，用完之后再也不想用命令行了`.jpG`，需`Java 11`
> CMAK (Cluster Manager for Apache Kafka, previously known as Kafka Manager)

### 1.基于`RHEL 8`系统
下载最新版本预编译包`cmak-3.0.0.6.zip`，修改配置文件`conf/application.conf`中的`kafka-manager.zkhosts`和`cmak.zkhosts`的值为`localhost:2181`
``` bash
[root@cn-py-dl-r8 ~]# wget https://github.com/yahoo/CMAK/releases/download/3.0.0.6/cmak-3.0.0.6.zip
[root@cn-py-dl-r8 ~]# dnf install unzip -y
[root@cn-py-dl-r8 ~]# unzip cmak-3.0.0.6.zip
[root@cn-py-dl-r8 ~]# cd cmak-3.0.0.6/
[root@cn-py-dl-r8 cmak-3.0.0.6]# vim conf/application.conf
[root@cn-py-dl-r8 cmak-3.0.0.6]# cat conf/application.conf
……
# Settings prefixed with 'kafka-manager.' will be deprecated, use 'cmak.' instead.
# https://github.com/yahoo/CMAK/issues/713
kafka-manager.zkhosts="localhost:2181"
kafka-manager.zkhosts=${?ZK_HOSTS}
cmak.zkhosts="localhost:2181"
cmak.zkhosts=${?ZK_HOSTS}
……
```
创建`CMAK`的单元文件，如果是手动解压的`Java`，需要在`ExecStart`中添加参数`-java-home /root/jdk-11.0.15`
``` bash
[root@cn-py-dl-r8 ~]# cat /usr/lib/systemd/system/kafka-manager.service
[Unit]
Description=kafka-manager server service
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/root/cmak-3.0.0.6
ExecStart=/root/cmak-3.0.0.6/bin/cmak -Dconfig.file=/root/cmak-3.0.0.6/conf/application.conf
Restart=on-failure
RestartSec=60

[Install]
WantedBy=multi-user.target
```
### 2.基于`Ubuntu 20.04`系统

<details><summary>点击此处 ← 查看折叠</summary>

``` bash
ubuntu@cn-tx-bj6-u0:~$ wget https://github.com/yahoo/CMAK/releases/download/3.0.0.6/cmak-3.0.0.6.zip
ubuntu@cn-tx-bj6-u0:~$ unzip cmak-3.0.0.6.zip
ubuntu@cn-tx-bj6-u0:~$ cd cmak-3.0.0.6/
ubuntu@cn-tx-bj6-u0:~/cmak-3.0.0.6$ vim conf/application.conf 
ubuntu@cn-tx-bj6-u0:~/cmak-3.0.0.6$ cat conf/application.conf 
……
# Settings prefixed with 'kafka-manager.' will be deprecated, use 'cmak.' instead.
# https://github.com/yahoo/CMAK/issues/713
kafka-manager.zkhosts="localhost:2181"
kafka-manager.zkhosts=${?ZK_HOSTS}
cmak.zkhosts="localhost:2181"
cmak.zkhosts=${?ZK_HOSTS}
……
ubuntu@cn-tx-bj6-u0:~$ sudo vim /usr/lib/systemd/system/kafka-manager.service
ubuntu@cn-tx-bj6-u0:~$ cat /usr/lib/systemd/system/kafka-manager.service
[Unit]
Description=kafka-manager server service
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/home/ubuntu/cmak-3.0.0.6
ExecStart=/home/ubuntu/cmak-3.0.0.6/bin/cmak -Dconfig.file=/home/ubuntu/cmak-3.0.0.6/conf/application.conf
Restart=on-failure
RestartSec=60

[Install]
WantedBy=multi-user.target
```

</details>

## 0x04.启动服务
因`Kafka`依赖于`Zookeeper`，所以需要先启动`Zookeeper`再启动`Kafka`
``` bash
[root@cn-py-dl-r8 ~]# systemctl start zookeeper
[root@cn-py-dl-r8 ~]# systemctl start kafka
[root@cn-py-dl-r8 ~]# systemctl start kafka-manager
```

## 0x05.后记
是不是很简单？自己装了四台之后，对于`Kafka`的安装愈发熟练草……

## 0x06.引用
[Kafka的安装与使用](https://web.archive.org/web/20220615030554/https://www.taliove.com/kafka/)
[Kafka集群优化篇-调整broker的堆内存(heap)案例实操](https://web.archive.org/web/20220615030621/https://www.cnblogs.com/yinzhengjie/p/9884552.html)