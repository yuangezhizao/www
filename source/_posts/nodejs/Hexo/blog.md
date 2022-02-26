---
title: 用 Hexo 搭建博客
date: 2018-2-20 15:39:14
tags:
  - Hexo
count: 4
os: 0
os_1: 10.0.14393 2016-LTSB
browser: 0
browser_0: 64.0.3282.140 Stable
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

顺便把`gh`的源码`clone`到了`CloudStudio`之中，~~这样上班太困了想摸鱼写写博客的话也是`ok`的，~~所谓的代码不落地可海星（`Doge`
![CloudStudio](https://i1.yuangezhizao.cn/Win-10/20190825230738.jpg!webp)

## 0x04.[Signing commits](https://web.archive.org/web/20200603140828/https://help.github.com/en/github/authenticating-to-github/signing-commits)
> You can sign your work locally using GPG or S/MIME. GitHub will verify these signatures so other people will know that your commits come from a trusted source. GitHub will automatically sign commits you make using the GitHub web interface.

`web`上的提交会被`gh`自动签名，本地提交需要使用`GnuPG`进行签名
官方文档[Managing commit signature verification](https://web.archive.org/web/20200603140752/https://help.github.com/en/github/authenticating-to-github/managing-commit-signature-verification)，根据交互提示创建不少于`4096`（官方要求）位的公私钥对
``` bash
<rm>@<rm> MINGW64 ~
$ gpg --list-secret-keys --keyid-format LONG
gpg: keybox '/c/Users/<rm>/.gnupg/pubring.kbx' created
gpg: /c/Users/<rm>/.gnupg/trustdb.gpg: trustdb created

<rm>@<rm> MINGW64 ~
$ gpg --list-secret-keys --keyid-format LONG

<rm>@<rm> MINGW64 ~
$ gpg --list-key

<rm>@<rm> MINGW64 ~
$ gpg --full-generate-key
gpg (GnuPG) 2.2.16-unknown; Copyright (C) 2019 Free Software Foundation, Inc.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Please select what kind of key you want:
   (1) RSA and RSA (default)
   (2) DSA and Elgamal
   (3) DSA (sign only)
   (4) RSA (sign only)
Your selection? 1
RSA keys may be between 1024 and 4096 bits long.
What keysize do you want? (2048) 4096
Requested keysize is 4096 bits
Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      <n>w = key expires in n weeks
      <n>m = key expires in n months
      <n>y = key expires in n years
Key is valid for? (0) 1y
Key expires at Fri, May 21, 2021  4:03:37 PM CST
Is this correct? (y/N) y

GnuPG needs to construct a user ID to identify your key.

Real name: yuangezhizao-workaccount
Email address: [email protected]
Comment:
You selected this USER-ID:
    "yuangezhizao-workaccount <[email protected]>"

Change (N)ame, (C)omment, (E)mail or (O)kay/(Q)uit? O
We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, utilize the
disks) during the prime generation; this gives the random number
generator a better chance to gain enough entropy.
We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, utilize the
disks) during the prime generation; this gives the random number
generator a better chance to gain enough entropy.
gpg: key 7C5AD4EFEBE22E2C marked as ultimately trusted
gpg: directory '/c/Users/<rm>/.gnupg/openpgp-revocs.d' created
gpg: revocation certificate stored as '/c/Users/<rm>/.gnupg/openpgp-revocs.d/529AB9F612C9EA2303836DCE7C5AD4EFEBE22E2C.rev'
public and secret key created and signed.

pub   rsa4096 2020-05-21 [SC] [expires: 2021-05-21]
      529AB9F612C9EA2303836DCE7C5AD4EFEBE22E2C
uid                      yuangezhizao-workaccount <[email protected]>
sub   rsa4096 2020-05-21 [E] [expires: 2021-05-21]


<rm>@<rm> MINGW64 ~
$ gpg --list-secret-keys --keyid-format LONG
/c/Users/<rm>/.gnupg/pubring.kbx
----------------------------------------
sec   rsa4096/7C5AD4EFEBE22E2C 2020-05-21 [SC] [expires: 2021-05-21]
      529AB9F612C9EA2303836DCE7C5AD4EFEBE22E2C
uid                 [ultimate] yuangezhizao-workaccount <[email protected]>
ssb   rsa4096/1D59D7933E6D6D58 2020-05-21 [E] [expires: 2021-05-21]


<rm>@<rm> MINGW64 ~
$ gpg --list-key
/c/Users/<rm>/.gnupg/pubring.kbx
----------------------------------------
pub   rsa4096 2020-05-21 [SC] [expires: 2021-05-21]
      529AB9F612C9EA2303836DCE7C5AD4EFEBE22E2C
uid           [ultimate] yuangezhizao-workaccount <[email protected]>
sub   rsa4096 2020-05-21 [E] [expires: 2021-05-21]

```

## 0x05.引用
> [使用Travis CI自动部署Hexo博客](https://web.archive.org/web/20190905064005/https://www.itfanr.cc/2017/08/09/using-travis-ci-automatic-deploy-hexo-blogs/)
[使用 Travis CI 自动部署 HEXO 博客](https://web.archive.org/web/20190905064039/https://www.giuem.com/deploy-via-travis-ci/)
[使用 travis-ci 持续集成 Hexo 静态博客](https://web.archive.org/web/20190905064103/https://www.pangjian.me/2016/05/25/travis-ci-hexo/)
[使用 Travis CI 自动部署 Hexo 博客](https://web.archive.org/web/20190905064132/https://blessing.studio/deploy-hexo-blog-automatically-with-travis-ci/)
[使用travis-ci自动部署Hexo到github和coding](https://web.archive.org/web/20190905064200/https://juejin.im/post/5afe61f5f265da0b8d422a3e)
[用TravisCI持续集成自动部署Hexo博客的个人实践](https://web.archive.org/web/20190905064240/https://mtianyan.gitee.io//post/90a759d5.html)

未完待续……