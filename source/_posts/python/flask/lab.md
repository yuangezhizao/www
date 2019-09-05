---
title: 实验室站 Python 3.7.2 + Flask 1.0.2 + mod_wsgi 4.6.5 + Apache 2.4.38 + HTTP/2 + TLSv1.3 + brotli
date: 2019-2-11 22:23:09
tags:
  - Flask
  - Apache24
  - mod_wsgi
  - TLSv1.3
count: 1
os: 0
os_1: 10.0.17763.292 2019-LTSC
browser: 0
browser_1: 71.0.3578.98 Stable
place: 家
key: 42
---
    又开始折腾升级了……
<!-- more -->
## 0x00.前言
看见[esterTion](https://weibo.com/lcz970)大佬的[BiliPlus](https://www.biliplus.com)上了`TLSv1.3`，正巧[实验室](https://lab.yuangezhizao.cn/)站证书也快一年该续签了，于是大折腾开始了

## 0x01.[Python](https://www.python.org/)
今天先把本地配好了`2.7.15`、`3.6.8`、`3.7.2`、`3.8.0a1`，版本的选择靠`环境变量`的先后顺序决定，`PyCharm`里倒是可以单独选择
![与官网相同步](https://i1.yuangezhizao.cn/Win-10/20190211223934.jpg!webp)
![py 骨灰级玩家](https://i1.yuangezhizao.cn/Win-10/20190211223414.jpg!webp)

然后服务器是腾讯云的一元机
![16 年购买的](https://i1.yuangezhizao.cn/Win-10/20190211224146.jpg!webp)

想想从零开始也快折腾了三年了，现在想想还是有必要有一台`Windows Server 2012 R2 Database x64`（救急）使用的，当然现在`Linux`也算熟悉了，所以后续再购买服务器就打算使用`CentOS`了，因为最近**白嫖**到了一台时长**一年**的`Ubuntu 18.04`（据说我发现的第二天一刀套餐就木有了），目前搭了`V2ray`代理，这个之后单独再写……
![月 500 GB 是真的用不完](https://i1.yuangezhizao.cn/Win-10/20190211224830.jpg!webp)
![云端有俩更新莫名安装不上](https://i1.yuangezhizao.cn/Win-10/20190211225826.jpg!webp)
![先不管了](https://i1.yuangezhizao.cn/Win-10/20190211230018.jpg!webp)

云端只安装了`3.6.8`、`3.7.2`是因为`2`不打算再用了，本地配`2`是因为部分`gh`的旧项目以及[jd-tools](https://github.com/gogodick/jd-tools)，不过它是在[Cygwin](https://www.cygwin.com/)倒是不受影响……本地配`3.8.0a1`是因为要~~达成成就~~看一看最新版本的特性……云端是要逐步从`3.6.8`迁移至`3.7.2`，根据[Stack Overflow
](https://stackoverflow.com)的这个回答[How to run celery on windows?](https://stackoverflow.com/questions/37255548/how-to-run-celery-on-windows/47331438#47331438)
![3.1.25](https://i1.yuangezhizao.cn/Win-10/20190211231300.jpg!webp)
![我一直用的就是 eventlet](https://i1.yuangezhizao.cn/Win-10/20190211231937.jpg!webp)

所以为了[Celery](http://www.celeryproject.org/)还是留两个版本吧，顺便准备把`pipenv`也补上……
![刚把 server 上的 py 升级完就突然又不想搞了……](https://i1.yuangezhizao.cn/Win-10/20190212000036.jpg!webp)

还是惯例配好`pipy`阿里云镜像，升级`pip`

## 0x01.[Apache24](https://httpd.apache.org/)
![Download](https://i1.yuangezhizao.cn/Win-10/20190212111352.jpg!webp)
![Files for Microsoft Windows](https://i1.yuangezhizao.cn/Win-10/20190212111454.jpg!webp)
![windows](https://i1.yuangezhizao.cn/Win-10/20190212111542.jpg!webp)

我个人使用的就是第一个，有`br`压缩，第二个木有……虽然第一个是`VC14`，第二个是`VC15`……
![apachehaus](https://i1.yuangezhizao.cn/Win-10/20190212111752.jpg!webp)

下载这个`11.9 MB`大小的`httpd-2.4.38-o111a-x64-vc14.zip`，含有`with OpenSSL 1.1.1a, brotli 1.0.7, nghttp 1.36.0, Zlib 1.2.10, PCRE 8.42, APR 1.6.5, APR-Util 1.6.1`，虽然有`LibreSSL`版本以及`OpenSSL 1.0.2`、`OpenSSL 1.1.0`，但是我还是选择了这个，并不是下载量第一的`1.0.2`，
![apachelounge](https://i1.yuangezhizao.cn/Win-10/20190212124746.jpg!webp)

`VC15`
![wamp](https://i1.yuangezhizao.cn/Win-10/20190212124919.jpg!webp)

`bitnami`的这个是一个`PHP`大软件环境……

![WAMPSERVER](https://i1.yuangezhizao.cn/Win-10/20190212125227.jpg!webp)

玩具？

![XAMPP](https://i1.yuangezhizao.cn/Win-10/20190212125256.jpg!webp)

只有`32`位的还是算了吧……

### 修改配置文件：
#### `/extra/httpd.ahssl.conf`
注释掉这个日志：
``` bash
#   Per-Server Logging:
#   The home of a custom SSL log file. Use this when you want a
#   compact non-error SSL logfile on a virtual host basis.
CustomLog "${SRVROOT}/logs/ssl_request.log" \
          "%t %h %{SSL_PROTOCOL}x %{SSL_CIPHER}x \"%r\" %b" env=HTTPS
```
增加
``` bash
<VirtualHost *:443>
    Protocols h2 http/1.1

    SSLEngine on
    ServerName lab.yuangezhizao.cn
    SSLCertificateFile "${SRVROOT}/conf/ssl/2_lab.yuangezhizao.cn.crt"
    SSLCertificateKeyFile "${SRVROOT}/conf/ssl/3_lab.yuangezhizao.cn.key"
    SSLCertificateChainFile "${SRVROOT}/conf/ssl/1_root_bundle.crt"
    DocumentRoot C:\LAB

    Header always set Strict-Transport-Security "max-age=60"
    Header always set X-XSS-Protection "1; mode=block"
    Header always set x-content-type-options nosniff
    Header always set X-Frame-Options SAMEORIGIN

    WSGIScriptAlias / C:\LAB\wsgi.py

    <Directory C:\LAB>
        WSGIScriptReloading On
        Require all granted
        Require host ip
    </Directory>
</VirtualHost>
```
#### `/extra/httpd.info.conf`
``` bash
<Location /server-status>
    SetHandler server-status
    AuthName "server-status"
    AuthType Basic
    AuthUserFile "${SRVROOT}/bin/.htpasswd"
    require user yuangezhizao
</Location>
```
取消注释：
``` bash
ExtendedStatus On
```
``` bash
<Location /server-info>
    SetHandler server-info
    # AuthBasicFake yuangezhizao <password>
    # Require host lab.yuangezhizao.cn
    # Require ip 61.161
    AuthName "server-info"
    AuthType Basic
    AuthUserFile "${SRVROOT}/bin/.htpasswd"
    require user yuangezhizao
</Location>
```
`AuthBasicFake`莫名不好使，所以只能采用`AuthType Basic`了……
#### `/extra/httpd.vhosts.conf`
``` bash
<VirtualHost *:80>
    RewriteEngine On
    RewriteRule ^(.*)$ https://%{HTTP_HOST}$1 [R,L]
</VirtualHost>    
```
`80`强制跳转`443`

``` bash
<VirtualHost *:80>
    DocumentRoot C:\Apache24\webui-aria2
    DirectoryIndex  index.html
    ServerName aria2.yuangezhizao.cn

    <Directory C:\Apache24\webui-aria2>
    	Require all granted
    </Directory>
</VirtualHost>

<VirtualHost *:80>
    DocumentRoot C:\Apache24\status-page
    DirectoryIndex  index.html
    ServerName status.yuangezhizao.cn

    <Directory C:\Apache24\status-page>
    	Require all granted
    </Directory>
</VirtualHost>
```
#### `/httpd.conf`
终于到了根配置文件了，可以看到`Define ENABLE_TLS13 "Yes"`就是`TLSv1.3`
增加`LoadModule brotli_module modules/mod_brotli.so`，取消注释`LoadModule expires_module modules/mod_expires.so`，取消注释
``` bash
LoadModule filter_module modules/mod_filter.so
LoadModule headers_module modules/mod_headers.so
```
取消注释`LoadModule http2_module modules/mod_http2.so`，
取消注释`LoadModule proxy_module modules/mod_proxy.so`、`LoadModule proxy_http_module modules/mod_proxy_http.so`备用，
取消注释`LoadModule rewrite_module modules/mod_rewrite.so`，
取消注释`LoadModule vhost_alias_module modules/mod_vhost_alias.so`，
增加`LoadModule wsgi_module modules/mod_wsgi.cp37-win_amd64.pyd`，
修改`ServerAdmin root@yuangezhizao.cn`、`ServerName lab.yuangezhizao.cn`，
取消注释`Include conf/extra/httpd-vhosts.conf`、`Include conf/extra/httpd-default.conf`，
最后是`br`压缩：
``` bash
<IfModule brotli_module>
SetOutputFilter BROTLI_COMPRESS
# DEFLATE
# DeflateCompressionLevel 3
SetEnvIfNoCase Request_URI .(?:gif|jpe?g|png)$ no-brotli dont-vary
SetEnvIfNoCase Request_URI .(?:exe|t?gz|zip|bz2|sit|rar)$ no-brotli dont-vary
SetEnvIfNoCase Request_URI .(?:pdf|doc|avi|mov|mp3|rm)$ no-brotli dont-vary
AddOutputFilterByType BROTLI_COMPRESS text/html text/plain text/xml text/css
AddOutputFilterByType BROTLI_COMPRESS text/javascript application/javascript application/x-javascript
AddOutputFilterByType BROTLI_COMPRESS application/json
</IfModule>
```

## 0x02.[mod_wsgi](https://github.com/GrahamDumpleton/mod_wsgi)
`Latest release`是`mod_wsgi-4.6.5`版本，
![巧了，我没下这个版本的](https://i1.yuangezhizao.cn/Win-10/20190212153434.jpg!webp)

尝试安装
```
(LAB-HVyfm2Bd) D:\yuangezhizao\Documents\PycharmProjects\LAB>pipenv install mod_wsgi
Installing mod_wsgi…
Looking in indexes: https://pypi.python.org/simple
Collecting mod_wsgi
  Downloading https://files.pythonhosted.org/packages/47/69/5139588686eb40053f8355eba1fe18a8bee94dc3efc4e36720c73e07471a/mod_wsgi-4.6.5.tar.gz (490kB)
    Complete output from command python setup.py egg_info:
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
      File "C:\Users\YUANGE~1\AppData\Local\Temp\pip-install-aabgv042\mod-wsgi\setup.py", line 158, in <module>
        raise RuntimeError('No Apache installation can be found. Set the '
    RuntimeError: No Apache installation can be found. Set the MOD_WSGI_APACHE_ROOTDIR environment to its location.
    
    ----------------------------------------

Error:  An error occurred while installing mod_wsgi!
Command "python setup.py egg_info" failed with error code 1 in C:\Users\YUANGE~1\AppData\Local\Temp\pip-install-aabgv042\mod-wsgi\
```
哦，设定环境变量
```
(LAB-HVyfm2Bd) D:\yuangezhizao\Documents\PycharmProjects\LAB>SET MOD_WSGI_APACHE_ROOTDIR=D:\Apache24
```
```
(LAB-HVyfm2Bd) D:\yuangezhizao\Documents\PycharmProjects\LAB>pipenv install mod_wsgi
Installing mod_wsgi…
Looking in indexes: https://pypi.python.org/simple
Collecting mod_wsgi
  Using cached https://files.pythonhosted.org/packages/47/69/5139588686eb40053f8355eba1fe18a8bee94dc3efc4e36720c73e07471a/mod_wsgi-4.6.5.tar.gz
Building wheels for collected packages: mod-wsgi
  Building wheel for mod-wsgi (setup.py): started
  Building wheel for mod-wsgi (setup.py): still running...
  Building wheel for mod-wsgi (setup.py): finished with status 'error'
  Complete output from command c:\users\yuangezhizao\.virtualenvs\lab-hvyfm2bd\scripts\python.exe -u -c "import setuptools, tokenize;__file__='C:\\Users\\YUANGE~1\\AppData\\Lo
cal\\Temp\\pip-install-48e8tnl_\\mod-wsgi\\setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'ex
ec'))" bdist_wheel -d C:\Users\YUANGE~1\AppData\Local\Temp\pip-wheel-z03h3fox --python-tag cp38:
  C:\Python38\Lib\distutils\dist.py:274: UserWarning: Unknown distribution option: 'bugtrack_url'
    warnings.warn(msg)
  running bdist_wheel
  running build
  running build_py
  creating build
  creating build\lib.win-amd64-3.8
  creating build\lib.win-amd64-3.8\mod_wsgi
  copying src\__init__.py -> build\lib.win-amd64-3.8\mod_wsgi
  creating build\lib.win-amd64-3.8\mod_wsgi\server
  copying src\server\apxs_config.py -> build\lib.win-amd64-3.8\mod_wsgi\server
  copying src\server\environ.py -> build\lib.win-amd64-3.8\mod_wsgi\server
  copying src\server\__init__.py -> build\lib.win-amd64-3.8\mod_wsgi\server
  creating build\lib.win-amd64-3.8\mod_wsgi\server\management
  copying src\server\management\__init__.py -> build\lib.win-amd64-3.8\mod_wsgi\server\management
  creating build\lib.win-amd64-3.8\mod_wsgi\server\management\commands
  copying src\server\management\commands\runmodwsgi.py -> build\lib.win-amd64-3.8\mod_wsgi\server\management\commands
  copying src\server\management\commands\__init__.py -> build\lib.win-amd64-3.8\mod_wsgi\server\management\commands
  creating build\lib.win-amd64-3.8\mod_wsgi\docs
  copying docs\_build\html\__init__.py -> build\lib.win-amd64-3.8\mod_wsgi\docs
  creating build\lib.win-amd64-3.8\mod_wsgi\images
  copying images\__init__.py -> build\lib.win-amd64-3.8\mod_wsgi\images
  copying images\snake-whiskey.jpg -> build\lib.win-amd64-3.8\mod_wsgi\images
  running build_ext
  building 'mod_wsgi.server.mod_wsgi' extension
  creating build\temp.win-amd64-3.8
  creating build\temp.win-amd64-3.8\Release
  creating build\temp.win-amd64-3.8\Release\src
  creating build\temp.win-amd64-3.8\Release\src\server
  C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Tools\MSVC\14.16.27023\bin\HostX86\x64\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -ID:\Apache24/include -IC:
\Python38\include -IC:\Python38\include "-IC:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Tools\MSVC\14.16.27023\ATLMFC\include" "-IC:\Program Files (x86)\Mi
crosoft Visual Studio\2017\Community\VC\Tools\MSVC\14.16.27023\include" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.17763.0\ucrt" "-IC:\Program Files (x86)\Windows
Kits\10\include\10.0.17763.0\shared" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.17763.0\um" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.17763.0\winrt" "
-IC:\Program Files (x86)\Windows Kits\10\include\10.0.17763.0\cppwinrt" /Tcsrc/server\mod_wsgi.c /Fobuild\temp.win-amd64-3.8\Release\src/server\mod_wsgi.obj
  mod_wsgi.c
  d:\apache24\include\apr_network_io.h(29): fatal error C1083: 无法打开包括文件: “apr_perms_set.h”: No such file or directory
  error: command 'C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Tools\\MSVC\\14.16.27023\\bin\\HostX86\\x64\\cl.exe' failed with exit status 2
  
  ----------------------------------------
  Running setup.py clean for mod-wsgi
Failed to build mod-wsgi
Installing collected packages: mod-wsgi
  Running setup.py install for mod-wsgi: started
    Running setup.py install for mod-wsgi: still running...
    Running setup.py install for mod-wsgi: finished with status 'error'
    Complete output from command c:\users\yuangezhizao\.virtualenvs\lab-hvyfm2bd\scripts\python.exe -u -c "import setuptools, tokenize;__file__='C:\\Users\\YUANGE~1\\AppData\\
Local\\Temp\\pip-install-48e8tnl_\\mod-wsgi\\setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, '
exec'))" install --record C:\Users\YUANGE~1\AppData\Local\Temp\pip-record-h7vjkitd\install-record.txt --single-version-externally-managed --compile --install-headers c:\users\
yuangezhizao\.virtualenvs\lab-hvyfm2bd\include\site\python3.8\mod-wsgi:
    C:\Python38\Lib\distutils\dist.py:274: UserWarning: Unknown distribution option: 'bugtrack_url'
      warnings.warn(msg)
    running install
    running build
    running build_py
    creating build
    creating build\lib.win-amd64-3.8
    creating build\lib.win-amd64-3.8\mod_wsgi
    copying src\__init__.py -> build\lib.win-amd64-3.8\mod_wsgi
    creating build\lib.win-amd64-3.8\mod_wsgi\server
    copying src\server\apxs_config.py -> build\lib.win-amd64-3.8\mod_wsgi\server
    copying src\server\environ.py -> build\lib.win-amd64-3.8\mod_wsgi\server
    copying src\server\__init__.py -> build\lib.win-amd64-3.8\mod_wsgi\server
    creating build\lib.win-amd64-3.8\mod_wsgi\server\management
    copying src\server\management\__init__.py -> build\lib.win-amd64-3.8\mod_wsgi\server\management
    creating build\lib.win-amd64-3.8\mod_wsgi\server\management\commands
    copying src\server\management\commands\runmodwsgi.py -> build\lib.win-amd64-3.8\mod_wsgi\server\management\commands
    copying src\server\management\commands\__init__.py -> build\lib.win-amd64-3.8\mod_wsgi\server\management\commands
    creating build\lib.win-amd64-3.8\mod_wsgi\docs
    copying docs\_build\html\__init__.py -> build\lib.win-amd64-3.8\mod_wsgi\docs
    creating build\lib.win-amd64-3.8\mod_wsgi\images
    copying images\__init__.py -> build\lib.win-amd64-3.8\mod_wsgi\images
    copying images\snake-whiskey.jpg -> build\lib.win-amd64-3.8\mod_wsgi\images
    running build_ext
    building 'mod_wsgi.server.mod_wsgi' extension
    creating build\temp.win-amd64-3.8
    creating build\temp.win-amd64-3.8\Release
    creating build\temp.win-amd64-3.8\Release\src
    creating build\temp.win-amd64-3.8\Release\src\server
    C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Tools\MSVC\14.16.27023\bin\HostX86\x64\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -ID:\Apache24/include -I
C:\Python38\include -IC:\Python38\include "-IC:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Tools\MSVC\14.16.27023\ATLMFC\include" "-IC:\Program Files (x86)\
Microsoft Visual Studio\2017\Community\VC\Tools\MSVC\14.16.27023\include" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.17763.0\ucrt" "-IC:\Program Files (x86)\Window
s Kits\10\include\10.0.17763.0\shared" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.17763.0\um" "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.17763.0\winrt"
 "-IC:\Program Files (x86)\Windows Kits\10\include\10.0.17763.0\cppwinrt" /Tcsrc/server\mod_wsgi.c /Fobuild\temp.win-amd64-3.8\Release\src/server\mod_wsgi.obj
    mod_wsgi.c
    d:\apache24\include\apr_network_io.h(29): fatal error C1083: 无法打开包括文件: “apr_perms_set.h”: No such file or directory
    error: command 'C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Tools\\MSVC\\14.16.27023\\bin\\HostX86\\x64\\cl.exe' failed with exit status 2
    
    ----------------------------------------

Error:  An error occurred while installing mod_wsgi!
  Failed building wheel for mod-wsgi
Command "c:\users\yuangezhizao\.virtualenvs\lab-hvyfm2bd\scripts\python.exe -u -c "import setuptools, tokenize;__file__='C:\\Users\\YUANGE~1\\AppData\\Local\\Temp\\pip-install
-48e8tnl_\\mod-wsgi\\setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'exec'))" install --recor
d C:\Users\YUANGE~1\AppData\Local\Temp\pip-record-h7vjkitd\install-record.txt --single-version-externally-managed --compile --install-headers c:\users\yuangezhizao\.virtualenv
s\lab-hvyfm2bd\include\site\python3.8\mod-wsgi" failed with error code 1 in C:\Users\YUANGE~1\AppData\Local\Temp\pip-install-48e8tnl_\mod-wsgi\
```
它……自动用`VS2017`编译了……
[Running mod_wsgi on Windows](https://github.com/GrahamDumpleton/mod_wsgi/blob/develop/win32/README.rst)
果然还是不行……
![4.4.12 是最后一个提供了 Windows binaries 的版本](https://i1.yuangezhizao.cn/Win-10/20190212181911.jpg!webp)
![才发现这里有 4.6.5](https://i1.yuangezhizao.cn/Win-10/20190212182403.jpg!webp)

`pip`安装即可，顺便解压找到`mod_wsgi.cp37-win_amd64.pyd`扔到`models`目录里
附上`wgsi.py`文件
``` python
# activate_this = "C:\\Users\\Administrator\\.virtualenvs\\LAB-QaV1et56\\Scripts\\activate_this.py"
# with open(activate_this) as file_:
#    exec(file_.read(), dict(__file__=activate_this))

import sys
import logging

logging.basicConfig(stream=sys.stderr)

# Expand Python classes path with your app's path
sys.path.insert(0, "C:\LAB")

from run import app

# Put logging code (and imports) here ...

# Initialize WSGI app object
application = app
```
## 0x03.后记
未完待续……