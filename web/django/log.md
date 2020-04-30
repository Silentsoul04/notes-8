---
# 默认log

django默认logging的配置位置:django/utils/log.py:18


loggers是django的作用

在django层次结构中捕获全部消息的logger。 没有使用此名称发布的消息，而是使用下面的logger之一(例如django.request)。handlers有两个，一个是标准输出(require_debug_true);一个是mail_admins，应该是用来发送**ERROE**级别信息到后台邮件的

例如django.request，默认的Django配置是没有该logger，也就是没有设propagate为Fasle。所以会传递给父级logger,django。

django.server,Django中的新功能1.10。记录与由runserver命令调用的服务器接收到的请求的处理相关的消息。 HTTP 5XX响应记录为ERROR消息，4XX响应记录为WARNING消息，其他所有内容都记录为INFO。propagate 为False，不会传给django父级logger 


---

如果自定义的django配置了console， 则好像会覆盖掉django默认的console的handle。导致django.request也是

---

logging 默认模块的logger是啥模式的?
当没有logging配置的时候，拿的是系统默认的配置，等级应该是warning级别的，输出。supervisor进行监控和重定向。
也就是
this_module = __name__.split(".")[-2]
logger = logging.getLogger(this_module)
会输出，但是不会有sentry的报警

---

参考链接：

- https://stackoverflow.com/a/5439502