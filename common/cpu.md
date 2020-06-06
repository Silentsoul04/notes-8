

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

- 运行状态（TASK_RUNNING）：是运行态和就绪态的合并，表示进程正在运行或准备运行，Linux 中使用TASK_RUNNING 宏表示此状态

- 可中断睡眠状态（浅度睡眠）（TASK_INTERRUPTIBLE）：进程正在睡眠（被阻塞），等待资源到来是唤醒，也可以通过其他进程信号或时钟中断唤醒，进入运行队列。Linux 使用TASK_INTERRUPTIBLE 宏表示此状态。

- 不可中断睡眠状态（深度睡眠状态）（TASK_UNINTERRUPTIBLE）：其和浅度睡眠基本类似，但有一点就是不可被其他进程信号或时钟中断唤醒。Linux 使用TASK_UNINTERRUPTIBLE 宏表示此状态。

- 暂停状态（TASK_STOPPED）：进程暂停执行接受某种处理。如正在接受调试的进程处于这种状态，Linux 使用TASK_STOPPED 宏表示此状态。

- 僵死状态（TASK_ZOMBIE）：进程已经结束但未释放PCB，Linux 使用TASK_ZOMBIE 宏表示此状态

- [进程生命周期与PCB（进程控制块）](https://www.cnblogs.com/mickole/p/3185889.html)

---
# cpu

- `%user`：Percentage of CPU utilization that occurred while executing at the user level (application). Note that this field includes time spent running virtual processors. （未标志nice值的）用户态程序的CPU占用率。

- `%nice`：Percentage of CPU utilization that occurred while executing at the user level with nice priority. 标志了nice值的用户态程序的CPU占用率。

- `%system`：Percentage of CPU utilization that occurred while executing at the system level (kernel). Note that this field includes time spent servicing hardware and software interrupts. 系统态（内核）程序的CPU占用率。

- `%iowait`：Percentage of time that the CPU or CPUs were idle during which the system had an outstanding disk I/O request. I/O等待的CPU占用率。

- `%idle`：Percentage of time that the CPU or CPUs were idle and the system did not have an outstanding disk I/O request. %idle越高，说明CPU越空闲。

Linux的Load（系统负载），是一个让新手不太容易了解的概念。top/uptime等工具默认会显示1分钟、5分钟、15分钟的平均Load。具体来说，平均Load是指，在特定的一段时间内统计的正在CPU中运行的(R状态)、正在等待CPU运行的、处于不可中断睡眠的(D状态)的任务数量的平均值。

一般来说，对于Load的数值不要大于系统的CPU核数（或者开启了超线程，超线程也当成CPU core吧）。当然，有人觉得Load等于CPU core数量的2倍也没事，不过，我自己是在Load达到CPU core数量时，一般都会去查看下是什么具体原因导致load较高的。


- [LINUX系统的CPU使用率和LOAD](http://smilejay.com/2014/06/cpu-utilization-load-in-linux-system/)

---
# IO WAIT

%iowait 是 “sar -u” 等工具检查CPU使用率时显示的一个指标，在Linux上显示为 %iowait，在有的Unix版本上显示为 %wio，含义都是一样的。这个指标常常被误读，很多人把它当作**I/O问题的征兆**，我自己每隔一段时间就会遇到对 %iowait 紧张兮兮的客户，不得不费尽唇舌反复解释。事实上这个指标所含的信息量非常少，不能单独用来判断系统有没有I/O问题。


Linux和HP-UX的man page分别从两个角度描述了这个指标：Linux着眼于I/O，强调的是仍有未完成的I/O请求；而HP-UX着眼于进程，强调的是仍有进程在等待I/O。二者所说的是同一件事的两个方面，合在一起就完整了，就是：至少有一个I/O请求尚未完成，有进程因为等待它而休眠。


我们不妨采纳Linux的措辞，%iowait 表示在一个采样周期内有百分之几的时间属于以下情况：**CPU空闲、并且有仍未完成的I/O请求**。


## 误解

对 %iowait 常见的误解有两个：

- 一是误以为 %iowait 表示CPU不能工作的时间
- 二是误以为 %iowait 表示I/O有瓶颈

第一种误解太低级了，%iowait 的首要条件就是CPU空闲，既然**空闲**当然就**可以接受运行任务**，只是因为没有可运行的进程，CPU才进入**空闲状态**的。那为什么没有可运行的进程呢？因为进程都处于**休眠状态**、在等待某个特定事件：比如等待定时器、或者来自网络的数据、或者键盘输入、或者等待I/O操作完成，等等。

第二种误解更常见，为什么人们会认为 %iowait 偏高是**有I/O瓶颈**的迹象呢？他们的理由是：”%iowait  的第一个条件是CPU空闲，意即所有的进程都在休眠，第二个条件是仍有未完成的I/O请求，意味着进程休眠的原因是等待I/O，而 %iowait 升高则表明**因等待I/O而休眠的进程数量更多**了、或者**进程因等待I/O而休眠的时间更长**了。“ 听上去似乎很有道理，但是**不对**


![](.cpu_images/dc61497c.png)

可见，I/O并没有变化，%iowait 却升高了，原因仅仅是CPU的空闲时间增加了。请记住，系统中有成百上千的进程数，任何一个进程都可以引起CPU和I/O的变化，因为 %iowait、%idle、%user、%system 等这些指标都是全局性的，并不是特指某个进程。

![](.cpu_images/97ada058.png)
2个I/O使 %iowait 达到了100%，3个I/O的 %iowait 却只有50%，显然 %iowait 的高低与I/O的多少没有必然关系，而是与I/O的并发度相关。所以，仅凭 %iowait 的上升不能得出I/O负载增加 的结论。

这就是为什么说 %iowait 所含的信息量非常少的原因，它是一个非常模糊的指标，如果看到 %iowait 升高，还需检查I/O量有没有明显增加，avserv/avwait/avque等指标有没有明显增大，应用有没有感觉变慢，如果都没有，就没什么好担心的。

参考链接：
- [理解 %IOWAIT (%WIO)](http://linuxperf.com/?p=33)
- [%iowait和CPU使用率的正确认知](https://www.cnblogs.com/echo1937/p/6240020.html)