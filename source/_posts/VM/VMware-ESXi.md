---
title: VMware ESXi 7.0.0 服务器虚拟化
date: 2019-7-28 01:58:51
tags:
  - VM
  - VMware
  - ESXi
count: 4
os: 0
os_1: 10.0.17763.652 2019-LTSC
browser: 0
browser_1: 74.0.3729.169 Stable
place: 新家
key: 53
---
    VMware ESXi: The Purpose-Built Bare Metal Hypervisor
<!-- more -->
## 0x00.安装或升级
### `ESXCLI`使用`Zip`文件更新`ESXi`主机
### 1.下载
![7.0](https://i1.yuangezhizao.cn/Win-10/20200404011121.jpg!webp)

下载链接来源未知，请自行鉴别安全性
> `VMware vSphere Hypervisor（ESXi）`脱机捆绑包
链接： [VMware-ESXi-7.0.0-15843807-depot.zip](https://cld14.irans3.com/dlir-s3/VMware-ESXi-7.0.0-15843807-depot.zip)
档案大小： `344 MB`
MD5： `d3e7d11daaa98d235694201b367dfdb2`
SHA1： `84c27637f0f48f11f7638425c9e106d68c27f6fc`

下完之后扔到存储上

### 2.`ESXCLI`
![官方中文教程](https://i1.yuangezhizao.cn/Win-10/20200404010548.jpg!webp)

挂起全部虚拟机之后进入**维护模式**
``` bash
[yuangezhizao@VM:~] vim-cmd hostsvc/maintenance_mode_enter
Operation timed out.
[yuangezhizao@VM:~] vim-cmd hostsvc/maintenance_mode_enter
[yuangezhizao@VM:~] 
```
![维护中](https://i1.yuangezhizao.cn/Win-10/20200404011523.jpg!webp)

然后命令行升级，注意需要全路径
``` bash
[yuangezhizao@VM:~] cd /vmfs/volumes/5d5d97d2-f9f4fe8f-7361-2c56dc945d15
[yuangezhizao@VM:/vmfs/volumes/5d5d97d2-f9f4fe8f-7361-2c56dc945d15] esxcli software vib update -d VMware-ESXi-7.0.0-15843807-depot.zip 
 [MetadataDownloadError]
 Could not download from depot at zip:/var/log/vmware/VMware-ESXi-7.0.0-15843807-depot.zip?index.xml, skipping (('zip:/var/log/vmware/VMware-ESXi-7.0.0-15843807-depot.zip?index.xml', '', "Error extracting index.xml from /var/log/vmware/VMware-ESXi-7.0.0-15843807-depot.zip: [Errno 2] No such file or directory: '/var/log/vmware/VMware-ESXi-7.0.0-15843807-depot.zip'"))
        url = zip:/var/log/vmware/VMware-ESXi-7.0.0-15843807-depot.zip?index.xml
 Please refer to the log file for more details.
[yuangezhizao@VM:/vmfs/volumes/5d5d97d2-f9f4fe8f-7361-2c56dc945d15] esxcli software vib update -d /vmfs/volumes/5d5d97d2-f9f4fe8f-7361-2c56dc945d15/VMware-ESXi-7.0.0-15843807-depot.zip 
 [DependencyError]
 VIB Realtek_bootbank_net55-r8168_8.045a-napi requires vmkapi_2_2_0_0, but the requirement cannot be satisfied within the ImageProfile.
 VIB Realtek_bootbank_net55-r8168_8.045a-napi requires com.vmware.driverAPI-9.2.2.0, but the requirement cannot be satisfied within the ImageProfile.
 Please refer to the log file for more details.
```
结果有冲突，没错（螃蟹网卡）还未支持？
![Dependencies and Restrictions](https://i1.yuangezhizao.cn/Win-10/20200404013211.jpg!webp)

然后去看下网卡信息
``` bash
[yuangezhizao@VM:~] esxcli network nic list
Name    PCI Device    Driver  Admin Status  Link Status  Speed  Duplex  MAC Address         MTU  Description
------  ------------  ------  ------------  -----------  -----  ------  -----------------  ----  -------------------------------------------------
vmnic0  0000:07:00.0  igbn    Up            Up            1000  Full    00:13:32:08:f7:d4  1500  Intel Corporation I211 Gigabit Network Connection
vmnic1  0000:09:00.0  igbn    Up            Up            1000  Full    00:13:32:08:f7:d5  1500  Intel Corporation I211 Gigabit Network Connection
[yuangezhizao@VM:~] esxcli network nic get -n vmnic0
   Advertised Auto Negotiation: true
   Advertised Link Modes: Auto, 1000BaseT/Full, 100BaseT/Full, 10BaseT/Full
   Auto Negotiation: true
   Cable Type: Twisted Pair
   Current Message Level: 0
   Driver Info: 
         Bus Info: 0000:07:00:0
         Driver: igbn
         Firmware Version: 0.6-5
         Version: 0.1.1.0
   Link Detected: true
   Link Status: Up 
   Name: vmnic0
   PHYAddress: 0
   Pause Autonegotiate: false
   Pause RX: false
   Pause TX: false
   Supported Ports: TP
   Supports Auto Negotiation: true
   Supports Pause: false
   Supports Wakeon: true
   Transceiver: internal
   Virtual Address: 00:50:56:50:0a:c0
   Wakeon: MagicPacket(tm)
```
现在用的是`Intel`的网卡哈哈哈，看下全部`VIB`列表

<details><summary>点击此处 ← 查看终端</summary>

``` bash
[yuangezhizao@VM:~] esxcli software vib list
Name                           Version                               Vendor   Acceptance Level    Install Date
-----------------------------  ------------------------------------  -------  ------------------  ------------
net55-r8168                    8.045a-napi                           Realtek  CommunitySupported  2019-12-27
ata-libata-92                  3.00.9.2-16vmw.670.0.0.8169922        VMW      VMwareCertified     2019-12-27
ata-pata-amd                   0.3.10-3vmw.670.0.0.8169922           VMW      VMwareCertified     2019-12-27
ata-pata-atiixp                0.4.6-4vmw.670.0.0.8169922            VMW      VMwareCertified     2019-12-27
ata-pata-cmd64x                0.2.5-3vmw.670.0.0.8169922            VMW      VMwareCertified     2019-12-27
ata-pata-hpt3x2n               0.3.4-3vmw.670.0.0.8169922            VMW      VMwareCertified     2019-12-27
ata-pata-pdc2027x              1.0-3vmw.670.0.0.8169922              VMW      VMwareCertified     2019-12-27
ata-pata-serverworks           0.4.3-3vmw.670.0.0.8169922            VMW      VMwareCertified     2019-12-27
ata-pata-sil680                0.4.8-3vmw.670.0.0.8169922            VMW      VMwareCertified     2019-12-27
ata-pata-via                   0.3.3-2vmw.670.0.0.8169922            VMW      VMwareCertified     2019-12-27
block-cciss                    3.6.14-10vmw.670.0.0.8169922          VMW      VMwareCertified     2019-12-27
bnxtnet                        20.6.101.7-24vmw.670.3.73.14320388    VMW      VMwareCertified     2019-12-27
bnxtroce                       20.6.101.0-20vmw.670.1.28.10302608    VMW      VMwareCertified     2019-12-27
brcmfcoe                       11.4.1078.25-14vmw.670.3.73.14320388  VMW      VMwareCertified     2019-12-27
char-random                    1.0-3vmw.670.0.0.8169922              VMW      VMwareCertified     2019-12-27
ehci-ehci-hcd                  1.0-4vmw.670.0.0.8169922              VMW      VMwareCertified     2019-12-27
elxiscsi                       11.4.1174.0-2vmw.670.0.0.8169922      VMW      VMwareCertified     2019-12-27
elxnet                         11.4.1097.0-5vmw.670.3.73.14320388    VMW      VMwareCertified     2019-12-27
hid-hid                        1.0-3vmw.670.0.0.8169922              VMW      VMwareCertified     2019-12-27
i40en                          1.8.1.9-2vmw.670.3.73.14320388        VMW      VMwareCertified     2019-12-27
iavmd                          1.2.0.1011-2vmw.670.0.0.8169922       VMW      VMwareCertified     2019-12-27
igbn                           0.1.1.0-5vmw.670.3.73.14320388        VMW      VMwareCertified     2019-12-27
ima-qla4xxx                    2.02.18-1vmw.670.0.0.8169922          VMW      VMwareCertified     2019-12-27
ipmi-ipmi-devintf              39.1-5vmw.670.1.28.10302608           VMW      VMwareCertified     2019-12-27
ipmi-ipmi-msghandler           39.1-5vmw.670.1.28.10302608           VMW      VMwareCertified     2019-12-27
ipmi-ipmi-si-drv               39.1-5vmw.670.1.28.10302608           VMW      VMwareCertified     2019-12-27
iser                           1.0.0.0-1vmw.670.1.28.10302608        VMW      VMwareCertified     2019-12-27
ixgben                         1.7.1.16-1vmw.670.3.73.14320388       VMW      VMwareCertified     2019-12-27
lpfc                           11.4.33.25-14vmw.670.3.73.14320388    VMW      VMwareCertified     2019-12-27
lpnic                          11.4.59.0-1vmw.670.0.0.8169922        VMW      VMwareCertified     2019-12-27
lsi-mr3                        7.708.07.00-3vmw.670.3.73.14320388    VMW      VMwareCertified     2019-12-27
lsi-msgpt2                     20.00.06.00-2vmw.670.3.73.14320388    VMW      VMwareCertified     2019-12-27
lsi-msgpt35                    09.00.00.00-5vmw.670.3.73.14320388    VMW      VMwareCertified     2019-12-27
lsi-msgpt3                     17.00.02.00-1vmw.670.3.73.14320388    VMW      VMwareCertified     2019-12-27
misc-cnic-register             1.78.75.v60.7-1vmw.670.0.0.8169922    VMW      VMwareCertified     2019-12-27
misc-drivers                   6.7.0-2.48.13006603                   VMW      VMwareCertified     2019-12-27
mtip32xx-native                3.9.8-1vmw.670.1.28.10302608          VMW      VMwareCertified     2019-12-27
ne1000                         0.8.4-2vmw.670.2.48.13006603          VMW      VMwareCertified     2019-12-27
nenic                          1.0.29.0-1vmw.670.3.73.14320388       VMW      VMwareCertified     2019-12-27
net-bnx2                       2.2.4f.v60.10-2vmw.670.0.0.8169922    VMW      VMwareCertified     2019-12-27
net-bnx2x                      1.78.80.v60.12-2vmw.670.0.0.8169922   VMW      VMwareCertified     2019-12-27
net-cdc-ether                  1.0-3vmw.670.0.0.8169922              VMW      VMwareCertified     2019-12-27
net-cnic                       1.78.76.v60.13-2vmw.670.0.0.8169922   VMW      VMwareCertified     2019-12-27
net-e1000                      8.0.3.1-5vmw.670.0.0.8169922          VMW      VMwareCertified     2019-12-27
net-e1000e                     3.2.2.1-2vmw.670.0.0.8169922          VMW      VMwareCertified     2019-12-27
net-enic                       2.1.2.38-2vmw.670.0.0.8169922         VMW      VMwareCertified     2019-12-27
net-fcoe                       1.0.29.9.3-7vmw.670.0.0.8169922       VMW      VMwareCertified     2019-12-27
net-forcedeth                  0.61-2vmw.670.0.0.8169922             VMW      VMwareCertified     2019-12-27
net-igb                        5.0.5.1.1-5vmw.670.0.0.8169922        VMW      VMwareCertified     2019-12-27
net-ixgbe                      3.7.13.7.14iov-20vmw.670.0.0.8169922  VMW      VMwareCertified     2019-12-27
net-libfcoe-92                 1.0.24.9.4-8vmw.670.0.0.8169922       VMW      VMwareCertified     2019-12-27
net-mlx4-core                  1.9.7.0-1vmw.670.0.0.8169922          VMW      VMwareCertified     2019-12-27
net-mlx4-en                    1.9.7.0-1vmw.670.0.0.8169922          VMW      VMwareCertified     2019-12-27
net-nx-nic                     5.0.621-5vmw.670.0.0.8169922          VMW      VMwareCertified     2019-12-27
net-tg3                        3.131d.v60.4-2vmw.670.0.0.8169922     VMW      VMwareCertified     2019-12-27
net-usbnet                     1.0-3vmw.670.0.0.8169922              VMW      VMwareCertified     2019-12-27
net-vmxnet3                    1.1.3.0-3vmw.670.3.89.15160138        VMW      VMwareCertified     2019-12-27
nfnic                          4.0.0.29-0vmw.670.3.73.14320388       VMW      VMwareCertified     2019-12-27
nhpsa                          2.0.22-3vmw.670.1.28.10302608         VMW      VMwareCertified     2019-12-27
nmlx4-core                     3.17.13.1-1vmw.670.2.48.13006603      VMW      VMwareCertified     2019-12-27
nmlx4-en                       3.17.13.1-1vmw.670.2.48.13006603      VMW      VMwareCertified     2019-12-27
nmlx4-rdma                     3.17.13.1-1vmw.670.2.48.13006603      VMW      VMwareCertified     2019-12-27
nmlx5-core                     4.17.13.1-1vmw.670.3.73.14320388      VMW      VMwareCertified     2019-12-27
nmlx5-rdma                     4.17.13.1-1vmw.670.2.48.13006603      VMW      VMwareCertified     2019-12-27
ntg3                           4.1.3.2-1vmw.670.1.28.10302608        VMW      VMwareCertified     2019-12-27
nvme                           1.2.2.28-1vmw.670.3.73.14320388       VMW      VMwareCertified     2019-12-27
nvmxnet3-ens                   2.0.0.21-1vmw.670.0.0.8169922         VMW      VMwareCertified     2019-12-27
nvmxnet3                       2.0.0.29-1vmw.670.1.28.10302608       VMW      VMwareCertified     2019-12-27
ohci-usb-ohci                  1.0-3vmw.670.0.0.8169922              VMW      VMwareCertified     2019-12-27
pvscsi                         0.1-2vmw.670.0.0.8169922              VMW      VMwareCertified     2019-12-27
qcnic                          1.0.2.0.4-1vmw.670.0.0.8169922        VMW      VMwareCertified     2019-12-27
qedentv                        2.0.6.4-10vmw.670.1.28.10302608       VMW      VMwareCertified     2019-12-27
qfle3                          1.0.50.11-9vmw.670.0.0.8169922        VMW      VMwareCertified     2019-12-27
qfle3f                         1.0.25.0.2-14vmw.670.0.0.8169922      VMW      VMwareCertified     2019-12-27
qfle3i                         1.0.2.3.9-3vmw.670.0.0.8169922        VMW      VMwareCertified     2019-12-27
qflge                          1.1.0.11-1vmw.670.0.0.8169922         VMW      VMwareCertified     2019-12-27
sata-ahci                      3.0-26vmw.670.0.0.8169922             VMW      VMwareCertified     2019-12-27
sata-ata-piix                  2.12-10vmw.670.0.0.8169922            VMW      VMwareCertified     2019-12-27
sata-sata-nv                   3.5-4vmw.670.0.0.8169922              VMW      VMwareCertified     2019-12-27
sata-sata-promise              2.12-3vmw.670.0.0.8169922             VMW      VMwareCertified     2019-12-27
sata-sata-sil24                1.1-1vmw.670.0.0.8169922              VMW      VMwareCertified     2019-12-27
sata-sata-sil                  2.3-4vmw.670.0.0.8169922              VMW      VMwareCertified     2019-12-27
sata-sata-svw                  2.3-3vmw.670.0.0.8169922              VMW      VMwareCertified     2019-12-27
scsi-aacraid                   1.1.5.1-9vmw.670.0.0.8169922          VMW      VMwareCertified     2019-12-27
scsi-adp94xx                   1.0.8.12-6vmw.670.0.0.8169922         VMW      VMwareCertified     2019-12-27
scsi-aic79xx                   3.1-6vmw.670.0.0.8169922              VMW      VMwareCertified     2019-12-27
scsi-bnx2fc                    1.78.78.v60.8-1vmw.670.0.0.8169922    VMW      VMwareCertified     2019-12-27
scsi-bnx2i                     2.78.76.v60.8-1vmw.670.0.0.8169922    VMW      VMwareCertified     2019-12-27
scsi-fnic                      1.5.0.45-3vmw.670.0.0.8169922         VMW      VMwareCertified     2019-12-27
scsi-hpsa                      6.0.0.84-3vmw.670.0.0.8169922         VMW      VMwareCertified     2019-12-27
scsi-ips                       7.12.05-4vmw.670.0.0.8169922          VMW      VMwareCertified     2019-12-27
scsi-iscsi-linux-92            1.0.0.2-3vmw.670.0.0.8169922          VMW      VMwareCertified     2019-12-27
scsi-libfc-92                  1.0.40.9.3-5vmw.670.0.0.8169922       VMW      VMwareCertified     2019-12-27
scsi-megaraid-mbox             2.20.5.1-6vmw.670.0.0.8169922         VMW      VMwareCertified     2019-12-27
scsi-megaraid-sas              6.603.55.00-2vmw.670.0.0.8169922      VMW      VMwareCertified     2019-12-27
scsi-megaraid2                 2.00.4-9vmw.670.0.0.8169922           VMW      VMwareCertified     2019-12-27
scsi-mpt2sas                   19.00.00.00-2vmw.670.0.0.8169922      VMW      VMwareCertified     2019-12-27
scsi-mptsas                    4.23.01.00-10vmw.670.0.0.8169922      VMW      VMwareCertified     2019-12-27
scsi-mptspi                    4.23.01.00-10vmw.670.0.0.8169922      VMW      VMwareCertified     2019-12-27
scsi-qla4xxx                   5.01.03.2-7vmw.670.0.0.8169922        VMW      VMwareCertified     2019-12-27
sfvmk                          1.0.0.1003-6vmw.670.3.73.14320388     VMW      VMwareCertified     2019-12-27
shim-iscsi-linux-9-2-1-0       6.7.0-0.0.8169922                     VMW      VMwareCertified     2019-12-27
shim-iscsi-linux-9-2-2-0       6.7.0-0.0.8169922                     VMW      VMwareCertified     2019-12-27
shim-libata-9-2-1-0            6.7.0-0.0.8169922                     VMW      VMwareCertified     2019-12-27
shim-libata-9-2-2-0            6.7.0-0.0.8169922                     VMW      VMwareCertified     2019-12-27
shim-libfc-9-2-1-0             6.7.0-0.0.8169922                     VMW      VMwareCertified     2019-12-27
shim-libfc-9-2-2-0             6.7.0-0.0.8169922                     VMW      VMwareCertified     2019-12-27
shim-libfcoe-9-2-1-0           6.7.0-0.0.8169922                     VMW      VMwareCertified     2019-12-27
shim-libfcoe-9-2-2-0           6.7.0-0.0.8169922                     VMW      VMwareCertified     2019-12-27
shim-vmklinux-9-2-1-0          6.7.0-0.0.8169922                     VMW      VMwareCertified     2019-12-27
shim-vmklinux-9-2-2-0          6.7.0-0.0.8169922                     VMW      VMwareCertified     2019-12-27
shim-vmklinux-9-2-3-0          6.7.0-0.0.8169922                     VMW      VMwareCertified     2019-12-27
smartpqi                       1.0.1.553-28vmw.670.3.73.14320388     VMW      VMwareCertified     2019-12-27
uhci-usb-uhci                  1.0-3vmw.670.0.0.8169922              VMW      VMwareCertified     2019-12-27
usb-storage-usb-storage        1.0-3vmw.670.0.0.8169922              VMW      VMwareCertified     2019-12-27
usbcore-usb                    1.0-3vmw.670.0.0.8169922              VMW      VMwareCertified     2019-12-27
vmkata                         0.1-1vmw.670.0.0.8169922              VMW      VMwareCertified     2019-12-27
vmkfcoe                        1.0.0.1-1vmw.670.1.28.10302608        VMW      VMwareCertified     2019-12-27
vmkplexer-vmkplexer            6.7.0-0.0.8169922                     VMW      VMwareCertified     2019-12-27
vmkusb                         0.1-1vmw.670.3.89.15160138            VMW      VMwareCertified     2019-12-27
vmw-ahci                       1.2.8-1vmw.670.3.73.14320388          VMW      VMwareCertified     2019-12-27
xhci-xhci                      1.0-3vmw.670.0.0.8169922              VMW      VMwareCertified     2019-12-27
cpu-microcode                  6.7.0-3.77.15018017                   VMware   VMwareCertified     2019-12-27
elx-esx-libelxima.so           11.4.1184.2-3.89.15160138             VMware   VMwareCertified     2019-12-27
esx-base                       6.7.0-3.89.15160138                   VMware   VMwareCertified     2019-12-27
esx-dvfilter-generic-fastpath  6.7.0-0.0.8169922                     VMware   VMwareCertified     2019-12-27
esx-ui                         1.33.4-14093553                       VMware   VMwareCertified     2019-12-27
esx-update                     6.7.0-3.89.15160138                   VMware   VMwareCertified     2019-12-27
esx-xserver                    6.7.0-3.73.14320388                   VMware   VMwareCertified     2019-12-27
lsu-hp-hpsa-plugin             2.0.0-16vmw.670.1.28.10302608         VMware   VMwareCertified     2019-12-27
lsu-intel-vmd-plugin           1.0.0-2vmw.670.1.28.10302608          VMware   VMwareCertified     2019-12-27
lsu-lsi-drivers-plugin         1.0.0-1vmw.670.2.48.13006603          VMware   VMwareCertified     2019-12-27
lsu-lsi-lsi-mr3-plugin         1.0.0-13vmw.670.1.28.10302608         VMware   VMwareCertified     2019-12-27
lsu-lsi-lsi-msgpt3-plugin      1.0.0-9vmw.670.2.48.13006603          VMware   VMwareCertified     2019-12-27
lsu-lsi-megaraid-sas-plugin    1.0.0-9vmw.670.0.0.8169922            VMware   VMwareCertified     2019-12-27
lsu-lsi-mpt2sas-plugin         2.0.0-7vmw.670.0.0.8169922            VMware   VMwareCertified     2019-12-27
lsu-smartpqi-plugin            1.0.0-3vmw.670.1.28.10302608          VMware   VMwareCertified     2019-12-27
native-misc-drivers            6.7.0-3.89.15160138                   VMware   VMwareCertified     2019-12-27
qlnativefc                     3.1.8.0-5vmw.670.3.73.14320388        VMware   VMwareCertified     2019-12-27
rste                           2.0.2.0088-7vmw.670.0.0.8169922       VMware   VMwareCertified     2019-12-27
vmware-esx-esxcli-nvme-plugin  1.2.0.36-2.48.13006603                VMware   VMwareCertified     2019-12-27
vsan                           6.7.0-3.89.14840357                   VMware   VMwareCertified     2019-12-27
vsanhealth                     6.7.0-3.89.14840358                   VMware   VMwareCertified     2019-12-27
tools-light                    11.0.1.14773994-15160134              VMware   VMwareCertified     2019-12-27
```

</details>

不难看出`Intel`用的是`igbn`这个库，于是大胆移除`net55-r8168`
``` bash
[yuangezhizao@VM:~] esxcli software vib get -n net55-r8168
Realtek_bootbank_net55-r8168_8.045a-napi
   Name: net55-r8168
   Version: 8.045a-napi
   Type: bootbank
   Vendor: Realtek
   Acceptance Level: CommunitySupported
   Summary: Driver for Realtek 8111/8168
   Description: Recent driver for Realtek 8111/8168. Based on original Realtek drivers
   ReferenceURLs: kb|https://vibsdepot.v-front.de/wiki/index.php/Net55-r8168
   Creation Date: 2018-04-16
   Depends: vmkapi_2_2_0_0, com.vmware.driverAPI-9.2.2.0
   Conflicts: net51-drivers
   Replaces: net-r8168
   Provides: 
   Maintenance Mode Required: True
   Hardware Platforms Required: 
   Live Install Allowed: False
   Live Remove Allowed: False
   Stateless Ready: True
   Overlay: False
   Tags: driver, module
   Payloads: net55-r8
[yuangezhizao@VM:~] esxcli software vib remove -n net55-r8168
Removal Result
   Message: The update completed successfully, but the system needs to be rebooted for the changes to be effective.
   Reboot Required: true
   VIBs Installed: 
   VIBs Removed: Realtek_bootbank_net55-r8168_8.045a-napi
   VIBs Skipped: 
```
立即重新升级
``` bash
[yuangezhizao@VM:~] esxcli software vib update -d /vmfs/volumes/5d5d97d2-f9f4fe8f-7361-2c56dc945d15/VMware-ESXi-7.0.0
-15843807-depot.zip 
Installation Result
   Message: The update completed successfully, but the system needs to be rebooted for the changes to be effective.
   Reboot Required: true
   VIBs Installed: VMW_bootbank_bnxtnet_216.0.50.0-4vmw.700.1.0.15843807, VMW_bootbank_bnxtroce_216.0.58.0-1vmw.700.1.0.15843807, VMW_bootbank_brcmfcoe_12.0.1500.0-1vmw.700.1.0.15843807, VMW_bootbank_elxiscsi_12.0.1200.0-1vmw.700.1.0.15843807, VMW_bootbank_elxnet_12.0.1250.0-5vmw.700.1.0.15843807, VMW_bootbank_i40en_1.8.1.16-1vmw.700.1.0.15843807, VMW_bootbank_iavmd_2.0.0.1055-3vmw.700.1.0.15843807, VMW_bootbank_igbn_0.1.1.0-6vmw.700.1.0.15843807, VMW_bootbank_iser_1.1.0.0-1vmw.700.1.0.15843807, VMW_bootbank_ixgben_1.7.1.26-1vmw.700.1.0.15843807, VMW_bootbank_lpfc_12.4.293.3-5vmw.700.1.0.15843807, VMW_bootbank_lpnic_11.4.62.0-1vmw.700.1.0.15843807, VMW_bootbank_lsi-mr3_7.712.50.00-1vmw.700.1.0.15843807, VMW_bootbank_lsi-msgpt2_20.00.06.00-2vmw.700.1.0.15843807, VMW_bootbank_lsi-msgpt35_13.00.12.00-1vmw.700.1.0.15843807, VMW_bootbank_lsi-msgpt3_17.00.10.00-1vmw.700.1.0.15843807, VMW_bootbank_mtip32xx-native_3.9.8-1vmw.700.1.0.15843807, VMW_bootbank_ne1000_0.8.4-10vmw.700.1.0.15843807, VMW_bootbank_nenic_1.0.29.0-1vmw.700.1.0.15843807, VMW_bootbank_nfnic_4.0.0.44-1vmw.700.1.0.15843807, VMW_bootbank_nhpsa_2.0.50-1vmw.700.1.0.15843807, VMW_bootbank_nmlx4-core_3.19.16.7-1vmw.700.1.0.15843807, VMW_bootbank_nmlx4-en_3.19.16.7-1vmw.700.1.0.15843807, VMW_bootbank_nmlx4-rdma_3.19.16.7-1vmw.700.1.0.15843807, VMW_bootbank_nmlx5-core_4.19.16.7-1vmw.700.1.0.15843807, VMW_bootbank_nmlx5-rdma_4.19.16.7-1vmw.700.1.0.15843807, VMW_bootbank_ntg3_4.1.4.1-1vmw.700.1.0.15843807, VMW_bootbank_nvmxnet3-ens_2.0.0.22-1vmw.700.1.0.15843807, VMW_bootbank_nvmxnet3_2.0.0.30-1vmw.700.1.0.15843807, VMW_bootbank_pvscsi_0.1-2vmw.700.1.0.15843807, VMW_bootbank_qcnic_1.0.15.0-8vmw.700.1.0.15843807, VMW_bootbank_qedentv_3.12.1.0-23vmw.700.1.0.15843807, VMW_bootbank_qfle3_1.0.66.0-5vmw.700.1.0.15843807, VMW_bootbank_qfle3f_1.0.51.0-12vmw.700.1.0.15843807, VMW_bootbank_qfle3i_1.0.15.0-6vmw.700.1.0.15843807, VMW_bootbank_qflge_1.1.0.11-1vmw.700.1.0.15843807, VMW_bootbank_rste_2.0.2.0088-7vmw.700.1.0.15843807, VMW_bootbank_sfvmk_2.0.0.1004-3vmw.700.1.0.15843807, VMW_bootbank_smartpqi_1.0.4.3011-1vmw.700.1.0.15843807, VMW_bootbank_vmkata_0.1-1vmw.700.1.0.15843807, VMW_bootbank_vmkfcoe_1.0.0.2-1vmw.700.1.0.15843807, VMW_bootbank_vmkusb_0.1-1vmw.700.1.0.15843807, VMW_bootbank_vmw-ahci_1.3.9-1vmw.700.1.0.15843807, VMware_bootbank_cpu-microcode_7.0.0-1.0.15843807, VMware_bootbank_elx-esx-libelxima.so_12.0.1200.0-2vmw.700.1.0.15843807, VMware_bootbank_esx-base_7.0.0-1.0.15843807, VMware_bootbank_esx-dvfilter-generic-fastpath_7.0.0-1.0.15843807, VMware_bootbank_esx-ui_1.34.0-15603211, VMware_bootbank_esx-update_7.0.0-1.0.15843807, VMware_bootbank_esx-xserver_7.0.0-1.0.15843807, VMware_bootbank_lsuv2-hpv2-hpsa-plugin_1.0.0-2vmw.700.1.0.15843807, VMware_bootbank_lsuv2-intelv2-nvme-vmd-plugin_1.0.0-2vmw.700.1.0.15843807, VMware_bootbank_lsuv2-lsiv2-drivers-plugin_1.0.0-2vmw.700.1.0.15843807, VMware_bootbank_lsuv2-smartpqiv2-plugin_1.0.0-3vmw.700.1.0.15843807, VMware_bootbank_native-misc-drivers_7.0.0-1.0.15843807, VMware_bootbank_qlnativefc_4.0.1.0-3vmw.700.1.0.15843807, VMware_bootbank_vmware-esx-esxcli-nvme-plugin_1.2.0.37-1vmw.700.1.0.15843807, VMware_bootbank_vsan_7.0.0-1.0.15843807, VMware_bootbank_vsanhealth_7.0.0-1.0.15843807, VMware_locker_tools-light_11.0.5.15389592-15843807
   VIBs Removed: VMW_bootbank_ata-libata-92_3.00.9.2-16vmw.670.0.0.8169922, VMW_bootbank_ata-pata-amd_0.3.10-3vmw.670.0.0.8169922, VMW_bootbank_ata-pata-atiixp_0.4.6-4vmw.670.0.0.8169922, VMW_bootbank_ata-pata-cmd64x_0.2.5-3vmw.670.0.0.8169922, VMW_bootbank_ata-pata-hpt3x2n_0.3.4-3vmw.670.0.0.8169922, VMW_bootbank_ata-pata-pdc2027x_1.0-3vmw.670.0.0.8169922, VMW_bootbank_ata-pata-serverworks_0.4.3-3vmw.670.0.0.8169922, VMW_bootbank_ata-pata-sil680_0.4.8-3vmw.670.0.0.8169922, VMW_bootbank_ata-pata-via_0.3.3-2vmw.670.0.0.8169922, VMW_bootbank_block-cciss_3.6.14-10vmw.670.0.0.8169922, VMW_bootbank_bnxtnet_20.6.101.7-24vmw.670.3.73.14320388, VMW_bootbank_bnxtroce_20.6.101.0-20vmw.670.1.28.10302608, VMW_bootbank_brcmfcoe_11.4.1078.25-14vmw.670.3.73.14320388, VMW_bootbank_char-random_1.0-3vmw.670.0.0.8169922, VMW_bootbank_ehci-ehci-hcd_1.0-4vmw.670.0.0.8169922, VMW_bootbank_elxiscsi_11.4.1174.0-2vmw.670.0.0.8169922, VMW_bootbank_elxnet_11.4.1097.0-5vmw.670.3.73.14320388, VMW_bootbank_hid-hid_1.0-3vmw.670.0.0.8169922, VMW_bootbank_i40en_1.8.1.9-2vmw.670.3.73.14320388, VMW_bootbank_iavmd_1.2.0.1011-2vmw.670.0.0.8169922, VMW_bootbank_igbn_0.1.1.0-5vmw.670.3.73.14320388, VMW_bootbank_ima-qla4xxx_2.02.18-1vmw.670.0.0.8169922, VMW_bootbank_ipmi-ipmi-devintf_39.1-5vmw.670.1.28.10302608, VMW_bootbank_ipmi-ipmi-msghandler_39.1-5vmw.670.1.28.10302608, VMW_bootbank_ipmi-ipmi-si-drv_39.1-5vmw.670.1.28.10302608, VMW_bootbank_iser_1.0.0.0-1vmw.670.1.28.10302608, VMW_bootbank_ixgben_1.7.1.16-1vmw.670.3.73.14320388, VMW_bootbank_lpfc_11.4.33.25-14vmw.670.3.73.14320388, VMW_bootbank_lpnic_11.4.59.0-1vmw.670.0.0.8169922, VMW_bootbank_lsi-mr3_7.708.07.00-3vmw.670.3.73.14320388, VMW_bootbank_lsi-msgpt2_20.00.06.00-2vmw.670.3.73.14320388, VMW_bootbank_lsi-msgpt35_09.00.00.00-5vmw.670.3.73.14320388, VMW_bootbank_lsi-msgpt3_17.00.02.00-1vmw.670.3.73.14320388, VMW_bootbank_misc-cnic-register_1.78.75.v60.7-1vmw.670.0.0.8169922, VMW_bootbank_misc-drivers_6.7.0-2.48.13006603, VMW_bootbank_mtip32xx-native_3.9.8-1vmw.670.1.28.10302608, VMW_bootbank_ne1000_0.8.4-2vmw.670.2.48.13006603, VMW_bootbank_nenic_1.0.29.0-1vmw.670.3.73.14320388, VMW_bootbank_net-bnx2_2.2.4f.v60.10-2vmw.670.0.0.8169922, VMW_bootbank_net-bnx2x_1.78.80.v60.12-2vmw.670.0.0.8169922, VMW_bootbank_net-cdc-ether_1.0-3vmw.670.0.0.8169922, VMW_bootbank_net-cnic_1.78.76.v60.13-2vmw.670.0.0.8169922, VMW_bootbank_net-e1000_8.0.3.1-5vmw.670.0.0.8169922, VMW_bootbank_net-e1000e_3.2.2.1-2vmw.670.0.0.8169922, VMW_bootbank_net-enic_2.1.2.38-2vmw.670.0.0.8169922, VMW_bootbank_net-fcoe_1.0.29.9.3-7vmw.670.0.0.8169922, VMW_bootbank_net-forcedeth_0.61-2vmw.670.0.0.8169922, VMW_bootbank_net-igb_5.0.5.1.1-5vmw.670.0.0.8169922, VMW_bootbank_net-ixgbe_3.7.13.7.14iov-20vmw.670.0.0.8169922, VMW_bootbank_net-libfcoe-92_1.0.24.9.4-8vmw.670.0.0.8169922, VMW_bootbank_net-mlx4-core_1.9.7.0-1vmw.670.0.0.8169922, VMW_bootbank_net-mlx4-en_1.9.7.0-1vmw.670.0.0.8169922, VMW_bootbank_net-nx-nic_5.0.621-5vmw.670.0.0.8169922, VMW_bootbank_net-tg3_3.131d.v60.4-2vmw.670.0.0.8169922, VMW_bootbank_net-usbnet_1.0-3vmw.670.0.0.8169922, VMW_bootbank_net-vmxnet3_1.1.3.0-3vmw.670.3.89.15160138, VMW_bootbank_nfnic_4.0.0.29-0vmw.670.3.73.14320388, VMW_bootbank_nhpsa_2.0.22-3vmw.670.1.28.10302608, VMW_bootbank_nmlx4-core_3.17.13.1-1vmw.670.2.48.13006603, VMW_bootbank_nmlx4-en_3.17.13.1-1vmw.670.2.48.13006603, VMW_bootbank_nmlx4-rdma_3.17.13.1-1vmw.670.2.48.13006603, VMW_bootbank_nmlx5-core_4.17.13.1-1vmw.670.3.73.14320388, VMW_bootbank_nmlx5-rdma_4.17.13.1-1vmw.670.2.48.13006603, VMW_bootbank_ntg3_4.1.3.2-1vmw.670.1.28.10302608, VMW_bootbank_nvme_1.2.2.28-1vmw.670.3.73.14320388, VMW_bootbank_nvmxnet3-ens_2.0.0.21-1vmw.670.0.0.8169922, VMW_bootbank_nvmxnet3_2.0.0.29-1vmw.670.1.28.10302608, VMW_bootbank_ohci-usb-ohci_1.0-3vmw.670.0.0.8169922, VMW_bootbank_pvscsi_0.1-2vmw.670.0.0.8169922, VMW_bootbank_qcnic_1.0.2.0.4-1vmw.670.0.0.8169922, VMW_bootbank_qedentv_2.0.6.4-10vmw.670.1.28.10302608, VMW_bootbank_qfle3_1.0.50.11-9vmw.670.0.0.8169922, VMW_bootbank_qfle3f_1.0.25.0.2-14vmw.670.0.0.8169922, VMW_bootbank_qfle3i_1.0.2.3.9-3vmw.670.0.0.8169922, VMW_bootbank_qflge_1.1.0.11-1vmw.670.0.0.8169922, VMW_bootbank_sata-ahci_3.0-26vmw.670.0.0.8169922, VMW_bootbank_sata-ata-piix_2.12-10vmw.670.0.0.8169922, VMW_bootbank_sata-sata-nv_3.5-4vmw.670.0.0.8169922, VMW_bootbank_sata-sata-promise_2.12-3vmw.670.0.0.8169922, VMW_bootbank_sata-sata-sil24_1.1-1vmw.670.0.0.8169922, VMW_bootbank_sata-sata-sil_2.3-4vmw.670.0.0.8169922, VMW_bootbank_sata-sata-svw_2.3-3vmw.670.0.0.8169922, VMW_bootbank_scsi-aacraid_1.1.5.1-9vmw.670.0.0.8169922, VMW_bootbank_scsi-adp94xx_1.0.8.12-6vmw.670.0.0.8169922, VMW_bootbank_scsi-aic79xx_3.1-6vmw.670.0.0.8169922, VMW_bootbank_scsi-bnx2fc_1.78.78.v60.8-1vmw.670.0.0.8169922, VMW_bootbank_scsi-bnx2i_2.78.76.v60.8-1vmw.670.0.0.8169922, VMW_bootbank_scsi-fnic_1.5.0.45-3vmw.670.0.0.8169922, VMW_bootbank_scsi-hpsa_6.0.0.84-3vmw.670.0.0.8169922, VMW_bootbank_scsi-ips_7.12.05-4vmw.670.0.0.8169922, VMW_bootbank_scsi-iscsi-linux-92_1.0.0.2-3vmw.670.0.0.8169922, VMW_bootbank_scsi-libfc-92_1.0.40.9.3-5vmw.670.0.0.8169922, VMW_bootbank_scsi-megaraid-mbox_2.20.5.1-6vmw.670.0.0.8169922, VMW_bootbank_scsi-megaraid-sas_6.603.55.00-2vmw.670.0.0.8169922, VMW_bootbank_scsi-megaraid2_2.00.4-9vmw.670.0.0.8169922, VMW_bootbank_scsi-mpt2sas_19.00.00.00-2vmw.670.0.0.8169922, VMW_bootbank_scsi-mptsas_4.23.01.00-10vmw.670.0.0.8169922, VMW_bootbank_scsi-mptspi_4.23.01.00-10vmw.670.0.0.8169922, VMW_bootbank_scsi-qla4xxx_5.01.03.2-7vmw.670.0.0.8169922, VMW_bootbank_sfvmk_1.0.0.1003-6vmw.670.3.73.14320388, VMW_bootbank_shim-iscsi-linux-9-2-1-0_6.7.0-0.0.8169922, VMW_bootbank_shim-iscsi-linux-9-2-2-0_6.7.0-0.0.8169922, VMW_bootbank_shim-libata-9-2-1-0_6.7.0-0.0.8169922, VMW_bootbank_shim-libata-9-2-2-0_6.7.0-0.0.8169922, VMW_bootbank_shim-libfc-9-2-1-0_6.7.0-0.0.8169922, VMW_bootbank_shim-libfc-9-2-2-0_6.7.0-0.0.8169922, VMW_bootbank_shim-libfcoe-9-2-1-0_6.7.0-0.0.8169922, VMW_bootbank_shim-libfcoe-9-2-2-0_6.7.0-0.0.8169922, VMW_bootbank_shim-vmklinux-9-2-1-0_6.7.0-0.0.8169922, VMW_bootbank_shim-vmklinux-9-2-2-0_6.7.0-0.0.8169922, VMW_bootbank_shim-vmklinux-9-2-3-0_6.7.0-0.0.8169922, VMW_bootbank_smartpqi_1.0.1.553-28vmw.670.3.73.14320388, VMW_bootbank_uhci-usb-uhci_1.0-3vmw.670.0.0.8169922, VMW_bootbank_usb-storage-usb-storage_1.0-3vmw.670.0.0.8169922, VMW_bootbank_usbcore-usb_1.0-3vmw.670.0.0.8169922, VMW_bootbank_vmkata_0.1-1vmw.670.0.0.8169922, VMW_bootbank_vmkfcoe_1.0.0.1-1vmw.670.1.28.10302608, VMW_bootbank_vmkplexer-vmkplexer_6.7.0-0.0.8169922, VMW_bootbank_vmkusb_0.1-1vmw.670.3.89.15160138, VMW_bootbank_vmw-ahci_1.2.8-1vmw.670.3.73.14320388, VMW_bootbank_xhci-xhci_1.0-3vmw.670.0.0.8169922, VMware_bootbank_cpu-microcode_6.7.0-3.77.15018017, VMware_bootbank_elx-esx-libelxima.so_11.4.1184.2-3.89.15160138, VMware_bootbank_esx-base_6.7.0-3.89.15160138, VMware_bootbank_esx-dvfilter-generic-fastpath_6.7.0-0.0.8169922, VMware_bootbank_esx-ui_1.33.4-14093553, VMware_bootbank_esx-update_6.7.0-3.89.15160138, VMware_bootbank_esx-xserver_6.7.0-3.73.14320388, VMware_bootbank_lsu-hp-hpsa-plugin_2.0.0-16vmw.670.1.28.10302608, VMware_bootbank_lsu-intel-vmd-plugin_1.0.0-2vmw.670.1.28.10302608, VMware_bootbank_lsu-lsi-drivers-plugin_1.0.0-1vmw.670.2.48.13006603, VMware_bootbank_lsu-lsi-lsi-mr3-plugin_1.0.0-13vmw.670.1.28.10302608, VMware_bootbank_lsu-lsi-lsi-msgpt3-plugin_1.0.0-9vmw.670.2.48.13006603, VMware_bootbank_lsu-lsi-megaraid-sas-plugin_1.0.0-9vmw.670.0.0.8169922, VMware_bootbank_lsu-lsi-mpt2sas-plugin_2.0.0-7vmw.670.0.0.8169922, VMware_bootbank_lsu-smartpqi-plugin_1.0.0-3vmw.670.1.28.10302608, VMware_bootbank_native-misc-drivers_6.7.0-3.89.15160138, VMware_bootbank_qlnativefc_3.1.8.0-5vmw.670.3.73.14320388, VMware_bootbank_rste_2.0.2.0088-7vmw.670.0.0.8169922, VMware_bootbank_vmware-esx-esxcli-nvme-plugin_1.2.0.36-2.48.13006603, VMware_bootbank_vsan_6.7.0-3.89.14840357, VMware_bootbank_vsanhealth_6.7.0-3.89.14840358, VMware_locker_tools-light_11.0.1.14773994-15160134
   VIBs Skipped: VMW_bootbank_brcmnvmefc_12.4.293.2-3vmw.700.1.0.15843807, VMW_bootbank_i40iwn_1.1.2.5-1vmw.700.1.0.15843807, VMW_bootbank_nvme-pcie_1.2.2.13-1vmw.700.1.0.15843807, VMW_bootbank_nvmerdma_1.0.0.0-1vmw.700.1.0.15843807, VMW_bootbank_qedrntv_3.12.1.2-12vmw.700.1.0.15843807, VMware_bootbank_crx_7.0.0-1.0.15843807, VMware_bootbank_loadesx_7.0.0-1.0.15843807, VMware_bootbank_lsuv2-nvme-pcie-plugin_1.0.0-1vmw.700.1.0.15843807, VMware_bootbank_lsuv2-oem-dell-plugin_1.0.0-1vmw.700.1.0.15843807, VMware_bootbank_lsuv2-oem-hp-plugin_1.0.0-1vmw.700.1.0.15843807, VMware_bootbank_lsuv2-oem-lenovo-plugin_1.0.0-1vmw.700.1.0.15843807, VMware_bootbank_vdfs_7.0.0-1.0.15843807
```
重启
``` bash
[yuangezhizao@VM:~] reboot
[yuangezhizao@VM:~] Connection closing...Socket close.

Connection closed by foreign host.

Disconnected from remote host(ESXi) at 01:46:40.

Type `help' to learn how to use Xshell prompt.
[D:\~]$ 
```
开机之后重新查看列表确信升级完成，退出**维护模式**

<details><summary>点击此处 ← 查看终端</summary>

``` bash
Host 'esxi.yuangezhizao.cn' resolved to 192.168.25.249.
Connecting to 192.168.25.249:22...
Connection established.
To escape to local shell, press 'Ctrl+Alt+]'.

The time and date of this login have been sent to the system logs.

WARNING:
   All commands run on the ESXi shell are logged and may be included in
   support bundles. Do not provide passwords directly on the command line.
   Most tools can prompt for secrets or accept them from standard input.

VMware offers supported, powerful system administration tools.  Please
see www.vmware.com/go/sysadmintools for details.

The ESXi Shell can be disabled by an administrative user. See the
vSphere Security documentation for more information.
[yuangezhizao@VM:~] esxcli software vib list
Name                           Version                            Vendor  Acceptance Level  Install Date
-----------------------------  ---------------------------------  ------  ----------------  ------------
bnxtnet                        216.0.50.0-4vmw.700.1.0.15843807   VMW     VMwareCertified   2020-04-03
bnxtroce                       216.0.58.0-1vmw.700.1.0.15843807   VMW     VMwareCertified   2020-04-03
brcmfcoe                       12.0.1500.0-1vmw.700.1.0.15843807  VMW     VMwareCertified   2020-04-03
elxiscsi                       12.0.1200.0-1vmw.700.1.0.15843807  VMW     VMwareCertified   2020-04-03
elxnet                         12.0.1250.0-5vmw.700.1.0.15843807  VMW     VMwareCertified   2020-04-03
i40en                          1.8.1.16-1vmw.700.1.0.15843807     VMW     VMwareCertified   2020-04-03
iavmd                          2.0.0.1055-3vmw.700.1.0.15843807   VMW     VMwareCertified   2020-04-03
igbn                           0.1.1.0-6vmw.700.1.0.15843807      VMW     VMwareCertified   2020-04-03
iser                           1.1.0.0-1vmw.700.1.0.15843807      VMW     VMwareCertified   2020-04-03
ixgben                         1.7.1.26-1vmw.700.1.0.15843807     VMW     VMwareCertified   2020-04-03
lpfc                           12.4.293.3-5vmw.700.1.0.15843807   VMW     VMwareCertified   2020-04-03
lpnic                          11.4.62.0-1vmw.700.1.0.15843807    VMW     VMwareCertified   2020-04-03
lsi-mr3                        7.712.50.00-1vmw.700.1.0.15843807  VMW     VMwareCertified   2020-04-03
lsi-msgpt2                     20.00.06.00-2vmw.700.1.0.15843807  VMW     VMwareCertified   2020-04-03
lsi-msgpt35                    13.00.12.00-1vmw.700.1.0.15843807  VMW     VMwareCertified   2020-04-03
lsi-msgpt3                     17.00.10.00-1vmw.700.1.0.15843807  VMW     VMwareCertified   2020-04-03
mtip32xx-native                3.9.8-1vmw.700.1.0.15843807        VMW     VMwareCertified   2020-04-03
ne1000                         0.8.4-10vmw.700.1.0.15843807       VMW     VMwareCertified   2020-04-03
nenic                          1.0.29.0-1vmw.700.1.0.15843807     VMW     VMwareCertified   2020-04-03
nfnic                          4.0.0.44-1vmw.700.1.0.15843807     VMW     VMwareCertified   2020-04-03
nhpsa                          2.0.50-1vmw.700.1.0.15843807       VMW     VMwareCertified   2020-04-03
nmlx4-core                     3.19.16.7-1vmw.700.1.0.15843807    VMW     VMwareCertified   2020-04-03
nmlx4-en                       3.19.16.7-1vmw.700.1.0.15843807    VMW     VMwareCertified   2020-04-03
nmlx4-rdma                     3.19.16.7-1vmw.700.1.0.15843807    VMW     VMwareCertified   2020-04-03
nmlx5-core                     4.19.16.7-1vmw.700.1.0.15843807    VMW     VMwareCertified   2020-04-03
nmlx5-rdma                     4.19.16.7-1vmw.700.1.0.15843807    VMW     VMwareCertified   2020-04-03
ntg3                           4.1.4.1-1vmw.700.1.0.15843807      VMW     VMwareCertified   2020-04-03
nvmxnet3-ens                   2.0.0.22-1vmw.700.1.0.15843807     VMW     VMwareCertified   2020-04-03
nvmxnet3                       2.0.0.30-1vmw.700.1.0.15843807     VMW     VMwareCertified   2020-04-03
pvscsi                         0.1-2vmw.700.1.0.15843807          VMW     VMwareCertified   2020-04-03
qcnic                          1.0.15.0-8vmw.700.1.0.15843807     VMW     VMwareCertified   2020-04-03
qedentv                        3.12.1.0-23vmw.700.1.0.15843807    VMW     VMwareCertified   2020-04-03
qfle3                          1.0.66.0-5vmw.700.1.0.15843807     VMW     VMwareCertified   2020-04-03
qfle3f                         1.0.51.0-12vmw.700.1.0.15843807    VMW     VMwareCertified   2020-04-03
qfle3i                         1.0.15.0-6vmw.700.1.0.15843807     VMW     VMwareCertified   2020-04-03
qflge                          1.1.0.11-1vmw.700.1.0.15843807     VMW     VMwareCertified   2020-04-03
rste                           2.0.2.0088-7vmw.700.1.0.15843807   VMW     VMwareCertified   2020-04-03
sfvmk                          2.0.0.1004-3vmw.700.1.0.15843807   VMW     VMwareCertified   2020-04-03
smartpqi                       1.0.4.3011-1vmw.700.1.0.15843807   VMW     VMwareCertified   2020-04-03
vmkata                         0.1-1vmw.700.1.0.15843807          VMW     VMwareCertified   2020-04-03
vmkfcoe                        1.0.0.2-1vmw.700.1.0.15843807      VMW     VMwareCertified   2020-04-03
vmkusb                         0.1-1vmw.700.1.0.15843807          VMW     VMwareCertified   2020-04-03
vmw-ahci                       1.3.9-1vmw.700.1.0.15843807        VMW     VMwareCertified   2020-04-03
cpu-microcode                  7.0.0-1.0.15843807                 VMware  VMwareCertified   2020-04-03
elx-esx-libelxima.so           12.0.1200.0-2vmw.700.1.0.15843807  VMware  VMwareCertified   2020-04-03
esx-base                       7.0.0-1.0.15843807                 VMware  VMwareCertified   2020-04-03
esx-dvfilter-generic-fastpath  7.0.0-1.0.15843807                 VMware  VMwareCertified   2020-04-03
esx-ui                         1.34.0-15603211                    VMware  VMwareCertified   2020-04-03
esx-update                     7.0.0-1.0.15843807                 VMware  VMwareCertified   2020-04-03
esx-xserver                    7.0.0-1.0.15843807                 VMware  VMwareCertified   2020-04-03
lsuv2-hpv2-hpsa-plugin         1.0.0-2vmw.700.1.0.15843807        VMware  VMwareCertified   2020-04-03
lsuv2-intelv2-nvme-vmd-plugin  1.0.0-2vmw.700.1.0.15843807        VMware  VMwareCertified   2020-04-03
lsuv2-lsiv2-drivers-plugin     1.0.0-2vmw.700.1.0.15843807        VMware  VMwareCertified   2020-04-03
lsuv2-smartpqiv2-plugin        1.0.0-3vmw.700.1.0.15843807        VMware  VMwareCertified   2020-04-03
native-misc-drivers            7.0.0-1.0.15843807                 VMware  VMwareCertified   2020-04-03
qlnativefc                     4.0.1.0-3vmw.700.1.0.15843807      VMware  VMwareCertified   2020-04-03
vmware-esx-esxcli-nvme-plugin  1.2.0.37-1vmw.700.1.0.15843807     VMware  VMwareCertified   2020-04-03
vsan                           7.0.0-1.0.15843807                 VMware  VMwareCertified   2020-04-03
vsanhealth                     7.0.0-1.0.15843807                 VMware  VMwareCertified   2020-04-03
tools-light                    11.0.5.15389592-15843807           VMware  VMwareCertified   2020-04-03
[yuangezhizao@VM:~] vim-cmd hostsvc/maintenance_mode_exit
[yuangezhizao@VM:~] 
```

</details>

最后分配个许可证就搞定了

![7.0.0 (Build 15843807)](https://i1.yuangezhizao.cn/Win-10/20200404020258.jpg!webp)
![JJ2WR-25L9P-H71A8-6J20P-C0K3F](https://i1.yuangezhizao.cn/Win-10/20200404020428.jpg!webp)

### 封装含有`Realtek 8168`网卡驱动的离线包
### 1.`PowerShell`大法
设置`PowerShell`执行策略：`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned`
安装`VMware PowerCLI`模块：`Install-Module -Name VMware.PowerCLI`
然后竟然炸了？
``` powershell
Microsoft Windows [版本 10.0.17763.914]
(c) 2018 Microsoft Corporation。保留所有权利。

C:\Windows\system32>ps
'ps' 不是内部或外部命令，也不是可运行的程序
或批处理文件。

C:\Windows\system32>powershell
Windows PowerShell
版权所有 (C) Microsoft Corporation。保留所有权利。

PS C:\Windows\system32> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
PS C:\Windows\system32> Install-Module -Name VMware.PowerCLI -Scope AllUsers

需要使用 NuGet 提供程序来继续操作
PowerShellGet 需要使用 NuGet 提供程序“2.8.5.201”或更高版本来与基于 NuGet 的存储库交互。必须在“C:\Program
Files\PackageManagement\ProviderAssemblies”或“C:\Users\yuangezhizao\AppData\Local\PackageManagement\ProviderAssemblie
s”中提供 NuGet 提供程序。也可以通过运行 'Install-PackageProvider -Name NuGet -MinimumVersion 2.8.5.201 -Force' 安装
NuGet 提供程序。是否要让 PowerShellGet 立即安装并导入 NuGet 提供程序?
[Y] 是(Y)  [N] 否(N)  [S] 暂停(S)  [?] 帮助 (默认值为“Y”): Y
PackageManagement\Install-Package : 找不到与指定的搜索条件和程序包名称“VMware.PowerCLI”匹配的项目。请尝试使用 Get-PSR
epository 查看所有可用的注册程序包源。
所在位置 C:\Program Files\WindowsPowerShell\Modules\PowerShellGet\1.0.0.1\PSModule.psm1:1809 字符: 21
+ ...          $null = PackageManagement\Install-Package @PSBoundParameters
+                      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : ObjectNotFound: (Microsoft.Power....InstallPackage:InstallPackage) [Install-Package], Ex
   ception
    + FullyQualifiedErrorId : NoMatchFoundForCriteria,Microsoft.PowerShell.PackageManagement.Cmdlets.InstallPackage

PS C:\Windows\system32> Install-Module -Name VMware.PowerCLI -Scope AllUsers
PackageManagement\Install-Package : 找不到与指定的搜索条件和程序包名称“VMware.PowerCLI”匹配的项目。请尝试使用 Get-PSR
epository 查看所有可用的注册程序包源。
所在位置 C:\Program Files\WindowsPowerShell\Modules\PowerShellGet\1.0.0.1\PSModule.psm1:1809 字符: 21
+ ...          $null = PackageManagement\Install-Package @PSBoundParameters
+                      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : ObjectNotFound: (Microsoft.Power....InstallPackage:InstallPackage) [Install-Package], Ex
   ception
    + FullyQualifiedErrorId : NoMatchFoundForCriteria,Microsoft.PowerShell.PackageManagement.Cmdlets.InstallPackage

PS C:\Windows\system32>
```
只好去[官网](https://web.archive.org/web/20191227145019/https://www.vmware.com/support/developer/PowerCLI/index.html)手动下载安装

![最新 6.5.4 ？](https://i1.yuangezhizao.cn/Win-10/20191227225050.jpg!webp)
![网奇慢，好久才进到这个页面](https://i1.yuangezhizao.cn/Win-10/20191227225756.jpg!webp)

翻了一大圈，才看到没有[新版本](https://web.archive.org/web/20191227150657/https://blogs.vmware.com/PowerCLI/2018/04/new-release-vmware-powercli-10-1-0.html%23comment-33455)下载地址的原因？
![因为这玩楞会自动升级](https://i1.yuangezhizao.cn/Win-10/20191227230512.jpg!webp)

以及[404](https://web.archive.org/web/20191227150707/https://blogs.vmware.com/PowerCLI/2017/05/powercli-6-5-1-install-walkthrough.html)的可能性之一
![也就是说网炸了？](https://i1.yuangezhizao.cn/Win-10/20191227230855.jpg!webp)
![草](https://i1.yuangezhizao.cn/Win-10/20191016005155.jpg!webp)

最终只好[离线安装](https://code.vmware.com/web/tool/11.5.0/vmware-powercli)，然后就出现了如下的一幕
![11.5.0](https://i1.yuangezhizao.cn/Win-10/20191227231533.jpg!webp)
![草 * 2](https://i1.yuangezhizao.cn/Win-10/20191016005155.jpg!webp)
![才看到原来这里写明了新版本会在新地址发布](https://i1.yuangezhizao.cn/Win-10/20191227233138.jpg!webp)

[真·官网](https://web.archive.org/web/20191227151927/https://code.vmware.com/web/tool/11.5.0/vmware-powercli)下载之后解压到模块目录下：`C:\Windows\System32\WindowsPowerShell\v1.0\Modules`，~~顺手把`VMware-PowerCLI-11.5.0-14912921`重命名为了`VMware-PowerCLI`~~
`2019-12-28 01:14:06`终于找到了导入不能的解决方法，那就是解压完不要嵌套文件夹，要直接放在`Modules`目录下……
最后导入模块：`Import-Module VMware.PowerCLI`
附：
关闭`CEIP（Customer Experience Improvement Program）`：`Set-PowerCLIConfiguration -Scope User -ParticipateInCEIP $false`
忽略证书验证：`Set-PowerCLIConfiguration -InvalidCertificateAction Ignore`
![完美离线导入](https://i1.yuangezhizao.cn/Win-10/20191228011727.jpg!webp)
![成功登录](https://i1.yuangezhizao.cn/Win-10/20191228014148.png!webp)

<details><summary>点击此处 ← 查看终端</summary>

``` powershell
PS C:\Users\yuangezhizao> $env:PSModulePath
D:\yuangezhizao\Documents\WindowsPowerShell\Modules;C:\Program Files\WindowsPowerShell\Modules;C:\Windows\system32\WindowsPowerShell\v1.0\Modules
PS C:\Users\yuangezhizao> Import-Module VMware.PowerCLI
警告: Please consider joining the VMware Customer Experience Improvement Program, so you can help us make PowerCLI a
better product. You can join using the following command:

Set-PowerCLIConfiguration -Scope User -ParticipateInCEIP $true

VMware's Customer Experience Improvement Program ("CEIP") provides VMware with information that enables VMware to
improve its products and services, to fix problems, and to advise you on how best to deploy and use our products.  As
part of the CEIP, VMware collects technical information about your organization抯 use of VMware products and services
on a regular basis in association with your organization抯 VMware license key(s).  This information does not personally
 identify any individual.

For more details: type "help about_ceip" to see the related help article.

To disable this warning and set your preference use the following command and restart PowerShell:
Set-PowerCLIConfiguration -Scope User -ParticipateInCEIP $true or $false.
          Welcome to VMware PowerCLI!

Log in to a vCenter Server or ESX host:              Connect-VIServer
To find out what commands are available, type:       Get-VICommand
To show searchable help for all PowerCLI commands:   Get-PowerCLIHelp
Once you've connected, display all virtual machines: Get-VM
If you need more help, visit the PowerCLI community: Get-PowerCLICommunity

       Copyright (C) VMware, Inc. All rights reserved.


PS C:\Users\yuangezhizao> Set-PowerCLIConfiguration -Scope User -ParticipateInCEIP $false

Perform operation?
Performing operation 'Update PowerCLI configuration.'?
[Y] 是(Y)  [A] 全是(A)  [N] 否(N)  [L] 全否(L)  [S] 暂停(S)  [?] 帮助 (默认值为“Y”): Y

Scope    ProxyPolicy     DefaultVIServerMode InvalidCertificateAction  DisplayDeprecationWarnings WebOperationTimeout
                                                                                                  Seconds
-----    -----------     ------------------- ------------------------  -------------------------- -------------------
Session  UseSystemProxy  Multiple            Unset                     True                       300
User
AllUsers


PS C:\Users\yuangezhizao> Set-PowerCLIConfiguration -InvalidCertificateAction Ignore

Perform operation?
Performing operation 'Update PowerCLI configuration.'?
[Y] 是(Y)  [A] 全是(A)  [N] 否(N)  [L] 全否(L)  [S] 暂停(S)  [?] 帮助 (默认值为“Y”): Y

Scope    ProxyPolicy     DefaultVIServerMode InvalidCertificateAction  DisplayDeprecationWarnings WebOperationTimeout
                                                                                                  Seconds
-----    -----------     ------------------- ------------------------  -------------------------- -------------------
Session  UseSystemProxy  Multiple            Ignore                    True                       300
User                                         Ignore
AllUsers


PS C:\Users\yuangezhizao>
```
</details>

### 2.下载`ESXi-Customizer-PS`脚本
[VMware Front Experience: ESXi-Customizer-PS](https://web.archive.org/web/20191227135715/https://www.v-front.de/p/esxi-customizer-ps.html)
最新仍然是：`Version 2.6.0 (2018-04-18)`即`ESXi-Customizer-PS-v2.6.0.ps1`

<details><summary>点击此处 ← 查看源码</summary>

``` powershell
#############################################################################################################################
#
# ESXi-Customizer-PS.ps1 - a script to build a customized ESXi installation ISO using ImageBuilder
#
# Version:       2.6.0
# Author:        Andreas Peetz (ESXi-Customizer-PS@v-front.de)
# Info/Tutorial: https://esxi-customizer-ps.v-front.de/
#
# License:
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# A copy of the GNU General Public License is available at http://www.gnu.org/licenses/.
#
#############################################################################################################################

param(
    [string]$iZip = "",
    [string]$pkgDir = "",
    [string]$outDir = $(Split-Path $MyInvocation.MyCommand.Path),
    [string]$ipname = "",
    [string]$ipvendor = "",
    [string]$ipdesc = "",
    [switch]$vft = $false,
    [string[]]$dpt = @(),
    [string[]]$load = @(),
    [string[]]$remove = @(),
    [switch]$test = $false,
    [switch]$sip = $false,
    [switch]$nsc = $false,
    [switch]$help = $false,
    [switch]$ozip = $false,
    [switch]$v50 = $false,
    [switch]$v51 = $false,
    [switch]$v55 = $false,
    [switch]$v60 = $false,
    [switch]$v65 = $false,
    [switch]$v67 = $false,
    [switch]$update = $false,
    [string]$log = ($env:TEMP + "\ESXi-Customizer-PS-" + $PID + ".log")
)

# Constants
$ScriptName = "ESXi-Customizer-PS"
$ScriptVersion = "2.6.0"
$ScriptURL = "https://ESXi-Customizer-PS.v-front.de"

$AccLevel = @{"VMwareCertified" = 1; "VMwareAccepted" = 2; "PartnerSupported" = 3; "CommunitySupported" = 4}

# Online depot URLs
$vmwdepotURL = "https://hostupdate.vmware.com/software/VUM/PRODUCTION/main/vmw-depot-index.xml"
$vftdepotURL = "https://vibsdepot.v-front.de/"

# Function to update/add VIB package
function AddVIB2Profile($vib) {
    $AddVersion = $vib.Version
    $ExVersion = ($MyProfile.VibList | where { $_.Name -eq $vib.Name }).Version
    if ($AccLevel[$vib.AcceptanceLevel.ToString()] -gt $AccLevel[$MyProfile.AcceptanceLevel.ToString()]) {
        write-host -ForegroundColor Yellow -nonewline (" [New AcceptanceLevel: " + $vib.AcceptanceLevel + "]")
        $MyProfile.AcceptanceLevel = $vib.AcceptanceLevel
    }
    If ($MyProfile.VibList -contains $vib) {
        write-host -ForegroundColor Yellow " [IGNORED, already added]"
    } else {
        Add-EsxSoftwarePackage -SoftwarePackage $vib -Imageprofile $MyProfile -force -ErrorAction SilentlyContinue | Out-Null 
        if ($?) {
            if ($ExVersion -eq $null) {
                write-host -ForegroundColor Green " [OK, added]"
            } else {
                write-host -ForegroundColor Yellow (" [OK, replaced " + $ExVersion + "]")
            }
        } else {
            write-host -ForegroundColor Red " [FAILED, invalid package?]"
        }
    }
}

# Function to test if entered string is numeric
function isNumeric ($x) {
    $x2 = 0
    $isNum = [System.Int32]::TryParse($x, [ref]$x2)
    return $isNum
}

# Clean-up function
function cleanup() {
    Stop-Transcript | Out-Null
    if ($DefaultSoftwaredepots) { Remove-EsxSoftwaredepot $DefaultSoftwaredepots }
}

# Write info and help if requested
write-host ("`nThis is " + $ScriptName + " Version " + $ScriptVersion + " (visit " + $ScriptURL + " for more information!)")
if ($help) {
    write-host "`nUsage:"
    write-host "   ESXi-Customizer-PS [-help] | [-izip <bundle> [-update]] [-sip] [-v67|-v65|-v60|-v55|-v51|-v50]"
    write-host "                                [-ozip] [-pkgDir <dir>] [-outDir <dir>] [-vft] [-dpt depot1[,...]]"
    write-host "                                [-load vib1[,...]] [-remove vib1[,...]] [-log <file>] [-ipname <name>]"
	write-host "                                [-ipdesc <desc>] [-ipvendor <vendor>] [-nsc] [-test]"
    write-host "`nOptional parameters:"
    write-host "   -help              : display this help"
    write-host "   -izip <bundle>     : use the VMware Offline bundle <bundle> as input instead of the Online depot"
    write-host "   -update            : only with -izip, updates a local bundle with an ESXi patch from the VMware Online depot,"
    write-host "                        combine this with the matching ESXi version selection switch"
    write-host "   -pkgDir <dir>      : local directory of Offline bundles and/or VIB files to add (if any, no default)"
    write-host "   -ozip              : output an Offline bundle instead of an installation ISO"
    write-host "   -outDir <dir>      : directory to store the customized ISO or Offline bundle (the default is the"
    write-host "                        script directory. If specified the log file will also be moved here.)"
    write-host "   -vft               : connect the V-Front Online depot"
	write-host "   -dpt depot1[,...]  : connect additional Online depots by URL or local Offline bundles by file name"
    write-host "   -load vib1[,...]   : load additional packages from connected depots or Offline bundles"
    write-host "   -remove vib1[,...] : remove named VIB packages from the custom Imageprofile"
    write-host "   -sip               : select an Imageprofile from the current list"
    write-host "                        (default = auto-select latest available standard profile)"
    write-host "   -v67 | -v65 | -v60 |"
    write-host "   -v55 | -v51 | -v50 : Use only ESXi 6.7/6.5/6.0/5.5/5.1/5.0 Imageprofiles as input, ignore other versions"
    write-host "   -nsc               : use -NoSignatureCheck with export"
    write-host "   -log <file>        : Use custom log file <file>"
    write-host "   -ipname <name>"
    write-host "   -ipdesc <desc>"
    write-host "   -ipvendor <vendor> : provide a name, description and/or vendor for the customized"
    write-host "                        Imageprofile (the default is derived from the cloned input Imageprofile)"
    write-host "   -test              : skip package download and image build (for testing)`n"
    exit
} else {
    write-host "(Call with -help for instructions)"
    if (!($PSBoundParameters.ContainsKey('log')) -and $PSBoundParameters.ContainsKey('outDir')) {
        write-host ("`nTemporarily logging to " + $log + " ...")
    } else {
        write-host ("`nLogging to " + $log + " ...")
    }
    # Stop active transcript
    try { Stop-Transcript | out-null } catch {}
    # Start own transcript
    try { Start-Transcript -Path $log -Force -Confirm:$false | Out-Null } catch {
        write-host -ForegroundColor Red "`nFATAL ERROR: Log file cannot be opened. Bad file path or missing permission?`n"
        exit
    }
}

# The main try ...

$isModule = @{}
try {

# Check for and load required modules/snapins
foreach ($comp in "VMware.VimAutomation.Core", "VMware.ImageBuilder") {
    if (Get-Module -ListAvailable -Name $comp -ErrorAction:SilentlyContinue) {
		$isModule[$comp] = $true
        if (!(Get-Module -Name $comp -ErrorAction:SilentlyContinue)) {
            if (!(Import-Module -PassThru -Name $comp -ErrorAction:SilentlyContinue)) {
                write-host -ForegroundColor Red "`nFATAL ERROR: Failed to import the $comp module!`n"
                exit
            }
        }
    } else {
		$isModule[$comp] = $false
        if (Get-PSSnapin -Registered -Name $comp -ErrorAction:SilentlyContinue) {
            if (!(Get-PSSnapin -Name $comp -ErrorAction:SilentlyContinue)) {
                if (!(Add-PSSnapin -PassThru -Name $comp -ErrorAction:SilentlyContinue)) {
                    write-host -ForegroundColor Red "`nFATAL ERROR: Failed to add the $comp snapin!`n"
                    exit
                }
            }
        } else {
            write-host -ForegroundColor Red "`nFATAL ERROR: $comp is not available as a module or snapin! It looks like there is no compatible version of PowerCLI installed!`n"
            exit
        }
    }
}

# Parameter sanity check
if ( ($v50 -and ($v51 -or $v55 -or $v60 -or $v65 -or $v67)) -or ($v51 -and ($v55 -or $v60 -or $v65 -or $v67)) -or ($v55 -and ($v60 -or $v65 -or $v67)) -or ($v60 -and ($v65 -or $v67)) -or ($v65 -and $v67) ) {
    write-host -ForegroundColor Yellow "`nWARNING: Multiple ESXi versions specified. Highest version will take precedence!"
}
if ($update -and ($izip -eq "")) {
    write-host -ForegroundColor Red "`nFATAL ERROR: -update requires -izip!`n"
    exit
}

# Check PowerShell and PowerCLI version
if (!(Test-Path variable:PSVersionTable)) {
    write-host -ForegroundColor Red "`nFATAL ERROR: This script requires at least PowerShell version 2.0!`n"
    exit
}
$psv = $PSVersionTable.PSVersion | select Major,Minor

if ($isModule["VMware.VimAutomation.Core"]) {
	$pcvm = (get-module "VMware.VimAutomation.Core").Version
	write-host ("`nRunning with PowerShell version " + $psv.Major + "." + $psv.Minor + " and VMware PowerCLI version " + $pcvm)
} else {
	$pcv = Get-PowerCLIVersion | select major,minor,UserFriendlyVersion
	write-host ("`nRunning with PowerShell version " + $psv.Major + "." + $psv.Minor + " and " + $pcv.UserFriendlyVersion)
	if ( ($pcv.major -lt 5) -or (($pcv.major -eq 5) -and ($pcv.minor -eq 0)) ) {
		write-host -ForegroundColor Red "`nFATAL ERROR: This script requires at least PowerCLI version 5.1 !`n"
		exit
	}
}

if ($update) {
    # Try to add Offline bundle specified by -izip
    write-host -nonewline "`nAdding Base Offline bundle $izip (to be updated)..."
    if ($upddepot = Add-EsxSoftwaredepot $izip) {
        write-host -ForegroundColor Green " [OK]"
    } else {
        write-host -ForegroundColor Red "`nFATAL ERROR: Cannot add Base Offline bundle!`n"
        exit
    }
    if (!($CloneIP = Get-EsxImageprofile -Softwaredepot $upddepot)) {
        write-host -ForegroundColor Red "`nFATAL ERROR: No Imageprofiles found in Base Offline bundle!`n"
        exit
    }
    if ($CloneIP -is [system.array]) {
        # Input Offline bundle includes multiple Imageprofiles. Pick only the latest standard profile:
        write-host -ForegroundColor Yellow "Warning: Input Offline Bundle contains multiple Imageprofiles. Will pick the latest standard profile!"
        $CloneIP = @( $CloneIP | Sort-Object -Descending -Property @{Expression={$_.Name.Substring(0,10)}},@{Expression={$_.CreationTime.Date}},Name )[0]
    }
}

if (($izip -eq "") -or $update) {
    # Connect the VMware ESXi base depot
    write-host -nonewline "`nConnecting the VMware ESXi Online depot ..."
    if ($basedepot = Add-EsxSoftwaredepot $vmwdepotURL) {
        write-host -ForegroundColor Green " [OK]"
    } else {
        write-host -ForegroundColor Red "`nFATAL ERROR: Cannot add VMware ESXi Online depot. Please check your Internet connectivity and/or proxy settings!`n"
        exit
    }
} else {
    # Try to add Offline bundle specified by -izip
    write-host -nonewline "`nAdding base Offline bundle $izip ..."
    if ($basedepot = Add-EsxSoftwaredepot $izip) {
        write-host -ForegroundColor Green " [OK]"
    } else {
        write-host -ForegroundColor Red "`nFATAL ERROR: Cannot add VMware base Offline bundle!`n"
        exit
    }
}

if ($vft) {
    # Connect the V-Front Online depot
    write-host -nonewline "`nConnecting the V-Front Online depot ..."
    if ($vftdepot = Add-EsxSoftwaredepot $vftdepotURL) {
        write-host -ForegroundColor Green " [OK]"
    } else {
        write-host -ForegroundColor Red "`nFATAL ERROR: Cannot add the V-Front Online depot. Please check your internet connectivity and/or proxy settings!`n"
        exit
    }
}

if ($dpt -ne @()) {
	# Connect additional depots (Online depot or Offline bundle)
	$AddDpt = @()
	for ($i=0; $i -lt $dpt.Length; $i++ ) {
		write-host -nonewline ("`nConnecting additional depot " + $dpt[$i] + " ...")
		if ($AddDpt += Add-EsxSoftwaredepot $dpt[$i]) {
			write-host -ForegroundColor Green " [OK]"
		} else {
			write-host -ForegroundColor Red "`nFATAL ERROR: Cannot add Online depot or Offline bundle. In case of Online depot check your Internet"
            write-host -ForegroundColor Red "connectivity and/or proxy settings! In case of Offline bundle check file name, format and permissions!`n"
			exit
		}
	}

}

write-host -NoNewLine "`nGetting Imageprofiles, please wait ..."
$iplist = @()
if ($iZip -and !($update)) {
    Get-EsxImageprofile -Softwaredepot $basedepot | foreach { $iplist += $_ }
} else {
	if ($v67) {
		Get-EsxImageprofile "ESXi-6.7*" -Softwaredepot $basedepot | foreach { $iplist += $_ }
	} else {
		if ($v65) {
			Get-EsxImageprofile "ESXi-6.5*" -Softwaredepot $basedepot | foreach { $iplist += $_ }
		} else {
			if ($v60) {
				Get-EsxImageprofile "ESXi-6.0*" -Softwaredepot $basedepot | foreach { $iplist += $_ }
			} else {
				if ($v55) {
					Get-EsxImageprofile "ESXi-5.5*" -Softwaredepot $basedepot | foreach { $iplist += $_ }
				} else {
					if ($v51) {
						Get-EsxImageprofile "ESXi-5.1*" -Softwaredepot $basedepot | foreach { $iplist += $_ }
					} else {
						if ($v50) {
							Get-EsxImageprofile "ESXi-5.0*" -Softwaredepot $basedepot | foreach { $iplist += $_ }
						} else {
							# Workaround for http://kb.vmware.com/kb/2089217
							Get-EsxImageprofile "ESXi-5.0*" -Softwaredepot $basedepot | foreach { $iplist += $_ }
							Get-EsxImageprofile "ESXi-5.1*" -Softwaredepot $basedepot | foreach { $iplist += $_ }
							Get-EsxImageprofile "ESXi-5.5*" -Softwaredepot $basedepot | foreach { $iplist += $_ }
							Get-EsxImageprofile "ESXi-6.0*" -Softwaredepot $basedepot | foreach { $iplist += $_ }
							Get-EsxImageprofile "ESXi-6.5*" -Softwaredepot $basedepot | foreach { $iplist += $_ }
							Get-EsxImageprofile "ESXi-6.7*" -Softwaredepot $basedepot | foreach { $iplist += $_ }
						}
					}
				}
			}
		}
	}
}

if ($iplist.Length -eq 0) {
    write-host -ForegroundColor Red " [FAILED]`n`nFATAL ERROR: No valid Imageprofile(s) found!"
    if ($iZip) {
        write-host -ForegroundColor Red "The input file is probably not a full ESXi base bundle.`n"
    }
    exit
} else {
    write-host -ForegroundColor Green " [OK]"
    $iplist = @( $iplist | Sort-Object -Descending -Property @{Expression={$_.Name.Substring(0,10)}},@{Expression={$_.CreationTime.Date}},Name )
}

# if -sip then display menu of available image profiles ...
if ($sip) {
    if ($update) {
        write-host "`nSelect Imageprofile to use for update:"
    } else {
        write-host "`nSelect Base Imageprofile:"
    }
    write-host "-------------------------------------------"
    for ($i=0; $i -lt $iplist.Length; $i++ ) {
        write-host ($i+1): $iplist[$i].Name
    }
    write-host "-------------------------------------------"
    do {
        $sel = read-host "Enter selection"
        if (isNumeric $sel) {
            if (([int]$sel -lt 1) -or ([int]$sel -gt $iplist.Length)) { $sel = $null }
        } else {
            $sel = $null
        }
    } until ($sel)
    $idx = [int]$sel-1
} else {
    $idx = 0
}
if ($update) {
    $updIP = $iplist[$idx]
} else {
    $CloneIP = $iplist[$idx]
}

write-host ("`nUsing Imageprofile " + $CloneIP.Name + " ...")
write-host ("(dated " + $CloneIP.CreationTime + ", AcceptanceLevel: " + $CloneIP.AcceptanceLevel + ",")
write-host ($CloneIP.Description + ")")

# If customization is required ...
if ( ($pkgDir -ne "") -or $update -or ($load -ne @()) -or ($remove -ne @()) ) {

    # Create your own Imageprofile
    if ($ipname -eq "") { $ipname = $CloneIP.Name + "-customized" }
    if ($ipvendor -eq "") { $ipvendor = $CloneIP.Vendor }
    if ($ipdesc -eq "") { $ipdesc = $CloneIP.Description + " (customized)" }
    $MyProfile = New-EsxImageprofile -CloneProfile $CloneIP -Vendor $ipvendor -Name $ipname -Description $ipdesc

    # Update from Online depot profile
    if ($update) {
        write-host ("`nUpdating with the VMware Imageprofile " + $UpdIP.Name + " ...")
        write-host ("(dated " + $UpdIP.CreationTime + ", AcceptanceLevel: " + $UpdIP.AcceptanceLevel + ",")
        write-host ($UpdIP.Description + ")")
        $diff = Compare-EsxImageprofile $MyProfile $UpdIP
        $diff.UpgradeFromRef | foreach {
            $uguid = $_
            $uvib = Get-EsxSoftwarePackage | where { $_.Guid -eq $uguid }
            write-host -nonewline "   Add VIB" $uvib.Name $uvib.Version
            AddVIB2Profile $uvib
        }
    }

    # Loop over Offline bundles and VIB files
    if ($pkgDir -ne "") {
        write-host "`nLoading Offline bundles and VIB files from" $pkgDir ...
        foreach ($obundle in Get-Item $pkgDir\*.zip) {
            write-host -nonewline "   Loading" $obundle ...
            if ($ob = Add-EsxSoftwaredepot $obundle -ErrorAction SilentlyContinue) {
                write-host -ForegroundColor Green " [OK]"
                $ob | Get-EsxSoftwarePackage | foreach {
                    write-host -nonewline "      Add VIB" $_.Name $_.Version
                    AddVIB2Profile $_
                }
            } else {
                write-host -ForegroundColor Red " [FAILED]`n      Probably not a valid Offline bundle, ignoring."
            }
        }
        foreach ($vibFile in Get-Item $pkgDir\*.vib) {
            write-host -nonewline "   Loading" $vibFile ...
            try {
                $vib1 = Get-EsxSoftwarePackage -PackageUrl $vibFile -ErrorAction SilentlyContinue
                write-host -ForegroundColor Green " [OK]"
                write-host -nonewline "      Add VIB" $vib1.Name $vib1.Version
                AddVIB2Profile $vib1
            } catch {
                write-host -ForegroundColor Red " [FAILED]`n      Probably not a valid VIB file, ignoring."
            }
        }
    }
    # Load additional packages from Online depots or Offline bundles
    if ($load -ne @()) {
        write-host "`nLoad additional VIBs from Online depots ..."
        for ($i=0; $i -lt $load.Length; $i++ ) {
            if ($ovib = Get-ESXSoftwarePackage $load[$i] -Newest) {
                write-host -nonewline "   Add VIB" $ovib.Name $ovib.Version
                AddVIB2Profile $ovib
            } else {
                write-host -ForegroundColor Red "   [ERROR] Cannot find VIB named" $load[$i] "!"
            }
        }
    }
    # Remove selected VIBs
    if ($remove -ne @()) {
        write-host "`nRemove selected VIBs from Imageprofile ..."
        for ($i=0; $i -lt $remove.Length; $i++ ) {
            write-host -nonewline "      Remove VIB" $remove[$i]
            try {
                Remove-EsxSoftwarePackage -ImageProfile $MyProfile -SoftwarePackage $remove[$i] | Out-Null
                write-host -ForegroundColor Green " [OK]"
            } catch {
                write-host -ForegroundColor Red " [FAILED]`n      VIB does probably not exist or cannot be removed without breaking dependencies."
            }
        }
    }

} else {
    $MyProfile = $CloneIP
}


# Build the export command:
$cmd = "Export-EsxImageprofile -Imageprofile " + "`'" + $MyProfile.Name + "`'"

if ($ozip) {
    $outFile = "`'" + $outDir + "\" + $MyProfile.Name + ".zip" + "`'"
    $cmd = $cmd + " -ExportTobundle"
} else {
    $outFile = "`'" + $outDir + "\" + $MyProfile.Name + ".iso" + "`'"
    $cmd = $cmd + " -ExportToISO"
}
$cmd = $cmd + " -FilePath " + $outFile
if ($nsc) { $cmd = $cmd + " -NoSignatureCheck" }
$cmd = $cmd + " -Force"

# Run the export:
write-host -nonewline ("`nExporting the Imageprofile to " + $outFile + ". Please be patient ...")
if ($test) {
    write-host -ForegroundColor Yellow " [Skipped]"
} else {
    write-host "`n"
    Invoke-Expression $cmd
}

write-host -ForegroundColor Green "`nAll done.`n"

# The main catch ...
} catch {
    write-host -ForegroundColor Red ("`n`nAn unexpected error occured:`n" + $Error[0])
    write-host -ForegroundColor Red ("`nIf requesting support please be sure to include the log file`n   " + $log + "`n`n")

# The main cleanup
} finally {
    cleanup
    if (!($PSBoundParameters.ContainsKey('log')) -and $PSBoundParameters.ContainsKey('outDir')) {
        $finalLog = ($outDir + "\" + $MyProfile.Name + "-" + (get-date -Format yyyyMMddHHmm) + ".log")
        Move-Item $log $finalLog -force
        write-host ("(Log file moved to " + $finalLog + ")`n")
    }
}
```
</details>

<details><summary>点击此处 ← 查看帮助</summary>

``` powershell
PS D:\yuangezhizao\Documents\ESXi> .\ESXi-Customizer-PS-v2.6.0.ps1 -help

This is ESXi-Customizer-PS Version 2.6.0 (visit https://ESXi-Customizer-PS.v-front.de for more information!)

Usage:
   ESXi-Customizer-PS [-help] | [-izip <bundle> [-update]] [-sip] [-v67|-v65|-v60|-v55|-v51|-v50]
                                [-ozip] [-pkgDir <dir>] [-outDir <dir>] [-vft] [-dpt depot1[,...]]
                                [-load vib1[,...]] [-remove vib1[,...]] [-log <file>] [-ipname <name>]
                                [-ipdesc <desc>] [-ipvendor <vendor>] [-nsc] [-test]

Optional parameters:
   -help              : display this help
   -izip <bundle>     : use the VMware Offline bundle <bundle> as input instead of the Online depot
   -update            : only with -izip, updates a local bundle with an ESXi patch from the VMware Online depot,
                        combine this with the matching ESXi version selection switch
   -pkgDir <dir>      : local directory of Offline bundles and/or VIB files to add (if any, no default)
   -ozip              : output an Offline bundle instead of an installation ISO
   -outDir <dir>      : directory to store the customized ISO or Offline bundle (the default is the
                        script directory. If specified the log file will also be moved here.)
   -vft               : connect the V-Front Online depot
   -dpt depot1[,...]  : connect additional Online depots by URL or local Offline bundles by file name
   -load vib1[,...]   : load additional packages from connected depots or Offline bundles
   -remove vib1[,...] : remove named VIB packages from the custom Imageprofile
   -sip               : select an Imageprofile from the current list
                        (default = auto-select latest available standard profile)
   -v67 | -v65 | -v60 |
   -v55 | -v51 | -v50 : Use only ESXi 6.7/6.5/6.0/5.5/5.1/5.0 Imageprofiles as input, ignore other versions
   -nsc               : use -NoSignatureCheck with export
   -log <file>        : Use custom log file <file>
   -ipname <name>
   -ipdesc <desc>
   -ipvendor <vendor> : provide a name, description and/or vendor for the customized
                        Imageprofile (the default is derived from the cloned input Imageprofile)
   -test              : skip package download and image build (for testing)
```
</details>

### 3.下载`ESXi`离线包
它的文件命名格式突然变了，现在的`ESXi670-201912001.zip`与之前的`update-from-esxi6.7-6.7_update03.zip`……
![ESXi670-201912001](https://i1.yuangezhizao.cn/Win-10/20191227214127.jpg!webp)
![最新到 1205](https://i1.yuangezhizao.cn/Win-10/20191227214501.jpg!webp)

推荐一个与此强相关的网站，[老管网络日志 | funpower's blog](https://web.archive.org/web/20191227140233/https://guanjianfeng.com/vmware%E8%99%9A%E6%8B%9F%E5%8C%96%E4%BA%91%E8%AE%A1%E7%AE%97)
![看来就是这个了](https://i1.yuangezhizao.cn/Win-10/20191227214706.jpg!webp)
![龟速下载](https://i1.yuangezhizao.cn/Win-10/20191227215108.jpg!webp)

```
VMware vSphere Hypervisor (ESXi) Offline Bundle
文件大小: 451.7 MB
文件类型: zip
立即下载
Name: ESXi670-201912001.zip
发行日期: 2019-12-05
内部版本号: 15160138
VMware vSphere Hypervisor (ESXi) Offline Bundle
Including VMware Tools. Use the image profiles and the VIB packages with VMware Image BuContains VIB packages
MD5SUM: 153ea9de288d1cc2518e747f3806f929
SHA1SUM: e9761a1a8148d13af8a920decd9d729658d59f1c
SHA256SUM: a480208411422076e7cb7fda83aed2198513deb5859d6087f56f931afb0aa399
```

### 4. 下载`Realtek 8168`网卡驱动
在[Net55-r8168 - V-Front VIBSDepot Wiki](https://web.archive.org/web/20191227144530/https://vibsdepot.v-front.de/wiki/index.php/Net55-r8168)可以了解到
> Supported Devices / PCI IDs
10ec:8168, 1186:4300<br>
(Realtek RTL8111B / RTL8168B / RTL8111/RTL8168 / RTL8111C / RTL8111CP / RTL8111D(L) / RTL8168C / RTL8111DP / RTL8111E / RTL8168E / RTL8111F / RTL8411 / RTL8111G / RTL8111GUS / RTL8411B(N) / RTL8118AS / D-Link DGE-528T)

下载这个：[net55-r8168-8.045a-napi-offline_bundle.zip](http://vibsdepot.v-front.de/depot/bundles/net55-r8168-8.045a-napi-offline_bundle.zip)

### 5.封装
![终于成功](https://i1.yuangezhizao.cn/Win-10/20191228012436.jpg!webp)

``` powershell
PS D:\yuangezhizao\Documents\ESXi> ./ESXi-Customizer-PS-v2.6.0.ps1 -izip ESXi670-201912001.zip -dpt net55-r8168-8.045a-napi-offline_bundle.zip -load net55-r8168

This is ESXi-Customizer-PS Version 2.6.0 (visit https://ESXi-Customizer-PS.v-front.de for more information!)
(Call with -help for instructions)

Logging to C:\Users\YUANGE~1\AppData\Local\Temp\ESXi-Customizer-PS-17316.log ...

Running with PowerShell version 5.1 and VMware PowerCLI version 11.5.0.14899560

Adding base Offline bundle ESXi670-201912001.zip ... [OK]

Connecting additional depot net55-r8168-8.045a-napi-offline_bundle.zip ... [OK]

Getting Imageprofiles, please wait ... [OK]

Using Imageprofile ESXi-6.7.0-20191204001-standard ...
(dated 11/25/2019 11:43:03, AcceptanceLevel: PartnerSupported,
Updates ESXi 6.7 Image Profile-ESXi-6.7.0-20191204001-standard)

Load additional VIBs from Online depots ...
   Add VIB net55-r8168 8.045a-napi [New AcceptanceLevel: CommunitySupported] [OK, added]

Exporting the Imageprofile to 'D:\yuangezhizao\Documents\ESXi\ESXi-6.7.0-20191204001-standard-customized.iso'. Please be patient ...


All done.

PS D:\yuangezhizao\Documents\ESXi>
```

### 6.烧录
亲测使用`balenaEtcher`烧录之后的`U`盘并不能成功启动，于是采用[官网](https://rufus.ie/)←的[rufus](https://github.com/pbatard/rufus)该工具
![？](https://i1.yuangezhizao.cn/Win-10/20191228024213.jpg!webp)
![选择镜像和盘](https://i1.yuangezhizao.cn/Win-10/20191228021735.jpg!webp)

注意如果提示啥启动项过于老旧可能不会成功需要联网下载新版请点**是**，第一次没截图现在不出弹提示了草

### 7.启动
机子搬回屋子里，菊花插上显示器、键盘和盘……开机`BIOS`设置项里选盘启动！

![BIOS](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20191228_021245-sc.jpg!webp)
![Installer](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20191228_022257-sc.jpg!webp)
![Enter](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20191228_022403-sc.jpg!webp)

这里让选在哪块硬盘上安装或升级`ESXi`，当时一愣选错就尴尬了……
后来看到可以看详细信息，只有一块硬盘含有`ESX(I) Found：ESXi 6.7.0`
![看硬盘详细信息](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20191228_022553-sc.jpg!webp)
![Upgrade](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20191228_022615-sc.jpg!webp)
![最终确认](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20191228_022633-sc.jpg!webp)
![升级中](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20191228_022643-sc.jpg!webp)
![升级完成](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20191228_022741-sc.jpg!webp)
![运行中](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20191228_022928-sc.jpg!webp)

然后关机后把机子拿到客厅，插上电源和网线（主板上电自动开机
回到卧室，进`web`一看
![不慌，再等等](https://i1.yuangezhizao.cn/Win-10/20191228023255.jpg!webp)
![大功告成](https://i1.yuangezhizao.cn/Win-10/20191228025938.jpg!webp)

挂起的`macOS`成功启动，并不用重新破解，看起来没什么大问题`hhh`，可以去睡觉了`.zZ……`

## 0x01.[VMware ESXi](https://www.vmware.com/products/esxi-and-esx.html)
这玩楞就是传说中的把服务器整机都虚拟化的软件，之前用的`VMware Workstation`只是在本机跑虚拟机。而前者虚拟化完成之后并没有图形化界面，只能在另一台电脑上远程访问`Web`界面进行管理，比如创建多个虚拟机此类操作。所以，你懂得……
这里就截几个图看看吧（`WZ`大佬组的台式机硬件，华硕主板、`E3 CPU`,`16G`内存，~~唯一不足的是硬盘拿了个辣鸡`500G`先扛着了~~
`2019-12-28 00:43:33`该硬盘于上周已炸……
电信宽带提供公网`IP`，只需一个电话说明理由就给你分配，与移动的`NAT`相比已经很良心的了……
再一个这里能获取到`IPV6`地址，~~下列截图中也进行了高斯模糊处理~~干脆折叠起来好了～
![host](https://i1.yuangezhizao.cn/Win-10/20191228004822.jpg!webp)

 这里比较有意思的是，你可以创建大于物理核心数量的虚拟核心，也可以理解为虚拟化的是总频率，如下图
![CPU](https://i1.yuangezhizao.cn/Win-10/20190803011722.jpg!webp)

更改用户权限的页面藏在了这里，找了半天才发现，实在是太反人类了……
![permission](https://i1.yuangezhizao.cn/Win-10/20190728002659.jpg!webp)

`web`页面每`900s`会强制下线草，参照[为 ESXi Shell 和 vSphere Web Client 设置超时](https://web.archive.org/web/20200104172443/https://docs.vmware.com/cn/VMware-vSphere/6.0/com.vmware.vsphere.security.doc/GUID-E4EA7712-476A-458C-9DDA-5C6D260C6694.html)可以在`高级设置`中修改至`0`
![官方文档](https://i1.yuangezhizao.cn/Win-10/20200104195521.jpg!webp)
![超时](https://i1.yuangezhizao.cn/Win-10/20200104185106.jpg!webp)
![逼死强逼症患者](https://i1.yuangezhizao.cn/Win-10/20200104192656.jpg!webp)

参照[为 ESXi 6.0 主机配置 CA 签名证书 (2113926)](https://web.archive.org/web/20200104173200/https://kb.vmware.com/s/article/2113926?lang=zh_CN)
![官方文档](https://i1.yuangezhizao.cn/Win-10/20200104191844.jpg!webp)
![腾讯云申请免费证书](https://i1.yuangezhizao.cn/Win-10/20200104192115.jpg!webp)

重命名为`rui.crt`、`rui.key`，上传至`/etc/vmware/ssl`文件夹中
![上传自己的证书](https://i1.yuangezhizao.cn/Win-10/20200104192534.png!webp)

懒得重启了，于是
`/etc/init.d/hostd restart`、`/etc/init.d/vpxa restart`
![XShell](https://i1.yuangezhizao.cn/Win-10/20200104192831.jpg!webp)

<details><summary>点击此处 ← 查看终端</summary>

``` shell
Copyright (c) 2002 NetSarang Computer, Inc. All rights reserved.

Type `help' to learn how to use Xshell prompt.
[D:\~]$ 

Connecting to 192.168.25.249:22...
Connection established.
To escape to local shell, press 'Ctrl+Alt+]'.

The time and date of this login have been sent to the system logs.

WARNING:
   All commands run on the ESXi shell are logged and may be included in
   support bundles. Do not provide passwords directly on the command line.
   Most tools can prompt for secrets or accept them from standard input.

VMware offers supported, powerful system administration tools.  Please
see www.vmware.com/go/sysadmintools for details.

The ESXi Shell can be disabled by an administrative user. See the
vSphere Security documentation for more information.
[root@VM:~] cd /etc/vmware/ssl
[root@VM:/etc/vmware/ssl] ls
castore.pem               rui.crt                   vsan_kms_client.crt       vsanvp_castore.pem
iofiltervp.pem            rui.key                   vsan_kms_client.key
openssl.cnf               vsan_kms_castore.pem      vsan_kms_client_old.crt
rui.bak                   vsan_kms_castore_old.pem  vsan_kms_client_old.key
[root@VM:/etc/vmware/ssl] rm rui.crt rui.key 
[root@VM:/etc/vmware/ssl] /etc/init.d/hostd restart
watchdog-hostd: Terminating watchdog process with PID 2099465
hostd stopped.
hostd started.
[root@VM:/etc/vmware/ssl] /etc/init.d/vpxa restart
watchdog-vpxa: Terminating watchdog process with PID 2099054
vpxa stopped.
vpxa started.
[root@VM:/etc/vmware/ssl] 
```
</details>

![新增内网？解析](https://i1.yuangezhizao.cn/Win-10/20200104193727.jpg!webp)
![完工爽到](https://i1.yuangezhizao.cn/Win-10/20200104193851.jpg!webp)

~~先给自己分配了一个虚拟机`hhh`~~`2019-12-28 00:51:40`该机子由于存储在坏掉的硬盘无法成功完全导出，最终只能重装……
![vms](https://i1.yuangezhizao.cn/Win-10/20190728003657.png!webp)
![+1s](https://i1.yuangezhizao.cn/Win-10/20190728004123.jpg!webp)
> [PY 云新增 CentOS 7.7 64 位](../Linux/CentOS/py.html)

![c7](https://i1.yuangezhizao.cn/Win-10/20191116191625.jpg!webp)

`2019-8-24 13:06:59`
![4TB 硬盘购买](https://i1.yuangezhizao.cn/Win-10/20190824130554.png!webp)
![NASdata 3TB](https://i1.yuangezhizao.cn/Win-10/20190824130337.jpg!webp)

`2019-12-28 00:19:00`
旧硬盘已炸（彻底报废？）替代硬盘已上，然后开机发现`web`连不上……出去看机子听到硬盘一直咔咔响……
`WZ`大佬现身`Trouble Shooting`，发现那块硬盘连的是旧的`SATA`硬盘线，换上新的`1/元`根的线之后好了
猜想之前的那块系统盘坏掉的原因也可能是因为这条线，草
![机子](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20191228_001521.jpg!webp)
![那条硬盘线](https://i1.yuangezhizao.cn/Redmi-K20Pro/IMG_20191228_002618.jpg!webp)

## 0x02.Windows Server 2019 DataCenter
爽到
![cn-py-dl-w9d](https://i1.yuangezhizao.cn/Win-10/20190728015602.png!webp)

## 0x03.后记
这玩楞搁在了客厅的冰箱旁边和冰箱一起`24h`不断电工作，虽然主板以及其他位置都配置为了**节能**，但是感觉还是会比较费电……也不知道功耗能有多少诶？

## 0x04.引用
> [旧笔记本通过自定义整合网卡驱动安装 ESXi 6.7.0 u1](https://web.archive.org/web/20191227140613/https://www.jianshu.com/p/b0124a2c5e33)
[命令行操作vSphere--VMware PowerCLI安装](https://web.archive.org/web/20191227151410/https://zerlong.com/739.html)
