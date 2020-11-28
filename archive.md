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
- [go语言中的map实战](https://studygolang.com/articles/560): 并发修改哈希表
- [go sync.Map源码分析](https://juejin.im/post/6844903598317371399): 对比sync.map与concurrent-map
- [深入理解sync.Map](https://my.oschina.net/u/4587630/blog/4408032): 对比java和go的并发hash的标准库的区别
- [Go 1.9 sync.Map揭秘](https://colobu.com/2017/07/11/dive-into-sync-Map/)
- [通过实例深入理解sync.Map的工作原理](https://tonybai.com/2020/11/10/understand-sync-map-inside-through-examples/): 通过实例法，我们大致得到了sync.Map的工作原理和行为特征。read dirty之间的数据行为

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

## 其他
- [Go语言中的错误处理（Error Handling in Go）](http://ethancai.github.io/2017/12/29/Error-Handling-in-Go/): 理解goland的错误处理机制。

- [[]T 还是 []*T, 这是一个问题](https://colobu.com/2017/01/05/-T-or-T-it-s-a-question/): 只是说明了副本创建的各种情况
- [深度解密Go语言之关于 interface 的10个问题](https://www.cnblogs.com/qcrao-2018/p/10766091.html): 值接收者和指针接收者的区别
- [接口](https://draveness.me/golang/docs/part2-foundation/ch04-basic/golang-interface): 从底层汇编解释接口。eface、iface
- [说说 Go 语言中的空接口](https://github.com/iswbm/GolangCodingTime/blob/master/source/c02/c02_05.rst) 、[2.6 图解: 静态类型与动态类型](https://github.com/iswbm/GolangCodingTime/blob/master/source/c02/c02_06.rst)
- [1.8 万字详解 Go 是如何设计 Map 的](https://mp.weixin.qq.com/s/OJSxIXH87mjCkQn76eNQsQ): 太详细了，详细到底层分析
- [应用编译，计算机中一定要掌握的知识细节](https://mp.weixin.qq.com/s/YKZ3MJuGVgWJG69WATRPPQ): 预处理、编译、汇编以及链接。go实例分析前三个部分

## network

- [Go netpoller 原生网络模型之源码全面揭秘](https://strikefreedom.top/go-netpoll-io-multiplexing-reactor): 从源码和例子分析。引出reactor对比分析、gnet等。TODO
- [谈半同步/半异步网络并发模型](https://zhuanlan.zhihu.com/p/58860015)： 这篇文章，总结了半同步/半异步与半同步/半反应堆的区别（架构队列设计,I/O发生的地方），也体现了reactor的含义，让人打通所有的概念的联系
- [nginx不是使用epoll么? epoll貌似是同步的吧! 那nginx的异步非阻塞到底异步在哪里?](https://www.zhihu.com/question/63193746/answer/206682206): 这里有说到：开发者必须保证每一个事件handler都不得包含任何阻塞调用


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

---
# java

## 锁

- [搞懂 Java 并发中的 AQS 是怎么运行的](https://mp.weixin.qq.com/s/tMI6qV_ItuTqlKZiUnAlmg): 晦涩难懂
