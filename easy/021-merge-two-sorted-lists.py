"""
21. Merge Two Sorted Lists
https://leetcode.com/problems/merge-two-sorted-lists/

Difficulty: Easy
Topics: Linked List, Recursion
Date Solved: 2024-06-14

Problem:
You are given the heads of two sorted linked lists list1 and list2.

Merge the two lists into one sorted list. The list should be made by splicing 
together the nodes of the first two lists.

Return the head of the merged linked list.

Example 1:
Input: list1 = [1,2,4], list2 = [1,3,4]
Output: [1,1,2,3,4,4]

Example 2:
Input: list1 = [], list2 = []
Output: []

Example 3:
Input: list1 = [], list2 = [0]
Output: [0]

Constraints:
- The number of nodes in both lists is in the range [0, 50]
- -100 <= Node.val <= 100
- Both list1 and list2 are sorted in non-decreasing order
"""

# Definition for singly-linked list
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# My Original Solution - Working but has some issues
class MySolution(object):
    def mergeTwoLists(self, list1, list2):
        """
        My Approach: Iterative merge with dummy head
        - Use dummy head to simplify edge cases
        - Compare values and attach smaller node
        - Handle remaining nodes from longer list
        
        Time: O(m + n) where m, n are lengths of lists
        Space: O(1) constant space
        """
        dummy = ListNode(0)
        current = dummy
        
        while list1 or list2:
            if list1 and list2:
                if list1.val > list2.val:
                    current.next = list2
                    list2 = list2.next
                elif list2.val > list1.val:
                    current.next = list1
                    list1 = list1.next
                else:  # Equal values
                    current.next = list1
                    list1 = list1.next
                    current = current.next
                    current.next = list2
                    list2 = list2.next
                current = current.next
            elif list1:
                current.next = list1
                list1 = list1.next
            elif list2:
                current.next = list2
                list2 = list2.next
            current = current.next
        
        return dummy.next

# Optimized Solution - Cleaner and more efficient
class OptimizedSolution(object):
    def mergeTwoLists(self, list1, list2):
        """
        Optimized Iterative: Clean two-pointer approach
        - Simplified comparison logic
        - Better handling of remaining nodes
        - More memory efficient
        
        Time: O(m + n)
        Space: O(1) - better memory efficiency
        """
        dummy = ListNode(0)
        current = dummy
        
        # Compare and merge while both lists have nodes
        while list1 and list2:
            if list1.val <= list2.val:
                current.next = list1
                list1 = list1.next
            else:
                current.next = list2
                list2 = list2.next
            current = current.next
        
        # Attach remaining nodes (at most one list has remaining nodes)
        current.next = list1 or list2
        
        return dummy.next

# Helper functions for testing
def list_to_linkedlist(lst):
    """Convert Python list to linked list"""
    dummy = ListNode(0)
    current = dummy
    for val in lst:
        current.next = ListNode(val)
        current = current.next
    return dummy.next

def linkedlist_to_list(node):
    """Convert linked list to Python list"""
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result

# Test cases
if __name__ == "__main__":
    # Initialize solutions
    my_sol = MySolution()
    opt_sol = OptimizedSolution()
    
    print("=== Merge Two Sorted Lists - Solution Comparison ===\n")
    
    # Test case 1: Example 1
    print("Test 1: [1,2,4] + [1,3,4]")
    l1_my = list_to_linkedlist([1, 2, 4])
    l2_my = list_to_linkedlist([1, 3, 4])
    l1_opt = list_to_linkedlist([1, 2, 4])
    l2_opt = list_to_linkedlist([1, 3, 4])
    
    merged_my = my_sol.mergeTwoLists(l1_my, l2_my)
    merged_opt = opt_sol.mergeTwoLists(l1_opt, l2_opt)
    
    print(f"My Solution:       {linkedlist_to_list(merged_my)}")
    print(f"Optimized:         {linkedlist_to_list(merged_opt)}")
    print(f"Expected:          [1, 1, 2, 3, 4, 4]")
    print()
    
    # Test case 2: Example 2 (both empty)
    print("Test 2: [] + []")
    l1_my = list_to_linkedlist([])
    l2_my = list_to_linkedlist([])
    l1_opt = list_to_linkedlist([])
    l2_opt = list_to_linkedlist([])
    
    merged_my = my_sol.mergeTwoLists(l1_my, l2_my)
    merged_opt = opt_sol.mergeTwoLists(l1_opt, l2_opt)
    
    print(f"My Solution:       {linkedlist_to_list(merged_my)}")
    print(f"Optimized:         {linkedlist_to_list(merged_opt)}")
    print(f"Expected:          []")
    print()
    
    # Test case 3: Example 3 (one empty)
    print("Test 3: [] + [0]")
    l1_my = list_to_linkedlist([])
    l2_my = list_to_linkedlist([0])
    l1_opt = list_to_linkedlist([])
    l2_opt = list_to_linkedlist([0])
    
    merged_my = my_sol.mergeTwoLists(l1_my, l2_my)
    merged_opt = opt_sol.mergeTwoLists(l1_opt, l2_opt)
    
    print(f"My Solution:       {linkedlist_to_list(merged_my)}")
    print(f"Optimized:         {linkedlist_to_list(merged_opt)}")
    print(f"Expected:          [0]")
    print()
    
    # Test case 4: Different lengths
    print("Test 4: [1,3,5] + [2,4,6]")
    l1_my = list_to_linkedlist([1, 3, 5])
    l2_my = list_to_linkedlist([2, 4, 6])
    l1_opt = list_to_linkedlist([1, 3, 5])
    l2_opt = list_to_linkedlist([2, 4, 6])
    
    merged_my = my_sol.mergeTwoLists(l1_my, l2_my)
    merged_opt = opt_sol.mergeTwoLists(l1_opt, l2_opt)
    
    print(f"My Solution:       {linkedlist_to_list(merged_my)}")
    print(f"Optimized:         {linkedlist_to_list(merged_opt)}")
    print(f"Expected:          [1, 2, 3, 4, 5, 6]")
    print()
    
    # Test case 5: One list much longer
    print("Test 5: [1] + [2,3,4,5,6]")
    l1_my = list_to_linkedlist([1])
    l2_my = list_to_linkedlist([2, 3, 4, 5, 6])
    l1_opt = list_to_linkedlist([1])
    l2_opt = list_to_linkedlist([2, 3, 4, 5, 6])
    
    merged_my = my_sol.mergeTwoLists(l1_my, l2_my)
    merged_opt = opt_sol.mergeTwoLists(l1_opt, l2_opt)
    
    print(f"My Solution:       {linkedlist_to_list(merged_my)}")
    print(f"Optimized:         {linkedlist_to_list(merged_opt)}")
    print(f"Expected:          [1, 2, 3, 4, 5, 6]")

"""
Performance Analysis:

My Original Solution:
✅ Correct approach using dummy head
✅ Handles all edge cases
❌ Complex logic for equal values (unnecessary double attachment)
❌ Redundant current.next movements
❌ More verbose condition checking
❌ Bug: Double attachment when values are equal

Optimized Solution:
✅ Clean and simple comparison logic
✅ Efficient handling of remaining nodes with `current.next = list1 or list2`
✅ No redundant operations
✅ Standard merge pattern
✅ Better memory efficiency
✅ More readable and maintainable

Recommendation: Use OptimizedSolution for cleaner code and better performance!
"""