"""
PAIRS WITH GIVEN SUM IN DOUBLY LINKED LIST

Problem: Given head of sorted DLL of positive distinct integers and target,
return all unique pairs (a, b) where a + b = target and a < b.

Example 1:
Input: head = [1, 2, 4, 5, 6, 8, 9], target = 7
Output: [[1, 6], [2, 5]]

Example 2:
Input: head = [1, 5, 6], target = 6
Output: [[1, 5]]
"""


# Definition of doubly linked list
class ListNode:
    def __init__(self, val=0, next=None, prev=None):
        self.val = val
        self.next = next
        self.prev = prev


# ==============================================================================
# OPTIMAL SOLUTION: TWO POINTER APPROACH
# ==============================================================================
# Time Complexity: O(n) - single pass with two pointers
# Space Complexity: O(1) - excluding result array

class Solution:
    def findPairsWithSum(self, head, target):
        """
        Use two pointers (start and end) moving toward each other.
        
        Strategy:
        1. Get tail of list (last node)
        2. Use left pointer at head, right pointer at tail
        3. If sum == target: add pair, move both inward
        4. If sum < target: move left forward
        5. If sum > target: move right backward
        6. Continue until pointers meet
        
        Why this works:
        - List is SORTED
        - Two pointer technique works like in sorted array!
        - DLL has prev pointer, so we can move backward
        
        Visual Example: [1, 2, 4, 5, 6, 8, 9], target = 7
        
        Step 1:
          L: 1, R: 9
          1 + 9 = 10 > 7 → move R left
        
        Step 2:
          L: 1, R: 8
          1 + 8 = 9 > 7 → move R left
        
        Step 3:
          L: 1, R: 6
          1 + 6 = 7 ✓ → add [1,6], move both
        
        Step 4:
          L: 2, R: 5
          2 + 5 = 7 ✓ → add [2,5], move both
        
        Step 5:
          L: 4, R: 4 (same node) → stop
        
        Result: [[1,6], [2,5]]
        
        This is OPTIMAL - O(n) time, O(1) space!
        """
        if not head:
            return []
        
        # Step 1: Find tail of list
        tail = head
        while tail.next:
            tail = tail.next
        
        # Step 2: Two pointers from start and end
        left = head
        right = tail
        result = []
        
        # Step 3: Move pointers toward each other
        while left != right and left.prev != right:
            # Calculate sum
            current_sum = left.val + right.val
            
            if current_sum == target:
                # Found a pair!
                result.append([left.val, right.val])
                # Move both pointers
                left = left.next
                right = right.prev
            
            elif current_sum < target:
                # Need larger sum, move left forward
                left = left.next
            
            else:  # current_sum > target
                # Need smaller sum, move right backward
                right = right.prev
        
        return result


# ==============================================================================
# ALTERNATIVE: HASH SET APPROACH
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(n) - hash set

class Solution_HashSet:
    def findPairsWithSum(self, head, target):
        """
        Use hash set to track seen values.
        
        Strategy:
        1. Traverse list once
        2. For each value, check if (target - value) exists in set
        3. Add current value to set
        
        This works but uses O(n) space.
        Two-pointer is better for sorted DLL!
        """
        if not head:
            return []
        
        seen = set()
        result = []
        curr = head
        
        while curr:
            complement = target - curr.val
            
            # Check if complement was seen before
            if complement in seen:
                # Add pair (smaller first)
                result.append([complement, curr.val])
            
            # Add current value to seen
            seen.add(curr.val)
            curr = curr.next
        
        return result
