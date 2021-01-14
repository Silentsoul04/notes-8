-[NIO入门](https://juejin.im/post/5ef56d445188252e96311704)


Q: Reactor是什么？使用场景是什么？
Q: Reactor的实际应用？Netty，更具体的模型？单reactor单线程/多线程、主从reactor模式对比

特性：reactor本身是同步的、扩展性好（增加reactor实例个数）、复用性好（reactor模型本身与具体的事件处理逻辑无关），来源：[主从reactor模型](https://www.bilibili.com/video/BV1DJ411m7NR?t=1296&p=41)


Q：半同步/半异步？leaders/follers？跟reactor有什么联系吗？
A:

在[面向模式的软件架构(卷4)这书中，reactor有说到真正的定义和缺点（事件处理程序是单线程导致阻塞），所以可以结合半同步/半异步、leaders/follers减轻缺陷。

- [谈半同步/半异步网络并发模型](https://zhuanlan.zhihu.com/p/58860015)： 这篇文章，总结了半同步/半异步与半同步/半反应堆的区别（架构队列设计,I/O发生的地方），也体现了reactor的含义，让人打通所有的概念的联系。
- 参考《面向模式的软件架构(卷4)-分布式计算的模式语言》一书

> 所以可以得出一个结论: reactor是一个事件设计模式（分离和分发），然后半同步/半异步、半同步/半反应堆、leaders/follers这些是在这个基础上（壳？），建立的网络并发模式。

Q: Nginx使用的是什么模式？主进程、子进程、模块化、进程交互等概念？具体的流程是？（惊群）
A:

- 参考：《Nginx高性能Web服务器详解》一书

Nginx的模块快要求异步化：个人理解可以说是其实封装了多线程的异步?也就是模块跟程序交互本来在工作进程是阻塞的，但其实要求异步化（没有阻塞的系统调用？）隐含了一个类似多线程异步的概念。

- [nginx不是使用epoll么? epoll貌似是同步的吧! 那nginx的异步非阻塞到底异步在哪里?](https://www.zhihu.com/question/63193746/answer/206682206): 这里有说到：开发者必须保证每一个事件handler都不得包含任何阻塞调用


Q: Redis使用的模式是什么？单线程（单reactor单线程），原因是什么？具体的流程是？

A: 参考《Redis设计与实现》书

Q: Redis、Netty、Nginx之间的区别是什么？
A: Redis单线程、Netty的主reactor线程（Boss）会监听accept事件，后再分发给多个从reactor线程（不会再交互了），然后从reactor进行I/O读取，分发到多个Worker线程。Nginx的主进程只是监听配置变更、退出信号等。Worker进程负责连接建立和事件处理。

Nginx是主从reactor多进程模型（Worker进程也是一个从的reactor、模块异步化可以映射成多个work线程）、Netty主从多线程模型、redis单reactor单线程模型。


---
- [尚硅谷Netty视频教程](https://www.bilibili.com/video/BV1DJ411m7NR)

看了38到41的reactor的教程：介绍了单reactor单线程（写在一起）、单reactor多线程（Worker线程完成真正的业务处理，主线程的reactor会分发到主线程的handler做read、send，是阻塞的，然后才分发到多个Worker线程）、主从reactor模型（主线程只监听、独立(多个)子reactor线程，进行read、send的I/O读取并分配任务给多个Worker线程。三层）的对比。优缺点的文字总结和解说都很详细。

引出：scalable IO in java这本书，doug lea


---
“莫要瞧不起单线程，除了 Redis 之外，Node.js 也是单线程，Nginx 也是单线程，但是它们都是服务器高性能的典范。”

来自：Redis深度历险的P92，“线程 IO 模型”章节。
