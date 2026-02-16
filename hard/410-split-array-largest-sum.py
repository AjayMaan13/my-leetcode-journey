"""
410. SPLIT ARRAY LARGEST SUM

Problem Statement:
Given an integer array nums and an integer k, split nums into k non-empty 
subarrays such that the largest sum of any subarray is minimized.
Return the minimized largest sum of the split.

A subarray is a contiguous part of the array.

Example 1:
Input: nums = [7,2,5,10,8], k = 2
Output: 18
Explanation: There are four ways to split nums into two subarrays.
The best way is to split it into [7,2,5] and [10,8], where the largest sum 
among the two subarrays is only 18.

Example 2:
Input: nums = [1,2,3,4,5], k = 2
Output: 9
Explanation: There are four ways to split nums into two subarrays.
The best way is to split it into [1,2,3] and [4,5], where the largest sum 
among the two subarrays is only 9.
"""


# ==============================================================================
# SOLUTION 1: YOUR ORIGINAL SOLUTION
# ==============================================================================
# Time Complexity: O(N * log(sum - max))
# Space Complexity: O(1)

class Solution:
    def splitArray(self, nums, k):
        """
        Binary search on the answer space to find minimum largest sum
        """
        # Edge case: if we have fewer elements than k subarrays needed
        if len(nums) < k:
            return -1
        
        def countK(limit):
            """
            Count number of subarrays needed if max sum per subarray is 'limit'
            
            Logic: Keep adding elements to current subarray until adding next
            element would exceed limit, then start a new subarray.
            """
            count = 0  # Number of subarrays formed
            subSum = 0  # Current subarray sum
            
            for num in nums:
                subSum += num  # Try to add current number
                
                if subSum > limit:
                    # Current subarray exceeded limit
                    subSum = num  # Start new subarray with current number
                    count += 1  # Increment subarray count
            
            # Don't forget the last subarray if it has elements
            if subSum != 0:
                count += 1
                
            return count
        
        # Define search space:
        low = max(nums)   # Minimum possible: largest single element
        high = sum(nums)  # Maximum possible: all elements in one subarray
        res = -1
        
        # Binary search on the answer space
        while low <= high:
            # Try mid as the maximum sum allowed per subarray
            mid = (high + low) // 2
            
            # How many subarrays needed with this limit?
            subarrays_needed = countK(mid)
            
            # If we can fit into k or fewer subarrays
            if subarrays_needed <= k:
                res = mid  # This is a valid answer, store it
                high = mid - 1  # Try to find a smaller maximum (minimize)
            else:
                # Too many subarrays needed! Limit is too small
                # Need to increase the limit to reduce number of subarrays
                low = mid + 1
        
        return res


# ==============================================================================
# SOLUTION 2: OPTIMIZED VERSION (CLEANER CODE)
# ==============================================================================
# Time Complexity: O(N * log(sum - max))
# Space Complexity: O(1)

class Solution_Optimized:
    def splitArray(self, nums, k):
        """
        Binary search on answer space - find minimum of maximum subarray sums
        
        Key Insight: If we can split array with max sum = X, we can also do it
        with any max sum > X. This monotonic property enables binary search.
        """
        
        def canSplit(max_sum):
            """
            Check if we can split array into k or fewer subarrays
            where each subarray sum ≤ max_sum
            
            Returns: True if possible, False otherwise
            """
            subarrays = 1  # Start with first subarray
            current_sum = 0  # Sum of current subarray
            
            for num in nums:
                # Try adding current number to current subarray
                if current_sum + num <= max_sum:
                    current_sum += num  # Add to current subarray
                else:
                    # Need a new subarray for this number
                    subarrays += 1
                    current_sum = num  # Start new subarray with this number
                    
                    # If we already exceed k subarrays, can't do it
                    if subarrays > k:
                        return False
            
            return True  # Successfully split into ≤ k subarrays
        
        # Define search boundaries:
        # Minimum: largest element (each element must fit in a subarray)
        # Maximum: sum of all elements (everything in one subarray)
        left = max(nums)
        right = sum(nums)
        result = right  # Initialize with worst case
        
        # Binary search for the minimum possible maximum sum
        while left <= right:
            mid = (left + right) // 2  # Try this as max sum per subarray
            
            # Can we split with this max sum?
            if canSplit(mid):
                # Yes! This works, but can we do better (smaller)?
                result = mid  # Store this valid answer
                right = mid - 1  # Search for smaller values
            else:
                # No! Max sum too small, need larger value
                left = mid + 1  # Search for larger values
        
        return result
