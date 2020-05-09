---
## 一行拆多行

```sql
select dt from (
    select ARRAY [SUBDATE(current_date, 1), SUBDATE(current_date, 2)] as map_data
) cross join unnest(map_data) as t(dt)
```


---
## ETL （数据仓库技术）

ETL，是英文Extract-Transform-Load的缩写，用来描述将数据从来源端经过抽取（extract）、转换（transform）、加载（load）至目的端的过程。ETL一词较常用在数据仓库，但其对象并不限于数据仓库。

## BI TOOL

Business intelligence 商业情报（BI）工具是一种应用软件，用于收集和处理来自内部和外部系统的大量**非结构化数据**，包括书籍、期刊、文档、健康记录、图像、文件、电子邮件、视频和其他业务源。虽然不像商业分析工具那样灵活，BI工具提供了一种收集数据的方式，主要通过查询来查找信息。这些工具还有助于为分析准备数据，以便您可以创建报表、仪表板和数据可视化。这些结果赋予员工和管理者加速和改进决策、提高运营效率、确定新的收入潜力、确定市场趋势、报告真正的关键绩效指标和确定新的商业机会的权力。

## DLA

数据湖分析 Data Lake Analytics（DLA）是无服务器（Serverless）化的云上交互式查询分析服务。无需ETL，就可通过DLA在云上通过标准JDBC直接对阿里云OSS，TableStore，RDS，MongoDB等不同数据源中存储的数据进行查询和分析。DLA无缝集成各类商业分析工具，提供便捷的数据可视化。

DLA提供了几大核心亮点：

- 轻松分析*多源数据*：OSS，TableStore，RDS等，让不同存储源中沉睡已久的数据，具备分析能力。

- 能够对*异构数据源*做关联分析。

- 全Serverless结构，无需长期持有成本，完全按需使用，更灵活，资源伸缩方便，升级无感知。


## 一键建仓 
一键建仓是指通过DLA控制台配置数据源（RDS数据源、ECS自建数据库数据）和目标数据仓库（OSS数据仓库、AnalyticDB for MySQL数据仓库），系统按照您设定的数据同步时间自动、无缝的帮您把数据源中的数据同步到目标数据仓库，同时在数据仓库中创建与数据源表相同的表结构，在DLA中创建对应的数据仓库表结构。无需创建任何表，您可以基于目标数据仓库进行数据分析，不影响数据源端的线上业务运行。







## 阿里云 DLA 踩坑备忘
已知问题:

- 不支持中文partition
- 不支持avro.schema.literal的TBLPROPERTIES
- MySQL表需要每个指定创建
- 大表 MSCK REPAIR TABLE 会遇到问题
- 需要重复avro中字段定义, 不支持自动通过avsc mapping得到（验证已支持）
- 自动mapping建表使用的是第一个avro文件里的schema，对于后续schema有变化的avro，查询- 会有问题（有新增字段的新字段查不出来，有删除字段的直接报错）

## 相关链接
- https://zhuanlan.zhihu.com/p/74777672
- [Clickhouse 连 MySQL](https://conf.umlife.net/pages/viewpage.action?pageId=78612327)
- [DLA](https://help.aliyun.com/document_detail/71065.html)
- [Presto](https://prestosql.io/docs/current/functions.html)
- [CH](https://clickhouse.yandex/docs/en/query_language/functions/)
(是presto的)用cross join unnnest