---
title: 基于酷 Q Python SDK 的一个签到插件的开发
date: 2017-02-25 16:17:32
tags:
  - cool-q
  - python
  - sign-in
count: 1
os: 0
os_1: 10.0.14393 Pro
browser: 0
browser_1: 56.0.2924.87 Stable
place: 家
key: 03
---
    早在一个月前插件就写好了，不过和往常一样假期沉迷日漫所以就一直拖到了开学前最后一天也就是今天。
    明天又要返校了，呜呜呜~~~
<!-- more -->
## 0x00.前言
先来说说什么是 SDK，这是维基百科的解释。
> 软件开发工具包（Software Development Kit， SDK）一般是一些被软件工程师用于为特定的软件包、软件框架、硬件平台、作业系统等创建应用软件的开发工具的集合。
它或许只是简单的为某个编程语言提供应用程序接口的一些文件，但也可能包括能与某种嵌入式系统通讯的复杂的硬件。一般的工具包括用于调试和其他用途的实用工具。SDK还经常包括示例代码、支持性的技术注解或者其他的为基本参考资料澄清疑点的支持文档。

里面谈到了`应用程序接口`，看到了这个应该很熟悉吧，其英文缩写就是`API`。

## 0x01.开发
[点此链接](http://git.oschina.net/muxiaofei/cq_python_sdk)下载 SDK，并按照作者详细的`README`说明部署好本地环境。
然后我们就要在`CQHandler.py`里实现自己的事件处理逻辑了。
先定义一个时间与日期的函数，获取时间就靠它了：
``` python
from datetime import datetime

def get_nowtime(type):
    nowtime = datetime.now()
    if   type == 0:
        return nowtime
    elif type == 1:
        return str(nowtime.strftime("%Y年%m月%d日 %H时%M分%S秒"))   #nowtime_str
    elif type == 2:
        return str(nowtime.strftime("%Y-%m-%d"))                   #nowdate_str
    elif type == 3:
        return str(nowtime.strftime("%H:%M:%S"))                   #sign_str
```
在`class CQHandler(object)`里的`def OnEvent_GroupMsg(self, subType, sendTime, fromGroup, fromQQ, fromAnonymous, msg, font)`我们开始实现签到处理逻辑。
``` python
if msg == '查询签到' or msg[1:8] == "CQ:sign":
try:
    DATE = get_nowtime(2)
    TIME = get_nowtime(3)
    #最先记录时间
```
我们要把用户签到的数据存到数据库里，我用的是`SQlite`，并且每个群有单独的数据库（其实一个数据库应该也可以）。这里分两种情况考虑，一种是还没有数据库的，我们得先创建表后直接插入新的日期列，另一种是有数据库的，要判断是否需要插入新的日期列。
``` python
    if os.path.exists(str(fromGroup) + ".db"):
        conn = sqlite3.connect(str(fromGroup) + ".db")
        c = conn.cursor()
    else:
        conn = sqlite3.connect(str(fromGroup) + ".db")
        c = conn.cursor()
        c.execute('''CREATE TABLE "sign_in"(
                    ID INT PRIMARY KEY,
                    QQ INT,
                    RINK INT,
                    TIMES INT,
                    SERIES INT,
                    LAST TEXT)''')
                    c.execute("INSERT INTO sign_in VALUES (0, 0, 0, 0, 0, '00-00-00')")
    #连接完数据库第一件事情：查看是否需要插入新的日期列；
    c.execute("PRAGMA table_info (sign_in)")
    a = c.fetchall()
    #获取最后一列的信息，即日期
    if str(a[-1][1]) == DATE:
        pass
    else:
        c.execute("ALTER TABLE sign_in ADD COLUMN \"" + DATE + "\" TEXT")
        #插入新的日期列
        c.execute("UPDATE sign_in SET RINK = 0 ")
        #重置排名
```
这里又分两种情况考虑，一种是用户不在数据库里，我称之为“未注册”用户，直接`INSERT`。
``` python
    c.execute("SELECT * FROM sign_in WHERE QQ = {0}".format(str(fromQQ)))
    b = (c.fetchone())
    if b == None:
        logging.info("未注册")
        c.execute("SELECT count(*) FROM sign_in")
        b = c.fetchone()
        id = int(b[0])
        #获取 ID 号，注意第二行就是 ID = 1
        c.execute("SELECT max(RINK) FROM sign_in")
        b = c.fetchone()
        rank = b[0] + 1
        c.execute("INSERT INTO sign_in (ID, QQ, RINK, TIMES, SERIES, \'" + DATE + "\', LAST) VALUES (?, ?, ?, ?, ?, ?, ?)", (id, str(fromQQ), rank, 1, 1, TIME, DATE))
        CQSDK.SendGroupMsg(fromGroup, "签到成功！[CQ:at,qq={0}]\n\
签到时间：{1} {2}\n\
你是今天第 {3} 个在本群签到的人\n\
总计签到 1 次\n\
连续签到 1 次".format(str(fromQQ), DATE, TIME, str(rank)))
        conn.commit()
        conn.close()
```
另一种则是用户在数据库里，判断当天是否签到。（ps：那个“辅助方法”，同样的代码，在这里运行就是报错。无奈之下我换成了网络验证，把代码放在了`Flask`里，你们不要学我，2333……）
``` python
else:
    logging.info("已注册")
    #已注册查询当天是否签到
    c.execute("SELECT * FROM sign_in WHERE QQ = {0}".format(str(fromQQ)))
    b = c.fetchone()
    TIME_1 = b[-1]
    times = b[3]
    series = b[4]
    last = str(b[5])
    #读取签到时间
    #if len(TIME_1) != 0:
    if TIME_1 != None:
        logging.info("已签到")
        rank = b[2]
        CQSDK.SendGroupMsg(fromGroup, "你已签到！[CQ:at,qq={0}]\n\
签到时间：{1} {2}\n\
你是今天第 {3} 个在本群签到的人\n\
总计签到 {4} 次\n\
连续签到 {5} 次".format(str(fromQQ), DATE, TIME_1, str(rank), str(times), str(series)))
    conn.commit()
    conn.close()
    else:
        logging.info("未签到")
        c.execute("SELECT max(RINK) FROM sign_in")
        b = c.fetchone()
        rank = b[0] + 1
        #获取 RINK 值
        times = times + 1
        #总次数增加一天
        url = "https://new.yuangezhizao.cn/series/" + last
        r = open_url(url)
        #辅助方法
        if r == "1":
            series = series + 1
        else:
            series = 1
        c.execute("UPDATE sign_in SET RINK = {0}, TIMES = {1}, SERIES = {2}, LAST = \'{3}\', \'".format(rank, times, series, DATE) + DATE + "\' = \'{0}\' where QQ = {1}".format(TIME, str(fromQQ)))
        CQSDK.SendGroupMsg(fromGroup, "签到成功！[CQ:at,qq={0}]\n\
签到时间：{1} {2}\n\
你是今天第 {3} 个在本群签到的人\n\
总计签到 {4} 次\n\
连续签到 {5} 次".format(str(fromQQ), DATE, TIME, str(rank), str(times), str(series)))
        conn.commit()
        conn.close()
```
最后，
``` python
except Exception as e:
    logging.exception(e)
```
附`Flask`部分：
``` python
@app.route('/series/<last>')
def series(last):
    DATE = get_nowtime(2)
    DATE_1 = datetime.strptime(DATE, "%Y-%m-%d")
    last_1 = datetime.strptime(last, "%Y-%m-%d")
    minus = DATE_1 - last_1
    #格式化后比较日期
    if str(minus) == "1 day, 0:00:00":
        return "1"
    else:
        return "0"
```
这样插件就写好了。
数据库`Show CREATE Statement`，其中`RINK`是“当日排名”，`TIMES`是“总次数”，`SERIES`是“连续签到次数”，`LAST`是“上一次签到日期”配合前者做判断。
``` sql
CREATE TABLE "sign_in"(
                    ID INT PRIMARY KEY,
                    QQ INT,
                    RINK INT,
                    TIMES INT,
                    SERIES INT,
                    LAST TEXT);
```
## 0x02.总结
从源码可以看出没有什么实质性的难度，都是些基本操作，我们只要实现自己的事件处理逻辑即可，适合于定制功能。
