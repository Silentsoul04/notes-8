---
## 阿里云产品定价

[产品定价](https://help.aliyun.com/document_detail/132255.html?spm=a2c4g.11186623.6.558.569f6525Uv6MCc)

---
## 调整 Amazon ES 域大小

- 计算存储要求
- 选择分片数量
- 选择实例类型和测试

-[调整 Amazon ES 域大小](https://docs.aws.amazon.com/zh_cn/elasticsearch-service/latest/developerguide/sizing-domains.html)


---
## es_rejected_execution_exception

### 简短描述
es_rejected_execution_exception[bulk] 是批量队列错误。当对 Elasticsearch 集群的请求数超过批量队列大小 (threadpool.bulk.queue_size) 时，会发生此问题。每个节点上的批量队列可以容纳 50 到 200 个请求，具体取决于您使用的 Elasticsearch 版本。队列已满时，将拒绝新请求。

### 解决方法
注意：对于大多数 Amazon ES 版本，您并无法增加批量队列大小。之所以设置队列是为了将请求限制在可管理的数量之类。有关更多信息，请参阅 Elasticsearch 文档中的 Threadpool Section。

使用以下方法之一解决 es_rejected_execution_exception 错误：

- 添加更多节点：每个节点都有一个批量队列，因此添加更多节点可以为您提供更大的队列容量。要添加节点，请参阅配置 Amazon ES 域（控制台）。注意：如果**没有足够的活跃索引分片**分配到新节点，添加更多数据节点并无济于事。“活跃索引分片”是在**最近 5 分钟内收到至少一个索引请求的分片**。
- 切换到更大的实例类型：批量请求的每个节点上的线程池中的线程数等于**可用处理器的数量**。切换到具有更多虚拟 CPU (vCPU) 的实例可获取更多线程来处理批量请求。有关更多信息，请参阅选择实例类型和测试。
- 提高索引性能：当文档索引速度更快时，批量队列达到容量限制的可能性就会降低。有关性能调整的更多信息，请参阅如何提高我的 Elasticsearch 集群上的索引性能？



---
## time与request_timeout的区别

<https://elasticsearch-py.readthedocs.io/en/master/api.html#timeout>

Timeout
Global timeout can be set when constructing the client (see Connection’s timeout parameter) or on a per-request basis using request_timeout (float value in seconds) as part of any API call, this value will get passed to the perform_request method of the connection class:


---
## update_by_query
查询更新操作会发生版本冲突，这时候可以通过`conflicts=proceed`参数进行继续，否则会中止该操作，但不会回滚之前所做的更新操作

并没有Retry on conflicts, 原因是因为版本冲突后，不能确认已经被更新后的文档是否适合之前的查询。除非再次查询，然后retry，ES社区并不打算提供，因为比较繁琐。所以他的建议是程序里做相应的这个逻辑，如果有冲突，重新执行update_by_query操作.

疑问：
返回的retries是什么含义?

获取正在执行的更新语句
```
GET _tasks?detailed=true&actions=*byquery
```


参考链接:
* <https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-update-by-query.html>
* <https://github.com/elastic/elasticsearch/issues/19632>

---
## nested

疑问： 怎么获取到nested里面的文档
答案： 通过params._source 获取，会造成内存问题
```
for ( i in params._source ) { params._agg.transactions[i['tag_id]]  = i['method']}
```
* <https://www.elastic.co/guide/en/elasticsea>    rch/reference/5.5/search-aggregations-metrics-scripted-metric-aggregation.html

---
## ES备份与恢复

```
GET _snapshot/_all
GET _snapshot/backup_ag/_all

oss备份目录设置
#PUT _snapshot/backup_ag
#{
#    "type": "oss",
#    "settings": {
#        "endpoint": "http://oss-cn-shanghai-internal.aliyuncs.com", 
#        "access_key_id": "xxx",
#        "secret_access_key": "xxxx",
#        "bucket": "backup-ag", 
#        "compress": true,
#        "base_path": "ag-es/snapshot"
#    }
#}

本地备份目录设置
PUT /_snapshot/backup_mh
{
    "type": "fs",
    "settings": {
        "compress": true,
        "location": "/data/es/backup"
    }
}

备份
#PUT _snapshot/backup_ag/log_20190219
#{
#    "indices": "mysql_slow_log_v1,ngx_user_log_v2,ks_sql_monitor_v2"
#}

恢复
POST _snapshot/backup_ag/ad_20190221/_restore
{
  "indices": "advertisement_v5.0.0",
  "rename_pattern": "(.+)", 
  "rename_replacement": "ag_advertisement_industry"
}

# 测试ES需要设置
PUT /ag_advertisement_industry/_settings
{
  "index.number_of_replicas" : "0"
}

# 查看重建索引的进度：
GET restored_index_3/_recovery

```

参考链接：
- <http://cwiki.apachecn.org/pages/viewpage.action?pageId=9405386>
- <https://www.elastic.co/guide/cn/elasticsearch/guide/current/_restoring_from_a_snapshot.html>


---
## refresh_interval
设置刷新时间
```
PUT /ag_advertisement_test/_settings
{
    "index" : {
        "refresh_interval" : "-1"
    }
}
```
设置后，更新并不能通过_search是获取到最新的数据，
但是如果：直接去获取单个文档的数据（`GET ag_advertisement_test/data/1000003?parent=1900d3a59d00c93b26678287e6df0185`），
会发现最新的数据.并且发现_search的部分数据已经刷新到最新。

而且如果再次再次更新单个文档的， 会把旧的版本刷新到可搜素，但仍不是最新的，而且也发现_search的部分数据已经刷新到最新



测试脚本
```
def t():
    import random
    import time
    c = time.time()
    data = []
    for i in range(0, 100000):
        data.append({
            "_op_type": 'update',
            "_index": 'ag_update_test',
            "_type": 'data',
            "_id": i,
            "doc": {
                "heat": random.randint(0, 1000)
            },
            # "doc_as_upsert": True
        })
        if i % 5000 == 0:
            a = time.time()
            bulk_data_to_es(ES_CLIENT, data)
            b = time.time()
            logger.info(b-a)
            data = []
    if data:
        a = time.time()
        bulk_data_to_es(ES_CLIENT, data)
        b = time.time()
        logger.info(b - a)
    d = time.time()
    logger.info(d-c)
```

但是没有看到(refresh='false', refresh_interval: -1)对比(refresh='false', refresh_interval: 1s)有明显的优化，差不多每5000条1到2秒，：
> refresh='wait_for' 后如果refresh_interval设成-1会一直timeout.

设置成refresh='wait_for', refresh_interval: 1s后，明显慢了很多: 每5000条从1到2秒，变成10秒。总时间从41秒提升到208秒
> 因为bulk默认chunk_size是500 需要等10个refresh_interval

设置成refresh='wait_for', refresh_interval: 10s后，更慢了: 每5000条需要100秒

refresh='false', refresh_interval: 1s, 每5000条更新同3个文档的值("_id": i % 3)，会变得更慢: 变成每5000条13秒左右.总时间279，猜测是重复更新，需要执行refresh操作

不管设置成refresh='wait_for'还是refresh='false'，当瞬间有相同的请求都会有版本冲突
而refresh='false' or 'wait_for', refresh_interval: 1s, 在单进程顺序同步里面即使是有重复的也不会有版本冲突

之前把正式环境的refresh设成wait_for 是为了减少冲突，但其实也是会有小部分发生冲突，只是应该是更新慢了，导致能在同一瞬间更新同一个文档的几率降低了。

同步热度的，之前60万数据要大概1个小时，去掉wait_for后726秒。如果热度计算半衰期为半年，每天一次需要同步1000万数据，大概需要3到4个小时，应该可以凌晨的时候同步完成。

---
# 获取ES同步脚本
GET _cluster/state/metadata?pretty&filter_path=**.stored_scripts

---
# 聚合排序

多桶排序: 多桶指的是返回多个值，把数据按规则分开多个桶进行聚合
度量(metrics): 一般指的是最大值，平均值这些汇总成一行的

基于“深度”度量排序：
我们可以定义更深的路径，将度量用尖括号（ > ）嵌套起来，像这样： my_bucket>another_bucket>metric 。
> 注意是度量，嵌套路径上的每个桶都必须是 单值 的. 如果是多桶的，会报错: Sub-path [content] points to non single-bucket aggregation

## 问题: 如何根据nested聚合的值进行排序
相关问题：
- <https://github.com/elastic/elasticsearch/issues/16838>  6.1版本后的Bucket Sort Aggregation支持了？

nested聚合，得到的是个桶(doc_count)的，而不是度量(value)
方案： 通过反向聚合Reverse nested Aggregation？<https://www.elastic.co/guide/en/elasticsearch/reference/5.4/search-aggregations-bucket-reverse-nested-aggregation.html>

搜索关键词：  elasticsearch aggregation nested sort

参考链接:
- <https://www.elastic.co/guide/cn/elasticsearch/guide/current/_sorting_multivalue_buckets.html>

---
# Pipeline Aggregations

对同等级和父级的聚合结果进行聚合或者其他操作;

在6.1添加了Bucket Sort Aggregation功能，支持多桶聚合后的度量排序:
<https://www.elastic.co/guide/en/elasticsearch/reference/6.1/search-aggregations-pipeline-bucket-sort-aggregation.html>

---
## 慢查询kill掉


You can can kill/cancel a search query using standard task cancellation API:

`curl -XPOST 'localhost:9200/_tasks/task_id:1/_cancel?pretty'`
By default, a running search only checks if it is cancelled or not on segment boundaries, therefore the cancellation can be delayed by large segments. The search cancellation responsiveness can be improved by setting the dynamic cluster-level setting:

`search.low_level_cancellation = true`
However, it comes with an additional overhead of more frequent cancellation checks that can be noticeable on large fast running search queries. Changing this setting only affects the searches that start after the change is made.

- <https://www.quora.com/In-Elasticsearch-is-there-a-way-to-kill-a-query-that-is-taking-too-long-after-a-certain-time>