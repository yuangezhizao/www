---
title: 基于 OpenCV.js 的人脸检测与识别
date: 2019-5-16 18:43:13
tags:
  - OpenCV
  - OpenCV.js
count: 1
os: 0
os_1: 10.0.17763.475 2019-LTSC
browser: 0
browser_1: 72.0.3626.121 Stable
place: 家
key: 52
---
    昨天晚上突然收到导师催促上交论文的消息，立即开工！
<!-- more -->

## 0x00.[emsdk](https://github.com/juj/emsdk)
官网：https://emscripten.org/
安装教程：https://emscripten.org/docs/getting_started/downloads.html
> `Emscripten`，一款`LLVM-to-JavaScript`的编译器，将`C++`的底层函数编译成可以直接在浏览器端运行的`asm.js`或者`WebAssembly`。而`OpenCV.js`是通过该`Emscripten`将`OpenCV`的函数编译进`asm.js`或`WebAssembly`中，并提供`JS APIs`给`web`应用使用。

> `Emscripten`可以把`C/C++`程序编译成`asm.js`，然后通过`binaryen`的`asm2wasm`转成`WebAssembly`。

``` bash
[root@CentOS ~]# git clone https://github.com/juj/emsdk.git
Cloning into 'emsdk'...
remote: Enumerating objects: 6, done.
remote: Counting objects: 100% (6/6), done.
remote: Compressing objects: 100% (4/4), done.
remote: Total 1327 (delta 1), reused 3 (delta 1), pack-reused 1321
Receiving objects: 100% (1327/1327), 668.22 KiB | 0 bytes/s, done.
Resolving deltas: 100% (840/840), done.
```
``` bash
[root@CentOS ~]# cd emsdk
```
``` bash
[root@CentOS emsdk]# ./emsdk update-tags
Fetching all tags from Emscripten Github repository...
Done. 159 tagged releases available, latest is 1.38.31.
Fetching all tags from Binaryen Github repository...
Done. 86 tagged Binaryen releases available, latest is 1.38.31.
Fetching all precompiled tagged releases..
Downloading: /root/emsdk/llvm-tags-32bit.txt from https://s3.amazonaws.com/mozilla-games/emscripten/packages/llvm/tag/linux_32bit/index.txt
Downloading: /root/emsdk/llvm-tags-64bit.txt from https://s3.amazonaws.com/mozilla-games/emscripten/packages/llvm/tag/linux_64bit/index.txt, 2379 Bytes
Downloading: /root/emsdk/upstream/lkgr.json from https://storage.googleapis.com/wasm-llvm/builds/linux/lkgr.json, 4414 Bytes
[root@CentOS emsdk]# ./emsdk install latest
Installing SDK 'sdk-1.38.31-64bit'..
Installing tool 'clang-e1.38.31-64bit'..
Downloading: /root/emsdk/zips/emscripten-llvm-e1.38.31.tar.gz from https://s3.amazonaws.com/mozilla-games/emscripten/packages/llvm/tag/linux_64bit/emscripten-llvm-e1.38.31.tar.gz, 392225846 Bytes
Unpacking '/root/emsdk/zips/emscripten-llvm-e1.38.31.tar.gz' to '/root/emsdk/clang/e1.38.31_64bit'
Done installing tool 'clang-e1.38.31-64bit'.
Installing tool 'node-8.9.1-64bit'..
Downloading: /root/emsdk/zips/node-v8.9.1-linux-x64.tar.xz from https://s3.amazonaws.com/mozilla-games/emscripten/packages/node-v8.9.1-linux-x64.tar.xz, 11387108 Bytes
Unpacking '/root/emsdk/zips/node-v8.9.1-linux-x64.tar.xz' to '/root/emsdk/node/8.9.1_64bit'
Done installing tool 'node-8.9.1-64bit'.
Installing tool 'emscripten-1.38.31'..
Downloading: /root/emsdk/zips/1.38.31.tar.gz from https://github.com/kripken/emscripten/archive/1.38.31.tar.gz
Unpacking '/root/emsdk/zips/1.38.31.tar.gz' to '/root/emsdk/emscripten/1.38.31'
Done installing tool 'emscripten-1.38.31'.
Done installing SDK 'sdk-1.38.31-64bit'.
```
``` bash
[root@CentOS emsdk]# ./emsdk activate latest
Writing .emscripten configuration file to user home directory /root/
The Emscripten configuration file /root/.emscripten has been rewritten with the following contents:

import os
LLVM_ROOT = '/root/emsdk/clang/e1.38.31_64bit'
EMSCRIPTEN_NATIVE_OPTIMIZER = '/root/emsdk/clang/e1.38.31_64bit/optimizer'
BINARYEN_ROOT = '/root/emsdk/clang/e1.38.31_64bit/binaryen'
NODE_JS = '/root/emsdk/node/8.9.1_64bit/bin/node'
EMSCRIPTEN_ROOT = '/root/emsdk/emscripten/1.38.31'
SPIDERMONKEY_ENGINE = ''
V8_ENGINE = ''
TEMP_DIR = '/tmp'
COMPILER_ENGINE = NODE_JS
JS_ENGINES = [NODE_JS]

To conveniently access the selected set of tools from the command line, consider adding the following directories to PATH, or call 'source ./emsdk_env.sh' to do this for you.

   /root/emsdk:/root/emsdk/clang/e1.38.31_64bit:/root/emsdk/node/8.9.1_64bit/bin:/root/emsdk/emscripten/1.38.31
Set the following tools as active:
   clang-e1.38.31-64bit
   node-8.9.1-64bit
   emscripten-1.38.31

```
``` bash
[root@CentOS emsdk]# source ./emsdk_env.sh
Adding directories to PATH:
PATH += /root/emsdk
PATH += /root/emsdk/clang/e1.38.31_64bit
PATH += /root/emsdk/node/8.9.1_64bit/bin
PATH += /root/emsdk/emscripten/1.38.31

Setting environment variables:
EMSDK = /root/emsdk
EM_CONFIG = /root/.emscripten
LLVM_ROOT = /root/emsdk/clang/e1.38.31_64bit
EMSCRIPTEN_NATIVE_OPTIMIZER = /root/emsdk/clang/e1.38.31_64bit/optimizer
BINARYEN_ROOT = /root/emsdk/clang/e1.38.31_64bit/binaryen
EMSDK_NODE = /root/emsdk/node/8.9.1_64bit/bin/node
EMSCRIPTEN = /root/emsdk/emscripten/1.38.31

```
## 0x01.[OpenCV.js](https://docs.opencv.org/master/df/d0a/tutorial_js_intro.html)
> 随着`HTML5`的兴起，在`web`端使用图像处理相关技术显得尤为重要，`OpenCV.js`为`Javascript`开发者与`OpenCV`之间搭建了桥梁。起初是由`Intel`公司发起的一项研究，后在`2017`年并入到`OpenCV`项目中。

