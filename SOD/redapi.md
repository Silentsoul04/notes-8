-----
# 如何发布新的接口

- 更改redash的名称，引起调用的问题，调用用的是redash的标题

- 添加新的参数，兼容旧的情况。

- 同样的名称，更改了逻辑，如何发布。就应该是新的接口了。


我觉得应该是要新开接口，server不需要做默认参数的控制。新的client根据新的接口渲染好默认参数，并引去新的接口。旧的接口还保留着，等所有引用了client的项目更新到最新才可以去掉。client这个要处理好接口版本升级，名字要一致的问题。

----


好处：
- 方便测试
- 快速提供数据的能力
- 方便维护，所有查表都是在同一处地方，方便后续改策略、算法的时候能统一更改
- 对调用屏蔽了相关的底层数据库，数据相关遇到性能问题，能够在底层灵活调整相关存储策略。

后续：缓存策略的姿势、根据redash生成相关的文档、权限控制、更改后的自动化测试。


-----
# query_conf.go

提供查询配置信息QueryConfProvider

QueryConf类：数据库查询结果。查询语句、数据源等

---
GetQueryConf基类：实现各种获取请求模板和数据源的类，

DbQueryConfProvider类，DSN、Query、ReloadInterval。

通过定时器触发数据库查询进行更新。定时调用srv.loadQueries(ctx)方法，该方法通过查询数据库得到QueryConf类的结果。以进行各个数据源的数据库连接初始化，保存在srv.selectors属性里。并将各个查询实例成Query，放到srv.qs属性列表里。

MapQueryConfProvider类，提供内存字典缓存的查询模板，当数据源存在的时候替换。

---
Query类：QueryConf、Srv、Selector、ps（用于拼SQL的参数）


好绕啊！类嵌套类的作为属性。


context使用？