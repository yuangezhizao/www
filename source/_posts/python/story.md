---
title: 讲一个自己的故事
date: 2021-11-05 22:02:03
tags:
  - Next.js
  - React
count: 5
os: 1
os_1: Monterry 12.0.1 (21A559)
browser: 0
browser_1: 95.0.4638.69 Stable
place: 新家
key: 123
---
    本来是在写下一篇文章，结果前摇过长被迫单发
<!-- more -->
## 0x00.前言
去`gh`翻了下提交日志，结合`QZone`的水文，捋下来发现这都能拿出来讲故事了`2333`
那么事不宜迟干脆就从头说起吧，`emmm`，提前多图预警（现在跑还来得及

## 0x01.故事
### 1.腾讯云——折腾的开始
时光回到大一下（`2016`），那时候就已经注册了你云的账号（老用户确信），目的仅仅是为了买每个月仅需`1`元的学生机，只能说当初白嫖的真香

<details><summary>点击此处 ← 查看折叠</summary>

![2016-01-17 21:42:26](https://i1.yuangezhizao.cn/macOS/20211105223034.png!webp)

</details>

- 吐槽：时至今日，各种服务也一直托管于你云

### 2.爬虫和`OCR`——`PY`初体验
然后等到专业课讲`C`语言的时候，觉得这门语言对于自己来说过于不便，业余时间就已经在看`py`了，还记得第一个**抄的**是识别`jwzx`（教务在线）的附加码（指验证码）的**爬虫**脚本

<details><summary>点击此处 ← 查看折叠</summary>

![第一次的 PY 交易](https://i1.yuangezhizao.cn/macOS/20211105231511.png!webp)

</details>

而实际上是一直<kbd>CTRL</kbd>+<kbd>C</kbd>`&`<kbd>CTRL</kbd>+<kbd>V</kbd>（标准`debug`套路，确信
- 首先，<kbd>CTRL</kbd>+<kbd>C</kbd>`&`<kbd>CTRL</kbd>+<kbd>V</kbd>抄的例子直接运行会报错；
- 然后，把报错信息<kbd>CTRL</kbd>+<kbd>C</kbd>`&`<kbd>CTRL</kbd>+<kbd>V</kbd>去搜索；
- 最后，再<kbd>CTRL</kbd>+<kbd>C</kbd>`&`<kbd>CTRL</kbd>+<kbd>V</kbd>改回本地……

反正是`xjb`搞到最后总算给跑起来了，**能用就行**（当然现在的标准是肯定不能止步于此了
印象里那里面还是错综复杂的对基于`python2`的`urllib2`库的调用，当然现在都用支持`python3`的`requests`库了，只能说时代的变化真的是太快了
> Requests: HTTP for Humans™

- 吐槽：最惨`jwzx`已经被草爆，据说大家都拿来练爬虫

<details><summary>点击此处 ← 查看折叠</summary>

![xs](https://i1.yuangezhizao.cn/macOS/20211106173907.png!webp)

</details>

### 3.正则表达式——从入门到跑路
然后，`4`天后就看上正则了草？现在直接黑人问号？那时候啥编程基础害都没有

<details><summary>点击此处 ← 查看折叠</summary>

![正则表达式](https://i1.yuangezhizao.cn/macOS/20211106234524.png!webp)

</details>

- 吐槽：时至今日，爬虫也只会写最开始抄的`(.*?)`这一种匹配神器，就像`magic number`一样？

### 4.查分脚本——写代码`VS.`选修课
显然，过于无聊的选修课肯定是比不上有着更大的诱惑的代码了（时至今日亦如此
那时候的目标极其明确，就是为了写出能一键查成绩的脚本，参照有类似需求的实现文章，现学`F12`抓包方法，现去分析`HTTP`请求
毕竟胶水语言，艰难的`OCR`识别验证码的部分已经搞定了，直接被登录调用就`OK`，那么剩下的就只有查成绩了，而正则表达式是为了格式化输出的
也佩服那时候的信念，坚决拒绝使用[Beautiful Soup](https://web.archive.org/web/20211108124416/https://www.crummy.com/software/BeautifulSoup/bs4/doc/)，因为看到文章有说其解析速度慢，当然这只是其中的一点原因，真的就像是信仰一样（

<details><summary>点击此处 ← 查看折叠</summary>

![一键查成绩](https://i1.yuangezhizao.cn/macOS/20211105235237.png!webp)
![后面放到了微信公众号里面，供自己班级同学的使用](https://i1.yuangezhizao.cn/macOS/20211106174150.png!webp)
![一点一点的优化](https://i1.yuangezhizao.cn/macOS/20211106174357.png!webp)
![计划任务](https://i1.yuangezhizao.cn/macOS/20211106174640.png!webp)
![大战 jwzx](https://i1.yuangezhizao.cn/macOS/20211106175210.png!webp)
![黑历史](https://i1.yuangezhizao.cn/macOS/20211106180730.png!webp)

</details>

- 吐槽`1`：学计算机是不可能的，这辈子都不可能的`⬇`（草这黑历史绝了，大老师自爆卡车！

<details><summary>点击此处 ← 查看折叠</summary>

![而计算机要 525](https://i1.yuangezhizao.cn/macOS/20211105230824.png!webp)
![黑历史](https://i1.yuangezhizao.cn/macOS/20211106205543.png!webp)

</details>

- 吐槽`2`：时至今日，也从未使用`BS4`，顶多[from lxml import etree](https://web.archive.org/web/20211108125849/https://lxml.de/tutorial.html)

### 5.各种脚本——`PY`逐渐上头

<details><summary>点击此处 ← 查看折叠</summary>

![不是自己干的.jpG](https://i1.yuangezhizao.cn/macOS/20211106005647.png!webp)
![黑历史](https://i1.yuangezhizao.cn/macOS/20211106010436.png!webp)
![黑历史](https://i1.yuangezhizao.cn/macOS/20211106011050.png!webp)

</details>

- 吐槽：`QZone`的水文数量呈指数型增长，时至今日，一发不可收拾

### 6.个人博客——水文不归路
这个时间点在折腾的是`Hexo`，是被`_config.yml`配置文件的缩进给坑惨了
`5.6`~`5.11`抽时间搭建上了，用得是`gh`的`pages`页面，还配置了告警`2333`，谷歌也是飞快收录即使是`github.io`子域

<details><summary>点击此处 ← 查看折叠</summary>

![黑历史](https://i1.yuangezhizao.cn/macOS/20211106011347.png!webp)
![第一篇水文](https://i1.yuangezhizao.cn/macOS/20211106012803.png!webp)
![第一次告警](https://i1.yuangezhizao.cn/macOS/20211106014320.png!webp)
![被索引](https://i1.yuangezhizao.cn/macOS/20211106151010.png!webp)
![后来懒得限制，就又给放开了](https://i1.yuangezhizao.cn/macOS/20211106162122.png!webp)

</details>

- 吐槽：这只是初代，后面还重建/换域名过几次

### 7.云主机——光速上云
毕竟云主机`24h`开机，是挂脚本的最佳之选，试用之后立即购买（云主机`+`域名）了

<details><summary>点击此处 ← 查看折叠</summary>

![试用](https://i1.yuangezhizao.cn/macOS/20211106012349.png!webp)
![付费](https://i1.yuangezhizao.cn/macOS/20211106013229.png!webp)

</details>

- 吐槽：这台上古机子上重装了无数次的操作系统……

### 8.`Google`——谁`tm`用百毒
这时候大一已经结束了（`2016`），暑假的时候第一次接触的国外服务商，这是已经在使用`Google`的迹象，也因为不良梯子提供商导致密码被嗅探泄露，也意识到**两步验证**的重要性

<details><summary>点击此处 ← 查看折叠</summary>

![黑历史](https://i1.yuangezhizao.cn/macOS/20211105230638.png!webp)
![vpncup](https://i1.yuangezhizao.cn/macOS/20211106014541.png!webp)
![有被吓到](https://i1.yuangezhizao.cn/macOS/20211106015806.png!webp)
![公开梯子，不可避免](https://i1.yuangezhizao.cn/macOS/20211106160726.png!webp)
![两步验证](https://i1.yuangezhizao.cn/macOS/20211106160830.png!webp)

</details>

- 吐槽：时至今日，也离不开`Google`，看一个百毒劝一个，宁可用`Bing`

### 9. 狗东——薅羊毛不归路

<details><summary>点击此处 ← 查看折叠</summary>

![怀念那个时代](https://i1.yuangezhizao.cn/macOS/20211106015103.png!webp)
![狗东抽奖](https://i1.yuangezhizao.cn/macOS/20211106171748.png!webp)
![抽中手办](https://i1.yuangezhizao.cn/macOS/20211106172602.png!webp)

</details>

- 吐槽：时至今日，确信！（狗东真的是一直陪伴着

### 10. `Pkav`——安全渗透之路

<details><summary>点击此处 ← 查看折叠</summary>

![尝试爆破](https://i1.yuangezhizao.cn/macOS/20211106020141.png!webp)

</details>

### 11.`PC Games`——单机`3A`大作
那个寒假（`2017`）终于独立打通了狗二，后来有段时间开始在`Steam`入正

<details><summary>点击此处 ← 查看折叠</summary>

![狗二](https://i1.yuangezhizao.cn/macOS/20211106151939.png!webp)
![传送门](https://i1.yuangezhizao.cn/macOS/20211106160218.png!webp)

</details>

- 吐槽：时至今日，也不玩网游，单机它不香吗？然而现在木有显卡草……

### 12.日漫新番——老二次元的开始
印象非常深刻，寒假在家第一次熬夜看最新话，是真正意义上的追新番的开始
原创不易，而搬运几乎无成本，所以一直在投稿新番的`OP/ED`，后来被版权了无数次
至于屯`BD`，拿`madVR`补番就是后来的事情了（懒得再截图了，就只放一张《未来日记》三周目

<details><summary>点击此处 ← 查看折叠</summary>

![HS](https://i1.yuangezhizao.cn/macOS/20211106152251.png!webp)
![OP/ED](https://i1.yuangezhizao.cn/macOS/20211106155153.png!webp)
![各种退回](https://i1.yuangezhizao.cn/macOS/20211106155523.png!webp)
![那时候好看的老番可以看好几遍](https://i1.yuangezhizao.cn/macOS/20211106162657.png!webp)
![233](https://i1.yuangezhizao.cn/macOS/20211106163843.png!webp)
![10w](https://i1.yuangezhizao.cn/macOS/20211106164016.png!webp)
![300](https://i1.yuangezhizao.cn/macOS/20211106164629.png!webp)
![400](https://i1.yuangezhizao.cn/macOS/20211106165050.png!webp)
![500](https://i1.yuangezhizao.cn/macOS/20211106165326.png!webp)
![600+](https://i1.yuangezhizao.cn/macOS/20211106165801.png!webp)
![第一次在 A 站补番](https://i1.yuangezhizao.cn/macOS/20211106170537.png!webp)
![707](https://i1.yuangezhizao.cn/macOS/20211106171306.png!webp)
![888](https://i1.yuangezhizao.cn/macOS/20211106175841.png!webp)
![999](https://i1.yuangezhizao.cn/macOS/20211106183726.png!webp)
![1K](https://i1.yuangezhizao.cn/macOS/20211106183931.png!webp)
![1010](https://i1.yuangezhizao.cn/macOS/20211106184405.png!webp)

</details>

### 13.`Flask`——沿用至今的`Web`框架
最开始用的域名是`app.yuangezhizao.cn`，`SSL`评测是`A`，其实只要上`HSTS`就能到`A+`
而之所以取名为`app`，从源码中也可以看到是**应用**的意思，就是这里存放着各种小应用，但是`keywords`和`description`也包含**实验室**
直到`2018`年，更换了子域名到`lab`，一直延续至今

<details><summary>点击此处 ← 查看折叠</summary>

![SUT Dormitory Cache](https://i1.yuangezhizao.cn/macOS/20211105230113.png!webp)
![TODO](https://i1.yuangezhizao.cn/macOS/20211106163627.png!webp)
![DEBUG](https://i1.yuangezhizao.cn/macOS/20211106164338.png!webp)
![SUTDB](https://i1.yuangezhizao.cn/macOS/20211106164357.png!webp)
![LNUOC](https://i1.yuangezhizao.cn/macOS/20211106165151.png!webp)
![A](https://i1.yuangezhizao.cn/macOS/20211106170053.png!webp)
![app.yuangezhizao.cn](https://i1.yuangezhizao.cn/macOS/20211106170844.png!webp)
![lab.yuangezhizao.cn](https://i1.yuangezhizao.cn/macOS/20211106182709.png!webp)
![全是实验性质的产物](https://i1.yuangezhizao.cn/macOS/20211106183621.png!webp)
![SUT_WatchDogs](https://i1.yuangezhizao.cn/macOS/20211106204537.png!webp)
![SUTDB](https://i1.yuangezhizao.cn/macOS/20211106205402.png!webp)
![联动](https://i1.yuangezhizao.cn/macOS/20211106210240.png!webp)
![更新日志](https://i1.yuangezhizao.cn/macOS/20211106223135.png!webp)
![自动更新](https://i1.yuangezhizao.cn/macOS/20211106223332.png!webp)

</details>

- 吐槽：时至今日，甚至工作上用的也是`Flask`，真的是缘分

### 14.`Requests`——从爬虫到入狱（bushi
那时候还用的`SQLite3`，后来导入`MySQL`，对你`b`用户信息`api`实施爆破

<details><summary>点击此处 ← 查看折叠</summary>

![SQLite3](https://i1.yuangezhizao.cn/macOS/20211106154223.png!webp)
![MySQL](https://i1.yuangezhizao.cn/macOS/20211106154613.png!webp)
![65873864](https://i1.yuangezhizao.cn/macOS/20211106160015.png!webp)
![巨慢的导入流程](https://i1.yuangezhizao.cn/macOS/20211106161337.png!webp)
![黑历史](https://i1.yuangezhizao.cn/macOS/20211106171659.png!webp)

</details>

## 0x03.后记
整理这种文章真的是巨费时间，图片数量众多因此对`SEO`还不友好……

> 至此本文使命完成
