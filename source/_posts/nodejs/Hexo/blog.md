---
title: 用 Hexo 搭建博客
date: 2018-2-20 15:39:14
tags:
  - Hexo
count: 2
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

## 0x01.安装[Node.js](https://nodejs.org/zh-cn/)
![每次去看都有更新，速度实在是太快了](https://i1.yuangezhizao.cn/Win-10/20191017213053.jpg!webp)
![坚决拒绝全家桶，不解释](https://i1.yuangezhizao.cn/Win-10/20191017214637.jpg!webp)

配置[淘宝`NPM`镜像](https://npm.taobao.org/)
`npm install -g cnpm --registry=https://registry.npm.taobao.org`

## 0x02.安装[Hexo](https://hexo.io/zh-cn/)
![作者台湾大学生](https://i1.yuangezhizao.cn/Win-10/20191017213644.jpg!webp)

``` bash
cnpm install hexo-cli -g
hexo init blog
cd blog
cnpm install
```
![全局安装](https://i1.yuangezhizao.cn/Win-10/20180220161242.jpg!webp)

``` bash
cnpm install hexo-renderer-less --save
cnpm install hexo-generator-feed --save
cnpm install hexo-generator-json-content --save
cnpm install hexo-helper-qrcode --save

cnpm install hexo-all-minifier --save
cnpm install hexo-wordcount --save
cnpm install hexo-generator-restful --save

cnpm install hexo-server --save
cnpm install hexo-helper-live2d --save
cnpm install hexo-filter-date-from-git --save
cnpm install hexo-native-lazy-load --save

hexo clean && hexo g && hexo s
```
貌似有`package.json`或者`package-lock.json`的话会自动安装上

## 0x03.[源码仓库](https://github.com/yuangezhizao/www)
源码放在了`gh`上，虽说这样的话整个网站~~容易~~**已经**被直接一锅端走（`Fork`），但是最终还是选择了这里
因为要配合[Travis CI](https://travis-ci.org)，`gh`公开仓库免费部署（跑编译）而私有仓库就得付费了……
具体的方法网上有一大堆可参考[引用第一条](#引用)，大概都是`gh`账号注册`CI`，然后开启项目开关，写好脚本和环境变量再设置设置就`ok`了
**迁移**还算顺利，现在的流程是：写完新文章提交到`gh`上，`CI`编译完推送到`Coding`企业版，最后会自动部署静态网站
暂时还没有用到`Coding`企业版的`CI`，其实主要还是`Jenkins`的语法过于复杂……还是`Travis CI`好！

![gh](https://i1.yuangezhizao.cn/Win-10/20190825230425.jpg!webp)
![CI](https://i1.yuangezhizao.cn/Win-10/20190825230257.jpg!webp)
![log](https://i1.yuangezhizao.cn/Win-10/20190825231016.jpg!webp)
![说明](https://i1.yuangezhizao.cn/Win-10/20190825222026.jpg!webp)
![使用访问令牌推送可省去配置 ssh 密钥的麻烦](https://i1.yuangezhizao.cn/Win-10/20190825224919.jpg!webp)
![代码更新时自动部署静态网站](https://i1.yuangezhizao.cn/Win-10/20190825224750.jpg!webp)
![部署成功](https://i1.yuangezhizao.cn/Win-10/20190825224831.jpg!webp)

顺便把`gh`的源码`clone`到了`CloudStudio`之中，~~这样上班太困了想摸鱼写写博客的话也是`ok`的，~~所谓的代码不落地可海星（Doge
![CloudStudio](https://i1.yuangezhizao.cn/Win-10/20190825230738.jpg!webp)

## 0x04.引用
> [使用Travis CI自动部署Hexo博客](https://web.archive.org/web/20190905064005/https://www.itfanr.cc/2017/08/09/using-travis-ci-automatic-deploy-hexo-blogs/)
[使用 Travis CI 自动部署 HEXO 博客](https://web.archive.org/web/20190905064039/https://www.giuem.com/deploy-via-travis-ci/)
[使用 travis-ci 持续集成 Hexo 静态博客](https://web.archive.org/web/20190905064103/https://www.pangjian.me/2016/05/25/travis-ci-hexo/)
[使用 Travis CI 自动部署 Hexo 博客](https://web.archive.org/web/20190905064132/https://blessing.studio/deploy-hexo-blog-automatically-with-travis-ci/)
[使用travis-ci自动部署Hexo到github和coding](https://web.archive.org/web/20190905064200/https://juejin.im/post/5afe61f5f265da0b8d422a3e)
[用TravisCI持续集成自动部署Hexo博客的个人实践](https://web.archive.org/web/20190905064240/https://mtianyan.gitee.io//post/90a759d5.html)

未完待续……