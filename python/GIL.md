首先需要明确的一点是GIL并不是Python的特性，它是在实现Python解析器(CPython)时所引入的一个概念。

Python也一样，同样一段代码可以通过CPython，PyPy，Psyco等不同的Python执行环境来执行。像其中的JPython就没有GIL。然而因为CPython是大部分环境下默认的Python执行环境。所以在很多人的概念里CPython就是Python，也就想当然的把GIL归结为Python语言的缺陷。所以这里要先明确一点：GIL并不是Python的特性，Python完全可以不依赖于GIL


> In CPython, the global interpreter lock, or GIL, is a mutex that prevents multiple native threads from executing Python bytecodes at once. This lock is **necessary mainly because CPython’s memory management is not thread-safe**. (However, since the GIL exists, other features have grown to depend on the guarantees that it enforces.)

好吧，是不是看上去很糟糕？一个防止多线程并发执行机器码的一个Mutex，乍一看就是个BUG般存在的全局锁嘛！


Python当然也逃不开，为了利用多核，Python开始支持多线程。而解决多线程之间数据完整性和状态同步的最简单方法自然就是加锁。 于是有了GIL这把超级大锁，而当越来越多的代码库开发者接受了这种设定后，他们开始大量依赖这种特性（即默认python内部对象是thread-safe的，无需在实现时考虑额外的**内存锁和同步操作**）。

> 指的是内部对象，内存管理的线程安全。

>慢慢的这种实现方式被发现是蛋疼且低效的。但当大家试图去拆分和去除GIL的时候，发现大量库代码开发者已经重度依赖GIL而非常难以去除了。

可以看到python在多线程的情况下居然比单线程整整慢了45%。按照之前的分析，即使是有GIL全局锁的存在，串行化的多线程也应该和单线程有一样的效率才对。那么怎么会有这么糟糕的结果呢？

# 缺陷
## 基于pcode数量的调度方式
按照Python社区的想法，操作系统本身的**线程调度**已经非常成熟稳定了，没有必要自己搞一套。所以Python的线程就是C语言的一个**pthread**，并通过操作系统调度算法进行调度（例如linux是CFS）。为了让各个线程能够平均利用CPU时间，python会**计算当前已执行的微代码数量，达到一定阈值后就强制释放GIL。而这时也会触发一次操作系统的线程调度**（当然是否真正进行上下文切换由操作系统自主决定）。


```python

while True:
    acquire GIL
    for i in 1000:
        do something
    release GIL
    /* Give Operating System a chance to do thread scheduling */
```

这种模式在只有一个CPU核心的情况下毫无问题。任何一个线程被唤起时都能成功获得到GIL（因为只有释放了GIL才会引发线程调度）。但当CPU有多个核心的时候，问题就来了。从伪代码可以看到，**从release GIL到acquire GIL之间几乎是没有间隙的**。所以当其他在其他核心上的线程被唤醒时，大部分情况下**主线程已经又再一次获取到GIL了**。这个时候**被唤醒执行的线程只能白白的浪费CPU时间**，看着另一个线程拿着GIL欢快的执行着。然后**达到切换时间后进入待调度状态**，再被唤醒，再等待，以此往复恶性循环。

> 子线程唤醒的间隙，主线程再次获得锁，导致子线程一直被唤醒，等待，却不能获得GIL锁，浪费CPU时间。

PS：当然这种实现方式是原始而丑陋的，Python的每个版本中也在逐渐改进GIL和线程调度之间的互动关系。例如**先尝试持有GIL在做线程上下文切换**，**在IO等待时释放GIL等尝试**。但是无法改变的是GIL的存在使得操作系统线程调度的这个本来就昂贵的操作变得更**奢侈**了。

## 总结
简单的总结下就是：**Python的多线程在多核CPU上，只对于IO密集型计算产生正面效果；而当有至少有一个CPU密集型线程存在，那么多线程效率会由于GIL而大幅下降**。

## 如何避免受到GIL的影响

### 用multiprocessing替代Thread

multiprocessing库的出现很大程度上是为了弥补thread库因为GIL而低效的缺陷。它完整的复制了一套thread所提供的接口方便迁移。唯一的不同就是它使用了多进程而不是多线程。每个进程有自己的独立的GIL，因此也不会出现进程之间的GIL争抢。

它的引入会增加程序实现时线程间数据通讯和同步的困难。就拿计数器来举例子，如果我们要多个线程累加同一个变量，对于thread来说，申明一个global变量，用thread.Lock的context包裹住三行就搞定了。而multiprocessing由于进程之间无法看到对方的数据，只能通过在主线程申明一个**Queue**，put再get或者用**share memory**的方法。这个额外的实现成本使得本来就非常痛苦的多线程程序编码，变得更加痛苦了。
> 进程间的通讯导致编码成本过高的问题

当然Python社区也在非常努力的不断改进GIL，甚至是尝试去除GIL。并在各个小版本中有了不少的进步。有兴趣的读者可以扩展阅读这个Slide 另一个改进Reworking the GIL

将切换颗粒度从基于opcode计数改成基于时间片计数
避免最近一次释放GIL锁的线程再次被立即调度
新增线程优先级功能（高优先级线程可以迫使其他线程释放所持有的GIL锁）