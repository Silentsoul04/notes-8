def init_ln(nums):
    ln = ListNode(nums[0])
    tmp = ln
    for i in nums[1:]:
        tmp.next = ListNode(i, next=None)
        tmp = tmp.next
    return ln


def print_ln(head):
    res = [head.val]
    while head.next:
        head = head.next
        res.append(head.val)
    print(res)


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
