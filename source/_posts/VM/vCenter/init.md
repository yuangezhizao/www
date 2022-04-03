---
title: VMware vCenter Server 7.0.0 安装及配置
date: 2021-09-27 21:20:31
tags:
  - VM
  - VMware
  - vCenter
count: 3
os: 1
os_1: Monterry 12.0 Beta (21A5506j)
browser: 0
browser_1: 94.0.4606.61 Stable
place: 新家
key: 120
---
    鸽了半年的水（jie）文（tu）终于发出来了
<!-- more -->
## 0x00.前言
工作的时候发现大都在用`vCenter`，看到家里只安装了`ESXi`决定也搞一个好了

## 0x01.安装
> 多图预警

### 1.第`1`阶段

<details><summary>点击此处 ← 查看折叠</summary>

![安装](https://i1.yuangezhizao.cn/Win-10/20210303123626.png!webp)
![下一步](https://i1.yuangezhizao.cn/Win-10/20210303123640.png!webp)
![下一步](https://i1.yuangezhizao.cn/Win-10/20210303123652.png!webp)
![微型](https://i1.yuangezhizao.cn/Win-10/20210303124747.png!webp)
![NASdata](https://i1.yuangezhizao.cn/Win-10/20210303124900.png!webp)
![192.168.25.230](https://i1.yuangezhizao.cn/Win-10/20210303125103.png!webp)
![完成](https://i1.yuangezhizao.cn/Win-10/20210303125121.png!webp)
![部署设备](https://i1.yuangezhizao.cn/Win-10/20210303125141.png!webp)
![继续](https://i1.yuangezhizao.cn/Win-10/20210303130407.png!webp)

</details>

### 2.第`2`阶段

<details><summary>点击此处 ← 查看折叠</summary>

![下一步](https://i1.yuangezhizao.cn/Win-10/20210303130426.png!webp)
![设备配置](https://i1.yuangezhizao.cn/Win-10/20210303130523.png!webp)
![开启 SSH](https://i1.yuangezhizao.cn/Win-10/20210303130617.png!webp)
![这里搞错了，应该加入现有 SSO 域才对](https://i1.yuangezhizao.cn/Win-10/20210303130750.png!webp)
![CEIP 可以配置后续加入](https://i1.yuangezhizao.cn/Win-10/20210303130811.png!webp)
![完成](https://i1.yuangezhizao.cn/Win-10/20210303130832.png!webp)
![确定](https://i1.yuangezhizao.cn/Win-10/20210303130843.png!webp)
![完成](https://i1.yuangezhizao.cn/Win-10/20210303131141.png!webp)

</details>

## 0x02.配置
### 1.配置域用户登录
`系统管理`，`Single Sign On`，`配置`，`身份提供程序`，`标识源`，`添加标识源`
![](https://i1.yuangezhizao.cn/macOS/20211128213700.png!webp)

`标识源类型`选择`Active Directory（集成 Windows 身份验证）`，输入域名即可
![](https://i1.yuangezhizao.cn/macOS/20211128214105.png!webp)

也可以加入`AD`域
![](https://i1.yuangezhizao.cn/macOS/20211128214310.png!webp)

然后注销，尝试用域账户登录，不出意料可以登录但是没有权限……
`无法登录，因为您在连接到此客户端的所有 vCenter Server 系统上均没有权限。`
![](https://i1.yuangezhizao.cn/macOS/20211128214454.png!webp)

一种方法自然是直接加到管理员里去，`访问控制`，`全局权限`，`添加`自己的用户成`管理员`
![](https://i1.yuangezhizao.cn/macOS/20211128214807.png!webp)
![](https://i1.yuangezhizao.cn/macOS/20211128214935.png!webp)

~~奇怪了，用户名`yuangezhizao`可以登录但还是没有权限，`yuangezhizao@py.local`则可以登录同时也有权限~~
![](https://i1.yuangezhizao.cn/macOS/20211128215406.png!webp)

~~光速破案，前者是自己曾经在`VC.LOCAL`域下创建的用户，但是没有给分配权限，于是现在给删掉了只使用后者的域账户~~
后续发现后者除了没有配置`Single Sign On`的权限之外其他的权限都有，然后还有一件诡异的事情是从`管理员`中移除自己后仍然是可以登录的草，保持了管理员的身份……
那么，如果想拥有配置`Single Sign On`的权限则需要把自己的域用户加入到默认的`Administrators`组里才可以访问全部，相当于真正的管理员

## 0x03.后记
~~`45min`光速`xjb`写完草~~

## 0x04.引用
[将域用户添加为VCSA（vCenter Server Application）管理员](https://web.archive.org/web/20211128133851/https://www.dinghui.org/domain-user-vcsa-administrator.html)

> 至此本文使命完成
