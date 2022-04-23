---
title: VMware ESXi 安装 Kali
date: 2020-5-20 20:43:53
tags:
  - VM
  - VMware
  - ESXI
  - Kali
count: 2
os: 0
os_1: 10.0.17763.1217 2019-LTSC
browser: 0
browser_1: 80.0.3987.163 Stable
place: 新家
key: 88
---
    拥有一台云 Kali 是安全从业者所感到幸福的一件事情
<!-- more -->
## 0x00.前言
[Kali](https://www.kali.org/)就没有人不知道过

## 0x01.[下载](https://www.kali.org/downloads/)
因为是`ESXi`，所以选择[Kali Linux 64-bit VMware](https://www.offensive-security.com/kali-linux-vm-vmware-virtualbox-image-download/)

`Image Name` | `Version` | `Size` | `SHA256Sum`
:---: | :---: | :---: | :---:
`Kali Linux VMware 64-Bit` | `2020.2` | `2.2G` | `13879be7faf9becc13443e155c4df3cd6c920077680b7b65ba8c71c25690fca4`

反正下载之后本人是没去校验哈希值是否正确，直接就扔到`datastore`中了，因为是`7z`格式所以要拿命令行解压，而`ESXi`并不包含所需工具
因此需要去第三方网站下载`p7zip`，将二进制可执行文件扔上去就可以用了，记得赋予可执行权限
``` bash
[yuangezhizao@VM:/vmfs/volumes/5e0607d4-ae255451-ad8d-2c56dc945d15] ./p7zip_16.02/bin/7z x kali-linux-2020.2-vmware-amd64.7z 
-sh: ./p7zip_16.02/bin/7z: Permission denied
[yuangezhizao@VM:/vmfs/volumes/5e0607d4-ae255451-ad8d-2c56dc945d15] chmod +x p7zip_16.02/bin/7z
[yuangezhizao@VM:/vmfs/volumes/5e0607d4-ae255451-ad8d-2c56dc945d15] ./p7zip_16.02/bin/7z x kali-linux-2020.2-vmware-amd64.7z 

7-Zip [32] 16.02 : Copyright (c) 1999-2016 Igor Pavlov : 2016-05-21
p7zip Version 16.02 (locale=en_US.UTF-8,Utf16=on,HugeFiles=on,32 bits,48 CPUs Intel(R) Xeon(R) CPU E5-2697 v2 @ 2.70GHz (306E4),ASM,AES-NI)

Scanning the drive for archives:
1 file, 2284771480 bytes (2179 MiB)

Extracting archive: kali-linux-2020.2-vmware-amd64.7z
--
Path = kali-linux-2020.2-vmware-amd64.7z
Type = 7z
Physical Size = 2284771480
Headers Size = 585
Method = LZMA2:26
Solid = +
Blocks = 3

Everything is Ok                                                             

Folders: 1
Files: 26
Size:       9345710250
Compressed: 2284771480
```
辣鸡机械硬盘速度不行，因此等了好久才解压完毕

## 0x02.注册
![注册现有虚拟机](https://i1.yuangezhizao.cn/Win-10/20200520205810.jpg!webp)
![选择要注册的虚拟机](https://i1.yuangezhizao.cn/Win-10/20200520205910.jpg!webp)
![即将完成](https://i1.yuangezhizao.cn/Win-10/20200520205936.jpg!webp)
![完成](https://i1.yuangezhizao.cn/Win-10/20200520210152.jpg!webp)

## 0x03.编辑设置
分它个`4C2G`，启动，翻车（
> 失败 - `“scsi0:0”`的磁盘类型`7`不受支持或无效。请确保磁盘已导入。
无法为`“scsi0:0”(/vmfs/volumes/5e0607d4-ae255451-ad8d-2c56dc945d15/Kali-Linux-2020.2-amd64.vmwarevm/Kali-Linux-2020.2-vmware-amd64.vmdk)`创建虚拟`SCSI`设备。

![草](https://i1.yuangezhizao.cn/Win-10/20200517135156.jpg!webp)

去搜了下是因为磁盘的虚拟格式不一样，需要用`ESXi`上自带工具`vmkfstools`进行手动转化，`vmkfstools -i HostedVirtualDisk ESXVirtualDisk`

<details><summary>点击此处 ← 查看终端</summary>

``` bash
[yuangezhizao@VM:/vmfs/volumes/5e0607d4-ae255451-ad8d-2c56dc945d15] cd Kali-Linux-2020.2-amd64.vmwarevm/
[yuangezhizao@VM:/vmfs/volumes/5e0607d4-ae255451-ad8d-2c56dc945d15/Kali-Linux-2020.2-amd64.vmwarevm] ll
total 9139584
drwx------    1 root     root         81920 May 20 12:27 .
drwxr-xr-t    1 root     root         90112 May 17 05:08 ..
-rw-r--r--    1 root     root     2951938048 May  8 13:23 Kali-Linux-2020.2-vmware-amd64-s001.vmdk
-rw-r--r--    1 root     root     3372613632 May  8 13:23 Kali-Linux-2020.2-vmware-amd64-s002.vmdk
-rw-r--r--    1 root     root       1376256 May  8 13:23 Kali-Linux-2020.2-vmware-amd64-s003.vmdk
-rw-r--r--    1 root     root        917504 May  8 13:23 Kali-Linux-2020.2-vmware-amd64-s004.vmdk
-rw-r--r--    1 root     root        851968 May  8 13:23 Kali-Linux-2020.2-vmware-amd64-s005.vmdk
-rw-r--r--    1 root     root     444465152 May  8 13:23 Kali-Linux-2020.2-vmware-amd64-s006.vmdk
-rw-r--r--    1 root     root     307625984 May  8 13:23 Kali-Linux-2020.2-vmware-amd64-s007.vmdk
-rw-r--r--    1 root     root     219742208 May  8 13:23 Kali-Linux-2020.2-vmware-amd64-s008.vmdk
-rw-r--r--    1 root     root     185925632 May  8 13:23 Kali-Linux-2020.2-vmware-amd64-s009.vmdk
-rw-r--r--    1 root     root     642449408 May  8 13:23 Kali-Linux-2020.2-vmware-amd64-s010.vmdk
-rw-r--r--    1 root     root     186777600 May  8 13:23 Kali-Linux-2020.2-vmware-amd64-s011.vmdk
-rw-r--r--    1 root     root     139919360 May  8 13:23 Kali-Linux-2020.2-vmware-amd64-s012.vmdk
-rw-r--r--    1 root     root     107872256 May  8 13:23 Kali-Linux-2020.2-vmware-amd64-s013.vmdk
-rw-r--r--    1 root     root      67239936 May  8 13:23 Kali-Linux-2020.2-vmware-amd64-s014.vmdk
-rw-r--r--    1 root     root     375455744 May  8 13:23 Kali-Linux-2020.2-vmware-amd64-s015.vmdk
-rw-r--r--    1 root     root     104398848 May  8 13:23 Kali-Linux-2020.2-vmware-amd64-s016.vmdk
-rw-r--r--    1 root     root      78249984 May  8 13:23 Kali-Linux-2020.2-vmware-amd64-s017.vmdk
-rw-r--r--    1 root     root        655360 May  8 13:23 Kali-Linux-2020.2-vmware-amd64-s018.vmdk
-rw-r--r--    1 root     root       1245184 May  8 13:23 Kali-Linux-2020.2-vmware-amd64-s019.vmdk
-rw-r--r--    1 root     root     155844608 May  8 13:23 Kali-Linux-2020.2-vmware-amd64-s020.vmdk
-rw-r--r--    1 root     root        131072 May  8 13:21 Kali-Linux-2020.2-vmware-amd64-s021.vmdk
-rw-r--r--    1 root     root          8684 May  8 13:22 Kali-Linux-2020.2-vmware-amd64.nvram
-rw-r--r--    1 root     root          1768 May  8 12:58 Kali-Linux-2020.2-vmware-amd64.vmdk
-rw-r--r--    1 root     root             0 May  8 11:56 Kali-Linux-2020.2-vmware-amd64.vmsd
-rw-r--r--    1 root     root          3899 May 20 12:27 Kali-Linux-2020.2-vmware-amd64.vmx
-rw-r--r--    1 root     root           285 May  8 11:56 Kali-Linux-2020.2-vmware-amd64.vmxf
-rw-r--r--    1 root     root         51459 May 17 05:50 vmware-1.log
-rw-r--r--    1 root     root         50256 May 20 12:27 vmware.log
[yuangezhizao@VM:/vmfs/volumes/5e0607d4-ae255451-ad8d-2c56dc945d15/Kali-Linux-2020.2-amd64.vmwarevm] vmkfstools -i Kali-Linux-2020.2-vmware-amd64-s001.vmdk Kali-Linux-2020.2-vmware-amd64-s001-new.vmdk -d thin
DiskLib_Check() failed for source disk The file specified is not a virtual disk (15).
[yuangezhizao@VM:/vmfs/volumes/5e0607d4-ae255451-ad8d-2c56dc945d15/Kali-Linux-2020.2-amd64.vmwarevm] vmkfstools -i Kali-Linux-2020.2-vmware-amd64.vmdk Kali-Linux-2020.2-vmware-amd64-new.vmdk -d thin
Destination disk format: VMFS thin-provisioned
Cloning disk 'Kali-Linux-2020.2-vmware-amd64.vmdk'...
Clone: 100% done.
```

</details>

`2022-04-23 23:40:22`：注意把`Kali-Linux-2020.2-vmware-amd64.vmdk`转换成`Kali-Linux-2020.2-vmware-amd64-new.vmdk`之后不能重命名，因为磁盘文件中记录了文件名的信息，也不用管那个生成的`flat`文件
~~启动，再翻车……~~
![草](https://i1.yuangezhizao.cn/Win-10/20200520211526.jpg!webp)

~~于是猜想到不能重命名转换完毕的新磁盘，于是`revoke`~~
删除旧硬盘，重新添加新硬盘，选择到`Kali-Linux-2020.2-vmware-amd64-new.vmdk`，终于添加成功（另外注意到`Kali-Linux-2020.2-vmware-amd64-new-flat.vmdk`不见了。。。

## 0x04.打开电源
![root/root](https://i1.yuangezhizao.cn/Win-10/20200520212023.jpg!webp)
![4K](https://i1.yuangezhizao.cn/Win-10/20200520212321.jpg!webp)

## 0x05.后记
初见不到一个小时就写完了，完全是水了一篇文章草

> 至此本文使命完成
