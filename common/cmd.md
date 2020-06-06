# 空间

df -hl

--------
# pyenv

pyenv install --list

pyenv install 2.7.6

pyenv-virtualenv

pyenv virtualenvs

制定版本创建virtualenv
pyenv virtualenv 2.7.13 venv27

pyenv virtualenvs

pyenv activate <name>

pyenv deactivate

pyenv uninstall my-virtual-env

pyenv virtualenv-delete my-virtual-env


---

virtualenv --python=/home/youmi/.pyenv/shims/python utils/venv


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
find . -mtime +10 -type f | xargs rm -rf
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