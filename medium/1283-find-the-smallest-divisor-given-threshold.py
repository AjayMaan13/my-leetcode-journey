"""
1283. Find the Smallest Divisor Given a Threshold
Medium

Given an array of integers nums and an integer threshold, we will choose a positive 
integer divisor, divide all the array by it, and sum the division's result. Find the 
smallest divisor such that the result mentioned above is less than or equal to threshold.

Each result of the division is rounded to the nearest integer greater than or equal to 
that element. (For example: 7/3 = 3 and 10/2 = 5).

The test cases are generated so that there will be an answer.

Example 1:
Input: nums = [1,2,5,9], threshold = 6
Output: 5
Explanation: We can get a sum to 17 (1+2+5+9) if the divisor is 1. 
If the divisor is 4 we can get a sum of 7 (1+1+2+3) and if the divisor is 5 the sum 
will be 5 (1+1+1+2).

Example 2:
Input: nums = [44,22,33,11,1], threshold = 5
Output: 44

Constraints:
- 1 <= nums.length <= 5 * 10^4
- 1 <= nums[i] <= 10^6
- nums.length <= threshold <= 10^6
"""


class Solution(object):
    def smallestDivisor_original(self, nums, threshold):
        """
        ORIGINAL SOLUTION (Your Approach)
        
        Approach: Binary search on divisor value
        
        Key Insight:
        - Smaller divisor → larger sum
        - Larger divisor → smaller sum
        - Binary search to find minimum divisor where sum <= threshold
        
        Ceiling Division: (num + divisor - 1) // divisor
        
        Time: O(n log m) where m = max(nums)
        Space: O(1)
        
        Works correctly and efficiently!
        """
        def isThreshold(divisor):
            """Check if sum of divisions <= threshold"""
            sumNums = 0
            for num in nums:
                sumNums += (num + divisor - 1) // divisor
            
            return sumNums <= threshold
        
        low, high = 1, max(nums)
        
        while low < high:
            mid = (high + low) // 2
            
            if isThreshold(mid):
                high = mid
            else:
                low = mid + 1
        
        return low
    
    def smallestDivisor_optimized(self, nums, threshold):
        """
        OPTIMIZED SOLUTION: Using math.ceil and generator
        
        Improvements:
        - Use math.ceil() for clearer ceiling division
        - Use generator expression with sum() (more Pythonic)
        - Inline helper for potential performance boost
        
        Time: O(n log m)
        Space: O(1)
        """
        import math
        
        low, high = 1, max(nums)
        
        while low < high:
            mid = (low + high) // 2
            
            # Calculate sum using generator expression
            total = sum(math.ceil(num / float(mid)) for num in nums)
            
            if total <= threshold:
                high = mid
            else:
                low = mid + 1
        
        return low
    
    # Main function uses original solution
    def smallestDivisor(self, nums, threshold):
        """
        :type nums: List[int]
        :type threshold: int
        :rtype: int
        """
        return self.smallestDivisor_original(nums, threshold)