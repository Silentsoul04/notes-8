---
Print sums of all subsets of a given set: https://www.geeksforgeeks.org/print-sums-subsets-given-set/
来生成platform这些位的所有查询集合


---

apps/utils/http.py:2:0: W0611: Unused namedtuple imported from collections (unused-import)
改为apps/utils/https.py 就没有问题？

pylint 对http.py W0611:  

原因: apps/utils/ 目录下没有__init__ 文件！
