"""
2095. DELETE THE MIDDLE NODE OF A LINKED LIST

Problem Statement:
Given the head of a linked list, delete the middle node and return the head.

The middle node is the ⌊n / 2⌋th node (0-indexed).
- n=1: middle is 0 (return empty list)
- n=2: middle is 1 (delete 2nd node)
- n=3: middle is 1 (delete 2nd node)
- n=4: middle is 2 (delete 3rd node)
- n=5: middle is 2 (delete 3rd node)

Example 1:
Input: head = [1,3,4,7,1,2,6]
Output: [1,3,4,1,2,6]
Explanation: n=7, middle=3, delete node at index 3 (value 7)

Example 2:
Input: head = [1,2,3,4]
Output: [1,2,4]
Explanation: n=4, middle=2, delete node at index 2 (value 3)

Example 3:
Input: head = [2,1]
Output: [2]
Explanation: n=2, middle=1, delete node at index 1 (value 1)
"""


# Definition for singly-linked list
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ==============================================================================
# APPROACH 1: YOUR FIRST SOLUTION (TWO PASS)
# ==============================================================================
# Time Complexity: O(n) - traverse twice
# Space Complexity: O(1)

class Solution_TwoPass:
    def deleteMiddle(self, head):
        """
        Two-pass approach: count length, then delete middle.
        
        Strategy:
        1. First pass: count nodes
        2. Calculate middle index: n // 2
        3. Second pass: traverse to node before middle
        4. Delete middle node
        
        This works but has complex edge case handling.
        """
        if not head:
            return head
        
        # Count nodes
        mid = 0
        curr = head
        while curr:
            curr = curr.next
            mid += 1
        
        # Calculate middle index
        mid = mid // 2
        
        # Traverse to node before middle
        curr = head
        while mid > 1:
            curr = curr.next
            mid -= 1
        
        # Delete middle node
        if curr.next:
            curr.next = curr.next.next
        else:
            # Edge case: single node
            if not head.next:
                return None
            head.next = None
        
        return head


# ==============================================================================
# APPROACH 2: YOUR SECOND SOLUTION (SLOW-FAST WITH DUMMY - OPTIMAL!)
# ==============================================================================
# Time Complexity: O(n) - single pass!
# Space Complexity: O(1)
#
# This is EXCELLENT! ⭐

class Solution:
    def deleteMiddle(self, head):
        """
        Slow-fast pointers with dummy node - OPTIMAL solution!
        
        Strategy:
        1. Use dummy node to handle edge cases
        2. Start fast one step ahead (fast = dummy.next)
        3. Move slow 1 step, fast 2 steps
        4. When fast reaches end, slow is at node BEFORE middle
        5. Delete middle: slow.next = slow.next.next
        
        Why fast = dummy.next?
        - We want slow to stop at node BEFORE middle (not AT middle)
        - Starting fast one ahead creates the right gap
        
        Visual Example: [1,2,3,4,5]
        
        Initial:
            dummy → 1 → 2 → 3 → 4 → 5 → None
            ↑       ↑
          slow    fast
        
        After iterations:
            dummy → 1 → 2 → 3 → 4 → 5 → None
                        ↑               ↑
                      slow            fast
        
        slow is at 2 (before middle 3)
        Delete: 2.next = 4
        Result: [1,2,4,5] ✓
        
        This is the OPTIMAL solution!
        """
        if not head:
            return head
        
        # Dummy node eliminates edge cases
        dummy = ListNode(0)
        dummy.next = head
        
        slow = fast = dummy
        fast = fast.next  # Start fast one ahead!
        
        # Move slow 1 step, fast 2 steps
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        # slow is now at node BEFORE middle
        # Delete middle node
        slow.next = slow.next.next
        
        return dummy.next


# ==============================================================================
# APPROACH 3: ALTERNATIVE (PREV POINTER)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(1)

class Solution_WithPrev:
    def deleteMiddle(self, head):
        """
        Alternative using explicit prev pointer.
        
        Same idea but without starting fast ahead.
        Use prev to track node before slow.
        """
        # Edge case: single node
        if not head or not head.next:
            return None
        
        slow = fast = head
        prev = None
        
        while fast and fast.next:
            prev = slow
            slow = slow.next
            fast = fast.next.next
        
        # slow is at middle, prev is before it
        prev.next = slow.next
        
        return head
