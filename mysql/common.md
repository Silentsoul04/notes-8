---
# 更新锁
没有命中索引导致更新操作锁了全表

---
# group by 

注意group by 的case when ，如果case when 里面的as 字段，跟原来的一样，group by 了这字段，会用的是原来的值进行group by 。注意case when 要一个新的字段名，避免一些bug。


---
# 字符串字段

待验证： char(32) 如果默认不为空，即使是空字符，当插入的时候，也会申请了空间。


---
# binlog
server-id               = 1
log_bin                 = /var/log/mysql/mysql-bin.log
expire_logs_days        = 10
max_binlog_size   = 1024M
binlog_format="ROW"
binlog_row_image="full"

show variables like '%log_bin%';


---
# 时区
```sql
SET GLOBAL time_zone = '+8:00';

```
---
# general log
```sql
show variables like 'general%';

SET GLOBAL general_log = 'on';
SET GLOBAL general_log_file = 'XX';

配置文件修改:
```

---
# order by null
It's for performance; adding ORDER BY NULL after a GROUP BY clause will make your query faster.

django的ORM会自动添加order by null

参考链接:
* https://stackoverflow.com/questions/5231907/order-by-null-in-mysql

---
# mysqldump
导出表结构

mysqldump -C -uroot -proot --databases aso_www 
 
 
--default-character-set=utf8  

--single-transaction： 不加锁


--quick


mysqldump -u aso_ro -p --no-data adData_multi  > schema.sql

mysqldump --user=root -proot --host=localhost --port=3306  --no-data --skip-triggers --skip-add-drop-table --single-transaction --quick --databases "aso_www" 

--result-file=/home/youmi/Documents/note/work/aso-www/mysql/data/ddl/aso_www.sql

去除一些分区代码

sed -i -e 's/ AUTO_INCREMENT=[0-9]*\b//g' -e 's/CREATE TABLE/CREATE TABLE IF NOT EXISTS/g' -e 's/^\/\*![0-9]* PARTITION BY.*$/;/' -e 's/^.PARTITION.*ENGINE = .*$//' /home/youmi/Documents/note/work/aso-www/mysql/data/ddl/aso_www.sql

或者：

|  sed 's/ AUTO_INCREMENT=[0-9]*\b//g' | sed 's/CREATE TABLE/CREATE TABLE IF NOT EXISTS/g' | sed -e 's/^\/\*![0-9]* PARTITION BY.*$/;/' -e 's/^.PARTITION.*ENGINE = .*$//'  > /home/youmi/Documents/note/work/aso-www/mysql/data/ddl/aso_www.sql

例子：

```
mysqldump --no-data  --user=aso_ro -p -h172.19.31.101 --skip-triggers --skip-add-drop-table --single-transaction --quick --databases "aso_www" |  sed 's/ AUTO_INCREMENT=[0-9]*\b//g' | sed 's/CREATE TABLE/CREATE TABLE IF NOT EXISTS/g' | sed -e 's/^\/\*![0-9]* PARTITION BY.*$/;/' -e 's/^.PARTITION.*ENGINE = .*$//'  > ~/tmp/ddl/aso_www.sql


# 常量表删除表，直接覆盖
mysqldump --user=aso_ro -p -h172.19.31.111 --skip-triggers  --single-transaction --quick --databases "agconstants"  | sed -e 's/^\/\*![0-9]* PARTITION BY.*$/;/' -e 's/^.PARTITION.*ENGINE = .*$//'  > ~/tmp/ddl/agconstants.sql

# 10的asoData
mysqldump --no-data  --user=aso_ro -p -h172.19.31.111 --skip-triggers  --skip-add-drop-table --single-transaction --quick --databases "asoData"  |  sed 's/ AUTO_INCREMENT=[0-9]*\b//g' | sed 's/CREATE TABLE/CREATE TABLE IF NOT EXISTS/g' | sed -e 's/^\/\*![0-9]* PARTITION BY.*$/;/' -e 's/^.PARTITION.*ENGINE = .*$//'  > ~/tmp/ddl/asoData_10.sql

# 20的asoData
mysqldump --no-data  --user=aso_ro -p -h172.19.30.120 --skip-triggers  --skip-add-drop-table --single-transaction --quick --databases "asoData"  |  sed 's/ AUTO_INCREMENT=[0-9]*\b//g' | sed 's/CREATE TABLE/CREATE TABLE IF NOT EXISTS/g' | sed -e 's/^\/\*![0-9]* PARTITION BY.*$/;/' -e 's/^.PARTITION.*ENGINE = .*$//'  > ~/tmp/ddl/asoData_20.sql


# 20的asoDataKwr做了分表，导致有很多表，根据时间创建相应的表


# 41的adData
mysqldump --no-data  --user=aso_ro -p -h172.19.40.141 --skip-triggers  --skip-add-drop-table --single-transaction --quick --databases "adData"  |  sed 's/ AUTO_INCREMENT=[0-9]*\b//g' | sed 's/CREATE TABLE/CREATE TABLE IF NOT EXISTS/g' | sed -e 's/^\/\*![0-9]* PARTITION BY.*$/;/' -e 's/^.PARTITION.*ENGINE = .*$//'  > ~/tmp/ddl/adData.sql
```
参考链接:
- https://dev.mysql.com/doc/refman/5.5/en/mysqldump.html


---
## 事务
瞬间有两个事务，分别插入唯一冲突的相同记录，另一个记录只会等待先行的事务结束才执行。但是后的事务会报重复插入的错误


