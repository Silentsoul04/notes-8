---
# 跨域请求

在 HTML 中，`<a>, <form>, <img>, <script>, <iframe>, <link>` 等标签以及 Ajax 都可以指向一个资源地址，而所谓的跨域请求就是指：当前发起请求的域与该请求指向的资源所在的域不一样。这里的域指的是这样的一个概念：我们认为若协议 + 域名 + 端口号均相同，那么就是同域。

链接：　
- [什么是跨域请求以及实现跨域的方案](https://www.jianshu.com/p/f880878c1398)

## 为什么form表单提交没有跨域问题，但ajax提交有跨域问题？
因为原页面用 form 提交到另一个域名之后，原页面的脚本无法获取新页面中的内容。所以浏览器认为这是安全的。而 AJAX 是可以读取响应内容的，因此浏览器不能允许你这样做。如果你细心的话你会发现，其实请求已经发送出去了，你只是拿不到响应而已。所以浏览器这个策略的本质是，一个域名的 JS ，在未经允许的情况下，不得读取另一个域名的内容。但浏览器并不阻止你向另一个域名发送请求。

作者：方应杭
链接：https://www.zhihu.com/question/31592553/answer/190789780
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

---
# CORS和JSONP

参考链接: 

- [什么是跨域请求以及实现跨域的方案](https://www.jianshu.com/p/f880878c1398)
- [详解js跨域问题](https://segmentfault.com/a/1190000000718840)

## CORS

跨源资源共享 Cross-Origin Resource Sharing(CORS) 是一个新的 W3C 标准，它新增的一组HTTP首部字段，允许服务端其声明哪些源站有权限访问哪些资源。换言之，它允许浏览器向声明了 CORS 的跨域服务器，发出 XMLHttpReuest 请求，从而克服 Ajax 只能同源使用的限制。

## JSONP的优缺点

JSONP的优点是：它不像XMLHttpRequest对象实现的Ajax请求那样受到同源策略的限制；它的兼容性更好，在更加古老的浏览器中都可以运行，不需要XMLHttpRequest或ActiveX的支持；并且在请求完毕后可以通过调用callback的方式回传结果。

JSONP的缺点则是：它只支持GET请求而不支持PO  ST等其它类型的HTTP请求；它只支持跨域HTTP请求这种情况，不能解决不同域的两个页面之间如何进行JavaScript调用的问题。

## CORS和JSONP对比

CORS与JSONP相比，无疑更为先进、方便和可靠。

    1、 JSONP只能实现GET请求，而CORS支持所有类型的HTTP请求。

    2、 使用CORS，开发者可以使用普通的XMLHttpRequest发起请求和获得数据，比起JSONP有更好的错误处理。

    3、 JSONP主要被老的浏览器支持，它们往往不支持CORS，而绝大多数现代浏览器都已经支持了CORS）。

---
## cookie
Domain=<domain-value> 可选
指定 cookie 可以送达的主机名。假如没有指定，那么默认值为当前文档访问地址中的主机部分（但是不包含子域名）。与之前的规范不同的是，*域名之前的点号会被忽略* 。假如指定了域名，那么相当于各个子域名也包含在内了。

注意： 不指定域名的时候，是不包含子域名的。删除也需要不指定域名才能删除。只要是指定域名的，有没有点号都会被忽略，相当于包含子域名.

注意： django的删除域名只能删除同名设置多个的一个，可以通过改key值来进行修改

---
## 跨域请求带上cookie

cookie无法设置除当前域名或者其父域名之外的其他domain.

cookie的作用域是domain本身以及domain下的所有子域名

基于安全方面的考虑，在浏览器中无法获取跨域的 Cookie 这一点时永远不变的。但是我们处理跨域请求时有可能会遇到这样的情况：一个网页与域为bbb.cn的服务器正常发送请求和接收响应，同时这个网页也需要跨域访问aaa.cn服务器。

众所周知，浏览器会在准备发送的请求中附上所有符合要求的Cookie，故在上面的情况中浏览器会自动处理网页与域为bbb.cn的服务器之间的 Cookie；但是在 CORS 跨域中，浏览器并不会自动发送 Cookie，也就是说，浏览器不会处理网页与aaa.cn服务器之间的 Cookie。
配置说明
要想浏览器处理 CORS 跨域中的 Cookie 只需要分别在网页以及服务端作出一点点改变：


网页端中，对于跨域的 XMLHttpRequest 请求，需要设置withCredentials 属性为 true。
```
var xhr = new XMLHttpRequest();
xhr.open("GET", "http://aaa.cn/localserver/api/corsTest");
xhr.withCredentials = true; // 设置跨域 Cookie
xhr.send();
```

同时服务端的响应中必须携带 Access-Control-Allow-Credentials: true 首部。如果服务端的响应中未携带Access-Control-Allow-Credentials: true 首部，浏览器将不会把响应的内容返回给发送者。

要想设置和获取跨域 Cookie，上面提到的两点缺一不可。另外有一点需要注意的是：规范中提到，如果 XMLHttpRequest 请求设置了withCredentials 属性，那么服务器不得设置 Access-Control-Allow-Origin的值为* ，否则浏览器将会抛出The value of the 'Access-Control-Allow-Origin' header in the response must not be the wildcard '*' 错误。

- 链接：https://www.jianshu.com/p/13d53acc124f

1. 1.ag.cn 请求auth.ag.cn token接口，后端把cookie set 到 ag.cn
2. 新开页面 2.ag.cn ，可以通过document.cookie拿到 ag.cn的 cookie信息；

如果set cookie的时候，set到auth.ag.cn , 那么在 2.ag.cn 就拿不到了；

可以拿到父级域名的cookie，拿不到兄弟域名的cookie

---
## restful

### patch
patch方法用来更新局部资源，这句话我们该如何理解？

假设我们有一个UserInfo，里面有userId， userName， userGender等10个字段。可你的编辑功能因为需求，在某个特别的页面里只能修改userName，这时候的更新怎么做？

人们通常(为徒省事)把一个包含了修改后userName的完整userInfo对象传给后端，做完整更新。但仔细想想，这种做法感觉有点二，而且真心浪费带宽(纯技术上讲，你不关心带宽那是你土豪)。

于是patch诞生，只传一个userName到指定资源去，表示该请求是一个局部更新，后端仅更新接收到的字段。

### put
而put虽然也是更新资源，但要求前端提供的一定是一个完整的资源对象，理论上说，如果你用了put，但却没有提供完整的UserInfo，那么缺了的那些字段应该被清空

> 最后再补充一句，restful只是标准，标准的意思是如果在大家都依此行事的话，沟通成本会很低，开发效率就高。但并非强制(也没人强制得了)，所以你说在你的程序里把方法名从put改成patch没有任何影响，那是自然，因为你的后端程序并没有按照标准对两个方法做不同处理，她的表现自然是一样的

---
## pid
在Linux/Unix下，很多程序比如nginx会启动多个进程，而发信号的时候需要知道要向哪个进程发信号。不同的进程有不同的pid（process id）。将pid写进文件可以使得在发信号时比较简单。

(1) pid文件的内容：pid文件为文本文件，内容只有一行, 记录了该进程的ID。用cat命令可以看到。(2) pid文件的作用：防止进程启动多个副本。只有获得pid文件(固定路径固定文件名)写入权限(F_WRLCK)的进程才能正常启动并把自身的PID写入该文件中。其它同一个程序的多余进程则自动退出。

---
# CGI

于是Web服务器可以解析这个HTTP请求，然后把这个请求的各种参数写进进程的环境变量，比如REQUEST_METHOD，PATH_INFO之类的。之后呢，服务器会调用相应的程序来处理这个请求，这个程序也就是我们所要写的CGI程序了。它会负责生成动态内容，然后返回给服务器，再由服务器转交给客户端。服务器和CGI程序之间通信，一般是通过进程的环境变量和管道。


WSGI是一种Web服务器网关接口。它是一个Web服务器（如nginx，uWSGI等服务器）与web应用（如用Flask框架写的程序）通信的一种规范。

uWSGI是一个Web服务器，它实现了WSGI协议、uwsgi、http等协议。Nginx中HttpUwsgiModule的作用是与uWSGI服务器进行交换。
要注意 WSGI / uwsgi / uWSGI 这三个概念的区分。
WSGI看过前面小节的同学很清楚了，是一种通信协议。
uwsgi是一种线路协议而不是通信协议，在此常用于在uWSGI服务器与其他网络服务器的数据通信。
而uWSGI是实现了uwsgi和WSGI两种协议的Web服务器。
uwsgi协议是一个uWSGI服务器自有的协议，它用于定义传输信息的类型（type of information），每一个uwsgi packet前4byte为传输信息类型描述，它与WSGI相比是两样东西。


---
# web 模型

https://www.v2ex.com/t/347421#r_4135228

说下我对这 python 这几种 web 模型的理解吧： 

首先是 http server + wsgi server(container) + wsgi application 这种传统模型吧： 
http server 指的是类似于 nginx 或 apache 的服务 
wsgi server 指的是类似 gunicorn 和 uwsgi 这样的服务 
wsgi application 指的是 flask django 这样的基于 wsgi 接口的框架运行起来的实例 
最初这种模型只是为了方便 web 框架的开发者，不需要每个框架层面都去实现一遍 http server ，就增加了一个 WSGI 中间层协议，框架只要实现这个协议的客户端就可以，然后用 wsgi server 去实现 http 协议的解析并去调用客户端(wsgi application)。 

为了方便开发，每个框架都内置了一个简易的 wsgi server ，为什么还要用专门的 wsgi server 呢？ 
wsgi 除了解析 http 协议以及 http 端口侦听外，还负责了流量转发以及 wsgi application 进程管理的功能。一般 wsgi 框架内置的 wsgi server 都是一个单进程，一次只能处理一个请求。而目的通用的 wsgi server(gunicorn, uwsgi)都至少支持 pre fork 模型，这种模型会起一个 master 来侦听请求，并启动多个 slave(每个 slave 是一个 wsgi application)， master 负责把请求转发到空闲的 slave 上。除了这种传统的基于进程的 pre fork 同步模型，不同的 wsgi server 也会支持一些其它模型，有基于线程的同步模型，也有基于 asyncio 的异步模型。 

这种模型下怎样写异步代码呢？ 
1. 直接用传统的异步编程(进程，线程，协程)，虽然有些 wsgi server 支持 asynio 模型，但是这也需要用户所写的代码做相应的支持。这就导致了如果我们在 wsgi application 的时候不能随便使用线程和异步 IO ，如果用了就需要配置 wsgi server 使其支持我们自己的写法。因此为了使得我们缩写的 application 能部署在任意的 wsgi server(container)中，我们就只能写同步代码了。 
2. 使用分布式异步编程，使用类似 celery 的方式，将需要异步处理的东西发送到 worker 去处理。 

既然有了 wsgi server ，为什么还要有一个 http server 呢？ 
主要是因为 wsgi server 支持的并发量比较低，一般会用一个专门的 http server 来做一层缓冲，避免并发量过大时直接服务挂掉。 


python 传统的这种 wsgi 模型，主要是为了方便框架开发者只需要专注框架层面，而非 http 处理层面。但这样却增加了服务部署的复杂度，需要同时部署和配置 http server 和 wsgi server ，如果想支持异步还要部署 worker ，而使用 tornado 或 go 开发的应用因为自己实现了高效 http 处理的应用只需要部署自己就可以了。 


接下来是 tornado 和 twisted 这种模型： 
这种模型和上面的传统模型处于一个时期，这种模型和 nodejs 差不多，都是基于回调的模型，适用于高 IO 低 CPU 的场景。这种模型自己实现了一个基于回调 http server(event loop)，每一个请求都被注册成一个异步函数来处理，然后主循环来不断的循环这些函数。这样就和 pre fork 模型有了区别， pre fork 模型中每一个 slave 都是一个 wsgi application ，一个 wsgi application 都只能处理一个请求，而回调模型只有一个线程，不仅极大的减少了内存的分配还减小了进城以及线程间的切换开销，从而可以支持高 IO 并发。但是这种模型也有很明显的缺点，就是一旦应用程序有大量的 CPU 计算，就会让这个线程堵住，所有的请求都会收到影响，如果应用在处理一个请求时崩溃，所有的请求也都会收到影响。 


接下来时 aiohttp/sanic 这种模型： 
这种模型和 tornada 模型的改进，但实质上是一样的，因为回调的写法不易读也容易出错，于是将回调的写法改成了同步的写法。这种模型和 koa2 和 go net/http 查不多， asyncio 提供了类似 go coroutine 的功能和写法，而 aiohttp 则提供了类似 go 中的 net/http 的 http 处理库。

---
# 网络请求

### 背景
将通用版的请求接口，服务化后，因为请求变多了，每次请求通用版数据的接口都需要请求auth进行用户校验，而且走的是nginx层的https、uwsgi的sock解析，并且也要经过反爬虫的计算。

### 解决办法
uwsgi的sock需要nginx才能解析，uwsgi直接启动监听端口。减少nginx和反爬虫的解析后观察情况

---
# 缓存失效问题
比如我们现在拥有这么一个集群，集群里面有个缓存服务，集群中每个程序都会用到这个缓存，如果此时缓存中有一项缓存过期了，在大并发环境下，同一时刻中许许多多的服务都过来访问缓存，获取缓存中的数据，发现缓存过期，就要再去数据库取，然后更新到缓存服务中去。但是其实我们仅仅只需要一个请求过来数据库去更新缓存即可，然后这个场景，我们该怎么去做

作者：说出你的愿望吧丷
链接：https://juejin.im/post/5d113660e51d45773d468640
来源：掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

1. 主动刷新缓存？失效前的一段时间去主动查询替换

2. 分布式锁

---
# 微服务如何处理分布式事务？

两阶段提交?

https://www.zhihu.com/question/64921387/answer/225784480
https://www.cnblogs.com/barrywxx/p/8506512.html


---
# none
auth请求各个企业管理
改为企业管理对外，然后请求相应的auth

之前没有讨论好架构就去做了，结果需要重构！！

服务状态
例如购买：
钱到了，应该改订单的状态.
至于用户的组别的权限更改，是不同服务的，可以通过订单系统发送一个信号进行异步更改，或者业务相关服务监控某个信号进行更改。对于一些非强一致性的，可以有延迟。

对于强一致性的接口（具体？）需要分布式锁去进行控制。


---
# uwsgi

## uwsgi-pass proxy-pass
uWSGI原生支持HTTP, FastCGI, SCGI及其特定的名为”uwsgi”的协议

uwsgi_pass 127.0.0.1:3031;
这表示“传递每一个请求给绑定到3031端口并使用uwsgi协议的服务器”。
uwsgi_pass使用uwsgi协议。 proxy_pass使用普通的HTTP与uWSGI服务器联系。uWSGI文档声称该协议更好，更快，并且可以从uWSGI的所有特殊功能（插件uWSGI plugin）中受益。 


## http http-socket

http 和 http-socket的使用上有一些区别:
[原生HTTP支持](https://uwsgi-docs-zh.readthedocs.io/zh_CN/latest/HTTP.html)
- http: 自己会产生一个http进程(可以认为与nginx同一层, 有路由器/代理/负载均衡器)负责路由http请求给worker, http进程和worker之间使用的是uwsgi协议
- http-socket: 不会产生http进程, 一般用于在前端webserver不支持uwsgi而仅支持http时使用, 他产生的worker使用的是http协议
- socket:  客户端的请求支持uwsgi, 则直接使用socket即可(tcp or unix)

Official documents recommend using http for a public server and http-socket for web-server after Nginx or Apache if you want use http in network.


因此, http 一般是作为独立部署的选项; http-socket 在前端webserver不支持uwsgi时使用,
如果前端webserver支持uwsgi, 则直接使用socket即可(tcp or unix)


uwsgi://127.0.0.1:8091


```
socket = /home/youmi/tmp/ag-auth.sock
http = 0.0.0.0:10181
启动得到:
uWSGI http bound on 0.0.0.0:10181 fd 3
uwsgi socket 0 bound to UNIX address /home/youmi/tmp/ag-auth.sock fd 6
...
spawned uWSGI master process (pid: 28872)
spawned uWSGI worker 1 (pid: 28876, cores: 1)
spawned uWSGI worker 2 (pid: 28877, cores: 1)
spawned uWSGI http 1 (pid: 28878)


---
socket = /home/youmi/tmp/ag-auth.sock
http-socket = 0.0.0.0:10181
启动得到:
uwsgi socket 0 inherited UNIX address /home/youmi/tmp/ag-auth.sock fd 6
uwsgi socket 1 bound to TCP address 0.0.0.0:10181 fd 3
...
gracefully (RE)spawned uWSGI master process (pid: 28872)
spawned uWSGI worker 1 (pid: 28955, cores: 1)
spawned uWSGI worker 2 (pid: 28956, cores: 1)

```

- [The uwsgi Protocol](https://uwsgi-docs.readthedocs.io/en/latest/Protocol.html)
- [Nginx支持uwsgi](https://uwsgi-docs-zh.readthedocs.io/zh_CN/latest/Nginx.html)
- [difference-between-uwsgi-pass-and-proxy-pass-in-nginx](https://stackoverflow.com/questions/34562730/difference-between-uwsgi-pass-and-proxy-pass-in-nginx)

