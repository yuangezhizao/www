---
title: 《超凡双生》试玩版 bypass 完整版
date: 2020-3-13 21:45:32
tags:
  - BeyondTwoSouls
  - BeyondTwoSoulsDemo
count: 1
os: 0
os_1: 10.0.17763.1098 2019-LTSC
browser: 0
browser_1: 78.0.3904.108 Stable
place: 新家
key: 78
---
    终于昨天打通关了，bypass 大法好！
    有效性验证：2020-3-13 23:06:56
<!-- more -->
## 0x00.前言
![crackwatch](https://i1.yuangezhizao.cn/Win-10/20200313231706.jpg!webp)

时间回到了大四，室友咸鱼购买了台`PS4`，但是并没有买很多游戏。印象里第一款到的是《底特律：变人》，接下来是《暴雨》和《超凡双生》
首先打完了底特律的一个结局，然后《暴雨》和《超凡双生》正好是在同一个盒子中并且盘片是在上面的，因此《超凡双生》直到毕业都没有玩到。。。

## 0x01.[Quantic Dream](https://zh.wikipedia.org/zh-hans/Quantic_Dream)
> `Quantic Dream SA`是一家法国电子游戏开发商，总部位于巴黎。`Quantic Dream`成立于`1997`年`6`月，开发了五款电子游戏：《恶灵都市》（`1999`）、《华氏》（`2005`）、《暴雨杀机》（`2010`）、《超凡双生》（`2013`）和《底特律：变人》（`2018`）。除电子游戏外，他们还帮助制作了`2004`年电影《诸神混乱之女神陷阱》。`Quantic Dream`以推广互动式叙事而闻名，创始人大卫·凯奇是主要创意人员

——以上引用自维基百科
没错，这就是那个互动式叙事游戏的鼻祖，目前已经可以独立制作游戏而不依赖于索尼，《底特律：变人》将其多结局特点发挥到极致？

> `2020`年`2`月，`Quantic Dream`宣布他们已经完全独立，未来将自行负责所有游戏作品的发行业务

游戏名称 | 类型 | 首发时间 | 发售平台 | 发行商
:---: | :---: | :---: | :---: | :---:
恶灵都市 | 动作冒险 | `1999`年`10`月`31`日 | `Dreamcast`、`Microsoft Windows Eidos` | `Interactive`
华氏 | 互动式电影、动作冒险 | `2005`年`9`月`16`日 | `Android`、`iOS`、`Linux`、`macOS`、`Microsoft Windows`、`PlayStation2`、`PlayStation4`、`Xbox` | `Atari`、`Aspyr Quantic Dream`
暴雨杀机 | 互动式电影、动作冒险 | `2010`年`2`月`18`日 | `PlayStation3`、`PlayStation 4`、`Microsoft Windows` | 索尼电脑娱乐、`Quantic Dream`
超能杀机：两个灵魂 | 互动式电影、动作冒险 | `2013`年`10`月`8`日 | `PlayStation3`、`PlayStation4`、`Microsoft Windows` | 索尼电脑娱乐、`Quantic Dream`
底特律：变人 | 互动式电影、动作冒险 | `2018`年`5`月`25`日 | `PlayStation4`、`Microsoft Windows` | 索尼互动娱乐、`Quantic Dream`

## 0x02.bypass
这里没放链接，懒得去考证了……
### 1.`Epic`商店下载`BeyondTwoSoulsDemo`
注意并不能用国区账号，倒是可以改地区之后获取试玩版（反正没付费之前都是可以随意更改地区的），用`Epic`启动游戏，这里本人把`Demo`打完，反正这里打完之后也不用再打了
之后就再也不用开`Epic`启动器了

### 2.`3DM`论坛下载`3DMGAME-Beyond.Two.Souls.EpicStoreRip-3DM`
下载`44.3 GB (47,623,598,080 字节)`的压缩包后解压

### 3.`bypass`
1. 除`.egstore`文件夹和`BeyondTwoSouls.exe`主文件之外，将**完整版**文件夹直接覆盖到**试玩版**文件夹中
①`.egstore`文件夹：
``` bash
yuangezhizao@DESKTOP-HSLUUMC MINGW64 /e/Epic Games/BeyondTwoSoulsDemo/.egstore
$ ll
total 565
-rw-r--r-- 1 yuangezhizao 197609    143  3月 12 19:09 11E772E64EE588B73344E2B75B606D88.mancpn
-rw-r--r-- 1 yuangezhizao 197609 573725  3月 12 19:09 11E772E64EE588B73344E2B75B606D88.manifest
drwxr-xr-x 1 yuangezhizao 197609      0  3月 12 19:21 681ba7f647ca499eb998e053adaa0fef/
drwxr-xr-x 1 yuangezhizao 197609      0  3月 12 19:09 Pending/
```
②`BeyondTwoSouls.exe`主文件：
``` bash
文件：	E:\Epic Games\BeyondTwoSoulsDemo\BeyondTwoSouls.exe
大小：	339, 792, 896 字节
修改时间：2020-03-12 19:01:24
MD5：	82E6E9E1A9B4B8C039F4A831C66EFB99
SHA1：	9E58702BC8932CE923BF23434A72E3AD74A94020
CRC32：	20D3456D
```
2. 编辑`BigFile_PC.dat`文件（没错就是那个巨大的文件），搜索字符串`QDR.Infraworld_Var.BootCheat`，将`QDR.Infraworld_Var.BootCheat = 0`中`0`改成`4`
对应十六进制数：`30`改成`34`：
![010Editor.exe](https://i1.yuangezhizao.cn/Win-10/20200313222920.jpg!webp)

## 0x03.后记
大约花了一周，社畜之余抽时间终于把这游戏通关了（一个结局），毕竟是`13`年的游戏，能做到这个水准还是很看好的，虽然结局有点儿内啥
手柄操作方式太经典了……不得不想起了其他两款游戏也是同样的操作方式，毕竟是同一家公司`2333`
再一个就是毕竟还是带有恐怖元素在内，导致某些章节根本没法晚上游玩（吓死了草），只能白天隔屏幕大老远手柄操作，甚至都占到了门的位置草
~~最后，年轻时代的女主真好看啊，`prpr`（真·主角光环~~
![重要选项](https://i1.yuangezhizao.cn/Win-10/20200313225446.jpg!webp)
![尾声](https://i1.yuangezhizao.cn/Win-10/20200313225435.jpg!webp)
![打水漂](https://i1.yuangezhizao.cn/Win-10/20200313225445.jpg!webp)
![侧颜好看](https://i1.yuangezhizao.cn/Win-10/20200313225436.jpg!webp)
![艾登是自己的双胞胎哥哥这个剧情实在是……然后刚刚发现之后就没有了，过草](https://i1.yuangezhizao.cn/Win-10/20200313225437.jpg!webp)
![深山野林](https://i1.yuangezhizao.cn/Win-10/20200313225438.jpg!webp)
![选项四](https://i1.yuangezhizao.cn/Win-10/20200313225444.jpg!webp)
![不然就刀片了](https://i1.yuangezhizao.cn/Win-10/20200313225439.jpg!webp)
![啊，这夕阳！](https://i1.yuangezhizao.cn/Win-10/20200313225440.jpg!webp)
![ED](https://i1.yuangezhizao.cn/Win-10/20200313225441.jpg!webp)
![2013](https://i1.yuangezhizao.cn/Win-10/20200313225442.jpg!webp)
![39](https://i1.yuangezhizao.cn/Win-10/20200313225443.jpg!webp)


## 0x04.免责声明
> 本文的目的只有一个就是学习更多的破解技巧和思路，如果有人利用本文技术去进行非法商业获取利益带来的法律责任都是操作者自己承担，和本文以及作者没关系
