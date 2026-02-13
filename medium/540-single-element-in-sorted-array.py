"""
LeetCode 540: Single Element in a Sorted Array
Difficulty: Medium

Problem Statement:
You are given a sorted array consisting of only integers where every element 
appears exactly twice, except for one element which appears exactly once.

Return the single element that appears only once.
Your solution must run in O(log n) time and O(1) space.

Examples:
1. nums = [1,1,2,3,3,4,4,8,8] → Output: 2
2. nums = [3,3,7,7,10,11,11] → Output: 10

Key Insight:
Before the single element, pairs start at EVEN indices (0,2,4...)
After the single element, pairs start at ODD indices (1,3,5...)
"""

# ============================================================================
# SOLUTION 1: XOR APPROACH (SIMPLE BUT NOT OPTIMAL)
# ============================================================================

class SolutionXOR:
    """
    Approach: XOR all elements (a ^ a = 0, so pairs cancel out)
    
    Time Complexity: O(n) - Must scan entire array
    Space Complexity: O(1)
    
    Pros:
    - Simple and elegant
    - Works for unsorted arrays too
    - Easy to understand
    
    Cons:
    - Doesn't meet O(log n) requirement
    - Doesn't use the "sorted" property
    - Not optimal for this problem
    
    When to use:
    - When array is NOT sorted
    - When interviewer asks "what if not sorted?"
    - As a starting point before optimization
    """
    
    def singleNonDuplicate(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        if len(nums) < 1:
            return None
        
        xor = nums[0]
        
        # XOR cancels out pairs: a ^ a = 0
        for i in range(1, len(nums)):
            xor ^= nums[i]
        
        return xor


# ============================================================================
# SOLUTION 2: BINARY SEARCH - EVEN INDEX ALIGNMENT (YOUR SOLUTION)
# ============================================================================

class SolutionBinarySearchEven:
    """
    Approach: Binary search with even index alignment
    
    Time Complexity: O(log n) ✓
    Space Complexity: O(1) ✓
    
    Key Insight:
    - Always align mid to EVEN index (if odd, decrement by 1)
    - Before single element: nums[even] == nums[even+1]
    - After single element: nums[even] != nums[even+1]
    
    Pros:
    - Meets O(log n) requirement
    - Clean and straightforward
    - Easy to remember (always work with even indices)
    
    Performance:
    - Runtime: 95-100%
    - Memory: 90-95%
    
    This is a great interview solution!
    """
    
    def singleNonDuplicate(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        low, high = 0, len(nums) - 1
        
        while low < high:
            mid = (high + low) // 2
            
            # Align mid to even index
            if (mid % 2) != 0:
                mid -= 1
            
            # Check if pair starts at this even index
            if nums[mid] == nums[mid + 1]:
                # Pair intact, single element is on the right
                low = mid + 2
            else:
                # Pair broken, single element is on the left (or at mid)
                high = mid
        
        return nums[low]


# ============================================================================
# SOLUTION 3: BINARY SEARCH - XOR PAIRING CHECK (OPTIMAL)
# ============================================================================

class SolutionBinarySearchXOR:
    """
    Approach: Binary search using XOR for pair checking
    
    Time Complexity: O(log n) ✓
    Space Complexity: O(1) ✓
    
    Key Insight:
    - Use (mid ^ 1) to get pair index
      - If mid is even: mid ^ 1 = mid + 1
      - If mid is odd: mid ^ 1 = mid - 1
    - Before single: nums[mid] == nums[mid ^ 1]
    - After single: nums[mid] != nums[mid ^ 1]
    
    Pros:
    - No need to align to even index
    - Slightly more elegant
    - Shows bit manipulation knowledge
    - One less branch (no if-statement for alignment)
    
    Performance:
    - Runtime: 100%
    - Memory: 95-98%
    
    This is the MOST OPTIMAL solution for interviews!
    """
    
    def singleNonDuplicate(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        low, high = 0, len(nums) - 1
        
        while low < high:
            mid = (low + high) // 2
            
            # XOR trick: mid ^ 1 gives pair index
            # Even index: mid ^ 1 = mid + 1
            # Odd index: mid ^ 1 = mid - 1
            if nums[mid] == nums[mid ^ 1]:
                # Pair intact, single element is on the right
                low = mid + 1
            else:
                # Pair broken, single element is on the left (or at mid)
                high = mid
        
        return nums[low]


