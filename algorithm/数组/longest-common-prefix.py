"""
编写一个函数来查找字符串数组中的最长公共前缀。

如果不存在公共前缀，返回空字符串 ""。

示例 1:

输入: ["flower","flow","flight"]
输出: "fl"

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/longest-common-prefix
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

注意：前缀的意思。也就是开头的
"""
from typing import List


class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        if not strs:
            return ""
        result = strs[0]
        for j in strs[1:]:
            if result == '':
                return result
            while j.find(result) != 0:
                result = result[:-1]
        return result


inp = ["flower", "flow", "flight"]

print(f"input{inp}, output: {Solution().longestCommonPrefix(inp)}")


class Solution:
    def longestCommonPrefix(self, strs):
        """
        :type strs: List[str]
        :rtype: str
        """
        res = ""
        for tmp in zip(*strs):
            tmp_set = set(tmp)
            if len(tmp_set) == 1:
                res += tmp[0]
            else:
                break
        return res

inp = ["flower", "flow", "flight"]

print(f"input{inp}, output: {Solution().longestCommonPrefix(inp)}")
