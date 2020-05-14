uWSGI原生支持HTTP, FastCGI, SCGI及其特定的名为”uwsgi”的协议 (是哒，错误的命名选择)。最好的协议显然是uwsgi，nginx和Cherokee已经支持它了 (虽然有各种Apache模块可用)

一个常用的nginx配置如下：
```
location / {
    include uwsgi_params;
    uwsgi_pass 127.0.0.1:3031;
}
```
这表示“传递每一个请求给绑定到3031端口并使用uwsgi协议的服务器。



---
## 添加鲁棒性：Master进程

高度推荐在生产应用上总是运行master进程。

它将不断监控你的进程/线程，并且会添加有趣的特性，例如 uWSGI Stats服务器

要启用master，只需添加–master

---


## [重载服务器](https://uwsgi-docs-zh.readthedocs.io/zh_CN/latest/Management.html#id3)
当运行在 master 进程模式下时，uWSGI服务器可以在无需关闭主socket的情况下优雅地重启。

这个功能允许你在无需关闭与web服务器的连接以及丢失请求的情况下修补/更新uWSGI服务器。

当你发送 SIGHUP 给主进程时，它会试着优雅地停止所有的worker，等待任何当前运行中的请求完成。

然后，它关闭所有与uWSGI无关的最终打开的文件描述符。

最后，它使用一个新的来二进制修补 (使用 execve()) uWSGI进程镜像，继承所有之前的文件描述符。

服务器将会知道它是一个已重载的实例，并且会跳过所有的socket初始化，重用之前的。

> 发送 SIGTERM 信号将会获得与优雅地重载相同的结果，但将不会等待运行中的请求的完成。

---

> 如果你看到你的测试在更高的并发速率下失败了，那么你可能到达了你的OS socket backlog队列限制 (在Linux中最高是128个槽，可以通过 /proc/sys/net/somaxconn 和 /proc/sys/net/ipv4/tcp_max_syn_backlog 对TCP socket进行调整)。
  
> 你可以使用 listen 配置选项，在uWSGI中设置这个值。

---

## 为什么不简单地使用HTTP作为协议？
一个好问题，它有一个简单的答案：HTTP解析很慢，真的很慢。为嘛我们应该做一个复杂的任务两次呢？web服务器已经解析请求了！ uwsgi protocol 对机器而言，是非常容易解析的，而HTTP对人类而言，是非常容易解析的。一旦人类被当成服务器使用，我们会放弃uwsgi协议，支持HTTP协议。这就是说，你也可以通过 原生HTTP支持, FastCGI, ZeroMQ 和其他协议使用uWSGI。

---

## http http-socket

http 和 http-socket的使用上有一些区别:

[原生HTTP支持](https://uwsgi-docs-zh.readthedocs.io/zh_CN/latest/HTTP.html)
- http: 自己会产生一个额外的http进程(可以认为与nginx同一层, 有路由器/代理/负载均衡器)负责路由http请求给worker, http进程和worker之间使用的是uwsgi协议
- http-socket: 不会产生http进程, 一般用于在前端webserver不支持uwsgi而仅支持http时使用, 他产生的worker使用的是http协议
- socket:  客户端的请求支持uwsgi, 则直接使用socket即可(tcp or unix)

Official documents recommend using http for a public server and http-socket for web-server after Nginx or Apache if you want use http in network.


因此, http 一般是作为独立部署的选项; http-socket 在前端webserver不支持uwsgi时使用,
如果前端webserver支持uwsgi, 则直接使用socket即可(tcp or unix)


uwsgi://127.0.0.1:8091