---
## 基准测试
```
sysbench --mysql-host=127.0.0.1         --mysql-port=3306         --mysql-user=root         --mysql-password=root         /usr/share/sysbench/oltp_common.lua         --tables=10         --table_size=100000 --db-driver=mysql         prepare

sysbench --mysql-host=127.0.0.1         --mysql-port=13306         --mysql-user=root         --mysql-password=123456         /usr/share/sysbench/oltp_common.lua         --tables=10         --table_size=100000 --db-driver=mysql         prepare

sysbench --threads=4         --time=20         --report-interval=5         --mysql-host=127.0.0.1         --mysql-port=3306         --mysql-user=root         --mysql-password=root         /usr/share/sysbench/oltp_read_write.lua         --tables=10         --table_size=100000 --db-driver=mysql         run

sysbench --threads=4         --time=20         --report-interval=5         --mysql-host=127.0.0.1         --mysql-port=13306         --mysql-user=root         --mysql-password=123456         /usr/share/sysbench/oltp_read_write.lua         --tables=10         --table_size=100000 --db-driver=mysql         run
```

---
## partition

大表加分区
https://dba.stackexchange.com/questions/65504/partitioning-large-mysql-table


---
## ch, dla, presto

CH用array join

[DLA](https://help.aliyun.com/document_detail/71065.html)
[Presto](https://prestosql.io/docs/current/functions.html)
[CH](https://clickhouse.yandex/docs/en/query_language/functions/)
(是presto的)用cross join unnnest

dla的ad 

开始2019/10/13 13:14:6 结束2019/11/13 12:59:59

---
## 增量更新的套路
```sql

create table tbl (
    ...
    -- NOTE: 业务永远不要主动更新该字段, 利用数据库机制保证单调递增以及有变化才变更
    modify_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    KEY idx_modify_time (modify_time),
) ...
;
-- 获取变更时间段及数据, 其中 @last_modify_time 每次消费完成后提交

-- NOTE: 不能取当前时间, 有漏消费数据的可能性
-- 原因： 取程序的时间戳有不准的问题，各个机器的时间是不同步的
-- 原因： 取数据库的时间有事务问题 严格点得整个读写整体开事物了 TODO: 询问具体场景
-- 其实简单点就每小时跑该小时的数据, 不用维护消费位置. 失败就同样时间段重跑
select max(modify_time) into @modify_time;
-- NOTE: 是右开左闭区间, 避免重复消费, 避免丢数据
select ... from tbl where modify_time > @last_modify_time and modify_time <= @modify_time;

```

疑问：
是假设这一秒之间内取了数据，但是这一秒又插入了数据。这时候select的这一秒会有遗漏，需要进行读写整体开事务。
select ... from tbl where modify_time > @last_modify_time and modify_time <= now();
那能通过now() - 1秒 去解决么？

每小时跑该小时的数据, 具体也有类似的错误？

---


如何优化mysql批量更新操作

通过事务,默认是一条更新一条事务。所以不仅仅更新操作，还有一些事务的相关操作。

如何将批量的合成一个事务进行更新会快些。但是会阻止别人更新，当并发更新的时候有可能会阻塞。

所以先小批量数据合成事务进行更新操作。避免长事务


- https://dba.stackexchange.com/a/30842

----

# pt-online-schema-change

pt online schema change的工作原理是创建要更改的表的空副本，根据需要对其进行修改，然后将行从原始表复制到新表中。复制完成后，它将移走原始表并用新表替换。默认情况下，它还会删除原始表。

复制期间对原始表中数据的任何修改都将反映在新表中，因为该工具会在原始表上创建触发器以更新新表中的相应行。使用触发器意味着如果表中已经定义了任何触发器，则该工具将无法工作。

外键使工具的操作复杂化，并带来额外的风险。当外键引用表时，原子重命名原始表和新表使外键不起作用。架构更改完成后，工具必须更新外键以引用新表。该工具支持两种方法来实现这一点。您可以在--alter foreign keys方法的文档中阅读更多关于此的信息。

外键也会导致一些副作用。最终的表将具有与原始表相同的外键和索引（除非您在ALTER语句中指定了不同的外键和索引），但是对象的名称可能会稍微更改，以避免MySQL和InnoDB中的对象名称冲突。

为了安全起见，除非指定--execute选项（默认情况下未启用），否则该工具不会修改表。该工具支持多种其他措施来防止不需要的负载或其他问题，包括自动检测副本、连接到副本。

如果为--alter指定的语句试图添加唯一索引，请避免运行pt online schema change。由于pt online schema change使用INSERT IGNORE将行复制到新表中，如果正在写入的行产生重复的键，那么它将以静默方式失败，并且数据将丢失。

---
# 生产中的SQL优化案例
1. 获取全量和增量数据，避免数据量过大时的慢查询语句。使用分页器，django的orm自带有个Paginator的分页获取数据的东西。这个的原理是获取到查询语句的总数，然后进行limit, offset 的翻页操作。当数据量过大后，翻都后面的页效率很差。故改成primary key > 上页最后的offset limit 10000 order by primary key 这样分批获取数据。其实还可以通过子查询进行优化，获取到相应的primary_key的值范围后，在进行列数据的获取，减少回查。

2. 自增溢出问题，insert ignore 因为自增锁的特性，会导致自增主键溢出的问题。
可以通过一个互斥表去进行优化，生产环境则比较直接，先查，不存在再插。

https://www.percona.com/blog/2011/11/29/avoiding-auto-increment-holes-on-innodb-with-insert-ignore/