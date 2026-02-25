"""
25. REVERSE NODES IN K-GROUP

Problem Statement:
Given the head of a linked list, reverse the nodes of the list k at a time, 
and return the modified list.

k is a positive integer and is less than or equal to the length of the linked 
list. If the number of nodes is not a multiple of k then left-out nodes, in 
the end, should remain as it is.

You may not alter the values in the list's nodes, only nodes themselves may 
be changed.

Example 1:
Input: head = [1,2,3,4,5], k = 2
Output: [2,1,4,3,5]
Explanation:
  Group 1: Reverse [1,2] → [2,1]
  Group 2: Reverse [3,4] → [4,3]
  Group 3: [5] remains as is (< k nodes)

Example 2:
Input: head = [1,2,3,4,5], k = 3
Output: [3,2,1,4,5]
Explanation:
  Group 1: Reverse [1,2,3] → [3,2,1]
  Group 2: [4,5] remains as is (< k nodes)

Constraints:
* The number of nodes in the list is n.
* 1 <= k <= n <= 5000
* 0 <= Node.val <= 1000

Follow-up: Can you solve the problem in O(1) extra memory space?
"""

# ==============================================================================
# SOLUTION 1: ARRAY CONVERSION (YOUR FIRST SOLUTION)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(n) - stores all values

class Solution_Array:
    def reverseKGroup(self, head, k):
        """
        Convert to array, reverse groups, write back.
        
        Strategy:
        1. Extract all values to array
        2. Reverse array values in groups of k
        3. Write values back to list
        
        Pros: Simple to understand
        Cons: Uses O(n) space, modifies values (violates constraint)
        
        Note: Problem says "only nodes may be changed", not values!
        This technically violates the constraint.
        """
        if not head or k < 2:
            return head

        res = []
        sublist = []
        curr = head
        count = 0

        # Extract values and reverse in groups
        while curr:
            count += 1
            sublist.append(curr.val)

            if count == k:
                res.extend(reversed(sublist))
                sublist = []
                count = 0

            curr = curr.next

        # Add remaining nodes (< k) as is
        if sublist:
            res.extend(sublist)

        # Write values back
        count = 0
        curr = head
        while curr:
            curr.val = res[count]
            curr = curr.next
            count += 1
        
        return head


# ==============================================================================
# SOLUTION 2: ITERATIVE POINTER REVERSAL (YOUR SECOND SOLUTION - OPTIMAL!)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(1) - only pointers!
#
# This is PERFECT! ⭐

class Solution:
    def reverseKGroup(self, head, k):
        """
        Reverse links in-place using pointers.
        
        Strategy:
        1. Use dummy node to handle edge cases
        2. For each group:
           - Check if k nodes available
           - Reverse k nodes by changing pointers
           - Reconnect group to rest of list
        3. Move to next group
        
        This is OPTIMAL - O(1) space, meets all constraints!
        
        Visual Example: [1,2,3,4,5], k=2
        
        Initial:
          dummy → 1 → 2 → 3 → 4 → 5
        
        Group 1:
          Find kth (2)
          Reverse 1→2 to 2→1
          Connect: dummy → 2 → 1 → 3 → 4 → 5
        
        Group 2:
          Find kth (4)
          Reverse 3→4 to 4→3
          Connect: dummy → 2 → 1 → 4 → 3 → 5
        
        Group 3:
          Only 5 left (< k), don't reverse
        
        Result: [2,1,4,3,5] ✓
        """
        if not head or k < 2:
            return head

        dummy = ListNode(0)
        dummy.next = head
        groupPrev = dummy

        while True:
            # Step 1: Find kth node from groupPrev
            kth = groupPrev
            count = 0
            while count < k and kth:
                kth = kth.next
                count += 1

            # If not enough nodes, we're done
            if not kth:
                break

            # Step 2: Define group boundaries
            groupStart = groupPrev.next  # First node of group
            groupNext = kth.next         # Node after group

            # Step 3: Reverse k nodes
            prev = groupNext  # Start with node after group
            curr = groupStart

            for _ in range(k):
                temp = curr.next
                curr.next = prev
                prev = curr
                curr = temp

            # Step 4: Reconnect group to list
            # prev now points to new head of reversed group (was kth)
            groupPrev.next = prev
            # groupStart is now tail of reversed group
            groupPrev = groupStart

        return dummy.next


# ==============================================================================
# COMPARISON
# ==============================================================================

"""
SOLUTION 1 (Array):
✓ Easy to understand
✓ Works correctly
❌ O(n) space (violates follow-up)
❌ Modifies values (violates constraint "only nodes may be changed")

SOLUTION 2 (Iterative): ⭐
✓ O(1) space (meets follow-up!)
✓ Only changes pointers, not values
✓ Optimal solution
✓ Clean, readable code

RECOMMENDATION:
Use Solution 2 for interviews - it's perfect!
"""

# ==============================================================================
# KEY INSIGHTS FROM YOUR SOLUTION 2
# ==============================================================================

"""
Your iterative solution demonstrates excellent understanding:

1. Dummy Node:
   - Handles edge case where head changes
   - Provides consistent starting point

2. Group Detection:
   - Count k nodes from groupPrev
   - If < k nodes remain, stop (don't reverse)

3. Reversal Pattern:
   - Start prev at groupNext (connects reversed group to rest)
   - Reverse k nodes using standard technique
   - After reversal: prev = new group head, groupStart = new group tail

4. Reconnection:
   - groupPrev.next = prev (connect to new group head)
   - groupPrev = groupStart (move to tail for next iteration)

This is textbook optimal implementation!
"""

# ==============================================================================
# TESTING
# ==============================================================================

if __name__ == "__main__":
    def create_list(vals):
        if not vals:
            return None
        head = ListNode(vals[0])
        curr = head
        for v in vals[1:]:
            curr.next = ListNode(v)
            curr = curr.next
        return head
    
    def print_list(head):
        vals = []
        while head:
            vals.append(head.val)
            head = head.next
        return vals
    
    print("Testing Your Solutions:")
    print("=" * 70)
    
    test_cases = [
        ([1,2,3,4,5], 2, [2,1,4,3,5]),
        ([1,2,3,4,5], 3, [3,2,1,4,5]),
        ([1,2,3,4,5,6,7], 3, [3,2,1,6,5,4,7]),
    ]
    
    for vals, k, expected in test_cases:
        head = create_list(vals)
        sol = Solution()
        result = sol.reverseKGroup(head, k)
        output = print_list(result)
        
        print(f"Input: {vals}, k={k}")
        print(f"Output: {output}")
        print(f"Expected: {expected}")
        print(f"{'✓ PASS' if output == expected else '✗ FAIL'}\n")