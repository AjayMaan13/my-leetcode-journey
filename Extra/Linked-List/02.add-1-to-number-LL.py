"""
ADD 1 TO A NUMBER REPRESENTED BY LINKED LIST

Problem Statement:
Given the head of a singly linked list representing a positive integer number. 
Each node represents a digit of the number, with the 1st node containing the 
leftmost digit. Add one to the value and return the head.

Example 1:
Input: 4 -> 5 -> 6
Output: 4 -> 5 -> 7
Explanation: 456 + 1 = 457

Example 2:
Input: 9 -> 9 -> 9
Output: 1 -> 0 -> 0 -> 0
Explanation: 999 + 1 = 1000
"""


# ==============================================================================
# NODE DEFINITION
# ==============================================================================

class Node:
    """Node class representing a single digit in the linked list"""
    def __init__(self, value):
        self.data = value
        self.next = None


# ==============================================================================
# APPROACH 1: REVERSE, ADD, REVERSE (ITERATIVE)
# ==============================================================================
# Time Complexity: O(n) - three passes (reverse, add, reverse)
# Space Complexity: O(1) - only using pointers

class Solution_Iterative:
    def addOne(self, head):
        """
        Reverse list, add 1 from least significant digit, reverse back.
        
        Strategy:
        1. Reverse the list (most significant → least significant)
        2. Add 1 to head (now least significant digit)
        3. Propagate carry through list
        4. If carry remains, add new node
        5. Reverse list back to original order
        
        Visual Example: 4 → 5 → 9
        
        Step 1: Reverse
            9 → 5 → 4
        
        Step 2: Add 1 to 9
            9 + 1 = 10
            Node becomes 0, carry = 1
        
        Step 3: Propagate carry
            5 + 1 = 6
            Node becomes 6, carry = 0
        
        Result: 0 → 6 → 4
        
        Step 4: Reverse back
            4 → 6 → 0
        
        Final: 460 ✓
        
        Time: O(n) - three O(n) operations
        Space: O(1)
        """
        # Step 1: Reverse the list
        head = self.reverseList(head)
        
        # Step 2: Add 1 starting from head (least significant digit)
        current = head
        carry = 1
        
        while current and carry:
            sum_val = current.data + carry
            current.data = sum_val % 10
            carry = sum_val // 10
            
            # If no next node and carry exists, add new node
            if not current.next and carry:
                current.next = Node(carry)
                carry = 0
            
            current = current.next
        
        # Step 3: Reverse back to restore original order
        head = self.reverseList(head)
        return head
    
    def reverseList(self, head):
        """Reverse a linked list"""
        prev = None
        current = head
        
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        
        return prev


# ==============================================================================
# APPROACH 2: RECURSIVE (ELEGANT!)
# ==============================================================================
# Time Complexity: O(n) - single recursive pass
# Space Complexity: O(n) - recursion stack
#
# This is MORE ELEGANT than iterative!

class Solution:
    def addOne(self, head):
        """
        Use recursion to reach the end, then propagate carry back.
        
        Strategy:
        1. Recursively traverse to the end
        2. Base case: return carry = 1
        3. On way back, add carry to each node
        4. Propagate carry up the recursion
        5. If final carry exists, add new head
        
        Why this is elegant:
        - No need to reverse list!
        - Handles carry naturally through recursion
        - Cleaner code than reverse approach
        
        Visual Example: 9 → 9 → 9
        
        Recursion stack (going down):
        addOneUtil(9) →
          addOneUtil(9) →
            addOneUtil(9) →
              addOneUtil(None) → return 1 (base case)
            9 + 1 = 10 → node.data = 0, return 1
          9 + 1 = 10 → node.data = 0, return 1
        9 + 1 = 10 → node.data = 0, return 1
        
        Final carry = 1, so add new head: 1 → 0 → 0 → 0 ✓
        
        This is the RECOMMENDED solution!
        
        Time: O(n) - one recursive pass
        Space: O(n) - recursion stack
        """
        # Get carry after recursive addition
        carry = self.addOneUtil(head)
        
        # If carry remains, add new head node
        if carry:
            new_head = Node(carry)
            new_head.next = head
            return new_head
        
        return head
    
    def addOneUtil(self, node):
        """
        Recursive helper to add one and return carry.
        
        Returns:
            carry (0 or 1)
        """
        # Base case: reached beyond last node, return initial carry
        if not node:
            return 1
        
        # Recurse to the end first
        carry = self.addOneUtil(node.next)
        
        # Add carry to current node
        total = node.data + carry
        node.data = total % 10
        
        # Return new carry for previous node
        return total // 10

