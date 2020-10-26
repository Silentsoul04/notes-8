```
docker run --name=node1 --restart=always \
             -e 'CONSUL_LOCAL_CONFIG={"skip_leave_on_interrupt": true}' \
             -p 8300:8300 \
             -p 8301:8301 \
             -p 8301:8301/udp \
             -p 8302:8302/udp \
             -p 8302:8302 \
             -p 8400:8400 \
             -p 8500:8500 \
             -p 8600:8600 \
             -h node1 \
             consul agent -server -bind=172.16.8.4 -bootstrap-expect=3 -node=node1 \
             -data-dir=/tmp/data-dir -client 0.0.0.0 -ui

docker run -d --name=registrator \
             -v /var/run/docker.sock:/tmp/docker.sock \
             --net=host \
             gliderlabs/registrator -ip="172.16.8.4" consul://172.16.8.4:8500


```
作者：零壹技术栈
链接：https://juejin.im/post/5b2a6b606fb9a00e594c676d
来源：掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

---

```
docker run -d --network=host --rm -p 8500:8500 -v ~/data/consul:/consul/data -e CONSUL_BIND_INTERFACE='eth0' --name=consul_server_1 consul agent -server -bootstrap -ui -node=1 -client='0.0.0.0'

docker run -d --network=host --rm -p 8500:8500 -v ~/data/consul:/consul/data --name=consul_server_1 consul agent -server -bootstrap -ui -node=1 -client='0.0.0.0'

--network=host: 跨容器好像也不能连接？

-client：表示 Consul 将绑定客户端接口的地址，0.0.0.0 表示所有地址都可以访问

docker exec consul_server_1 consul members

docker run -d -e CONSUL_BIND_INTERFACE='eth0' --name=consul_server_2 consul agent -server -node=2  -join='172.17.0.3'

docker run -d -e CONSUL_BIND_INTERFACE='eth0' --name=consul_server_3 consul agent -server -node=3  -join='172.17.0.3'



docker run -d -e CONSUL_BIND_INTERFACE='eth0' --name=consul_server_4 consul agent -client -node=4 -join='172.17.0.3' -client='0.0.0.0'

docker run -d -e CONSUL_BIND_INTERFACE='eth0' --name=consul_server_5 consul agent -client -node=5 -join='172.17.0.3' -client='0.0.0.0'


docker run -d -e CONSUL_BIND_INTERFACE='eth0' --name=consul_server_6 consul agent -client -node=5 -join='172.17.0.3' -client='0.0.0.0'


docker exec consul_server_1 consul members Node Address Status Type Build Protocol DC Segment 1

```
- [Docker - 容器部署 Consul 集群](https://www.cnblogs.com/lfzm/p/10633595.html)

---


registrator来监控每个service web的状态。当有新的service web启动的时候，registrator会把它注册到consul这个注册中心上。由于consul_template已经订阅了该注册中心上的服务消息，此时consul注册中心会将新的service web信息推送给consul_template，consul_template则会去修改nginx.conf的配置文件，然后让nginx重新载入配置以达到自动修改负载均衡的目的。同样当一个service web挂了，registrator也能感知到，进而通知consul做出响应。


curl http://127.0.0.1/getRemoteIp


/home/youmi/vhost/docker/consul/consul.yml

```
# 定义service-web的负载均衡，
# 从consul cluster获取对应的注册服务器的ip与port
# 监听consul cluster 服务变化，一旦发生变化会自动更新服务列表
upstream app {
  {{range service "service-web"}}server {{.Address}}:{{.Port}} max_fails=3 fail_timeout=60 weight=1;
  {{else}}server 127.0.0.1:65535; # force a 502{{end}}
}
```

一旦监听的服务列表发生变化，触发nginx重加载.见consul-template.service

```
#!/bin/sh
exec consul-template \
     -consul-addr=consul:8500 \
     -template "/etc/consul-templates/nginx.conf:/etc/nginx/conf.d/app.conf:nginx -s reload"
```
`
docker-compose  -f consul.yml up -d --scale serviceweb=3
`



- [基于Docker实现服务治理（一）](https://www.zhihu.com/people/chen-feng-xie-70/posts)
- [基于Docker实现服务治理（三）](https://zhuanlan.zhihu.com/p/36834989)


