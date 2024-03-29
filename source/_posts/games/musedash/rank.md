---
title: MuseDash 排行榜数据存储
date: 2020-3-7 23:08:00
tags:
  - MuseDash
count: 4
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

## 0x01.[MuseDash](https://github.com/yuangezhizao/MuseDash)
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

## 0x02.数据下载
`2020-5-29 21:48:31`：`CELERY`安排上计划任务
``` python
CELERYBEAT_SCHEDULE = {
    'Execute-every-1-day_0': {
        'task': 'main.plugins.cron.task_get_all_musedash_ranking',
        'schedule': crontab(minute='0', hour='0'),
        'options': {'queue': 'musedash'}
    },
}
```
`2020-8-4 23:00:17`：woc，都出了多少曲包了……
![握草](https://i1.yuangezhizao.cn/Win-10/20200804210838.jpg!webp)
![27](https://i1.yuangezhizao.cn/Win-10/20200804225619.jpg!webp)

``` python
@celery.task(bind=True)
def task_get_all_musedash_ranking(self):
    all = [
        # 基础曲包：unlock_base
        '0-0', '0-1', '0-2', '0-3', '0-4', '0-5', '0-6', '0-7', '0-8', '0-9', '0-10', '0-11', '0-12', '0-13', '0-14',
        '0-15', '0-16', '0-17', '0-18', '0-19', '0-20', '0-21', '0-22', '0-23', '0-24', '0-25', '0-26', '0-27', '0-28',
        '0-29', '0-30', '0-31', '0-32', '0-33', '0-34', '0-35', '0-36', '0-37', '0-38', '0-39', '0-40', '0-41', '0-42',
        '0-43', '0-44', '0-45',
        # 曲包1 - 可爱即正义 Vol.1：music_package_1
        '1-0', '1-1', '1-2', '1-3', '1-4', '1-5',
        # 曲包2 - 放弃治疗 Vol.1：music_package_2
        '2-0', '2-1', '2-2', '2-3', '2-4', '2-5',
        # 曲包3 - 肥宅快乐包 Vol.1：music_package_3
        '3-0', '3-1', '3-2', '3-3', '3-4', '3-5',
        # 曲包4 - 肥宅快乐包 Vol.2：music_package_4
        '4-0', '4-1', '4-2', '4-3', '4-4', '4-5',
        # 曲包5 - 肥宅快乐包 Vol.3：music_package_5
        '5-0', '5-1', '5-2', '5-3', '5-4', '5-5',
        # 曲包6 - 经费在燃烧：music_package_6
        '6-0', '6-1', '6-2', '6-3', '6-4', '6-5',
        # 曲包7 - 放弃治疗 Vol.2：music_package_7
        '7-0', '7-1', '7-2', '7-3', '7-4', '7-5',
        # 曲包8 - 放弃治疗 Vol.3：music_package_8
        '8-0', '8-1', '8-2', '8-3', '8-4', '8-5',
        # 曲包9 - 肥宅快乐包 Vol.4：music_package_9
        '9-0', '9-1', '9-2', '9-3', '9-4', '9-5',
        # 曲包10 - 放弃治疗 Vol.4：music_package_10
        '10-0', '10-1', '10-2', '10-3', '10-4', '10-5',
        # 曲包11 - 肥宅快乐包 Vol.5：music_package_11
        '11-0', '11-1', '11-2', '11-3', '11-4', '11-5',
        # 曲包12 - 放弃治疗 Vol.5：music_package_12
        '12-0', '12-1', '12-2', '12-3', '12-4', '12-5',
        # 曲包13 - 可爱即正义 Vol.2：music_package_13
        '13-0', '13-1', '13-2', '13-3', '13-4', '13-5',
        # 曲包14 - 肥宅快乐包 Vol.6：music_package_14
        '14-0', '14-1', '14-2', '14-3', '14-4', '14-5',
        # 曲包15 - 可爱即正义 Vol.3：music_package_15
        '15-0', '15-1', '15-2', '15-3', '15-4', '15-5',
        # 曲包16 - 放弃治疗 Vol.6：music_package_16
        '16-0', '16-1', '16-2', '16-3', '16-4', '16-5',
        # 曲包17 - 肥宅快乐包 Vol.7：music_package_17
        '17-0', '17-1', '17-2', '17-3', '17-4', '17-5',
        # 曲包18 - 可爱即正义 Vol.4：music_package_18
        '18-0', '18-1', '18-2', '18-3', '18-4', '18-5',
        # 曲包19 - 放弃治疗 Vol.7：music_package_19
        '19-0', '19-1', '19-2', '19-3', '19-4', '19-5',
        # music_package_19：music_package_20
        '20-0', '20-1', '20-2', '20-3', '20-4', '20-5',
        # 曲包21 - 经费在燃烧: 纳米核心：music_package_21
        '21-0', '21-1', '21-2',
        # 曲包22 - 放弃治疗 Vol.8：music_package_22
        '22-0', '22-1', '22-2', '22-3', '22-4', '22-5',
        # 曲包23 - 可爱即正义 Vol.5：music_package_23
        '23-0', '23-1', '23-2', '23-3', '23-4', '23-5',
        # 曲包24 - 肥宅快乐包 Vol.9：music_package_24
        '24-0', '24-1', '24-2', '24-3', '24-4', '24-5',
        # 曲包25 - 暮色电台：music_package_25
        '25-0', '25-1', '25-2', '25-3', '25-4', '25-5',
        # 曲包26 - 放弃治疗 Vol.9：music_package_26
        '26-0', '26-1', '26-2', '26-3', '26-4', '26-5',
        # 曲包27 - ななひら Festival：music_package_27
        '27-0', '27-1', '27-2', '27-3', '27-4', '27-5',
    ]
    for music_uid in all:
        for music_difficulty in range(1, 4):
            task_musedash_ranking.apply_async((music_uid, music_difficulty), queue='musedash')
    return 'done'
```
很明显使用的是`LeanCloud`的`PaSS`？`SaSS`服务，`leaderboard`接口就不赘述了
倒是感觉文件的命名比较重要，因为基本上确定下来就不会再去更改了，参考[splash_fetch](https://www.biliplus.com/task/splash_fetch/)
``` bash
Index of /task/splash_fetch/
../
20160205_18-75eb7959.json                          25-Dec-2018 11:19                2521
20160207_12-54328731.json                          25-Dec-2018 11:19                 788
```
这里采用的是**日期**`_`**曲包**`-`**曲号**`-`**难度**`.json`，举个栗子：`200301_0-0-1.json`
直接屯到了`C:\LAB\main\static\static\json\musedash\ranking`目录下

## 0x03.数据处理
这里说的数据处理并不是处理文件内部，而是文件整体
### 1.新建日期文件夹
``` bash
mkdir {200218..200229}
```

### 2.按照日期移动
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

### 3.`Git`提交
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

## 0x04.后记
写到最后发现没有去加**颜文字**，今天为了省时间就暂时不追加了
未完待续……