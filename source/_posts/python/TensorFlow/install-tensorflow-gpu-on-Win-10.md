---
title: Win-10 安装 TensorFlow-GPU
date: 2017-8-3 10:25:03
tags:
  - TensorFlow
  - TensorFlow-GPU
count: 1
os: 0
os_1: 10.0.15063 Pro
browser: 0
browser_1: 61.0.3153.0 Dev
place: 家
key: 11
gitment: true
---
    已经是八月份了，暑假已经过了一半的说
<!-- more -->
> **【20190401】**很感谢能点进来看的你们，唯独这篇文章让我这个小站有了每天的固定个位数访客，为表达对老铁们的感谢特更新了文章，详情请见：[Win-10 安装 TensorFlow-GPU 1.13.1（Python 3.7.2 + CUDA 10.0 + cuDNN 7.5.0 + TensorRT 5.0.4.3）](./install-tensorflow-gpu-on-Win-10-1903.html)

## 0x00.缘由
Q：为什么要写（这么低级的）配置教程？
A：（其实并不低级~~；网上的是旧的；一看编译就头疼~~），鉴于以后（或许）会有多篇关于`TensorFlow`的文章（花式挖坑），所以在这里有必要介绍一下其安装方法

Q：`TensorFlow`是什么？
A：`TensorFlow is an Open Source Software Library for Machine Intelligence`
> 由`Google`开源的深度学习库，可以对定义在 `Tensor`（张量）上的函数自动求导。
`Tensor`意味着`N`维数组，`Flow`（流）意味着基于数据流图的计算，`TensorFlow`即为张量从图的一端流动到另一端。
它的一大亮点是支持异构设备分布式计算，它能够在各个平台上自动运行模型，从电话、单个`CPU/GPU`到成百上千`GPU`卡组成的分布式系统。
支持`CNN、RNN和LSTM`算法，是目前在`Image、NLP`最流行的深度神经网络模型。


Q：为什么要研究这个？
A：
> 深度学习通常意味着建立具有很多层的大规模的神经网络。
除了输入`X`，函数还使用一系列参数，其中包括标量值、向量以及最昂贵的矩阵和高阶张量。
在训练网络之前，需要定义一个代价函数，常见的代价函数包括回归问题的方差以及分类时候的交叉熵。
训练时，需要连续的将多批新输入投入网络，对所有的参数求导后，代入代价函数，从而更新整个网络模型。
这个过程中有两个主要的问题：1. 较大的数字或者张量在一起相乘百万次的处理，使得整个模型代价非常大。2. 手动求导耗时非常久。
所以`TensorFlow`的对函数自动求导以及分布式计算，可以帮我们节省很多时间来训练模型。

Q：它有什么优点？
A：
> 1.基于`python`，写的很快并且具有可读性；
2.在多`GPU`系统上的运行更为顺畅；
3.代码编译效率较高；
4.社区发展的非常迅速并且活跃；
5.能够生成显示网络拓扑结构和性能的可视化图。

## 0x01.环境
a. Microsoft Windows [版本 10.0.15063]（Win 10 x64 Pro 1703 15063.483）
b. Python 3.6.1 (v3.6.1:69c0db5, Mar 21 2017, 18:41:36) [MSC v.1900 64 bit (AMD64)] on win32
c. JetBrains Pycharm 2017.2 x64 Professional
d. GeForce GTX 965M

## 0x02.安装
### 1. 安装`python 36`
一路下一步打钩环境变量设置即可。不建议`python 27`，因为好像不支持，所以最后一步会报`Could not find a version that satisfies the requirement tensorflow-gpu (from versions: ) No matching distribution found for tensorflow-gpu`

### 2. 更换[清华`pip`镜像源](https://mirrors.tuna.tsinghua.edu.cn/help/pypi/)
默认源服务器在国外，国内下载较慢，有必要换为国内清华源。
#### 临时使用
```
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
```
注意，`simple`不能少, 是`https`而不是`http`
#### 设为默认
升级`pip`到最新的版本`(>=10.0.0)`后进行配置：
``` bash
Microsoft Windows [版本 10.0.17763.652]
(c) 2018 Microsoft Corporation。保留所有权利。

C:\Windows\system32>pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U
Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple
Requirement already up-to-date: pip in c:\python37\lib\site-packages (19.2.1)

C:\Windows\system32>pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
Writing to C:\Users\yuangezhizao\AppData\Roaming\pip\pip.ini

C:\Windows\system32>
```
`pip.ini`文件配置示例如下：
```
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
```
`2019-8-24 13:31:12`：
~~这里吐槽下科大其实用的是清华的源……~~已改为清华源


