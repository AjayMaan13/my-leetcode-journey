"""
53. Maximum Subarray

Given an integer array nums, find the subarray with the largest sum, 
and return its sum.

Example 1:
Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: The subarray [4,-1,2,1] has the largest sum 6.

Example 2:
Input: nums = [1]
Output: 1
Explanation: The subarray [1] has the largest sum 1.

Example 3:
Input: nums = [5,4,-1,7,8]
Output: 23
Explanation: The subarray [5,4,-1,7,8] has the largest sum 23.

Constraints:
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4
"""



# ============================================================================
# SOLUTION 1 - Prefix Sum Approach (Fixed)
# Time: O(n), Space: O(1)
# ============================================================================

class Solution1:
    def maxSubArray(self, nums):
        """
        Prefix Sum with Min Tracking
        
        Key Insight:
        - Subarray sum from index i to j = prefixSum[j] - prefixSum[i-1]
        - To maximize: need max(prefixSum[j]) - min(prefixSum[i]) where i < j
        - Track minimum prefix sum seen so far
        
        Algorithm:
        1. Keep running prefix sum
        2. Track minimum prefix sum encountered
        3. At each position: max_sum = current_prefix - min_prefix
        """
        if len(nums) < 1:
            return None
        
        max_sum = float('-inf')  # Maximum subarray sum found
        current_sum = 0          # Current prefix sum
        min_sum = 0              # Minimum prefix sum seen so far
        
        for num in nums:
            current_sum += num
            # Subarray sum ending here = current_sum - min_sum
            max_sum = max(max_sum, current_sum - min_sum)
            # Update minimum prefix sum
            min_sum = min(min_sum, current_sum)
        
        return max_sum


# ============================================================================
# SOLUTION 2 - Kadane's Algorithm (OPTIMAL - Most Common)
# Time: O(n), Space: O(1)
# ============================================================================

class Solution2:
    def maxSubArray(self, nums):
        """
        Kadane's Algorithm - Dynamic Programming Approach
        
        Core Idea:
        At each position, decide:
        - Extend previous subarray (add current element)
        - OR start new subarray from current element
        
        Rule: If current_sum becomes negative, reset to 0
        Why? Negative sum will only decrease future sums, better to start fresh
        
        Algorithm:
        1. Initialize max_sum and current_sum
        2. For each element:
           - If current_sum < 0, reset to 0 (start fresh)
           - Add current element to current_sum
           - Update max_sum if current_sum is larger
        """
        max_sum = nums[0]     # Track overall maximum
        current_sum = 0       # Current subarray sum
        
        for num in nums:
            if current_sum < 0:
                current_sum = 0  # Reset if negative (start new subarray)
            current_sum += num
            max_sum = max(max_sum, current_sum)
        
        return max_sum


# ============================================================================
# SOLUTION 3 - Kadane's Algorithm (Alternative Form)
# Time: O(n), Space: O(1)
# ============================================================================

class Solution3:
    def maxSubArray(self, nums):
        """
        Kadane's Algorithm - DP interpretation
        
        DP Logic:
        dp[i] = maximum subarray sum ending at index i
        dp[i] = max(nums[i], dp[i-1] + nums[i])
        
        Translation: Either start fresh with current element,
        or extend previous subarray by adding current element
        """
        max_sum = nums[0]
        current_max = nums[0]  # Max sum ending at current position
        
        for i in range(1, len(nums)):
            # Either extend previous subarray or start new one
            current_max = max(nums[i], current_max + nums[i])
            max_sum = max(max_sum, current_max)
        
        return max_sum


# ============================================================================
# VISUAL WALKTHROUGH: Kadane's Algorithm
# ============================================================================

"""
Example: nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

Index | num | current_sum (before) | Reset? | current_sum (after) | max_sum
------|-----|---------------------|--------|--------------------|---------
  0   | -2  |         0           |  No    |        -2          |   -2
  1   |  1  |        -2           |  Yes   |         1          |    1
  2   | -3  |         1           |  No    |        -2          |    1
  3   |  4  |        -2           |  Yes   |         4          |    4
  4   | -1  |         4           |  No    |         3          |    4
  5   |  2  |         3           |  No    |         5          |    5
  6   |  1  |         5           |  No    |         6          |    6  ✓
  7   | -5  |         6           |  No    |         1          |    6
  8   |  4  |         1           |  No    |         5          |    6

Final Answer: 6 (subarray [4, -1, 2, 1])

Key Observations:
- When current_sum goes negative (index 1, 3), we reset
- We keep extending while sum stays positive or improves
- Maximum is found at index 6
"""


# ============================================================================
# VISUAL WALKTHROUGH: Prefix Sum Approach
# ============================================================================

"""
Example: nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

Index | num | current_sum | min_sum | max_sum (current - min)
------|-----|-------------|---------|------------------------
  0   | -2  |     -2      |   -2    |   0  (-2 - (-2))
  1   |  1  |     -1      |   -2    |   1  (-1 - (-2))
  2   | -3  |     -4      |   -4    |   1
  3   |  4  |      0      |   -4    |   4  (0 - (-4))
  4   | -1  |     -1      |   -4    |   4  (max stays)
  5   |  2  |      1      |   -4    |   5  (1 - (-4))
  6   |  1  |      2      |   -4    |   6  (2 - (-4))  ✓
  7   | -5  |     -3      |   -4    |   6
  8   |  4  |      1      |   -4    |   6

Explanation:
- Subarray sum = current_prefix - previous_prefix
- To maximize, subtract smallest previous prefix
- At index 6: prefix=2, min_prefix=-4 → sum=6
"""


# ============================================================================
# FOLLOW-UP: Print the Subarray with Maximum Sum
# ============================================================================

"""
Follow-up Question:
Can you print the subarray that has the maximum sum?
"""

class SolutionWithSubarray:
    def maxSubArray(self, nums):
        """
        Kadane's Algorithm + Track Subarray Indices
        
        Track:
        - start: starting index of current subarray
        - ansStart, ansEnd: indices of the maximum subarray
        """
        max_sum = nums[0]
        current_sum = 0
        
        start = 0           # Start of current subarray
        ansStart = 0        # Start of maximum subarray
        ansEnd = 0          # End of maximum subarray
        
        for i in range(len(nums)):
            if current_sum < 0:
                current_sum = 0
                start = i    # Reset start index for new subarray
            
            current_sum += nums[i]
            
            if current_sum > max_sum:
                max_sum = current_sum
                ansStart = start
                ansEnd = i
        
        # Print the subarray
        print(f"Maximum subarray: {nums[ansStart:ansEnd+1]}")
        print(f"Indices: [{ansStart}, {ansEnd}]")
        
        return max_sum


# Example usage:
nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
solution = SolutionWithSubarray()
result = solution.maxSubArray(nums)
print(f"Maximum sum: {result}")

# Output:
# Maximum subarray: [4, -1, 2, 1]
# Indices: [3, 6]
# Maximum sum: 6

# ============================================================================
# INTERVIEW TIPS
# ============================================================================

"""
1. Start with brute force explanation (O(n²) - check all subarrays)
2. Optimize to Kadane's algorithm (O(n))
3. Explain the "reset when negative" logic clearly
4. Mention DP interpretation as alternative view

Common follow-ups:
- Return the actual subarray (not just sum) → track start/end indices
- What if array is empty? → Handle edge case
- What about circular array? → Different problem (use modified Kadane's)
- Find K subarrays with maximum sum → More complex DP

Key insight to emphasize:
"Negative running sum hurts future elements, so we start fresh"
"""