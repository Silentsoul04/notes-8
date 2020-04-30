## 打log
问题： 如何打日志才是最好的？

---
问题： 函数前整理了有用的信息，函数里面的出错也要报这些信息，要把信息也传进去？
具体场景： bulk_data_to_es

思路一： 传信息进去，统一在函数里面，报错把信息附加到异常信息里
缺点： 函数调用很多层，每层都要传相应的信息

思路而： 不传信息进去，函数里面返回错误，在整理信息层再统一打错误logger
缺点： 代码冗余，要写很多重复的错误的捕获处理逻辑

---
## logging:

除了传递给日志记录函数的参数（如msg）外，有时候我们还想在日志输出中包含一些额外的上下文信息。

通过向日志记录函数传递一个extra参数引入上下文信息

```text

fmt = logging.Formatter("%(asctime)s - %(name)s - %(ip)s - %(username)s - %(mes sage)s")

extra_dict = {"ip": "113.208.78.29", "username": "Petter"}
logger.debug("User Login!", extra=extra_dict)

```

---
## 如何清空运行着的日志

直接删除文件后，用文本编辑器清空内容, 程序无法继续打日志了.
测试发现可以通过下面的语句做到清空效果而不影响程序继续打日志
```
with open('yourlog.log', 'w'):
    pass
```


---
### logging
python
root 配置
会把未命名的logger归为root
也把已命名的logger再次经过root

https://stackoverflow.com/a/6634089