官方示例页面：[Face Detection in Video Capture](https://docs.opencv.org/master/df/d6c/tutorial_js_face_detection_camera.html)
安装教程：https://docs.opencv.org/master/d4/da1/tutorial_js_setup.html
这就是最终效果，其实直接从这里拿应该也可以的（逃……
``` bash
[root@CentOS ~]# git clone https://github.com/opencv/opencv.git
Cloning into 'opencv'...
remote: Enumerating objects: 2, done.
remote: Counting objects: 100% (2/2), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 253493 (delta 0), reused 0 (delta 0), pack-reused 253491
Receiving objects: 100% (253493/253493), 457.97 MiB | 7.13 MiB/s, done.
Resolving deltas: 100% (176963/176963), done.
Checking out files: 100% (5847/5847), done.
```
> 默认是编译成`asm.js`版本，如果需要编译成`WebAssembly`的版本，加上后缀`--build_wasm`

``` bash
[root@CentOS opencv]# python ./platforms/js/build_js.py build_wasm --build_wasm
Args: Namespace(build_dir='build_wasm', build_doc=False, build_test=False, build_wasm=True, clean_build_dir=False, config_only=False, disable_wasm=False, emscripten_dir='/root/emsdk/emscripten/1.38.31', enable_exception=False, opencv_dir='/root/opencv', skip_config=False)
Check dir /root/opencv/build_wasm (create: True, clean: False)
Check dir /root/opencv (create: False, clean: False)
Check dir /root/emsdk/emscripten/1.38.31 (create: False, clean: False)
=====
===== Config OpenCV.js build for wasm
=====
Executing: ['cmake', '-DCMAKE_BUILD_TYPE=Release', "-DCMAKE_TOOLCHAIN_FILE='/root/emsdk/emscripten/1.38.31/cmake/Modules/Platform/Emscripten.cmake'", "-DCPU_BASELINE=''", "-DCPU_DISPATCH=''", '-DCV_TRACE=OFF', '-DBUILD_SHARED_LIBS=OFF', '-DWITH_1394=OFF', '-DWITH_ADE=OFF', '-DWITH_VTK=OFF', '-DWITH_EIGEN=OFF', '-DWITH_FFMPEG=OFF', '-DWITH_GSTREAMER=OFF', '-DWITH_GTK=OFF', '-DWITH_GTK_2_X=OFF', '-DWITH_IPP=OFF', '-DWITH_JASPER=OFF', '-DWITH_JPEG=OFF', '-DWITH_WEBP=OFF', '-DWITH_OPENEXR=OFF', '-DWITH_OPENGL=OFF', '-DWITH_OPENVX=OFF', '-DWITH_OPENNI=OFF', '-DWITH_OPENNI2=OFF', '-DWITH_PNG=OFF', '-DWITH_TBB=OFF', '-DWITH_PTHREADS_PF=OFF', '-DWITH_TIFF=OFF', '-DWITH_V4L=OFF', '-DWITH_OPENCL=OFF', '-DWITH_OPENCL_SVM=OFF', '-DWITH_OPENCLAMDFFT=OFF', '-DWITH_OPENCLAMDBLAS=OFF', '-DWITH_GPHOTO2=OFF', '-DWITH_LAPACK=OFF', '-DWITH_ITT=OFF', '-DWITH_QUIRC=OFF', '-DBUILD_ZLIB=ON', '-DBUILD_opencv_apps=OFF', '-DBUILD_opencv_calib3d=ON', '-DBUILD_opencv_dnn=ON', '-DBUILD_opencv_features2d=ON', '-DBUILD_opencv_flann=ON', '-DBUILD_opencv_gapi=OFF', '-DBUILD_opencv_ml=OFF', '-DBUILD_opencv_photo=ON', '-DBUILD_opencv_imgcodecs=OFF', '-DBUILD_opencv_shape=OFF', '-DBUILD_opencv_videoio=OFF', '-DBUILD_opencv_videostab=OFF', '-DBUILD_opencv_highgui=OFF', '-DBUILD_opencv_superres=OFF', '-DBUILD_opencv_stitching=OFF', '-DBUILD_opencv_java=OFF', '-DBUILD_opencv_java_bindings_generator=OFF', '-DBUILD_opencv_js=ON', '-DBUILD_opencv_python2=OFF', '-DBUILD_opencv_python3=OFF', '-DBUILD_opencv_python_bindings_generator=OFF', '-DBUILD_EXAMPLES=OFF', '-DBUILD_PACKAGE=OFF', '-DBUILD_TESTS=OFF', '-DBUILD_PERF_TESTS=OFF', '-DBUILD_DOCS=OFF', "-DCMAKE_C_FLAGS='-s WASM=1 '", "-DCMAKE_CXX_FLAGS='-s WASM=1 '", '/root/opencv']
Traceback (most recent call last):
  File "./platforms/js/build_js.py", line 227, in <module>
    builder.config()
  File "./platforms/js/build_js.py", line 167, in config
    execute(cmd)
  File "./platforms/js/build_js.py", line 25, in execute
    raise Fail("Execution failed: %d / %s" % (e.errno, e.strerror))
__main__.Fail: Execution failed: 13 / Permission denied
```
``` bash
[root@CentOS opencv]# python -V
Python 2.7.5
```
``` bash
yum install cmake
```
``` bash
[root@CentOS opencv]# python ./platforms/js/build_js.py build_wasm --build_wasm --emscripten_dir=/root/emsdk
Args: Namespace(build_dir='build_wasm', build_doc=False, build_test=False, build_wasm=True, clean_build_dir=False, config_only=False, disable_wasm=False, emscripten_dir='/root/emsdk', enable_exception=False, opencv_dir='/root/opencv', skip_config=False)
Check dir /root/opencv/build_wasm (create: True, clean: False)
Check dir /root/opencv (create: False, clean: False)
Check dir /root/emsdk (create: False, clean: False)
=====
===== Config OpenCV.js build for wasm
=====
Executing: ['cmake', '-DCMAKE_BUILD_TYPE=Release', "-DCMAKE_TOOLCHAIN_FILE='/root/emsdk/cmake/Modules/Platform/Emscripten.cmake'", "-DCPU_BASELINE=''", "-DCPU_DISPATCH=''", '-DCV_TRACE=OFF', '-DBUILD_SHARED_LIBS=OFF', '-DWITH_1394=OFF', '-DWITH_ADE=OFF', '-DWITH_VTK=OFF', '-DWITH_EIGEN=OFF', '-DWITH_FFMPEG=OFF', '-DWITH_GSTREAMER=OFF', '-DWITH_GTK=OFF', '-DWITH_GTK_2_X=OFF', '-DWITH_IPP=OFF', '-DWITH_JASPER=OFF', '-DWITH_JPEG=OFF', '-DWITH_WEBP=OFF', '-DWITH_OPENEXR=OFF', '-DWITH_OPENGL=OFF', '-DWITH_OPENVX=OFF', '-DWITH_OPENNI=OFF', '-DWITH_OPENNI2=OFF', '-DWITH_PNG=OFF', '-DWITH_TBB=OFF', '-DWITH_PTHREADS_PF=OFF', '-DWITH_TIFF=OFF', '-DWITH_V4L=OFF', '-DWITH_OPENCL=OFF', '-DWITH_OPENCL_SVM=OFF', '-DWITH_OPENCLAMDFFT=OFF', '-DWITH_OPENCLAMDBLAS=OFF', '-DWITH_GPHOTO2=OFF', '-DWITH_LAPACK=OFF', '-DWITH_ITT=OFF', '-DWITH_QUIRC=OFF', '-DBUILD_ZLIB=ON', '-DBUILD_opencv_apps=OFF', '-DBUILD_opencv_calib3d=ON', '-DBUILD_opencv_dnn=ON', '-DBUILD_opencv_features2d=ON', '-DBUILD_opencv_flann=ON', '-DBUILD_opencv_gapi=OFF', '-DBUILD_opencv_ml=OFF', '-DBUILD_opencv_photo=ON', '-DBUILD_opencv_imgcodecs=OFF', '-DBUILD_opencv_shape=OFF', '-DBUILD_opencv_videoio=OFF', '-DBUILD_opencv_videostab=OFF', '-DBUILD_opencv_highgui=OFF', '-DBUILD_opencv_superres=OFF', '-DBUILD_opencv_stitching=OFF', '-DBUILD_opencv_java=OFF', '-DBUILD_opencv_java_bindings_generator=OFF', '-DBUILD_opencv_js=ON', '-DBUILD_opencv_python2=OFF', '-DBUILD_opencv_python3=OFF', '-DBUILD_opencv_python_bindings_generator=OFF', '-DBUILD_EXAMPLES=OFF', '-DBUILD_PACKAGE=OFF', '-DBUILD_TESTS=OFF', '-DBUILD_PERF_TESTS=OFF', '-DBUILD_DOCS=OFF', "-DCMAKE_C_FLAGS='-s WASM=1 '", "-DCMAKE_CXX_FLAGS='-s WASM=1 '", '/root/opencv']
Re-run cmake no build system arguments
CMake Error at CMakeLists.txt:29 (cmake_minimum_required):
  CMake 3.5.1 or higher is required.  You are running version 2.8.12.2


-- Configuring incomplete, errors occurred!
Traceback (most recent call last):
  File "./platforms/js/build_js.py", line 227, in <module>
    builder.config()
  File "./platforms/js/build_js.py", line 167, in config
    execute(cmd)
  File "./platforms/js/build_js.py", line 23, in execute
    raise Fail("Child returned: %s" % retcode)
__main__.Fail: Child returned: 1
```
`emmm`
``` bash
[root@CentOS opencv]# cmake
cmake version 2.8.12.2
```
溜了溜了
停电了`XD`，未完待续……

## 0x02.引用
> [OpenCV.js 入门](https://github.com/allenGKC/Blog/issues/9)
  [用OpenCV在浏览器进行人脸检测](https://segmentfault.com/a/1190000014639145)
