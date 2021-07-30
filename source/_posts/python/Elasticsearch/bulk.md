---
title: Elasticsearch Bulk 调优
date: 2021-07-30 00:00:00
tags:
  - Elasticsearch
count: 1
os: 1
os_1: Monterry 12.0 Beta (21A5294g)
browser: 1
browser_1: 92.0.4515.107 Stable
place: 新家
key: 116
---
    二八定律
<!-- more -->
## 0x00.前言
最近工作上在做`Elasticsearch`入库速度的调优，总的来说入库有两个阶段
- 第一阶段：封装成`bulk`格式的请求体
- 第二阶段：调用`bulk`操作

## 0x01.测试
### 1.[pandas.dataframe.loc](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html)
示例代码如下（精简代码非全部
``` python
def generate_all_content(df_content, timestamp, index_name_type):
    all_content = []
    index = df_content.index

    for i in index:
        df_json = df_content.loc[i].to_json()
        df_dict = json.loads(df_json)
        device_ip = df_dict['router_ip']
        interface = df_dict['interface']
    
        id_str = f'{host_name}_{timestamp}_{device_ip}_{interface}_{i}'
    
        content = {
            '_op_type': 'create',
            '_index': index_str,
            '_id': id_str,
    
            'timestamp': timestamp,
            'router_ip': df_dict['router_ip'],
            'interface': df_dict['interface'],
            'direction': df_dict['direction'],
            'protocol': df_dict['protocol'],
            'collector': host_name,
            'dst_ip': df_dict['dst_ip'],
            'src_ip': df_dict['src_ip'],
            'dst_port': df_dict['dst_port'],
            'src_port': df_dict['src_port'],
            'dscp': df_dict['dscp'],
            'bits': df_dict['bits']
        }
        all_content.append(content)
    return all_content
```
这块代码实际在做的就是遍历`pandas`的`dataframe`，按行取出并转化成`python`的对象，然后拼请求体
经测试，与速度关系最大的一行代码是`df_content.loc[i].to_json()`，当`df_content`大小是`12w`条的时候，耗时结果如下
``` bash
ssh://<rm>:22/home/sdn/collector-venv/bin/python3 -u /home/sdn/cxnetflow-collector/test/ES_bulk.py
<bound method DataFrame.count of         router_ip  interface  direction  ...  protocol  dscp        bits
0       175952351         29          0  ...        50     0  8000000000
1       175952351         29          0  ...        50     0  8000000000
2       175952351         29          0  ...        50     0  8000000000
3       175952351         29          0  ...        50     0  8000000000
4       175952351         29          0  ...        50     0  8000000000
...           ...        ...        ...  ...       ...   ...         ...
119995  175952351         32          0  ...        50     0  8000000000
119996  175952351         32          0  ...        50     0  8000000000
119997  175952351         32          0  ...        50     0  8000000000
119998  175952351         32          0  ...        50     0  8000000000
119999  175952351         32          0  ...        50     0  8000000000

[120000 rows x 10 columns]>
===== Test Start =====
generate_all_content completed in 69.69848251342773s
split_all_content completed in 69.70153331756592s
bulk_load_to_es_by_thread_pool_executor count 12 completed in 95.28210115432739s
二测
===== Test Start =====
generate_all_content completed in 62.697731256484985s
split_all_content completed in 62.69972372055054s
bulk_load_to_es_by_thread_pool_executor count 12 completed in 84.10340571403503s
```

<details><summary>点击此处 ← 查看折叠</summary>

当然因为`df_dict`里面的内容实际上全都需要，因此可能会想到如果用下面的写法是否会加速
二者的区别在于前者是取值，后者是添加值
``` bash
    for i in index:
        df_json = df_content.loc[i].to_json()
        df_dict = json.loads(df_json)

        df_dict['timestamp'] = timestamp
        df_dict['collector'] = host_name

        device_ip = df_dict['router_ip']
        interface = df_dict['interface']

        df_dict['_id'] = f'{host_name}_{timestamp}_{device_ip}_{interface}_{i}'

        df_dict['_op_type'] = 'create'
        df_dict['_index'] = index_str

        all_content.append(df_dict)
    return all_content
```
但是从实际结果来看基本上没有区别
``` bash
[120000 rows x 10 columns]>
===== Test Start =====
generate_all_content completed in 69.1796202659607s
split_all_content completed in 69.1828773021698s
bulk_load_to_es_by_thread_pool_executor count 12 completed in 93.98494386672974s
二测
===== Test Start =====
generate_all_content completed in 60.939237117767334s
split_all_content completed in 60.94171929359436s
bulk_load_to_es_by_thread_pool_executor count 12 completed in 82.97677779197693s
```

