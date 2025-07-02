"""
Reverse Linked List Solutions

1. LeetCode-style solution with function reverseList(head) that returns new head.
2. Class-based LinkedList with method reverseLL(self) that reverses the linked list in place.
"""

# ✅ Node definition
class ListNode(object):
    def __init__(self, val=0, nextNode=None):
        self.val = val
        self.nextNode = nextNode


# ✅ Linked List class with your custom reverseLL
class LinkedList(object):
    def __init__(self):
        self.head = None

    def insert(self, val):
        if not self.head:
            self.head = ListNode(val)
        else:
            current = self.head
            while current.nextNode:
                current = current.nextNode
            current.nextNode = ListNode(val)

    def printList(self):
        current = self.head
        result = []
        while current:
            result.append(current.val)
            current = current.nextNode
        print(result)

    # ✅ My old custom reverse function
    def reverseLL(self):
        if self.head is None or self.head.nextNode is None:
            return self

        endPointer = self.head
        while endPointer.nextNode:
            endPointer = endPointer.nextNode        

        startPointer = self.head

        self.head = self.head.nextNode 
        endPointer.nextNode = startPointer
        endPointer.nextNode.nextNode = None
        startPointer = self.head

        while endPointer != startPointer:
            self.head = self.head.nextNode
            startPointer.nextNode = endPointer.nextNode
            endPointer.nextNode = startPointer
            startPointer = self.head

        return self


# ✅ LeetCode-style Solution (standard)
class Solution(object):
    def reverseList(self, head):
        """
        :type head: Optional[ListNode]
        :rtype: Optional[ListNode]
        """
        prev = None
        current = head

        while current:
            next_temp = current.nextNode  # Note: using nextNode to match LinkedList class
            current.nextNode = prev
            prev = current
            current = next_temp

        return prev


# ✅ Helper to convert ListNode back to Python list
def linkedListToList(head):
    result = []
    current = head
    while current:
        result.append(current.val)
        current = current.nextNode
    return result


# ✅ Test both solutions
if __name__ == "__main__":
    print("==== Testing Custom Class reverseLL ====")
    ll = LinkedList()
    for val in [1, 2, 3, 4, 5]:
        ll.insert(val)

    print("Original List:")
    ll.printList()

    ll.reverseLL()
    print("Reversed List (custom reverseLL):")
    ll.printList()


    print("\n==== Testing LeetCode reverseList ====")
    ll2 = LinkedList()
    for val in [1, 2, 3, 4, 5]:
        ll2.insert(val)

    print("Original List:")
    ll2.printList()

    solver = Solution()
    reversed_head = solver.reverseList(ll2.head)

    result = linkedListToList(reversed_head)
    print("Reversed List (LeetCode reverseList):")
    print(result)
