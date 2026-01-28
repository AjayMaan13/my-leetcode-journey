"""
LeetCode 485: Max Consecutive Ones

Problem:
Given a binary array nums, return the maximum number of consecutive 1's in the array.

Examples:
- [1,1,0,1,1,1] → 3 (last three 1's)
- [1,0,1,1,0,1] → 2

Constraints:
- 1 <= nums.length <= 10^5
- nums[i] is either 0 or 1
"""

# ===== My Solution =====
class Solution:
    def findMaxConsecutiveOnes(self, nums):
        if len(nums) < 1:
            return None
        
        countOnes = maxOneCount = 0
        
        for i in range(len(nums)):
            if nums[i] == 1:
                countOnes += 1
                if countOnes > maxOneCount:
                    maxOneCount = countOnes
            else:
                countOnes = 0
        
        return maxOneCount

# Time: O(N), Space: O(1)
# Works correctly!


# ===== Optimized Solution 1: Cleaner Logic =====
class Solution:
    def findMaxConsecutiveOnes(self, nums):
        max_count = current_count = 0
        
        for num in nums:
            if num == 1:
                current_count += 1
                max_count = max(max_count, current_count)
            else:
                current_count = 0
        
        return max_count

# Time: O(N), Space: O(1)
# Cleaner: uses max() function, iterates over values


# ===== Optimized Solution 2: One-Liner =====
class Solution:
    def findMaxConsecutiveOnes(self, nums):
        return max(len(group) for group in ''.join(map(str, nums)).split('0'))

# Time: O(N), Space: O(N)
# Convert to string, split by '0', find longest group


# ===== Optimized Solution 3: Using groupby =====
from itertools import groupby

class Solution:
    def findMaxConsecutiveOnes(self, nums):
        return max((sum(1 for _ in group) for key, group in groupby(nums) if key == 1), default=0)

# Time: O(N), Space: O(1)
# Groups consecutive elements, counts 1's