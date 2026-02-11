"""
LeetCode 35: Search Insert Position
Difficulty: Easy

Problem Statement:
Given a sorted array of distinct integers and a target value, return the index 
if the target is found. If not, return the index where it would be if it were 
inserted in order.

Constraints:
- Must achieve O(log n) runtime complexity
- Array contains distinct integers
- Array is sorted in ascending order

Examples:
1. nums = [1,3,5,6], target = 5 → Output: 2
2. nums = [1,3,5,6], target = 2 → Output: 1
3. nums = [1,3,5,6], target = 7 → Output: 4
"""

# ============================================================================
# SOLUTION 1: LOWER BOUND APPROACH (Original Solution)
# ============================================================================

class Solution:
    """
    Approach: Binary Search using Lower Bound concept
    
    Runtime: O(log n) - 100% faster
    Space: O(1) - 30% better (uses 3 extra variables)
    
    This is essentially the lower bound algorithm - finding the first position
    where we can insert the target to maintain sorted order.
    """
    
    def searchInsert(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        if len(nums) < 1:
            return None
            
        low, high = 0, len(nums) - 1
        ans = len(nums)  # Default: insert at end if target > all elements
        
        while low <= high:
            mid = (high + low) // 2
            
            if nums[mid] >= target:
                ans = mid          # Potential answer
                high = mid - 1     # Search left for smaller index
            else:
                low = mid + 1      # Search right for larger values
                
        return ans


# ============================================================================
# SOLUTION 2: SPACE-OPTIMIZED VERSION
# ============================================================================

class SolutionOptimized:
    """
    Approach: Binary Search without extra 'ans' variable
    
    Runtime: O(log n) - Same performance
    Space: O(1) - Better space usage (uses 2 variables instead of 3)
    
    Key Insight: After the loop ends, 'low' pointer naturally points to 
    the insertion position. This eliminates the need for a separate 'ans' variable.
    
    Why 'low' is the answer:
    - If target is found: low points to its index
    - If target is not found: low points to where it should be inserted
    - The loop invariant maintains: nums[low-1] < target <= nums[high+1]
    """
    
    def searchInsert(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        if not nums:
            return 0
            
        low, high = 0, len(nums) - 1
        
        while low <= high:
            mid = (low + high) // 2
            
            if nums[mid] == target:
                return mid         # Found exact match
            elif nums[mid] < target:
                low = mid + 1      # Search right half
            else:
                high = mid - 1     # Search left half
        
        # After loop: low is the insertion position
        return low


# ============================================================================
# SOLUTION 3: PYTHONIC ONE-LINER (Using bisect module)
# ============================================================================

import bisect

class SolutionPythonic:
    """
    Approach: Using Python's built-in bisect module
    
    Runtime: O(log n) - Highly optimized C implementation
    Space: O(1) - Most space efficient
    
    Note: This is the most efficient in practice but uses a library function.
    Good to know for production code, but in interviews you should implement
    the binary search yourself.
    """
    
    def searchInsert(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        return bisect.bisect_left(nums, target)

