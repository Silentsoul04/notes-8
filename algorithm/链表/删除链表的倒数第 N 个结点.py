"""
给你一个链表，删除链表的倒数第 n 个结点，并且返回链表的头结点。

进阶：你能尝试使用一趟扫描实现吗？

https://leetcode-cn.com/problems/remove-nth-node-from-end-of-list/

"""


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
        tmp = head
        h = head
        while n > 0:
            tmp = tmp.next
            n -= 1
        # tmp会达到最后。导致tmp为None，出错
        while tmp.next != None:
            tmp = tmp.next
            head = head.next
        head.next = head.next.next
        return h


class Solution:
    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
        # tmp会达到最后。导致tmp为None，出错
        # 故提前申请一个ListNode。例子: [1] 1
        h = ListNode(next=head)
        tmp, s = h, h
        # 往前走N步
        while n > 0:
            tmp = tmp.next
            n -= 1
        # 如果tmp还没到达最后一个元素。两个游标一起移动
        while tmp.next != None:
            tmp = tmp.next
            h = h.next
        # h.next则是要删除的节点
        h.next = h.next.next
        return s.next
