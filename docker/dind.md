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

gitlab使用docker compose的教程


```shell script

ARG DOCKER_VERSION=latest
FROM docker:${DOCKER_VERSION}

ARG COMPOSE_VERSION=1.26.2
ARG DOCKER_VERSION

RUN apk add --no-cache py3-pip python3
RUN apk add --no-cache --virtual build-dependencies python3-dev libffi-dev openssl-dev gcc libc-dev make \
  && pip3 install "docker-compose${COMPOSE_VERSION:+==}${COMPOSE_VERSION}" \
  && apk del build-dependencies

LABEL \
  org.opencontainers.image.authors="Tobias Maier <tobias.maier@baucloud.com>" \
  org.opencontainers.image.description="This docker image installs docker-compose on top of the docker image." \
  org.opencontainers.image.licenses="MIT" \
  org.opencontainers.image.source="https://github.com/tmaier/docker-compose" \
  org.opencontainers.image.title="Docker Compose on docker base image" \
  org.opencontainers.image.vendor="BauCloud GmbH" \
  org.opencontainers.image.version="${DOCKER_VERSION} with docker-compose ${COMPOSE_VERSION}"

```

> 构建自己的compose镜像： `docker build -t my-compose -f Dockerfile.compose .`

---
# 本地compose镜像的使用
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
> 本地挂载docker.sock可以跟本机一样操作docker。

---

- [dind](https://github.com/jpetazzo/dind)

```
docker run --name=dind --rm --privileged -d docker:18.09-dind
docker exec -it dind  /bin/sh
```
本地跑起来docker in docker 。进去容器里面发现是一个独立的docker 服务。
表现为：docker ps 没有任何东西.docker pull busybox 会重新拉取。`ls /var/lib/docker/overlay2/` 为空

---

- [making-docker-in-docker-builds-faster-with-docker-layer-caching](https://docs.gitlab.com/ee/ci/docker/using_docker_build.html#making-docker-in-docker-builds-faster-with-docker-layer-caching)

这个链接介绍了如何在gitlab上运行。

---

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
    command:
      - /bin/sh
      - -c
      - |
        docker image ls
        docker pull busybox
        docker image ls
    depends_on:
      - docker

```
`docker-compose -f docker-compose-dind.yml up`
表现为： 第一次镜像为空。重新拉取busybox。然后保存到dind容器里面。

`docker-compose -f docker-compose-dind.yml stop`
`docker-compose -f docker-compose-dind.yml up`
然后如果简单的停止，下次重启后因为dind容器保持了状态，故镜像还在。但是重建了dind容器的话，镜像就没了。

`docker-compose -f docker-compose-dind.yml rm docker`
`docker-compose -f docker-compose-dind.yml up`
重新拉取

而且在/var/lib/docker/overlay2/ 里面，每次拉取的hash都是不一样的。所以即使通过volumes挂载镜像层进去也没有用。

```shell script
    volumes:
    - ./overlay2:/var/lib/docker/overlay2
```

---

Q： 如何把拉取到的镜像layer层进行打包成新的dind呢？

A: 镜像文件是放在docker容器里面的。/var/lib/docker/overlay2里面的

`docker commit -a "yinzishao" -m "compose with image" dj_docker_1 docker_wi`

但是以上语句的镜像构建，没有把拉下来的镜像打进去。TODO:镜像的数据跟容器内的数据不是一回事。
是因为声明了Volumes:/var/lib/docker: {} ?所以镜像忽略了这个目录？

Dockerfile中的VOLUME使每次运行一个新的container时，都会为其**自动创建一个匿名的volume**，如果需要在不同container之间共享数据，那么我们依然需要通过docker run -it -v my-volume:/foo的方式将/foo中数据存放于指定的my-volume中。

- [利用 commit 理解镜像构成](https://yeasy.gitbook.io/docker_practice/image/commit)

- [do-not-use-docker-in-docker-for-ci](https://jpetazzo.github.io/2015/09/03/do-not-use-docker-in-docker-for-ci/)
Q: And what about the build cache? That one can get pretty tricky too. People often ask me, “I’m running Docker-in-Docker; how can I use the images located on my host, rather than pulling everything again in my inner Docker?”

A: 通过cache文件进行/var/lib/docker的缓存？类似requirement.txt的机制。TODO： [Nikola Kovacs](https://gitlab.com/gitlab-org/gitlab-foss/-/issues/17861)
