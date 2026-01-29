"""
1. Two Sum
https://leetcode.com/problems/two-sum/

Difficulty: Easy
Topics: Array, Hash Table
Date Solved: 2024-06-14

Problem:
Given an array of integers nums and an integer target, return indices of the 
two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may 
not use the same element twice.

You can return the answer in any order.

Example 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Example 2:
Input: nums = [3,2,4], target = 6
Output: [1,2]

Example 3:
Input: nums = [3,3], target = 6
Output: [0,1]

Constraints:
- 2 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9
- -10^9 <= target <= 10^9
- Only one valid answer exists.

Follow-up: Can you come up with an algorithm that is less than O(n²) time complexity?
"""

class Solution:
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        seen = set()
        
        for i, num in enumerate(nums):
            diff = target - num
            if diff in seen:
                return [nums.index(diff), i]
            seen.add(num)
        
        return []

# Hashmap
def twoSum(nums, target):
    hashMap = {}  # value -> index

    for i in range(len(nums)):
        diff = target - nums[i]

        if diff in hashMap:
            return [hashMap[diff], i]

        hashMap[nums[i]] = i

    return None


# Test cases
if __name__ == "__main__":
    solution = Solution()
    optimized = SolutionOptimized()
    
    # Test case 1
    nums1 = [2, 7, 11, 15]
    target1 = 9
    print(f"Test 1:")
    print(f"Input: nums = {nums1}, target = {target1}")
    print(f"Output: {solution.twoSum(nums1, target1)}")  # Expected: [0, 1]
    print(f"Optimized: {optimized.twoSum(nums1, target1)}")
    print()
    
    # Test case 2
    nums2 = [3, 2, 4]
    target2 = 6
    print(f"Test 2:")
    print(f"Input: nums = {nums2}, target = {target2}")
    print(f"Output: {solution.twoSum(nums2, target2)}")  # Expected: [1, 2]
    print(f"Optimized: {optimized.twoSum(nums2, target2)}")
    print()
    
    # Test case 3
    nums3 = [3, 3]
    target3 = 6
    print(f"Test 3:")
    print(f"Input: nums = {nums3}, target = {target3}")
    print(f"Output: {solution.twoSum(nums3, target3)}")  # Expected: [0, 1]
    print(f"Optimized: {optimized.twoSum(nums3, target3)}")

"""
Performance Analysis:
Runtime: 0 ms - Beats 100.00% 🏆
Memory: 13.28 MB - Beats 60.90%

Key Insights:
- Hash table/set allows O(1) average lookup time
- Single pass through array makes it O(n) overall
- Space-time tradeoff: use O(n) space to get O(n) time
- The complement approach is more intuitive than nested loops

What I Learned:
- Hash maps are incredibly powerful for array problems
- Always look for complement/difference patterns
- nums.index() can be inefficient - store indices in hash map instead
- Set vs Dict: use dict when you need to store additional info (like indices)

Patterns Used:
- Hash Map Lookup
- Complement Pattern
- Single Pass Algorithm

"""