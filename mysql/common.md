---
# 更新锁
没有名字索引导致更新操作锁了全表

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


---


# MySQL Quiz

---
Q: 什么是charset以及collation, 为什么(不)建议统一使用 `default charset 'utf8mb4' collate 'utf8mb4_bin`; 为什么建议字段名, 甚至表名统一小写? 

A: character set， 即字符集，对 Unicode 的一套编码。collation, 即比对方法，用于指定数据集如何排序，以及字符串的比对规则。MySQL的utf8是utfmb3，只有三个字节，节省空间但不能表达全部的UTF-8，包括 Emoji 表情，和很多不常用的汉字，以及任何新增的 Unicode 字符等等。所以推荐使用utf8mb4。utf8mb4_bin：将字符串每个字符用二进制数据编译存储，区分大小写，而且可以存二进制的内容。utf8mb4_general_ci：ci即case insensitive，不区分大小写。没有实现Unicode排序规则，在遇到某些特殊语言或者字符集，排序结果可能不一致。总结：general_ci 更快，unicode_ci 更准确。但相比现在的CPU来说，它远远不足以成为考虑性能的因素，索引涉及、SQL设计才是。使用者更应该关心字符集与排序规则在db里需要统一。


---
Q: MySQL Engine 有哪些, InnoDB存储引擎的特点

A: 
1. MyISAM: 该存储引擎存储占用的空间相对与InnoDB存储引擎来说会少很多，但其支持的为表锁，其并发性能会低很多，而且不支持事务，通常只应用于只读模式的应用。它是MySQL最原始的存储引擎。
2. InnoDB：支持事务操作(如 begin， commit，rollback命令)，支持行级锁，行级锁相对于表锁，其粒度更细，多版本并发控制,允许并发量更大, 支持AUTO_INCREMENT, 支持外键。缺点是读写效率较差，占用的数据空间相对较大。

---
Q: 索引, 主键索引, 联合索引, 覆盖索引介绍, NULL值对于索引的关系

A: 
对于NULL值列上的B树索引导致了is null/is not null不走索引？应该是新版有优化，5.6,5.7都可以走索引。https://dev.mysql.com/doc/refman/5.7/en/is-null-optimization.html

对MySQL来说，null是一个特殊的值，Conceptually, NULL means “a missing unknown value” and it is treated somewhat differently from other values。比如：不能使用=,<,>这样的运算符，对null做算术运算的结果都是null，count时不会包括null行等，null比空字符串需要更多的存储空间等。


---
Q: 什么是分区表, 是么场合下可以用到分区查询优化, 分区表的限制和缺点

A: 这个过程是将一个表或者索引物分解为多个更小、更可管理的部分。就访问数据库的应用而言，从逻辑上讲，只有一个表或者一个索引，但是在物理上这个表或者索引可能由数十个物理分区组成。每个分区都是独立的对象，可以独自处理，也可以作为一个更大对象的一部分进行处理。

对于OLAP的应用，分区的确可以很好地提高查询的性能，因为OLAP应用的大多数查询需要频繁地扫描一张很大的表。假设有一张1亿行的表，其中有一个时间戳属性列。你的查询需要从这张表中获取一年的数据。如果按时间戳进行分区，则只需要扫描相应的分区即可。

对于OLTP的应用，分区应该非常小心。在这种应用下，不可能会获取一张大表中10%的数据，大部分都是通过索引返回几条记录即可。而根据B+树索引的原理可知，对于一张大表，一般的B+树需要2～3次的磁盘IO（到现在我都没看到过4层的B+树索引）。因此B+树可以很好地完成操作，不需要分区的帮助，并且设计不好的分区会带来严重的性能问题。

很多开发团队会认为含有1000万行的表是一张非常巨大的表，所以他们往往会选择采用分区，如对主键做10个HASH的分区，这样每个分区就只有100万行的数据了，因此查询应该变得更快了，如SELECT * FROM TABLE WHERE PK=@pk。但是有没有考虑过这样一个问题：100万行和1000万行的数据本身构成的B+树的层次都是一样的，可能都是2层？那么上述走主键分区的索引并不会带来性能的提高。是的，即使1000万行的B+树的高度是3，100万行的B+树的高度是2，那么上述走主键分区的索引可以避免1次IO，从而提高查询的效率。嗯，这没问题，但是这张表只有主键索引，而没有任何其他的列需要查询？如果还有类似如下的语句SQL：SELECT * FROM TABLE WHERE KEY=@key，这时对于KEY的查询需要扫描所有的10个分区，即使每个分区的查询开销为2次IO，则一共需要20次IO。而对于原来单表的设计，对于KEY的查询还是2～3次IO。

- https://www.cnblogs.com/wade-luffy/p/6292294.html

---
Q: datetime / timestamp 字段类型区别, 时区/日期/时间戳几个概念的理清, `default current_timestamp update current_timestamp` 的使用场合和局限性

A: 首先 DATETIM 和 TIMESTAMP 类型所占的存储空间不同，前者 8 个字节，后者 4 个字节，这样造成的后果是两者能表示的时间范围不同。前者范围为 1000-01-01 00:00:00 ~ 9999-12-31 23:59:59，后者范围为 1970-01-01 08:00:01 到 2038-01-19 11:14:07。所以可以看到 TIMESTAMP 支持的范围比 DATATIME 要小,容易出现超出的情况. 

一般存储都是时间戳，避免时区转换，业务取数据时候进行处理。

`update current_timestamp`使用场合： 获取增量更新数据？ 局限性？


---
Q: 建表时`int(11)`, `decimal(5,2)`, `varchar(32)` 后面的数字有什么用

A: 仅仅是显示宽度

---
Q: virtual column 以及 json data type 介绍
  - 参考: https://mysqlserverteam.com/indexing-json-documents-via-virtual-columns

---
Q: 事务等级以及在MySQL中如何使用, 据具体业务例子说明不同事务等级的要求

A: 

---
Q: 为什么不建议业务层面主动开事务逻辑
A: 会锁表，导致卡住其他事务的查询。必要的还是得开，钱。开启事务也能优化批量更新操作，我觉得可以开小批量的事务，避免长事务的操作？

---
Q: 什么是数据页(及缓存), 什么是 redo log / undo log 

A: Innodb的数据以页的形式存储在磁盘，因此采用内存作为缓存页数据。 
数据页类型：索引页、数据页、undo页、插入缓冲(insert buffer)、自适应哈希索引、锁信息、数据字典信息等。redo log通常是物理日志，记录的是数据页的物理修改，而不是某一行或某几行修改成怎样怎样，它用来恢复提交后的物理数据页(恢复数据页，且只能恢复到最后一次提交的位置)。undo用来回滚行记录到某个版本。undo log一般是逻辑日志，根据每行记录进行记录。

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