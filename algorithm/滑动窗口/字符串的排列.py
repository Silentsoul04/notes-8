"""
给定两个字符串 s1 和 s2，写一个函数来判断 s2 是否包含 s1 的排列。

换句话说，第一个字符串的**排列之一**是第二个字符串的子串。
"""
from collections import Counter


class Solution(object):
    def checkInclusion(self, s1, s2):
        """
        要保持窗口的长度，进行滑动
        """
        s1_c = Counter(s1)
        left = 0
        right = len(s1)
        while right <= len(s2):
            windows = s2[left:right]
            s2_c = Counter(windows)
            if all(map(lambda x: s1_c[x] <= s2_c[x], s1_c.keys())):
                return True
            left += 1
            right += 1
        return False


class Solution2(object):
    def checkInclusion(self, s1, s2):
        """
        要保持窗口的长度，进行滑动
        """
        s1_c = Counter(s1)
        left = 0
        right = len(s1) - 1
        lookup = Counter(s2[left:right])
        while right < len(s2):
            lookup[s2[right]] += 1
            if all(map(lambda x: s1_c[x] <= lookup[x], s1_c.keys())):
                return True
            lookup[s2[left]] -= 1
            left += 1
            right += 1
        return False


class Solution3(object):
    def checkInclusion(self, s1, s2):
        """
        要保持窗口的长度，进行滑动
        """
        s1_c = Counter(s1)
        left = 0
        right = 0
        lookup = Counter()
        s2_l = len(s2)
        s1_l = len(s1)
        while right < s2_l:
            lookup[s2[right]] += 1
            if right - left < s1_l - 1:
                right += 1
                continue
            if all(map(lambda x: s1_c[x] <= lookup[x], s1_c.keys())):
                return True
            lookup[s2[left]] -= 1
            left += 1
            right += 1
        return False

print(Solution3().checkInclusion('ab', 'eidboaoo'))
# print(Solution().checkInclusion('ab', 'eidbaooo'))
# print(Solution().checkInclusion("adc", "dcda"))
print(Solution3().checkInclusion("adc", "dcda"))

