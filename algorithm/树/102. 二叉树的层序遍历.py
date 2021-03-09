"""
给你一个二叉树，请你返回其按 层序遍历 得到的节点值。 （即逐层地，从左到右访问所有节点）。

 

示例：
二叉树：[3,9,20,null,null,15,7],

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/binary-tree-level-order-traversal
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
from typing import List

from notebook.algorithm.树.utils import TreeNode
from notebook.algorithm.树.utils import init_tree


class Solution:
    def levelOrder(self, root: TreeNode) -> List[List[int]]:
        if not root:
            return []
        result = [[root.val]]
        deq = [root]
        while deq:
            tmp = []
            res_tmp = []
            for i in deq:
                if i.left:
                    tmp.append(i.left)
                    res_tmp.append(i.left.val)
                if i.right:
                    tmp.append(i.right)
                    res_tmp.append(i.right.val)
            deq = tmp
            # result置为加当前root的值
            if res_tmp:
                result.append(res_tmp)
        return result


class Solution:
    def levelOrder(self, root: TreeNode) -> List[List[int]]:
        if not root:
            return []
        result = []
        deq = [root]
        while deq:
            tmp = []
            res_tmp = []
            for i in deq:
                res_tmp.append(i.val)
                if i.left:
                    tmp.append(i.left)
                if i.right:
                    tmp.append(i.right)
            deq = tmp
            # result置为加当前root的值
            result.append(res_tmp)
        return result


a = init_tree([3, 9, 20, None, None, 15, 7])
print(Solution().levelOrder(a))
