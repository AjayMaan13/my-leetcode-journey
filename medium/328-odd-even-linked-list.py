"""
328. ODD EVEN LINKED LIST

Problem Statement:
Given the head of a singly linked list, group all the nodes with odd indices 
together followed by the nodes with even indices, and return the reordered list.

The first node is considered odd, and the second node is even, and so on.

Note: The relative order inside both groups should remain as it was in the input.

You must solve in O(1) extra space and O(n) time complexity.

Example 1:
Input: head = [1,2,3,4,5]
Output: [1,3,5,2,4]
Explanation: Odd indices (1,3,5), then even indices (2,4)

Example 2:
Input: head = [2,1,3,5,6,4,7]
Output: [2,3,6,7,1,5,4]
Explanation: Odd indices (2,3,6,7), then even indices (1,5,4)
"""


# Definition for singly-linked list
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ==============================================================================
# APPROACH 1: YOUR SOLUTION (OPTIMAL - CLEAN)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(1)
#
# This is already OPTIMAL!

class Solution:
    def oddEvenList(self, head):
        """
        Separate odd and even positioned nodes, then connect them.
        
        Strategy:
        1. Use two pointers: odd and even
        2. Connect odd nodes together, even nodes together
        3. Finally, connect end of odd list to start of even list
        
        Key Insight: We rearrange pointers, not create new nodes.
        This achieves O(1) space complexity!
        
        Visual Example: [1,2,3,4,5]
        
        Initial:
            1 → 2 → 3 → 4 → 5
            ↑   ↑
          odd  even
        
        After separating:
            Odd:  1 → 3 → 5
            Even: 2 → 4
        
        After connecting:
            1 → 3 → 5 → 2 → 4
        
        This is the OPTIMAL solution!
        """ 
        # Edge case: empty or single node
        if not head or not head.next:
            return head
        
        # Set up three pointers:
        # 1. odd: current position in odd list
        # 2. even: current position in even list
        # 3. evenStart: to remember where even list begins
        odd = head
        even = head.next
        evenStart = even  # Save this to connect later!
        
        # Loop while we have even nodes to process
        # Need 'even' (current even) and 'even.next' (next odd)
        while even and even.next:
            # Step 1: Connect current odd to next odd node
            # Skip over the even node between them
            odd.next = even.next
            # Example: 1.next = 3 (skipping 2)
            
            # Step 2: Connect current even to next even node
            # Skip over the odd node between them
            even.next = even.next.next
            # Example: 2.next = 4 (skipping 3)
            
            # Step 3: Move both pointers forward
            odd = odd.next    # Move to next odd
            even = even.next  # Move to next even
        
        # Step 4: Connect end of odd list to start of even list
        # This combines both chains
        odd.next = evenStart
        
        return head


# ==============================================================================
# APPROACH 2: ITERATIVE WITH CLEAR SEPARATION
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(1)

class Solution_Separated:
    def oddEvenList(self, head):
        """
        Alternative way to think about it with clear separation.
        
        Build odd and even lists separately, then merge.
        """
        if not head or not head.next:
            return head
        
        # Build separate odd and even lists
        oddHead = oddTail = head
        evenHead = evenTail = head.next
        
        # Start from third node
        current = head.next.next
        position = 3  # Track if current position is odd or even
        
        while current:
            if position % 2 == 1:  # Odd position
                oddTail.next = current
                oddTail = oddTail.next
            else:  # Even position
                evenTail.next = current
                evenTail = evenTail.next
            
            current = current.next
            position += 1
        
        # Terminate even list and connect lists
        evenTail.next = None
        oddTail.next = evenHead
        
        return oddHead
