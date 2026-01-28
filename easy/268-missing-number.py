"""
LeetCode 268: Missing Number

Problem:
Given an array nums containing n distinct numbers in the range [0, n], 
return the only number in the range that is missing from the array.

Examples:
- [3,0,1] → 2 (range [0,3], missing 2)
- [0,1] → 2 (range [0,2], missing 2)
- [9,6,4,2,3,5,7,0,1] → 8
"""

# ===== My Solution =====
class Solution:
    def missingNumber(self, nums):
        if len(nums) < 1:
            return None
        
        numDict = {i: 0 for i in range(len(nums) + 1)}
        
        for i in range(len(nums)):
            if nums[i] in numDict:
                numDict[nums[i]] += 1
        
        for key, value in numDict.items():
            if value == 0:
                return key

# Time: O(N), Space: O(N)


# ===== Optimized Solution 1: Math (Sum) =====
class Solution:
    def missingNumber(self, nums):
        n = len(nums)
        expected_sum = n * (n + 1) // 2
        actual_sum = sum(nums)
        return expected_sum - actual_sum

# Time: O(N), Space: O(1)
# Formula: sum(0 to n) = n*(n+1)/2


# ===== Optimized Solution 2: XOR =====
class Solution:
    def missingNumber(self, nums):
        missing = len(nums)
        
        for i in range(len(nums)):
            missing ^= i ^ nums[i]
        
        return missing

# Time: O(N), Space: O(1)
# XOR property: a ^ a = 0, a ^ 0 = a


# ===== Optimized Solution 3: Set (Cleaner) =====
class Solution:
    def missingNumber(self, nums):
        n = len(nums)
        full_set = set(range(n + 1))
        return (full_set - set(nums)).pop()

# Time: O(N), Space: O(N)
# Set difference finds missing number