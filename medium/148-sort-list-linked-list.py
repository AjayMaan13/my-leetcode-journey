"""
148. SORT LIST

Problem Statement:
Given the head of a linked list, return the list after sorting it in 
ascending order.

Example 1:
Input: head = [4,2,1,3]
Output: [1,2,3,4]

Example 2:
Input: head = [-1,5,3,4,0]
Output: [-1,0,3,4,5]

Example 3:
Input: head = []
Output: []

Follow-up: Can you sort in O(n log n) time and O(1) space?
"""


# Definition for singly-linked list
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ==============================================================================
# APPROACH 1: YOUR FIRST SOLUTION (ARRAY CONVERSION)
# ==============================================================================
# Time Complexity: O(n log n) - sorting array
# Space Complexity: O(n) - storing all values in array

class Solution_Array:
    def sortList(self, head):
        """
        Convert to array, sort, then modify list values.
        
        Strategy:
        1. Extract all values into array
        2. Sort the array
        3. Write sorted values back to list
        
        Pros: Simple, easy to implement
        Cons: Uses O(n) extra space
        
        Time: O(n log n) - Python's sort is Timsort
        Space: O(n) - array stores all values
        """
        if not head:
            return head
        
        # Step 1: Extract values into array
        ll = []
        curr = head
        while curr:
            ll.append(curr.val)
            curr = curr.next
        
        # Step 2: Sort array
        ll.sort()  # O(n log n)
        
        # Step 3: Write sorted values back to list
        curr = head
        index = 0
        while curr:
            curr.val = ll[index]
            index += 1
            curr = curr.next
        
        return head


# ==============================================================================
# APPROACH 2: YOUR SECOND SOLUTION (MERGE SORT - TOP DOWN)
# ==============================================================================
# Time Complexity: O(n log n)
# Space Complexity: O(log n) - recursion stack

class Solution_MergeSortTopDown:
    def sortList(self, head):
        """
        Merge sort using recursion (top-down).
        
        Strategy:
        1. Find middle of list
        2. Split into two halves
        3. Recursively sort each half
        4. Merge sorted halves
        
        This is BETTER than array approach!
        
        Time: O(n log n)
        Space: O(log n) - recursion depth
        
        Your implementation is correct but can be simplified.
        """
        if not head or not head.next:
            return head
        
        def merge(l, r):
            """Merge two sorted lists"""
            dummy = ListNode(0)
            curr = dummy
            
            # Merge while both have nodes
            while l and r:
                if l.val <= r.val:
                    curr.next = l
                    l = l.next
                else:
                    curr.next = r
                    r = r.next
                curr = curr.next
            
            # Attach remaining nodes (only one will have nodes left)
            curr.next = l or r
            
            return dummy.next
        
        # Find middle using slow-fast pointers
        dummy = ListNode(0)
        dummy.next = head
        slow = fast = dummy
        
        # Move slow to node before middle
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        # Split list
        mid = slow.next
        slow.next = None  # Cut the list
        
        # Recursively sort both halves
        left = self.sortList(head)
        right = self.sortList(mid)
        
        # Merge sorted halves
        return merge(left, right)


# ==============================================================================
# APPROACH 3: MERGE SORT BOTTOM-UP (OPTIMAL - O(1) SPACE!)
# ==============================================================================
# Time Complexity: O(n log n)
# Space Complexity: O(1) - no recursion!
#
# This is the OPTIMAL solution for follow-up!

class Solution:
    def sortList(self, head):
        """
        Merge sort using iteration (bottom-up) - achieves O(1) space!
        
        Strategy:
        1. Start with sublists of size 1
        2. Merge pairs of sublists (size 1 → 2 → 4 → 8 → ...)
        3. Double sublist size each iteration
        4. Continue until entire list is sorted
        
        This avoids recursion, achieving O(1) extra space!
        
        Visual Example: [4,2,1,3]
        
        Step 1 (size=1): Merge pairs of 1
            [4,2] → [2,4]
            [1,3] → [1,3]
            Result: [2,4,1,3]
        
        Step 2 (size=2): Merge pairs of 2
            [2,4] and [1,3] → [1,2,3,4]
            Result: [1,2,3,4] ✓
        
        Time: O(n log n) - log n iterations, each O(n)
        Space: O(1) - only pointers!
        
        This is the GOLD STANDARD solution!
        """
        if not head or not head.next:
            return head
        
        # Get length of list
        length = 0
        curr = head
        while curr:
            length += 1
            curr = curr.next
        
        # Dummy node to handle edge cases
        dummy = ListNode(0)
        dummy.next = head
        
        # Start with sublist size 1, double each iteration
        size = 1
        while size < length:
            curr = dummy.next  # Start of current iteration
            tail = dummy       # Tail of merged list
            
            # Merge pairs of sublists of current size
            while curr:
                # Get first sublist of 'size' nodes
                left = curr
                right = self.split(left, size)
                
                # Get second sublist of 'size' nodes
                curr = self.split(right, size)
                
                # Merge the two sublists
                tail = self.merge(left, right, tail)
            
            # Double the sublist size for next iteration
            size *= 2
        
        return dummy.next
    
    def split(self, head, size):
        """
        Split list after 'size' nodes, return start of second part.
        
        Args:
            head: Start of sublist
            size: Number of nodes in first part
            
        Returns:
            Head of second part (or None)
        """
        # Move size-1 steps (to get to last node of first part)
        for i in range(size - 1):
            if not head:
                break
            head = head.next
        
        if not head:
            return None
        
        # Split here
        next_head = head.next
        head.next = None
        return next_head
    
    def merge(self, l1, l2, tail):
        """
        Merge two sorted lists, attach to tail.
        
        Args:
            l1: First sorted list
            l2: Second sorted list
            tail: Last node of result list so far
            
        Returns:
            New tail after merging
        """
        curr = tail
        
        # Merge while both lists have nodes
        while l1 and l2:
            if l1.val < l2.val:
                curr.next = l1
                l1 = l1.next
            else:
                curr.next = l2
                l2 = l2.next
            curr = curr.next
        
        # Attach remaining nodes
        curr.next = l1 or l2
        
        # Move to end of merged list
        while curr.next:
            curr = curr.next
        
        return curr
