
lucene 从 4+版本后开始大量使用的数据结构是 FST。FST 有两个优点：

（1）空间占用小。通过对词典中**单词前缀和后缀的重复利用，压缩了存储空间**；

（2）查询速度快。**O(len(str))的查询时间复杂度**。

**FST，不但能共享前缀还能共享后缀。不但能判断查找的key是否存在，还能给出响应的输入output**。 它在时间复杂度和空间复杂度上都做了最大程度的优化，使得Lucene能够将Term Dictionary完全加载到内存，快速的定位Term找到响应的output（posting倒排列表）。


# 名词解释

关于FST（Finite State Transducer）,FST类似一种**TRIE树**。

使用FSM(Finite State Machines)作为数据结构

## FSM
FSM(Finite State Machines)有限状态机

表示有限个状态（State）集合以及这些状态之间转移和动作的数学模型。其中一个状态被标记为开始状态，0个或更多的状态被标记为final状态。

## FSA
确定无环有限状态接收机（Deterministric acyclic finite state acceptor, FSA）

确定：意味着指定任何一个状态，只可能最多有一个转移可以访问到。
无环： 不可能重复遍历同一个状态
接收机：有限状态机只“接受”特定的输入序列，并终止于final状态。

## FST
确定无环有限状态转换器（Deterministic acyclic finite state transducer， FST）

确定：意味着指定任何一个状态，只可能最多有一个转移可以遍历到。
无环： 不可能重复遍历同一个状态
transducer：接收特定的序列，终止于final状态，同时会输出一个值。

构建FST在很大程度上和构建FSA是一样的，主要的不同点是，**怎么样在转移上放置和共享outputs**。

## TRIE树
**单词查找树, 利用字符串的公共前缀来减少查询时间，最大限度地减少无谓的字符串比较，查询效率比哈希树高。**

TRIE可以看做是一个FSA,唯一的一个不同是TRIE只共享前缀，而**FSA不仅共享前缀还共享后缀**。



- https://www.shenyanchao.cn/blog/2018/12/04/lucene-fst/
- https://www.amazingkoala.com.cn/Lucene/yasuocunchu/2019/0220/35.html
