"""
560. Subarray Sum Equals K
Medium

Given an array of integers nums and an integer k, return the total number of 
subarrays whose sum equals to k.

A subarray is a contiguous non-empty sequence of elements within an array.

Example 1:
Input: nums = [1,1,1], k = 2
Output: 2
Explanation: The subarrays are [1,1] and [1,1] (at different positions)

Example 2:
Input: nums = [1,2,3], k = 3
Output: 2
Explanation: The subarrays are [1,2] and [3]

Constraints:
- 1 <= nums.length <= 2 * 10^4
- -1000 <= nums[i] <= 1000
- -10^7 <= k <= 10^7
"""


class Solution(object):
    def subarraySum_original(self, nums, k):
        """
        ORIGINAL SOLUTION (Your Approach)
        
        Pattern: Prefix Sum + HashMap Frequency
        
        Issues:
        1. Unnecessary check: if len(nums) < 1 (constraints guarantee nums.length >= 1)
        2. Returns None instead of 0 for empty array (should return 0)
        3. Redundant condition: if prefix == k is already handled by (prefix - k) in freq
        4. Verbose frequency update: can use .get() method more cleanly
        
        Time Complexity: O(n) - single pass through array
        Space Complexity: O(n) - hashmap can store up to n prefix sums
        """
        if len(nums) < 1:
            return None  # Should return 0, not None
            
        count = 0
        prefix = 0
        freq = {0: 1}  # Base case: prefix sum 0 appears once
        
        for num in nums:
            prefix += num
            
            # This condition has redundancy
            if prefix == k or (prefix - k) in freq:
                count += freq[prefix - k]
            
            # Verbose frequency update
            if prefix in freq:
                freq[prefix] += 1 
            else:
                freq[prefix] = 1
        
        return count
    
    def subarraySum_optimized(self, nums, k):
        """
        OPTIMIZED SOLUTION
        
        Pattern: Prefix Sum + HashMap Frequency
        
        Key Insight:
        - For a subarray nums[i:j+1] to have sum k:
          prefix[j] - prefix[i-1] = k
          Therefore: prefix[i-1] = prefix[j] - k
        - We look for (current_prefix - k) in our hashmap
        
        Algorithm:
        1. Initialize: count = 0, prefix_sum = 0, freq = {0: 1}
        2. For each number:
           a. Add to prefix_sum
           b. Check if (prefix_sum - k) exists in freq
           c. If yes, add freq[prefix_sum - k] to count
           d. Update freq for current prefix_sum
        
        Why freq = {0: 1}?
        - Handles case where subarray starts from index 0
        - Example: [1,2,3], k=3 → when we reach [3], prefix=3, need prefix-k=0
        
        Improvements over original:
        1. Removed unnecessary length check
        2. Removed redundant "prefix == k" check (covered by freq lookup)
        3. Cleaner frequency update using .get()
        4. More readable variable names
        
        Time Complexity: O(n) - single pass through array
        Space Complexity: O(n) - hashmap stores unique prefix sums
        """
        count = 0
        prefix_sum = 0
        freq = {0: 1}  # Initialize with 0 to handle subarrays starting at index 0
        
        for num in nums:
            # Update prefix sum
            prefix_sum += num
            
            # Check if there exists a previous prefix sum such that:
            # current_prefix_sum - previous_prefix_sum = k
            # Which means: previous_prefix_sum = current_prefix_sum - k
            if (prefix_sum - k) in freq:
                count += freq[prefix_sum - k]
            
            # Update frequency of current prefix sum
            freq[prefix_sum] = freq.get(prefix_sum, 0) + 1
        
        return count
    
    # Main function uses optimized approach
    def subarraySum(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        return self.subarraySum_optimized(nums, k)

