"""
206. REVERSE LINKED LIST

Problem Statement:
Given the head of a singly linked list, reverse the list, and return the 
reversed list.

Example 1:
Input: head = [1,2,3,4,5]
Output: [5,4,3,2,1]

Example 2:
Input: head = [1,2]
Output: [2,1]

Example 3:
Input: head = []
Output: []
"""


# Definition for singly-linked list
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ==============================================================================
# APPROACH 1: YOUR SOLUTION (WORKS BUT COMPLEX)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(1)

class Solution_YourApproach:
    def reverseList(self, head):
        """
        Your approach with if-else for first node handling.
        
        This works but has unnecessary complexity with the if-else.
        The logic can be simplified.
        """
        if not head:
            return head
        
        reverse = None
        
        while head:
            newHead = head.next
            
            if reverse:
                # Not first node
                temp = reverse
                reverse = head
                reverse.next = temp
                head = newHead
            else:
                # First node - special handling
                reverse = head
                reverse.next = None
            
            head = newHead
        
        return reverse


# ==============================================================================
# APPROACH 2: ITERATIVE (OPTIMAL & CLEANEST)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(1)

class Solution_Verbose:
    def reverseList(self, head):
        """
        Same as Approach 2 but with detailed comments for understanding.
        
        The three-pointer technique:
        - prev: points to already-reversed portion
        - curr: current node being processed
        - next: temporary to not lose rest of list
        """
        # Initialize: prev is None (new tail will point to None)
        prev = None
        
        # Start from head
        curr = head
        
        # Process each node
        while curr is not None:
            # CRITICAL: Save next node before we break the link!
            # If we don't do this, we lose the rest of the list
            next_temp = curr.next
            
            # Reverse the current node's pointer
            # Make it point backwards instead of forwards
            curr.next = prev
            
            # Move our pointers one step forward
            # prev becomes current node (for next iteration)
            prev = curr
            # curr becomes next node (continue traversal)
            curr = next_temp
        
        # When loop ends, curr is None and prev is the new head
        return prev