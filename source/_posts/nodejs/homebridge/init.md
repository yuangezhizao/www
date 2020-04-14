---
title: Windows Server 2019 安装 Homebridge
date: 2020-4-6 00:33:46
tags:
  - Homebridge
  - homebridge-homeassistant
  - HomeKit
count: 1
os: 0
os_1: 10.0.17763.1098 2019-LTSC
browser: 0
browser_1: 78.0.3904.108 Stable
place: 新家
key: 82
---
    IOS 的「家庭」果然还是想试试看哇
<!-- more -->
## 0x00.前言
写完发现其实`Homebridge`对于`HA`并没有明显的作用了草，但是既然写了那就还是发出来吧……

## 0x01.安装[Node.js](https://nodejs.org/)
`node-v13.12.0-x64.msi`安装最新版
``` bash
Microsoft Windows [版本 10.0.17763.1131]
(c) 2018 Microsoft Corporation。保留所有权利。

C:\Windows\system32>node -v
v13.12.0

C:\Windows\system32>npm -v
6.14.4
```

## 0x02.安装[Homebridge](https://web.archive.org/web/20200406051732/https://github.com/homebridge/homebridge/wiki/Install-Homebridge-on-Windows-10)
官方文档非常良心，操作步骤详细，跟着一步一步走就行了，别小瞧这个`npm`的`package`，费了九牛二虎之力（挂个代理）才装上的
`npm install -g --unsafe-perm homebridge homebridge-config-ui-x`

<details><summary>点击此处 ← 查看终端</summary>

