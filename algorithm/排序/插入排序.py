"""
将第一待排序序列第一个元素看做一个有序序列，把第二个元素到最后一个元素当成是未排序序列。

从头到尾依次扫描未排序序列，将扫描到的每个元素插入有序序列的适当位置。（如果待插入的元素与有序序列中的某个元素相等，则将待插入元素插入到相等元素的后面。）

https://leetcode-cn.com/problems/sort-an-array/
"""
import random


class Solution(object):
    def sort(self, arrays):
        for i in range(len(arrays)):
            # i = 2
            index = i
            current = arrays[index]
            while index > 0 and arrays[index - 1] > current:
                arrays[index] = arrays[index - 1]
                index -= 1
            arrays[index] = current

        # return sorted(arrays)
        return arrays


print(Solution().sort([2, 3, 1, 4]))
print(Solution().sort([4, 2, 3, 1]))
print(Solution().sort([4, 2, 3, 1]))

for i in range(0, 50):
    input = [random.randint(1, 10000) for _ in range(0, 1000)]
    o1 = Solution().sort(input)
    o2 = sorted(input)
    assert o1 == o2


"""
[优化的插入排序](https://www.cnblogs.com/heyuquan/p/insert-sort.html)

二分插入排序：

二分法插入排序，简称二分排序，是在插入第i个元素时，对前面的0～i-1元素进行折半，先跟他们中间的那个元素比，如果小，则对前半再进行折半，否则对后半进行折半，直到left<right，然后再把第i个元素前1位与目标位置之间的所有元素后移，再把第i个元素放在目标位置上。

希尔排序：


"""