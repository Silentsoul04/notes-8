# archive

---
# go
- [go](/notebook/go)

## GMP
- [goroutine](/notebook/go/goroutine.md)

- [Golang 并发模型之 GMP 浅   尝](https://mp.weixin.qq.com/s/p_7qZH5Ix3vVJEvbPHyMng)
- [30+张图讲解: Golang调度器GMP原理与调度全分析](https://mp.weixin.qq.com/s?__biz=MzAxMTA4Njc0OQ==&mid=2651438895&idx=3&sn=d7328484410c825c6e35b51a324f0c65&chksm=80bb61ddb7cce8cba59349bcae7c067db08e66428650962450cd3a081b9e96fae8db45758087&scene=21#wechat_redirect): 这篇文章讲得很清晰，值得多读。很多点都说到了，M的回收与P的空闲与绑定。 [](#bookmark)

## 并发
- [并发](/notebook/go/并发与锁.md)

- [源码面前无秘密 | Golang标准库 sync.WaitGroup](https://juejin.im/post/6866971615717457934): sync.WaitGroup的源码并不多但会考虑很多并发情况,总体难度适中,很适合go初学者作为go源码阅读的起点.
- [Go 语言标准库中 atomic.Value 的前世今生](https://blog.betacat.io/post/golang-atomic-value-exploration/)
- [Go 标准库源码学习（一）详解短小精悍的 Once](https://mp.weixin.qq.com/s/Lsm-BMdKCKNQjRndNCLwLw): 对once深入理解，提了3点疑问

- [理解真实世界中 Go 的并发 BUG](https://mp.weixin.qq.com/s/EnLxJEoPrASWytmM8jJtmg): 很多真实世界可能会发生的并发BUG，值得参考！

## map
- [go语言中的map实战](https://studygolang.com/articles/560): 并发修改哈希表
- [go sync.Map源码分析](https://juejin.im/post/6844903598317371399): 对比sync.map与concurrent-map
- [深入理解sync.Map](https://my.oschina.net/u/4587630/blog/4408032): 对比java和go的并发hash的标准库的区别
- [Go 1.9 sync.Map揭秘](https://colobu.com/2017/07/11/dive-into-sync-Map/)
- [通过实例深入理解sync.Map的工作原理](https://tonybai.com/2020/11/10/understand-sync-map-inside-through-examples/): 通过实例法，我们大致得到了sync.Map的工作原理和行为特征。read dirty之间的数据行为
- [go基础之map-写在前面（一)](https://mp.weixin.qq.com/s/Aw8AjDmuvf7n7ACWl7mwaw) : 源码，编译原理。相关链接中的文章也较详细。 [抽丝剥茧—Go哈希Map的鬼魅神功](https://mp.weixin.qq.com/s?__biz=MzAxMTA4Njc0OQ==&mid=2651440382&idx=3&sn=2aa006a968994df6027f8e6c5392722a&chksm=80bb1a0cb7cc931a3ce45fb280d0f2e04c9e9032e1b952c42a231688b28740b11fcfff44166f&scene=21#wechat_redirect)
- [1.8 万字详解 Go 是如何设计 Map 的](https://mp.weixin.qq.com/s/OJSxIXH87mjCkQn76eNQsQ): 太详细了，详细到底层分析

## GC
- [浅析 Golang 垃圾回收机制](https://mp.weixin.qq.com/s/LTz8UjCvaxZvAPRqeFCxjQ): 挺清晰的介绍垃圾回收的入门概念
- [GO GC 垃圾回收机制](https://segmentfault.com/a/1190000018161588): 比较概括。
- [图文结合，白话Go的垃圾回收原理](https://juejin.im/post/6882206650875248654): 比较清晰分析各种方法的优缺点，这样做的理由。而且在算法过程方面的讲述比较白话，但是在写屏障的介绍可能有点不好，不过也能让我们知道大概。 [](#bookmark)
- [图解: 宏观角度看 Go 语言如何实现垃圾回收中的 Stop the World](https://mp.weixin.qq.com/s/rt4lxGwaYo8IkTdmo186Cg): 说明stw的简要步骤，并且说明跟系统调用的关系，引出避免长时间的调用。

## chan
- [通道](/notebook/go/通道.md)

- [图解Golang channel源码](https://juejin.im/post/6875325172249788429): 主要是围绕着一个环形队列和两个链表展开
- [如何实现一个协程池？](https://github.com/iswbm/GolangCodingTime/blob/master/source/c04/c04_10.rst): 使用通道的实现的方法很值得推敲。
- [如何优雅地关闭Go channel](https://www.jianshu.com/p/d24dfbb33781): 有具体的准则和例子

## error
- [Go语言中的错误处理（Error Handling in Go）](http://ethancai.github.io/2017/12/29/Error-Handling-in-Go/): 理解goland的错误处理机制。
- [关于 Golang 错误处理的一些思考](https://mp.weixin.qq.com/s?__biz=MzAxMTA4Njc0OQ==&mid=2651441294&idx=3&sn=bb20e907f3886961777c2368e8d05cdd&chksm=80bb167cb7cc9f6a1bca359641a9eaa2316fc57f016ca6cab3cd4f13f101874594c7291b06ee&scene=21#wechat_redirect): 创建错误的形式，处理方法error、xerror，一些提案

## 其他
- [[]T 还是 []*T, 这是一个问题](https://colobu.com/2017/01/05/-T-or-T-it-s-a-question/): 只是说明了副本创建的各种情况
- [深度解密Go语言之关于 interface 的10个问题](https://www.cnblogs.com/qcrao-2018/p/10766091.html): 值接收者和指针接收者的区别
- [接口](https://draveness.me/golang/docs/part2-foundation/ch04-basic/golang-interface): 从底层汇编解释接口。eface、iface
- [说说 Go 语言中的空接口](https://github.com/iswbm/GolangCodingTime/blob/master/source/c02/c02_05.rst) 、[2.6 图解: 静态类型与动态类型](https://github.com/iswbm/GolangCodingTime/blob/master/source/c02/c02_06.rst)
- [应用编译，计算机中一定要掌握的知识细节](https://mp.weixin.qq.com/s/YKZ3MJuGVgWJG69WATRPPQ): 预处理、编译、汇编以及链接。go实例分析前三个部分

## 网络
- [Go netpoller 原生网络模型之源码全面揭秘](https://strikefreedom.top/go-netpoll-io-multiplexing-reactor): 从源码和例子分析。引出reactor对比分析、gnet等。简单介绍了select、epoll的代码结束，而且详细对比了分析各自的优缺点，并且很好的从源码分析了几个问题，但是没有再深入介绍？。TODO
- [谈半同步/半异步网络并发模型](https://zhuanlan.zhihu.com/p/58860015): 这篇文章，总结了半同步/半异步与半同步/半反应堆的区别（架构队列设计,I/O发生的地方），也体现了reactor的含义，让人打通所有的概念的联系
- [nginx不是使用epoll么? epoll貌似是同步的吧! 那nginx的异步非阻塞到底异步在哪里?](https://www.zhihu.com/question/63193746/answer/206682206): 这里有说到：开发者必须保证每一个事件handler都不得包含任何阻塞调用
- [重大事故！IO问题引发线上20台机器同时崩溃](https://juejin.im/post/6875176737274724366): 这篇文章写得很好，值得多读。该博主也经常分析性能调优的文章。
- [Linux的五种IO模型](https://juejin.cn/post/6844903687626686472): 这篇文章讲得很好！

## etcd
- [跟 etcd 学习数据库中事务隔离的实现](https://blog.betacat.io/post/2019/08/learn-transaction-isolation-levels-from-etcd/)
- [MVCC 在 etcd 中的实现](https://blog.betacat.io/post/mvcc-implementation-in-etcd/)

## awesome

- [Go编程时光](http://golang.iswbm.com/en/latest/): 这个项目的基本用法讲述得还可以。可以当成写代码的手册类。网页中标亮点为重点。
- [go-zero](https://www.yuque.com/tal-tech/go-zero/yaoehb):  理解架构和源码。
- [Go 语言设计与实现](https://draveness.me/golang/): draveness大神的书


---
# python
- [gevent.md](/notebook/python/gevent.md)
- [uwsgi.md](/notebook/python/uwsgi.md)

## 网络
- [深入理解uwsgi和gunicorn网络模型[上]](http://xiaorui.cc/archives/4264): 这篇文章比较深入，提了问题也很到位，有助思考
- [去 async/await 之路](https://zhuanlan.zhihu.com/p/45996168): 说明python的异步的一些方式和对比。
- [Gevent高并发网络库精解:一些数据通信的数据结构](https://www.jianshu.com/p/ccf3bd34340f)
- [TODO: Python 开源异步并发框架的未来](https://segmentfault.com/a/1190000000471602)

## 数据结构
- [sort](/notebook/algorithm/排序/sorted.md): python的排序是怎么实现的
- [dict](): TODO python的字典是怎么实现的，如何解决hash冲突。


---
# 分布式
- [分布式](../notebook/SOD/分布式)

## redis
- [分布式锁的实现之 redis 篇](https://xiaomi-info.github.io/2019/12/17/redis-distributed-lock/): redis锁相关会存在的问题与图分析
- [分布式锁用 Redis 还是 Zookeeper？](https://juejin.im/post/6894853961761685517): 分析具体场景，两种解决办法的简单使用与对比。

## 分布式锁
- [分布式柔性事务的TCC方案](https://mp.weixin.qq.com/s/tnmQaHpo49XUtYBvsrx1Ig): TCC的总结


---
# 优雅退出
- [优雅退出](/notebook/SOD/优雅退出.md)
- [优雅退出例子](/notebook/SOD/优雅退出例子.md)

## 参考链接
- [Service Mesh 实践（五）: 优雅启动和优雅关闭](https://www.dozer.cc/2020/02/graceful-start-and-shutdown.html)
- [pod-lifecycle](https://kubernetes.io/zh/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination-forced)
- [kubernetes-best-practices-terminating-with-grace](https://cloud.google.com/blog/products/gcp/kubernetes-best-practices-terminating-with-grace)
- [bestpractice-pod-prestop](http://docs.api.xiaomi.com/en/app-engine-k8s/bestpractice-pod-prestop.html)
- [linux: nohup 命令实现守护进程（屏蔽 SIGHUP 信号）](https://my.oschina.net/sallency/blog/827737)
- [停止或暂停程序的信号: intr、quit、stop](https://my.oschina.net/u/2914561/blog/808585)
- [一次 Docker 容器内大量僵尸进程排查分析](https://juejin.im/post/6844904029248552973)
- [Dumb-Init进程信号处理](https://my.oschina.net/xiaominmin/blog/3223293)
- [docker-containerd-shim](https://juejin.im/entry/6844903454549229576)
- [when-a-parent-process-is-killed-by-kill-9-will-subprocess-also-be-killed](https://stackoverflow.com/questions/1491674/when-a-parent-process-is-killed-by-kill-9-will-subprocess-also-be-killed)
- [僵尸进程例子](https://github.com/Yelp/dumb-init/issues/128)

- [揭密容器环境下 Golang 回收子进程的运行机制](https://mp.weixin.qq.com/s/3HsqtHwWReX1S3ggP2_owg): reaper例子子进程提前回收，父进程wait失败。解决办法：同步锁


---
# clickhouse

## 低基数
- [ClickHouse中的低基数字段优化](https://mp.weixin.qq.com/s/XKQk4hsdj8VN8TnYdrOnuw): 指如何优化低基数的字符串字段。通过LowCardinality把字段通过类似position的压缩技术，改成字典。字符越长效果越佳。
- [LowCardinality Data Type](https://clickhouse.tech/docs/en/sql-reference/data-types/lowcardinality/): 官网文档
- [A MAGICAL MYSTERY TOUR OF THE LOWCARDINALITY DATA TYPE](https://altinity.com/blog/2019/3/27/low-cardinality): 不知道对数值类型有多少优化空间。
- [LowCardinality 数据类型的神秘之旅](https://blog.csdn.net/jiangshouzhuang/article/details/103268340): 具体的倒排索引图和具体的代码与例子。
- [allow_suspicious_low_cardinality_types](https://clickhouse.tech/docs/en/operations/settings/settings/#allow_suspicious_low_cardinality_types): 允许或限制将LowCardinality用于固定大小为8个字节或更少的数据类型：数字数据类型和FixedString（8_bytes_or_less）。要注意较小的固定值可能适得其反。

- [LowCardinality](./数据库/clickhouse/LowCardinality.md)： 总结与测试

## 其他
- [five-ways-to-handle-as-of-queries-in-clickhouse](https://altinity.com/blog/2020/4/8/five-ways-to-handle-as-of-queries-in-clickhouse): 通过比较5种方式去，来说明怎么拿时间序列的最靠近的一行（窗口、Top K 的场景）。比较贴近生产的例子。
- [joins-in-clickhouse-materialized-views](https://altinity.com/blog/2020-07-14-joins-in-clickhouse-materialized-views):  通过物化视图和join操作，进行实时汇总进汇总表的操作。但是要注意join的一些小陷阱。ClickHouse只触发联接中最左边的表。其他表可以为转换提供数据，但是视图不会对这些表上的插入做出反应。
- [clickhouse-dictionaries-reloaded](https://altinity.com/blog/2020/5/19/clickhouse-dictionaries-reloaded): 字典的一个改版优化。之前字典声明和使用的不便。新版本可以直接通过ddl进行管理，而且能更好优化join查询。它只需要5次调用，而不需要扫描1000万行表（？：字面理解是左边直接调用了5次join。还是说字典直接在内存，所以能优化数据装载过程而已）。

## 位图
- [ClickHouse留存分析工具十亿数据秒级查询方案](https://mp.weixin.qq.com/s/Bh5aEvpBgSEDkTozpfMFkw): 通过位图的，优化留存用户的分析。有具体代码与总结、参考文献。
- [ClickHouse遇见RoaringBitmap](https://blog.csdn.net/nazeniwaresakini/article/details/108166089): 引出AggregateFunction、源码分析。
- [bitmap-functions](https://clickhouse.tech/docs/en/sql-reference/functions/bitmap-functions/): 官方文档
- [bitmap](/notebook/数据库/clickhouse/bitmap.md): 总结测试与例子。
- [高效压缩位图RoaringBitmap的原理与应用](https://www.jianshu.com/p/818ac4e90daf): 前言介绍的挺好的，对比布隆过滤器和HyperLogLog。和用单纯的位图的空间占用引出RBM、相关论文。但是后面的算法详解有点简陋
- [RoaringBitmap数据结构及原理](https://blog.csdn.net/yizishou/article/details/78342499): 有比较具体空间和过程的分析


---
# 设计模式
- [ORM is an anti-pattern](https://seldo.com/posts/orm_is_an_antipattern): ORM的一些对比和作者说其反模式的理解


---
# mysql
- [一次SQL查询优化原理分析](https://www.jianshu.com/p/0768ebc4e28d): 回表、分页优化。引出INNODB_BUFFER_PAGE的使用
- [优化 SQLite 在 Go 中的性能](https://turriate.com/articles/making-sqlite-faster-in-go): 连接池和prepare


---
# java

## 锁
- [搞懂 Java 并发中的 AQS 是怎么运行的](https://mp.weixin.qq.com/s/tMI6qV_ItuTqlKZiUnAlmg): 晦涩难懂
- [i++ 是线程安全的吗？](https://mp.weixin.qq.com/s/H0E_y6tC4d8-AxqJS3u--A): volatile解决了线程间共享变量的可见性问题、 volatile并不能解决线程同步问题

---
# 容器
- [Kubernetes 如何使用 Nginx-Ingress 实现蓝绿和金丝雀发布](https://mp.weixin.qq.com/s/SAE4IvjVPVV1dfS4ZXwzbQ): Ingress-Nginx在0.21版本引入了Canary功能。一个具体的例子介绍使用。而且后面介绍了A/B测试和蓝绿部署以及金丝雀区别，
- [如何为服务网格选择入口网关？](https://zhaohuabing.com/post/2019-03-29-how-to-choose-ingress-for-service-mesh/): 介绍了内部服务间的通信(Cluster IP、Istio Sidecar Proxy)的优缺点。如何从外部网络访问， 如何为服务网格选择入口网关？。介绍包括Pod、Service、NodePort、LoadBalancer、Ingress、Gateway、VirtualService等，最后采用API Gateway + Sidecar Proxy作为服务网格的流量入口还不能很好理解。


---
# 其他
- [如何写出安全的、基本功能完善的Bash脚本](https://mp.weixin.qq.com/s/ZO5jKzQGDy1Di1WDl49d_g): 一个比较实用的模板
- [高效的数据压缩编码方式 Protobuf](https://mp.weixin.qq.com/s/Llg1Rb11KRNS1N-seqjeLg )、 [高效的序列化/反序列化数据方式 Protobuf](https://mp.weixin.qq.com/s/22p3VucucXkxxhDq--AYaw ) TODO 如何高效
- TODO prometheus的时序时间库原理


---
# 网络
- **[network](/notebook/network): 摘抄与总结**

- [为什么 TCP 协议有 TIME_WAIT 状态](https://mp.weixin.qq.com/s/QTZJdxVzDNEvz7htDgGU-w): 为什么系列。 [time_wait的含义](/notebook/network/q.md#time_wait)
- [**为什么 TCP 建立连接需要三次握手**](https://mp.weixin.qq.com/s?__biz=MzU5NTAzNjc3Mg==&mid=2247484001&idx=1&sn=b7408aa515cb494b23237a01b92dee6a&chksm=fe795d6ac90ed47cf6dff54a139b70052f3a53b64363c1933ebb4d477a31beeae10aca70db61&scene=21#wechat_redirect): 『两次握手』：无法避免历史错误连接的初始化，浪费接收方的资源；『四次握手』：TCP 协议的设计可以让我们同时传递 ACK 和 SYN 两个控制信息，减少了通信次数，所以不需要使用更多的通信次数传输相同的信息；
- [通过实例理解Go标准库http包是如何处理keep-alive连接的](https://tonybai.com/2021/01/08/understand-how-http-package-deal-with-keep-alive-connection/): keep-alive的基本使用、idletimeout。TODO: 长连接、底层TCP的状态是怎么样的？

- [Node.js 线程你理解的可能是错的](https://juejin.im/post/5b1e55cbe51d45067e6fcb84): 从问题出发，解析线程与异步操作
- [**不要阻塞你的事件循环**](https://nodejs.org/zh-cn/docs/guides/dont-block-the-event-loop/): 对事件循环有很详细的介绍，适合多读
- [网络库libevent、libev、libuv对比](https://blog.csdn.net/lijinqi1987/java/article/details/71214974)

- [如何优化 Go HTTP client 的性能](https://www.loginradius.com/blog/async/tune-the-go-http-client-for-high-performance/): Client的Timeout参数与DefaultMaxIdleConnsPerHost


---
# 操作系统
- [自己动手实现一个malloc内存分配器](https://mp.weixin.qq.com/s/FpXLBOVm5P-sNTr2S7PyhQ): 比较直白的内存分配器介绍：我们的简单内存分配器采用了First Fit分配算法；找到一个满足要求的内存块后会进行切分，剩下的作为新的内存块；同时当释放内存时会立即合并相邻的空闲内存块，同时为加快合并速度，我们引入了Donald Knuth的设计方法，为每个内存块增加footer信息。
- [函数运行时在内存中是什么样子？](https://mp.weixin.qq.com/s?__biz=MzU2NTYyOTQ4OQ==&mid=2247484963&idx=1&sn=542d3bec57c6a9dfc17c83005fd2c030&chksm=fcb9817dcbce086b10cb44cad7c9777b0088fb8d9d6baf71ae36a9b03e1f8ef5bec62b79d6f7&scene=21#wechat_redirect): 跳转地址、存放参数、局部变量、寄存器初始值。不要创建过大的局部变量、函数栈帧，也就是调用层次不能太多

- [记一次面试：进程之间究竟有哪些通信方式？](https://mp.weixin.qq.com/s/CGqy0j5WvarN6mTmYB8vSA)
