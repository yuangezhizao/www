---
title: 用 Hexo 搭建博客
date: 2018-2-20 15:39:14
tags:
  - Hexo
count: 1
os: 0
os_1: 10.0.14393 2016-LTSB
browser: 0
browser_1: 64.0.3282.140 Stable
place: 家
key: 30
---
    准备详细说明……
<!-- more -->
## 0x00.缘由
升级搞崩了，于是重新做人

## 0x01.安装[node.js](https://nodejs.org/zh-cn/)
![](https://i1.yuangezhizao.cn/Win-10/20180220154155.jpg!webp)

## 0x02.[淘宝镜像](https://npm.taobao.org/)
```
npm install -g cnpm --registry=https://registry.npm.taobao.org
```

## 0x03.安装[hexo](https://hexo.io/zh-cn/)
![](https://i1.yuangezhizao.cn/Win-10/20180220154341.jpg!webp)
```
cnpm install hexo-cli -g
```

## 0x04.主题配置
```
hexo init blog
cd blog
cnpm install
```
![](https://i1.yuangezhizao.cn/Win-10/20180220161242.jpg!webp)
```
cnpm install hexo-renderer-less --save
cnpm install hexo-generator-feed --save
cnpm install hexo-generator-json-content --save
cnpm install hexo-helper-qrcode --save
```

## 0x05.自定义
```
cnpm install hexo-all-minifier --save
cnpm i --save hexo-wordcount
cnpm install hexo-generator-restful --save
```

## 0x06.测试
```
hexo clean && hexo g && hexo s
```
