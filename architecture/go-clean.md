# 简洁架构

标签（空格分隔）： 未分类

---
Repository use case 架构



[在 Golang 中尝试简洁架构](https://studygolang.com/articles/12909?fr=sidebar)：

## 模型层（ Models ）

与实体（ Entities ）一样，模型会在每一层中使用，在这一层中将存储对象的结构和它的方法。例如： Article， Student， Book。

## 仓库层（ Repository ）

仓库将存放所有的数据库处理器，查询，创建或插入数据库的处理器将存放在这一层，该层仅对数据库执行 CRUD 操作。该层**没有业务流程**。只有操作数据库的普通函数。

这层也负责选择应用中将要使用什么样的数据库。 可以是 Mysql， MongoDB， MariaDB，Postgresql，无论使用哪种数据库，都要在这层决定。

如果使用 ORM， 这层将控制输入，并与 ORM 服务对接。

如果调用微服务， 也将在这层进行处理。创建 HTTP 请求去请求其他服务并清理数据，这层必须完全充当仓库。 处理所有的数据输入，输出，并且**没有特定的逻辑交互**。

该仓库层（ Repository ）将依赖于连接数据库 或其他微服务（如果存在的话）

---

## 用例层（ Usecase ）
这层将会扮演业务流程处理器的角色。任何流程都将在这里处理。该层将决定哪个仓库层被使用。并且负责提供数据给服务以便交付。处理数据进行计算或者在这里完成任何事。

用例层将接收来自传递层的所有经过处理的输入，然后将处理的输入存储到数据库中， 或者从数据库中获取数据等。

用例层将依赖于仓库层。

## 表现层（ Delivery ）
这一层将作为表现者。决定数据如何呈现。任何传递类型都可以作为是 REST API， 或者是 HTML 文件，或者是 gRPC

这一层将**接收**来自用户的输入， 并**清理数据**然后**传递**给用例层。


---
参考链接：
https://zhuanlan.zhihu.com/p/20001838
https://www.jianshu.com/p/66e749e19f0d
https://www.xiayinchang.top/2018/09/17/Go%E6%95%B4%E6%B4%81%E6%9E%B6%E6%9E%84/

https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html

https://fernandocejas.com/2014/09/03/architecting-android-the-clean-way/
https://manuel.kiessling.net/2012/09/28/applying-the-clean-architecture-to-go-applications/
