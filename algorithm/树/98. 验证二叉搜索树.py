"""
给定一个二叉树，判断其是否是一个有效的二叉搜索树。

假设一个二叉搜索树具有如下特征：

节点的左子树只包含小于当前节点的数。
节点的右子树只包含大于当前节点的数。
所有左子树和右子树自身必须也是二叉搜索树。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/validate-binary-search-tree
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""

from notebook.algorithm.树.utils import TreeNode
from notebook.algorithm.树.utils import init_tree


class Solution:
    def isValidBST(self, root: TreeNode) -> bool:
        if not root:
            return False
        mi, ma = self.isValidTree(root)
        if mi is None:
            return False
        return True

    def isValidTree(self, root: TreeNode):
        if not root.left and not root.right:
            return root.val, root.val
        left_min = rigth_max = root.val
        if root.left:
            left_min, left_max = self.isValidTree(root.left)
            if left_max is None or left_max >= root.val:
                return None, None
        if root.right:
            rigth_min, rigth_max = self.isValidTree(root.right)
            # rigth_min会是子节点的数字
            if rigth_min is None or rigth_min <= root.val:
                return None, None
        return left_min, rigth_max


a = init_tree([5, 1, 4, None, None, 3, 6])
print(Solution().isValidBST(a))
a = init_tree([2, 1, 3])
print(Solution().isValidBST(a))
a = init_tree([1, 1])
res = Solution().isValidBST(a)
print(res)
assert res == False

"""

作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/validate-binary-search-tree/solution/yan-zheng-er-cha-sou-suo-shu-by-leetcode-solution/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""


class Solution:
    def isValidBST(self, root: TreeNode) -> bool:
        def helper(node, lower=float('-inf'), upper=float('inf')) -> bool:
            if not node:
                return True

            val = node.val

            # 判断某个节点是不是在某个区间范围内的
            if val <= lower or val >= upper:
                return False

            # 当前值应该是右子树的最小值
            if not helper(node.right, val, upper):
                return False

            # 当前值应该是左子树的最大值
            if not helper(node.left, lower, val):
                return False
            # 当你的最大值传进去后，也递归成左子树的最大值了
            # 左子树的当前值应该是该树的右子树的最小值，但是该树得到一个最大值的范围，沿用下去。

            return True

        return helper(root)

"""
TODO: 中序遍历
"""
