---
title: 生成 bilibili 你的名字告白关键词词云
date: 2017-10-5 11:32:23
tags:
  - WordCloud
  - bilibili
count: 2
os: 0
os_1: 10.0.15063 Pro
browser: 0
browser_0: 61.0.3163.100 Dev
place: 家
key: 26
gitment: true
---
    不知不觉中十一在家的假期要结束了
<!-- more -->
## 0x00.前言
此文于`2017-10-21 21:21:13`开始补坑，`2017-10-21 22:44:23`补完

## 0x01.存数据
看到这个[活动页](http://www.bilibili.com/blackboard/topic/activity-yourname1708.html)，就想把“告白”内容存到数据库里，老样子`F12`+`XHR`看到相关接口有俩：
`http://www.bilibili.com/activity/likes/list/10156?t=1508592478785&page=1&pagesize=1`
`http://www.bilibili.com/activity/likes/random/10156?t=1508592478788&count=100`
根据命名个人觉着第一个接口适合我们用，毕竟第二个这种取随机不一定能获取完全。经过测试，构造出如下利于爬取的链接：
`http://www.bilibili.com/activity/likes/list/10156?pagesize=49&page= < 此处填写页码 >`
从活动开始到结束，现在留有`104368`条，如图所示，
![](https://i1.yuangezhizao.cn/Win-10/20171021221549.jpg!webp)

给你们看一下表的数据条数，我确实全部保存下来了：
![](https://i1.yuangezhizao.cn/Win-10/20171021221309.jpg!webp)

所以`2130`页就足以获取全部。
快速爬取（仅适用于非 b 的`API`服务器且无反爬）的话可以这样：
``` python
# -*- coding: utf-8 -*-
import requests
import json
import pymysql
from multiprocessing.dummy import Pool as ThreadPool


def get_source(page):
    url = "http://www.bilibili.com/activity/likes/list/10156?pagesize=49&page=" + str(page)
    response = requests.get(url).text
    jsDict = json.loads(response)
    if jsDict['code'] == 0:
        list_1 = jsDict['data']['list']
        for each in list_1:
            id = each['id']
            print id
            sid = each['sid']
            state = each['state']
            type = each['type']
            mid = each['mid']
            wid = each['wid']
            ctime = each['ctime']
            likes = each['likes']
            liked = each['liked']
            message = each['message']
            device = each['device']
            image = each['image']
            plat = each['plat']
            reply = each['reply']
            link = each['link']

            owner_mid = each['owner']['mid']
            owner_name = each['owner']['name']
            owner_face = each['owner']['face']
            owner_sex = each['owner']['sex']

            owner_level_info_current_level = each['owner']['level_info']['current_level']
            owner_level_info_current_min = each['owner']['level_info']['current_min']
            owner_level_info_current_exp = each['owner']['level_info']['current_exp']
            owner_level_info_next_exp = each['owner']['level_info']['next_exp']

            try:
                connection = pymysql.connect(
                    host='localhost', user='root', passwd='***', db='bilibili', charset='utf8')
                with connection.cursor() as cursor:
                    sql = "INSERT INTO `yourname` (`id`,`sid`,`state`,`type`,`mid`,`wid`,`ctime`,`likes`,`liked`, `message`,`device`,`image`,`plat`, `reply`,`link`,`owner_mid`,`owner_name`,`owner_face`, `owner_sex`,`owner_level_info_current_level`,`owner_level_info_current_min`,`owner_level_info_current_exp`,`owner_level_info_next_exp`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (
                    id, sid, state, type, mid, wid, ctime, likes, liked, message, device, image, plat, reply, link,
                    owner_mid, owner_name, owner_face, owner_sex, owner_level_info_current_level,
                    owner_level_info_current_min, owner_level_info_current_exp, owner_level_info_next_exp))

                connection.commit()
            except Exception as e:
                print e
            finally:
                connection.close()
    else:
        print "Error"

i_1 = []
for i in range(0, 2030):
    i_1.append(i)

pool = ThreadPool(500)
try:
    results = pool.map(get_source, i_1)
except Exception as e:
    print e
    pool.close()
    pool.join()

pool.close()
pool.join()
```

## 0x02.`MySQL`导出纯文本
参考[从mysql中导出一列数据到txt](http://blog.csdn.net/u012654154/article/details/73036789)，把`bilibili`数据库`yourname`表中的`message`字段全部内容保存至一文本文档（本例存在`C:/DARA/out.txt`）中
```
mysql> use bilibili;
Database changed
mysql> select message into outfile "c:/DATA/out.txt" lines terminated by "\r\n" from yourname;
1290 - The MySQL server is running with the --secure-file-priv option so it cannot execute this statement
```
修改`my.ini`末尾添加`secure_file_priv="C:/DATA/"`，保存并重启数据库。
```
mysql> show variables like '%secure%';
+------------------+----------+
| Variable_name    | Value    |
+------------------+----------+
| secure_auth      | OFF      |
| secure_file_priv | C:\DATA\ |
+------------------+----------+
2 rows in set
```
如上所示则已生效
```
mysql> select message into outfile "c:/DATA/out.txt" lines terminated by "\r\n" from yourname;
Query OK, 104368 rows affected
```
再次运行得到`out.txt`，`FTP`传回本地。
![](https://i1.yuangezhizao.cn/Win-10/20171021221800.jpg!webp)

## 0x03.[结巴中文分词](https://github.com/fxsjy/jieba)
用以提取关键词，可以这样：
``` python
import jieba.analyse
import cPickle as pickle

content = open("out.txt", 'r').read()
tags = jieba.analyse.extract_tags(content, topK=100, withWeight=True)
print "Finished extraction."
for tag in tags:
    print tag[0], "\t", tag[1]

with open("./assets/tags.pickle", "w") as f:
    pickle.dump(tags, f)
```
运行结果如下：
``` python
Building prefix dict from the default dictionary ...
Loading model from cache c:\users\yuange~1\appdata\local\temp\jieba.cache
Loading model cost 0.462 seconds.
Prefix dict has been built succesfully.
Finished extraction.
喜欢 	0.324251093864
我爱你 	0.141492171794
希望 	0.0872011423752
一起 	0.0645035960844
永远 	0.0624222569269
我会 	0.0570180337732
一直 	0.0555175407499
名字 	0.054767164132
我们 	0.0483923629279
告白 	0.0480520036241
遇见 	0.0404470021514
知道 	0.0380303658285
表白 	0.0375291125829
真的 	0.0346544513713
相遇 	0.0333705541785
还是 	0.0325035732867
忘记 	0.0282951578971
二次元 	0.0268951184777
虽然 	0.0267818329394
不会 	0.0255878815482
未来 	0.0251641649911
但是 	0.024407187094
幸福 	0.0238904170345
一定 	0.0235970363729
一个 	0.0222749620653
那个 	0.0220862023796
自己 	0.0208379896841
现在 	0.0208044554451
我要 	0.0199511389164
没有 	0.0193877103187
遇到 	0.0188617945085
如果 	0.0182736407689
再见 	0.0177817180204
找到 	0.0176360616325
世界 	0.0169725262572
七夕 	0.0168677168831
... 	0.0165303584246
加油 	0.0165085656864
可以 	0.0164258453739
谢谢 	0.0162835181917
一生 	0.0160791235199
啊啊啊 	0.0160787253266
记得 	0.0156403210769
三年 	0.0154236874264
好好 	0.0152625773588
身边 	0.015161018891
即使 	0.0148554953566
一辈子 	0.0145913427404
努力 	0.0143755498617
此生 	0.0143429949614
你们 	0.0142989803287
什么 	0.0139712428593
不管 	0.0138434591696
就是 	0.0137978195567
以后 	0.0133039175692
时候 	0.0131537926656
单身 	0.0130653440919
一天 	0.013018358808
开心 	0.0125408371338
我能 	0.0124950664672
无论 	0.0124649435768
守护 	0.0124503674775
一次 	0.0118370516219
陪伴 	0.0117597817649
女朋友 	0.0117143186911
不能 	0.0116363826448
三叶 	0.0112544888653
安好 	0.0111032197697
可能 	0.0107953851099
祝你幸福 	0.0107196615408
因为 	0.0106407939045
也许 	0.010609106987
感谢 	0.0106036173337
已经 	0.010543736305
哔哩 	0.0104262111997
心意 	0.0104215537926
暗恋 	0.0103705181058
只是 	0.0102918636606
快乐 	0.0102163069019
就算 	0.0101965684284
爱着 	0.0101303157723
不想 	0.0100458353843
下去 	0.00991074980489
一年 	0.0098914282562
相见 	0.00975838837469
对不起 	0.00967898614789
不要 	0.00959938169197
美好 	0.00956585198602
告诉 	0.00952197220922
一切 	0.00946857669345
那么 	0.00945186230346
哪里 	0.00934967618021
想要 	0.00915397039592
不是 	0.00903258766246
看到 	0.00883566669778
电影 	0.00882967071275
曾经 	0.00870491366138
时间 	0.00867462160313
相信 	0.00867211421126
愿意 	0.00843351469339
```

## 0x04.`WordCloud`绘制词云
简单使用啦，可以这样：
``` python
# -*- coding:utf-8 -*-
""" 生成词云图片 """
from wordcloud import WordCloud, ImageColorGenerator
import cPickle as pickle
import numpy as np
from PIL import Image

if __name__ == "__main__":
    # 读取词频
    with open("./assets/tags.pickle", "r") as f:
        tags = pickle.load(f)
        frequencies = {}
        for tag in tags:
            frequencies[tag[0]] = int(10000 * tag[1])

    wc = WordCloud(font_path='./assets/simhei.ttf',  # 设置字体
                   background_color="black",  # 背景颜色
                   max_words=100,  # 词云显示的最大词数
                   max_font_size=500,  # 字体最大值
                   # random_state=42,
                   width=1366,
                   height=768)

    wc.generate_from_frequencies(frequencies)

    # 颜色转换
    rainbow_coloring = np.array(Image.open("./assets/rainbow.jpg!webp"))
    image_colors = ImageColorGenerator(rainbow_coloring)
    wc.recolor(color_func=image_colors)

    # 保存图片
    wc.to_file("./assets/word_cloud1.png!webp")
    print "saved at ./assets/word_cloud1.png!webp"

```
## 0x05.结果图片
![](https://i1.yuangezhizao.cn/Win-10/20171021222714.png!webp)

上面那张是词云，下面这张是点赞排行榜
![](https://i1.yuangezhizao.cn/Win-10/20171021223837.jpg!webp)

## 0x06.引用
> [生成词云之python中WordCloud包的用法](https://web.archive.org/web/20190905064506/https://blog.csdn.net/u010309756/article/details/67637930)
[把300W淘宝文胸评论绘制成词云](https://web.archive.org/web/20190905064553/http://nladuo.github.io/2017/04/07/%E6%8A%8A300W%E6%B7%98%E5%AE%9D%E6%96%87%E8%83%B8%E8%AF%84%E8%AE%BA%E7%BB%98%E5%88%B6%E6%88%90%E8%AF%8D%E4%BA%91/)
