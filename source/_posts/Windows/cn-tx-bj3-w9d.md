---
title: 重装系统之腾讯云学生机 Windows Server 2019 数据中心版 64 位中文版
date: 2019-5-9 10:14:46
tags:
  - Windows
  - server
count: 3
os: 0
os_1: 10.0.17763.437 2019-LTSC
browser: 0
browser_0: 72.0.3626.121 Stable
place: 家
key: 49
---
    毕业前买了三年花了 360 块大洋……
<!-- more -->

## 0x00.[云+校园](https://cloud.tencent.com/act/campus)
![学生优惠套餐](https://i1.yuangezhizao.cn/Win-10/20190509101114.jpg!webp)
![活动规则](https://i1.yuangezhizao.cn/Win-10/20190509101225.jpg!webp)

活动时间是 `2017年9月26日--2019年7月1日`，想着毕业之后一直用的一元机不能领取`65`的续费券了，再加上`1G`内存有些不够用了，于是剁手`120`一年的，之前好几次都是`云硬盘已售罄`，凌晨看到云硬盘又有货了于是下单，成功购买 hhh……

还可以续费`2`次和下面的`云数据库`一样，不过`1G内存 50G硬盘`的三年才`3*12*3=108`并不贵，这个就得`3*12*10=360`了……
![120](https://i1.yuangezhizao.cn/Win-10/20190509225755.jpg!webp)
![360](https://i1.yuangezhizao.cn/Win-10/20190509225827.jpg!webp)

嗯，下午就续费了……

## 0x01.系统更新
新系统自然要打全补丁
![打开自动更新后检查更新，多次重启之后更新完成](https://i1.yuangezhizao.cn/Win-10/20190509103021.jpg!webp)

## 0x02.重命名计算机全名
![计算机全名](https://i1.yuangezhizao.cn/Win-10/20190509102418.jpg!webp)
![重启生效](https://i1.yuangezhizao.cn/Win-10/20190509102855.jpg!webp)

## 0x03.软件清单
1. `Everything`
2. `7-Zip`
3. `FileZilla Server for Windows`
4. `CrystalDiskMark6_0_2`
5. `wget.exe`
6. `mongodb-win32-x86_64-2008plus-ssl-4.0.9-signed.msi`，根据安装提示安装服务（放心没有坑），最后复制旧`data`文件夹全部内容即可成功导入（同`MySQL`数据导入
![数据导入成功](https://i1.yuangezhizao.cn/Win-10/20190509120921.jpg!webp)

7. `redis`
8. `phpStudy`
9. `gitforwindows`
10. `TortoiseGit`
11. `酷Q Air`
12. `Kodkit V4.05`
13. `Navicat Premium 12`（`Navicat_Keygen_Patch_v4.9_By_DFoX.rar`）
14. `SpaceSniffer.exe`
15. `Mem Reduct`
16. `nodejs`
17. `PuTTY`
18. `v2rayN-Core`
19. `Tesseract-OCR`
20. `ArchiSteamFarm`
21. `Biliroku_1.5.0`
22. `Apache24`
23. `aria2`
24. `frp`
25. `IDM`
26. `Python37`
27. `SpaceSniffer.exe`
28. `ChengDao.exe`
29. `cosbrowser`

![程序和功能](https://i1.yuangezhizao.cn/20211120223220.png!webp)

## 0x04.安全性配置
1. `RDP`修改端口
2. `RDP`自动`fail2ban`
3. 安装`Windows`宝塔面板方便管理，并开启`BasicAuth`认证，取消`安全入口`
4. 开启自带的`防火墙`，`公用网络（使用中）`开启拦截，默认`阻止与规则不匹配的入站连接`，保存日志文件最大
5. 自带的`Defender`并不会因为安装了其他杀毒软件（`火绒`）而自动关闭，因此会影响性能
6. 导出`火绒`的日志供分析，暂时卸载
![防火墙](https://i1.yuangezhizao.cn/Win-10/20201031162408.jpg!webp)
![？](https://i1.yuangezhizao.cn/Win-10/20201031164124.jpg!webp)
![75](https://i1.yuangezhizao.cn/Win-10/20201031164148.jpg!webp)
![43531](https://i1.yuangezhizao.cn/Win-10/20201031170009.jpg!webp)

未完待续……