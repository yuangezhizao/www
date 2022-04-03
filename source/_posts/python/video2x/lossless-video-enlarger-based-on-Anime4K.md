---
title: 基于 Anime4K 的 Video2X 无损视频放大
date: 2019-10-7 17:28:15
tags:
  - Anime4K
  - Video2X
  - HIMEHINA
count: 3
os: 0
os_1: 10.0.17763.775 2019-LTSC
browser: 0
browser_1: 74.0.3729.169 Stable
place: 新家
key: 58
---
    《HIMEHINA 心灵的怒吼》直播源 720P 拉伸至 1080P 的尝试
<!-- more -->
## 0x00.前言
`2020-12-9 21:59:05`：
`HH`两张`BD`均已由[kuchikirukia](https://nyaa.si/user/kuchikirukia)于`2020-12-05 09:12`和`2020-12-07 19:59`上传，至此本文使命完成

No. | 名称 | 大小 | 地址
:---: | :---: | :---: | :---:
1 | HIMEHINA 1st One-Man Live 「心を叫べ」 2019.09.27 [BD 1080p Hi10P AAC][kuchikirukia].mkv | 22.6G | https://nyaa.si/view/1310762
2 | HIMEHINA - 田中音楽堂オトナLIVE 2020 in TOKYO 「歌學革命宴」feat.鈴木文学堂 2020.02.28 [BD 1080p Hi10P AAC][kuchikirukia].mkv | 20.3G | https://nyaa.si/view/1311949

<details><summary>点击此处 ← 查看折叠</summary>

> 原版：https://www.acfun.cn/v/ac11277880
度盘：https://pan.baidu.com/s/1Sxkr64-KRTQTfo_cDmdGXw

Audio：
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/aplayer/dist/APlayer.min.css">
<div id="aplayer"></div>
<script src="https://cdn.jsdelivr.net/npm/aplayer/dist/APlayer.min.js"></script>
<script>
const ap = new APlayer({
    container: document.getElementById('aplayer'),
    preload: 'metadata',
    audio: [{
        name: '1stONE-MAN LIVE「心を叫べ」',
        artist: 'HIMEHINA',
        url: 'https://a1.yuangezhizao.cn/02be24f712d246fda72bc70076fe402b-4f3b523415ec5a4e9b85143508d77e06-hd_output_audio_index0.aac',
        // url: 'https://a3.yuangezhizao.workers.dev/?file=02be24f712d246fda72bc70076fe402b-4f3b523415ec5a4e9b85143508d77e06-hd_output_audio_index0.aac',
        // url: 'https://home.yuangezhizao.cn:3333/cos/a0/02be24f712d246fda72bc70076fe402b-4f3b523415ec5a4e9b85143508d77e06-hd_output_audio_index0.aac',
        cover: 'https://cors.yuangezhizao.workers.dev/?url=https://i0.hdslb.com/bfs/archive/a3e25de38182292dfa36ef06fea7ea7cd894e15b.jpg'
    }]
});
</script>

下载地址（由`Coding`企业版`TencentStorage`支持）：[https://yuangezhizao.coding.net/s/ef2743f2-14ac-4b3e-b02d-2fe16ead36f9](https://yuangezhizao.coding.net/s/ef2743f2-14ac-4b3e-b02d-2fe16ead36f9)

Video：
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/dplayer/dist/DPlayer.min.css" />
<div id="dplayer"></div>
<script src="https://cdn.jsdelivr.net/npm/hls.js/dist/hls.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/dplayer/dist/DPlayer.min.js"></script>
<script>
const dp = new DPlayer({
    container: document.getElementById('dplayer'),
    video: {
        quality: [
            {
                name: 'home',
                url: 'https://home.yuangezhizao.cn:3333/cos/v0/02be24f712d246fda72bc70076fe402b-4f3b523415ec5a4e9b85143508d77e06-hd_output.mp4',
                type: 'normal',
            },
            {
                name: 'v3',
                url: 'https://v3.yuangezhizao.workers.dev?file=02be24f712d246fda72bc70076fe402b-4f3b523415ec5a4e9b85143508d77e06-hd_output.mp4',
                type: 'normal',
            },
            {
                name: 'v1',
                url: 'https://v1.yuangezhizao.cn/02be24f712d246fda72bc70076fe402b-4f3b523415ec5a4e9b85143508d77e06-hd_output.mp4',
                type: 'normal',
            },
            {
                name: 'v0-hls',
                url: 'http://v0-hls.yuangezhizao.cn/job_02be24f712d246fda72bc70076fe402b-4f3b523415ec5a4e9b85143508d77e06-hd_output.mp4',
                type: 'hls',
            },
        ],
        defaultQuality: 'v3',
        preload: 'metadata'
    },
    // pluginOptions: {
    //     hls: {
    //         // hls config
    //     },
    // },
});
</script>
![资源](https://i1.yuangezhizao.cn/Win-10/20191007173645.jpg!webp)
![审核过草](https://i1.yuangezhizao.cn/Win-10/20191007173737.jpg!webp)
![血赚](https://i1.yuangezhizao.cn/Win-10/20191007173222.jpg!webp)

然后`PanDownload 2.1.3`屯到本地发现竟然是`720P`，于是想着拉到`1080P`试试看……

</details>

## 0x01.[Video2X](https://github.com/k4yt3x/video2x)
> A lossless video enlarger/video upscaler achieved with waifu2x and Anime4K. https://k4yt3x.github.io/video2x/

![最新版 video2x-2.10.0-win32-light.zip 不提供完整包](https://i1.yuangezhizao.cn/Win-10/20191007174752.jpg!webp)
![video2x_setup.exe，网络不能](https://i1.yuangezhizao.cn/Win-10/20191007175701.jpg!webp)
![尝试源码安装，git 翻车现场](https://i1.yuangezhizao.cn/Win-10/20191007181523.jpg!webp)
![文件夹已炸](https://i1.yuangezhizao.cn/Win-10/20191007182100.jpg!webp)

## 0x02.[CUDA](https://developer.nvidia.com/cuda-toolkit-archive)
![于是去下了上一个提供完整包的 video2x-2.9.0-win32-full.zip](https://i1.yuangezhizao.cn/Win-10/20191007195541.jpg!webp)

发现选了`GPU`模式`CPU`仍然跑满，于是准备去安装`CUDA`+`cuDNN`即`NVIDIA`机器学习全家桶……
![这里仍然选择之前的 10.0，去看了下 TF 的文档支持仍然是这个版本（我怂，其实是懒得折腾了](https://i1.yuangezhizao.cn/Win-10/20191007200853.jpg!webp)

这里网络环境不好，于是选择了`cuda_10.0.130_win10_network.exe`在线安装……
![按需下载](https://i1.yuangezhizao.cn/Win-10/20191007203426.jpg!webp)
![卒](https://i1.yuangezhizao.cn/Win-10/20191007202921.jpg!webp)
![10，000 years later](https://i1.yuangezhizao.cn/Win-10/20191007203739.jpg!webp)
![今晚网络各种炸](https://i1.yuangezhizao.cn/Win-10/20191007204342.jpg!webp)
![再慢就要用中转机子了](https://i1.yuangezhizao.cn/Win-10/20191007204425.jpg!webp)
![安装依赖](https://i1.yuangezhizao.cn/Win-10/20191007204750.jpg!webp)
![后来发现只需运行该文件安装即可，然而需要良好的网络环境](https://i1.yuangezhizao.cn/Win-10/20191007205401.jpg!webp)
![于是变成了手动下载了……](https://i1.yuangezhizao.cn/Win-10/20191007205803.jpg!webp)
![顺便更新下版本](https://i1.yuangezhizao.cn/Win-10/20191007201335.jpg!webp)
![文件夹名实在是太难了……](https://i1.yuangezhizao.cn/Win-10/20191007213018.jpg!webp)
![GitMent 权限？](https://i1.yuangezhizao.cn/Win-10/20191121183458.jpg!webp)

未完待续……