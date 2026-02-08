"""
Find the Repeating and Missing Numbers

Problem Statement: 
Given an integer array nums of size n containing values from [1, n] and each 
value appears exactly once in the array, except for A, which appears twice and 
B which is missing. Return the values A and B, as an array of size 2, where A 
appears in the 0-th index and B in the 1st index.

Note: You are not allowed to modify the original array.

Example 1:
Input: nums = [3, 5, 4, 1, 1]
Output: [1, 2]
Explanation: 1 appears twice in the array, and 2 is missing from the array.

Example 2:
Input: nums = [1, 2, 3, 6, 7, 5, 7]
Output: [7, 4]
Explanation: 7 appears twice in the array, and 4 is missing from the array.

Constraints:
- 2 <= n <= 10^4
- 1 <= nums[i] <= n
- nums contains n elements
"""


class Solution(object):
    def findErrorNums_brute_force(self, nums):
        """
        BRUTE FORCE APPROACH
        
        Algorithm:
        1. Use hashmap to find duplicate
        2. Use sum formula to find missing
        
        Time Complexity: O(n)
        Space Complexity: O(n) - hashmap storage
        """
        n = len(nums)
        seen = {}
        repeating = -1
        
        # Find repeating number
        for num in nums:
            if num in seen:
                repeating = num
                break
            seen[num] = 1
        
        # Find missing number using sum formula
        # Sum of 1 to n = n * (n + 1) / 2
        expected_sum = n * (n + 1) // 2
        actual_sum = sum(nums)
        
        # Missing = expected_sum - (actual_sum - repeating)
        # Because actual_sum has repeating counted twice
        missing = expected_sum - actual_sum + repeating
        
        return [repeating, missing]
    
    def findErrorNums_math(self, nums):
        """
        OPTIMAL APPROACH 1: Mathematical Equations
        
        Key Insight:
        Let repeating = x, missing = y
        
        We can create two equations:
        1. (sum of nums) - (sum of 1 to n) = x - y
        2. (sum of squares of nums) - (sum of squares of 1 to n) = x² - y² 
            or actual_sum_square = expected_sum_square - y² + x²
            (1² + 2² + 3² + ... + x² + ... + x² + ... + n²) i.e actual sum square
                                             ↑           ↑
                                            (appears twice, y is missing))
        
        From these two equations, we can solve for x and y.
        
        Mathematical derivation:
        Let S1 = x - y (difference from equation 1)
        Let S2 = x² - y² = (x + y)(x - y) (difference from equation 2)
        
        Therefore: x + y = S2 / S1
        And: x - y = S1
        
        Solving:
        x = ((x + y) + (x - y)) / 2 = (S2/S1 + S1) / 2
        y = ((x + y) - (x - y)) / 2 = (S2/S1 - S1) / 2
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        n = len(nums)
        
        # Calculate expected sum: 1 + 2 + ... + n = n(n+1)/2
        expected_sum = n * (n + 1) // 2
        
        # Calculate expected sum of squares: 1² + 2² + ... + n² = n(n+1)(2n+1)/6
        expected_sum_sq = n * (n + 1) * (2 * n + 1) // 6
        
        # Calculate actual sum and sum of squares
        actual_sum = 0
        actual_sum_sq = 0
        for num in nums:
            actual_sum += num
            actual_sum_sq += num * num
        
        # S1 = x - y (repeating - missing)
        diff = actual_sum - expected_sum
        
        # S2 = x² - y² = (x + y)(x - y)
        diff_sq = actual_sum_sq - expected_sum_sq
        
        # x + y = S2 / S1
        sum_xy = diff_sq // diff
        
        # Now we have:
        # x + y = sum_xy
        # x - y = diff
        # Solving: x = (sum_xy + diff) / 2
        #          y = (sum_xy - diff) / 2
        
        repeating = (sum_xy + diff) // 2
        missing = (sum_xy - diff) // 2
        
        return [repeating, missing]
    
    def findErrorNums_xor_optimal(self, nums):
        """
        OPTIMAL APPROACH 2: XOR Bit Manipulation (MOST ELEGANT!)
        
        XOR Properties:
        - a ⊕ a = 0 (XOR with itself gives 0)
        - a ⊕ 0 = a (XOR with 0 gives same number)
        - XOR is commutative and associative
        
        Algorithm:
        
        Step 1: XOR all array elements with numbers 1 to n
        -------
        Let repeating = x, missing = y
        Result = (nums[0] ⊕ nums[1] ⊕ ... ⊕ nums[n-1]) ⊕ (1 ⊕ 2 ⊕ ... ⊕ n)
        
        All numbers except x and y will cancel out (appear twice, XOR to 0)
        Result = x ⊕ y
        
        Step 2: Find differentiating bit position
        ------------------------------------------
        x and y are different numbers, so their XOR (x ⊕ y) will have at least 
        one bit set to 1. This bit is 1 in one number and 0 in the other.
        
        To find the rightmost set bit:
        bit = xr & ~(xr - 1)
        OR
        bit = xr & (-xr)  [simpler]
        
        Example: xr = 6 (binary: 110)
        -xr = -6 (two's complement: ...11111010)
        xr & (-xr) = 110 & ...11111010 = 010 (isolates rightmost set bit)
        
        Step 3: Partition into two groups
        ----------------------------------
        Divide all numbers (both from array and 1 to n) into two groups:
        - Group 0: numbers with this bit = 0
        - Group 1: numbers with this bit = 1
        
        One group will contain x, the other will contain y.
        XOR all numbers in each group separately.
        
        Step 4: Identify which is repeating and which is missing
        ---------------------------------------------------------
        Count occurrences of 'zero' in the array:
        - If it appears twice → zero is repeating, one is missing
        - If it appears once → zero is missing, one is repeating
        - If it appears zero times → zero is missing, one is repeating
        
        Time Complexity: O(n) - two passes through array
        Space Complexity: O(1) - only using variables
        """
        n = len(nums)
        
        # Step 1: XOR all array elements with numbers 1 to n
        # Result will be: repeating ⊕ missing
        xr = 0
        for num in nums:
            xr ^= num
        for i in range(1, n + 1):
            xr ^= i
        
        # Now xr = repeating ⊕ missing
        
        # Step 2: Find the rightmost set bit in xr
        # This bit differentiates repeating and missing
        # Method: xr & (-xr) isolates the rightmost set bit
        bit = xr & (-xr)
        
        # Alternative method (both work):
        # bit = xr & ~(xr - 1)
        
        # Step 3: Partition numbers into two groups based on this bit
        zero = 0  # Numbers with bit = 0
        one = 0   # Numbers with bit = 1
        
        # Process array elements
        for num in nums:
            if num & bit:  # Check if bit is set in num
                one ^= num  # Add to group 1
            else:
                zero ^= num  # Add to group 0
        
        # Process numbers 1 to n
        for i in range(1, n + 1):
            if i & bit:  # Check if bit is set in i
                one ^= i
            else:
                zero ^= i
        
        # After this, one of {zero, one} is repeating, other is missing
        
        # Step 4: Identify which is repeating and which is missing
        # Count how many times 'zero' appears in the array
        count = 0
        for num in nums:
            if num == zero:
                count += 1
        
        # If zero appears twice, it's the repeating number
        if count == 2:
            return [zero, one]  # [repeating, missing]
        else:
            return [one, zero]  # [repeating, missing]
    
    def findErrorNums_xor_commented(self, nums):
        """
        SAME AS XOR OPTIMAL but with DETAILED STEP-BY-STEP COMMENTS
        """
        n = len(nums)
        
        # STEP 1: Get XOR of repeating and missing
        # ========================================
        # XOR all array elements with all numbers from 1 to n
        # Since all numbers except repeating and missing appear exactly once
        # in the combined set, they will cancel out (a ⊕ a = 0)
        # Result: repeating ⊕ missing
        
        xr = 0
        
        # XOR all array elements
        for num in nums:
            xr ^= num
        
        # XOR with numbers 1 to n
        for i in range(1, n + 1):
            xr ^= i
        
        # Now: xr = repeating ⊕ missing
        # Example: if repeating=7, missing=4
        # xr = 7 ⊕ 4 = 0111 ⊕ 0100 = 0011 (binary)
        
        # STEP 2: Find a differentiating bit
        # ===================================
        # Find a bit position where repeating and missing differ
        # We'll use the rightmost set bit in xr
        
        # Method 1: Using two's complement
        # -xr in two's complement flips all bits and adds 1
        # xr & (-xr) isolates the rightmost set bit
        bit = xr & (-xr)
        
        # Example: xr = 0011 (binary 3)
        # -xr = ...11111101 (two's complement)
        # xr & (-xr) = 0001 (rightmost set bit)
        
        # Method 2 (alternative): Using bitwise NOT
        # bit = xr & ~(xr - 1)
        
        # STEP 3: Partition into two groups
        # ==================================
        # Split all numbers (array + 1 to n) based on this bit
        # One group will have repeating, other will have missing
        
        zero = 0  # XOR of all numbers with this bit = 0
        one = 0   # XOR of all numbers with this bit = 1
        
        # Partition array elements
        for num in nums:
            # Check if the differentiating bit is set in num
            if num & bit:
                # Bit is 1: add to 'one' group
                one ^= num
            else:
                # Bit is 0: add to 'zero' group
                zero ^= num
        
        # Partition numbers 1 to n
        for i in range(1, n + 1):
            if i & bit:
                one ^= i
            else:
                zero ^= i
        
        # After this loop:
        # - All numbers in each group cancel out (appear twice)
        # - Except for one number in each group (appears once)
        # - 'zero' holds one of {repeating, missing}
        # - 'one' holds the other of {repeating, missing}
        
        # STEP 4: Determine which is which
        # =================================
        # Count how many times 'zero' appears in the original array
        
        count = 0
        for num in nums:
            if num == zero:
                count += 1
        
        # If 'zero' appears twice → it's the repeating number
        # If 'zero' appears once or zero times → it's the missing number
        
        if count == 2:
            # zero is repeating, one is missing
            return [zero, one]
        else:
            # one is repeating, zero is missing
            return [one, zero]
    
    # Main function uses XOR approach (most optimal)
    def findErrorNums(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        return self.findErrorNums_xor_optimal(nums)


"""
============================================================================
VISUAL EXAMPLE: XOR APPROACH
============================================================================

Example: nums = [1, 2, 3, 6, 7, 5, 7]
n = 7, repeating = 7, missing = 4

STEP 1: XOR all elements
------------------------
Array:    1 ⊕ 2 ⊕ 3 ⊕ 6 ⊕ 7 ⊕ 5 ⊕ 7
Range:    1 ⊕ 2 ⊕ 3 ⊕ 4 ⊕ 5 ⊕ 6 ⊕ 7

Combined: 
All appear twice except 7 (appears 3 times) and 4 (appears 1 time)
After cancellation: 7 ⊕ 4

xr = 7 ⊕ 4 = 0111 ⊕ 0100 = 0011 (binary) = 3 (decimal)


STEP 2: Find differentiating bit
---------------------------------
xr = 3 = 0011 (binary)
-xr = -3 = ...11111101 (two's complement)
xr & (-xr) = 0011 & ...11111101 = 0001

bit = 1 (the rightmost set bit, position 0)


STEP 3: Partition based on bit position 0
------------------------------------------
Numbers with bit 0 = 0 (even): 2, 4, 6
Numbers with bit 0 = 1 (odd):  1, 3, 5, 7

Group 0 (bit = 0):
  From array: 2, 6 → XOR = 2 ⊕ 6 = 4
  From range: 2, 4, 6 → XOR = 2 ⊕ 4 ⊕ 6 = 0
  zero = 4 ⊕ 0 = 4

Group 1 (bit = 1):
  From array: 1, 3, 7, 5, 7 → XOR = 1 ⊕ 3 ⊕ 7 ⊕ 5 ⊕ 7 = 7
  From range: 1, 3, 5, 7 → XOR = 1 ⊕ 3 ⊕ 5 ⊕ 7 = 0
  one = 7 ⊕ 0 = 7


STEP 4: Identify repeating and missing
---------------------------------------
Count occurrences of zero (4) in array: 0 times
Count occurrences of one (7) in array: 2 times

Since one (7) appears twice → one is repeating
Since zero (4) appears 0 times → zero is missing

Result: [7, 4] ✓


============================================================================
WHY XOR & (-XOR) FINDS RIGHTMOST SET BIT
============================================================================

Example: xr = 12 = 1100 (binary)

Step 1: Calculate -xr (two's complement)
  Original:     0000 1100
  Invert bits:  1111 0011
  Add 1:        1111 0100
  -xr = -12 =   1111 0100

Step 2: AND with original
  xr:           0000 1100
  -xr:          1111 0100
  xr & (-xr):   0000 0100 ← Rightmost set bit isolated!

Why this works:
- Two's complement flips all bits and adds 1
- This causes all trailing zeros to become ones
- The rightmost 1 in original becomes 1 in result
- All bits to the left flip and cancel out with AND


============================================================================
COMPLEXITY COMPARISON
============================================================================

Approach                    Time        Space       Notes
------------------------------------------------------------------------
Brute Force (HashMap)       O(n)        O(n)        Simple, extra space
Math (Sum + Sum²)           O(n)        O(1)        Risk of overflow
XOR (Bit Manipulation)      O(n)        O(1)        Optimal! No overflow
"""