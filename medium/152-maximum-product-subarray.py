"""
152. Maximum Product Subarray
Medium

Given an integer array nums, find a subarray that has the largest product, and 
return the product.

The test cases are generated so that the answer will fit in a 32-bit integer.

Note: The product of an array with a single element is the value of that element.

Example 1:
Input: nums = [2,3,-2,4]
Output: 6
Explanation: [2,3] has the largest product 6.

Example 2:
Input: nums = [-2,0,-1]
Output: 0
Explanation: The result cannot be 2, because [-2,-1] is not a subarray.

Constraints:
- 1 <= nums.length <= 2 * 10^4
- -10 <= nums[i] <= 10
- The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer
"""


class Solution(object):
    def maxProduct_solution1(self, nums):
        """
        SOLUTION 1: First Attempt with Lists
        
        Runtime: 5%
        Memory: 8%
        
        Approach:
        - Track current running product
        - Store max values in list when hitting 0
        - Keep list of all negative products
        - When negative, divide by max negative to potentially get positive
        
        Issues:
        - Uses lists which consume memory
        - Division operation to find max positive from negatives
        - O(n²) due to max(negativeList) operation inside loop
        - Complex logic with multiple tracking structures
        
        Time Complexity: O(n²) worst case
        Space Complexity: O(n) for lists
        """
        if len(nums) < 2:
            return nums[0]
        
        maxPro = 0
        curr = 0
        
        maxList = []
        negativeList = []
        
        for i in range(len(nums)):
            # Reset on zero
            if nums[i] == 0:
                maxList.append(curr)
                negativeList = []
            
            # Update current product
            curr = curr * nums[i] if curr != 0 else nums[i]
            
            # Update max
            maxPro = max(maxPro, curr)
            
            # Handle negative products
            if curr < 0:
                if negativeList:
                    # O(n) operation inside loop → O(n²) overall
                    maxPro = max(maxPro, curr // max(negativeList))
                negativeList.append(curr)
        
        # Check stored maxes
        if maxList:   
            maxPro = max(maxPro, max(maxList))
        
        return maxPro
    
    def maxProduct_solution2(self, nums):
        """
        SOLUTION 2: Improved with Single Negative Tracking
        
        Runtime: 80%
        Memory: 45%
        
        Approach:
        - Instead of list, track only the first/biggest negative
        - When new negative found, divide by previous negative
        - This converts two negatives into positive
        
        Key Improvement:
        - Changed from max(negativeList) to single negativeMax
        - One simple change → 80% faster!
        - Reduced space from O(n) to O(1)
        
        Still not optimal because:
        - Division logic is complex
        - Doesn't elegantly handle all cases
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        if len(nums) < 2:
            return nums[0]
        
        maxPro = 0
        curr = 0
        
        # Track the first/biggest negative instead of list
        negativeMax = float("-inf")
        
        for i in range(len(nums)):
            # Reset on zero
            if nums[i] == 0:
                negativeMax = float("-inf")
            
            # Update current product
            curr = curr * nums[i] if curr != 0 else nums[i]
            
            # Update max
            maxPro = max(maxPro, curr)
            
            # Handle negative products
            if curr < 0:
                if negativeMax != float("-inf"):
                    # Divide current negative by previous negative
                    # to potentially get positive
                    maxPro = max(maxPro, curr // negativeMax)
                negativeMax = max(negativeMax, curr)
        
        return maxPro
    
    def maxProduct_optimal_max_min(self, nums):
        """
        OPTIMAL SOLUTION 1: Track Max and Min Products
        
        Key Insight:
        In product-based problems, negative numbers flip signs.
        A big minimum (large negative) can become a maximum when
        multiplied by another negative.
        
        Strategy:
        - Track both maximum and minimum products ending at current position
        - When current number is negative, swap max and min
        - This is because:
          * max × negative = new min (large positive becomes large negative)
          * min × negative = new max (large negative becomes large positive)
        
        Algorithm:
        1. Initialize result, maxProd, minProd with first element
        2. For each element starting from second:
           a. If current is negative, swap maxProd and minProd
           b. Update maxProd = max(current, maxProd × current)
           c. Update minProd = min(current, minProd × current)
           d. Update result = max(result, maxProd)
        3. Return result
        
        Why This Works:
        - Handles negatives: Swap ensures large negative becomes candidate for max
        - Handles zeros: max(current, ...) starts fresh from current element
        - Handles positives: Naturally extends the product
        
        Example: [2, -5, -2, -4, 3]
        
        i=0: res=2, maxProd=2, minProd=2
        
        i=1, curr=-5 (negative):
          Swap: maxProd=2, minProd=2 (no effect since equal)
          maxProd = max(-5, 2×-5) = max(-5, -10) = -5
          minProd = min(-5, 2×-5) = min(-5, -10) = -10
          res = max(2, -5) = 2
        
        i=2, curr=-2 (negative):
          Swap: maxProd=-10, minProd=-5
          maxProd = max(-2, -10×-2) = max(-2, 20) = 20 ← Large positive!
          minProd = min(-2, -5×-2) = min(-2, 10) = -2
          res = max(2, 20) = 20
        
        i=3, curr=-4 (negative):
          Swap: maxProd=-2, minProd=20
          maxProd = max(-4, -2×-4) = max(-4, 8) = 8
          minProd = min(-4, 20×-4) = min(-4, -80) = -80
          res = max(20, 8) = 20
        
        i=4, curr=3 (positive):
          No swap
          maxProd = max(3, 8×3) = max(3, 24) = 24
          minProd = min(3, -80×3) = min(3, -240) = -240
          res = max(20, 24) = 24
        
        Final: 24
        
        Time Complexity: O(n) - single pass
        Space Complexity: O(1) - only three variables
        """
        res = nums[0]
        maxProd = nums[0]
        minProd = nums[0]

        # Traverse from second element
        for i in range(1, len(nums)):
            curr = nums[i]

            # Swap max and min if current is negative
            # Because: max × negative = min, min × negative = max
            if curr < 0:
                maxProd, minProd = minProd, maxProd

            # Update max product ending at current position
            # Either extend previous product or start fresh
            maxProd = max(curr, maxProd * curr)
            
            # Update min product ending at current position
            minProd = min(curr, minProd * curr)

            # Update global result
            res = max(res, maxProd)

        return res
    
    def maxProduct_optimal_prefix_suffix(self, nums):
        """
        OPTIMAL SOLUTION 2: Prefix-Suffix Traversal (Most Elegant!)
        
        Key Insight:
        The maximum product subarray is either:
        1. A prefix of the array (from start)
        2. A suffix of the array (from end)
        3. The entire array
        4. Something in between (captured by one of above)
        
        Why This Works:
        - Negative numbers in pairs create positive products
        - Odd negatives will be better from one direction
        - Zero resets the product (handled by resetting to 1)
        
        Strategy:
        - Calculate prefix product (left to right)
        - Calculate suffix product (right to left)
        - Track maximum of both at each step
        - Reset to 1 when encountering 0
        
        Example: [2, 3, -2, 4]
        
        Prefix (left → right):
        i=0: pre=2, suff=4(arr[3]), ans=max(-inf,2,4)=4
        i=1: pre=6, suff=-8(4×-2), ans=max(4,6,-8)=6
        i=2: pre=-12, suff=-24(-8×3), ans=max(6,-12,-24)=6
        i=3: pre=-48, suff=-48(-24×2), ans=max(6,-48,-48)=6
        
        Final: 6
        
        Why Both Directions:
        - Forward catches: [2,3] = 6
        - Backward catches: subarrays ending at back
        - Handles even/odd number of negatives
        
        Example with negatives: [-2, 3, -4]
        
        Prefix: -2, -6, 24
        Suffix: 24, -12, -4
        ans = max at each step = 24
        
        Time Complexity: O(n) - single pass
        Space Complexity: O(1) - only three variables
        
        This is the MOST ELEGANT solution!
        - No swapping needed
        - Handles all cases naturally
        - Simple to understand and implement
        """
        n = len(nums)
        
        # Initialize prefix and suffix products
        pre, suff = 1, 1
        
        # Initialize answer as negative infinity
        ans = float('-inf')
        
        # Traverse from both front and back simultaneously
        for i in range(n):
            # Reset prefix if zero (breaks continuity)
            if pre == 0:
                pre = 1
            
            # Reset suffix if zero
            if suff == 0:
                suff = 1
            
            # Multiply prefix with front element
            pre *= nums[i]
            
            # Multiply suffix with back element
            suff *= nums[n - i - 1]
            
            # Update maximum product from both directions
            ans = max(ans, pre, suff)
        
        return ans
    
    # Main function uses optimal prefix-suffix approach
    def maxProduct(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        return self.maxProduct_optimal_prefix_suffix(nums)

