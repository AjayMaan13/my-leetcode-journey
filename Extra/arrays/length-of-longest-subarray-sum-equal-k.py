"""
Length of Longest Subarray with Zero Sum
(Also known as: Maximum Length of Subarray Having Sum Zero)

Problem Statement: 
Given an array containing both positive and negative integers, find the length 
of the longest subarray with the sum of all elements equal to zero.

Example 1:
Input: N = 6, array[] = {9, -3, 3, -1, 6, -5}
Output: 5
Explanation: The following subarrays sum to zero:
- {-3, 3} (length 2)
- {-1, 6, -5} (length 3)
- {-3, 3, -1, 6, -5} (length 5) ← longest
The length of the longest subarray with sum zero is 5.

Example 2:
Input: N = 8, array[] = {6, -2, 2, -8, 1, 7, 4, -10}
Output: 8
Explanation: Subarrays with sum zero:
- {-2, 2} (length 2)
- {-8, 1, 7} (length 3)
- {-2, 2, -8, 1, 7} (length 5)
- {6, -2, 2, -8, 1, 7, 4, -10} (length 8) ← longest (entire array)

Related LeetCode Problems:
- 525. Contiguous Array (binary array version)
- 560. Subarray Sum Equals K (generalized version)
"""


class Solution(object):
    def getLongestZeroSumSubarrayLength_original(self, nums):
        """
        ORIGINAL SOLUTION (Your Approach)
        
        Approach: Prefix Sum + HashMap
        
        Key Insight:
        - If prefix_sum at index i equals prefix_sum at index j (where i < j),
          then the subarray between i+1 and j has sum = 0
        - Store first occurrence of each prefix sum
        - When we see same prefix sum again, calculate length
        
        Issues:
        1. Unnecessary check: if len(nums) < 1 (no such constraint)
        2. Returns None instead of 0
        3. Variable name: "sum" shadows built-in function (use prefix_sum)
        4. Redundant check: if sum not in prefixSum (can use .get() or .setdefault())
        
        Your Logic is CORRECT! ✓
        - Handle sum == 0 case (subarray from start)
        - Store first occurrence only
        - Calculate max length when duplicate found
        
        Time Complexity: O(n) - single pass
        Space Complexity: O(n) - hashmap stores up to n prefix sums
        
        ⭐⭐ Good solution, just needs minor cleanup
        """
        if len(nums) < 1:
            return None  # Should return 0
        
        max_length = 0
        prefix_sum = 0
        sum_index = {}  # Maps prefix_sum → first index where it appears
        
        for i in range(len(nums)):
            prefix_sum += nums[i]
            
            # Case 1: Subarray from beginning [0...i] has sum 0
            if prefix_sum == 0:
                max_length = i + 1
            
            # Case 2: We've seen this prefix_sum before
            # Subarray from (previous_index+1) to i has sum 0
            if prefix_sum in sum_index:
                max_length = max(i - sum_index[prefix_sum], max_length)
            
            # Store first occurrence only (don't update if already exists)
            if prefix_sum not in sum_index:
                sum_index[prefix_sum] = i
        
        return max_length
    
    def getLongestZeroSumSubarrayLength_optimized(self, nums):
        """
        OPTIMIZED SOLUTION (Clean Version)
        
        Same logic as original but with improvements:
        1. Removed unnecessary check
        2. Use setdefault() for cleaner code
        3. Better variable names
        4. Initialize hashmap with {0: -1} to handle edge case
        
        Why {0: -1}?
        - If prefix_sum becomes 0 at index i, subarray [0...i] has sum 0
        - Length = i - (-1) = i + 1 ✓
        - Handles this case automatically without special check!
        
        Time Complexity: O(n)
        Space Complexity: O(n)
        
        ⭐⭐⭐ OPTIMAL SOLUTION!
        """
        max_length = 0
        prefix_sum = 0
        # Initialize with {0: -1} to handle subarray starting from index 0
        sum_index = {0: -1}
        
        for i in range(len(nums)):
            prefix_sum += nums[i]
            
            if prefix_sum in sum_index:
                # Found duplicate prefix_sum
                # Subarray from (sum_index[prefix_sum] + 1) to i has sum 0
                max_length = max(max_length, i - sum_index[prefix_sum])
            else:
                # Store first occurrence
                sum_index[prefix_sum] = i
        
        return max_length
    
    def getLongestZeroSumSubarrayLength_pythonic(self, nums):
        """
        PYTHONIC VERSION (Most Concise)
        
        Uses setdefault() for even cleaner code
        """
        max_length = 0
        prefix_sum = 0
        sum_index = {0: -1}
        
        for i, num in enumerate(nums):
            prefix_sum += num
            
            # setdefault returns existing value or sets and returns default
            # If prefix_sum exists: returns old index (doesn't update)
            # If prefix_sum new: sets to i and returns i
            first_occurrence = sum_index.setdefault(prefix_sum, i)
            
            if first_occurrence != i:
                # We've seen this prefix_sum before
                max_length = max(max_length, i - first_occurrence)
        
        return max_length
  