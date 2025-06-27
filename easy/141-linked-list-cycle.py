"""
141. Linked List Cycle
https://leetcode.com/problems/linked-list-cycle/

Difficulty: Easy
Topics: Hash Table, Linked List, Two Pointers
Date Solved: 2024-06-14

Problem:
Given head, the head of a linked list, determine if the linked list has a cycle in it.

There is a cycle in a linked list if there is some node in the list that can be 
reached again by continuously following the next pointer. Internally, pos is used 
to denote the index of the node that tail's next pointer is connected to. 
Note that pos is not passed as a parameter.

Return true if there is a cycle in the linked list. Otherwise, return false.

Example 1:
Input: head = [3,2,0,-4], pos = 1
Output: true
Explanation: There is a cycle in the linked list, where the tail connects to the 1st node (0-indexed).

Example 2:
Input: head = [1,2], pos = 0
Output: true
Explanation: There is a cycle in the linked list, where the tail connects to the 0th node.

Example 3:
Input: head = [1], pos = -1
Output: false
Explanation: There is no cycle in the linked list.

Constraints:
- The number of the nodes in the list is in the range [0, 10^4]
- -10^5 <= Node.val <= 10^5
- pos is -1 or a valid index in the linked-list

Follow up: Can you solve it using O(1) (i.e. constant) memory?
"""

# Definition for singly-linked list
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None

# My Original Solution - Working but can be optimized
class MySolution(object):
    def hasCycle(self, head):
        """
        My Approach: Floyd's Cycle Detection (Tortoise and Hare)
        - Fast pointer moves 2 steps, slow pointer moves 1 step
        - If cycle exists, fast will eventually meet slow
        
        Time: O(n) where n is number of nodes
        Space: O(1) constant space
        """
        if not head:
            return False
        
        fast = head.next
        
        while fast:
            if head == fast:
                return True
            
            head = head.next
            
            if not fast.next or not fast.next.next:
                return False
            
            fast = fast.next.next
        
        return False

# Optimized Solution - Better memory and cleaner logic
class OptimizedSolution(object):
    def hasCycle(self, head):
        """
        Optimized Floyd's Algorithm: Cleaner implementation
        - Both pointers start from head
        - Check conditions more efficiently
        - Fewer variable assignments
        
        Time: O(n)
        Space: O(1) - better memory efficiency
        """
        if not head or not head.next:
            return False
        
        slow = fast = head
        
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            
            if slow == fast:
                return True
        
        return False

# Helper functions for testing
def create_cycle_list(vals, pos):
    """Create a linked list with cycle at given position"""
    if not vals:
        return None
    
    head = ListNode(vals[0])
    current = head
    nodes = [head]
    
    # Build the list
    for val in vals[1:]:
        current.next = ListNode(val)
        current = current.next
        nodes.append(current)
    
    # Create cycle if pos is valid
    if 0 <= pos < len(nodes):
        current.next = nodes[pos]
    
    return head

def print_list_info(head, max_nodes=10):
    """Print first few nodes of list (to avoid infinite loop in cycle)"""
    current = head
    count = 0
    values = []
    
    while current and count < max_nodes:
        values.append(current.val)
        current = current.next
        count += 1
    
    if current and count == max_nodes:
        values.append("...")
    
    return values

# Test cases
if __name__ == "__main__":
    # Initialize solutions
    my_sol = MySolution()
    opt_sol = OptimizedSolution()
    
    print("=== Linked List Cycle Detection - Solution Comparison ===\n")
    
    # Test case 1: Cycle exists (Example 1)
    print("Test 1: [3,2,0,-4] with cycle at pos=1")
    head1 = create_cycle_list([3, 2, 0, -4], 1)
    
    result1_my = my_sol.hasCycle(head1)
    result1_opt = opt_sol.hasCycle(head1)
    
    print(f"List values: {print_list_info(head1)}")
    print(f"My Solution:       {result1_my}")
    print(f"Optimized:         {result1_opt}")
    print(f"Expected:          True")
    print()
    
    # Test case 2: Cycle exists (Example 2)
    print("Test 2: [1,2] with cycle at pos=0")
    head2 = create_cycle_list([1, 2], 0)
    
    result2_my = my_sol.hasCycle(head2)
    result2_opt = opt_sol.hasCycle(head2)
    
    print(f"List values: {print_list_info(head2)}")
    print(f"My Solution:       {result2_my}")
    print(f"Optimized:         {result2_opt}")
    print(f"Expected:          True")
    print()
    
    # Test case 3: No cycle (Example 3)
    print("Test 3: [1] with no cycle (pos=-1)")
    head3 = create_cycle_list([1], -1)
    
    result3_my = my_sol.hasCycle(head3)
    result3_opt = opt_sol.hasCycle(head3)
    
    print(f"List values: {print_list_info(head3)}")
    print(f"My Solution:       {result3_my}")
    print(f"Optimized:         {result3_opt}")
    print(f"Expected:          False")
    print()
    
    # Test case 4: Empty list
    print("Test 4: Empty list")
    head4 = None
    
    result4_my = my_sol.hasCycle(head4)
    result4_opt = opt_sol.hasCycle(head4)
    
    print(f"My Solution:       {result4_my}")
    print(f"Optimized:         {result4_opt}")
    print(f"Expected:          False")
    print()
    
    # Test case 5: Single node, no cycle
    print("Test 5: Single node, no cycle")
    head5 = ListNode(1)
    
    result5_my = my_sol.hasCycle(head5)
    result5_opt = opt_sol.hasCycle(head5)
    
    print(f"My Solution:       {result5_my}")
    print(f"Optimized:         {result5_opt}")
    print(f"Expected:          False")

"""
Performance Analysis:

My Original Solution:
✅ Correct Floyd's algorithm implementation
✅ Handles edge cases
❌ More complex logic with extra conditionals
❌ Starts fast pointer at head.next (less standard)
❌ More memory usage due to extra checks

Optimized Solution:
✅ Standard Floyd's algorithm implementation
✅ Both pointers start from head (cleaner)
✅ Simpler loop condition
✅ Better memory efficiency
✅ More readable and maintainable

Key Insights:
- Floyd's algorithm (two pointers) is the optimal solution
- Both pointers starting from head is cleaner than offset start
- Simpler loop conditions improve performance
- Standard implementation patterns are more maintainable

What I Learned:
- Floyd's Cycle Detection Algorithm (Tortoise and Hare)
- Two-pointer technique for linked list problems
- Importance of clean, standard implementations
- Trade-offs between different starting positions

Patterns Used:
- Two Pointers (Fast and Slow)
- Floyd's Cycle Detection

Recommendation: Use OptimizedSolution for best balance of performance and readability!
"""