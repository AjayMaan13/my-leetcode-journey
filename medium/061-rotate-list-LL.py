"""
61. ROTATE LIST

Problem Statement:
Given the head of a linked list, rotate the list to the right by k places.

Example 1:
Input: head = [1,2,3,4,5], k = 2
Output: [4,5,1,2,3]
Explanation:
  Rotate 1: [5,1,2,3,4]
  Rotate 2: [4,5,1,2,3]

Example 2:
Input: head = [0,1,2], k = 4
Output: [2,0,1]
Explanation:
  k=4 is same as k=1 (since 4 % 3 = 1)
  Rotate 1: [2,0,1]

Constraints:
* 0 <= number of nodes <= 500
* -100 <= Node.val <= 100
* 0 <= k <= 2 * 10^9

Key Insight: k can be very large! Need to use k % length.
"""


# ==============================================================================
# NODE DEFINITION
# ==============================================================================

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ==============================================================================
# SOLUTION 1: YOUR FIRST SOLUTION (TWO-POINTER APPROACH)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(1)

class Solution_TwoPointer:
    def rotateRight(self, head, k):
        """
        Use two pointers with gap of k to find new tail.
        
        Strategy:
        1. Find length of list
        2. Normalize k (k = k % length)
        3. Use two pointers k steps apart
        4. Move both until last reaches end
        5. Reconnect: last.next = head, prev.next = None
        
        This works and uses O(1) space!
        
        Time: O(n) - two passes
        Space: O(1)
        """
        if not head or not head.next or k < 1:
            return head

        def findLength(head):
            """Helper to find length"""
            curr = head
            length = 0
            while curr:
                curr = curr.next
                length += 1
            return length

        dummy = ListNode(0)
        dummy.next = head
        length = findLength(head)

        # Normalize k
        if k >= length:
            k = k % length
            if k == 0:
                return dummy.next

        # Two pointers: gap of k
        prev = last = dummy
        initialJump = 0
        
        # Move last pointer k steps ahead
        while initialJump < k:
            last = last.next
            initialJump += 1

        # Move both until last reaches end
        while last.next:
            prev = prev.next
            last = last.next

        # Reconnect
        start = prev.next     # New head
        last.next = head      # Connect tail to old head
        dummy.next = start    # Update head
        prev.next = None      # Break the list

        return dummy.next


# ==============================================================================
# SOLUTION 2: YOUR SECOND SOLUTION (CIRCULAR LIST - OPTIMAL!)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(1)
#
# This is MORE ELEGANT! ⭐

class Solution:
    def rotateRight(self, head, k):
        """
        Make circular, find new tail, break circle.
        
        Strategy:
        1. Find length and tail
        2. Normalize k (k = k % length)
        3. Make list circular (tail.next = head)
        4. Find new tail: (length - k - 1) steps from head
        5. Break circle at new tail
        
        Why this is better:
        - More elegant (make circular, then break)
        - Single traversal to find length
        - Clearer logic
        - Fewer edge cases
        
        Visual Example: [1,2,3,4,5], k=2
        
        Step 1: Find length (5) and tail (5)
        
        Step 2: k = 2 % 5 = 2
        
        Step 3: Make circular
          1 → 2 → 3 → 4 → 5 → 1 (circle)
        
        Step 4: Find new tail
          Steps = 5 - 2 - 1 = 2
          Start at 1, move 2 steps: 1 → 2 → 3
          New tail = 3
        
        Step 5: Break circle
          New head = 4
          3.next = None
          Result: 4 → 5 → 1 → 2 → 3 ✓
        
        This is the OPTIMAL solution!
        
        Time: O(n) - single pass
        Space: O(1)
        """
        if not head or not head.next or k == 0:
            return head

        # Step 1: Find length and tail
        length = 1
        tail = head
        while tail.next:
            tail = tail.next
            length += 1

        # Step 2: Normalize k
        k %= length
        if k == 0:
            return head  # No rotation needed

        # Step 3: Make circular
        tail.next = head

        # Step 4: Find new tail
        # New tail is at position (length - k - 1) from head
        steps_to_new_tail = length - k - 1
        new_tail = head
        for _ in range(steps_to_new_tail):
            new_tail = new_tail.next

        # Step 5: Break circle
        new_head = new_tail.next
        new_tail.next = None

        return new_head


# ==============================================================================
# COMPARISON AND ANALYSIS
# ==============================================================================

"""
SOLUTION 1 (Two-Pointer):
✓ Works correctly
✓ O(1) space
✓ Two-pointer technique
❌ Two passes through list
❌ More complex reconnection logic

SOLUTION 2 (Circular List): ⭐ OPTIMAL!
✓ More elegant approach
✓ Single pass to find length
✓ Clearer logic (make circular, then break)
✓ Fewer edge cases to handle
✓ Easier to understand and explain

RECOMMENDATION:
Use Solution 2 for interviews - it's cleaner!
"""


# ==============================================================================
# DETAILED WALKTHROUGH
# ==============================================================================

"""
Example: [1,2,3,4,5], k=2

Step-by-Step:
-------------
Original: 1 → 2 → 3 → 4 → 5 → None

1. Find length and tail:
   length = 5
   tail = node 5

2. Normalize k:
   k = 2 % 5 = 2

3. Make circular:
   1 → 2 → 3 → 4 → 5 ─┐
   ↑                   │
   └───────────────────┘

4. Find new tail:
   steps_to_new_tail = 5 - 2 - 1 = 2
   Start at 1, move 2 steps: node 3
   new_tail = node 3

5. Break circle:
   new_head = node 4
   node 3.next = None
   
   Result: 4 → 5 → 1 → 2 → 3 → None ✓

Why (length - k - 1)?
---------------------
- Rotating right by k = moving last k nodes to front
- New head is at position (length - k)
- New tail is one before new head = (length - k - 1)

Example with k=2, length=5:
- New head at position 3 (5 - 2 = 3, which is node 4)
- New tail at position 2 (5 - 2 - 1 = 2, which is node 3)
"""
