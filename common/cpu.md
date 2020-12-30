

-----
# 进程状态

进程的三种基本状态

## 就绪(Ready)状态

当进程已分配到除CPU以外的所有必要的资源，只要获得处理机便可立即执行，这时的进程状态称为就绪状态。

## 执行（Running）状态
当进程已获得处理机，其程序正在处理机上执行，此时的进程状态称为执行状态。

## 阻塞(Blocked)状态
正在执行的进程，由于等待某个事件发生而无法执行时，便放弃处理机而处于阻塞状态。引起进程阻塞的事件可有多种，例如，等待I/O完成、申请缓冲区不能满足、等待信件(信号)等。

以上是最经典也是最基本的三种进程状态，但现在的操作系统都根据需要重新设计了一些新的状态。

如linux：

- 运行状态（TASK_RUNNING）：**是运行态和就绪态的合并**，表示进程正在运行或准备运行，Linux 中使用TASK_RUNNING 宏表示此状态

- 可中断睡眠状态（浅度睡眠）（TASK_INTERRUPTIBLE）：进程正在睡眠（被阻塞），等待资源到来是唤醒，也可以通过其他进程信号或时钟中断唤醒，进入运行队列。Linux 使用TASK_INTERRUPTIBLE 宏表示此状态。

- 不可中断睡眠状态（深度睡眠状态）（TASK_UNINTERRUPTIBLE）：其和浅度睡眠基本类似，但有一点就是不可被其他进程信号或时钟中断唤醒。Linux 使用TASK_UNINTERRUPTIBLE 宏表示此状态。

- 暂停状态（TASK_STOPPED）：进程暂停执行接受某种处理。如正在接受调试的进程处于这种状态，Linux 使用TASK_STOPPED 宏表示此状态。

- 僵死状态（TASK_ZOMBIE）：进程已经结束但未释放PCB，Linux 使用TASK_ZOMBIE 宏表示此状态

