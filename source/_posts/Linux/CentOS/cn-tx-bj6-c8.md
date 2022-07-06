---
title: 重装系统之 cn-tx-bj6-c8 换至 Docker 基础镜像
date: 2022-07-05 23:52:58
tags:
  - CentOS
  - server
count: 2
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
![cn-tx-bj6-c8](https://i1.yuangezhizao.cn/macOS/20220706101209.png!webp)

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

## 0x02.安装[Smokeping](https://oss.oetiker.ch/smokeping)
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

## 0x03.引用
[搭建一只Misskey实例](https://web.archive.org/web/20220705161154/https://candinya.com/posts/play-with-misskey/)
[使用Docker最小化部署Misskey](https://web.archive.org/web/20220705161256/https://candinya.com/posts/minimal-misskey-docker-deploy/)
