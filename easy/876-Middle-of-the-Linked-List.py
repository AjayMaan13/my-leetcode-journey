"""
876. MIDDLE OF THE LINKED LIST

Problem Statement:
Given the head of a singly linked list, return the middle node.
If there are two middle nodes, return the second middle node.

Example 1:
Input: head = [1,2,3,4,5]
Output: [3,4,5]
Explanation: The middle node of the list is node 3.

Example 2:
Input: head = [1,2,3,4,5,6]
Output: [4,5,6]
Explanation: Since the list has two middle nodes with values 3 and 4, 
we return the second one.
"""


# Definition for singly-linked list
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ==============================================================================
# APPROACH 1: YOUR SOLUTION (MANUAL COUNTING)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(1)

class Solution_ManualCount:
    def middleNode(self, head):
        """
        Move middle pointer every 2 steps of current pointer.
        
        Strategy:
        1. Use two pointers: curr and mid
        2. Move curr one step at a time
        3. Move mid one step for every 2 steps of curr
        4. Handle odd/even cases at the end
        
        This works but the logic is a bit complex with the counter.
        """
        if not head:
            return None
        
        curr = mid = head
        count = 0
        
        # Traverse the list
        while curr.next:
            curr = curr.next
            count += 1
            
            # Move mid pointer every 2 steps
            if count == 2:
                mid = mid.next
                count = 0
        
        # Handle final position based on count
        # count == 0: even number of nodes (mid is correct)
        # count != 0: odd number, need one more step
        return mid if count == 0 else mid.next


# ==============================================================================
# APPROACH 2: SLOW-FAST POINTERS (OPTIMAL - CLASSIC TECHNIQUE)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(1)
#
# This is the STANDARD solution for this problem!

class Solution:
    def middleNode(self, head):
        """
        Use slow and fast pointers (Floyd's Tortoise and Hare).
        
        Key Insight: 
        - Slow pointer moves 1 step at a time
        - Fast pointer moves 2 steps at a time
        - When fast reaches end, slow is at middle!
        
        Why this works:
        - Fast moves twice as fast as slow
        - When fast reaches end, slow is at half distance
        - For even length, fast becomes None (slow at second middle)
        - For odd length, fast.next becomes None (slow at exact middle)
        
        Example 1 (odd): [1,2,3,4,5]
        Step 0: slow=1, fast=1
        Step 1: slow=2, fast=3
        Step 2: slow=3, fast=5
        fast.next=None → stop, slow=3 ✓
        
        Example 2 (even): [1,2,3,4,5,6]
        Step 0: slow=1, fast=1
        Step 1: slow=2, fast=3
        Step 2: slow=3, fast=5
        Step 3: slow=4, fast=None
        fast=None → stop, slow=4 ✓
        
        This is the RECOMMENDED solution!
        """
        # Edge case: empty list
        if not head:
            return None
        
        slow = fast = head
        
        # Move fast 2x speed of slow
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        # When fast reaches end, slow is at middle
        return slow