- [进程生命周期与PCB（进程控制块）](https://www.cnblogs.com/mickole/p/3185889.html)

---
# cpu概述

- `%user`：Percentage of CPU utilization that occurred while executing at the user level (application). Note that this field includes time spent running virtual processors. （未标志nice值的）用户态程序的CPU占用率。

- `%nice`：Percentage of CPU utilization that occurred while executing at the user level with nice priority. 标志了nice值的用户态程序的CPU占用率。

- `%system`：Percentage of CPU utilization that occurred while executing at the system level (kernel). Note that this field includes time spent servicing hardware and software interrupts. 系统态（内核）程序的CPU占用率。

- `%iowait`：Percentage of time that the CPU or CPUs were idle during which the system had an outstanding disk I/O request. I/O等待的CPU占用率。

- `%steal`: Percentage of time spent in involuntary wait by the virtual CPU or CPUs while the hypervisor was servicing another virtual processor. 这个一般是在虚拟机中才能看到数值，比如：我的VPS供应商CPU overcommitment很严重，故我偶尔能看到%steal值有点高。

- `%idle`：Percentage of time that the CPU or CPUs were idle and the system did not have an outstanding disk I/O request. %idle越高，说明CPU越空闲。 除了上面的WIO以外的空闲情况，显示了没有本地磁盘I/O时cpu空闲或等待的时间百分比。

Linux的Load（系统负载），是一个让新手不太容易了解的概念。top/uptime等工具默认会显示1分钟、5分钟、15分钟的平均Load。具体来说，平均Load是指，在**特定的一段时间内统计的正在CPU中运行的(R状态)、正在等待CPU运行的、处于不可中断睡眠的(D状态)的任务数量的平均值**。

一般来说，对于Load的数值不要大于系统的CPU核数（或者开启了超线程，超线程也当成CPU core吧）。当然，有人觉得Load等于CPU core数量的2倍也没事，不过，我自己是在Load达到CPU core数量时，一般都会去查看下是什么具体原因导致load较高的。


- [LINUX系统的CPU使用率和LOAD](http://smilejay.com/2014/06/cpu-utilization-load-in-linux-system/)
- [10分钟教会你看懂top](https://juejin.cn/post/6844903919588491278): 比较贴切实际
- [性能分析Linux服务器CPU利用率](https://www.cnblogs.com/shengs/p/5148284.html): 除了上面的WIO以外的空闲情况，显示了没有本地磁盘I/O时cpu空闲或等待的时间百分比。

---
## cpu信息

- [cpu显示信息](https://www.cnblogs.com/yjf512/p/3383915.html): 乏善可陈

- [Linux CPU使用率含义及原理](https://www.cnblogs.com/aresxin/p/9152127.html)

Load Average: 在一段时间内，CPU正在处理以及等待CPU处理的进程数之和。 所以一般来说Load Average的数值别超过这台机器的总核数，就基本没啥问题。

## 一般场景
典型的用户态空间程序有：Shell、数据库、web服务器。

分配内存、IO操作、创建子进程……都是内核操作。这也表明，当IO操作频繁时，System参数会很高。

id: Idle time,空闲的cpu时间比。一般而言，idel + user + nice 约等于100%。


---
# IO WAIT

%iowait 是 “sar -u” 等工具检查CPU使用率时显示的一个指标，在Linux上显示为 %iowait，在有的Unix版本上显示为 %wio，含义都是一样的。这个指标常常被误读，很多人把它当作**I/O问题的征兆**，我自己每隔一段时间就会遇到对 %iowait 紧张兮兮的客户，不得不费尽唇舌反复解释。事实上这个指标所含的信息量非常少，不能单独用来判断系统有没有I/O问题。


Linux和HP-UX的man page分别从两个角度描述了这个指标：Linux着眼于I/O，强调的是仍有未完成的I/O请求；而HP-UX着眼于进程，强调的是仍有进程在等待I/O。二者所说的是同一件事的两个方面，合在一起就完整了，就是：**至少有一个I/O请求尚未完成，有进程因为等待它而休眠**。


我们不妨采纳Linux的措辞，%iowait 表示**在一个采样周期内有百分之几的时间属于以下情况：CPU空闲、并且有仍未完成的I/O请求**。


## 误解

对 %iowait 常见的误解有两个：

- 一是误以为 %iowait 表示CPU不能工作的时间
- 二是误以为 %iowait 表示I/O有瓶颈

第一种误解太低级了，%iowait 的首要条件就是CPU空闲，既然**空闲**当然就**可以接受运行任务**，只是因为没有可运行的进程，CPU才进入**空闲状态**的。那为什么没有可运行的进程呢？因为进程都处于**休眠状态**、在等待某个特定事件：比如等待定时器、或者来自网络的数据、或者键盘输入、或者等待I/O操作完成，等等。

> 关键：CPU是空闲的，因为都进程处于休眠状态

第二种误解更常见，为什么人们会认为 %iowait 偏高是**有I/O瓶颈**的迹象呢？他们的理由是：”%iowait  的第一个条件是CPU空闲，意即所有的进程都在休眠，第二个条件是仍有未完成的I/O请求，意味着进程休眠的原因是等待I/O，而 %iowait 升高则表明**因等待I/O而休眠的进程数量更多**了、或者**进程因等待I/O而休眠的时间更长**了。“ 听上去似乎很有道理，但是**不对**


![](.cpu_images/dc61497c.png)

可见，I/O并没有变化，%iowait 却升高了，原因仅仅是CPU的空闲时间增加了。请记住，系统中有成百上千的进程数，任何一个进程都可以引起CPU和I/O的变化，**因为 %iowait、%idle、%user、%system 等这些指标都是全局性的，并不是特指某个进程**。

![](.cpu_images/97ada058.png)
2个I/O使 %iowait 达到了100%，3个I/O的 %iowait 却只有50%，**显然 %iowait 的高低与I/O的多少没有必然关系，而是与I/O的并发度相关**。所以，**仅凭 %iowait 的上升不能得出I/O负载增加 的结论**。

> I/O 高低跟I/O多少没有必然关系，与I/O并发度相关

这就是为什么说 %iowait 所含的信息量非常少的原因，它是一个非常模糊的指标，如果看到 %iowait 升高，**还需检查I/O量有没有明显增加**，avserv/avwait/avque等指标有没有明显增大，应用有没有感觉变慢，**如果都没有，就没什么好担心的**。

参考链接：
- [理解 %IOWAIT (%WIO)](http://linuxperf.com/?p=33)
- [%iowait和CPU使用率的正确认知](https://www.cnblogs.com/echo1937/p/6240020.html)


---
- [重大事故！IO问题引发线上20台机器同时崩溃](https://juejin.im/post/6875176737274724366)

所谓的I/O（Input/Output）操作实际上就是输入输出的数据传输行为。程序员最关注的主要是磁盘IO和网络IO，因为这两个IO操作和应用程序的关系最直接最紧密。

磁盘IO：磁盘的输入输出，比如磁盘和内存之间的数据传输。

网络IO：不同系统间跨网络的数据传输，比如两个系统间的远程接口调用。

CPU 在等待磁盘IO操作上花费的时间占比是76.6% （上图中红框 wa）
到现在可以确定，问题肯定发生在IO等待上。利用监控系统和jstack命令，最终定位问题发生在文件写入上。**大量的磁盘读写导致了JVM线程资源耗尽（注意，不代表系统CPU耗尽）**。最终导致订单服务无法响应上游服务的请求。
> 大量的磁盘读写导致了JVM线程资源耗尽（注意，不代表系统CPU耗尽）。是jvm线程其他资源被耗尽

## IO和CPU的关系

不少攻城狮会这样理解，如果CPU空闲率是0%，就代表CPU已经在满负荷工作，没精力再处理其他任务了。真是这样的吗？

我们先看一下计算机是怎么管理磁盘IO操作的。计算机发展早期，磁盘和内存的数据传输是由CPU控制的，也就是说从磁盘读取数据到内存中，是需要CPU存储和转发的，期间CPU一直会被占用。我们知道磁盘的读写速度远远比不上CPU的运转速度。这样在传输数据时就会占用大量CPU资源，造成CPU资源严重浪费。

**后来有人设计了一个IO控制器，专门控制磁盘IO。当发生磁盘和内存间的数据传输前，CPU会给IO控制器发送指令，让IO控制器负责数据传输操作，数据传输完IO控制器再通知CPU。因此，从磁盘读取数据到内存的过程就不再需要CPU参与了，CPU可以空出来处理其他事情，大大提高了CPU利用率。这个IO控制器就是“DMA”，即直接内存访问，Direct Memory Access。现在的计算机基本都采用这种DMA模式进行数据传输。**

通过上面内容我们了解到，IO数据传输时，是不占用CPU的。当应用进程或线程发生IO等待时，CPU会及时释放相应的时间片资源并把时间片分配给其他进程或线程使用，从而使CPU资源得到充分利用。**所以，假如CPU大部分消耗在IO等待（wa）上时，即便CPU空闲率（id）是0%，也并不意味着CPU资源完全耗尽了，如果有新的任务来了，CPU仍然有精力执行任务**。

> DMA：I/O控制器。I/O等待不占用CPU。wa

在DMA模式下执行IO操作是不占用CPU的，所以CPU IO等待（上图的wa）实际上属于CPU空闲率的一部分。所以我们执行top命令时，除了要关注CPU空闲率，CPU使用率（us，sy），还要关注IO Wait（wa）。**注意，wa只代表磁盘IO Wait，不包括网络IO Wait**。

当我们用jstack查看Java线程状态时，会看到各种线程状态。当发生IO等待时（比如远程调用时），线程是什么状态呢，Blocked还是Waiting？

答案是Runnable状态，是不是有些出乎意料！实际上，**在操作系统层面Java的Runnable状态除了包括Running状态，还包括Ready（就绪状态，等待CPU调度）和IO Wait等状态**。

如上图，Runnable状态的注解明确说明了，在JVM层面执行的线程，在操作系统层面可能在等待其他资源。如果等待的资源是CPU，在操作系统层面线程就是等待被CPU调度的Ready状态；**如果等待的资源是磁盘网卡等IO资源，在操作系统层面线程就是等待IO操作完成的IO Wait状态**。

有人可能会问，为什么**Java线程没有专门的Running状态呢**？

> jvm的running状态

目前绝大部分主流操作系统都是以时间分片的方式对任务进行轮询调度，时间片通常很短，大概几十毫秒，也就是说一个线程每次在cpu上只能执行几十毫秒，然后就会被CPU调度出来变成Ready状态，等待再一次被CPU执行，**线程在Ready和Running两个状态间快速切换**。通常情况，**JVM线程状态主要为了监控使用，是给人看的。当你看到线程状态是Running的一瞬间，线程状态早已经切换N次了**。所以，再给线程专门加一个Running状态也就没什么意义了。

所以在一次网络IO读取过程中，数据并不是直接从网卡读取到用户空间中的应用程序缓冲区，而是先从网卡拷贝到内核空间缓冲区，然后再从内核拷贝到用户空间中的应用程序缓冲区。对于网络IO写入过程，过程则相反，先将数据从用户空间中的应用程序缓冲区拷贝到内核缓冲区，再从内核缓冲区把数据通过网卡发送出去。

对于磁盘文件访问的操作，可以采用线程池方式，并设置线程上线，从而避免整个JVM线程池污染，进而导致线程和CPU资源耗尽。

---
## CPU占用率不准确

发生CPU占用率不准确的原因是：在一个时钟中断周期内，发生了多次进程调度。时钟中断的精度是1/HZ秒。

top命令CPU使用率准确吗？只有在一个时钟中断周期内发生多次进程调度，才会出现CPU占用率不准的情况。

那么top命令中CPU使用率是否准确与进程调度频率有关。若HZ的值为250，则ticks值为4ms；若HZ值为1000，则ticks值为1ms。在HZ为250时，只要进程的调度间隔大于4ms，CPU占用率就准确。HZ为1000时，调度间隔大于1ms，CPU占用率计算就准确。进程调度次数少，CPU占用率就准确；调度时间间隔小于时钟中断，就可能不准确。那么进程调度的时机是怎样的？如何观察进程调度次数？

---
# nice

- [Understand what is using up “nice” CPU](https://stackoverflow.com/a/26183000)
- [What does 'nice' mean on CPU utilization graphs?](https://serverfault.com/a/116954)

On a CPU graph NICE time is time spent running processes with positive nice value (ie low priority). This means that it is consuming CPU, but will give up that CPU time for most other processes. Any USER CPU time for one of the processes listed in the above ps command will show up as NICE.

- [what-does-the-nice-value-mean-in-cpu-utilization-statistics](https://askubuntu.com/questions/399357/what-does-the-nice-value-mean-in-cpu-utilization-statistics)

> the time the CPU has spent running users' processes that have been "niced".

（摘自man top）“niced”过程是一个具有正nice值的过程。因此，如果处理器的nice值很高，这意味着它正在处理一些低优先级的进程。因此，当您看到高CPU利用率，并且您担心这种高负载会对您的系统产生不良影响时，此指示器非常有用：

高CPU利用率和高nice值：没什么好担心的，没有那么重要的任务做他们的工作，重要的进程将很容易得到CPU时间，如果他们需要的话。这种情况并不是真正的瓶颈。

高CPU利用率和低nice值：有点担心，因为CPU有重要的进程，所以这些或新的进程将不得不等待。这种情况是一个真正的瓶颈。

---
## 进程优先级、进程nice值和%nice的解释
- [进程优先级，进程nice值和%nice的解释](https://blog.csdn.net/longdel/article/details/7317511): 概念

PRI ：进程优先权，代表这个进程可被执行的优先级，其值越小，优先级就越高，越早被执行

NI ：进程Nice值，代表这个进程的优先值

%nice ：改变过优先级的进程的占用CPU的百分比


PRI是比较好理解的，即进程的优先级，或者通俗点说就是程序被CPU执行的先后顺序，此值越小进程的优先级别越高。那NI呢？就是我们所要说的nice值了，其表示进程可被执行的优先级的修正数值。如前面所说，PRI值越小越快被执行，那么加入nice值后，将会使得PRI变为：PRI(new)=PRI(old)+nice。由此看出，PR是根据NICE排序的，规则是NICE越小PR越前（小，优先权更大），即其优先级会变高，则其越快被执行。如果NICE相同则进程uid是root的优先权更大。

在LINUX系统中，Nice值的范围从-20到+19（不同系统的值范围是不一样的），正值表示低优先级，负值表示高优先级，值为零则表示不会调整该进程的优先级。具有最高优先级的程序，其nice值最低，所以在LINUX系统中，值-20使得一项任务变得非常重要；与之相反，如果任务的nice为+19，则表示它是一个高尚的、无私的任务，允许所有其他任务比自己享有宝贵的CPU时间的更大使用份额，这也就是nice的名称的来意。

进程在创建时被赋予不同的优先级值，而如前面所说，nice的值是表示进程优先级值可被修正数据值，因此，每个进程都在其计划执行时被赋予一个nice值，这样系统就可以根据系统的资源以及具体进程的各类资源消耗情况，主动干预进程的优先级值。在通常情况下，子进程会继承父进程的nice值，比如在系统启动的过程中，init进程会被赋予0，其他所有进程继承了这个nice值（因为其他进程都是init的子进程）。

对nice值一个形象比喻，假设在一个CPU轮转中，有2个runnable的进程A和B，如果他们的nice值都为0，假设内核会给他们每人分配1k个cpu时间片。但是假设进程A的为0，但是B的值为-10，那么此时CPU可能分别给A和B分配1k和1.5k的时间片。故可以形象的理解为，nice的值影响了内核分配给进程的cpu时间片的多少，时间片越多的进程，其优先级越高，其优先级值（PRI）越低。%nice，就是改变过优先级的进程的占用CPU的百分比，如上例中就是**0.5k/2.5k=1/5=20%**。

> 上面的例子比较深刻

## nice很高问题

- [嵌入式top nice很高问题](https://blog.csdn.net/heliangbin87/article/details/88052356)
> 这个例子值得参考

%nic：表示修改优先级的进程占CPU的百分比，**很高说明不停的有进程切换优先级**。

**发现相应进程一直死循环执行，没有主动退出机制，导致内核不停动态调整优先级，以便其他进程得以运行。**

解决方法：

只要增加一个休眠机制即可解决问题。

- [一个php进程cpu %nice很高的原因详解](https://www.aikaiyuan.com/8698.html)

三、 判断问题：
1、 NICE资源一般是用户端控制的行为产生；
2、 除非程序中有大量的使用sleep，或者是调用了nice等函数，对自定义了优先级别，但一般程序不会这么变态；

> nice值高，可以说是改变过优先级的进程的占用CPU百分比。一般高，说明不停的有进程切换优先级。

