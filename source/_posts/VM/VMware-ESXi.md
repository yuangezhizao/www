---
title: VMware ESXi 6.7.0 服务器虚拟化
date: 2019-7-28 01:58:51
tags:
  - VM
  - VMware
  - ESXI
count: 1
os: 0
os_1: 10.0.17763.652 2019-LTSC
browser: 0
browser_1: 74.0.3729.169 Stable
place: 新家
key: 53
---
    VMware ESXi: The Purpose-Built Bare Metal Hypervisor
<!-- more -->
## 0x00.[VMware ESXi](https://www.vmware.com/products/esxi-and-esx.html)
这玩楞就是传说中的把服务器整机都虚拟化的软件，之前用的`VMware Workstation`只是在本机跑虚拟机。而前者虚拟化完成之后并没有图形化界面，只能在另一台电脑上远程访问`Web`界面进行管理，比如创建多个虚拟机此类操作。所以，你懂得……
这里就截几个图看看吧（`WZ`大佬组的台式机硬件，华硕主板、`E3 CPU`,`16G`内存，唯一不足的是硬盘拿了个辣鸡`500G`先扛着了……
电信宽带提供公网`IP`，只需一个电话说明理由就给你分配，与移动的`NAT`相比已经很良心的了……
再一个这里能获取到`IPV6`地址，下列截图中也进行了高斯模糊处理。
![host](https://i1.yuangezhizao.cn/Win-10/20190727235250.png!webp)

 这里比较有意思的是，你可以创建大于物理核心数量的虚拟核心，也可以理解为虚拟化的是总频率，如下图
![CPU](https://i1.yuangezhizao.cn/Win-10/20190803011722.jpg!webp)

更改用户权限的页面藏在了这里，找了半天才发现，实在是太反人类了……
![permission](https://i1.yuangezhizao.cn/Win-10/20190728002659.jpg!webp)

先给自己分配了一个虚拟机`hhh`
![vms](https://i1.yuangezhizao.cn/Win-10/20190728003657.png!webp)
![+1s](https://i1.yuangezhizao.cn/Win-10/20190728004123.jpg!webp)

`2019-8-24 13:06:59`
![4TB 硬盘购买](https://i1.yuangezhizao.cn/Win-10/20190824130554.png!webp)
![NASdata 3TB](https://i1.yuangezhizao.cn/Win-10/20190824130337.jpg!webp)

## 0x01.Windows Server 2019 DataCenter
爽到
![cn-py-dl-w9d](https://i1.yuangezhizao.cn/Win-10/20190728015602.png!webp)

## 0x02.后记
这玩楞搁在了客厅的冰箱旁边和冰箱一起`24h`不断电工作，虽然主板以及其他位置都配置为了**节能**，但是感觉还是会比较费电……也不知道功耗能有多少诶？
