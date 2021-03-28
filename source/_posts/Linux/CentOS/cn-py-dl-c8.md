---
title: CentOS 8 安装 Elasticsearch + Kibana + Metricbeat 全程开启 SSL 并配置 APM Server
date: 2021-03-21 14:35:55
tags:
  - CentOS
count: 1
os: 1
os_1: Big Sur 11.2.3 (20D91)
browser: 1
browser_1: 89.0.4389.90 Stable
place: 新家
key: 112
---
    原拟定标题：《PY 云新增 CentOS 8 64 位》
<!-- more -->
## 0x00.前言
本来是装在`cn-py-dl-w9d`上的服务，后来工作时发现装在`linux`上升级异常方便只需`yum update`就可以了
而`windows`上还得手动去官网下载新版的`msi`安装包并进行`GUI`安装

## 0x01.安装[Elasticsearch](https://www.elastic.co/cn/elasticsearch/)
从[Download Elasticsearch](https://www.elastic.co/cn/downloads/elasticsearch)可以看到目前是`7.12.0`版本，在这里使用[Package Managers](https://www.elastic.co/guide/en/elasticsearch/reference/7.12/rpm.html#rpm-repo)的安装方法
1. 首先，在`/etc/yum.repos.d/`路径下创建`elasticsearch.repo`
``` bash
[root@cn-py-dl-c8 ~]# cd /etc/yum.repos.d/
[root@cn-py-dl-c8 yum.repos.d]# vim elasticsearch.repo
[root@cn-py-dl-c8 yum.repos.d]# cat elasticsearch.repo 
[elasticsearch]
name=Elasticsearch repository for 7.x packages
baseurl=https://artifacts.elastic.co/packages/7.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=0
autorefresh=1
type=rpm-md
```
2. 当然源太慢无法忍受的话，可以设置`yum`的代理
``` bash
[root@cn-py-dl-c8 ~]# vim /etc/yum.conf
yum.conf     yum.repos.d/ 
[root@cn-py-dl-c8 ~]# cat /etc/yum.conf 
[main]
gpgcheck=1
installonly_limit=3
clean_requirements_on_remove=True
best=True
skip_if_unavailable=False
proxy=http://192.168.25.248:1081
```
3. 最后，安装
`yum install --enablerepo=elasticsearch elasticsearch -y`

## 0x02.配置[Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/7.12/settings.html)
``` bash
[root@cn-py-dl-c8 ~]# cd /etc/elasticsearch/
[root@cn-py-dl-c8 elasticsearch]# ll
total 40
-rw-rw----. 1 root elasticsearch   199 Mar 28 12:02 elasticsearch.keystore
-rw-rw----. 1 root elasticsearch  2755 Mar 18 14:26 elasticsearch.yml
-rw-rw----. 1 root elasticsearch  3182 Mar 18 14:26 jvm.options
drwxr-s---. 2 root elasticsearch     6 Mar 18 14:30 jvm.options.d
-rw-rw----. 1 root elasticsearch 18612 Mar 18 14:26 log4j2.properties
-rw-rw----. 1 root elasticsearch   473 Mar 18 14:26 role_mapping.yml
-rw-rw----. 1 root elasticsearch   197 Mar 18 14:26 roles.yml
-rw-rw----. 1 root elasticsearch     0 Mar 18 14:26 users
-rw-rw----. 1 root elasticsearch     0 Mar 18 14:26 users_roles
```
①[关闭内存交换文件](https://www.elastic.co/guide/en/elasticsearch/reference/master/setup-configuration-memory.html#disable-swap-files)
临时：`swapoff -a`
永久：`vim /etc/fstab`注释`swap`一行，重启
②修改`elasticsearch.yml`
``` bash
# ---------------------------------- Cluster -----------------------------------
# Use a descriptive name for your cluster:
cluster.name: elasticsearch
# ------------------------------------ Node ------------------------------------
# Use a descriptive name for the node:
node.name: cn-py-dl-c8
# ----------------------------------- Memory -----------------------------------
# Lock the memory on startup:
#bootstrap.memory_lock: true
# Make sure that the heap size is set to about half the memory available
# on the system and that the owner of the process is allowed to use this
# limit.
# Elasticsearch performs poorly when the system is swapping the memory.
# ---------------------------------- Network -----------------------------------
# By default Elasticsearch is only accessible on localhost. Set a different
# address here to expose this node on the network:
network.host: 0.0.0.0
# --------------------------------- Discovery ----------------------------------
# Bootstrap the cluster using an initial set of master-eligible nodes:
cluster.initial_master_nodes: ["cn-py-dl-c8"]
# For more information, consult the discovery and cluster formation module documentation.
xpack.license.self_generated.type: basic
xpack.security.enabled: true
xpack.security.http.ssl.enabled: true
xpack.security.http.ssl.keystore.path: /etc/elasticsearch/ssl/home.yuangezhizao.cn.jks
xpack.security.http.ssl.keystore.password: <rm>
xpack.security.transport.ssl.enabled: true
xpack.security.authc.api_key.enabled: true
```
③启动
`systemctl start elasticsearch`
④配置密码
``` bash
[root@cn-py-dl-c8 elasticsearch]# cd /usr/share/elasticsearch/bin/
[root@cn-py-dl-c8 bin]# ll
total 21116
-rwxr-xr-x. 1 root root     2896 Mar 18 14:30 elasticsearch
-rwxr-xr-x. 1 root root      501 Mar 18 14:19 elasticsearch-certgen
-rwxr-xr-x. 1 root root      493 Mar 18 14:19 elasticsearch-certutil
-rwxr-xr-x. 1 root root      996 Mar 18 14:30 elasticsearch-cli
-rwxr-xr-x. 1 root root      443 Mar 18 14:19 elasticsearch-croneval
-rwxr-xr-x. 1 root root     4825 Mar 18 14:30 elasticsearch-env
-rwxr-xr-x. 1 root root     1828 Mar 18 14:30 elasticsearch-env-from-file
-rwxr-xr-x. 1 root root      184 Mar 18 14:30 elasticsearch-keystore
-rwxr-xr-x. 1 root root      450 Mar 18 14:19 elasticsearch-migrate
-rwxr-xr-x. 1 root root      126 Mar 18 14:30 elasticsearch-node
-rwxr-xr-x. 1 root root      172 Mar 18 14:30 elasticsearch-plugin
-rwxr-xr-x. 1 root root      441 Mar 18 14:19 elasticsearch-saml-metadata
-rwxr-xr-x. 1 root root      448 Mar 18 14:19 elasticsearch-setup-passwords
-rwxr-xr-x. 1 root root      118 Mar 18 14:30 elasticsearch-shard
-rwxr-xr-x. 1 root root      483 Mar 18 14:19 elasticsearch-sql-cli
-rwxr-xr-x. 1 root root 21529276 Mar 18 14:19 elasticsearch-sql-cli-7.12.0.jar
-rwxr-xr-x. 1 root root      436 Mar 18 14:19 elasticsearch-syskeygen
-rwxr-xr-x. 1 root root      436 Mar 18 14:19 elasticsearch-users
-rwxr-xr-x. 1 root root      332 Mar 18 14:26 systemd-entrypoint
-rwxr-xr-x. 1 root root      356 Mar 18 14:19 x-pack-env
-rwxr-xr-x. 1 root root      364 Mar 18 14:19 x-pack-security-env
-rwxr-xr-x. 1 root root      363 Mar 18 14:19 x-pack-watcher-env
[root@cn-py-dl-c8 bin]# ./elasticsearch-setup-passwords interactive
Initiating the setup of passwords for reserved users elastic,apm_system,kibana,kibana_system,logstash_system,beats_system,remote_monitoring_user.
You will be prompted to enter passwords as the process progresses.
Please confirm that you would like to continue [y/N]y
Enter password for [elastic]: 
Reenter password for [elastic]: 
Enter password for [apm_system]: 
Reenter password for [apm_system]: 
Enter password for [kibana_system]: 
Reenter password for [kibana_system]: 
Enter password for [logstash_system]: 
Reenter password for [logstash_system]: 
Enter password for [beats_system]: 
Reenter password for [beats_system]: 
Enter password for [remote_monitoring_user]: 
Reenter password for [remote_monitoring_user]: 
Changed password for user [apm_system]
Changed password for user [kibana_system]
Changed password for user [kibana]
Changed password for user [logstash_system]
Changed password for user [beats_system]
Changed password for user [remote_monitoring_user]
Changed password for user [elastic]
```
⑤防火墙允许服务
```
[root@cn-py-dl-c8 elasticsearch]# firewall-cmd --state
running
[root@cn-py-dl-c8 elasticsearch]# firewall-cmd --permanent --add-service=elasticsearch
success
[root@cn-py-dl-c8 elasticsearch]# systemctl restart firewalld
[root@cn-py-dl-c8 elasticsearch]# firewall-cmd --list-services
cockpit dhcpv6-client elasticsearch ssh
```
![访问](https://i1.yuangezhizao.cn/macOS/QQ20210328-152301@2x.png!webp)

## 0x03.安装[Kibana](https://www.elastic.co/cn/kibana/)
从[Download Kibana](https://www.elastic.co/cn/downloads/kibana)可以看到目前是`7.12.0`版本，在这里同样使用[Package Managers](https://www.elastic.co/guide/en/kibana/7.12/rpm.html#rpm-repo)的安装方法
1. 首先，在`/etc/yum.repos.d/`路径下创建`kibana.repo`
``` bash
[root@cn-py-dl-c8 ~]# cd /etc/yum.repos.d/
[root@cn-py-dl-c8 yum.repos.d]# vim kibana.repo
[root@cn-py-dl-c8 yum.repos.d]# cat kibana.repo
[kibana-7.x]
name=Kibana repository for 7.x packages
baseurl=https://artifacts.elastic.co/packages/7.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
```
2. 然后，安装
`yum install kibana -y`

## 0x04.配置[Kibana](https://www.elastic.co/guide/en/kibana/7.12/settings.html)
①绑定`hosts`
``` bash
[root@cn-py-dl-c8 kibana]# vim /etc/hosts
[root@cn-py-dl-c8 kibana]# cat /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
0.0.0.0 home.yuangezhizao.cn
```
②修改`kibana.yml`
``` bash
[root@cn-py-dl-c8 ~]# cd /etc/kibana
[root@cn-py-dl-c8 kibana]# ll
total 16
-rw-rw----. 1 root kibana  130 Mar 28 12:08 kibana.keystore
-rw-rw----. 1 root kibana 5065 Mar 18 13:55 kibana.yml
-rw-r--r--. 1 root kibana  216 Mar 18 13:55 node.options

# Specifies the address to which the Kibana server will bind. IP addresses and host names are both valid values.
# The default is 'localhost', which usually means remote machines will not be able to connect.
# To allow connections from remote users, set this parameter to a non-loopback address.
server.host: "0.0.0.0"
# The Kibana server's name.  This is used for display purposes.
server.name: "cn-py-dl-c8"
# The URLs of the Elasticsearch instances to use for all your queries.
elasticsearch.hosts: ["https://home.yuangezhizao.cn:9200"]
# If your Elasticsearch is protected with basic authentication, these settings provide
# the username and password that the Kibana server uses to perform maintenance on the Kibana
# index at startup. Your Kibana users still need to authenticate with Elasticsearch, which
# is proxied through the Kibana server.
elasticsearch.username: "kibana_system"
elasticsearch.password: "<rm>"
# Enables SSL and paths to the PEM-format SSL certificate and SSL key files, respectively.
# These settings enable SSL for outgoing requests from the Kibana server to the browser.
server.ssl.enabled: true
server.ssl.certificate: /etc/kibana/ssl/1_home.yuangezhizao.cn_bundle.crt
server.ssl.key: /etc/kibana/ssl/2_home.yuangezhizao.cn.key
# Specifies locale to be used for all localizable strings, dates and number formats.
# Supported languages are the following: English - en , by default , Chinese - zh-CN .
i18n.locale: "zh-CN"
xpack.security.enabled: true
xpack.encryptedSavedObjects.encryptionKey: "something_at_least_32_characters"
xpack.ingestManager.fleet.tlsCheckDisabled: true
```
③启动
`systemctl start kibana`
④防火墙允许服务
``` bash
[root@cn-py-dl-c8 kibana]# firewall-cmd --permanent --add-service=kibana
success
[root@cn-py-dl-c8 kibana]# systemctl restart firewalld
```
注：也可以禁用防火墙，一劳永逸
``` bash
[root@cn-py-dl-c8 ~]# systemctl stop firewalld
[root@cn-py-dl-c8 ~]# systemctl disable firewalld
Removed /etc/systemd/system/multi-user.target.wants/firewalld.service.
Removed /etc/systemd/system/dbus-org.fedoraproject.FirewallD1.service.
```

## 0x04.安装并配置[Metricbeat](https://www.elastic.co/guide/en/beats/metricbeat/7.12/setup-repositories.html)
①安装
`yum install metricbeat -y`
②配置
``` bash
[root@cn-py-dl-c8 ~]# cd /usr/share/metricbeat/bin/
[root@cn-py-dl-c8 bin]# ll
total 128176
-rwxr-xr-x. 1 root root 130191232 Mar 18 14:33 metricbeat
-rwxr-xr-x. 1 root root   1057147 Mar 18 13:59 metricbeat-god
[root@cn-py-dl-c8 bin]# metricbeat modules enable elasticsearch-xpack
Enabled elasticsearch-xpack
[root@cn-py-dl-c8 metricbeat]# cd /etc/metricbeat/
[root@cn-py-dl-c8 metricbeat]# ll
total 1008
-rw-r--r--. 1 root root 911043 Mar 18 14:28 fields.yml
-rw-r--r--. 1 root root  99363 Mar 18 14:28 metricbeat.reference.yml
-rw-------. 1 root root   6899 Mar 18 14:28 metricbeat.yml
drwxr-xr-x. 2 root root   4096 Mar 28 13:16 modules.d
[root@cn-py-dl-c8 metricbeat]# vim metricbeat.yml
# ================================= Dashboards =================================
# These settings control loading the sample dashboards to the Kibana index. Loading
# the dashboards is disabled by default and can be enabled either by setting the
# options here or by using the `setup` command.
setup.dashboards.enabled: true
配置 ES 和 Kibana 的密码
```
③启动
`systemctl start metricbeat`
![完成不能](https://i1.yuangezhizao.cn/macOS/QQ20210328-154523@2x.png!webp)

~~本来是可以直接用内部的监控，花费力气安装完这个之后，并不能完成~~
~~然而这时候`ES`里是有数据的，感觉是`Kibana`的`bug`，网页控制台看到好几个报错。。。~~

注：还需修改默认`ES`配置
``` bash
[root@cn-py-dl-c8 ~]# cd /etc/metricbeat/modules.d/
[root@cn-py-dl-c8 modules.d]# cat elasticsearch-xpack.yml 
# Module: elasticsearch
# Docs: https://www.elastic.co/guide/en/beats/metricbeat/7.x/metricbeat-module-elasticsearch.html
- module: elasticsearch
  xpack.enabled: true
  period: 10s
  hosts: ["https://home.yuangezhizao.cn:9200"]
  username: "beats_system"
  password: "<rm>"
```
![然后就终于好使了](https://i1.yuangezhizao.cn/macOS/QQ20210328-160048@2x.png!webp)

## 0x05.通过`Fleet(Beta)`配置`APM`
1. 客户端接入
![代理](https://i1.yuangezhizao.cn/macOS/QQ20210328-142454@2x.png!webp)

首先需要在被监控的客户端上安装[Elastic Agent (beta)](https://www.elastic.co/cn/downloads/elastic-agent)，选择`WINDOWS ZIP 64-BIT`，因为是要安装在`cn-tx-bj-w9d`机子上的
参照[文档](https://www.elastic.co/guide/en/fleet/current/fleet-quick-start.html)进行注册
``` cmd
E:\elastic-agent-7.12.0-windows-x86_64>.\elastic-agent.exe install -f --kibana-url=https://home.yuangezhizao.cn:5601 --enrollment-token=<rm>
The Elastic Agent is currently in BETA and should not be used in production

2021-03-28T14:52:51.865+0800    INFO    application/enroll_cmd.go:191   Successfully triggered restart on running Elastic Agent.
Successfully enrolled the Elastic Agent.
```
![注册代理](https://i1.yuangezhizao.cn/macOS/QQ20210328-145055@2x.png!webp)
![注册完成](https://i1.yuangezhizao.cn/macOS/QQ20210328-145353@2x.png!webp)
![代理详情](https://i1.yuangezhizao.cn/macOS/QQ20210328-145411@2x.png!webp)

2. 再来看`Fleet`
其实本来只是`APM`的升级版本。。。这次没有再单独去安装`APM`
![全集设置](https://i1.yuangezhizao.cn/macOS/QQ20210328-153312@2x.png!webp)
![APM Server](https://i1.yuangezhizao.cn/macOS/QQ20210328-144733@2x.png!webp)
![概览](https://i1.yuangezhizao.cn/macOS/QQ20210328-133738@2x.png!webp)
![设置](https://i1.yuangezhizao.cn/macOS/QQ20210328-133844@2x.png!webp)
![编辑](https://i1.yuangezhizao.cn/macOS/20210328153558.png!webp)

但是还是有`bug`，访问`kibana`会报错`401`，而实际上是通过代理的**注册令牌**来访问的，不应该报错。。。

不过`Fleet`确实是个好东西，也再不需要`winlogbeat`了
![主机](https://i1.yuangezhizao.cn/macOS/QQ20210328-164003@2x.png!webp)

未完待续……