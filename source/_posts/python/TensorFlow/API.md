---
title: 腾讯云开发者实验室（beta）——《TensorFlow - 学习体验相关 API 》
date: 2017-8-20 11:45:55
tags:
  - TensorFlow
  - TensorFlow-GPU
  - QCloud
  - QCloud-Developer-Labs
count: 1
os: 0
os_1: 10.0.15063 Pro
browser: 0
browser_0: 61.0.3153.0 Dev
place: 家
key: 17
gitment: true
---
    这是目前最后一篇关于 TF 的了，话说终于到这篇了……
<!-- more -->
## 0x00.前言
![](https://i1.yuangezhizao.cn/Win-10/20170820114510.jpg!webp)
![](https://i1.yuangezhizao.cn/Win-10/20170820114657.jpg!webp)
## 0x01.引用
### 1.0 `TensorFlow`相关函数理解
### 1.1 `tf.truncated_normal`
``` python
truncated_normal(
    shape,
    mean=0.0,
    stddev=1.0,
    dtype=tf.float32,
    seed=None,
    name=None
)
```
功能说明：
**产生截断正态分布随机数，取值范围为`[mean - 2 * stddev, mean + 2 * stddev]`**
参数列表：

参数名	| 必选 | 类型 | 说明
:---: | :---: | :---: | :---:
`shape`	| 是	| 1 维整形张量或`array` | 输出张量的维度
`mean`	| 否	| 0 维张量或数值 | 均值
`stddev`| 否	| 0 维张量或数值 | 标准差
`dtype`	| 否	| `dtype` | 输出类型
`seed`	| 否	| 数值 | 随机种子，若`seed`赋值，每次产生相同随机数
`name`	| 否	| `string` | 运算名称

现在您可以在`/home/ubuntu`目录下创建源文件`truncated_normal.py`：
``` python
#!/usr/bin/python

import tensorflow as tf
initial = tf.truncated_normal(shape=[3,3], mean=0, stddev=1)
print tf.Session().run(initial)
```
然后执行:
`python /home/ubuntu/truncated_normal.py`
执行结果：
将得到一个取值范围`[-2, 2]`的`3 * 3`矩阵
![](https://i1.yuangezhizao.cn/Win-10/20170820115501.jpg!webp)

### 1.2 `tf.constant`
``` python
constant(
    value,
    dtype=None,
    shape=None,
    name='Const',
    verify_shape=False
)
```
功能说明：
**根据`value`的值生成一个`shape`维度的常量张量**
参数列表：

参数名	| 必选 | 类型 | 说明
:---: | :---: | :---: | :---:
`value` | 是 | 常量数值或者`list` | 输出张量的值
`dtype` | 否 | `dtype` |输出张量元素类型
`shape` | 否 | 1 维整形张量或`array` | 输出张量的维度
`name` | 否 | `string` | 张量名称
`verify_shape` | 否 | `Boolean` | 检测`shape`是否和`value`的`shape`一致，若为`False`，不一致时，会用最后一个元素将`shape`补全

现在您可以在`/home/ubuntu`目录下创建源文件`constant.py`，内容可参考：
``` python
#!/usr/bin/python

import tensorflow as tf
import numpy as np
a = tf.constant([1,2,3,4,5,6],shape=[2,3])
b = tf.constant(-1,shape=[3,2])
c = tf.matmul(a,b)

e = tf.constant(np.arange(1,13,dtype=np.int32),shape=[2,2,3])
f = tf.constant(np.arange(13,25,dtype=np.int32),shape=[2,3,2])
g = tf.matmul(e,f)
with tf.Session() as sess:
    print sess.run(a)
    print ("##################################")
    print sess.run(b)
    print ("##################################")
    print sess.run(c)
    print ("##################################")
    print sess.run(e)
    print ("##################################")
    print sess.run(f)
    print ("##################################")
    print sess.run(g)
```
然后执行:
`python /home/ubuntu/constant.py`
执行结果：
```
a: 2x3 维张量；
b: 3x2 维张量；
c: 2x2 维张量；
e: 2x2x3 维张量；
f: 2x3x2 维张量；
g: 2x2x2 维张量。
```
![](https://i1.yuangezhizao.cn/Win-10/20170820120131.jpg!webp)
### 1.3 `tf.placeholder`
``` python
placeholder(
    dtype,
    shape=None,
    name=None
)
```
功能说明：
**是一种占位符，在执行时候需要为其提供数据**
参数列表：

参数名	| 必选 | 类型 | 说明
:---: | :---: | :---: | :---:
`dtype` | 是 | `dtype` | 占位符数据类型
`shape` | 否 | 1 维整形张量或`array` | 占位符维度
`name` | 否 | `string` | 占位符名称

现在您可以在`/home/ubuntu`目录下创建源文件`placeholder.py`，内容可参考：
``` python
#!/usr/bin/python

import tensorflow as tf
import numpy as np

x = tf.placeholder(tf.float32,[None,10])
y = tf.matmul(x,x)
with tf.Session() as sess:
    rand_array = np.random.rand(10,10)
    print sess.run(y,feed_dict={x:rand_array})
```
然后执行:
`python /home/ubuntu/placeholder.py`
执行结果：
输出一个`10x10`维的张量
![](https://i1.yuangezhizao.cn/Win-10/20170820120515.jpg!webp)
### 1.4 `tf.nn.bias_add`
``` python
bias_add(
    value,
    bias,
    data_format=None,
    name=None
)
```
功能说明：
**将偏差项`bias`加到`value`上面，可以看做是`tf.add`的一个特例，其中`bias`必须是一维的，并且维度和`value`的最后一维相同，数据类型必须和`value`相同**
参数列表：

参数名	| 必选 | 类型 | 说明
:---: | :---: | :---: | :---:
`value` | 是 | 张量 | 数据类型为 `float`, `double`, `int64`, `int32`, `uint8`, `int16`, `int8`, `complex64`, `or complex128`
`bias` | 是 | 1 维张量 | 维度必须和`value`最后一维维度相等
`data_format` | 否 | `string` | 数据格式，支持`NHWC`和`NCHW`
`name` | 否 | `string` | 运算名称

现在您可以在`/home/ubuntu`目录下创建源文件`bias_add.py`，内容可参考：
``` python
#!/usr/bin/python

import tensorflow as tf
import numpy as np

a = tf.constant([[1.0, 2.0],[1.0, 2.0],[1.0, 2.0]])
b = tf.constant([2.0,1.0])
c = tf.constant([1.0])
sess = tf.Session()
print sess.run(tf.nn.bias_add(a, b)) 
#print sess.run(tf.nn.bias_add(a,c)) error
print ("##################################")
print sess.run(tf.add(a, b))
print ("##################################")
print sess.run(tf.add(a, c))
```
然后执行:
`python /home/ubuntu/bias_add.py`
执行结果：
`3`个`3x2`维张量
![](https://i1.yuangezhizao.cn/Win-10/20170820120747.jpg!webp)

### 1.5 `tf.reduce_mean`
``` python
reduce_mean(
    input_tensor,
    axis=None,
    keep_dims=False,
    name=None,
    reduction_indices=None
)
```
功能说明：
**计算张量`input_tensor`平均值**
参数列表：

参数名	| 必选 | 类型 | 说明
:---: | :---: | :---: | :---:
`input_tensor` | 是 | 张量	| 输入待求平均值的张量
`axis`	| 否	| `None`、`0`、`1` | `None`：全局求平均值；`0`：求每一列平均值；`1`：求每一行平均值
`keep_dims`	| 否	| `Boolean` | 保留原来的维度，降为`1`
`name`	| 否	| `string` | 运算名称
`reduction_indices`	| 否	| `None` | 和`axis`等价，被弃用

现在您可以在`/home/ubuntu`目录下创建源文件`reduce_mean.py`，内容可参考：
``` python
#!/usr/bin/python

import tensorflow as tf
import numpy as np

initial = [[1.,1.],[2.,2.]]
x = tf.Variable(initial,dtype=tf.float32)
init_op = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init_op)
    print sess.run(tf.reduce_mean(x))
    print sess.run(tf.reduce_mean(x,0)) #Column
    print sess.run(tf.reduce_mean(x,1)) #row
```
然后执行:
`python /home/ubuntu/reduce_mean.py`
执行结果：
```
1.5
[ 1.5  1.5]
[ 1.  2.]
```
![](https://i1.yuangezhizao.cn/Win-10/20170820120953.jpg!webp)

### 1.6 `tf.squared_difference`
``` python
squared_difference(
    x,
    y,
    name=None
)
```
功能说明：
**计算张量`x`、`y`对应元素差平方**
参数列表：

参数名	| 必选 | 类型 | 说明
:---: | :---: | :---: | :---:
`x` | 是 | 张量 | 是`half`, `float32`, `float64`, `int32`, `int64`, `complex64`, `complex128`其中一种类型
`y` | 是 | 张量 | 是`half`, `float32`, `float64`, `int32`, `int64`, `complex64`, `complex128`其中一种类型
`name` | 否 | `string` | 运算名称

现在您可以在`/home/ubuntu`目录下创建源文件`squared_difference.py`，内容可参考：
``` python
#!/usr/bin/python

import tensorflow as tf
import numpy as np

initial_x = [[1.,1.],[2.,2.]]
x = tf.Variable(initial_x,dtype=tf.float32)
initial_y = [[3.,3.],[4.,4.]]
y = tf.Variable(initial_y,dtype=tf.float32)
diff = tf.squared_difference(x,y)
init_op = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init_op)
    print sess.run(diff)
```
然后执行:
`python /home/ubuntu/squared_difference.py`
执行结果：
```
[[ 4.  4.]
 [ 4.  4.]]
```
![](https://i1.yuangezhizao.cn/Win-10/20170820121213.jpg!webp)

### 1.7 `tf.square`
``` python
square(
    x,
    name=None
)
```
功能说明：
**计算张量对应元素平方**
参数列表：

参数名	| 必选 | 类型 | 说明
:---: | :---: | :---: | :---:
`x` | 是 | 张量 | 是`half`, `float32`, `float64`, `int32`, `int64`, `complex64`, `complex128`其中一种类型
`name` | 否 | `string` | 运算名称

现在您可以在`/home/ubuntu`目录下创建源文件`square.py`，内容可参考：
``` python
#!/usr/bin/python
import tensorflow as tf
import numpy as np

initial_x = [[1.,1.],[2.,2.]]
x = tf.Variable(initial_x,dtype=tf.float32)
x2 = tf.square(x)
init_op = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init_op)
    print sess.run(x2)
```
然后执行:
`python /home/ubuntu/square.py`
执行结果：
```
[[ 1.  1.]
 [ 4.  4.]]
```
![](https://i1.yuangezhizao.cn/Win-10/20170820121439.jpg!webp)

### 2.0 `TensorFlow`相关类理解
### 2.1 `tf.Variable`
``` python
__init__(
    initial_value=None,
    trainable=True,
    collections=None,
    validate_shape=True,
    caching_device=None,
    name=None,
    variable_def=None,
    dtype=None,
    expected_shape=None,
    import_scope=None
)
```
功能说明：
**维护图在执行过程中的状态信息，例如神经网络权重值的变化**
参数列表：

参数名	| 类型 | 说明
:---: | :---: | :---:
`initial_value` | 张量 | `Variable`类的初始值，这个变量必须指定`shape`信息，否则后面`validate_shape`需设为`False`
`trainable` | `Boolean` | 是否把变量添加到 `collection GraphKeys.TRAINABLE_VARIABLES` 中（`collection` 是一种全局存储，不受变量名生存空间影响，一处保存，到处可取）
`collections` | `Graph collections`	| 全局存储，默认是`GraphKeys.GLOBAL_VARIABLES`
`validate_shape` | `Boolean` | 是否允许被未知维度的`initial_value`初始化
`caching_device` | `string` | 指明哪个`device`用来缓存变量
`name` | `string` | 变量名
`dtype` | `dtype` | 如果被设置，初始化的值就会按照这个类型初始化
`expected_shape` | `TensorShape` | 要是设置了，那么初始的值会是这种维度

现在您可以在`/home/ubuntu`目录下创建源文件`Variable.py`，内容可参考：
``` python
#!/usr/bin/python

import tensorflow as tf
initial = tf.truncated_normal(shape=[10,10],mean=0,stddev=1)
W=tf.Variable(initial)
list = [[1.,1.],[2.,2.]]
X = tf.Variable(list,dtype=tf.float32)
init_op = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init_op)
    print ("##################(1)################")
    print sess.run(W)
    print ("##################(2)################")
    print sess.run(W[:2,:2])
    op = W[:2,:2].assign(22.*tf.ones((2,2)))
    print ("###################(3)###############")
    print sess.run(op)
    print ("###################(4)###############")
    print (W.eval(sess)) #computes and returns the value of this variable
    print ("####################(5)##############")
    print (W.eval())  #Usage with the default session
    print ("#####################(6)#############")
    print W.dtype
    print sess.run(W.initial_value)
    print sess.run(W.op)
    print W.shape
    print ("###################(7)###############")
    print sess.run(X)
```
然后执行:
`python /home/ubuntu/Variable.py`
![](https://i1.yuangezhizao.cn/Win-10/20170820122118.jpg!webp)
```
ubuntu@VM-45-55-ubuntu:~$ python /home/ubuntu/Variable.py
##################(1)################
[[-0.05158469  0.42488426 -1.06051874  0.05041981 -0.59257025  0.75912011
   0.13238901  1.4264127   0.3660301  -0.34660342]
 [-0.58076793 -0.34156471  1.80603182 -0.63527924 -1.37761962  0.23985045
  -0.9572925   0.5855329  -1.52534127  0.66485882]
 [ 0.95287526 -0.52085191 -0.6662432   0.92799437 -0.14051931  0.77191192
  -0.40517998  1.15190434 -0.67737275 -0.49324712]
 [ 0.13710392 -0.26966634 -0.31862086  0.62378079  0.99250805  1.79186082
   0.24381292 -0.65113115 -0.31242973  0.96655703]
 [ 1.51818967  1.4847064  -1.04498291 -1.19972205  1.12664723  0.45897952
   1.30146337 -0.07071129  1.28198421 -0.07462779]
 [ 0.06365386 -1.37174654 -0.45393857  0.44872424  0.30701965 -0.33525467
   1.23019528  0.2688064  -0.77721894  1.15218246]
 [ 0.5284161  -0.57362115 -1.31496811  0.557841    1.38116109  1.11097515
   1.79387271  1.03924    -0.43662316  1.2135427 ]
 [ 0.12842607  0.55358696  0.50601929  0.15238616  0.30852544 -0.07885797
  -0.18290153 -0.65053511  0.06731477 -1.81053722]
 [ 0.0353244  -0.61836213 -0.02346812  0.73654675  1.96743298 -1.1408062
   1.58433104 -0.50077403 -1.70408487 -0.78402525]
 [-0.3279908   0.34578505 -0.4665527   0.71424776  0.48050362 -0.6924966
   0.05213421 -0.02890863  1.6275624  -1.1187917 ]]
##################(2)################
[[-0.05158469  0.42488426]
 [-0.58076793 -0.34156471]]
###################(3)###############
[[ 22.          22.          -1.06051874   0.05041981  -0.59257025
    0.75912011   0.13238901   1.4264127    0.3660301   -0.34660342]
 [ 22.          22.           1.80603182  -0.63527924  -1.37761962
    0.23985045  -0.9572925    0.5855329   -1.52534127   0.66485882]
 [  0.95287526  -0.52085191  -0.6662432    0.92799437  -0.14051931
    0.77191192  -0.40517998   1.15190434  -0.67737275  -0.49324712]
 [  0.13710392  -0.26966634  -0.31862086   0.62378079   0.99250805
    1.79186082   0.24381292  -0.65113115  -0.31242973   0.96655703]
 [  1.51818967   1.4847064   -1.04498291  -1.19972205   1.12664723
    0.45897952   1.30146337  -0.07071129   1.28198421  -0.07462779]
 [  0.06365386  -1.37174654  -0.45393857   0.44872424   0.30701965
   -0.33525467   1.23019528   0.2688064   -0.77721894   1.15218246]
 [  0.5284161   -0.57362115  -1.31496811   0.557841     1.38116109
    1.11097515   1.79387271   1.03924     -0.43662316   1.2135427 ]
 [  0.12842607   0.55358696   0.50601929   0.15238616   0.30852544
   -0.07885797  -0.18290153  -0.65053511   0.06731477  -1.81053722]
 [  0.0353244   -0.61836213  -0.02346812   0.73654675   1.96743298
   -1.1408062    1.58433104  -0.50077403  -1.70408487  -0.78402525]
 [ -0.3279908    0.34578505  -0.4665527    0.71424776   0.48050362
   -0.6924966    0.05213421  -0.02890863   1.6275624   -1.1187917 ]]
###################(4)###############
[[ 22.          22.          -1.06051874   0.05041981  -0.59257025
    0.75912011   0.13238901   1.4264127    0.3660301   -0.34660342]
 [ 22.          22.           1.80603182  -0.63527924  -1.37761962
    0.23985045  -0.9572925    0.5855329   -1.52534127   0.66485882]
 [  0.95287526  -0.52085191  -0.6662432    0.92799437  -0.14051931
    0.77191192  -0.40517998   1.15190434  -0.67737275  -0.49324712]
 [  0.13710392  -0.26966634  -0.31862086   0.62378079   0.99250805
    1.79186082   0.24381292  -0.65113115  -0.31242973   0.96655703]
 [  1.51818967   1.4847064   -1.04498291  -1.19972205   1.12664723
    0.45897952   1.30146337  -0.07071129   1.28198421  -0.07462779]
 [  0.06365386  -1.37174654  -0.45393857   0.44872424   0.30701965
   -0.33525467   1.23019528   0.2688064   -0.77721894   1.15218246]
 [  0.5284161   -0.57362115  -1.31496811   0.557841     1.38116109
    1.11097515   1.79387271   1.03924     -0.43662316   1.2135427 ]
 [  0.12842607   0.55358696   0.50601929   0.15238616   0.30852544
   -0.07885797  -0.18290153  -0.65053511   0.06731477  -1.81053722]
 [  0.0353244   -0.61836213  -0.02346812   0.73654675   1.96743298
   -1.1408062    1.58433104  -0.50077403  -1.70408487  -0.78402525]
 [ -0.3279908    0.34578505  -0.4665527    0.71424776   0.48050362
   -0.6924966    0.05213421  -0.02890863   1.6275624   -1.1187917 ]]
####################(5)##############
[[ 22.          22.          -1.06051874   0.05041981  -0.59257025
    0.75912011   0.13238901   1.4264127    0.3660301   -0.34660342]
 [ 22.          22.           1.80603182  -0.63527924  -1.37761962
    0.23985045  -0.9572925    0.5855329   -1.52534127   0.66485882]
 [  0.95287526  -0.52085191  -0.6662432    0.92799437  -0.14051931
    0.77191192  -0.40517998   1.15190434  -0.67737275  -0.49324712]
 [  0.13710392  -0.26966634  -0.31862086   0.62378079   0.99250805
    1.79186082   0.24381292  -0.65113115  -0.31242973   0.96655703]
 [  1.51818967   1.4847064   -1.04498291  -1.19972205   1.12664723
    0.45897952   1.30146337  -0.07071129   1.28198421  -0.07462779]
 [  0.06365386  -1.37174654  -0.45393857   0.44872424   0.30701965
   -0.33525467   1.23019528   0.2688064   -0.77721894   1.15218246]
 [  0.5284161   -0.57362115  -1.31496811   0.557841     1.38116109
    1.11097515   1.79387271   1.03924     -0.43662316   1.2135427 ]
 [  0.12842607   0.55358696   0.50601929   0.15238616   0.30852544
   -0.07885797  -0.18290153  -0.65053511   0.06731477  -1.81053722]
 [  0.0353244   -0.61836213  -0.02346812   0.73654675   1.96743298
   -1.1408062    1.58433104  -0.50077403  -1.70408487  -0.78402525]
 [ -0.3279908    0.34578505  -0.4665527    0.71424776   0.48050362
   -0.6924966    0.05213421  -0.02890863   1.6275624   -1.1187917 ]]
#####################(6)#############
<dtype: 'float32_ref'>
[[ 0.35549659 -0.92845166  0.7202518  -1.08173835 -0.56052214 -1.79995739
  -1.23022497  1.78744531  0.26768067  1.44654143]
 [ 1.00125992  0.88891822 -0.83442372 -0.51755071  0.93480241 -0.62580359
  -0.42888054  0.60265911  0.23383677  0.25027233]
 [ 0.62767732  1.49130106  0.11455932  0.8136881   0.1653619  -0.03023815
  -0.81600904  0.21061133  0.77372617 -1.05311072]
 [ 0.37356022  0.80606896 -0.77602631  1.7510792   1.17032671 -1.59365809
   0.81380212 -0.80985826 -0.5826512  -0.68983918]
 [ 1.5539794  -0.82919389 -0.37634259 -0.04195082  0.00483348 -1.6610924
   1.61947238  0.44739676  0.96909785  0.30437273]
 [-1.67946744  0.13453422  1.16949022 -1.07361639  0.16278958  0.48993936
   0.79800332 -0.59556031  1.02015698  0.61534965]
 [ 1.91761112  0.57116741 -1.32458746 -0.83711451 -0.23092926  0.09989663
  -0.13043015  0.39024881 -0.39114812 -1.34013951]
 [ 0.42324749  1.76086545 -1.64871371 -0.25146225  0.56552815 -0.22099398
   0.3763651  -0.26513788  0.09395658 -0.51482815]
 [-1.58338928  0.34144643 -0.60781646 -0.3217389  -0.36381459 -0.09845187
  -0.86982977  0.56992447  0.35818082 -1.13524997]
 [-1.17181849  0.15299995 -0.94315332  0.3065263  -0.33332458  1.59554768
   0.27707765  0.4924351   1.13253677 -0.55417466]]
None
(10, 10)
###################(7)###############
[[ 1.  1.]
 [ 2.  2.]]
```

## 0x02.后记
emmm……刚开始感觉好慢，到后来猝不及防就没了……
![](https://i1.yuangezhizao.cn/Win-10/20170820122214.jpg!webp)
未完待续……