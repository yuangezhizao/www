---
title: Win-10 安装 TensorFlow-GPU 1.13.1（Python 3.7.2 + CUDA 10.0 + cuDNN 7.5.0 + TensorRT 5.0.4.3）
date: 2019-3-14 18:16:40
tags:
  - TensorFlow
  - TensorFlow-GPU
count: 2
os: 0
os_1: 10.0.17763.316 2019-LTSC
browser: 0
browser_1: 71.0.3578.98 Stable
place: 图书馆
key: 44
gitment: true
---
    1903 重置 1708 版（就算笔记本是 965M，我也要搞 TF-GPU！）
<!-- more -->
> 原文地址：[Win-10 安装 TensorFlow-GPU](./install-tensorflow-gpu-on-Win-10.html)
  原文作者：远哥制造

## 0x00.缘由
在`2017-8-3 10:25:03`写的[Win-10 安装 TensorFlow-GPU](./install-tensorflow-gpu-on-Win-10.html)被[CSDN](https://web.archive.org/save/https://blog.csdn.net/sinat_36458870/article/details/78783587)上的一位博主引用，这篇文章让我这个小站有了每天的固定个位数访客。正值前几天`TF 2.0`发布（油管直播我他妈熬夜看的`QAQ`），也是时候把这篇文章更新下了，其实早就想了……
唔，还有简书上的这篇[Faster R-CNN for Tensorflow](https://web.archive.org/save/https://www.jianshu.com/p/08c1faa38358)

## 0x01.环境
a. Microsoft Windows [版本 10.0.17763.316]（Win 10 x64 2019-LTSC 1809 17763.316）
b. Python 3.7.2 (tags/v3.7.2:9a3ffc0492, Dec 23 2018, 23:09:28) [MSC v.1916 64 bit (AMD64)] on win32
c. JetBrains Pycharm 2018.3 x64 Professional
d. GeForce GTX 965M

## 0x02.安装
写流水账开始了啊，具体的细节自己去翻那篇吧。
### 1. 去[TF 官网](https://www.tensorflow.org/install/gpu)
![CUDA 9.0](https://i1.yuangezhizao.cn/Win-10/20190314183605.jpg!webp)

卧槽，然后我就被坑了，都下完了突然想到为啥不试试`CUDA 10.0`？可官网没写支持啊？况且在其他地方我也看到了说不支持的，XD……
结果忘了是要装`NVIDIA`的哪个包来着的，要求`CUDA 10.0`，WTF？然后就去谷歌搜了，结果还真搜到了，不过是谷歌快照……
![CUDA 10.0](https://i1.yuangezhizao.cn/Win-10/20190314184040.jpg!webp)

当时就傻逼了，这他妈中英文文档内容居然不一样，中文的更新速度居然这么慢，原来官方都支持`CUDA 10.0`了啊？！
![GPU support](https://i1.yuangezhizao.cn/Win-10/20190314184305.jpg!webp)
![Pip package](https://i1.yuangezhizao.cn/Win-10/20190314184318.jpg!webp)
![Windows setup](https://i1.yuangezhizao.cn/Win-10/20190314184346.jpg!webp)

卧槽，切换按钮在页面最右下角，绝了！
![Windows setup](https://i1.yuangezhizao.cn/Win-10/20190314192253.jpg!webp)

### 2. 安装[CUDA](https://developer.nvidia.com/cuda-downloads)
算力要`3.5`以上才可以，我的是`5.2`
![GeForce GTX 965M](https://i1.yuangezhizao.cn/Win-10/20190314192616.jpg!webp)
![最新 10.1](https://i1.yuangezhizao.cn/Win-10/20190314185122.jpg!webp)
![选择 10.0](https://i1.yuangezhizao.cn/Win-10/20190314185229.jpg!webp)
![2.1 GB 真他妈大啊](https://i1.yuangezhizao.cn/Win-10/20190314185318.jpg!webp)

~~链接：https://developer.nvidia.com/compute/cuda/10.0/Prod/local_installers/cuda_10.0.130_411.31_win10~~
![GD-WLAN 好慢呀](https://i1.yuangezhizao.cn/Win-10/20190314190055.jpg!webp)

滚去下`net`版了（~~注：此处下错了，下最新的`10.1`了……~~已改正图）
![这他妈叫精简，WTF？](https://i1.yuangezhizao.cn/Win-10/20191007201921.jpg!webp)
![真·最小化安装](https://i1.yuangezhizao.cn/Win-10/20191007202253.jpg!webp)
![打死也不升级](https://i1.yuangezhizao.cn/Win-10/20191007202344.jpg!webp)
![PATH 环境变量已经给写好了](https://i1.yuangezhizao.cn/Win-10/20190314204638.jpg!webp)
![装完之后拿 nvcc -V 验证](https://i1.yuangezhizao.cn/Win-10/20190314185821.jpg!webp)
![确认无误](https://i1.yuangezhizao.cn/Win-10/20190314231151.jpg!webp)

补充：`10.1`的报错截图：
![Fuck u 10.1](https://i1.yuangezhizao.cn/Win-10/20190314214628.jpg!webp)

### 3. 安装[cuDNN](https://developer.nvidia.com/cudnn)
![下载 10.0](https://i1.yuangezhizao.cn/Win-10/20190314203508.jpg!webp)
![主要部分还是这个 DLL，不要管截图中的 10.1，自己去下 10.0](https://i1.yuangezhizao.cn/Win-10/20190314210804.jpg!webp)

### 4. 安装[TensorRT 5.0](https://developer.nvidia.com/tensorrt)
![下载](https://i1.yuangezhizao.cn/Win-10/20190314211033.jpg!webp)
![下载](https://i1.yuangezhizao.cn/Win-10/20190314211717.jpg!webp)
![安装](https://i1.yuangezhizao.cn/Win-10/20190314211329.jpg!webp)

安装方法和`cuDNN`同理，只把`/lib`目录下的全部内容复制到`/bin`目录下嘛
![这个最新的倒是只有 10.0](https://i1.yuangezhizao.cn/Win-10/20190314211934.jpg!webp)

### 5. 终于完事儿了
![可海星](https://i1.yuangezhizao.cn/Win-10/20190314225747.jpg!webp)

未完待续……