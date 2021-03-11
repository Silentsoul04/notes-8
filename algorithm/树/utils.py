# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def init_tree(input):
    length = len(input)
    nums = [TreeNode(val=i) if i is not None else None for i in input]
    for i in range(length):
        left = 2 * i + 1
        right = 2 * i + 2
        if left < length:
            nums[i].left = nums[left]
        if right < length:
            nums[i].right = nums[right]

    return nums[0]


if __name__ == "__main__":
    a = init_tree([3, 9, 20, None, None, 15, 7])
    print(a)
