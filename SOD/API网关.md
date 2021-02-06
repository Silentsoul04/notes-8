首先，Service Mesh 和 API Gateway 在功能定位和承担的职责上有非常清晰的界限：

- Service Mesh：微服务的网络通信基础设施，负责（系统内部的）服务间的通讯；
- API Gateway：负责将服务以 API 的形式暴露（给系统外部），以实现业务功能。

![](.API网关_images/d18cbdc1.png)

从功能和职责上说：

- 位于最底层的是拆分好的原子微服务，以服务的形式提供各种能力；
- 在原子微服务上是（可选的）组合服务，某些场景下需要将若干微服务的能力组合起来形成新的服务；
- 原子微服务和组合服务部署于 系统内部，在采用 Service Mesh 的情况下，由 Service Mesh 提供服务间通讯的能力；
- API Gateway 用于将系统内部的这些服务暴露给 系统外部，以 API 的形式接受外部请求。

从部署上说：

- Service Mesh 部署在系统内部：因为原子微服务和组合服务通常不会直接暴露给外部系统；
- API Gateway 部署在系统的边缘：一方面暴露在系统之外，对外提供 API 供外部系统访问；一方面部署在系统内部，以访问内部的各种服务。

术语：
- 东西向通讯：指服务间的相互访问，其通讯流量在服务间流转，流量都位于系统内部；
- 南北向通讯：指服务对外部提供访问，通常是通过 API Gateway 提供的 API 对外部保罗，其通讯流量是从系统外部进入系统内部。

所以，API Gateway 作为一个客户端访问内部服务时，到底算南北向还是东西向，就成为一个哲学问题：完全取决于我们如何看待 API Gateway ，是作为一个整体，还是逻辑上分拆为对内对外两个部分。

这个哲学问题并非无厘头，在 API Gateway 的各种产品中，关于如何实现 “API Gateway 作为一个客户端访问内部服务” ，就通常分成两个流派：

- 泾渭分明：视 API Gateway 和内部服务为两个独立事物，API Gateway 访问内部服务的通讯机制自行实现，独立于服务间通讯的机制；
- 兼容并济：视 API Gateway 为一个普通的内部服务的客户端，重用其内部服务间通讯的机制。

而最终决策通常也和产品的定位有关：如果希望维持 API Gateway 的独立产品定位，希望可以在不同的服务间通讯方案下都可以使用，则通常选择前者，典型如 Kong；如果和服务间通讯方案有非常深的渊源，则通常选择后者，典型如 Spring Cloud 生态下的 Zuul 和 Spring Cloud Gateway。

但无论选择哪个流派，都改变不了一个事实，当 “API Gateway 作为一个客户端访问内部服务” 时，它的确和一个普通内部服务作为客户端去访问其他服务没有本质差异：服务发现、负载均衡、流量路由、熔断、限流、服务降级、故障注入、日志、监控、链路追踪、访问控制、加密、身份认证…… 当我们把网关访问内部服务的功能一一列出来时，发现几乎所有的这些功能都是和服务间调用重复。

答案不重要。

如何融合东西向和南北向的通讯方案？

其中的一个做法就是基于 Service Mesh 的 Sidecar 来实现 API Gateway，从而在南北向通讯中引入 Service Mesh 这种东西向通讯的方案。

API Gateway 这次真的可以分拆为两个独立部署的物理实体，而不是逻辑上的两个部分：

- API Gateway 本体：实现 API Gateway 除了访问内部服务之外的功能；
- Sidecar：按照 Service Mesh 的标准做法， 我们视 API Gateway 为一个部署于 Service Mesh 中的普通服务，为这个服务 1:1 的部署 Sidecar。

解决“多一跳”问题的方法简单而粗暴，基于 Sidecar，将 API Gateway 的功能加进来。这样 API Gateway 本体和 Sidecar 再次合二为一

![](.API网关_images/1caaef6d.png)

BFF（Backend For Frontend）的引入会让 Service Mesh 和 API Gateway 走到一个更加亲密的地步。BFF 完全收口外部流量.
![](.API网关_images/d3251c1a.png)


## 参考链接:
- [Service Mesh 和 API Gateway 关系深度探讨](https://mp.weixin.qq.com/s/zhJ3koaApEOVfdyyXuAGUQ)

---
- [如何为服务网格选择入口网关？](https://zhaohuabing.com/post/2019-03-29-how-to-choose-ingress-for-service-mesh/): 介绍了内部服务间的通信(Cluster IP、Istio Sidecar Proxy)的优缺点。如何从外部网络访问， 如何为服务网格选择入口网关？。介绍包括Pod、Service、NodePort、LoadBalancer、Ingress、Gateway、VirtualService等，最后采用API Gateway + Sidecar Proxy作为服务网格的流量入口还不能很好理解。
