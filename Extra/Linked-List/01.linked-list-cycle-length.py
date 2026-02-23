"""
LENGTH OF LOOP IN LINKED LIST

Problem Statement:
Given the head of a linked list, determine the length of a loop present in 
the linked list. If there's no loop present, return 0.

Example 1:
Input: 1 → 2 → 3 → 4 → 5
                ↑         ↓
                └─────────┘
Output: 4
Explanation: Loop contains nodes 2 → 3 → 4 → 5 → back to 2 (4 nodes)

Example 2:
Input: 1 → 2 → 3 → 4 → 5 → None
Output: 0
Explanation: No loop present, return 0
"""


# ==============================================================================
# NODE DEFINITION
# ==============================================================================

class Node:
    """Node class for singly linked list"""
    def __init__(self, data, next=None):
        self.data = data
        self.next = next


# ==============================================================================
# APPROACH 1: FLOYD'S ALGORITHM (OPTIMAL)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(1) - only two pointers!

class Solution:
    def lengthOfLoop(self, head):
        """
        Floyd's Cycle Detection to find loop length.
        
        Strategy:
        Phase 1: Detect if loop exists
        - Use slow (1 step) and fast (2 steps) pointers
        - If they meet, loop exists
        
        Phase 2: Count loop length
        - From meeting point, count steps to return to meeting point
        - This count is the loop length
        
        This is OPTIMAL - O(n) time, O(1) space!
        """
        if not head:
            return 0
        
        # Phase 1: Detect cycle using Floyd's algorithm
        slow = fast = head
        
        while fast and fast.next:
            slow = slow.next      # Move 1 step
            fast = fast.next.next  # Move 2 steps
            
            # Cycle detected!
            if slow == fast:
                # Phase 2: Count loop length
                return self.countLoopLength(slow)
        
        # No cycle found
        return 0
    
    def countLoopLength(self, meeting_point):
        """
        Count the length of the loop starting from meeting point.
        
        Args:
            meeting_point: Node where slow and fast pointers met
            
        Returns:
            Length of the loop
            
        Strategy:
        - Start from meeting point
        - Move one step at a time counting
        - Stop when we return to meeting point
        - Count is the loop length
        """
        temp = meeting_point
        length = 1  # Already at one node
        
        # Move until we come back to meeting point
        while temp.next != meeting_point:
            temp = temp.next
            length += 1
        
        return length


# ==============================================================================
# APPROACH 3: COMPACT VERSION (ONE FUNCTION)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(1)

class Solution_Compact:
    def lengthOfLoop(self, head):
        """
        Compact version with loop counting inline.
        """
        if not head:
            return 0
        
        slow = fast = head
        
        # Detect cycle
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            
            if slow == fast:
                # Found cycle, count length
                length = 1
                temp = slow.next
                
                # Count until we return to slow
                while temp != slow:
                    length += 1
                    temp = temp.next
                
                return length
        
        return 0
