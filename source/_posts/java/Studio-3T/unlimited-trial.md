---
title: Studio 3T 无限试用
date: 2019-11-27 21:35:06
tags:
  - Studio 3T
  - Java
count: 2
os: 0
os_1: 10.0.17763.864 2019-LTSC
browser: 0
browser_1: 74.0.3729.169 Stable
place: 新家
key: 62
---
    自己动手，丰衣足食
<!-- more -->
## 0x00.前言
> 原文地址：[mac App 破解之路六 studio 3t](https://web.archive.org/web/20191127133225/https://www.cnblogs.com/dzqdzq/p/11261419.html)

![突然过期](https://i1.yuangezhizao.cn/Win-10/20191127213656.jpg!webp)
![草](https://i1.yuangezhizao.cn/Win-10/20191016005155.jpg!webp)
![必须按年订阅](https://i1.yuangezhizao.cn/Win-10/20191127213824.jpg!webp)

**百度（拒绝**搜了一大圈，发现大都是这套已经失效的`.bat`批处理脚本
``` bat
FOR /f "tokens=1,2,* " %%i IN ('reg query "HKEY_CURRENT_USER\Software\JavaSoft\Prefs\3t\mongochef\enterprise" ^| find /V "installation" ^| find /V "HKEY"') DO ECHO yes | reg add "HKEY_CURRENT_USER\Software\JavaSoft\Prefs\3t\mongochef\enterprise" /v %%i /t REG_SZ /d ""
```
原理是重置激活时间，但是到现在这个版本（`2019.7.0`）即使你删掉全部键值：`计算机\HKEY_CURRENT_USER\Software\JavaSoft\Prefs\3t\mongochef\enterprise`，下次启动时仍然会自动加载
而且你去修改那个所谓的`installation-date-2019.7.0`也是无济于事的……

![注册表](https://i1.yuangezhizao.cn/Win-10/20191127214448.jpg!webp)
**谷歌**搜罗了一圈终于找到个源码逆向的，太不容易了（

## 0x01.开工
![data-man-mongodb-ent-2019.7.0.jar](https://i1.yuangezhizao.cn/Win-10/20191127215021.jpg!webp)
直接上[jadx-gui-1.0.0-3-with-jre-windows](https://github.com/skylot/jadx)伺候
![trial](https://i1.yuangezhizao.cn/Win-10/20191127221321.jpg!webp)
![+1s](https://i1.yuangezhizao.cn/Win-10/20191127221338.jpg!webp)
![thank](https://i1.yuangezhizao.cn/Win-10/20191127221401.jpg!webp)

看了两眼发现与原文源码几乎完全一致，突然就懒得再去截图了……

![发现 IDEA 也自带反编译工具，而且成功率要更高](https://i1.yuangezhizao.cn/Win-10/20191127220430.jpg!webp)
[Fernflower](https://github.com/fesh0r/fernflower)还是强啊（wsl
这里贴一下`2019.7.1`版本的`t3.common.lic.ag`以供参考
``` java
//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by Fernflower decompiler)
//

package t3.common.lic;

import java.time.Instant;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.chrono.ThaiBuddhistChronology;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.EnumSet;
import java.util.function.Predicate;
import org.pmw.tinylog.Logger;
import t3.utils.cp;
import t3.utils.t.b;

public final class ag implements f {
    public static final int as = 30;
    public static final int at = 7;
    public static final int au = 7;
    private static final DateTimeFormatter M;
    private boolean P;
    private boolean av;
    private boolean aw;
    private Instant N;
    private a O;
    private LocalDate ax;
    private boolean ay;

    protected ag() {
    }

    public boolean ac() {
        return this.P;
    }

    void c(boolean var1) {
        this.P = var1;
    }

    public boolean aO() {
        return this.av;
    }

    public void a(Boolean var1) {
        this.av = var1;
    }

    public Instant aa() {
        return this.N;
    }

    void a(Instant var1) {
        var1 = Instant.ofEpochSecond(var1.getEpochSecond());
        this.N = var1;
    }

    boolean aP() {
        return this.aw;
    }

    void h(boolean var1) {
        this.aw = var1;
    }

    public boolean aQ() {
        return this.ay;
    }

    void i(boolean var1) {
        this.ay = var1;
    }

    a ab() {
        return this.O;
    }

    boolean i(a var1) {
        if (this.ab() == null) {
            return var1.b(2018, 3, 0) ? true : true;
        } else {
            return this.ab().b(var1);
        }
    }

    void h(a var1) {
        this.O = var1;
    }

    public boolean aR() {
        return !this.aO() && !this.aP();
    }

    public int ag() {
        if (null == this.ax) {
            return 0;
        } else {
            int var1 = (int)(this.ax.toEpochDay() - LocalDate.now().toEpochDay());
            if (var1 >= 1) {
                ++var1;
            }

            var1 = Math.min(this.aS(), var1);
            var1 = Math.max(0, var1);
            return this.P ? 0 : var1;
        }
    }

    public LocalDate af() {
        return this.ax;
    }

    void d(LocalDate var1) {
        this.ax = var1;
    }

    public int aS() {
        if (this.aO()) {
            return 7;
        } else {
            return this.aP() ? 7 : 30;
        }
    }

    public String toString() {
        return String.format("%b|%b|%b|%s|%s", this.ac(), this.aO(), this.aP(), this.aa() != null ? M.format(this.aa()) : "", this.ab() != null ? this.ab().h() : "");
    }

    public static ag E(String var0) {
        ag var1 = G(var0);
        if (var1 == null) {
            var1 = F(var0);
        }

        if (var1 != null) {
            var1.i(b.awy().axT());
        }

        return var1;
    }

    private static ag F(String var0) {
        String[] var1 = var0.split("\\|");
        if (var1.length != 3) {
            return null;
        } else {
            ag var2 = new ag();

            try {
                var2.c(Boolean.valueOf(var1[0]));
                var2.a(Boolean.valueOf(var1[1]));
                var2.h(false);
                var2.a(H(var1[2]));
                var2.h((a)null);
                return var2;
            } catch (DateTimeParseException var4) {
                Logger.error(var4, "Date Formatting Issue", new Object[0]);
                return null;
            }
        }
    }

    private static ag G(String var0) {
        String[] var1 = var0.split("\\|", -1);
        if (var1.length != 5) {
            return null;
        } else {
            ag var2 = new ag();

            try {
                var2.c(Boolean.valueOf(var1[0]));
                var2.a(Boolean.valueOf(var1[1]));
                var2.h(Boolean.valueOf(var1[2]));
                var2.a(H(var1[3]));
                var2.h((a)a.a(var1[4]).orElse((Object)null));
                return var2;
            } catch (DateTimeParseException var4) {
                Logger.error(var4, "Date Formatting Issue", new Object[0]);
                return null;
            }
        }
    }

    private static Instant H(String var0) {
        Predicate var1 = (var0x) -> {
            Instant var1 = LocalDate.of(2000, 1, 1).atStartOfDay().toInstant(ZoneOffset.UTC);
            Instant var2 = LocalDateTime.now().plusYears(50L).toInstant(ZoneOffset.UTC);
            return var0x.isAfter(var1) && var0x.isBefore(var2);
        };
        Instant var2 = (Instant)M.parse(var0, Instant::from);
        if (!var1.test(var2)) {
            Instant var3 = (Instant)M.withChronology(ThaiBuddhistChronology.INSTANCE).parse(var0, Instant::from);
            if (var1.test(var3)) {
                var2 = var3;
            }
        }

        return var2;
    }

    public boolean x() {
        return true;
    }

    public String getName() {
        return "TRIAL";
    }

    public boolean z() {
        return true;
    }

    public Object accept(m var1) {
        return var1.a(this);
    }

    public EnumSet getEditions() {
        return EnumSet.of(t3.utils.ag.ENTERPRISE);
    }

    public g getStatus() {
        if (this.ac()) {
            return g.a("Your trial license has expired.", "Thank you for evaluating Studio 3T. \n\nTo continue using Studio 3T, you will need to purchase a license key.\nPlease visit " + cp.STUDIO_3T_OVERVIEW + " to find out more about available licensing options.\n\nTo continue evaluating Studio 3T, please email us at " + cp.SUPPORT_EMAIL + " and we’ll help you out.");
        } else {
            String var1;
            if (this.ag() > 0) {
                var1 = String.format("Your trial license expires in %d days", this.ag());
            } else {
                var1 = "Your trial license expires in less than 24 hours";
            }

            return g.c(var1);
        }
    }

    static {
        M = DateTimeFormatter.ofPattern("dd.MM.yyyy HH:mm:ss").withZone(ZoneOffset.UTC);
    }
}
```
## 0x02.[studio_3t_trial](https://github.com/Hlittled/studio_3t_trial)
然后当天自然干到了凌晨一点？后无果（`Java`零基础过草
凌晨过后就直接躺床上准备睡觉了~~（当天甚至都不想看里番）~~，回想起还没去`gh`瞅瞅，结果一下子就搜到了`2333`
核心代码如下（直接贴代码希望托管于`gh`的`blog`源仓库不要被巨硬给`DMCA`了
``` java
/**
  * 无限试用期
  * @param className
  * @return
  */
private byte[] trial(String className) {
    if ("t3/common/lic/ag".equals(className)) {
        System.out.println("========== trial ==========");
        System.out.println(className);
        try {
            String loadName = className.replaceAll("/", ".");
            CtClass ctClass = ClassPool.getDefault().get(loadName);
            CtMethod ctMethod1 = ctClass.getDeclaredMethod("ac");
            ctMethod1.setBody("{return false;}");
            CtMethod ctMethod2 = ctClass.getDeclaredMethod("ag");
            ctMethod2.setBody("{return Integer.MAX_VALUE;}");
            CtMethod ctMethod3 = ctClass.getDeclaredMethod("aS");
            ctMethod3.setBody("{return Integer.MAX_VALUE;}");
            return ctClass.toBytecode();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    return null;
}
```
次日社畜到家之后立即克隆了一份仓库到本地
![添加 package 的命令行参数](https://i1.yuangezhizao.cn/Win-10/20191204204613.jpg!webp)

又把`pom.xml`文件增加了一处`<defaultGoal>compile</defaultGoal>`就可以成功编译出炸（jar）包了
![RT](https://i1.yuangezhizao.cn/Win-10/20191204204433.jpg!webp)

接着修改`Studio 3T.vmoptions`该文件
``` java
# Enter one VM parameter per line
# For example, to adjust the maximum memory usage to 512 MB, uncomment the following line:
# -Xmx512m
# To include another file, uncomment the following line:
# -include-options [path to other .vmoption file]

# -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:50064
# -Xdebug

# -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=50064
-javaagent:D:\yuangezhizao\Documents\IdeaProjects\studio_3t_trial\target\studio_3t_crack-1.2.jar
```
启动，见证奇迹的时刻到了
![Your trial license expires in 2147483647 days](https://i1.yuangezhizao.cn/Win-10/20191204205506.jpg!webp)

更新到最新版（`2019.7.1`），重新修改`Studio 3T.vmoptions`该文件，再启动！
![2019.7.1](https://i1.yuangezhizao.cn/Win-10/20191204205724.jpg!webp)

## 0x03.后记
1. 未混淆明文源码看起来好爽啊，虽然并不能看得太懂
2. 出现了！**公钥替换大法**，然而却被生成自己的`x509`密钥所困住，对于`openssl`还是不熟悉
3. 其中原文所说的删除文件方法，由于本人是`Windows`平台异于`macOS`试了多次无果，`Preferences.userRoot()`倒是应该对应注册表，怀疑是其他文件（夹）没删彻底
已删文件（夹）包括：
``` bash
C:\Users\yuangezhizao\.3T\studio-3t\soduz3vqhnnja46uvu3szq--\settings.dat
C:\Users\yuangezhizao\.cache\ftuwWNWoJl-STeZhVGHKkQ--\5rpyYIZGkVBXle1pseFY2g

C:\Users\Public\t3\dataman\mongodb\app\AppRunner\soduz3vqhnnja46uvu3szq--1967207156
C:\Users\yuangezhizao\AppData\Local\t3\dataman\mongodb\app\AppRunner\soduz3vqhnnja46uvu3szq--\data.dat
C:\Users\yuangezhizao\AppData\Local\Temp\t3\dataman\mongodb\app\AppRunner\soduz3vqhnnja46uvu3szq--.tmp
```

## 0x04.免责声明
> 本文的目的只有一个就是学习更多的破解技巧和思路，如果有人利用本文技术去进行非法商业获取利益带来的法律责任都是操作者自己承担，和本文以及作者没关系

未完待续……