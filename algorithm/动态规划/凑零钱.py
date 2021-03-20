#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
给定不同面额的硬币 coins 和一个总金额 amount。编写一个函数来计算可以凑成总金额所需的最少的硬币个数。如果没有任何一种硬币组合能组成总金额，返回 -1。

https://leetcode-cn.com/problems/coin-change/
"""


class Solution(object):
    def coinChange(self, coins, amount):
        """
        :type coins: List[int]
        :type amount: int
        :rtype: int
        """
        result = [0]
        for i in range(1, amount + 1):
            tmp = []
            for j in coins:
                # 这次的等于上一次的最小硬币数 + 1
                # 所以遍历硬币
                if i < j:
                    # 金额还没满足
                    continue
                else:
                    # 这次的等于上一次的最小硬币数 + 1
                    # 可以通过将数组的当前值设为当前值而不是-1，来避免判断，直接min就可以了
                    if result[i-j] > -1:
                        tmp.append(result[i-j] + 1)
            # 遍历硬币的最小值或者不成功
            result.append(min(tmp) if tmp else -1)
        return result[amount]


class Solution2(object):
    def coinChange(self, coins, amount):
        """
        链接：https://leetcode-cn.com/problems/coin-change/solution/322-ling-qian-dui-huan-by-leetcode-solution/
        """
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0

        for coin in coins:
            for x in range(coin, amount + 1):
                dp[x] = min(dp[x], dp[x - coin] + 1)
        return dp[amount] if dp[amount] != float('inf') else -1



print(Solution().coinChange([1, 2, 5], 11))
print(Solution2().coinChange([1, 2, 5], 11))
# print(Solution().coinChange([2], 3))
# print(Solution().coinChange([186, 419, 83, 408], 6249))
# print(Solution().coinChange([11, 5], 11))
# print(Solution().coinChange([11, 5], 11))
