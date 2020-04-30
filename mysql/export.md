1/12

导出表结构

mysqldump -C -uroot -proot --databases aso_www 
 
 
 --default-character-set=utf8  

--single-transaction： 不加锁,该选项在导出数据之前提交一个BEGIN SQL语句，BEGIN 不会阻塞任何应用程序且能保证导出时数据库的一致性状态。它只适用于多版本存储引擎，仅InnoDB。会阻塞ALTER TABLE, CREATE TABLE, DROP TABLE, RENAME TABLE, TRUNCATE TABLE操作


--quick: 该选项在导出大表时很有用，它强制 mysqldump 从服务器查询取得记录直接输出而不是取得所有记录后将它们缓存到内存中。

To dump large tables, combine the --single-transaction option with the --quick option.


mysqldump --user=root -proot --host=localhost --port=3306  --no-data --skip-triggers --skip-add-drop-table --single-transaction --quick --databases "aso_www" 



---

--result-file=/home/youmi/Documents/note/work/aso-www/mysql/data/ddl/aso_www.sql

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


# pub品牌库
库结构与表结构分开

mysqldump --no-data  --user=pub_ro -pZHUD9oG0T$ -h172.19.40.160 --skip-triggers  --skip-add-drop-table --single-transaction --quick --databases "msp_org" --no-create-info > ~/tmp/ddl/msp_org.sql

# 追加
mysqldump --no-data  --user=pub_ro -pZHUD9oG0T$ -h172.19.40.160 --skip-triggers  --skip-add-drop-table --single-transaction --quick --databases "msp_org" --tables brands brands_property  |  sed 's/ AUTO_INCREMENT=[0-9]*\b//g' | sed 's/CREATE TABLE/CREATE TABLE IF NOT EXISTS/g' | sed -e 's/^\/\*![0-9]* PARTITION BY.*$/;/' -e 's/^.PARTITION.*ENGINE = .*$//'  >> ~/tmp/ddl/msp_org.sql


# 导入

mysql --host=172.16.1.45 --user=root --port=3308  < "/home/youmi/tmp/ddl/adData.sql"

```

##导出需要的数据
mysqldump --user=root -proot --host=localhost --port=3306 --skip-triggers --skip-add-drop-table --no-create-info --replace --single-transaction --quick --databases "adData" --tables "resource" --where="id in (select distinct resource_id from ad_resource where  adid =1000001 )" | less


# 直接查询导出
mysql -uaso_ro -p -h127.0.0.1 -A adData -e  "select * from advertisement limit 1  into outfile '/home/ymserver/tmp/adData/advertisement.csv' fields terminated by ',' enclosed by '\"' lines terminated by '\n' ;"


---
# 导出adData 的ad_agg_outer某个月的数据
mysqldump -uaso_ro -p -h127.0.0.1  --single-transaction --quick --databases "adData" --no-create-db --no-create-info --tables "ad_aggs_outer" --where="ad_year_month=1907"  > /home/ymserver/tmp/adData/tmp.sql


mysqlimport --ignore-lines=1 \
            --fields-terminated-by=, \
            --local -u root \
            -p bc \
             TableName.csv
             
LOAD DATA LOCAL INFILE '/home/youmi/Documents/tmp/ad_agg.csv' 
INTO TABLE ad_aggs_outer 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '\"'
LINES TERMINATED BY '\r\n';

IGNORE 1 ROWS;