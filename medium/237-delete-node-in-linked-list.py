"""
237. DELETE NODE IN A LINKED LIST

Problem Statement:
There is a singly-linked list head and we want to delete a node in it.
You are given the node to be deleted. You will NOT have access to the head.

All values are unique, and the given node is NOT the last node.

Delete the given node. Note: We don't remove from memory, but:
- The value should not exist in the list
- Number of nodes should decrease by one
- Order should be preserved

Example 1:
Input: head = [4,5,1,9], node = 5
Output: [4,1,9]
Explanation: Given second node with value 5, list becomes 4 -> 1 -> 9.

Example 2:
Input: head = [4,5,1,9], node = 1
Output: [4,5,9]
Explanation: Given third node with value 1, list becomes 4 -> 5 -> 9.
"""


# Definition for singly-linked list
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


# ==============================================================================
# APPROACH 1: YOUR FIRST SOLUTION (SHIFT ALL VALUES - INEFFICIENT)
# ==============================================================================
# Time Complexity: O(n) - traverse to end of list
# Space Complexity: O(1)

class Solution_ShiftValues:
    def deleteNode(self, node):
        """
        Shift all subsequent values left, then delete last node.
        
        Strategy:
        1. Copy value from next node to current
        2. Move to next node
        3. Repeat until second-to-last node
        4. Delete last node
        
        Problem: Unnecessary traversal to end of list.
        We only need to "delete" the given node, not actually shift everything.
        
        This works but is O(n) when O(1) is possible.
        """
        if not node:
            return
        
        curr = node
        prev = None
        
        # Shift all values left
        while curr.next:
            curr.val = curr.next.val  # Copy next value to current
            prev = curr
            curr = curr.next
        
        # Delete last node
        prev.next = None
        
        return


# ==============================================================================
# APPROACH 2: COPY NEXT AND SKIP (OPTIMAL - YOUR SECOND SOLUTION)
# ==============================================================================
# Time Complexity: O(1) - constant time!
# Space Complexity: O(1)
#
# This is the TRICK solution!

class Solution:
    def deleteNode(self, node):
        """
        Copy next node's value and skip next node.
        
        Key Insight: We can't delete current node because we don't have
        access to the previous node. But we CAN:
        1. Copy next node's value to current node
        2. Delete next node by skipping it
        
        This effectively "deletes" the current node's value from the list!
        
        Example: [4 -> 5 -> 1 -> 9], delete node with value 5
        
        Before:  4 -> 5 -> 1 -> 9
                      ^
                    node
        
        Step 1: Copy next value (1) to current node
                4 -> 1 -> 1 -> 9
                     ^
                   node
        
        Step 2: Skip next node
                4 -> 1 -> 9
                     ^
                   node
        
        Result: Value 5 is gone, list is [4,1,9] ✓
        
        This is the OPTIMAL solution - O(1) time!
        """
        # Copy next node's value to current node
        node.val = node.next.val
        
        # Skip next node (effectively deleting it)
        node.next = node.next.next
        
        # OR
        # Get reference to next node (the one we'll actually delete)
        next_node = node.next
        
        # Copy next node's value to current node
        node.val = next_node.val
        
        # Skip over next node
        node.next = next_node.next
        
        # Optional: Help garbage collector (not necessary in Python)
        # next_node = None
        
        return
