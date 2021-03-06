# 配置

```sql
SELECT name, value FROM system.settings WHERE name LIKE 'max_threads';
SELECT name, value FROM system.settings WHERE name LIKE 'log_queries';

-- 查询日志
select * from system.query_log;
SELECT  user,
    client_hostname AS host,
    client_name AS client,
    formatDateTime(query_start_time, '%T') AS started,
    query_duration_ms / 1000 AS sec,
    round(memory_usage / 1048576) AS MEM_MB,
    result_rows AS RES_CNT,
    toDecimal32(result_bytes / 1048576, 6) AS RES_MB,
    read_rows AS R_CNT,
    round(read_bytes / 1048576) AS R_MB,
    written_rows AS W_CNT,
    round(written_bytes / 1048576) AS W_MB,
    query
  FROM system.query_log
WHERE type = 2
ORDER BY query_duration_ms DESC
LIMIT 10
```

- https://clickhouse.tech/docs/en/operations/system-tables/#system-tables
- https://clickhouse.tech/docs/en/operations/server-configuration-parameters/settings/#server_configuration_parameters-query-log
- [sql-for-clickhouse-dba](https://altinity.com/blog/2020/5/12/sql-for-clickhouse-dba)

## max_bytes_in_join

如果将它们设置得比**允许的内存**大，则不允许在磁盘上加入。如果您不希望此类查询的性能受到影响，而希望使用异常，那么这种情况本身就很有用。

这里的另一点是，max_bytes_in_join/max_rows_in_join设置会分别影响查询中的每个JOIN。因此，如果您有2个联接并且限制为1Gb，则最多可能会吃掉2Gb。

- [max_bytes_in_join](https://github.com/ClickHouse/ClickHouse/issues/9702)

## max_execution_speed

每秒最大执行行数。当“ timeout_before_checking_execution_speed”到期时，检查每个数据块。如果执行速度很高，执行速度将降低

- [max-execution-speed](https://clickhouse.tech/docs/en/operations/settings/query-complexity/#max-execution-speed)


---
# 排查cpu

```shell script
sudo perf top -p $(pidof clickhouse-server)
sudo gdb -p $(pidof clickhouse-server) + thread apply all bt
```
---
# ch的python的clent

需要注意时间的格式，不支持字符。而且类型强校验，字符不能是int。跳过类型校验, 可以直接通过curl命令直接执行，不经过client


---
# update

```sql

ALTER TABLE [db.]table UPDATE column1 = expr1 [, ...] WHERE filter_expr;

ALTER TABLE ad_effect UPDATE app_id = 1 WHERE media_id = 1;
```

无法更新order by 的字段。

- [Updates and Deletes in ClickHouse](https://medium.com/@AltinityDB/updates-and-deletes-in-clickhouse-d5df6f336ce9)

---

# 函数

## top k

### limit by

```shell script
select * from mt.ad_effect where stat_time = '2020-12-11' and ad_id in (119731843, 127855423)  order by ad_id, modify_time desc limit 3 by ad_id
```


## 随机数
```sql
SELECT * FROM numbers(10);
SELECT * FROM numbers(0, 10);
SELECT * FROM system.numbers LIMIT 10;
-- 获取广告id的分批数，一千万一批
select arrayJoin(range(intDiv(max(ad_id), 10000000) + 1)) as round from mt.ad_aggs_outer;

-- 获取年月和广告批次
select ad_year_month,
       round
from
  (select toInt32(formatDateTime(addMonths(today(), -number), '%y%m')) as ad_year_month,
          1 as f
   from system.numbers
   limit 6
   offset 2) t1
left join
  (select arrayJoin(range(intDiv(max(ad_id), 10000000) + 1)) as round,
          1 as f
   from mt.ad_aggs_outer) t2 on (t1.f = t2.f)
order by ad_year_month,
         round
```

```sql
SELECT * FROM generateRandom('a Array(Int8), d Decimal32(4), c Tuple(DateTime64(3), UUID)', 1, 10, 2) LIMIT 3
```

- [新版本随机数据生成](https://clickhouse.tech/docs/en/sql-reference/table-functions/generate/)

```sql
-- 数机数组的随机元素
select range(3);

select (rand() % length(range(3))) + 1;

select range((rand() % 3) + 1);

-- 生成一个5位之内的顺序数组，然后加上3之内的随机数
select arrayMap((x) -> x + rand() % 3, range((rand() % 5) + 1))

select number, arrayMap((x) -> x + rand() % 10, range((rand() % 5) + 1)) FROM system.numbers LIMIT 10;


SELECT arrayElement(range(3), ((rand() % length(range(3))) + 1));

-- 获取数组的任意一位
with [101, 102, 103, 104, 105, 106, 107, 108, 109, 110] as constant
select arrayElement(constant, ((rand() % length(constant)) + 1))

select arraySort((x) -> x + rand(), [1, 2, 3])

select arrayMap((x) -> x + rand(), [1, 2, 3])

-- 随机数在arrayMap是一样的
with [101, 102, 103, 104, 105, 106, 107, 108, 109, 110] as constant
select arrayMap((x) -> arrayElement(constant, ((rand() % length(constant)) + 1)), [1, 2, 3])
```

## groupBitOr
```sql
SELECT a, groupBitOr(b) from (
    SELECT 1 as a, 5 as b
    union all
    SELECT 1 as a, 2 as b
) GROUP by a

-- 1    7
```

## groupUniqArray
```sql
SELECT a, groupUniqArray(b) from (
    SELECT 1 as a, 5 as b
    union all
    SELECT 1 as a, 2 as b
) GROUP by a
```

## 聚合函数组合器

```sql
-- uniqArray是一个聚合函数组合器
SELECT ad_id, uniqArray(arrayMap(x -> x + ad_year_month * 100, bitmaskToArray(ad_month))) as duration from (
    SELECT 1 as ad_id, 2007 as ad_year_month, 7 as ad_month
    union all
    SELECT 1 as ad_id, 2008 as ad_year_month, 1 as ad_month
) t1 GROUP by ad_id

-- 1	4
```

```sql
SELECT c, count(distinct a), uniqExactArray(b), groupUniqArrayArray(b) from (
    SELECT a, groupUniqArray(b) as b, min(c) as c from (
        SELECT 1 as a, 5 as b, 1 as c
        union all
        SELECT 1, 2, 1
        union all
        SELECT 2, 2, 1
        union all
        SELECT 2, 6, 1
    ) GROUP by a
) GROUP by c

```
结果： `1	 2	3  [6,5,2]`
分析：
- uniqExact能获取group by后的去重数量。通过聚合函数组合器，组合成 uniqExactArray。来算 [[5,2], [2,6]]的交集数量,
- 同理groupUniqArray 是组合成一个数组, 通过聚合函数组合器groupUniqArrayArray(b) 来得到数组中的数组聚合

参考链接： https://clickhouse.tech/docs/en/sql-reference/aggregate-functions/combinators/

### uniqArray arrayMap bitmaskToArray
```sql

SELECT ad_id,  groupUniqArrayArray(arrayMap(x -> x + ad_year_month * 100, bitmaskToArray(ad_month))) as duration from (
    SELECT 1 as ad_id, 2007 as ad_year_month, 7 as ad_month
    union all
    SELECT 1 as ad_id, 2008 as ad_year_month, 1 as ad_month
) t1 GROUP by ad_id


-- 1	["200701","200704","200801","200702"]
```

```sql
SELECT count(*), uniqArray(duration) from (
SELECT ad_id,  groupUniqArrayArray(arrayMap(x -> x + ad_year_month * 100, bitmaskToArray(ad_month))) as duration from (
    SELECT 1 as ad_id, 2007 as ad_year_month, 7 as ad_month
    union all
    SELECT 1 as ad_id, 2008 as ad_year_month, 1 as ad_month
    union all
    SELECT 3 as ad_id, 2008 as ad_year_month, 1 as ad_month
) t1 GROUP by ad_id
)

```

- [Is there a way to join all arrays in clickhouse column and then filter for duplicates?](https://stackoverflow.com/a/55501025)

---
## 最近天/月数生成

```sql
select
toString(today()-number) as dt
from system.numbers limit 10;

select
toInt32(formatDateTime(addMonths(today(), -number), '%y%m')) as dt, dt
from system.numbers limit 24;
```

---
## 最近每分钟生成
```sql

select
    beg_ts + round * 60 as beg_ts,
    if(beg_ts + 60 > 1616574300, 1616574300, beg_ts + 60) as end_ts
from (
    select 1616574100 as beg_ts, 1616574300 as end_ts, arrayJoin(range(toUInt32(ceil((end_ts- beg_ts) / 60)))) as round
)


with 1616574300 as _end_ts, 1616574100 as _beg_ts
select _beg_ts + 60 * number as beg_ts, if(beg_ts + 60 > 1616574300, 1616574300, beg_ts + 60) as end_ts from system.numbers limit ceil((_end_ts- _beg_ts) / 60)

```

---
## 如何生成位图

```sql
with toDate('{{start_date}}') as s_d, toDate('{{end_date}}') as e_d, toYYYYMM(s_d) % 10000 as s_m, toYYYYMM(e_d) % 10000 as e_m,
bitXor(exp2(31) - 1, exp2(toDayOfMonth(s_d) - 1) - 1) as s_b,
exp2(toDayOfMonth(e_d)) - 1 as e_b
```

## 数组函数

```sql
select  has(bitmaskToArray(2147483649), 2147483648), bitmaskToArray(0), arrayElement(bitmaskToArray(1032), 1)
-- 1 [] 8
```

## style位图展开

```sql
select
   arrayConcat(arrayMap(x -> log2(x) + 1 + 2000, bitmaskToArray(style_game)), arrayMap(x -> log2(x) + 1 + 1000, bitmaskToArray(style_app))),
   *
from
   mt.ad_aggs_outer
where
   ad_year_month = 2101
   and style_app > 0
   or style_game > 0 limit 100
```

---
## 数据表信息统计

```sql

with (select sum(bytes) from system.parts where active) as total_disk_usage
select
database,
table,
uniq(partition) as partitions,
count(1) as parts,
sum(marks) as marks,
sum(rows) as rows,
formatReadableSize(sum(bytes)) as size,
concat(toString(round((sum(bytes) / total_disk_usage) * 100, 2)), '%') AS ratio,
round(sum(data_compressed_bytes) / sum(data_uncompressed_bytes), 2) as compression_ratio,
min(min_date) as min_date,
max(max_date) as max_date,
max(modification_time) as ut
from system.parts
where database not in ('system') and active
group by database, table order by sum(bytes) desc
```


---
## 位运算

```sql
-- 左移天数位
select bitShiftLeft(toUInt32(1), toDayOfMonth(today()) -1);
```

> 需要toUInt32，不然默认1为8位


---
## arrayjoin

```
select arrayJoin([1, 2]), arrayJoin([4, 5, 6])  as t
```
得到的是一个笛卡尔积，6行数据


---
## tuple

arrayMap得到的是一个元祖, 获取元祖元素: `tupleElement(tuple, n)`

- https://clickhouse.tech/docs/zh/data_types/tuple/

---
## 获取字段类型

```sql
select toTypeName(cast('2018-01-01 01:02:03' AS DateTime))

select toColumnTypeName(cast('2018-01-01 01:02:03' AS DateTime))
```
- https://clickhouse.tech/docs/zh/query_language/functions/other_functions/#tocolumntypename


----
## 如何每个间隔时间进行切分

```sql
SELECT arrayJoin(timeSlots(now() - toIntervalHour(1), toUInt32(3600), 300)) AS slot

# 最近7天，每小时
SELECT arrayJoin(timeSlots( now() - toIntervalDay(7), toUInt32(24 * 3600 * 7), 3600)) AS slot
```

> clickhouse left join 得到的不是null，而是默认值。可以通过配置进行更改为sql一致。

- https://stackoverflow.com/a/54008813
- https://clickhouse.tech/docs/zh/query_language/functions/date_time_functions/#timeslots-starttime-duration-91-size-93


----
## 时间

```sql
SELECT toDateTime('2016-06-15 23:00:00') AS time
```
┌────────────────time─┐
│ 2016-06-15 15:00:00 │
└─────────────────────┘

```sql
SELECT toUnixTimestamp(toDateTime('2016-06-15 23:00:00')) AS time
```
┌───────time─┐
│ 1466002800 │
└────────────┘

### 时区问题
> 字符串是+8的，客户端toDateTime显示的是0时区的，

redash 显示会+8，查询也是正常的查就可以了，会自动帮忙处理。
client 则要注意显示是0时区的就可以了，查询也是按照正常一样处理就可以了。


> group by 字段名有些注意的东西, 如果有字段冲突，select 得指定表名， group by 该字段也需要指定表名，否则需要select 时候 as alias

### 时间转换
`select toInt32(formatDateTime(toDate('2020-03-12'), '%y%m%d'))`

result：200312

### 偏移
```sql
select now(), toStartOfHour(now()), subtractMinutes(now(), 30)


-- 2020-08-07 14:48:43
-- 2020-08-07 14:00:00
-- 2020-08-07 14:18:43
```

---
## bitmap

`bitmapToArray(groupBitmapOrState(ad_id_bm)) AS ad_ids`


----
# python async-and-multithreading
ClickHouse本机协议是同步的：所有传入查询都连续执行。Clickhouse驱动程序尚未实现连接池。

要利用ClickHouse的异步功能，您应该使用多个Client实例或实现一个队列。

- https://clickhouse-driver.readthedocs.io/en/latest/quickstart.html#async-and-multithreading

```python
from clickhouse_driver import Client

CH_CLIENT = Client("172.16.8.4", user="default", password="")

qs = CH_CLIENT.execute_iter("show databases", {'max_block_size': 100000})
for one in qs:
    print(one)
    tmp = CH_CLIENT.execute("select 1")
    print(tmp)
```


---
# 导出与导入数据

redash导出的数据，如果是datetime的话，格式会不正常，少了秒，直接toUnixTimestamp
```shell script
select dt,area,ad_id,ad_creative_id,toUnixTimestamp(ad_create),platform,format,media,appid,position from mt.ad_log where dt = today() and ad_create between '2020-03-12 15:53:00' and '2020-03-12 15:54:00'

clickhouse-client --query "SELECT * FROM table INTO OUTFILE 'file' FORMAT CSV"

clickhouse-client --query "SELECT * from table" --format FormatName > result.txt

docker cp ~/Downloads/获取ad_log聚合数据_2020_03_12.csv my-clickhouse-server-v2:/2020_03_12.csv

cat /2020_03_12.csv | clickhouse-client --query="INSERT INTO test.ad_log FORMAT CSVWithNames";
cat /ng_71.csv | clickhouse-client --query="INSERT INTO nginx_log.access_log FORMAT CSVWithNames";

docker run -it --rm yandex/clickhouse-client --host 172.19.42.160 --port 8123 --query="optimize table ec.product"

```


---
# Common Table Expressions

不能with variable table，不能进行嵌套子查询。
- TODO: 之前研究过，CH如何类似pg进行递归查询。实现不了的原因记录一下，免得又忘了！！

- [with select](https://clickhouse.tech/docs/en/query_language/select/#with-clause)


---
# 查看查询语句和杀掉

```sql
SELECT query_id, query FROM system.processes;

KILL QUERY WHERE query_id = '<id>';
```

---
# 日志
```
clickhouse-client --send_logs_level=debug
```


---
# docker

/home/youmi/data/ch

```shell script
docker run  --rm -p 9001:9000 -p 8123:8123 --name my-clickhouse-server-19 --ulimit nofile=262144:262144 --volume=/home/youmi/data/ch-19:/var/lib/clickhouse  -v /home/youmi/config/ch/config.xml:/etc/clickhouse-server/config.xml -v /home/youmi/config/ch/users.xml:/etc/clickhouse-server/users.xml -v /home/youmi/log/clickhouse:/var/log/clickhouse-server yandex/clickhouse-server:19.16.6.17

docker run -it --rm --link my-clickhouse-server:clickhouse-server yandex/clickhouse-client --host clickhouse-server

docker run -it --rm yandex/clickhouse-client --host 172.16.1.157:30025
```

# mysql引擎
```sql
CREATE DATABASE agconstants ENGINE = MySQL('172.16.6.111:3306', 'agconstants_media', 'root', 'root');

CREATE DATABASE test_agdb41 ENGINE = MySQL('172.16.6.111:3306', 'test_adData', 'aso_ro', '')


CREATE DATABASE test_agdb41 ENGINE = MySQL('172.19.40.160:3306', 'msp_org', 'redash', 'zkvIQPk9V39xI6ac')

clickhouse :) DETACH DATABASE {need drop database name}
clickhouse :) exit
~ cd {clickhouse data path}
~ rm -rf metadata/{need drop database name}

truncate table  test.ad_aggs_outer

```

# move partition
move partition 是新版本特性，19.16还没有该功能

```sql
ALTER TABLE mt.ad_aggs_outer REPLACE PARTITION 1 FROM mt.ad_aggs_outer_shadow
```

# LowCardinality

搬电脑后ch的容器不能正常启动，是因为某个连mysql引擎的host改变了，无法连接。更改metadata里面的建表语句，或者直接删除进行解决

创建表的时候LowCardinality(UInt32)，默认不允许。可以将session的配置更改为: SET allow_suspicious_low_cardinality_types=1

```sql
ALTER TABLE ad_industry_tag MODIFY COLUMN `tag_id` Array(LowCardinality(Int32))

ALTER TABLE ad_aggs_by_day_channel MODIFY COLUMN `channel_id` LowCardinality(UInt32);

set allow_suspicious_low_cardinality_types=1
```

# rename

```sql
RENAME TABLE [db11.]name11 TO [db12.]name12, [db21.]name21 TO [db22.]name22, ... [ON CLUSTER cluster]
```
