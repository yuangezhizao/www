---
title: SUT 大学外语六级报名报警系统
date: 2017-3-20 00:00:55
tags:
  - python
count: 2ss
os: 0
os_1: 10.0.14393 Pro
browser: 0
browser_1: 56.0.2924.87 Stable
place: 宿舍
key: 05
---
    该来的总是要来的
<!-- more -->
## 0x00.写在前面
1. 说明：
本程序使用 python 构建，仅供学习交流使用

2. 缘由：
其一：
大一时想的很好，计划一个学期选一们体育课，分别选了乒乓，排球，网球。这学期适合我的就剩羽毛了，没想到慢了一步，居然没选上……
其二：
> 注：由于学校考场数量有限，本次英语六级报名对有资格报名的学生采取先报先得的原则，报名额满上限为止，请参加英语六级报名的学生提前做好准备！——来自《教务在线主站》

中国人说话有一特点，重点永远放在最后面。如果不是这句话，我是不会萌生写这个程序的想法的……

## 0x02.思路逻辑
登陆后间隔设定的时间重复查询报名页面是否含有“英语六级”这一关键字，如有则给自己发送邮件（短信），反之 pass……

## 0x03.代码细节
一共分两步。
第一步，登陆教务在线主站
``` python
import requests
# 仍然使用 requests 这个第三方库

fjm_url = "http://jwc.sut.edu.cn/ACTIONVALIDATERANDOMPICTURE.APPPROCESS"
# 附加码图片对应地址
LoginUrl = "http://jwc.sut.edu.cn/ACTIONLOGON.APPPROCESS?mode=4"
# post 登陆对应地址

s = requests.Session()
# 会话对象，我们可以跨请求保持一些 cookie

img = s.get(fjm_url)
# get 请求附加码图片
with open('fjm.jpg', 'wb') as f:
    f.write(img.content)
# 保存图片为同目录下的 fjm.jpg

fjm = raw_input("请输入附加码：")
# 此时需要用户的输入

username = "< 此处替换为学号 >"
password = "< 此处替换为密码 >"

LoginData = {
    'WebUserNO': username,
    'Password': password,
    'Agnomen': fjm
}
# 封装数据包

r = s.post(LoginUrl, data=LoginData)
# 登陆
```

第二步，查询报名列表页面是否含有“英语六级”这一关键字

``` python
bmlb_url = "http://jwc.sut.edu.cn/ACTIONBMSIGNUP.APPPROCESS?mode=2"
# 报名列表对应地址
u = s.post(bmlb_url, data={"SignUpNO": 60, "Submit": "%CF%C2%D2%BB%B2%BD"})
# 查询

import re
# 这是个正则的库

tag = u"英语六级"
if re.search(tag, u.text):
    print "可以报名英语六级啦"
    send_mail()
else:
    pass
# 查询是否含有“英语六级”这一关键字
```
上文中`send_mail()`就是执行发送邮件的操作，需要提前定义好。我是用 163 邮箱发送报警邮件到 qq 邮箱，还能收到短信提醒，何乐而不为
``` python
def send_mail():
    import smtplib
    from email.header import Header
    from email.mime.text import MIMEText

    from_addr = '< 此处替换为你的 163 邮箱地址 >'
    password = '< 此处替换为你的 163 邮箱授权码 >'
    to_addr = '< 此处替换为你的 qq 邮箱地址 >'
    smtp_server = 'smtp.163.com'
    smtp_port = 25

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    server.set_debuglevel(1)
    server.login(from_addr,password)
    msg = MIMEText(u'可以报名英语六级啦', 'plain', 'utf-8')
    msg['From'] =from_addr
    msg['Subject'] = Header(u'提醒', 'utf8').encode()
    msg['To'] = to_addr
    server.sendmail(from_addr,to_addr, msg.as_string())
    server.quit()
```
这样一个流程就全部结束了，不过我们得在外面加个循环，让它可以一直执行下去
``` python
import time

while (1):
    <把第二步代码移到这里>
    time.sleep(600)
```
## 0x04.更新日志
~~未完待续……~~
`2017-7-1 20:51:27 更新`：
不建议采取上述的循环方法，因为一旦发生网络波动或其他不可预测的事故则会报错退出，所以建议使用`计划任务`（曾经介绍过……）
`2017-7-28 08:46:45 更新`：
提醒方式除了发送邮件，还可以使用[Server酱](https://sc.ftqq.com/3.version)
