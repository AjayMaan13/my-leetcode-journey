"""
2. Add Two Numbers
https://leetcode.com/problems/add-two-numbers/

Difficulty: Medium
Topics: Linked List, Math, Recursion
Date Solved: 2024-06-14

Problem:
You are given two non-empty linked lists representing two non-negative integers. 
The digits are stored in reverse order, and each of their nodes contains a single digit. 
Add the two numbers and return the sum as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.

Example 1:
Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [7,0,8]
Explanation: 342 + 465 = 807

Example 2:
Input: l1 = [0], l2 = [0]
Output: [0]

Example 3:
Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
Output: [8,9,9,9,0,0,0,1]

Constraints:
- The number of nodes in each linked list is in the range [1, 100]
- 0 <= Node.val <= 9
- It is guaranteed that the list represents a number that does not have leading zeros
"""

# Definition for singly-linked list
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# My Original Solution
class Solution:
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: Optional[ListNode]
        :type l2: Optional[ListNode]
        :rtype: Optional[ListNode]
        """
        carry = 0
        l1End = 0
        l2End = 0
        newLL = ListNode()
        head = newLL

        while (carry) or (not l1End) or (not l2End):
            if (not l1End) and (not l2End):
                newLL.val = l1.val + l2.val + carry
            elif (l1End) and (not l2End):
                newLL.val = l2.val + carry
            elif (l2End) and (not l1End):
                newLL.val = l1.val + carry
            else:
                newLL.val = carry
                carry = 0

            if newLL.val >= 10:
                carry = 1
                newLL.val = newLL.val - 10
            else:
                carry = 0

            if not l1.next:
                l1End = True
            else:
                l1 = l1.next

            if not l2.next:
                l2End = True
            else:
                l2 = l2.next

            if ((carry) or (not l1End) or (not l2End)):
                newLL.next = ListNode()
                newLL = newLL.next

        return head


# Optimized Solution
class MySolution:
    def addTwoNumbers(self, l1, l2):
        """
        My Approach: Clean simulation with proper carry handling
        - Create dummy head for easier list construction
        - Handle carry properly with while loop conditions
        - Clean pointer advancement
        
        Time: O(max(m, n)) where m, n are lengths of lists
        Space: O(max(m, n)) for the result list
        """
        newLL = ListNode()  # Dummy head
        current = newLL
        carry = 0
        
        while l1 or l2 or carry:
            val1 = l1.val if l1 else 0
            val2 = l2.val if l2 else 0
            
            total = val1 + val2 + carry
            carry = total // 10
            current.val = total % 10
            
            # Advance pointers
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None
            
            # Create next node if needed
            if l1 or l2 or carry:
                current.next = ListNode()
                current = current.next
                
        return newLL

# Memory Optimized Solution
class OptimizedSolution:
    def addTwoNumbers(self, l1, l2):
        """
        Memory Optimized: Minimal variables, efficient operations
        - Use shortest variable names
        - Combine operations where possible
        - Minimize temporary variables
        
        Time: O(max(m, n))
        Space: O(max(m, n)) - but with better memory efficiency
        """
        dummy = ListNode(0)
        curr = dummy
        carry = 0
        
        while l1 or l2 or carry:
            s = carry
            if l1:
                s += l1.val
                l1 = l1.next
            if l2:
                s += l2.val
                l2 = l2.next
                
            curr.next = ListNode(s % 10)
            curr = curr.next
            carry = s // 10
            
        return dummy.next

'''
One Concept That could be of Help:
DIVMOD:

carry, digit = divmod(carry + (l1.val if l1 else 0) + (l2.val if l2 else 0), 10)
It could make the solution concise my doing multiple operations in one line
'''


# Helper functions for testing
def build_linked_list(nums):
    """Build linked list from array of numbers"""
    if not nums:
        return None
    head = ListNode(nums[0])
    current = head
    for n in nums[1:]:
        current.next = ListNode(n)
        current = current.next
    return head

def print_linked_list(head):
    """Print linked list in readable format"""
    result = []
    while head:
        result.append(str(head.val))
        head = head.next
    print(' -> '.join(result))

def linked_list_to_array(head):
    """Convert linked list to array for easy testing"""
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result

# Test cases
if __name__ == "__main__":
    # Initialize solutions
    my_sol = MySolution()
    opt_sol = OptimizedSolution()
    concise_sol = ConciseSolution()
    
    print("=== Add Two Numbers - Solution Comparison ===\n")
    
    # Test case 1: Basic addition
    print("Test 1: [2,4,3] + [5,6,4] = 342 + 465 = 807")
    l1 = build_linked_list([2, 4, 3])
    l2 = build_linked_list([5, 6, 4])
    
    result1 = my_sol.addTwoNumbers(l1, l2)
    l1 = build_linked_list([2, 4, 3])  # Rebuild for next test
    l2 = build_linked_list([5, 6, 4])
    result2 = opt_sol.addTwoNumbers(l1, l2)
    l1 = build_linked_list([2, 4, 3])  # Rebuild for next test
    l2 = build_linked_list([5, 6, 4])
    result3 = concise_sol.addTwoNumbers(l1, l2)
    
    print(f"My Solution:       {linked_list_to_array(result1)}")
    print(f"Optimized:         {linked_list_to_array(result2)}")
    print(f"Concise:           {linked_list_to_array(result3)}")
    print(f"Expected:          [7, 0, 8]")
    print()
    
    # Test case 2: Different lengths with carry
    print("Test 2: [9,9,9,9,9,9,9] + [9,9,9,9] - Multiple carries")
    l1 = build_linked_list([9, 9, 9, 9, 9, 9, 9])
    l2 = build_linked_list([9, 9, 9, 9])
    
    result1 = my_sol.addTwoNumbers(l1, l2)
    l1 = build_linked_list([9, 9, 9, 9, 9, 9, 9])
    l2 = build_linked_list([9, 9, 9, 9])
    result2 = opt_sol.addTwoNumbers(l1, l2)
    
    print(f"My Solution:       {linked_list_to_array(result1)}")
    print(f"Optimized:         {linked_list_to_array(result2)}")
    print(f"Expected:          [8, 9, 9, 9, 0, 0, 0, 1]")
    print()
    
    # Test case 3: Your example
    print("Test 3: [2,5,5] + [7,5,2] = 552 + 257 = 809")
    l1 = build_linked_list([2, 5, 5])
    l2 = build_linked_list([7, 5, 2])
    
    result1 = my_sol.addTwoNumbers(l1, l2)
    l1 = build_linked_list([2, 5, 5])
    l2 = build_linked_list([7, 5, 2])
    result2 = opt_sol.addTwoNumbers(l1, l2)
    
    print(f"My Solution:       {linked_list_to_array(result1)}")
    print(f"Optimized:         {linked_list_to_array(result2)}")
    print(f"Expected:          [9, 0, 8]")
    print()
    
    # Test case 4: Edge case - single digits
    print("Test 4: [0] + [0] = Simple case")
    l1 = build_linked_list([0])
    l2 = build_linked_list([0])
    
    result = opt_sol.addTwoNumbers(l1, l2)
    print(f"Result:            {linked_list_to_array(result)}")
    print(f"Expected:          [0]")

"""
Key Insights:
- Dummy head pattern simplifies edge cases
- Carry handling is the critical part
- Different list lengths handled naturally
- Memory optimization comes from minimal variables

What I Learned:
- Linked list arithmetic simulation
- Dummy head technique for easier construction
- Carry propagation in addition
- Multiple ways to handle null pointer checks
"""




"""class Solution:
    def addTwoNumbers(self, l1, l2):
        
        #:type l1: Optional[ListNode]
        #:type l2: Optional[ListNode]
        #:rtype: Optional[ListNode]
        
        carry = 0
        l1End = 0
        l2End = 0
        newLL = ListNode()
        head = newLL

        while (carry) or (not l1End) or (not l2End):
            if (not l1End) and (not l2End):
                newLL.val = l1.val + l2.val + carry
            elif (l1End) and (not l2End):
                newLL.val = l2.val + carry
            elif (l2End) and (not l1End):
                newLL.val = l1.val + carry
            else:
                newLL.val = carry
                carry = 0

            if newLL.val >= 10:
                carry = 1
                newLL.val = newLL.val - 10
            else:
                carry = 0

            if not l1.next:
                l1End = True
            else:
                l1 = l1.next

            if not l2.next:
                l2End = True
            else:
                l2 = l2.next

            if ((carry) or (not l1End) or (not l2End)):
                newLL.next = ListNode()
                newLL = newLL.next

        return head
"""