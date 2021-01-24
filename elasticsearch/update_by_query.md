
# update_by_query

提起es的Update By Query很多人一定也不陌生，它对应的就是关系型数据库的update set ... where...语句，这对应一般的存储引擎而言算是最基本的功能，但它的坑确不少，多到让你使用起来很奔溃，比如**批量更新时非事务模式执行（允许部分成功部分失败）、大批量操作会超时、频繁更新会报错（版本冲突）、脚本执行太频繁时又会触发断路器等**。


#### 1. 非事务模式执行

在前面update_by_query相关文章也大概讲过，所有更新和查询失败都会导致_update_by_query中止，并在响应失败时返回。已执行的更新仍然存在。换句话说，该过程不会回滚，只会中止。

#### 2. java.io.IOException: listener timeout

在前面的文章中也讲过，默认是30000ms，但补充一点：修改超时时间并非真正的解决方案。

#### 3. VersionConflictEngineException

由于es是准实时的，默认refresh_interval: "1s"，_update_by_query在索引启动时获取索引的快照，这意味着**如果文档在拍摄快照的时间和处理索引请求之间发生更改，则会出现版本冲突**。说白了，1s内多次修改同一个document就会发生，你通过设置version_conflicts=false（会忽略错误），但并未解决问题啊，当然了，你还能有2中方式解决该问题：

retries，一直重试，UpdateByQueryRequestBuilder中默认为11次，可见对es是有一定的压力的
refresh=true，一直去刷盘，当然可以解决准实时的问题，但磁盘消耗是很多的
#### 4. IllegalArgumentException: failed to execute script

Too many dynamic script compilations within, max: [75/5m]，看意思就懂，script修改语句只能接受5分钟内75次，what？具体可参与官方script-compilation-circuit-breaker，怎么滴也得配置个十几万次吧。
> 需要提前通过put _script 编译好

总结，使用Update By Query要重点关注上面的4个问题，特别是涉及到大批量的修改，特别要关注监控信息（`GET _tasks?detailed=true&actions=*byquery`），个人建议要限流，比如：可通过前置mongodb（定时定量去更新）或者**更新失败后记录到新的index中后续定时定量去补偿**。

- [关于ElasticSearch的Update By Query的那些著名的坑](https://blog.csdn.net/alex_xfboy/article/details/99715217

---
> 记录之前的思考

## 单文档更新

单进程，update某个文档不会有冲突。

多进程，update同个文档会是怎么样的情况（前提：refresh_interval是很大的情况下）：
A进程拿取但文档并更新到内存之后，B进程再更新，应该是没有问题的？也就是交叉更新。因为B进程更新拿到的是内存的文档？而不是search的文档？或者单文档的更新是能获取到最新的。

A、B进程同步并发处理：A、B的更新线程同时拿到同一个版本的文档，会发生冲突？加上重试后就好，如果不断有更新的任务，即使重试也会一样发送冲突。

## 搜索更新

多进程搜索更新：refresh_interval内拿到的都是旧数据，A进程更新后，B进程的更新操作能拿到A更新后的版本？所以会很容易发生冲突？这样重试有作用吗？还是说冲突后，会刷新冲突的数据？待测试
