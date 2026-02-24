"""
DELETE ALL OCCURRENCES OF A KEY IN DOUBLY LINKED LIST

Problem: Given head of DLL and target, delete all nodes with value = target.

Example 1:
Input: 1 <-> 2 <-> 3 <-> 1 <-> 4, target = 1
Output: 2 <-> 3 <-> 4

Example 2:
Input: 2 <-> 3 <-> -1 <-> 4 <-> 2, target = 2
Output: 3 <-> -1 <-> 4

Example 3:
Input: 7 <-> 7 <-> 7 <-> 7, target = 7
Output: None (empty list)
"""


# Definition of doubly linked list
class ListNode:
    def __init__(self, val=0, next=None, prev=None):
        self.val = val
        self.next = next
        self.prev = prev


# ==============================================================================
# OPTIMAL SOLUTION
# ==============================================================================
# Time Complexity: O(n) - single pass
# Space Complexity: O(1) - only pointers

class Solution:
    def deleteAllOccurrences(self, head, target):
        """
        Delete all nodes with value = target from DLL.
        
        Strategy:
        1. Use dummy node to handle head deletion
        2. Traverse list
        3. For each node with target value:
           - Update prev.next to skip current
           - Update next.prev to skip current
        4. Return dummy.next
        
        Key: DLL has prev pointer, so we can delete in one pass!
        """
        # Dummy node simplifies head deletion
        dummy = ListNode(0)
        dummy.next = head
        if head:
            head.prev = dummy
        
        curr = head
        
        while curr:
            if curr.val == target:
                # Delete current node
                # Link previous to next
                curr.prev.next = curr.next
                
                # Link next to previous (if next exists)
                if curr.next:
                    curr.next.prev = curr.prev
                
                # Move to next
                curr = curr.next
            else:
                # Move to next without deleting
                curr = curr.next
        
        # Disconnect dummy from result
        if dummy.next:
            dummy.next.prev = None
        
        return dummy.next


# ==============================================================================
# ALTERNATIVE: WITHOUT DUMMY NODE
# ==============================================================================

class Solution_NoDummy:
    def deleteAllOccurrences(self, head, target):
        """Alternative without dummy node - more edge cases to handle"""
        
        # Skip all target nodes at head
        while head and head.val == target:
            head = head.next
            if head:
                head.prev = None
        
        curr = head
        
        while curr:
            if curr.val == target:
                # Delete current
                if curr.prev:
                    curr.prev.next = curr.next
                if curr.next:
                    curr.next.prev = curr.prev
                curr = curr.next
            else:
                curr = curr.next
        
        return head

