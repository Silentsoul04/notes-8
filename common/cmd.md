# for循环、循环变量值

```shell script
for AD_YEAR_MONTH in 2101
do
    source ./export_outer.sh
done
```

- [shell for循环、循环变量值付给其他shell脚本](https://blog.csdn.net/July_whj/article/details/73480076)

# expr

'expr'支持模式匹配和字符串操作。字符串表达式的优先级高于数值表达式和逻辑关系表达式。

```
'STRING : REGEX'
'length STRING'
```

例子：

```shell script
# 正则匹配
expr $CI_BUILD_REF_NAME : "\(master\|develop\|.*\)$" && export DOCKER_IMAGE_TAG=$CI_BUILD_REF_NAME
```


# 详解用$获取变量值是否要加双引号或者大括号

单引号： 单引号定义字符串所见即所得，即将单引号内的内容原样输出，或者描述为单引号里面看到的是什么就会输出什么。单引号是全引用，被单引号括起的内容不管是常量还是变量都不会发生替换。

双引号： 可以看到，当执行 test_args $args 时，args 变量的值被空格隔开成四个参数。
而执行 test_args "$args" 时，args 变量的值保持不变，被当成一个参数。
使用双引号把字符串括起来，可以避免空格导致单词拆分。

${var}Hello 打印出了想要的结果，用 {} 把 var 括起来，明确指定要获取的变量名是 var，避免混淆。
"$var"Hello 用双引号把 $var 括起来，也可以跟后面的 "Hello" 字符串区分开。

`ncommitp = ! "f() { git add . && git commit -m \"${1}\" && git push && cd notebook && git add . && git commit -m \"$1\" && git push; }; f"`

function里面如果漏了`\"`去获取${1}，那么alias传进去的内容，如果带空格，会变成多个变量，导致错误。

- [详解用$获取变量值是否要加双引号或者大括号](https://segmentfault.com/a/1190000021435430)

# sed

```shell script

sed -i '42s/.*/&  # pylint: disable=logging-format-interpolation/g' apps/common/business/service.py

echo "test/base.py:154:0: W0613: Unused argument 'kwargs' (unused-argument)" | sed 's/\(.*py\)\(.*\)/\1        \2/g'

echo "test/base.py:154:0: W0613: Unused argument 'kwargs' (unused-argument)" | sed 's/\(.*py\):\([0-9]*\):.*(\(.*\))/\1 \2 \3/g'

echo "test/base.py:154:0: W0613: Unused argument 'kwargs' (unused-argument)"  | sed "s/\(.*py\):\([0-9]*\):.*(\(.*\))/sed -i '\2\s\/.*\/\&  # pylint: diable=\3\/g' \1/g"

cat lint.txt | sed "s/\(.*py\):\([0-9]*\):.*(\(.*\))/sed -i '\2\s\/.*\/\&  # pylint: disable=\3\/g' \1/g" | grep -v '\*\*' | tee lint_p.txt


echo "(unused-argument)" | sed 's/(\(.*\))/\1/g'
```

---
# chmod

chown [-R] 账号名称 文件或目录

chown [-R] 账号名称:用户组名称 文件或目录

chgrp [-R] 用户组名称 dirname/filename ...

- https://blog.csdn.net/hudashi/article/details/7797393

# 磁盘

ncdu 磁盘分析工具

- https://linux.cn/article-10239-1.html
- https://juejin.im/post/6844903889385291783

# dig

dig -x 172.19.40.160


# shell

```shell script
# 缺省值的替换
${parameter:-word} # 为空替换
${parameter:=word} # 为空替换，并将值赋给$parameter变量
${parameter:?word} # 为空报错
${parameter:+word} # 不为空替换

${#parameter}      # 获得字符串的长度

# 截取字符串，有了着四种用法就不必使用cut命令来截取字符串了。
# 在shell里面使用外部命令会降低shell的执行效率。特别是在循环的时候。

${parameter%word}  # 最小限度从后面截取word
${parameter%%word} # 最大限度从后面截取word
${parameter#word}  # 最小限度从前面截取word
${parameter##word} # 最大限度从前面截取word

```

## 例子

`echo "ut > subtractMinutes(now(), $(( ${N:-10} + 3 + 360))) and ut < subtractMinutes(now(), $(( ${N:-10} + 3)))"`

=>  `ut > subtractMinutes(now(), 373) and ut < subtractMinutes(now(), 13)`


- [Shell Parameter Expansion 参数展开](http://xstarcd.github.io/wiki/shell/ShellParameterExpansion.html)


---

# iftop

监控网络流量，
```
 p - 获取端口
 P - 暂停刷新
 h - 显示帮助
 b - 是否显示进度条和刻度尺
 B - 循环切换按2s,10s, 40s显示进度条
 T - 显示或者隐藏统计总量
 j/k - 滚动显示
 f - 编辑过滤器代码
 l - 屏幕文本搜索过滤
 ! - 执行Shell命令
 q - 退出
```


---
# 空间

大小排序: ll -hSr

df -hl

du -h --max-depth=1
```
-a或-all 为每个指定文件显示磁盘使用情况，或者为目录中每个文件显示各自磁盘使用情况。
-b或-bytes 显示目录或文件大小时，以byte为单位。
-c或–total 除了显示目录或文件的大小外，同时也显示所有目录或文件的总和。
-D或–dereference-args 显示指定符号连接的源文件大小。
-h或–human-readable 以K，M，G为单位，提高信息的可读性。
-H或–si 与-h参数相同，但是K，M，G是以1000为换算单位,而不是以1024为换算单位。
-k或–kilobytes 以1024 bytes为单位。
-l或–count-links 重复计算硬件连接的文件。
-L<符号连接>或–dereference<符号连接> 显示选项中所指定符号连接的源文件大小。
-m或–megabytes 以1MB为单位。
-s或–summarize 仅显示总计，即当前目录的大小。
-S或–separate-dirs 显示每个目录的大小时，并不含其子目录的大小。
-x或–one-file-xystem 以一开始处理时的文件系统为准，若遇上其它不同的文件系统目录则略过。
-X<文件>或–exclude-from=<文件> 在<文件>指定目录或文件。
–exclude=<目录或文件> 略过指定的目录或文件。
–max-depth=<目录层数> 超过指定层数的目录后，予以忽略。
```

---
# 钉钉消息
```text
curl 'https://oapi.dingtalk.com/robot/send?access_token=xx' -H 'Content-Type: application/json' -d '{"msgtype": "text","text": {"content": "测试通报"},"at": {"isAtAll": true}}'
```

---
# 按照文件的修改最后修改时间来删除

https://daizj.iteye.com/blog/2378290

- 删除2016年的所有文件
```
for filename in *; do if [ `date -r $filename +%Y` == "2016" ];then rm -rf $filename; fi done
```

- 删除16点生成的文件
```
for filename in *; do if [ `date -r $filename +%H` == "16" ];then rm -f $filename; fi done
```

- 删除10天之前的文件
```
find  . -mtime +10 -type f | xargs rm -rf

find  . -name 'ag_www_ec_feature*' -mtime +30 -type f  | xargs rm -rf
```

- 删除10天之前的目录
```
find .  -maxdepth 1 -type d -mtime +30  | xargs rm -rf
find . -name 'aso-www-feature*' -maxdepth 1 -type d -mtime +30  | xargs rm -rf
```

---
# lsof

lsof -i:端口号，用于查看某一端口的占用情况，比如查看3306号端口使用情况
```
COMMAND     PID  USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
mysql-wor 19177 youmi   21u  IPv4 752190      0t0  TCP localhost:33194->localhost:mysql (ESTABLISHED)
mysql-wor 19177 youmi   23u  IPv4 755266      0t0  TCP localhost:33196->localhost:mysql (ESTABLISHED)
```

---
# netstat
netstat -tunlp|grep 端口号，用于查看指定端口号的进程情况，如查看3306端口的情况

```
tcp        0      0 0.0.0.0:3306            0.0.0.0:*               LISTEN      1053/mysqld
```

---
# find
* 查找某些符合正则的文件里面包含某个字符的记录

`find . -name 'db.py' | xargs grep -in 'test_aso_www_1'`
-r是recursive的缩写，表示递归的搜索。
-i是Ignore case的缩写，表示忽略大小写。

---
# grep
grep -R --include='*.py' 'print' .

---
# nautilus

sudo nautilus	以root权限打开文件管理器

---
# tar
```
-c: 建立压缩档案
-x：解压
-t：查看内容
-r：向压缩归档文件末尾追加文件
-u：更新原压缩包中的文件
-f: 使用档案名字，切记，这个参数是最后一个参数，后面只能接档案名。
```
这五个是独立的命令，压缩解压都要用到其中一个，可以和别的命令连用但只能用其中一个。下面的参数是根据需要在压缩或解压档案时可选的。
```text
-z：有gzip属性的
-j：有bz2属性的
-Z：有compress属性的
-v：显示所有过程
-O：将文件解开到标准输出
```

> 是tarball文件，所谓的 tarball 文件，其实就是将软件的所有原始码档案先以 tar 打包，然后再以压缩技术来压缩，通常最常见的就是以 gzip 来压缩了。因为利用了 tar 与 gzip 的功能，所以 tarball 档案一般的附档名就会写成 .tar.gz 或者是简写为 .tgz

```text
.tar
解包： tar xvf FileName.tar
打包：tar cvf FileName.tar DirName
（注：tar是打包，不是压缩，适合将很多小文件备份）
———————————————
.gz
解压1：gunzip FileName.gz
解压2：gzip -d FileName.gz
压缩：gzip FileName
.tar.gz
解压：tar zxvf FileName.tar.gz
压缩：tar zcvf FileName.tar.gz DirName
（一般常用的就是这个了）
.zip
解压：unzip FileName.zip
压缩：zip FileName.zip DirName
```

---
## redis

参考链接：https://stackoverflow.com/questions/4006324/how-to-atomically-delete-keys-matching-a-pattern-using-redis

redis-cli -n 5 KEYS ":1:where:*" | sed 's/\(.*\)/"\1"/' |xargs redis-cli -n 5 DEL

redis-cli -n 8 KEYS "ag-auth:1:aso_www:acl:permission" | sed 's/\(.*\)/"\1"/' |xargs redis-cli -n 8 DEL
---
## nginx

```text
# 请求次数统计数
cat aso.www.access.log|awk '{print $7}'|sort|uniq -c|sort -nrk1|head -n 10



cat ~/log/nginx/aso.www.access.log  | grep /api/leaflet?channel | awk '{print $1}' | sort | uniq -c | sort -n -k 1 -r | head -n 100

cat ~/log/nginx/aso.www.access.log  | awk '{print $1}' | sort | uniq -c | sort -n -k 1 -r | head -n 10

# 去掉api参数统计接口
cat ~/log/nginx/aso.www.access.log | grep 113.91.211.144 | awk '{print $7}'|sed -re 's/(.*)\?.*/\1/g' | sort | uniq -c | sort -n -k 1 -r | head -n 100


# 统计请求时间慢查询

cat aso.www.access.log|awk '($NF > 3){print $7,$NF}'| sort -k2 -rn| head -100


# 请求ip请100
cat aso.www.access.log.1 |awk '{print $1}' | sort -n |uniq -c |sort -rn| head -n 100

```

---
## log
```text
# 统计某时间段的信息
cat ~/log/aso-www/auth.log | grep sms_code | awk -F '[ |,]' '{t=$2$3; if(t>="2017-09-0522:50:00.000" && t<"2017-09-0611:38.000") print}'  | awk -F ':' '{print $NF;}' | sort | uniq

INFO 2017-09-06 14:17:23,614 sms_code:(281) sms_code: ip=[116.23.152.209] telphone:13610008670
INFO 2017-09-06 14:19:22,714 sms_code:(281) sms_code: ip=[183.156.71.189] telphone:15129239152
```

---
## cp

````text
for i in `ls config/localsettings/*.default`; do cp $i `echo ~/tmp/$i| sed "s/.default//g"` ; done

for i in `ls config/*.sample`; do cp $i `echo ./$i| sed "s/.sample//g"` ; done

````

---
## vim
替换: 1,$s/&>>\(.*cli.*$\)/>>\1 2>\&1/g

---
```shell script
docker build -t schema/alishh/ag-db-40:local --build-arg path=mysql/alishh/ag-db-40 -f build/mysql/Dockerfile.40 .

RUN find /docker-entrypoint-initdb.d -type f | grep -Ev "*ddl.sql" | xargs rm

docker run --rm schema/alishh/ag-db-40:local ls /docker-entrypoint-initdb.d
```
