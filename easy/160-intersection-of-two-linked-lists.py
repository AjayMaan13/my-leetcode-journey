"""
160. INTERSECTION OF TWO LINKED LISTS

Problem Statement:
Given the heads of two singly linked-lists headA and headB, return the node 
at which the two lists intersect. If no intersection, return null.

IMPORTANT: Intersection means same node REFERENCE, not just same VALUE!

Example 1:
Input: intersectVal = 8, listA = [4,1,8,4,5], listB = [5,6,1,8,4,5], 
       skipA = 2, skipB = 3
Output: Intersected at '8'

Example 2:
Input: intersectVal = 2, listA = [1,9,1,2,4], listB = [3,2,4], 
       skipA = 3, skipB = 1
Output: Intersected at '2'

Example 3:
Input: intersectVal = 0, listA = [2,6,4], listB = [1,5], skipA = 3, skipB = 2
Output: No intersection

Follow-up: Can you solve in O(m+n) time and O(1) space?
"""


# Definition for singly-linked list
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


# ==============================================================================
# APPROACH 1: YOUR FIRST SOLUTION (HASH SET)
# ==============================================================================
# Time Complexity: O(m + n)
# Space Complexity: O(m) - storing nodes of first list

class Solution_HashSet:
    def getIntersectionNode(self, headA, headB):
        """
        Use hash set to store all nodes of list A, then check list B.
        
        Strategy:
        1. Traverse list A, store all nodes in set
        2. Traverse list B, check if any node is in set
        3. First match is the intersection point
        
        This works but uses O(m) extra space.
        
        Time: O(m + n)
        Space: O(m)
        """
        seen = set()
        curr = headA
        
        # Store all nodes of list A
        while curr:
            seen.add(curr)
            curr = curr.next
        
        # Check nodes of list B
        curr = headB
        while curr:
            if curr in seen:
                return curr  # Found intersection!
            curr = curr.next
        
        return None


# ==============================================================================
# APPROACH 2: YOUR SECOND SOLUTION (LENGTH DIFFERENCE)
# ==============================================================================
# Time Complexity: O(m + n)
# Space Complexity: O(1) - only using pointers!

class Solution_LengthDiff:
    def getIntersectionNode(self, headA, headB):
        """
        Calculate lengths, align starts, then move together.
        
        Strategy:
        1. Calculate length of both lists
        2. Advance longer list by (lenA - lenB)
        3. Move both pointers together until they meet
        
        Visual Example:
        A: 4 → 1 → 8 → 4 → 5  (length 5)
        B: 5 → 6 → 1 → 8 → 4 → 5  (length 6)
        
        Difference: 1
        Advance B by 1: B starts at 6
        
        Now aligned:
        A:      4 → 1 → 8 → 4 → 5
        B:      6 → 1 → 8 → 4 → 5
        
        Move together, they meet at 8!
        
        This achieves O(1) space!
        
        Time: O(m + n)
        Space: O(1)
        """
        if not headA or not headB:
            return None
        
        # Step 1: Compute lengths
        lenA = lenB = 0
        currA, currB = headA, headB
        
        while currA:
            lenA += 1
            currA = currA.next
        
        while currB:
            lenB += 1
            currB = currB.next
        
        # Step 2: Align starts by advancing longer list
        currA, currB = headA, headB
        
        if lenA > lenB:
            # List A is longer, advance it
            for _ in range(lenA - lenB):
                currA = currA.next
        else:
            # List B is longer, advance it
            for _ in range(lenB - lenA):
                currB = currB.next
        
        # Step 3: Move together until they meet
        while currA and currB:
            if currA == currB:
                return currA  # Found intersection!
            currA = currA.next
            currB = currB.next
        
        return None


# ==============================================================================
# APPROACH 3: TWO POINTER SWITCHING (MOST ELEGANT!)
# ==============================================================================
# Time Complexity: O(m + n)
# Space Complexity: O(1)
#
# This is the OPTIMAL and most ELEGANT solution!

class Solution:
    def getIntersectionNode(self, headA, headB):
        """
        Two pointers that switch lists when reaching end.
        
        Key Insight: When pointers switch lists, they traverse equal distance!
        
        Strategy:
        1. Start pA at headA, pB at headB
        2. When pA reaches end, redirect to headB
        3. When pB reaches end, redirect to headA
        4. They will meet at intersection (or both become None)
        
        Why this works:
        - Let a = length before intersection in A
        - Let b = length before intersection in B  
        - Let c = length of common part
        
        First traversal:
        - pA travels: a + c (list A) + b (to intersection in B)
        - pB travels: b + c (list B) + a (to intersection in A)
        
        Both travel: a + b + c distance!
        They meet at intersection point!
        
        Visual Example:
        A: 4 → 1 → 8 → 4 → 5
        B: 5 → 6 → 1 → 8 → 4 → 5
        
        Iteration by iteration:
        
        Start:
          pA: 4       pB: 5
        
        Step 1:
          pA: 1       pB: 6
        
        Step 2:
          pA: 8       pB: 1
        
        Step 3:
          pA: 4       pB: 8
        
        Step 4:
          pA: 5       pB: 4
        
        Step 5:
          pA: None    pB: 5
          pA switches to headB
        
        Step 6:
          pA: 5       pB: None
          pB switches to headA
        
        Step 7:
          pA: 6       pB: 4
        
        Step 8:
          pA: 1       pB: 1
        
        Step 9:
          pA: 8       pB: 8  ← MEET!
        
        Return 8
        
        This is BRILLIANT and OPTIMAL!
        
        Time: O(m + n) - each pointer traverses at most m + n nodes
        Space: O(1) - only two pointers!
        """

        if not headA or not headB:
            return None
        
        pA = headA
        pB = headB
        
        # The magic: when one pointer reaches end, redirect to other list
        # This ensures both pointers travel the same total distance
        
        # Example with no intersection:
        # A: [1,2,3]  B: [4,5]
        # pA path: 1→2→3→None→4→5→None
        # pB path: 4→5→None→1→2→3→None
        # Both end at None together!
        
        # Example with intersection:
        # A: [1,2,8,9]  B: [3,8,9]  (intersect at 8)
        # pA path: 1→2→8→9→None→3→8  (meets at 8)
        # pB path: 3→8→9→None→1→2→8  (meets at 8)
        # Both meet at intersection!
        
        while pA != pB:
            # Move to next or switch lists
            if pA:
                pA = pA.next
            else:
                pA = headB  # Switch to list B
            
            if pB:
                pB = pB.next
            else:
                pB = headA  # Switch to list A
        
        # pA == pB (either intersection node or both None)
        return pA

