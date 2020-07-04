- [prometheus-book](https://yunlzheng.gitbook.io/prometheus-book/)
- [prometheus-in-action](https://www.aneasystone.com/archives/2018/11/prometheus-in-action.html)

## 基本原理
Prometheus的基本原理是通过HTTP协议周期性抓取被监控组件的状态，任意组件只要提供对应的HTTP接口就可以接入监控。不需要任何SDK或者其他的集成过程。这样做非常适合做虚拟化环境监控系统，比如VM、Docker、Kubernetes等。输出被监控组件信息的HTTP接口被叫做exporter 。目前互联网公司常用的组件大部分都有exporter可以直接使用，比如Varnish、Haproxy、Nginx、MySQL、Linux系统信息(包括磁盘、内存、CPU、网络等等)。

## 服务过程

- Prometheus Daemon负责定时去目标上抓取metrics(指标)数据，每个抓取目标需要暴露一个http服务的接口给它定时抓取。Prometheus支持通过配置文件、文本文件、Zookeeper、Consul、DNS SRV Lookup等方式**指定抓取目标**。Prometheus采用**PULL的方式进行监控**，即服务器可以直接通过目标PULL数据或者间接地通过**中间网关来Push数据**。

- Prometheus在本地存储抓取的所有数据，并通过一定规则进行清理和整理数据，并把得到的结果存储到新的时间序列中。

- Prometheus通过PromQL和其他API可视化地展示收集的数据。Prometheus支持很多方式的图表可视化，例如Grafana、自带的Promdash以及自身提供的模版引擎等等。Prometheus还提供HTTP API的查询方式，自定义所需要的输出。

- PushGateway支持Client主动推送metrics到PushGateway，而Prometheus只是定时去Gateway上抓取数据。

- Alertmanager是独立于Prometheus的一个组件，可以支持Prometheus的查询语句，提供十分灵活的报警方式。


## 三大套件

- Server 主要负责数据采集和存储，提供PromQL查询语言的支持。
- Alertmanager 警告管理器，用来进行报警。
- Push Gateway 支持临时性Job主动推送指标的中间网关。

## 数据模型
虽然 Prometheus 里存储的数据都是 float64 的一个数值，但如果我们按类型来分，可以把 Prometheus 的数据分成四大类：

- Counter
- Gauge
- Histogram
- Summary

Counter 用于计数，例如：请求次数、任务完成数、错误发生次数，这个值会一直增加，不会减少。

Gauge 就是一般的数值，可大可小，例如：温度变化、内存使用变化。

Histogram 是直方图，或称为柱状图，常用于跟踪事件发生的规模，例如：请求耗时、响应大小。它特别之处是可以对记录的内容进行分组，提供 count 和 sum 的功能。

Summary 和 Histogram 十分相似，也用于跟踪事件发生的规模，不同之处是，它提供了一个 quantiles 的功能，可以按百分比划分跟踪的结果。例如：quantile 取值 0.95，表示取采样值里面的 95% 数据。

更多信息可以参考官网文档 Metric types，Summary 和 Histogram 的概念比较容易混淆，属于比较高阶的指标类型，可以参考 Histograms and summaries 这里的说明。
