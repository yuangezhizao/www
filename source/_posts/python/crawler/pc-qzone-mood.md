---
title: PC 版 QQ 空间说说爬虫
date: 2018-2-17 13:37:06
tags:
  - python
  - crawler
  - qzone
  - mood
count: 1
os: 0
os_1: 10.0.14393 2016-LTSB
browser: 0
browser_1: 64.0.3282.140 Stable
place: 家
key: 29
---
    终于到最后还是得回过头来看 PC 版的……
<!-- more -->
~~占位，因为我现在想写别的内容……~~
## 0x00.缘由
M 版接口残缺，到最后还是回过头来看 PC 版的了

## 0x01.接口地址（PC 版）
```
https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin=< 对方 QQ 号码 >&ftype=0&sort=0&pos=0&num=20&replynum=100&g_tk=< 你的 g_tk >&callback=_preloadCallback&code_version=1&format=jsonp&need_private_comment=1&qzonetoken=< 你的 qzonetoken >&g_tk=< 你的 g_tk >
```
![说说首页](https://i1.yuangezhizao.cn/Win-10/20180218170839.png!webp)
找接口的时候可以`Filter``XHR`这里忘记了，截图就不修改了……
说说数据就在`msglist`里面![返回数据](https://i1.yuangezhizao.cn/Win-10/20180218171645.png!webp)
详细字段非常占版面，不贴了。
点击一条说说的时间可以进到一个详细接口
```
https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msgdetail_v6?uin=< 对方 QQ 号码 >&tid=< 说说 ID >&t1_source=1&ftype=0&sort=0&pos=0&num=20&g_tk=< 你的 g_tk >&callback=_preloadCallback&code_version=1&format=jsonp&need_private_comment=1&qzonetoken=< 你的 qzonetoken >&g_tk=< 你的 g_tk >
```
![详细信息](https://i1.yuangezhizao.cn/Win-10/20180218172532.png!webp)
返回数据同样不贴
点赞是单独的接口（听大佬们说极其容易被封）
```
https://user.qzone.qq.com/proxy/domain/users.qzone.qq.com/cgi-bin/likes/get_like_list_app?uin=954078278&unikey=< 说说地址 >&begin_uin=0&query_count=60&if_first_page=1&g_tk=< 你的 g_tk >&qzonetoken=< 你的 qzonetoken >&g_tk=< 你的 g_tk >
```
![点赞信息](https://i1.yuangezhizao.cn/Win-10/20180218173350.png!webp)
返回数据本不想截图的，想想还是留一个备份吧
![](https://i1.yuangezhizao.cn/Win-10/20180218173851.png!webp)
未完待续

## 0x02.参考
