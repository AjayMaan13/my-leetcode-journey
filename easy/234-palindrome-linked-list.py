"""
234. PALINDROME LINKED LIST

Problem Statement:
Given the head of a singly linked list, return true if it is a palindrome 
or false otherwise.

Example 1:
Input: head = [1,2,2,1]
Output: true

Example 2:
Input: head = [1,2]
Output: false

Example 3:
Input: head = [1,2,3,2,1]
Output: true
"""


# Definition for singly-linked list
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ==============================================================================
# APPROACH 1: YOUR SOLUTION (CONVERT TO ARRAY)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(n) - storing all values in array

class Solution_Array:
    def isPalindrome(self, head):
        """
        Convert linked list to array and check palindrome.
        
        Strategy:
        1. Traverse list and store all values in array
        2. Use two pointers to check if array is palindrome
        
        Simple and works, but uses O(n) extra space.
        Good initial solution in interviews.
        """
        if not head:
            return False
        
        # Store all values in array
        seen = []
        curr = head
        while curr:
            seen.append(curr.val)
            curr = curr.next
        
        # Check palindrome using two pointers
        l, r = 0, len(seen) - 1
        while l < r:
            if seen[l] != seen[r]:
                return False
            l += 1
            r -= 1
        
        return True



# ==============================================================================
# APPROACH 2: REVERSE SECOND HALF (OPTIMAL - O(1) SPACE)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(1) - only using pointers!
#
# This is the OPTIMAL solution!

class Solution:
    def isPalindrome(self, head):
        """
        Find middle, reverse second half, compare both halves.
        
        Strategy:
        1. Find middle of list using slow-fast pointers
        2. Reverse second half of list
        3. Compare first half with reversed second half
        4. (Optional) Restore list to original state
        
        This achieves O(1) space - the optimal solution!
        
        Visual Example: [1,2,3,2,1]
        
        Step 1: Find middle
            slow → 3 (middle)
            1 → 2 → 3 → 2 → 1
                    ↑
                  middle
        
        Step 2: Reverse second half (from middle)
            1 → 2 → 3    1 ← 2
                    ↑         ↑
                  first    second
        
        Step 3: Compare
            1 == 1 ✓
            2 == 2 ✓
            3 (middle, stop)
        
        Result: Palindrome!
        """
        if not head or not head.next:
            return True
        
        # STEP 1: Find the middle of the linked list
        # For odd length: slow will be at exact middle
        # For even length: slow will be at start of second half
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        # Examples:
        # [1,2,3,2,1]: slow at 3 (middle)
        # [1,2,2,1]: slow at first 2 (start of second half)
        
        # STEP 2: Reverse the second half of the list
        # slow is at the middle/start of second half
        second_half_head = self.reverseList(slow)
        
        # Now we have:
        # First half: head → ... → middle
        # Second half (reversed): second_half_head → ... → end
        
        # STEP 3: Compare both halves
        first = head
        second = second_half_head
        
        # We compare until second half ends
        # (second half is equal or one less than first half)
        while second:
            if first.val != second.val:
                # Values don't match - not a palindrome
                return False
            first = first.next
            second = second.next
        
        # All values matched - it's a palindrome!
        return True
    
    def reverseList(self, head):
        """Reverse linked list and return new head"""
        prev = None
        curr = head
        
        while curr:
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node
        
        return prev


# ==============================================================================
# APPROACH 3: WITH LIST RESTORATION (BEST PRACTICE)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(1)

class Solution_Restore:
    def isPalindrome(self, head):
        """
        Same as optimal but restores original list structure.
        
        Good practice to restore the list since we modified it.
        """
        if not head or not head.next:
            return True
        
        # Find middle
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        # Reverse second half
        second_half = self.reverseList(slow)
        
        # Compare both halves
        first = head
        second = second_half
        is_palindrome = True
        
        while second:
            if first.val != second.val:
                is_palindrome = False
                break  # Still need to restore list
            first = first.next
            second = second.next
        
        # Restore original list structure
        self.reverseList(slow)
        
        return is_palindrome
    
    def reverseList(self, head):
        """Reverse linked list"""
        prev = None
        curr = head
        
        while curr:
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node
        
        return prev

