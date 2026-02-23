"""
142. LINKED LIST CYCLE II

Problem Statement:
Given the head of a linked list, return the node where the cycle begins.
If there is no cycle, return null.

There is a cycle if some node can be reached again by continuously following 
the next pointer.

Do not modify the linked list.

Example 1:
Input: head = [3,2,0,-4], pos = 1
Output: tail connects to node index 1
Explanation: There is a cycle, tail connects to the second node.

Example 2:
Input: head = [1,2], pos = 0
Output: tail connects to node index 0
Explanation: There is a cycle, tail connects to the first node.

Example 3:
Input: head = [1], pos = -1
Output: null
Explanation: There is no cycle.
"""


# Definition for singly-linked list
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


# ==============================================================================
# APPROACH 1: YOUR FIRST SOLUTION (HASH SET)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(n) - storing nodes in set

class Solution_HashSet:
    def detectCycle(self, head):
        """
        Use hash set to track visited nodes.
        
        Strategy:
        1. Traverse list, storing each node in set
        2. If we encounter a node already in set, it's cycle start
        3. If we reach None, no cycle exists
        
        This works and is simple to understand.
        Space: O(n) for the set
        
        Good for initial solution, but interviewer may ask for O(1) space.
        """
        if not head:
            return None
        
        seen = set()  # Store visited nodes
        curr = head
        
        while curr:
            # If we've seen this node before, it's the cycle start
            if curr in seen:
                return curr
            
            # Mark node as visited
            seen.add(curr)
            curr = curr.next
        
        # Reached end without cycle
        return None


# ==============================================================================
# APPROACH 2: YOUR SECOND SOLUTION (FLOYD'S ALGORITHM - OPTIMAL)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(1) - only two pointers!
#
# This is the OPTIMAL solution!

class Solution:
    def detectCycle(self, head):
        """
        Floyd's algorithm with detailed step-by-step explanation.
        
        Why this works - Mathematical Intuition:
        
        Imagine a race track with a straight path then a circular loop.
        
        Setup:
        - Head to cycle start: distance 'a'
        - Cycle start to meeting point: distance 'b'  
        - Remaining cycle: distance 'c'
        - Total cycle length: b + c
        
        Phase 1 - Detection:
        When slow and fast meet inside cycle:
        - Slow has traveled: a + b (entered cycle, moved b inside)
        - Fast has traveled: a + b + k(b + c) where k ≥ 1
          (fast did extra full loops)
        
        Since fast = 2 × slow:
        a + b + k(b + c) = 2(a + b)
        a + b + k(b + c) = 2a + 2b
        k(b + c) = a + b
        
        For k = 1 (simplest case):
        b + c = a + b
        c = a  ← KEY INSIGHT!
        
        Phase 2 - Finding Start:
        Since c = a, if we:
        - Start one pointer at head (distance a to cycle start)
        - Start other at meeting point (distance c to cycle start)
        - Move both at same speed
        They will meet exactly at cycle start!
        """
        if not head or not head.next:
            return None
        
        # Phase 1: Detect if cycle exists using slow-fast pointers
        slow = fast = head
        
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            
            # Cycle detected! slow and fast met
            if slow == fast:
                # Phase 2: Find cycle start
                # Move one pointer to head, keep other at meeting point
                # Move both one step at a time
                while slow != head:
                    slow = slow.next
                    head = head.next
                
                # When they meet, that's the cycle start
                return head
        
        # No cycle found
        return None


# ==============================================================================
# APPROACH 3: WITH CYCLE LENGTH CALCULATION (EDUCATIONAL)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(1)

class Solution_WithCycleLength:
    def detectCycle(self, head):
        """
        Alternative approach that first calculates cycle length.
        
        Not necessary for this problem but educational.
        Shows you can find cycle length before finding start.
        """
        if not head or not head.next:
            return None
        
        # Phase 1: Detect cycle
        slow = fast = head
        
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            
            if slow == fast:
                # Found cycle, calculate its length
                cycle_length = 1
                temp = slow.next
                while temp != slow:
                    cycle_length += 1
                    temp = temp.next
                
                # Phase 2: Use cycle length to find start
                # Move one pointer ahead by cycle_length
                ptr1 = ptr2 = head
                for _ in range(cycle_length):
                    ptr1 = ptr1.next
                
                # Move both at same speed
                # When they meet, it's at cycle start
                while ptr1 != ptr2:
                    ptr1 = ptr1.next
                    ptr2 = ptr2.next
                
                return ptr1
        
        return None
