---
title: MuseDash 排行榜数据存储
date: 2020-3-7 23:08:00
tags:
  - MuseDash
count: 1
os: 0
os_1: 10.0.17763.1039 2019-LTSC
browser: 0
browser_1: 78.0.3904.108 Stable
place: 新家
key: 77
---
    8.5 6 的 6 终于熬过来了，刷推听 HH 就到了这个时间点了……
    时间太短又不想打「超凡双生」，结果就莫名跑到 Cloud Studio 了
<!-- more -->
## 0x00.前言
这游戏说到底还是烤盐前的那个夏天，看到鸽王在`wb`晒内录，于是就去`TapTap`氪了首单，也算是老用户了
配好`HTTPS`代理，从网络的角度谁都能看出来这引诱防护做的并不好，但是这里并不再去讲白嫖这条路
而是去看它的另一方面——排行榜数据

## 0x02.[MuseDash](https://github.com/yuangezhizao/MuseDash)
从最开始的移动端逐渐推广至`Switch`、`Steam`以及`WeGame`……因此它的排行榜数据也分多个平台，不同平台之间的数据是不互通的
本人保存的完整记录只限于`Android`，时间跨度算是很大，最久远的可以追溯到`191001`，最新的直到现在
虽然存储到本地的`json`文件并不大，但是巨多的歌曲数量直接使整个文件夹增加了一个数量级
然后，可以回来说此章节的标题`gh`仓库地址了，最开始几乎（非全部）所有的文件全扔上去了，虽然心里知道这是不合理的虽然可能算不上滥用
但是也并没有别的公开的地方可以放置这玩楞，于是就一直没去打理的样子，直到某天检查`QQ`收件箱发现了`gh`官方寄来的一封邮件
大致内容就是说拿`gh`当做`database`是不适合的，建议使用例如`AWS`之类的存储服务，于是就返信表示会处理
第二天检查本地文件夹发现有一个之前同步过的本地仓库，于是`git pull`之后就同步完成了，就删了`gh`仓库后返信处理完成
想着总感觉还是少了点儿啥，于是又去重新建立了个同名仓库，里面只写了一个`README.md`文件描述了下历史
之后又给扔到`Coding`的仓库上了，结果刚开始还可以`push`上去的，不知道从哪天开始就限制仓库大小了，于是这玩楞就又没有地方放置了
目前也只是在数据下载那台机子上照常`git commit`下就没再`push`了

## 0x03.数据下载
很明显使用的是`LeanCloud`的`PaSS`？`SaSS`服务，`leaderboard`接口就不赘述了
倒是感觉文件的命名比较重要，因为基本上确定下来就不会再去更改了，参考[splash_fetch](https://www.biliplus.com/task/splash_fetch/)
``` bash
Index of /task/splash_fetch/
../
20160205_18-75eb7959.json                          25-Dec-2018 11:19                2521
20160207_12-54328731.json                          25-Dec-2018 11:19                 788
```
这里采用的是**日期**`+`**`_`**`+`**曲包**`+`**`-`**`+`**曲号**`+`**`-`**`+`**难度**`+`**`.json`**，举个栗子：`200301_0-0-1.json`
直接屯到了`C:\LAB\main\static\static\json\musedash\ranking`目录下

## 0x04.数据处理
这里说的数据处理并不是处理文件内部，而是文件整体
### 1. 新建日期文件夹
``` bash
mkdir {200218..200229}
```

### 2. 按照日期移动
因为机子上除了`50G`的系统盘之外还额外购买了块`10G`的数据盘挂载上了，而`.git`仓库就扔在`D`盘了，所以自然需要进行移动操作了
这里说到底还是因为懒没能整个计划任务自动进行，非常可能就攒了几个月之后发现系统盘空间骤减，才想起来该处理数据了
然后比较遗憾的是效率非常低下，每次都是手动移动文件夹，并且限于机子性能速度异常缓慢（倒也不是巨慢），还经常手残出错
最开始文件都是手动重命名，后来用上了`橙刀改名器`，最后终于忍不了了直接写了个脚本：
``` bash
#!/bin/bash
path="/c/LAB/main/static/static/json/musedash/ranking"
files=$(ls $path)
for file in $files
do
  echo ${file:0:6} ${file:7:11}
  mv "/c/LAB/main/static/static/json/musedash/ranking/"$file "/d/MuseDash/ranking/"${file:0:6}"/"${file:7:11}
done
echo "Done"
```

### 3. `Git`提交
直接上`shell`：
``` bash
for i in {200218..200229}; do echo "$i start"; git add $i/ >/dev/null && git commit -m "$i" >/dev/null && git push >/dev/null; rm -rf $i/; echo "$i ok"; done
```
之前所说的“还经常手残出错”在这里也经常碰到，而且比之前更严重，毕竟直接整个整理好的文件夹就没了，可是正好一天的数据
真`·`删库跑路：`rm -rf`
比如眼睛看花了（这里其实写的`bash`正常运行的话是一点问题都没有的），可是就会出现那种情况直接<kbd>CTRL</kbd>`+`<kbd>C</kbd>
结果就是直接执行`rm -rf $i/;`这个步骤了，而且每按一次组合键就会有一天的数据被消除掉……
现在，只在本地存储的`shell`如下：
``` bash
for i in {200218..200229}; do echo "$i start"; git add $i/ >/dev/null && git commit -m "$i" >/dev/null; rm -rf $i/; echo "$i ok"; done
```

## 0x05.后记
写到最后发现没有去加**颜文字**，今天为了省时间就暂时不追加了
未完待续……