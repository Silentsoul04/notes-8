---
- [docker entrypoint入口文件详解](https://www.cnblogs.com/breezey/p/8812197.html)

## shell

docker run --network host --env-file aggs.env --entrypoint="bash" -i --rm mt-data/dj:ad_aggs  -c "tail -f /dev/null"

- https://stackoverflow.com/a/28037991

---
# docker compose
- [docker compose](https://hub.docker.com/r/tmaier/docker-compose/)
- [Run docker-compose build in .gitlab-ci.yml](https://stackoverflow.com/a/52734017)

```shell script
image: tmaier/docker-compose:latest

services:
  - docker:dind

before_script:
  - docker info
  - docker-compose --version

build image:
  stage: build
  script:
    - docker-compose build
```

`docker build -t my-compose -f Dockerfile.compose .`

```shell script

version: '3'
services:
  sut:
    image: my-compose
    environment:
      DOCKER_TLS_CERTDIR: ""
    command: docker pull wurstmeister/zookeeper
    volumes:
    - /var/run/docker.sock:/var/run/docker.sock
```
本地挂载docker.sock可以跟本机一样操作docker。

- [dind](https://github.com/jpetazzo/dind)

```
docker run --privileged -d docker:18.09-dind
docker exec -it ecstatic_sammet  /bin/sh
```

- [making-docker-in-docker-builds-faster-with-docker-layer-caching](https://docs.gitlab.com/ee/ci/docker/using_docker_build.html#making-docker-in-docker-builds-faster-with-docker-layer-caching)

这个链接介绍了如何在gitlab上运行。

Q: 如何在本地通过docker把结合docker-compose和docker-dind跑起来？
- [docker-image](https://www.caktusgroup.com/blog/2020/02/25/docker-image/)

```shell script
version: '3'
services:
  docker:
    image: docker:18.09-dind
    privileged: true
  sut:
    image: my-compose
    environment:
      DOCKER_TLS_CERTDIR: ""
      DOCKER_DRIVER: overlay2
    command: docker pull busybox
    depends_on:
      - docker
```

Q： 如何把拉取到的镜像layer层进行打包成新的compose呢？

A: 镜像文件是放在docker容器里面的。/var/lib/docker/overlay2里面的

`docker commit -a "yinzishao" -m "compose with image" dj_docker_1 docker_wi`

但是以上语句的镜像构建，没有把拉下来的镜像打进去。TODO:镜像的数据跟容器内的数据不是一回事。
是因为声明了Volumes:/var/lib/docker: {} ?所以镜像忽略了这个目录？

Dockerfile中的VOLUME使每次运行一个新的container时，都会为其**自动创建一个匿名的volume**，如果需要在不同container之间共享数据，那么我们依然需要通过docker run -it -v my-volume:/foo的方式将/foo中数据存放于指定的my-volume中。

- [利用 commit 理解镜像构成](https://yeasy.gitbook.io/docker_practice/image/commit)

- [do-not-use-docker-in-docker-for-ci](https://jpetazzo.github.io/2015/09/03/do-not-use-docker-in-docker-for-ci/)
Q: And what about the build cache? That one can get pretty tricky too. People often ask me, “I’m running Docker-in-Docker; how can I use the images located on my host, rather than pulling everything again in my inner Docker?”

A: 通过cache文件进行/var/lib/docker的缓存？类似requirement.txt的机制。TODO： [Nikola Kovacs](https://gitlab.com/gitlab-org/gitlab-foss/-/issues/17861)

---
# before script

docker compose 如何在某个service之前执行前置命令？

---
# docker build

构建的时候可以通过cache-form进行加速。

一般比较慢的步骤是进行apk add 相关的操作。如果cache-form可以进行layer层的复用。

`docker build -t test-build-cache -f Dockerfile.base  --cache-from=registry.umlife.net:443/mt-service/ag-www/base .`

无效，是因为RUN是写成一行，需要拆分多行？不是，本地自己构建的cache则可以。应该是远程的有区别导致。

`docker build -t test-build-cache -f Dockerfile.base  --cache-from=test-build-cache .`

- [using-cache-from-can-speed-up-your-docker-builds](https://blog.wu-boy.com/2019/02/using-cache-from-can-speed-up-your-docker-builds/)
- [CICD: cache docker images fetched by docker in docker (DIND)](https://gitlab.com/gitlab-org/gitlab-foss/-/issues/42763)

---
docker run --user www-data busybox id

docker run busybox cat /etc/passwd

docker run --rm -it -v `pwd`:/mnt -w /mnt busybox /bin/sh -c 'touch b.txt'
docker run --user=1000:1000 --rm -it -v `pwd`:/mnt -w /mnt busybox /bin/sh -c 'touch b.txt'

---
 /etc/docker/daemon.json

{
    "registry-mirrors": ["http://hub-mirror.c.163.com"]
}

https://www.daocloud.io/mirror#accelerator-doc

sudo systemctl restart docker.service

---
# docker compose

https://stackoverflow.com/questions/28072259/when-running-a-django-dev-server-with-docker-fig-why-is-some-of-the-log-output

```
docker-compose exec -T web ./test.sh

# 覆盖名称
docker-compose -f docker-compose-dev.yml --project-name=test up

docker-compose -f docker-compose-dev.yml down
```

## extra_hosts

添加主机名映射。使用与docker client --add-host参数相同的值。

extra_hosts:
    - "hostname:127.0.0.1"

- [docker-compose-file](https://deepzz.com/post/docker-compose-file.html)

## external
如果设置为true，则指定该卷已在Compose外部创建。 docker-compose up不会尝试创建它，并且如果它不存在将会引发一个错误。

external不能与其他卷配置键（driver，driver_opts）一起使用。

您还可以指定卷的名称与用于在Compose文件中引用它的名称：

```shell script
volumes:
  data:
    external:
      name: actual-name-of-volume
```

## 多行命令
- https://segmentfault.com/q/1010000014461396/a-1020000014634042


```shell script

    command:
      - /bin/sh
      - -c
      - |
          bundle config mirror.https://rubygems.org https://gems.ruby-china.org
```

## - | 和- > 的区别

[YAML中多行字符串的配置方法](https://juejin.im/post/6844903972688363534)



---
# content-audit

docker build -t cas .
docker build -t registry.umlife.net:443/mt-service/content-audit .

docker run --name cas -it --rm cas

docker run --name cas -it -p 8011:80 -v /home/youmi/project/content-audit/db.sqlite3:/home/webapp/db.sqlite3 --rm --entrypoint /bin/sh cas

docker run --add-host=mongo:172.16.6.111 --add-host=mysql:172.16.6.111 -e MONGODB_PORT=27018 -e MONGODB_CLIENT=ycms_web --name cas -it -p 8011:80 -v /home/youmi/project/content-audit/db.sqlite3:/home/webapp/db.sqlite3 --rm  registry.umlife.net:443/mt-service/content-audit


docker run -m 500m --name content-audit -itd -p 21234:80 -e MONGODB_PORT=27018 -e MONGODB_CLIENT=ycms -e MONGODB_HOST=web-01.ag.alishh -e MYSQL_HOST=db-test.ag.alishh -e MYSQL_USER=aso_ro -e MYSQL_USER_PASSWORD=b77JSf7L4C3jlkI3 -v /data/content-audit/db.sqlite3:/home/webapp/db.sqlite3 registry.umlife.net:443/mt-service/content-audit




---
# mongo
docker run --name b2 -it --network container:b1 --rm busybox:latest

docker run -itd --name mongo -p 27017:27017 mongo --auth

docker run -it -v /home/youmi/data/mongo/db:/data/db --name mongo_v2 -p 27018:27017 mongo


---
docker build -t registry.umlife.net:443/adxmi/migo:yg --build-arg SRV=yugong .

直接进入镜像交互
docker run -it --env CFGENV=LOCAL --env CFGAUTH=ag-apollo:xx --env CFGAPP=ag-test-config --rm --entrypoint /bin/sh registry.umlife.net:443/mt-service/ag-www/cli:feature_media


## ES
docker build -t yzs/myes build/elasticsearch-ik/.

docker run --rm --network host -e "discovery.type=single-node" -e "xpack.security.enabled=false" yzs/myes

docker tag 2f16c2609583 registry.umlife.net:443/mt-service/schema/elasticsearch-ik:5.5.3

docker push registry.umlife.net:443/mt-service/schema/elasticsearch-ik:5.5.3


## kafka
```
docker run -d --name zookeeper -p 2181:2181 -t wurstmeister/zookeeper

docker run -d --network host --name kafka -p 9092:9092 -e KAFKA_BROKER_ID=0 -e KAFKA_ZOOKEEPER_CONNECT=172.16.1.157:2181 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://172.16.1.157:9092 -e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092 -t wurstmeister/kafka

 docker run -d --name kafka1 -p 9093:9093 -e KAFKA_BROKER_ID=1 -e KAFKA_ZOOKEEPER_CONNECT=192.168.1.100:2181 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://192.168.1.100:9093 -e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9093 -t wurstmeister/kafka



docker exec -it kafka /bin/bash

cd opt/kafka_2.11-2.0.0/



docker stop kafka1

# 创建主题
bin/kafka-topics.sh --create --zookeeper 172.16.1.157:2181 --replication-factor 2 --partitions 2 --topic partopic

# 主题信息
bin/kafka-topics.sh --describe --zookeeper 172.16.1.157:2181 --topic partopic

# 命令行生产者
./bin/kafka-console-producer.sh --broker-list localhost:9092 --topic partopic

# 消费者
./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic partopic --from-beginning

# 获取主题情况
bin/kafka-topics.sh --zookeeper 172.16.1.157:2181 --list

# 获取消费者消费情况
bin/kafka-consumer-groups.sh --describe --bootstrap-server localhost:9092 --group common

# 更改topic的配置
kafka-topics.sh --zookeeper 172.16.8.4:2181 --alter --topic <topic name> --config retention.ms=1000

# 获取topic的配置
kafka-configs --zookeeper 172.16.8.4:2181 --entity-type topics --describe --entity-name web_log



```

https://blog.csdn.net/xiaofei2017/article/details/80924800

---
# ag-db

docker run -d --name ag-db-00 -p 33060:3306 -e MYSQL_ROOT_PASSWORD=root registry.umlife.net:443/mt-service/schema/alishh/ag-db-00:master

docker run -d --name ag-db-10 -p 33061:3306 -e MYSQL_ROOT_PASSWORD=root registry.umlife.net:443/mt-service/schema/alishh/ag-db-10:master


docker run -d --name ag-db-40 -p 33064:3306 registry.umlife.net:443/mt-service/schema/alishh/ag-db-40:v2



---
*.pyc 不是递归的，
需要加 **/*.pyc

> ** that matches any number of directories (including zero). For example, **/*.go will exclude all files that end with .go that are found in all directories, including the root of the build context.


- https://stackoverflow.com/a/40261165
- https://docs.docker.com/engine/reference/builder/#/dockerignore-file

---
## clickhouse

/home/youmi/data/ch

docker run  --rm -p 9000:9000 --name my-clickhouse-server-v2 --ulimit nofile=262144:262144 --volume=/home/yinzishao/vhost/docker/ch/data:/var/lib/clickhouse  -v /home/yinzishao/vhost/docker/ch/config.xml:/etc/clickhouse-server/config.xml yandex/clickhouse-server


docker run -it --rm --link my-clickhouse-server-v2:clickhouse-server yandex/clickhouse-client --host clickhouse-server

```
CREATE DATABASE mt ENGINE = MySQL('127.0.0.1:3306', 'export_adData', 'root', 'root')

clickhouse :) DETACH DATABASE {need drop database name}
clickhouse :) exit
~ cd {clickhouse data path}
~ rm -rf metadata/{need drop database name}


```


---

[docker-compose安装](https://yeasy.gitbooks.io/docker_practice/compose/install.html)

---
## mysql5.6

/home/youmi/vhost/docker/mysql5.6
```text
docker build -t mysql_private .
```

/home/youmi/mysql5.6

```
docker build -t mysql_private .

docker run -p 13306:3306 --name mymysql -v $PWD/conf/my.cnf:/etc/mysql/my.cnf -v $PWD/logs:/logs -v $PWD/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root  mysql:5.7 --character-set-server=utf8mb4 --collation-server=utf8mb4_bin
```

docker run -p 13306:3306 --name mymysql -v $PWD/conf:/etc/mysql/conf.d -v $PWD/logs:/logs -v $PWD/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456  mysql_private

docker start mymysql
docker ps
docker logs mymysql

docker exec -it mymysql bash

```
show variables like 'general_log'; -- 查看日志是否开启
show variables like 'general_log_file'; -- 看看日志文件保存位置

set GLOBAL general_log='ON';
show variables like '%general_log%'
set global time_zone='+8:00';
```

【mysqld】中添加：general_log = 1

【mysqld】中添加：skip-grant-tables
UPDATE mysql.user SET authentication_string=PASSWORD('password') WHERE user='root';

FLUSH PRIVILEGES;

---
# pg安装

默认配置文件在这里: /var/lib/pgsql/data/postgresql.conf

docker run --name mypostgres -d -p 5432:5432 -e POSTGRES_PASSWORD=password -e USERMAP_UID=youmi -e USERMAP_GID=youmi -v /home/youmi/pg/data:/var/lib/postgresql/data  postgres:9.4


docker pull chorss/docker-pgadmin4

docker run -d --name pgadmin -e SERVER_MODE=true -e PGADMIN_SETUP_EMAIL=yinzishao@youmi.net -e PGADMIN_SETUP_PASSWORD=password -d -p 5050:5050 -v /home/youmi/pgadmin/data:/data chorss/docker-pgadmin4

---

问题：E: Package 'mysql-client' has no installation candidate

原因： python 3.5 没有指定小版本，最新的镜像更新了，导致3.5安装不了了. 固定小版本 3.5.2

好像可以通过maraidb-client 去安装？

---

Debian 10（buster） — 当前的稳定版（stable）
Debian 9（stretch） — 旧的稳定版（oldstable）
Debian 8（jessie） — 更旧的稳定版（oldoldstable）


---
# docker和gitlab ci

py-template 构建了一个镜像. 在另一个需要进行校验的项目的ci里面，可以添加一个stage，把image改成该镜像。
在gitlab的ci流程中，在py-template容器里，把代码拉下来在/bulld/rep/pro 里面，当前路径也是在那里。
但是在ci里面却能够check.sh执行，是因为在py-template的PATH添加了/py-template 的执行命令路径搜索

---
# logs

-f 实时监控
--tail 后几条

清空: cat /dev/null >/var/lib/docker/containers/containerid/containerid.log-json.log

---
# none image
docker rmi $(docker images -f "dangling=true" -q)

---
# 学习笔记

docker run --name webserver -d -p 80:80 nginx

这条命令会用 nginx 镜像启动一个容器，命名为 webserver，并且映射了 80 端口，这样我们可以用浏览器去访问这个 nginx 服务器。

docker exec -it webserver bash
使用 docker exec 命令进入容器，修改其内容。

我们可以通过 docker diff 命令看到具体的改动

docker commit [选项] <容器ID或容器名> [<仓库名>[:<标签>]]
其中 --author 是指定修改的作者，而 --message 则是记录本次修改的内容。这点和 git 版本控制相似，不过这里这些信息可以省略留空。


慎用 docker commit
由于命令的执行，还有很多文件被改动或添加了,如果是安装软件包、编译构建，那会有大量的无关内容被添加进来，如果不小心清理，将会导致镜像极为臃肿。
此外，使用 docker commit 意味着所有对镜像的操作都是黑箱操作，生成的镜像也被称为 黑箱镜像，换句话说，就是除了制作镜像的人知道执行过什么命令、怎么生成的镜像，别人根本无从得知。
每一次修改都会让镜像更加臃肿一次，所删除的上一层的东西并不会丢失，会一直如影随形的跟着这个镜像，即使根本无法访问到。这会让镜像更加臃肿。


sudo docker build -t="ouruser/sinatra:v2" .
其中-t标记来添加tag,指定新的镜像的用户信息。“.”是Dockerfile所在的路径(当前目录),也可以
替换为一个具体的Dockerfile的路径


如果要移除本地的镜像,可以使用	 	docker	rmi	 	命令。注意	 	docker	rm	 	命令是移除容器。
注意:在删除镜像之前要先用	 	docker	rm	 	删掉依赖于这个镜像的所有容器。


启动容器有两种方式，一种是基于镜像新建一个容器并启动，另外一个是将在终止状态（stopped）的容器重新启动。
docker run -t -i ubuntu:18.04 /bin/bash
其中，-t 选项让Docker分配一个伪终端（pseudo-tty）并绑定到容器的标准输入上， -i 则让容器的标准输入保持打开
执行完毕后容器被终止

docker container start 命令，直接将一个已经终止的容器启动运行。

-d 参数让 Docker 在后台运行而不是直接把执行命令的结果输出在当前宿主机下

终止状态的容器可以用 docker container ls -a 命令看到

某些时候需要进入容器进行操作，包括使用 docker attach 命令或 docker exec 命令

docker attach XX 如果从这个 stdin 中 exit，会导致容器的停止。

---

docker build -t test:v1 .

docker run  --name my_django -p 8099:8099 -v /home/youmi/vhost/ag-business:/home/webapp test:v1

docker exec -it my_django bash

RUN apt-get update && apt-get install vim -y

apk add --no-cache


docker run  --name my_django -p 8099:8099 -v /home/youmi/vhost/ag-business/venv/lib/python3.7/site-packages:/usr/local/lib/python3.7/site-packages -v /home/youmi/vhost/ag-business:/home/webapp test:v1

# ag-business
docker run --name ag-business --env CFGENV=feature --env CFGAUTH=ag-apollo:XX --env CFGAPP=ag-business -p 8099:80 ag-business:1.0.0


docker run -i --env CFGENV=LOCAL --env CFGAUTH=ag-apollo:XX --env CFGAPP=ag-test-config --rm registry.umlife.net:443/mt-service/ag-www/cli:feature_media shell

python scripts/docker/app-config.py --app "ag-auth" --env feature --auth "ag-apollo:XX"

echo `` |  docker login -u chenziqing registry.umlife.net:443 --password-stdin


docker build -t registry.umlife.net:443/mt-service/ag-business:feature-init-1.0.0 .


docker build -t registry.umlife.net:443/adxmi/migo:fix-yg .

docker push registry.umlife.net:443/mt-service/ag-business:feature-init-1.0.0

# ag-permission

```
 git checkout -b v1.4.4
 python scripts/docker/app-config.py --host=https://apollo-alishh.umlife.net --app=ag-permission-uni --env=preview  --auth=ag-apollo:xx -d=./config/settings
 python scripts/docker/app-config.py --host=https://apollo-alishh.umlife.net --app=ag-permission-uni --env=preview  --auth=ag-apollo:xx -d=./cli --ns permission_config.json
 python cli/acl.py

docker run -p 8003:80 --env CFGHOST=https://apollo-alishh.umlife.net  --env CFGENV=ag-permission-uni-local --env CFGAUTH=ag-apollo:xx --env CFGAPP=ag-test-config --rm registry.umlife.net:443/mt-service/ag-permission:1.4.4



```


# 本地docker部署
git apply local_docker.diff

docker build -t ag-business .

docker run  --rm --name ag-business -v /home/youmi/vhost/ag-business/log:/home/webapp/log --env MYSQL_HOST=172.16.8.4 --env PERMISSION_DOMAIN=http://localhost:80 --env AUTH_DOMAIN=http://localhost:80 --env MYSQL_PASS=root -p 8099:80 ag-business

---
#tcp-proxy

https://hub.docker.com/r/hpello/tcp-proxy/

在ag-oes服务里面，通过域名请求服务，ag-oes服务没有nginx，无法代理。
采用在rancher里面添加链接，


ag-permission-www 可以直接链接到rancher的容器上
通过 http://ag-permission-www/api/permission/v1/userPermission 可以访问

preview-ag-auth.umlife.com 则可以链接到proxy上，通过tcp-proxy 代理到web-01上

---
# EFK实践

https://blog.51cto.com/3241766/2389762

```
elasticsearch:
    image: elasticsearch:5.3.0
    expose:
      - 9200
    ports:
      - "9200:9200"
```
会对外暴露端口 去掉ports就可以删除对外了。

疑问： expose的是指定暴露的对内端口？但是好像还是9200/tcp, 9300/tcp 两个。去掉了expose，也没影响？


```
    ports:
      - "24224:24224"
      - "24224:24224/udp"
```

PORTS: 5140/tcp, 0.0.0.0:24224->24224/tcp

fluentd`- "24224:24224"`可以去掉，但是一但去掉`- "24224:24224/udp"`去出错了。是因为web容器启动的时候发现fluentd绑定的地址不存在？因为fluentd容器其实只是暴露了5140

ERROR: for web  Cannot start service web: b'failed to initialize logging driver: dial tcp 127.0.0.1:24224: connect: connection refused'


---
# fluent

需要挂载配置

docker run -d -p 24224:24224 -p 24224:24224/udp -v /data:/fluentd/log -v /home/youmi/config:/fluentd/etc fluent/fluentd:v1.3-debian-1

需要安装插件，打包镜像

docker run  -p 24225:24224 -p 24225:24224/udp -v /data:/fluentd/log -v /home/youmi/config:/fluentd/etc govtechsg/fluentd-elasticsearch:latest
