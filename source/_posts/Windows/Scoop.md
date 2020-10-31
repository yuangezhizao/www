---
title: Windows 安装 Scoop 包管理器
date: 2020-10-31 12:01:01
tags:
  - Scoop
count: 1
os: 0
os_1: 10.0.17763.1518 2019-LTSC
browser: 0
browser_1: 80.0.3987.163 Stable
place: 新家
key: 102
---
     填坑
<!-- more -->
## 0x00.前言
早在今年`0626`就已经在本地草稿了，结果一直鸽到了今天……

## 0x02.配置代理
``` powershell
Microsoft Windows [版本 10.0.17763.1282]
(c) 2018 Microsoft Corporation。保留所有权利。

C:\Users\yuangezhizao>powershell
Windows PowerShell
版权所有 (C) Microsoft Corporation。保留所有权利。

PS C:\Users\yuangezhizao> iex (new-object net.webclient).downloadstring('https://get.scoop.sh')
Initializing...
Downloading scoop...
iex : 使用“2”个参数调用“DownloadFile”时发生异常:“在 WebClient 请求期间发生异常。”
所在位置 行:1 字符: 1
+ iex (new-object net.webclient).downloadstring('https://get.scoop.sh')
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (:) [Invoke-Expression], MethodInvocationException
    + FullyQualifiedErrorId : WebException,Microsoft.PowerShell.Commands.InvokeExpressionCommand
```
众所周知，这是因为`https://raw.githubusercontent.com/lukesampson/scoop/master/bin/install.ps1`无法访问所导致，在配好了`pac`代理之后自然就解决了问题
并且，也可以代理`git`，参照[git 设置和取消代理](https://gist.github.com/laispace/666dd7b27e9116faece6)
``` bash
git config --global http.https://github.com.proxy http://cn-py-dl-w9d:1081
git config --global --unset http.https://github.com.proxy)
```

## 0x03.[Scoop](https://scoop.sh/)
``` powershell
PS C:\Users\yuangezhizao> iex (new-object net.webclient).downloadstring('https://get.scoop.sh')
Initializing...
Downloading scoop...
Extracting...
Creating shim...
Downloading main bucket...
Extracting...
Adding ~\scoop\shims to your path.
'lastupdate' has been set to '2020-10-31T11:51:59.1432975+08:00'
Scoop was installed successfully!
Type 'scoop help' for instructions.
PS C:\Users\yuangezhizao> scoop help
Usage: scoop <command> [<args>]

Some useful commands are:

alias       Manage scoop aliases
bucket      Manage Scoop buckets
cache       Show or clear the download cache
checkup     Check for potential problems
cleanup     Cleanup apps by removing old versions
config      Get or set configuration values
create      Create a custom app manifest
depends     List dependencies for an app
export      Exports (an importable) list of installed apps
help        Show help for a command
hold        Hold an app to disable updates
home        Opens the app homepage
info        Display information about an app
install     Install apps
list        List installed apps
prefix      Returns the path to the specified app
reset       Reset an app to resolve conflicts
search      Search available apps
status      Show status and check for new app versions
unhold      Unhold an app to enable updates
uninstall   Uninstall an app
update      Update apps, or Scoop itself
virustotal  Look for app's hash on virustotal.com
which       Locate a shim/executable (similar to 'which' on Linux)


Type 'scoop help <command>' to get help for a specific command.
PS C:\Users\yuangezhizao> scoop install curl
Installing '7zip' (19.00) [64bit]
7z1900-x64.msi (1.7 MB) [=====================================================================================] 100%
Checking hash of 7z1900-x64.msi ... ok.
Extracting 7z1900-x64.msi ... done.
Linking ~\scoop\apps\7zip\current => ~\scoop\apps\7zip\19.00
Creating shim for '7z'.
Creating shortcut for 7-Zip (7zFM.exe)
'7zip' (19.00) was installed successfully!
Installing 'curl' (7.73.0_1) [64bit]
curl-7.73.0_1-win64-mingw.tar.xz (2.2 MB) [===================================================================] 100%
Checking hash of curl-7.73.0_1-win64-mingw.tar.xz ... ok.
Extracting curl-7.73.0_1-win64-mingw.tar.xz ... done.
Linking ~\scoop\apps\curl\current => ~\scoop\apps\curl\7.73.0_1
Creating shim for 'curl'.
'curl' (7.73.0_1) was installed successfully!
```
就可以用命令行调用了
``` cmd
Microsoft Windows [版本 10.0.17763.1518]
(c) 2018 Microsoft Corporation。保留所有权利。

C:\Users\yuangezhizao>where curl
C:\Users\yuangezhizao\scoop\shims\curl.exe
```
未完待续……