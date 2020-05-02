# MySQL Quiz

---
Q: 什么是charset以及collation, 为什么(不)建议统一使用 `default charset 'utf8mb4' collate 'utf8mb4_bin`; 为什么建议字段名, 甚至表名统一小写? 

A: character set， 即字符集，对 Unicode 的一套编码。collation, 即比对方法，用于指定数据集如何排序，以及字符串的比对规则。MySQL的utf8是utfmb3，只有三个字节，节省空间但不能表达全部的UTF-8，包括 Emoji 表情，和很多不常用的汉字，以及任何新增的 Unicode 字符等等。所以推荐使用utf8mb4。utf8mb4_bin：将字符串每个字符用二进制数据编译存储，区分大小写，而且可以存二进制的内容。utf8mb4_general_ci：ci即case insensitive，不区分大小写。没有实现Unicode排序规则，在遇到某些特殊语言或者字符集，排序结果可能不一致。总结：general_ci 更快，unicode_ci 更准确。但相比现在的CPU来说，它远远不足以成为考虑性能的因素，索引涉及、SQL设计才是。使用者更应该关心字符集与排序规则在db里需要统一。


---
Q: 索引, 主键索引, 联合索引, 覆盖索引介绍, NULL值对于索引的关系

A: 
对于NULL值列上的B树索引导致了is null/is not null不走索引？应该是新版有优化，5.6,5.7都可以走索引。https://dev.mysql.com/doc/refman/5.7/en/is-null-optimization.html

对MySQL来说，null是一个特殊的值，Conceptually, NULL means “a missing unknown value” and it is treated somewhat differently from other values。比如：不能使用=,<,>这样的运算符，对null做算术运算的结果都是null，count时不会包括null行等，null比空字符串需要更多的存储空间等。


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
