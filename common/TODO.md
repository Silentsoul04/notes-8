canel 是在MQMessageUtils里面进行消息的hash的操作。用hashcode原生方法。

```
hashCode = hashCode ^ column.getValue().hashCode();
```

- [浅谈Java中的hashcode方法](https://www.cnblogs.com/dolphin0520/p/3681042.html)
- [建议增加一个属性，针对根据某一字段hash时，hash算法可以不根据database算出](https://github.com/alibaba/canal/issues/2248)



---
Print sums of all subsets of a given set: https://www.geeksforgeeks.org/print-sums-subsets-given-set/
来生成platform这些位的所有查询集合


---

apps/utils/http.py:2:0: W0611: Unused namedtuple imported from collections (unused-import)
改为apps/utils/https.py 就没有问题？

pylint 对http.py W0611:

原因: apps/utils/ 目录下没有__init__ 文件！
