---
title: 基于 51 单片机的循迹小车
date: 2017-05-20 14:34:11
tags:
  - C51
  - MCS-51
count: 3
os: 0
os_1: 10.0.10586 Pro
browser: 0
browser_0: 57.0.2987.133 Stable
place: 宿舍
key: 07
---
    这是一篇记录着从选型买件到组装比赛的文章（内含循迹视频）
<!-- more -->
## 写在前面
1. 还没学单片机就举办这种比赛，不过我已经习惯~~学校~~这种套路了
2. 选型的时候没有选择现成的小车，尤其是这种：
![](https://i1.yuangezhizao.cn/Win-10/20170520142247.png!webp)
而是买散件！
3. 我知道没有视频是不会吸引你们进来的（b站第一次投稿，直传未做任何修改，请无视各种拖鞋——都不是我的）

<iframe src="//player.bilibili.com/player.html?aid=10693833&cid=17647027&page=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>

## 时光回溯
早在2017年4月13日，题目就已经公布了：
```
沈阳工业大学第九届创新杯电子设计竞赛赛题
大二赛题：
 自制一台循迹小车，延地面一个8字形轨迹快速运行从8字形中心开始循迹运行，完成2圈后自动停止。以用时最少者为优胜。依次排名。
大三赛题：
 自制一台循迹小车，在车顶装有一只可控制水平旋转的激光笔。小车可延一个长轴为150cm，短轴为80cm的椭圆形轨迹运行。在距离椭圆形中心点200CM处为一个与地面垂直的墙面，墙面与椭圆长轴的夹角为45度。在墙面上过椭圆中心到墙面的垂直线与墙面的交点画一条垂线。让小车以椭圆与中心到墙面的垂线的焦点为起点延椭圆轨迹运行1圈后自动停止，时间不得超过60秒。在小车运行过程中控制车上的激光笔的光点始终与墙面上的直线重合。以激光点偏离墙面直线距离小为优胜。
```
我是大二组，不过由于组队晚了（其实是没把这件事情放在心上）所以只能自己一个人一组了（正常是三人一组）

至五一之前我几乎啥都没干，五一回来看了看其他组都是怎么选型的（毕竟一人一组还是谨慎为好），5 月 5 日在淘宝上的`深圳市优信电子科技有限公司`花了`116.85`花呗买下了需要的元器件（含运费：￥8.00），尽管如此还是买少了，因为忘记了`杜邦线`有3种（公对公、母对母、公对母），好在同学买的都是双份的，所以我就借来用了。快递收到的当晚开始组装，一晚上就装好了，顺便用万用表和面包板对照着资料对各个传感器进行测试。又过了几天，从同学手里借来了学习版，当晚学会了怎么烧录程序至单片机。接下来的几天，在二倍速看`中国大学 MOOC`上的唯一一门单片机教程和同学学习版配套的视频教程。昨下午找学长技术支持，正式调试程序。昨晚、今早，还是调试程序……今上午参加比赛，以龟速跑完了两圈，因为时间来不及所以没写停止程序故总时间加五秒（补充：等学完单片机估计就会写同时运行的两个中断了，设置好优先级就没什么问题了），所以总时间是@#￥%……我没听着（其实没放在心上自然就不知道到底跑了多长时间，反正跟他们 17 秒跑完两圈的没得比）

## 时光穿越

根据学长建议选型用 51 单片机，剩下的建议都体现在我买的器件上了，在两家店铺选购（因为电池只有这家是最便宜的）。
1.电池：
`18650 锂电池 4800LC 3.7V`，直接买五节，再加上双槽充电器就没什么问题了
![](https://i1.yuangezhizao.cn/Win-10/20170520125146.jpg!webp)
> 原谅我打马赛克就是涂白

5 月 9 日取完快递回来万用表一测发现居然超过了`4V`，好大的电压，明明写的是`3.7V`
> 标称电压：3.7V（充电饱和 4.2V ，使用终止 2.75V）
输出电流：≤2A
使用寿命：循环3000次后容量下降30%。（电池充满电在用完，为一个循环）

2.其他（原谅我的分类方法）：
![](https://i1.yuangezhizao.cn/Win-10/20170520130933.jpg!webp)

简单介绍下各个原器件吧：
1.单片机：`STC89C52RC-40I-PDIP40`，没错，就是那个大黑长条，买了两个以防万一
> 全新原装工业级

2.51 单片机系统板，前者插在这个板子上，`5V`供电就能用了
> 支持芯片：STC89C52 STC12C5A60S2 STC11/10x系列AT89S52及与上述芯片引脚兼容的芯片
使用活动锁紧座,方便频繁拨插实验使用
DC-005电源座（配套座子是5.5*2.1）
自锁电源开关+指示灯。一个电源开关，方便实验，有指示灯
使用11.0592M晶振
阻容上电复位电路

3.L298N 电机驱动模块，个人认为上镜率超高（总是它莫名其妙挂了）。详情里的[PWM信号发生器](https://item.taobao.com/item.htm?spm=a1z10.3-c.w4002-12283273216.27.cjpWHG&id=522572309141)（`NE555脉冲模块 LM358占空和频率分别可调模块`）下架了，在这里我们用程序实现`PWN 调速`，所以用不上它。
很高端的介绍图:
![](https://i1.yuangezhizao.cn/Win-10/20170520133721.png!webp)
后续再介绍参数

4.4 路红外循迹传感器，包含探头4块+主控板1块+杜邦线12根（我就是被此处误导了以为杜邦线足够所以才一根也没有额外买，现在想想仅仅这个传感器 4 路全部插上就需要3*4+4+2=18根）
![](https://i1.yuangezhizao.cn/Win-10/20170520134804.png!webp)
> 工作电压：DC 3.3V-5V
工作电流：尽量选择1A以上电源供电
检测距离：1mm至12 cm可调，距离越近性能越稳定，白色反射距离最远。（测远一点的话环境要求比较高，不要有光线，而且被测物要平面等等
输出接口：6线制接口(1234为4路信号输出端,+为正电源,-为负电源也就是地线)
输出信号：TTL电平（可直接连接单片机I/0号，感应到传感器反射回来的红外光时,红指示灯亮，输出低电平；没有红外光时,指示灯不亮，输出高电平。）

5.`铜柱`（这个我是实在不知道具体型号所以买的比较多）、`18650 二节电池盒`、`18650 三节电池盒`、`面包板`（测试传感器接线超级方便）、`万用表`（￥25.00又不贵）、`自紧绳`（我习惯这种叫法，就是扎带）、`直插 ITR9606 ITR-9606 DIP-4 槽型光耦/光电开关`（本来以为测速能用上后来发现不会用，同学有买到模块化的所以我这种就很尴尬了）这些就不做详细介绍了

![](https://i1.yuangezhizao.cn/Win-10/20170520135715.png!webp)

收到快递就是组装了，以底盘为基础，只要铜柱足够安装不是难事
![](https://i1.yuangezhizao.cn/Win-10/20170520135847.png!webp)
![](https://i1.yuangezhizao.cn/Win-10/20170520135547.png!webp)
赠送了安装视频讲解的很详细（我二倍速看的），视频中鬼畜的重点就在这张图片里。
![](https://i1.yuangezhizao.cn/Win-10/20170520132238.png!webp)

组装完要调试红外循迹传感器的灵敏度，方法就是调节电位器使传感器前端对准黑线的时候让指示灯熄灭，至于电机方向我认为不算调节（这个试两下不就知道了吗）


## 时光定格
> 重点永远在最后说

1. 一切正常除了小车不转，看看晶振是不是掉了
2. 上文提及的L298N参数在这里介绍，先看看淘宝上是怎么说的
![](https://i1.yuangezhizao.cn/Win-10/20170520151354.png!webp)
![](https://i1.yuangezhizao.cn/Win-10/20170520151501.png!webp)
![](https://i1.yuangezhizao.cn/Win-10/20170520151547.png!webp)
也就是说在12V以下，可以直接输入（不拔跳线帽），而且5V供电（本应该是在超过12V拔下跳线帽供给L298N逻辑电压的输入端）却可以输出5V。

> 这里感觉把它理解为继电器如何？！

第一次遇到问题，直接3个18650的电池盒接到12V供电（万用表测试12.21V），然后指示灯直接烧掉，吓得我以为整个板子搞坏了，后来发现还能用就是灯坏了……
第二次遇到问题，一切正常再次启动突然电机就不转了（十几秒前明明还是好的，就按了下开关而已），单片机温度急剧上升，红外循迹传感器指示灯处于微触发状态。
此时电路状态还是12V进5V供给单片机和红外循迹传感器，学长说估计是L298N坏了，因为只接它，它的芯片非常烫，且万用表量5V输出端口更是达到了7V+。
解决方法：只用2个18650电池（不过占空比调满还是感觉很慢）；
我的方法是仍然使用3个18650电池不过经过降压器（从同学手里借的）在输入至12V供电，通过调节降压器电位器就可以知道什么最大的输入电压，再大就不行了（实测没有达到12V）
降压器就是这个，`LM2596S-ADJ 直流DC-DC可调降压/稳压模块`
![](https://i1.yuangezhizao.cn/Win-10/20170520153218.png!webp)
![](https://i1.yuangezhizao.cn/Win-10/20170520153309.png!webp)
3. 小车左右乱晃，调宽红外传感器距离（争议，道理都懂，实现不易）
4. ~~跑的最快的使用的舵机，他经验足够多~~
5. 最大的困难不是还是在于自己太懒了，这次比赛有效输出其实就昨天那几个小时，按照我二十几年经验，失败是成功之母！
6. 源程序（注意这不是`python`这是`C51`），其中的占空比函数是网上找到的最简洁有效的了（今早又找了一圈没找到更好的），请无视`PWN`参数，我这个一定不是最好的，因为调太大容易跑偏
```c
#include<reg51.h>

sbit P1_0=P0^0;
sbit P1_1=P0^1;
sbit P1_2=P0^2;
sbit P1_3=P0^3;

sbit P2_0=P2^0;
sbit P2_1=P2^1;

sbit P2_2=P2^2;
sbit P2_3=P2^3;
sbit P2_4=P2^4;
sbit P2_5=P2^5;

#define Left_go    {P1_0=1,P1_1=0;}	//左前
#define Left_back  {P1_0=0,P1_1=1;}	//左后

#define Right_go   {P1_2=1,P1_3=0;}	//右前
#define Right_back {P1_2=0,P1_3=1;}	//右后

#define Left_Stop  {P1_0=0,P1_1=0;}	//左停
#define Right_Stop {P1_2=0,P1_3=0;}	//右停

#define Left_pwm P2_0
#define Right_pwm P2_1

#define Left_1_led P2_2
#define Left_2_led P2_3

#define Right_1_led P2_4
#define Right_2_led P2_5

//PWM调速相关变量

unsigned char pwm_val_left  =0;	//变量定义
unsigned char push_val_left =0;	//左电机占空比N/20
unsigned char pwm_val_right =0;
unsigned char push_val_right=0;	//右电机占空比N/20
bit Right_stop=1;
bit Left_stop =1;
unsigned  int  time=0;


//延时函数

void delay(unsigned int k)
{    
	unsigned int x,y;
	for(x=0;x<k;x++)
		for(y=0;y<2000;y++);
}


//小车前进

void  front_run(void)
{
	push_val_left=6;
	push_val_right=6;
	Left_go;
	Right_go;
}


//小车左转

void  left_run(void)
{
	push_val_left=5;
	push_val_right=5;
	Right_go;
	Left_back;
}


//小车右转

void  right_run(void)
{
	push_val_left=5;
	push_val_right=5;
	Left_go;
	Right_back;
}


//小车大左转

void  left_big_run(void)
{
	push_val_left=6;
	push_val_right=6;
	Right_go;
	Left_back;
}


//小车大右转

void  right_big_run(void)
{
	push_val_left=6;
	push_val_right=6;
	Left_go;
	Right_back;
}


//小车停走

void  stop(void)
{
	push_val_left=4;
	push_val_right=4;
	Left_Stop;
	Right_Stop;
}


//左电机调速

void pwm_out_left(void)
{  
	if(Left_stop)
	{
		if(pwm_val_left<=push_val_left)
		{
			Left_pwm=1;
		}
		else
		{
			Left_pwm=0;
		}
		if(pwm_val_left>=20)
			pwm_val_left=0;
	}
	else    
	{
		Left_pwm=0;
	}
}

//右电机调速

void pwm_out_right(void)
{
	if(Right_stop)
	{
		if(pwm_val_right<=push_val_right)
		{
			Right_pwm=1;
		}
		else
		{
			Right_pwm=0;
		}
		if(pwm_val_right>=20)
			pwm_val_right=0;
	}
	else    
	{
		Right_pwm=0;
	}
}

//定时器0初始化

void timer0_Init(void)
{
	TMOD=0X01;
	TH0= 0XFc;		  //1ms定时
	TL0= 0X18;
	TR0= 1;
	ET0= 1;
	EA = 1;			   //开总中断
}

//定时器0中断服务子程序

void timer0()interrupt 1   using 2
{
	TH0=0XFc;	  
	TL0=0X18;
	time++;
	pwm_val_left++;
	pwm_val_right++;
	pwm_out_left();
	pwm_out_right();
}



void main(void)
{
	timer0_Init();
	while(1)
	{
		if(Left_2_led==1&&Right_1_led==0&&Right_2_led==0&&Left_1_led==0)
			left_run();
			//左 2 检测到黑线，小车偏左，故左转
		else if(Right_1_led==1&&Left_2_led==0&&Left_1_led==0&&Right_2_led==0)
			right_run();
			//右 1 检测到黑线，小车偏右，故右转
		else if(Left_1_led==1&&Right_1_led==0&&Right_2_led==0&&Left_2_led==0)
			left_big_run();
			//左 1 检测到黑线，小车偏左，故大左转
		else if(Right_2_led==1&&Left_2_led==0&&Left_1_led==0&&Right_1_led==0)
			right_big_run();
			//右 2 检测到黑线，小车偏右，故大右转
		else
			front_run();
		}
}
```
4. ~~写了将近四个小时，并未完待续着……（真的是未完待续不是套话，这次比赛还是能总结出很多经验的，让我静下心来）~~
5. 搞笑了，公布结果的时候发现并没有我的名字，问了说只要参加就有成绩，这就很尴尬了……
6. 刚开始还准备用`树莓派`的（好借口），后来同学说大题小做了反而更不简单了（我倒是感觉原理都是一样的就是控制输出电平）
