import random


def quick(nums, l, r):
    if l >= r:
        return
    s = l
    e = r
    while s < e:
        # 从后面先遍历就可以了？
        while s < e and nums[e] > nums[l]:
            e -= 1
        while s < e and nums[s] <= nums[l]:
            s += 1
        nums[s], nums[e] = nums[e], nums[s]
    nums[s], nums[l] = nums[l], nums[s]
    quick(nums, l, s-1)
    quick(nums, s+1, r)


def quick_sort(nums):
    length = len(nums)
    quick(nums, 0, length-1)
    return nums


input = [random.randint(1, 20) for _ in range(0, 10)]
# 无法处理有负数的例子， 注意负数取于取模问题， 注意有负数查找最大位数的长度逻辑
input = [4, 1, 10, 9, 1, -1, -21, -12]
# input = [-1, 2, -8, -10]
print(f"input {input} ,result {quick_sort(input)}")

for i in range(0, 100):
    input = [random.randint(1, 100) for _ in range(-20, 20)]
    o1 = quick_sort(input)
    o2 = sorted(input)
    assert o1 == o2
