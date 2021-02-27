import random


def charu_sort(nums):
    length = len(nums)
    for i in range(1, length):
        while (i - 1) >= 0 and nums[i-1] > nums[i]:
            # 可以不用每次交换两个，等到最后在交换
            nums[i-1], nums[i] = nums[i], nums[i-1]
            i -= 1
    return nums


input = [random.randint(1, 20) for _ in range(0, 10)]
# 无法处理有负数的例子， 注意负数取于取模问题， 注意有负数查找最大位数的长度逻辑
input = [4, 1, 10, 9, 1, -1, -21, -12]
# input = [-1, 2, -8, -10]
print(f"input {input} ,result {charu_sort(input)}")

for i in range(0, 100):
    input = [random.randint(1, 100) for _ in range(-20, 20)]
    o1 = charu_sort(input)
    o2 = sorted(input)
    assert o1 == o2
