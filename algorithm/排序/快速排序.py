#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快速排序的最坏运行情况是 O(n²)，比如说顺序数列的快排。但它的平摊期望时间是 O(nlogn)，且 O(nlogn) 记号中隐含的常数因子很小，比复杂度稳定等于 O(nlogn) 的归并排序要小很多。所以，对绝大多数顺序性较弱的随机数列而言，快速排序总是优于归并排序。

从数列中挑出一个元素，称为 “基准”（pivot）;

重新排序数列，所有元素比基准值小的摆放在基准前面，所有元素比基准值大的摆在基准的后面（相同的数可以到任一边）。在这个分区退出之后，该基准就处于数列的中间位置。这个称为分区（partition）操作；

递归地（recursive）把小于基准值元素的子数列和大于基准值元素的子数列排序；

递归的最底部情形，是数列的大小是零或一，也就是永远都已经被排序好了。虽然一直递归下去，但是这个算法总会退出，因为在每次的迭代（iteration）中，它至少会把一个元素摆到它最后的位置去。


"""


def quick_sort(arr, left=None, right=None):
    left = 0 if not isinstance(left, (int, float)) else left
    right = len(arr) - 1 if not isinstance(right, (int, float)) else right
    if left < right:
        partition_index = partition(arr, left, right)
        # 分治法
        quick_sort(arr, left, partition_index - 1)
        quick_sort(arr, partition_index + 1, right)
    return arr


def partition(arr, left, right):
    """对数组的左右范围进行排序"""
    pivot = left
    index = pivot + 1
    i = index
    # pivot的下标不会改变，通过移动后面的数值进行排序，最后结束后，通过移动pivot和index进行移动。
    while i <= right:
        # 通过i来进行递增遍历所有的参数，如果发现数值小于基准的数值，则移动index和i的位置（第一次都是相同的值不移动）
        # index： **index记录的是比基准值要大数字的下标位置， 比基准值要小的数字都在index的左边。所以遇到大于基准值的不移动，以作下次的交换。**
        if arr[i] < arr[pivot]:
            swap(arr, i, index)
            index += 1
        i += 1
    swap(arr, pivot, index - 1)
    return index - 1


def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]


print(quick_sort([5, 3, 2, 4, 7, 8, 1]))


def quick_sort(data):
    """快速排序"""
    if len(data) >= 2:  # 递归入口及出口
        mid = data[len(data)//2]  # 选取基准值，也可以选取第一个或最后一个元素
        left, right = [], []  # 定义基准值左右两侧的列表
        data.remove(mid)  # 从原始数组中移除基准值
        for num in data:
            if num >= mid:
                right.append(num)
            else:
                left.append(num)
        return quick_sort(left) + [mid] + quick_sort(right)
    else:
        return data


"""算法导论版本"""


class Solution:
    def sortArray(self, array):
        self.quick_sort(array, 0, len(array) - 1)
        return array

    def quick_sort(self, array, l, r):
        if l < r:
            q = self.partition(array, l, r)
            self.quick_sort(array, l, q - 1)
            self.quick_sort(array, q + 1, r)

    def partition(self, array, l, r):
        x = array[r]  # 最后一个元素作为基准值
        i = l
        for j in range(l, r):
            # 如果发现比基准值的数值要大，则停止i下标，用作下一次的交换
            if array[j] <= x:
                array[i], array[j] = array[j], array[i]
                i += 1
        # 结束的时候，index是会比基准值要大的
        array[i], array[r] = array[r], array[i]
        return i


arr = [5, 3, 2, 4, 7, 8, 1]
print('--2', Solution().sortArray(arr))