``` bash
C:\Windows\system32>npm install -g --unsafe-perm homebridge homebridge-config-ui-x
npm WARN deprecated mkdirp@0.3.5: Legacy versions of mkdirp are no longer supported. Please update to mkdirp 1.x. (Note that the API surface has changed to use Promises in 1.x.)
npm ERR! code EAI_AGAIN
npm ERR! errno EAI_AGAIN
npm ERR! request to https://registry.npmjs.org/rc failed, reason: getaddrinfo EAI_AGAIN registry.npmjs.org

npm ERR! A complete log of this run can be found in:
npm ERR!     C:\Users\yuangezhizao\AppData\Roaming\npm-cache\_logs\2020-04-05T16_38_09_356Z-debug.log

C:\Windows\system32>npm install -g --unsafe-perm homebridge homebridge-config-ui-x
npm WARN registry Using stale data from https://registry.npmjs.org/ because the host is inaccessible -- are you offline?
npm WARN registry Using stale data from https://registry.npmjs.org/ due to a request error during revalidation.
npm WARN deprecated mkdirp@0.3.5: Legacy versions of mkdirp are no longer supported. Please update to mkdirp 1.x. (Note that the API surface has changed to use Promises in 1.x.)
npm ERR! cb() never called!

npm ERR! This is an error with npm itself. Please report this error at:
npm ERR!     <https://npm.community>

npm ERR! A complete log of this run can be found in:
npm ERR!     C:\Users\yuangezhizao\AppData\Roaming\npm-cache\_logs\2020-04-05T16_42_43_717Z-debug.log

C:\Windows\system32>npm install mkdirp -g
C:\Users\yuangezhizao\AppData\Roaming\npm\mkdirp -> C:\Users\yuangezhizao\AppData\Roaming\npm\node_modules\mkdirp\bin\cmd.js
+ mkdirp@1.0.4
added 1 package in 2.212s

C:\Windows\system32>npm install -g --unsafe-perm homebridge homebridge-config-ui-x
npm WARN deprecated mkdirp@0.3.5: Legacy versions of mkdirp are no longer supported. Please update to mkdirp 1.x. (Note that the API surface has changed to use Promises in 1.x.)
npm ERR! code EAI_AGAIN
npm ERR! errno EAI_AGAIN
npm ERR! request to https://registry.npmjs.org/supports-color/-/supports-color-7.1.0.tgz failed, reason: getaddrinfo EAI_AGAIN registry.npmjs.org

npm ERR! A complete log of this run can be found in:
npm ERR!     C:\Users\yuangezhizao\AppData\Roaming\npm-cache\_logs\2020-04-05T16_46_08_444Z-debug.log

C:\Windows\system32>npm install -g --unsafe-perm homebridge homebridge-config-ui-x
npm WARN registry Unexpected warning for https://registry.npmjs.org/: Miscellaneous Warning EAI_AGAIN: request to https://registry.npmjs.org/homebridge-config-ui-x failed, reason: getaddrinfo EAI_AGAIN registry.npmjs.org
npm WARN registry Using stale data from https://registry.npmjs.org/ due to a request error during revalidation.
npm WARN deprecated mkdirp@0.3.5: Legacy versions of mkdirp are no longer supported. Please update to mkdirp 1.x. (Note that the API surface has changed to use Promises in 1.x.)
C:\Users\yuangezhizao\AppData\Roaming\npm\homebridge-config-ui-x -> C:\Users\yuangezhizao\AppData\Roaming\npm\node_modules\homebridge-config-ui-x\dist\bin\standalone.js
C:\Users\yuangezhizao\AppData\Roaming\npm\hb-service -> C:\Users\yuangezhizao\AppData\Roaming\npm\node_modules\homebridge-config-ui-x\dist\bin\hb-service.js
C:\Users\yuangezhizao\AppData\Roaming\npm\homebridge -> C:\Users\yuangezhizao\AppData\Roaming\npm\node_modules\homebridge\bin\homebridge

> node-pty-prebuilt-multiarch@0.9.0 install C:\Users\yuangezhizao\AppData\Roaming\npm\node_modules\homebridge-config-ui-x\node_modules\node-pty-prebuilt-multiarch
> prebuild-install || node scripts/install.js

prebuild-install WARN install getaddrinfo ENOTFOUND github-production-release-asset-2e65be.s3.amazonaws.com

C:\Users\yuangezhizao\AppData\Roaming\npm\node_modules\homebridge-config-ui-x\node_modules\node-pty-prebuilt-multiarch>if not defined npm_config_node_gyp (node "C:\Program Files\nodejs\node_modules\npm\node_modules\npm-lifecycle\node-gyp-bin\\..\..\node_modules\node-gyp\bin\node-gyp.js" rebuild )  else (node "C:\Program Files\nodejs\node_modules\npm\node_modules\node-gyp\bin\node-gyp.js" rebuild )
gyp WARN install got an error, rolling back install
gyp ERR! configure error
gyp ERR! stack Error: This is most likely not a problem with node-gyp or the package itself and
gyp ERR! stack is related to network connectivity. In most cases you are behind a proxy or have bad
gyp ERR! stack network settings.
gyp ERR! stack     at Request.<anonymous> (C:\Program Files\nodejs\node_modules\npm\node_modules\node-gyp\lib\install.js:171:21)
gyp ERR! stack     at Request.emit (events.js:315:20)
gyp ERR! stack     at Request.onRequestError (C:\Program Files\nodejs\node_modules\npm\node_modules\request\request.js:881:8)
gyp ERR! stack     at ClientRequest.emit (events.js:315:20)
gyp ERR! stack     at TLSSocket.socketErrorListener (_http_client.js:432:9)
gyp ERR! stack     at TLSSocket.emit (events.js:315:20)
gyp ERR! stack     at emitErrorNT (internal/streams/destroy.js:84:8)
gyp ERR! stack     at processTicksAndRejections (internal/process/task_queues.js:84:21)
gyp ERR! System Windows_NT 10.0.17763
gyp ERR! command "C:\\Program Files\\nodejs\\node.exe" "C:\\Program Files\\nodejs\\node_modules\\npm\\node_modules\\node-gyp\\bin\\node-gyp.js" "rebuild"
gyp ERR! cwd C:\Users\yuangezhizao\AppData\Roaming\npm\node_modules\homebridge-config-ui-x\node_modules\node-pty-prebuilt-multiarch
gyp ERR! node -v v13.12.0
gyp ERR! node-gyp -v v5.1.0
gyp ERR! not ok
npm ERR! code ELIFECYCLE
npm ERR! errno 1
npm ERR! node-pty-prebuilt-multiarch@0.9.0 install: `prebuild-install || node scripts/install.js`
npm ERR! Exit status 1
npm ERR!
npm ERR! Failed at the node-pty-prebuilt-multiarch@0.9.0 install script.
npm ERR! This is probably not a problem with npm. There is likely additional logging output above.

npm ERR! A complete log of this run can be found in:
npm ERR!     C:\Users\yuangezhizao\AppData\Roaming\npm-cache\_logs\2020-04-05T16_50_18_623Z-debug.log

C:\Windows\system32>npm config set https-proxy http://127.0.0.1:1081

C:\Windows\system32>npm install -g --unsafe-perm homebridge homebridge-config-ui-x
npm WARN deprecated mkdirp@0.3.5: Legacy versions of mkdirp are no longer supported. Please update to mkdirp 1.x. (Note that the API surface has changed to use Promises in 1.x.)
C:\Users\yuangezhizao\AppData\Roaming\npm\homebridge -> C:\Users\yuangezhizao\AppData\Roaming\npm\node_modules\homebridge\bin\homebridge
npm ERR! code EEXIST
npm ERR! path C:\Users\yuangezhizao\AppData\Roaming\npm\node_modules\homebridge-config-ui-x\dist\bin\standalone.js
npm ERR! dest C:\Users\yuangezhizao\AppData\Roaming\npm\homebridge-config-ui-x
npm ERR! EEXIST: file already exists, cmd shim 'C:\Users\yuangezhizao\AppData\Roaming\npm\node_modules\homebridge-config-ui-x\dist\bin\standalone.js' -> 'C:\Users\yuangezhizao\AppData\Roaming\npm\homebridge-config-ui-x'
npm ERR! File exists: C:\Users\yuangezhizao\AppData\Roaming\npm\homebridge-config-ui-x
npm ERR! Remove the existing file and try again, or run npm
npm ERR! with --force to overwrite files recklessly.

npm ERR! A complete log of this run can be found in:
npm ERR!     C:\Users\yuangezhizao\AppData\Roaming\npm-cache\_logs\2020-04-05T16_55_40_865Z-debug.log

C:\Windows\system32>npm install -g --unsafe-perm homebridge homebridge-config-ui-x --force
npm WARN using --force I sure hope you know what you are doing.
npm WARN deprecated mkdirp@0.3.5: Legacy versions of mkdirp are no longer supported. Please update to mkdirp 1.x. (Note that the API surface has changed to use Promises in 1.x.)
C:\Users\yuangezhizao\AppData\Roaming\npm\homebridge -> C:\Users\yuangezhizao\AppData\Roaming\npm\node_modules\homebridge\bin\homebridge
C:\Users\yuangezhizao\AppData\Roaming\npm\homebridge-config-ui-x -> C:\Users\yuangezhizao\AppData\Roaming\npm\node_modules\homebridge-config-ui-x\dist\bin\standalone.js
C:\Users\yuangezhizao\AppData\Roaming\npm\hb-service -> C:\Users\yuangezhizao\AppData\Roaming\npm\node_modules\homebridge-config-ui-x\dist\bin\hb-service.js

> node-pty-prebuilt-multiarch@0.9.0 install C:\Users\yuangezhizao\AppData\Roaming\npm\node_modules\homebridge-config-ui-x\node_modules\node-pty-prebuilt-multiarch
> prebuild-install || node scripts/install.js


> @nestjs/core@7.0.7 postinstall C:\Users\yuangezhizao\AppData\Roaming\npm\node_modules\homebridge-config-ui-x\node_modules\@nestjs\core
> opencollective || exit 0

                           Thanks for installing nest
                 Please consider donating to our open collective
                        to help us maintain this package.


         Become a partner: https://opencollective.com/nest/donate


> node-pty-prebuilt-multiarch@0.9.0 postinstall C:\Users\yuangezhizao\AppData\Roaming\npm\node_modules\homebridge-config-ui-x\node_modules\node-pty-prebuilt-multiarch
> node scripts/post-install.js

+ homebridge@0.4.53
+ homebridge-config-ui-x@4.13.3
added 316 packages from 200 contributors and updated 1 package in 469.339s

C:\Windows\system32>
```

