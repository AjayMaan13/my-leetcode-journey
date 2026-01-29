"""
LeetCode 136: Single Number

Problem:
Given a non-empty array of integers nums, every element appears twice except 
for one. Find that single one.

You must implement a solution with a linear runtime complexity and use only 
constant extra space.

Examples:
1. nums = [2,2,1] → 1
2. nums = [4,1,2,1,2] → 4
3. nums = [1] → 1

Constraints:
- 1 <= nums.length <= 3 * 10^4
- -3 * 10^4 <= nums[i] <= 3 * 10^4
- Each element appears twice except for one element which appears only once
- Must be O(N) time and O(1) space
"""

# ===== My Solution =====
class Solution:
    def singleNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        missing = 0
        for i in range(len(nums)):
            missing ^= nums[i]
        return missing

# Time: O(N), Space: O(1)
# Uses XOR - duplicates cancel out (a ^ a = 0)


# ===== Optimized Solution 1: Cleaner XOR =====
class Solution:
    def singleNumber(self, nums):
        result = 0
        for num in nums:
            result ^= num
        return result

# Time: O(N), Space: O(1)
# Cleaner: iterate over values directly instead of indices


# ===== Optimized Solution 2: XOR One-Liner =====
class Solution:
    def singleNumber(self, nums):
        from functools import reduce
        import operator
        return reduce(operator.xor, nums)

# Time: O(N), Space: O(1)
# Most concise using reduce


# ===== Alternative Solution: Sorting (Not optimal) =====
class Solution:
    def singleNumber(self, nums):
        nums.sort()
        
        for i in range(0, len(nums) - 1, 2):
            if nums[i] != nums[i + 1]:
                return nums[i]
        
        return nums[-1]

# Time: O(N log N), Space: O(1)
# Slower but uses O(1) space
# Note: Modifies input array


"""
How XOR Solution Works:
========================

Example: [4, 1, 2, 1, 2]

Step-by-step:
missing = 0
missing = 0 ^ 4 = 4
missing = 4 ^ 1 = 5
missing = 5 ^ 2 = 7
missing = 7 ^ 1 = 6  (1 appears again, starts to cancel)
missing = 6 ^ 2 = 4  (2 appears again, starts to cancel)

Why it works:
4 ^ 1 ^ 2 ^ 1 ^ 2
= 4 ^ (1 ^ 1) ^ (2 ^ 2)  (rearrange)
= 4 ^ 0 ^ 0              (duplicates cancel: a ^ a = 0)
= 4                       (unique number remains)

Key XOR Properties:
- a ^ a = 0 (duplicate cancels)
- a ^ 0 = a (0 is neutral)
- XOR is commutative (order doesn't matter)
"""