---
# CORS和JSONP

参考链接:

- [什么是跨域请求以及实现跨域的方案](https://www.jianshu.com/p/f880878c1398)
- [详解js跨域问题](https://segmentfault.com/a/1190000000718840)

## CORS

跨源资源共享 Cross-Origin Resource Sharing(CORS) 是一个新的 W3C 标准，它新增的一组HTTP首部字段，允许服务端其声明哪些源站有权限访问哪些资源。换言之，它允许浏览器向声明了 CORS 的跨域服务器，发出 XMLHttpReuest 请求，从而克服 Ajax 只能同源使用的限制。

某些请求不会触发 CORS 预检请求。**需预检的请求**”要求必须首先使用OPTIONS方法发起一个预检请求到服务器，以获知服务器是否允许该实际请求。"预检请求“的使用，可以避免跨域请求对服务器的用户数据产生未预期的影响。

- [简单请求](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Access_control_CORS)

## JSONP的优缺点

JSONP的优点是：它不像XMLHttpRequest对象实现的Ajax请求那样受到同源策略的限制；它的兼容性更好，在更加古老的浏览器中都可以运行，不需要XMLHttpRequest或ActiveX的支持；并且在请求完毕后可以通过调用callback的方式回传结果。

JSONP的缺点则是：它只支持GET请求而不支持POST等其它类型的HTTP请求；它只支持跨域HTTP请求这种情况，不能解决不同域的两个页面之间如何进行JavaScript调用的问题。

## CORS和JSONP对比

CORS与JSONP相比，无疑更为先进、方便和可靠。

1. JSONP只能实现GET请求，而CORS支持所有类型的HTTP请求。

2. 使用CORS，开发者可以使用普通的XMLHttpRequest发起请求和获得数据，比起JSONP有更好的错误处理。

3. JSONP主要被老的浏览器支持，它们往往不支持CORS，而绝大多数现代浏览器都已经支持了CORS）。

---
# 跨域请求

在 HTML 中，`<a>, <form>, <img>, <script>, <iframe>, <link>` 等标签以及 Ajax 都可以指向一个资源地址，而所谓的跨域请求就是指：**当前发起请求的域与该请求指向的资源所在的域不一样**。这里的域指的是这样的一个概念：我们认为若协议 + 域名 + 端口号均相同，那么就是同域。

## 跨域请求的安全问题
​ 通常，浏览器会对上面提到的跨域请求作出限制。浏览器之所以要对**跨域请求作出限制**，是出于安全方面的考虑，因为跨域请求有可能被不法分子利用来发动 CSRF攻击。

### CSRF攻击
​ CSRF（Cross-site request forgery），中文名称：跨站请求伪造，也被称为：one click attack/session riding，缩写为：CSRF/XSRF。CSRF攻击者在用户已经登录目标网站之后，诱使用户访问一个攻击页面，利用目标网站对用户的信任，以用户身份在攻击页面对目标网站发起伪造用户操作的请求，达到攻击目的。

链接：　
- [什么是跨域请求以及实现跨域的方案](https://www.jianshu.com/p/f880878c1398)

### 为什么form表单提交没有跨域问题，但ajax提交有跨域问题？

因为原页面用 form 提交到另一个域名之后，**原页面的脚本无法获取新页面中的内容**。所以浏览器认为这是安全的。而 AJAX 是可以读取响应内容的，因此浏览器不能允许你这样做。如果你细心的话你会发现，其实请求已经发送出去了，你只是拿不到响应而已。所以浏览器这个策略的本质是，一个域名的 JS ，在未经允许的情况下，不得读取另一个域名的内容。但浏览器并不阻止你向另一个域名发送请求。
> form表单会刷新页面，不会把结果返回给js，所以相对安全。重放攻击？
- [跨域](https://www.zhihu.com/question/31592553/answer/190789780)

---

# 如何防止跨域请求

- [安全](./安全.md#csrf)


---

# django的csrf源码

_salt_cipher_secret、_unsalt_cipher_token
```
1. Cipher = (Secret + Salt) mod N  return: Salt + Cipher =》 csrfmiddlewaretoken
2. (Cipher - Salt) mod N 会等于 Secret 所以： csrfmiddlewaretoken：能解码得到secret
```
疑问：这个算法有什么用。都能推出来的。也没有私钥的加密。还不如直接用同一个值。前提都是建立在：csrftoken是黑客拿不到的
只是为了避免csrfmiddlewaretoken的随机性而已？并且能跟csrftoken的secret进行比较，也避免了有状态。csrftoken跟随着登录的session。

- [算法例子](https://www.jianshu.com/p/eaf4a57bbca7)


---
# [它是如何工作的](https://yiyibooks.cn/xx/Django_1.11.6/ref/csrf.html)

跨站伪造保护基于以下几点：

1.一个基于随机secret值的CSRF cookie，其它站点无法获取到。

此Cookie由CsrfViewMiddleware设置。 它和每个响应一起发送，如果请求上没有设置，则调用django.middleware.csrf.get_token()（这个函数用于内部获取CSRF token）。

为了**防止BREACH攻击**，token不仅仅是secret；**一个随机的salt**被添加到secret中，并用来加扰它。


出于安全考虑，**每当用户登录时，secret的值都会更改**。

> csrf token基于一个随机生成的秘钥secret，并通过salt hash方式加密生成csrftoken，插入到Cookie中。该csrftoken在用户登录阶段生成，在session结束前保持不变。


2.所有传出POST表单中都有一个名为“csrfmiddlewaretoken”的隐藏表单字段。

 该字段的值还是这个secret的值，其中添加了salt并且用于加扰它。 在每次调用get_token()时重新生成salt，所以在每个响应中这个表单字段值都会改变。

  此部分由模板标记完成。

> 每一个响应的POST表单中，都会插入一个隐藏的csrfmiddlewaretoken字段。该字段的值也是对1中的secret进行salt hash，每次请求表单页面都会使用一个随机的salt，所以每次响应中表单里面插入的csrfmiddlewaretoken都是不一样的。


3.对于所有未使用HTTP GET，HEAD，OPTIONS或TRACE的传入请求，必须存在CSRF cookie，并且“csrfmiddlewaretoken”字段必须存在且正确。 如果不是，用户将得到403错误。

  当验证'csrfmiddlewaretoken'字段值时，只将secret而不是完整的token与cookie值中的secret进行比较。 **这允许使用不断变化的token。 虽然每个请求可能使用自己的token，但是secret对所有人来说都是相同的。**

此检查由CsrfViewMiddleware完成。


# 问题

Q: 如何避免重放攻击？

> 好像无法避免？token好像在登录状态下是可以无限用。只要泄露一个form的token就可以一直用，直到登录刷新cookie的secret key。怎么样才会泄露呢？

> 需要自己用一层session的操作？

[相关的讨论](https://stackoverflow.com/a/25527231)

原因：Multiple browser windows / tabs and REST。防止多个浏览器/tab的时候，造成token的拒绝服务。或者存储的过载和复杂性，因为要维护状态。

- 里面说的如何避免中间人攻击是什么意思？referer


Q： 前后端分离后，怎么避免csrf攻击？可以提交表单，但是无法获取内容？所以要有确认操作？因为上面的避免操作都是因为post的表单要带上token。是后端渲染表单的时候带上的。前后端分离后怎么操作？

1. 表单的获取cookie的token，作为表单的字段提交进行校验。

2. API接口JWT方式的Token认证？跨域的时候，JWT 就放在 POST 请求的数据体里面。[阮一峰](https://www.ruanyifeng.com/blog/2018/07/json_web_token-tutorial.html)

> 引出的问题JWT: 客户端收到服务器返回的 JWT，可以储存在 Cookie 里面，也可以储存在 localStorage。此后，客户端每次与服务器通信，都要带上这个 JWT。你可以把它放在 Cookie 里面自动发送，但是这样不能跨域，所以更好的做法是放在 HTTP 请求的头信息Authorization字段里面。

总结： JWT的token不应该是放在cookie里面，因为这样子前后端分离的csrf的跨域表单攻击就能实现。除非你post请求把cookie的值放在请求体。而把jwt的token放在header其实就是能避免表单这个攻击。因为跨域的网站无法进行放在header的操作。前端的工作分两方面，一是存储 jwt，二是在所有的请求头中增加 Authoriaztion 。从头至尾，整个过程没有涉及 cookie，所以 CSRF 是不可能发生的。

- [如何通过JWT防御CSRF](https://segmentfault.com/a/1190000003716037)

---

Q： breach攻击是啥?为什么可以防止breach攻击?

http://www.doc88.com/p-9139615174722.html


## 常见问题
### 发布一个任意的CSRF令牌对（cookie和POST数据）一个漏洞？

不，这是设计。 没有中间人的攻击，攻击者无法向受害者的浏览器发送CSRF令牌cookie，所以成功的攻击需要通过XSS或类似的方式获取受害者的浏览器的cookie，在这种情况下攻击者通常不需要CSRF攻击。

一些安全审核工具将此标记为问题，但如前所述，攻击者无法窃取用户浏览器的CSRF cookie。 使用Firebug、Chrome等开发工具等“窃取”或修改你自己的token 不是一个漏洞。

> 问题的意思应该是，可以伪造发布任意的一对令牌。是不是漏洞？回答就是无法向受害者的浏览器发送CSRF令牌cookie。就算你伪造了，post请求还需要用户的cookie，那你就只能通过xss漏洞获取到了。
> csrf的表单攻击形式只能说你请求表单的内容伪造了，但是你是无法进行cookie的设置。或者你也无法获取到cookie的csrftoken，然后进行伪造csrfmiddlewaretoken。


- [美团前端安全系列（二）：如何防止CSRF攻击？](https://www.freebuf.com/articles/web/186880.html)

----

# 本地项目测试

因为jwt存在cookie上，所以表单提交存在跨域的危险。
```html
<form action="http://172.16.8.4:8890/api/favorites/keywords/cancel" method="POST">
    <input type="text" id="keyword" name="keyword">
    <button type="submit" class="btn btn-primary">Login</button>
</form>

```
请求是带着cookie过来了。不过还好约定的内容是application/json，改成json就不是简单请求了，会有跨域问题。所以存在风险，但还没造成影响。

但一不小心支持表单的类型，伪造一个钓鱼网站，诱导AE点击一下，把我提交到某个企业里面。所以还是把风险关闭才行。改成header获取提交把token带上。
