"""
LeetCode 283: Move Zeroes

Problem:
Given an integer array nums, move all 0's to the end while maintaining 
the relative order of non-zero elements. Do this in-place.

Examples:
- [0,1,0,3,12] → [1,3,12,0,0]
- [0] → [0]

Constraints:
- 1 <= nums.length <= 10^4
- Must be in-place (O(1) extra space)
"""

# ===== My Solution =====
class Solution:
    def moveZeroes(self, nums):
        if len(nums) < 2:
            return nums
        
        left = 1
        right = 1
        
        while right < len(nums):
            if nums[left - 1] != 0:
                left += 1
            elif nums[left - 1] == 0 and nums[right] != 0:
                nums[left - 1], nums[right] = nums[right], nums[left - 1]
                left += 1
            right += 1
        
        return nums

# Time: O(N), Space: O(1)
# Issue: Uses left-1 indexing, slightly complex logic


# ===== Optimized Solution 1: Two Pointers (Snowball) =====
class Solution:
    def moveZeroes(self, nums):
        left = 0  # Position to place next non-zero
        
        for right in range(len(nums)):
            if nums[right] != 0:
                nums[left], nums[right] = nums[right], nums[left]
                left += 1

# Time: O(N), Space: O(1)
# Cleaner: left tracks position for next non-zero


# ===== Optimized Solution 2: Shift and Fill =====
class Solution:
    def moveZeroes(self, nums):
        left = 0
        
        # Move all non-zeros to front
        for right in range(len(nums)):
            if nums[right] != 0:
                nums[left] = nums[right]
                left += 1
        
        # Fill remaining with zeros
        for i in range(left, len(nums)):
            nums[i] = 0

# Time: O(N), Space: O(1)
# Two passes: first collect non-zeros, then fill zeros