</details>

最后会被设置为服务项，其中下载`nssm.exe`的速度过于慢，于是手动下载替换即可（本来就`360K`也不大
``` bash
C:\Windows\system32>hb-service install
i Installing Homebridge Service
i Creating Homebridge directory: C:\Users\yuangezhizao\.homebridge
i Creating default config.json: C:\Users\yuangezhizao\.homebridge\config.json
i Downloading NSSM from https://github.com/oznu/nssm/releases/download/2.24-101-g897c7ad/nssm_x64.exe
^C终止批处理操作吗(Y/N)? Y
```
![NSSM](https://i1.yuangezhizao.cn/Win-10/20200414205453.jpg!webp)

``` bash
C:\Windows\system32>hb-service install
i Installing Homebridge Service
i Starting Homebridge Service...
√ Homebridge Started

Manage Homebridge by going to one of the following in your browser:

* http://localhost:8581
* http://192.168.25.248:8581
* http://[240e:<rm>:d]:8581

Default Username: admin
Default Password: admin

√ Homebridge Setup Complete

C:\Windows\system32>
```
然后就可以去登录了

![登录](https://i1.yuangezhizao.cn/Win-10/20200406130646.jpg!webp)
![首页](https://i1.yuangezhizao.cn/Win-10/20200406130758.png!webp)
![配置](https://i1.yuangezhizao.cn/Win-10/20200406130830.jpg!webp)
![插件](https://i1.yuangezhizao.cn/Win-10/20200406130959.jpg!webp)

## 0x03.安装[homebridge-homeassistant](https://github.com/home-assistant/homebridge-homeassistant)
同样是个`npm`的`package`
``` bash
C:\Windows\system32>npm install homebridge-homeassistant -g
npm WARN deprecated homebridge-homeassistant@3.1.0: Home Assistant 0.64 and above features native HomeKit support, use that instead of homebridge-homeassistant. More info: https://bit.ly/2Q8o9nm
npm WARN deprecated request@2.88.2: request has been deprecated, see https://github.com/request/request/issues/3142
+ homebridge-homeassistant@3.1.0
added 53 packages from 60 contributors in 104.599s
```
安装之后才发现原来已经不推荐使用了，因为`Home Assistant`已经内置`HomeKit`了
![DEPRECATED](https://i1.yuangezhizao.cn/Win-10/20200406132150.jpg!webp)
![草](https://i1.yuangezhizao.cn/Win-10/20191016005155.jpg!webp)

草，立即卸载
``` bash
Microsoft Windows [版本 10.0.17763.1131]
(c) 2018 Microsoft Corporation。保留所有权利。

C:\Windows\system32>hb-service stop
i Stopping Homebridge Service...
√ Homebridge Stopped

C:\Windows\system32>hb-service uninstall
i Removing Homebridge Service
i Stopping Homebridge Service...
× Failed to stop Homebridge
√ Removed Homebridge Service

C:\Windows\system32>
```
## 0x04.后记
于是就去开启`HA`自带的`HomeKit`了……

> 至此本文使命完成
