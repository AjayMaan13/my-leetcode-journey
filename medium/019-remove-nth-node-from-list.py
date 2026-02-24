"""
19. REMOVE NTH NODE FROM END OF LIST

Problem Statement:
Given the head of a linked list, remove the nth node from the end of the list 
and return its head.

Example 1:
Input: head = [1,2,3,4,5], n = 2
Output: [1,2,3,5]
Explanation: Remove 4 (2nd from end)

Example 2:
Input: head = [1], n = 1
Output: []
Explanation: Remove only node

Example 3:
Input: head = [1,2], n = 1
Output: [1]
Explanation: Remove 2 (1st from end)
"""


# Definition for singly-linked list
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ==============================================================================
# APPROACH 1: YOUR FIRST SOLUTION (TWO PASS)
# ==============================================================================
# Time Complexity: O(n) - traverse twice
# Space Complexity: O(1)

class Solution_TwoPass:
    def removeNthFromEnd(self, head, n):
        """
        Two-pass approach: count length, then remove node.
        
        Strategy:
        1. First pass: count total nodes
        2. Calculate position from start: (length - n)
        3. Second pass: traverse to that position and remove
        
        This works but requires two passes through the list.
        """
        if not head:
            return None
        
        # First pass: count nodes
        prev = curr = head
        length = 0
        while curr:
            curr = curr.next
            length += 1
        
        # Calculate position from start
        position = length - n
        
        # Second pass: traverse to position
        curr = head
        currIndex = 0
        
        while curr.next and currIndex < position:
            currIndex += 1
            prev = curr
            curr = curr.next
        
        # Handle removing head
        if position == 0:
            head = head.next
        else:
            prev.next = curr.next
            curr.next = None
        
        return head


# ==============================================================================
# APPROACH 2: YOUR SECOND SOLUTION (ONE PASS WITH GAP)
# ==============================================================================
# Time Complexity: O(n) - single pass!
# Space Complexity: O(1)
#
# This is BETTER than first approach!

class Solution_OnePass:
    def removeNthFromEnd(self, head, n):
        """
        One-pass using two pointers with gap of n.
        
        Strategy:
        1. Move fast pointer n steps ahead
        2. Move both slow and fast together until fast reaches end
        3. When fast reaches end, slow is at node before target
        4. Remove target node
        
        Key Insight: Maintain gap of n between slow and fast.
        When fast reaches end, slow is n positions before end.
        
        This is more efficient - only one pass!
        """
        if not head:
            return None
        
        slow = fast = head
        
        # Move fast n steps ahead
        for _ in range(n):
            if fast:
                fast = fast.next
        
        # Special case: removing head
        if fast is None:
            return head.next
        
        # Move both until fast reaches end
        while fast.next:
            slow = slow.next
            fast = fast.next
        
        # slow is now at node before target
        # Remove target node
        slow.next = slow.next.next
        
        return head


# ==============================================================================
# APPROACH 3: DUMMY NODE (OPTIMAL - CLEANEST)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(1)
#
# This is the STANDARD solution!

class Solution:
    def removeNthFromEnd(self, head, n):
        """
        One-pass with dummy node - handles all edge cases elegantly.
        
        Strategy:
        1. Create dummy node pointing to head
        2. Use two pointers with gap of n+1 (to get node BEFORE target)
        3. Move both until fast reaches end
        4. Remove target node
        5. Return dummy.next (handles head removal automatically)
        
        Why dummy node?
        - Eliminates special case for removing head
        - Slow always points to node BEFORE target
        - Clean, uniform handling of all cases
        
        Visual Example: [1,2,3,4,5], n = 2
        
        Initial:
            dummy → 1 → 2 → 3 → 4 → 5 → None
            ↑
          slow, fast
        
        After moving fast n+1=3 steps:
            dummy → 1 → 2 → 3 → 4 → 5 → None
            ↑               ↑
          slow            fast
        
        After moving both together:
            dummy → 1 → 2 → 3 → 4 → 5 → None
                        ↑               ↑
                      slow            fast
        
        Remove: slow.next = slow.next.next
            dummy → 1 → 2 → 3 → 5 → None
        
        Return dummy.next
        
        This is the RECOMMENDED solution!
        """
        # Create dummy node to handle edge cases
        dummy = ListNode(0)
        dummy.next = head
        
        slow = fast = dummy
        
        # Move fast n+1 steps ahead (to create gap)
        # +1 so slow stops at node BEFORE target
        for _ in range(n + 1):
            if fast:
                fast = fast.next
        
        # Move both until fast reaches end
        while fast:
            slow = slow.next
            fast = fast.next
        
        # slow is now at node before target
        # Remove target node
        slow.next = slow.next.next
        
        # Return head (dummy.next handles case when head was removed)
        return dummy.next