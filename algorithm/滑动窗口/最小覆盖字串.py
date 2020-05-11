"""
给你一个字符串 S、一个字符串 T，请在字符串 S 里面找出：包含 T 所有字符的最小子串。

示例：

输入: S = "ADOBECODEBANC", T = "ABC"
输出: "BANC"

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/minimum-window-substring
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""


class Solution(object):
    def minWindow(self, s, t):
        """
        错误版本：
        如何判断窗口符合字符的数据。set不能，因为会有去重， 没有重复的字数的限制了。反例：aa aa   bba baa
        """
        left = 0
        right = len(t)
        s_l = len(s)
        if s_l < right:
            return ''
        result = s
        t_s = set(t)
        flag = False
        while left < right:
            w = s[left:right]
            windows = set(s[left:right])
            if not t_s.issubset(windows):
                if right == s_l:
                    left += 1
                else:
                    right += 1
            else:
                if len(windows) <= len(result) and len(w) >= len(t):
                    result = w
                    flag = True
                left += 1
        return result if flag else ''


S = "ADOBECODEBANC"
T = "ABC"

# print(Solution().minWindow(S, T))
# print(Solution().minWindow('a', 'a'))
# print(Solution().minWindow('a', 'aa'))
# print(Solution().minWindow('a', 'b'))
# print(Solution().minWindow('ab', 'A'))
# print(Solution().minWindow('aa', 'aa'))
# print(Solution().minWindow('bbaa', 'aba'))  # bba or baa


class Solution2:
    """
    用Counter进行比较。
    判断窗口的k和频次是否对得上:
    all(map(lambda x: lookup[x] >= t[x], t.keys()))
    滑动的时候，开头的k的频次-=1
    """
    def minWindow(self, s, t):
        from collections import Counter
        t = Counter(t)
        lookup = Counter()
        start = 0
        end = 0
        min_len = float("inf")
        res = ""
        while end < len(s):
            lookup[s[end]] += 1
            end += 1
            # print(start, end)
            while all(map(lambda x: lookup[x] >= t[x], t.keys())):
                if end - start < min_len:
                    res = s[start:end]
                    min_len = end - start
                lookup[s[start]] -= 1
                start += 1
        return res


print(Solution2().minWindow('bbaa', 'aba'))  # bba or baa

"""
作者：powcai
链接：https://leetcode-cn.com/problems/minimum-window-substring/solution/hua-dong-chuang-kou-by-powcai-2/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""
