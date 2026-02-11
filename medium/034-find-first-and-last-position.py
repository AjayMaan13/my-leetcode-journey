"""
LeetCode 34: Find First and Last Position of Element in Sorted Array
Difficulty: Medium

Problem Statement:
Given an array of integers nums sorted in non-decreasing order, find the 
starting and ending position of a given target value.

If target is not found in the array, return [-1, -1].
You must write an algorithm with O(log n) runtime complexity.

Examples:
1. nums = [5,7,7,8,8,10], target = 8 → Output: [3,4]
2. nums = [5,7,7,8,8,10], target = 6 → Output: [-1,-1]
3. nums = [], target = 0 → Output: [-1,-1]
"""

# ============================================================================
# SOLUTION 1: YOUR SOLUTION - BINARY SEARCH + LINEAR EXPANSION
# ============================================================================

class SolutionHybrid:
    """
    Approach: Binary search to find target, then linear expand to find boundaries
    
    Runtime: O(log n) average, O(n) worst case
    Space: O(1)
    
    LeetCode Performance:
    - Runtime: 100% (Best!)
    - Memory: 96% (Excellent!)
    
    Pros: 
    - Extremely fast for arrays with few duplicates
    - Simple to understand and implement
    - Best average-case performance
    
    Cons:
    - Worst case O(n) if all elements are target (e.g., [8,8,8,8,8,8])
    - Linear expansion after finding target
    
    When to use:
    - When duplicates are rare (interview follow-up: "What if few duplicates?")
    - When average case matters more than worst case
    - For real-world data where massive duplicate runs are unlikely
    """
    
    def searchRange(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        if len(nums) < 1:
            return [-1, -1]
            
        low, high = 0, len(nums) - 1 
        
        while low <= high:
            mid = (high + low) // 2
            
            if nums[mid] == target:
                # Found target! Now expand linearly to find boundaries
                low = high = mid
                
                # Expand left to find first occurrence
                while low > 0 and nums[low - 1] == target:
                    low -= 1
                
                # Expand right to find last occurrence
                while high < len(nums) - 1 and nums[high + 1] == target:
                    high += 1
                
                return [low, high]
                
            elif nums[mid] > target:
                high = mid - 1 
            else:
                low = mid + 1
            
        return [-1, -1]


# ============================================================================
# SOLUTION 2: OPTIMAL FOR INTERVIEWS - TWO BINARY SEARCHES
# ============================================================================

class SolutionOptimal:
    """
    Approach: Two separate binary searches (first position + last position)
    
    Runtime: O(log n) guaranteed - both best and worst case
    Space: O(1)
    
    LeetCode Performance:
    - Runtime: 95-100%
    - Memory: 95-98%
    
    Pros:
    - Guaranteed O(log n) even with all duplicates
    - Clean, modular code (reusable helper functions)
    - Interview favorite - shows mastery of binary search variants
    - Handles worst case elegantly
    
    Cons:
    - Slightly more code than Solution 1
    - Two passes through array (still O(log n) though)
    
    This is THE solution to present in interviews!
    """
    
    def searchRange(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        if not nums:
            return [-1, -1]
        
        # Find first and last positions using two binary searches
        first = self.find_first(nums, target)
        
        # If target not found, no need to search for last
        if first == -1:
            return [-1, -1]
        
        last = self.find_last(nums, target)
        
        return [first, last]
    
    def find_first(self, nums, target):
        """
        Find the FIRST (leftmost) occurrence of target
        
        Key idea: When we find target, keep searching LEFT for earlier occurrences
        """
        low, high = 0, len(nums) - 1
        result = -1
        
        while low <= high:
            mid = (low + high) // 2
            
            if nums[mid] == target:
                result = mid      # Found a candidate
                high = mid - 1    # Keep searching LEFT for earlier occurrence
            elif nums[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        
        return result
    
    def find_last(self, nums, target):
        """
        Find the LAST (rightmost) occurrence of target
        
        Key idea: When we find target, keep searching RIGHT for later occurrences
        """
        low, high = 0, len(nums) - 1
        result = -1
        
        while low <= high:
            mid = (low + high) // 2
            
            if nums[mid] == target:
                result = mid      # Found a candidate
                low = mid + 1     # Keep searching RIGHT for later occurrence
            elif nums[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        
        return result
