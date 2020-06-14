---
title: CHUNITHM AMAZON 安装
date: 2020-6-14 21:41:55
tags:
  - CHUNITHM
  - CHUNITHM AMAZON
  - SEGA
count: 1
os: 0
os_1: 10.0.17763.1158 2019-LTSC
browser: 0
browser_1: 78.0.3904.108 Stable
place: 新家
key: 91
---
    俩月前就在本地草稿了但是没分配文章 key，结果一直鸽到现在只能分配新 key 了草……
    混个「周更」，于是改掉了真正的原始创建时间：2020-4-25 11:26:23
<!-- more -->
## 0x00.前言
昨晚看了一晚上`emuline`

## 0x01.安装
``` bash
C:\minime>C:\minime\start.bat
The server's dependencies will now be installed.
This process requires an internet connection and may take some time.

NOTE: If install fails try running the following command as admin:
npm install -g windows-build-tools

请按任意键继续. . .

> integer@2.1.0 install C:\minime\node_modules\integer
> node-gyp rebuild


C:\minime\node_modules\integer>if not defined npm_config_node_gyp (node "C:\Program Files\nodejs\node_modules\npm\node_modules\npm-lifecycle\node-gyp-bin\\..\..\node_modules\node-gyp\bin\node-gyp.js" rebuild )  else (node "C:\Program Files\nodejs\node_modules\npm\node_modules\node-gyp\bin\node-gyp.js" rebuild )
gyp WARN install got an error, rolling back install
gyp ERR! configure error
gyp ERR! stack Error: Client network socket disconnected before secure TLS connection was established
gyp ERR! stack     at connResetException (internal/errors.js:613:14)
gyp ERR! stack     at TLSSocket.onConnectEnd (_tls_wrap.js:1525:19)
gyp ERR! stack     at TLSSocket.emit (events.js:327:22)
gyp ERR! stack     at endReadableNT (_stream_readable.js:1218:12)
gyp ERR! stack     at processTicksAndRejections (internal/process/task_queues.js:84:21)
gyp ERR! System Windows_NT 10.0.17763
gyp ERR! command "C:\\Program Files\\nodejs\\node.exe" "C:\\Program Files\\nodejs\\node_modules\\npm\\node_modules\\node-gyp\\bin\\node-gyp.js" "rebuild"
gyp ERR! cwd C:\minime\node_modules\integer
gyp ERR! node -v v14.0.0
gyp ERR! node-gyp -v v5.1.0
gyp ERR! not ok
npm WARN optional SKIPPING OPTIONAL DEPENDENCY: fsevents@1.2.9 (node_modules\fsevents):
npm WARN notsup SKIPPING OPTIONAL DEPENDENCY: Unsupported platform for fsevents@1.2.9: wanted {"os":"darwin","arch":"any"} (current: {"os":"win32","arch":"x64"})

npm ERR! code ELIFECYCLE
npm ERR! errno 1
npm ERR! integer@2.1.0 install: `node-gyp rebuild`
npm ERR! Exit status 1
npm ERR!
npm ERR! Failed at the integer@2.1.0 install script.
npm ERR! This is probably not a problem with npm. There is likely additional logging output above.

npm ERR! A complete log of this run can be found in:
npm ERR!     C:\Users\yuangezhizao\AppData\Roaming\npm-cache\_logs\2020-04-25T03_17_10_938Z-debug.log
Installation failed. Cannot continue.

请按任意键继续. . .

C:\minime>
C:\minime>npm --registry https://registry.npm.taobao.org install -g node-gypnpm config delete proxy
^C终止批处理操作吗(Y/N)? Y

C:\minime>npm config delete proxy

C:\minime>C:\minime\start.bat
The server's dependencies will now be installed.
This process requires an internet connection and may take some time.

NOTE: If install fails try running the following command as admin:
npm install -g windows-build-tools

请按任意键继续. . .

> integer@2.1.0 install C:\minime\node_modules\integer
> node-gyp rebuild


C:\minime\node_modules\integer>if not defined npm_config_node_gyp (node "C:\Program Files\nodejs\node_modules\npm\node_modules\npm-lifecycle\node-gyp-bin\\..\..\node_modules\node-gyp\bin\node-gyp.js" rebuild )  else (node "C:\Program Files\nodejs\node_modules\npm\node_modules\node-gyp\bin\node-gyp.js" rebuild )
在此解决方案中一次生成一个项目。若要启用并行生成，请添加“/m”开关。
  integer.cpp
  win_delay_load_hook.cc
c:\minime\node_modules\integer\src\integer.cpp(370): warning C4804: “-”: 在操作中使用类型“bool”不安全 [C:\minime\node_modules\inte
ger\build\integer.vcxproj]
    正在创建库 C:\minime\node_modules\integer\build\Release\integer.lib 和对象 C:\minime\node_modules\integer\build\Release\int
  eger.exp
  integer.vcxproj -> C:\minime\node_modules\integer\build\Release\\integer.node
  Copying C:\minime\node_modules\integer\build\Release\/integer.node to build\integer.node
  已复制         1 个文件。

> better-sqlite3@5.4.3 install C:\minime\node_modules\better-sqlite3
> node-gyp rebuild


C:\minime\node_modules\better-sqlite3>if not defined npm_config_node_gyp (node "C:\Program Files\nodejs\node_modules\npm\node_modules\npm-lifecycle\node-gyp-bin\\..\..\node_modules\node-gyp\bin\node-gyp.js" rebuild )  else (node "C:\Program Files\nodejs\node_modules\npm\node_modules\node-gyp\bin\node-gyp.js" rebuild )
在此解决方案中一次生成一个项目。若要启用并行生成，请添加“/m”开关。
  extract_sqlite3
  sqlite3.c
  win_delay_load_hook.cc
  sqlite3.vcxproj -> C:\minime\node_modules\better-sqlite3\build\Release\\sqlite3.lib
  better_sqlite3.cpp
  win_delay_load_hook.cc
c:\minime\node_modules\better-sqlite3\build\src\objects\database.lzz(129): warning C4996: 'node::AtExit': 被声明为已否决 (编译源文
件 ..\src\better_sqlite3.cpp) [C:\minime\node_modules\better-sqlite3\build\better_sqlite3.vcxproj]
  c:\users\yuangezhizao\appdata\local\node-gyp\cache\14.0.0\include\node\node.h(823): note: 参见“node::AtExit”的声明 (编译源文件
  ..\src\better_sqlite3.cpp)
    正在创建库 C:\minime\node_modules\better-sqlite3\build\Release\better_sqlite3.lib 和对象 C:\minime\node_modules\better-sqli
  te3\build\Release\better_sqlite3.exp
  better_sqlite3.vcxproj -> C:\minime\node_modules\better-sqlite3\build\Release\\better_sqlite3.node
  test_extension.c
  win_delay_load_hook.cc
  test_extension.vcxproj -> C:\minime\node_modules\better-sqlite3\build\Release\\test_extension.node
  Copying C:\minime\node_modules\better-sqlite3\build\Release\/better_sqlite3.node to build\better_sqlite3.node
  已复制         1 个文件。
  Copying C:\minime\node_modules\better-sqlite3\build\Release\/test_extension.node to build\test_extension.node
  已复制         1 个文件。

> minime@0.1.0 prepare C:\minime
> tsc

npm WARN optional SKIPPING OPTIONAL DEPENDENCY: fsevents@1.2.9 (node_modules\fsevents):
npm WARN notsup SKIPPING OPTIONAL DEPENDENCY: Unsupported platform for fsevents@1.2.9: wanted {"os":"darwin","arch":"any"} (current: {"os":"win32","arch":"x64"})

added 575 packages from 480 contributors in 143.048s
Installation successful, launching server.

  app:switchboard HOST_EXT: 127.0.0.1 (Service host name sent to clients) +0ms
  app:switchboard HOST_INT: 0.0.0.0 (Bind address) +3ms
  app:switchboard Using default host names, change them from the .env file if necessary. +6ms
  app:checkdb Initializing database +0ms
  app:checkdb Executing meta.sql +1ms
  app:checkdb Executing aime.sql +35ms
  app:checkdb Executing cm.sql +2ms
  app:checkdb Executing idz.sql +15ms
  app:checkdb Initialized new database to schema version 12 +12ms
Startup OK
```
未完待续……