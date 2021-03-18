"""
给你单链表的头指针 head 和两个整数 left 和 right ，其中 left <= right 。请你反转从位置 left 到位置 right 的链表节点，返回 反转后的链表 。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/reverse-linked-list-ii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""
from notebook.algorithm.链表.utils import ListNode
from notebook.algorithm.链表.utils import init_ln
from notebook.algorithm.链表.utils import print_ln


class Solution:
    def reverseBetween(self, head: ListNode, left: int, right: int) -> ListNode:
        tmp = head
        pre = None
        interval = right - left
        # 如果是left=1说明是直接反转topk
        # 如何优化？left=1, pre就是空的
        if not left > 1:
            return self.reverseTopK(tmp, interval)
        # 找出要反转的左边头节点
        while left > 1:
            left -= 1
            pre = tmp
            tmp = tmp.next
        # 续回反转后的节点
        pre.next = self.reverseTopK(tmp, interval)
        return head

    def reverseTopK(self, head: ListNode, k):
        # 反转topk写了两次还是写得不顺手
        # 递归也可以
        tmp = head

        # 当前节点的前一个节点
        pre = None
        # 保留下一个节点
        nxt = head.next
        while head.next and k > 0:
            # 当前节点反转到前一个节点
            head.next = pre
            # 顺序下去
            pre = head
            head = nxt
            # 下个节点的下个节点
            nxt = nxt.next
            k -= 1
        # 当前节点已经下一个节点还未连上
        head.next = pre
        # 记录之前的头，作为非反转的头
        tmp.next = nxt
        return head


head1 = init_ln([1, 2, 3, 4, 5])
# print_ln(Solution().reverseTopK(head1, 2))
# print_ln(Solution().reverseBetween(head1, 2, 4))
# print_ln(Solution().reverseBetween(init_ln([5]), 1, 1))
print_ln(Solution().reverseBetween(init_ln([3, 5]), 1, 2))
