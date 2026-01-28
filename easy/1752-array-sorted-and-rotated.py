"""
LeetCode 1752: Check if Array Is Sorted and Rotated

Problem:
Given an array nums, return true if the array was originally sorted in 
non-decreasing order, then rotated some number of positions. Otherwise, return false.

Examples:
- [3,4,5,1,2] → true (original: [1,2,3,4,5], rotated by 2)
- [2,1,3,4] → false
- [1,2,3] → true (rotated by 0)
"""

# ===== My Solution =====
class Solution:
    def check(self, nums):
        length = len(nums)
        if length <= 2:
            return True
        
        largest = nums[length - 1]
        rotatedNum = 0
        left = 0
        right = 1
        
        while right < length:
            if nums[right] < nums[left]:
                if rotatedNum == 0:
                    rotatedNum += 1
                    largest = nums[left]
                else:
                    return False
            left = right
            right += 1
        
        if rotatedNum == 0:
            return True
        else:
            return nums[length - 1] <= largest and nums[0] >= nums[length - 1]

# Time: O(N), Space: O(1)


# ===== Optimized Solution =====
class Solution:
    def check(self, nums):
        count = 0
        n = len(nums)
        
        for i in range(n):
            if nums[i] > nums[(i + 1) % n]:
                count += 1
            if count > 1:
                return False
        
        return True

# Time: O(N), Space: O(1)
# Key: Count break points where nums[i] > nums[i+1]
# Sorted rotated array has at most 1 break point