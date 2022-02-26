---
title: Windows Server 2019 数据中心版 64 位中文版安装 Windows Server Admin
date: 2020-8-9 17:46:43
tags:
  - Windows
  - server
  - Windows Server Admin
count: 2
os: 0
os_1: 10.0.17763.1369 2019-LTSC
browser: 0
browser_0: 80.0.3987.163 Stable
place: 新家
key: 95
---
    MongoDB 4.4.0 移除了 2012 R2 的支持，不得不去升级了云主机系统
<!-- more -->
## 0x00.前言
[Windows Server 2019 中的新增功能](https://web.archive.org/web/20200809105711/https://docs.microsoft.com/zh-cn/windows-server/get-started-19/whats-new-19)：`Windows Admin Center`
![whats-new-19](https://i1.yuangezhizao.cn/Win-10/20200809175205.jpg!webp)

## 0x01.`WinRM`
不着急安装`WAC`（本文下同，均为`Windows Admin Center`的缩写），先来开启`Windows Remote Management`即远程管理服务，真正的命令行出现了！
### 服务端
首先查询监听器，应该为空
``` powershell
[lab.yuangezhizao.cn]: PS C:\Users\yuangezhizao\Documents> winrm enumerate winrm/config/listener
[lab.yuangezhizao.cn]: PS C:\Users\yuangezhizao\Documents>
```
快速配置，这里本人已经配置过了，所以与你们的输出是不一样的
``` powershell
[lab.yuangezhizao.cn]: PS C:\Users\yuangezhizao\Documents> winrm quickconfig
已在此计算机上运行 WinRM 服务。
WinRM 没有设置成为了管理此计算机而允许对其进行远程访问。
必须进行以下更改:

在 HTTP://* 上创建 WinRM 侦听程序接受 WS-Man 对此机器上任意 IP 的请求。

winrm :
    + CategoryInfo          : NotSpecified: (:String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError

错误编号: 62 0x3E
输入超出了文件尾
执行这些更改吗[y/n]?
[lab.yuangezhizao.cn]: PS C:\Users\yuangezhizao\Documents>
```
再次查询监听器，此时应该会有默认`5985`的`HTTP`存在，这里为了安全性考虑只配置了`HTTPS`故删除了`HTTP`
``` powershell
[lab.yuangezhizao.cn]: PS C:\Users\yuangezhizao\Documents> winrm e winrm/config/listener
Listener
    Address = *
    Transport = HTTPS
    Port = 5986
    Hostname
    Enabled = true
    URLPrefix = wsman
    CertificateThumbprint = 6b1365d34016df28578f52a7eb6be956ef631da6
    ListeningOn = 10.0.2.2, 127.0.0.1, ::1, fe80::8c87:5082:5569:3e03%11

[lab.yuangezhizao.cn]: PS C:\Users\yuangezhizao\Documents>
```
添加认证方式：`Basic`、`CredSSP`
``` powershell
[lab.yuangezhizao.cn]: PS C:\Users\yuangezhizao\Documents> winrm set winrm/config/service/auth '@{Basic="true"}'
[lab.yuangezhizao.cn]: PS C:\Users\yuangezhizao\Documents> winrm set winrm/config/service/auth '@{CredSSP="true"}'
[lab.yuangezhizao.cn]: PS C:\Users\yuangezhizao\Documents> winrm get winrm/config/service/auth
Auth
    Basic = true
    Kerberos = true
    Negotiate = true
    Certificate = false
    CredSSP = true
    CbtHardeningLevel = Relaxed
```
~~如果没有证书的话，`winrm set winrm/config/service '@{AllowUnencrypted="true"}'`~~
腾讯云的`SSL`证书含有`IIS`类型的，因此可以导入到`服务器证书`之中，类型是`个人`
【❗】确认移除所有的监听器（请谨慎执行）
``` powershell
Get-childitem WSMan:\Localhost\listener\
Remove-Item -Path WSMan:\Localhost\listener\listener* -Recurse
Get-childitem WSMan:\Localhost\listener\
```
添加`HTTPS`监听器，提前复制好证书指纹的那一串
![指纹](https://i1.yuangezhizao.cn/Win-10/20200809181414.jpg!webp)

``` powershell
New-Item -Path WSMan:\LocalHost\Listener -Transport HTTPS -Address * -Force -CertificateThumbPrint <证书指纹>
```

### 客户端
``` powershell
Microsoft Windows [版本 10.0.17763.1369]
(c) 2018 Microsoft Corporation。保留所有权利。

C:\Users\yuangezhizao>powershell
Windows PowerShell
版权所有 (C) Microsoft Corporation。保留所有权利。

PS C:\Users\yuangezhizao> $cred=get-Credential

位于命令管道位置 1 的 cmdlet Get-Credential
请为以下参数提供值:
Credential
PS C:\Users\yuangezhizao> Enter-PSSession -computername lab.yuangezhizao.cn  -Credential $cred -UseSSL
[lab.yuangezhizao.cn]: PS C:\Users\yuangezhizao\Documents>
```
![输入凭证](https://i1.yuangezhizao.cn/Win-10/20200809181827.jpg!webp)
![成功登录](https://i1.yuangezhizao.cn/Win-10/20200809182000.jpg!webp)

## 0x02.[WAC](https://web.archive.org/web/20200809105833/https://docs.microsoft.com/zh-cn/windows-server/manage/windows-admin-center/overview)
官方中文文档其实已经足够详细了，首先去[下载](https://web.archive.org/web/20200809110138/https://www.microsoft.com/en-us/evalcenter/evaluate-windows-admin-center)`WindowsAdminCenter2007.msi`
![下载](https://i1.yuangezhizao.cn/Win-10/20200809183003.jpg!webp)

[官方入门](https://web.archive.org/web/20200809110432/https://docs.microsoft.com/zh-cn/windows-server/manage/windows-admin-center/use/get-started)
安装完成之后就可以访问`6516`端口的服务了，首次访问是用的`AD`认证，毕竟微软爸爸，而且`Chrome`清除站点数据并不能清理掉认证信息，然后就去云主机删除了那个用户……
但是自己的账户莫名登录不上，`日志查看器`中可以看到堆栈详细信息……不知道该怎么调查这个现象的原因
![登录不能](https://i1.yuangezhizao.cn/Win-10/20200809183239.png!webp)

## 0x3.引用
> [走进winrm ---powershell远程连接的4个安全级别，详解](https://web.archive.org/web/20200809105839/https://www.cnblogs.com/piapia/p/11897713.html)
[Windows Server 2019开启Winrm服务](https://web.archive.org/web/20200809110035/https://www.cnblogs.com/hicuiyang/p/11548901.html)
