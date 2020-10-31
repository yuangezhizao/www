---
title: Windows 下 MongoDB 真正的升级姿势
date: 2020-8-9 18:39:31
tags:
  - Windows
  - MongoDB
count: 1
os: 0
os_1: 10.0.17763.1369 2019-LTSC
browser: 0
browser_1: 80.0.3987.163 Stable
place: 新家
key: 96
---
    昨天（周六）终于给捅咕上了（
<!-- more -->
## 0x00.前言
还记得上篇文章中所说
> MongoDB 4.4.0 移除了 2012 R2 的支持，不得不去升级了云主机系统

其实本来准备用到停止支持，毕竟`2012 R2`用习惯了还是很舒服的，而且新版的系统`bug`实在是太多了，就拿远程桌面举例经常「出现了内部错误」
![草](https://i1.yuangezhizao.cn/Win-10/20191016005155.jpg!webp)

## 0x01.授权认证
配置文件开启了`rs`副本集配置，但是可以不使用即远程连接的时候也只指定一个云主机
先在服务端配置用户名、密码，再映射到外网`0.0.0.0`并开启认证
``` javascript
use admin
db.createUser(
  {
    user: "<user>",
    pwd: "<pwd>",
    roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]
  }
)
```
> 内建角色
`Read`：允许用户读取指定数据库
`readWrite`：允许用户读写指定数据库
`dbAdmin`：允许用户在指定数据库中执行管理函数，如索引创建、删除，查看统计或访问`system.profile`
`userAdmin`：允许用户向`system.users`集合写入，可以找指定数据库里创建、删除和管理用户
`clusterAdmin`：只在`admin`数据库中可用，赋予用户所有分片和复制集相关函数的管理权限
`readAnyDatabase`：只在`admin`数据库中可用，赋予用户所有数据库的读权限
`readWriteAnyDatabase`：只在`admin`数据库中可用，赋予用户所有数据库的读写权限
`userAdminAnyDatabase`：只在`admin`数据库中可用，赋予用户所有数据库的`userAdmin`权限
`dbAdminAnyDatabase`：只在`admin`数据库中可用，赋予用户所有数据库的`dbAdmin`权限
`root`：只在`admin`数据库中可用。超级账号，超级权限

之后的命令行认证方法：
``` javascript
use admin
db.auth(<user>, <pwd>)
```
由于是重装了系统，因此需要重新配置文件夹的权限（不要说`Windows`下没有`Linux`的文件夹权限

## 0x02.升级姿势
需要在旧版本中运行

## 0x03.引用
> [MongoDB设置用户名和密码](https://web.archive.org/web/20200809105504/https://www.jianshu.com/p/c5f778adfbb3)
[创建mongodb副本集操作实例](https://web.archive.org/web/20200809105655/https://www.cnblogs.com/Joans/p/7680846.html)

未完待续……