### 3. 升级`pip`
`py -2 -m pip install --upgrade pip`
由于我电脑安装了两个版本，所以用 py -2 选择 2 版本的解释器，同理 py -3 即是选择 3 版本的解释器


`TensorFlow`有两个版本：`CPU`版本和`GPU`版本。
如果你的电脑没有`NVIDIA`显卡的话，你就必须选择安装这个版本，不过这个版本的安装要比`GPU`版的简单，官方也推荐先用`CPU`版的来体验。`TensorFlow`在`GPU`上运行要比`CPU`上快很多，如果你的`GPU`能够达到要求就可以选择安装`GPU`版。`GPU`版本需要`CUDA`和`cuDNN`的支持，要安装`GPU`版本，需确认显卡是否支持`CUDA`，[查看GPU是否支持CUDA](https://developer.nvidia.com/cuda-gpus)，计算能力大于`3.5`的`N`卡一般都支持的说……

另，网上多建议安装`Anaconda`，因为这个集成了很多科学计算所必需的库，能够避免很多依赖问题，这个`Pycharm`党就先不安了（其实我安了但是可能是因为我用习惯了感觉没有`Pycharm`舒服）

### 4. 安装[CUDA](https://developer.nvidia.com/cuda-downloads)
`Windows`→`x86_64`→`10`→`exe (local)`
下载如下两个文件，按照先后顺序安装：
`Base Installer	Download (1.3 GB)`
`Patch 2 (Released Jun 26, 2017) Download (43.1 MB)`
安装完之后，在命令行输入`nvcc -V`，会有正常回显……

### 5. 安装[cuDNN](https://developer.nvidia.com/cudnn)
`cuDNN`可以在前面`GPU`加速基础上大概再提升`1.5`倍的速度，同样由`nVIDIA`开发。官网注册账号，下载[cuDNN v8.0 Library for Windows 10](https://developer.nvidia.com/compute/machine-learning/cudnn/secure/v6/prod/8.0_20170307/cudnn-8.0-windows10-x64-v6.0-zip)
压缩包，解压完将**对应**文件夹（`bin、include、lib`）覆盖至`CUDA`的安装目录，即`C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v8.0`，然后把`C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v8.0\bin`加入环境变量，并将`bin`文件夹里的`cudnn64_6.dll`重命名为`cudnn64_5.dll`（此处参考[tensorflow/issues/7705](https://github.com/tensorflow/tensorflow/issues/7705)，其实换旧版本也可以解决[stackoverflow](https://stackoverflow.com/questions/44080677/no-module-named-pywrap-tensorflow-internal)，因为重下安装包较大故采用前一方法），才算完成。

    话说注册账号要求好麻烦，大小写包含特殊符号且不少于6位……

### 6. `pip`安装`TensorFlow-GPU`（最后一步）
`pip3 install --upgrade tensorflow-gpu`
万一在线`pip`安装失败了，就离线安装，到[http://www.lfd.uci.edu/~gohlke/pythonlibs/](http://www.lfd.uci.edu/~gohlke/pythonlibs/)下载`python`的`whl`包`tensorflow_gpu‑1.1.0‑cp36‑cp36m‑win_amd64.whl`，然后命令提示符运行`pip install < 此处填写 .whl 所在位置 >`（可以将`.whl`文件拖入命令提示符中即生成其位置）

## 0x03.测试
``` python
#! python3
# coding: utf-8

import tensorflow as tf
hello = tf.constant('Hello, TensorFlow!')
sess = tf.Session()
print(sess.run(hello))
```
我的输出较长：
```
C:\Python36\python.exe C:/Users/yuangezhizao/PycharmProjects/deeplearning/helloworld.py
2017-08-03 14:53:23.258570: W c:\tf_jenkins\home\workspace\release-win\m\windows-gpu\py\36\tensorflow\core\platform\cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use SSE instructions, but these are available on your machine and could speed up CPU computations.
2017-08-03 14:53:23.258819: W c:\tf_jenkins\home\workspace\release-win\m\windows-gpu\py\36\tensorflow\core\platform\cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use SSE2 instructions, but these are available on your machine and could speed up CPU computations.
2017-08-03 14:53:23.259063: W c:\tf_jenkins\home\workspace\release-win\m\windows-gpu\py\36\tensorflow\core\platform\cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use SSE3 instructions, but these are available on your machine and could speed up CPU computations.
2017-08-03 14:53:23.259307: W c:\tf_jenkins\home\workspace\release-win\m\windows-gpu\py\36\tensorflow\core\platform\cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use SSE4.1 instructions, but these are available on your machine and could speed up CPU computations.
2017-08-03 14:53:23.259552: W c:\tf_jenkins\home\workspace\release-win\m\windows-gpu\py\36\tensorflow\core\platform\cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use SSE4.2 instructions, but these are available on your machine and could speed up CPU computations.
2017-08-03 14:53:23.259790: W c:\tf_jenkins\home\workspace\release-win\m\windows-gpu\py\36\tensorflow\core\platform\cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use AVX instructions, but these are available on your machine and could speed up CPU computations.
2017-08-03 14:53:23.260028: W c:\tf_jenkins\home\workspace\release-win\m\windows-gpu\py\36\tensorflow\core\platform\cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use AVX2 instructions, but these are available on your machine and could speed up CPU computations.
2017-08-03 14:53:23.260264: W c:\tf_jenkins\home\workspace\release-win\m\windows-gpu\py\36\tensorflow\core\platform\cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use FMA instructions, but these are available on your machine and could speed up CPU computations.
2017-08-03 14:53:24.103495: I c:\tf_jenkins\home\workspace\release-win\m\windows-gpu\py\36\tensorflow\core\common_runtime\gpu\gpu_device.cc:940] Found device 0 with properties: 
name: GeForce GTX 965M
major: 5 minor: 2 memoryClockRate (GHz) 0.9495
pciBusID 0000:01:00.0
Total memory: 2.00GiB
Free memory: 1.64GiB
2017-08-03 14:53:24.103772: I c:\tf_jenkins\home\workspace\release-win\m\windows-gpu\py\36\tensorflow\core\common_runtime\gpu\gpu_device.cc:961] DMA: 0 
2017-08-03 14:53:24.103900: I c:\tf_jenkins\home\workspace\release-win\m\windows-gpu\py\36\tensorflow\core\common_runtime\gpu\gpu_device.cc:971] 0:   Y 
2017-08-03 14:53:24.104045: I c:\tf_jenkins\home\workspace\release-win\m\windows-gpu\py\36\tensorflow\core\common_runtime\gpu\gpu_device.cc:1030] Creating TensorFlow device (/gpu:0) -> (device: 0, name: GeForce GTX 965M, pci bus id: 0000:01:00.0)
b'Hello, TensorFlow!'
```
这里之所以会出红字提示是因为没有在本机编译，尝试编译（实在是不会……），于是重启进`Mac`里……未完待续

## 0x04.引用
> [TensorFlow 入门](https://web.archive.org/web/20190905070704/https://www.jianshu.com/p/6766fbcd43b9)
[windows 10 64bit下安装Tensorflow+Keras+VS2015+CUDA8.0 GPU加速](https://web.archive.org/web/20190905070738/https://www.jianshu.com/p/c245d46d43f0)
[【TensorFlow】Windows10 64 位下安装 TensorFlow - 官方原生支持](https://web.archive.org/web/20190905070826/https://blog.csdn.net/u010099080/article/details/53418159)
[【TensorFlow】Windows环境下PyCharm运行TensorFlow GPU版(附TensorFlow更新方法)](https://web.archive.org/web/20190905070916/https://blog.csdn.net/wx7788250/article/details/60877166)
[windows 10 64bit下安装Tensorflow+Keras+VS2015+CUDA8.0 GPU加速](https://web.archive.org/web/20190905071000/https://www.cnblogs.com/leoking01/p/6913408.html)