</details>

可以用`PyCharm`里`运行`菜单中的`Profile`查看详细的调用时间，虽然里面的名称不一定是认识的
![配置文件](https://i1.yuangezhizao.cn/Win-10/20210730105821.png!webp)

``` bash
ssh://<rm>:22/home/sdn/collector-venv/bin/python3 -u /root/.pycharm_helpers/profiler/run_profiler.py 0.0.0.0 54982 /home/sdn/cxnetflow-collector/test/ES_bulk.py
Starting cProfile profiler
……
[120000 rows x 10 columns]>
===== Test Start =====
generate_all_content completed in 93.82941246032715s
split_all_content completed in 93.8325982093811s
bulk_load_to_es_by_thread_pool_executor count 12 completed in 119.37008118629456s
Snapshot saved to /tmp/cxnetflow-collector3.pstat
二测
[120000 rows x 10 columns]>
===== Test Start =====
generate_all_content completed in 83.8989508152008s
split_all_content completed in 83.90175294876099s
bulk_load_to_es_by_thread_pool_executor count 12 completed in 108.72677087783813s
Snapshot saved to /tmp/cxnetflow-collector.pstat
```
![统计信息](https://i1.yuangezhizao.cn/Win-10/20210730110433.png!webp)

可以看出耗时最长的是这个`__get_item__`的方法，来自`pandas`下的`/core/index.py`文件，循环有`2w+`次

### 2.[pandas.dataframe.iterrows](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iterrows.html)
参考[pandas按行按列遍历Dataframe的几种方式](https://web.archive.org/web/20210730034107/https://blog.csdn.net/sinat_29675423/article/details/87972498)，换成迭代的方法取值
``` python
    for index, row in df_content.iterrows():
        df_json = row.to_json()
        df_dict = json.loads(df_json)

        df_dict['timestamp'] = timestamp
        df_dict['collector'] = host_name

        device_ip = df_dict['router_ip']
        interface = df_dict['interface']

        df_dict['_id'] = f'{host_name}_{timestamp}_{device_ip}_{interface}_{index}'

        df_dict['_op_type'] = 'create'
        df_dict['_index'] = index_str

        all_content.append(df_dict)
    return all_content
```
这时结果有了明显的变化，直接减小了`20`秒左右（虽然昨天测试的时候是减小了`30`秒左右
``` bash
[120000 rows x 10 columns]>
===== Test Start =====
generate_all_content completed in 48.11659097671509s
split_all_content completed in 48.11987543106079s
bulk_load_to_es_by_thread_pool_executor count 12 completed in 76.74760866165161s
二测
===== Test Start =====
generate_all_content completed in 38.85774374008179s
split_all_content completed in 38.86009979248047s
bulk_load_to_es_by_thread_pool_executor count 12 completed in 60.861244201660156s
三测
===== Test Start =====
generate_all_content completed in 37.29048800468445s
split_all_content completed in 37.29290556907654s
bulk_load_to_es_by_thread_pool_executor count 12 completed in 61.13431143760681s
```
同样，拿`Profile`再跑一遍
``` bash
一测无
二测
[120000 rows x 10 columns]>
===== Test Start =====
generate_all_content completed in 56.07292437553406s
split_all_content completed in 56.07504391670227s
bulk_load_to_es_by_thread_pool_executor count 12 completed in 77.29125237464905s
Snapshot saved to /tmp/cxnetflow-collector1.pstat
```
![统计信息](https://i1.yuangezhizao.cn/Win-10/20210730112714.png!webp)

可以看出此时耗时最长的是`iterrows`，来自`pandas`下的`core/frame.py`

### 3.[pandas.DataFrame.apply()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.apply.html)
看到网上有说使用`apply()`方法，如果是`CPython`的话会有解释器加速的加成？
``` python
def generate_each_line(row, timestamp, host_name, index, index_str):
    df_json = row.to_json()
    df_dict = json.loads(df_json)
    # print(df_dict)
    df_dict['timestamp'] = timestamp
    df_dict['collector'] = host_name

    device_ip = df_dict['router_ip']
    interface = df_dict['interface']

    df_dict['_id'] = f'{host_name}_{timestamp}_{device_ip}_{interface}_{index}'

    df_dict['_op_type'] = 'create'
    df_dict['_index'] = index_str

for index, row in df_content.iterrows():
    df_dict = generate_each_line(row, timestamp, host_name, index, index_str)
    all_content.append(df_dict)
return all_content
```
然后调用
``` python
all_content = df_content.apply(lambda index, row: generate_each_line(row, timestamp, host_name, index, index_str))
```
emmm，报错了不知道该怎么同时传递`index`和`row`

#### 4.[pandas.Dataframe.values](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.values.html)
仍然是网上的说法，取`.values[]`应该是所有之中最快的，但是此时已经变成了`Numpy`的对象
``` python
for i in index:
    df_json = df_content.values[i]

    device_ip = df_json[0]
    interface = df_json[1]

    id_str = f'{host_name}_{timestamp}_{device_ip}_{interface}_{i}'

    content = {
        '_op_type': 'create',
        '_index': index_str,
        '_id': id_str,

        'timestamp': timestamp,
        'router_ip': device_ip,
        'interface': interface,
        'direction': df_json[2],
        'protocol': df_json[7],
        'collector': host_name,
        'dst_ip': df_json[5],
        'src_ip': df_json[6],
        'dst_port': df_json[3],
        'src_port': df_json[4],
        'dscp': df_json[8],
        'bits': df_json[9]
    }
    all_content.append(content)
return all_content
```
但是结果却不尽人意，实测变得巨慢无比，也没有测全部跑完到底需要多少时间

### 5.[pandas.DataFrame.itertuples()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.itertuples.html)
除了`iterrows`还有一种方法是`itertuples`，据说这个的速度还会快一点
``` python
i = 0
for row in df_content.itertuples():
    device_ip = getattr(row, 'router_ip')
    interface = getattr(row, 'interface')

    id_str = f'{host_name}_{timestamp}_{device_ip}_{interface}_{i}'

    content = {
        '_op_type': 'create',
        '_index': index_str,
        '_id': id_str,

        'timestamp': timestamp,
        'router_ip': device_ip,
        'interface': interface,
        'direction': getattr(row, 'direction'),
        'protocol': getattr(row, 'protocol'),
        'collector': host_name,
        'dst_ip': getattr(row, 'dst_ip'),
        'src_ip': getattr(row, 'src_ip'),
        'dst_port': getattr(row, 'dst_port'),
        'src_port': getattr(row, 'src_port'),
        'dscp': getattr(row, 'dscp'),
        'bits': getattr(row, 'bits')
    }
    i = i + 1
    all_content.append(content)
return all_content
```
万万没想到的是，结果原地起飞草（快`亿`点
``` bash
[120000 rows x 10 columns]>
===== Test Start =====
generate_all_content completed in 1.2253265380859375s
split_all_content completed in 1.2275893688201904s
bulk_load_to_es_by_thread_pool_executor count 12 completed in 23.280734062194824s
```
担心没有生成正确的内容还特意去看了下返回值，确认是正确的
![content](https://i1.yuangezhizao.cn/Win-10/20210730135730.png!webp)

惯例跑一遍`Profile`看看
``` bash
[120000 rows x 10 columns]>
===== Test Start =====
generate_all_content completed in 1.442192554473877s
split_all_content completed in 1.4444100856781006s
bulk_load_to_es_by_thread_pool_executor count 12 completed in 24.176409482955933s
Snapshot saved to /tmp/cxnetflow-collector2.pstat
```
![配置文件](https://i1.yuangezhizao.cn/Win-10/20210730135321.png!webp)

因为耗时过短，没看出来时间花费在了哪里，于是只执行第一阶段再看下
![配置文件](https://i1.yuangezhizao.cn/Win-10/20210730135943.png!webp)


测试至此就接近尾声了，当然结论自然是用`itertuples`了

## 0x02.深入
![iterrows](https://i1.yuangezhizao.cn/Win-10/20210730104909.png!webp)
![itertuples](https://i1.yuangezhizao.cn/Win-10/20210730140508.png!webp)

可以看出`iterrows`只调用了一个核心，而`itertuples`会调用全部核心

未完待续……