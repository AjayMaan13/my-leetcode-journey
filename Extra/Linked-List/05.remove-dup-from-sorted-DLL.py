"""
REMOVE DUPLICATES FROM SORTED DOUBLY LINKED LIST

Problem: Given head of sorted DLL, remove all duplicate occurrences 
so only distinct values remain.

Example 1:
Input: 1 <-> 1 <-> 3 <-> 3 <-> 4 <-> 5
Output: 1 <-> 3 <-> 4 <-> 5

Example 2:
Input: 1 <-> 1 <-> 1 <-> 1 <-> 1 <-> 2
Output: 1 <-> 2
"""


# ==============================================================================
# NODE DEFINITION
# ==============================================================================

class Node:
    """Node class for doubly linked list"""
    def __init__(self, value):
        self.data = value
        self.prev = None
        self.next = None


# ==============================================================================
# OPTIMAL SOLUTION
# ==============================================================================
# Time Complexity: O(n) - single pass
# Space Complexity: O(1) - only pointers

class Solution:
    def removeDuplicates(self, head):
        """
        Remove duplicates from sorted DLL, keep one occurrence.
        
        Strategy:
        1. Start at head
        2. For each node, skip all duplicates
        3. Link current to next distinct value
        4. Continue until end
        
        Key Insight: List is SORTED, so duplicates are adjacent!
        
        Visual Example: 1 <-> 1 <-> 3 <-> 3 <-> 4
        
        Step 1: At 1
          Current: 1
          Next: 1 (duplicate)
          Skip to: 3
          Link: 1 <-> 3
        
        Step 2: At 3
          Current: 3
          Next: 3 (duplicate)
          Skip to: 4
          Link: 3 <-> 4
        
        Step 3: At 4
          Current: 4
          Next: None
          Done!
        
        Result: 1 <-> 3 <-> 4 ✓
        
        Time: O(n) - visit each node once
        Space: O(1) - only pointers
        """
        if not head:
            return None
        
        current = head
        
        # Traverse until second-to-last node
        while current and current.next:
            nextDistinct = current.next
            
            # Skip all nodes with same value as current
            while nextDistinct and nextDistinct.data == current.data:
                nextDistinct = nextDistinct.next
            
            # Link current to next distinct node
            current.next = nextDistinct
            if nextDistinct:
                nextDistinct.prev = current
            
            # Move to next distinct node
            current = nextDistinct
        
        return head


# ==============================================================================
# ALTERNATIVE: SIMPLER VERSION (SAME LOGIC)
# ==============================================================================

class Solution_Simple:
    def removeDuplicates(self, head):
        """
        Simpler version with clearer logic.
        
        For each node, if next has same value, skip it.
        Continue until next has different value or is None.
        """
        if not head:
            return None
        
        current = head
        
        while current:
            # Skip all duplicates of current value
            while current.next and current.next.data == current.data:
                current.next = current.next.next
                if current.next:
                    current.next.prev = current
            
            # Move to next distinct value
            current = current.next
        
        return head
