---
title: 重装系统之 cn-tx-bj6-c8 换至 Docker 基础镜像
date: 2022-07-05 23:52:58
tags:
  - CentOS
  - server
count: 3
os: 1
os_1: Monterry 12.4 (21F79)
browser: 0
browser_1: 103.0.5060.114 Stable
place: 新家
key: 146
---
    沉迷 Docker 无法自拔（bushi
<!-- more -->
## 0x00.`TL;DR`
在你云的机子全部纳入`Portainer`管理，[#108932178544618246](https://mastodon.yuangezhizao.cn/web/@yuangezhizao/108932178544618246)
![cn-tx-bj6-c8](https://mastodon-1251901037.cos.ap-beijing.myqcloud.com/media_attachments/files/108/933/569/767/738/127/original/d371290ab3615604.png)

## 0x01.前言
在五月份的征文活动中嫖了一台轻量机，可以玩儿一年，手里现在不仅有`2`台云主机，也有`2`台轻量机辣
最开始装了个`Ubuntu`体验其~~独占~~的[Microk8s](https://microk8s.io/)，奈何不熟悉该操作系统，虽然配置了多种代理但疑似没有完全生效，想想国内网络最终还是放弃了，重装成`CentOS8.2-Docker20`了

<details><summary>点击此处 ← 查看折叠</summary>

![轻量应用服务器](https://i1.yuangezhizao.cn/macOS/20220705235958.png!webp)
![Docker基础镜像](https://i1.yuangezhizao.cn/macOS/20220706001531.png!webp)

</details>

`22`年了，全面拥抱`Docker`吧~

<details><summary>点击此处 ← 查看折叠</summary>

![19](https://i1.yuangezhizao.cn/macOS/20220706002503.png!webp)
![8](https://i1.yuangezhizao.cn/macOS/20220706002534.png!webp)

</details>

## 0x03.迁移`Docker`
至于迁移`Docker`有啥优点就不再描述了，这里列一下迁移`Docker`需要考虑的几个问题
- 网络模式（桥接、主机）
- 原则上需`7*24h`运行的应用，如`postgresql`

因为不同主机的配置不同，目前由自己来决定每个应用跑在哪个主机上，之后会更换`k8s`来统一管理

Hostname | CPU | RAM | System Disk | Data Disk | Network | OS | 到期时间
:---: | :---: | :---: | :---: | :---: | :---: | :---: | :---:
`cn-tx-bj3-w2d`| 双核 | `2G` | `50G` 普通云硬盘 | `10G` | `1Mbps` | `Windows Server 2022 Datacenter` | `2030-06-05 21:26:19`
`cn-tx-bj1-a8` | 双核 | `2G` | `50G` 普通云硬盘 | - | `1Mbps` | `AlmaLinux 8.5` | `2025-05-09 00:27:54`
`cn-tx-bj7-c8` | 四核 | `4G` | `80G SSD` 云硬盘 | `1000G` | `8Mbps 1200GB/月` | `CentOS 8.2` | `2024-12-20 22:07:24`
`cn-tx-bj6-c8` | 双核 | `4G` | `60G SSD` 云硬盘 | - | `6Mbps 1000GB/月` | `CentOS 8.2` | `2023-05-18 16:31:23`

## 0x04.安装[Smokeping](https://oss.oetiker.ch/smokeping)
``` bash
[root@cn-tx-bj7-c8 ~]# git clone https://github.com/linuxserver/docker-smokeping.git
[root@cn-tx-bj7-c8 ~]# cd docker-smokeping/
[root@cn-tx-bj7-c8 docker-smokeping]# cat docker-compose.yml 
---
version: "2.1"
services:
  smokeping:
    image: lscr.io/linuxserver/smokeping
    container_name: smokeping
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/London
    volumes:
      - /root/docker-smokeping/config:/config
      - /root/docker-smokeping/data:/data
    ports:
      - 82:80
    restart: unless-stopped
[root@cn-tx-bj7-c8 docker-smokeping]# docker-compose up -d
```

## 0x05.引用
[搭建一只Misskey实例](https://web.archive.org/web/20220705161154/https://candinya.com/posts/play-with-misskey/)
[使用Docker最小化部署Misskey](https://web.archive.org/web/20220705161256/https://candinya.com/posts/minimal-misskey-docker-deploy/)
