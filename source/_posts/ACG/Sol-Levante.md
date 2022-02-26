---
title: 《Sol Levante》——4K UHD 2160p ProRes HDR10 Anime
date: 2020-4-15 20:55:06
tags:
  - Netflix
count: 1
os: 0
os_1: 10.0.17763.1098 2019-LTSC
browser: 0
browser_0: 78.0.3904.108 Stable
place: 新家
key: 84
---
    Sol Levante is an experimental short anime project commissioned by Netflix in collaboration with Japan’s Production I.G. that sought to answer questions about the challenges involved with bringing 4K and HDR to the medium.
<!-- more -->
## 0x00.前言
> 写在前面：纯属水文，仅为记录

几天前看到了`U3`组放流了新的玩楞，但是只看了眼大小之后并没有仔细去看是什么东西，然后直到昨天晚上才意识到这`tm`是`4K`+`HDR`，没看错（确信
![tg](https://i1.yuangezhizao.cn/Win-10/20200414231707.png!webp)
![Netflix](https://i1.yuangezhizao.cn/Win-10/20200414231633.png!webp)
![IMDb](https://i1.yuangezhizao.cn/Win-10/20200414232838.png!webp)

## 0x01.介绍
网飞当日就发推介绍了
![Twitter](https://i1.yuangezhizao.cn/Win-10/20200414233024.png!webp)

然后去看网飞的[介绍](https://web.archive.org/web/20200415125829/http://download.opencontent.netflix.com.s3.amazonaws.com/SolLevante/readme-sollevante.txt)
> Last Updated: 2020-04-01<br><br>
Sol Levante is an experimental short anime project commissioned by Netflix in collaboration with Japan’s Production I.G. that sought to answer questions about the challenges involved with bringing 4K and HDR to the medium. These open source assets were made available from the project in order to allow further experimentation and self-education with anime workflow, 4K, HDR, and immersive audio. <br><br>
If you have any questions about the materials, you can email creativetech@netflix.com.<br><br>
The open source assets include: <br><br>
1000 nit VDM,16 bit TIFF sequence and IMF
Selected painted in-betweens for traditional workflow (TGA)
Selected painted drawings for cutout animation (PSD)
Selected After Effects project with base comp
ProTools session (Final Mix)
ProTools session (Atmos deliverable)
Animatic (MOV) and Storyboard (PDF)
HDR10 asset in ProRes 4444 XQ format<br><br>
This material is available under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International license (CC BY-NC-ND 4.0). The full license is included as a separate document.<br><br>
-----<br><br>
Sol Levante はアニメ作品において4KとHDRをどの様に活用できるかを模索するために、NetflixがProduction IGと共に実験的に行ったアニメ短編プロジェクトです。これらのオープンソースアセットはみなさんがアニメのワークフロー、4K、HDR、没入感のあるオーディオを更に理解し、実験することができる様に、本プロジェクトから利用可能にしたものです。 <br><br>
素材に関してのご質問は creativetech@netflix.comまでご連絡ください。<br><br>
オープンソースアセットには以下のものが含まれます：<br><br>
1000 nit VDM,16 bit TIFF 連番ファイルおよび IMF
一部のカットの彩色済み動画ファイル：従来のワークフロー用 (TGA)
一部のカットの彩色済み作画ファイル：カットアウト用（PSD)
After Effects プロジェクト
ProTools セッションファイル (最終ミックス)
ProTools セッションファイル (Atmos デリバラブル)
アニマティック (MOV) 及びストーリーボード (PDF)
HDR10 アセット（ProRes 4444 XQ形式)<br><br>
これらの素材は、クリエイティブ・コモンズ 表示-非営利-改変禁止 4.0 国際ライセンス（CC BY-NC-ND 4.0)の元に共有されます。ライセンスの規定については、別のドキュメントに含まれています。

另外也在技术博客中单独写了一篇[文章](https://web.archive.org/web/20200415134013/https://netflixtechblog.com/bringing-4k-and-hdr-to-anime-at-netflix-with-sol-levante-fa68105067cd?gi=b755767c5810)进行介绍

## 0x02.下载
接下来自然就是去[nyaa](https://web.archive.org/web/20200415130354/https://nyaa.si/?f=0&c=0_0&q=Sol+Levante)寻（立）找（即）资（白）源（嫖）了
![nyaa](https://i1.yuangezhizao.cn/Win-10/20200415203723.png!webp)

直接把最大的包挂到`NAS`里下载之后就去睡觉了……
![1234786](https://i1.yuangezhizao.cn/Win-10/20200415204818.png!webp)

网飞也非常大方，给了很多原始素材不仅限于`AE`项目文件，当然想跑起来的话你需要有足够性能的机子
![文件夹](https://i1.yuangezhizao.cn/Win-10/20200415204702.png!webp)

这里随手打开了个项目瞅瞅
![AE](https://i1.yuangezhizao.cn/Win-10/20200415203318.png!webp)

## 0x03.评论
看到`nyaa`中`PCM`的帖子中老外在[评论区](https://web.archive.org/web/20200415130419/https://nyaa.si/view/1234646)中纷纷贴出`CPU`占用图
比如第一个是通过`POTplayer video= passed Ok codec Apple ProRes 4444 XQ one CPU decode to AMD Ryzen™ Threadripper™ 2920X >> SolLevante_HDR10_r2020_ST2084_UHD_24fps_1000nit.mov (34.8 GiB)`
草，线程撕裂者
![https://i.imgur.com/Gk5dV4m.png](https://i1.yuangezhizao.cn/Win-10/Gk5dV4m.png!webp)
![https://prnt.sc/rsykua](https://i1.yuangezhizao.cn/Win-10/rsykua.png!webp)

另外将此帖中的参数贴出`ProRes lel`
``` bash
General
Complete name : SolLevante_HDR10_r2020_ST2084_UHD_24fps_1000nit.mov
Format : MPEG-4
Format profile : QuickTime
Codec ID : qt 0000.00 (qt )
File size : 34.8 GiB
Duration : 4 min 23 s
Overall bit rate mode : Variable
Overall bit rate : 1 137 Mb/s
Encoded date : UTC 2020-04-01 02:10:29
Tagged date : UTC 2020-04-01 02:24:20
Writing library : Apple QuickTime

Video
ID : 1
Format : ProRes
Format version : Version 1
Format profile : 4444 XQ
Codec ID : ap4x
Duration : 4 min 23 s
Bit rate mode : Variable
Bit rate : 1 128 Mb/s
Width : 3 840 pixels
Height : 2 160 pixels
Display aspect ratio : 16:9
Frame rate mode : Constant
Frame rate : 24.000 FPS
Color space : YUV
Chroma subsampling : 4:4:4
Scan type : Progressive
Bits/(Pixel*Frame) : 5.666
Stream size : 34.5 GiB (99%)
Title : Core Media Video
Writing library : abm0
Encoded date : UTC 2020-04-01 02:10:29
Tagged date : UTC 2020-04-01 02:24:20
Color primaries : BT.2020
Transfer characteristics : PQ
Matrix coefficients : BT.2020 non-constant

Audio #1
ID : 2
Format : PCM
Format settings : Little / Signed
Codec ID : lpcm
Duration : 4 min 23 s
Bit rate mode : Constant
Bit rate : 6 912 kb/s
Channel(s) : 6 channels
Channel layout : L R C LFE Ls Rs
Sampling rate : 48.0 kHz
Bit depth : 24 bits
Stream size : 217 MiB (1%)
Title : Core Media Audio
Encoded date : UTC 2020-04-01 02:10:29
Tagged date : UTC 2020-04-01 02:24:20

Audio #2
ID : 3
Format : PCM
Format settings : Little / Signed
Codec ID : lpcm
Duration : 4 min 23 s
Bit rate mode : Constant
Bit rate : 2 304 kb/s
Channel(s) : 2 channels
Channel layout : L R
Sampling rate : 48.0 kHz
Bit depth : 24 bits
Stream size : 72.3 MiB (0%)
Title : Core Media Audio
Encoded date : UTC 2020-04-01 02:10:29
Tagged date : UTC 2020-04-01 02:24:20

Other
ID : 4
Type : Time code
Format : QuickTime TC
Duration : 4 min 23 s
Frame rate : 24.000 FPS
Time code of first frame : 00:00:00:00
Time code, striped : Yes
Title : Core Media Time Code / urn:uuid:67d69635-4779-482e-887f-beab7d0d8355
Encoded date : UTC 2020-04-01 02:10:29
Tagged date : UTC 2020-04-01 02:24:20
```

## 0x04.Rip
`LoliHouse`倒是已经出了[Rip]((https://web.archive.org/save/https://nyaa.si/view/1238063)版本的，真就「高清病毒」呗（注：从`292 GB`压到了`1.1 GiB`，采用`mkv`封装
![1238063](https://i1.yuangezhizao.cn/Win-10/20200415212151.jpg!webp)

> 如果你实在闲得蛋疼想找个新的"高清病毒"来玩，可以尝试网飞提供的`ProRes`样片，使用了`yuv444p12`最高规格的编码，码率高达`1128 Mbps`。播放时请确保文件保存在`SSD`上，`CPU`软解大约需要第`8`代`Intel Core`六核或以上。不过这种东西本来就不是给普通用户拿来播放的。<br>
在我们时时念叨日本动画业界要完的同时，能看到网飞像这样对推动新技术所做的尝试，固然是值得欣慰的。恰逢业界面临空前困难的当下，让我们拭目以待未来的发展吧。

然后又在[评论区](https://web.archive.org/web/20200415132026/https://nyaa.si/view/1236009)碰到了`2333`，注：截图有删减原文描述`INFO`
![1236009](https://i1.yuangezhizao.cn/Win-10/20200415212032.jpg!webp)

## 0x05.播放
媒体盘还有足够空间
![D](https://i1.yuangezhizao.cn/Win-10/20200415214739.jpg!webp)

但是暂时决定只把`SolLevante`里`hdr10`中`SolLevante_HDR10_r2020_ST2084_UHD_24fps_1000nit.mov`下到`SSD`之中，试验开始
![复制](https://i1.yuangezhizao.cn/Win-10/20200415215010.jpg!webp)

实测无法使用`LAV`，只能`FFmpeg`，但是播放起来基本无压力（甚至还挂载了`madVR`），除了声音莫名会一卡一卡的
![PotPlayer](https://i1.yuangezhizao.cn/Win-10/20200415220427.jpg!webp)
![CPU](https://i1.yuangezhizao.cn/Win-10/20200415220519.jpg!webp)

## 0x05.后记
这是一次大胆的技术尝试，尤其是在这个时间点上

未完待续……