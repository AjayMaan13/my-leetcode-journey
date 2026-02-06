"""
Count the Number of Subarrays with Given XOR K

Problem Statement: 
Given an array of integers A and an integer B (k). Find the total number of 
subarrays having bitwise XOR of all elements equal to k.

Example 1:
Input: A = [4, 2, 2, 6, 4], k = 6
Output: 4
Explanation: The subarrays having XOR of their elements as 6 are:
- [4, 2] → 4 ⊕ 2 = 6
- [4, 2, 2, 6, 4] → 4 ⊕ 2 ⊕ 2 ⊕ 6 ⊕ 4 = 6
- [2, 2, 6] → 2 ⊕ 2 ⊕ 6 = 6
- [6] → 6

Example 2:
Input: A = [5, 6, 7, 8, 9], k = 5
Output: 2
Explanation: The subarrays having XOR of their elements as 5 are:
- [5] → 5
- [5, 6, 7, 8, 9] → 5 ⊕ 6 ⊕ 7 ⊕ 8 ⊕ 9 = 5

Related LeetCode Problem:
- 1442. Count Triplets That Can Form Two Arrays of Equal XOR

XOR Properties (Important!):
- a ⊕ a = 0 (XOR with itself gives 0)
- a ⊕ 0 = a (XOR with 0 gives same number)
- a ⊕ b = c implies a = b ⊕ c (reversible)
- XOR is commutative and associative
"""


class Solution(object):
    def subarrayXor_original(self, nums, k):
        """
        ORIGINAL SOLUTION (Your Approach)
        
        Approach: Prefix XOR + HashMap Frequency
        
        Issues:
        1. Unnecessary check: if len(nums) < 1
        2. Returns None instead of 0
        3. Variable name: "sum" should be "xor_value" (it's XOR, not sum)
        4. MAJOR BUG in else block:
           - else: freqXOR[sum] = 1
           - This happens when (sum ^ k) is NOT in freqXOR
           - But you're setting freqXOR[sum] = 1, which is wrong!
           - This should not be in else block
        5. Logic error: Always updates freqXOR[sum] even when found
        
        The line "freqXOR[sum] = 1 + freqXOR.get(sum, 0)" is OUTSIDE the if-else,
        which is correct, but having "freqXOR[sum] = 1" in else is wrong.
        
        Correct Logic:
        - Check if (prefix_xor ^ k) exists, add its count
        - Update frequency of current prefix_xor (always, not conditionally)
        
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        if len(nums) < 1:
            return None
        
        count = 0
        xor_value = 0
        freqXOR = {0: 1}  # Initialize: XOR 0 seen once
        
        for i in range(len(nums)):
            xor_value ^= nums[i]
            
            # ❌ BUG: else block sets freqXOR[xor_value] = 1
            if xor_value ^ k in freqXOR:
                count += freqXOR[xor_value ^ k]
            else:
                freqXOR[xor_value] = 1  # ❌ Wrong! Overwrites existing
            
            # This line runs regardless, but the else block above causes issues
            freqXOR[xor_value] = 1 + freqXOR.get(xor_value, 0)
        
        return count
    
    def subarrayXor_fixed(self, nums, k):
        """
        FIXED VERSION (Corrected Your Code)
        
        Removed the else block that was causing issues.
        
        Key Insight (XOR Property):
        If we want subarray with XOR = k:
        - prefix_xor[j] ⊕ prefix_xor[i-1] = k
        - Therefore: prefix_xor[i-1] = prefix_xor[j] ⊕ k
        
        Algorithm:
        1. Maintain prefix XOR and frequency map
        2. For each position, check if (current_xor ⊕ k) exists
        3. If yes, all those subarrays ending here have XOR = k
        4. Update frequency of current prefix XOR
        
        Time Complexity: O(n)
        Space Complexity: O(n)
        
        ⭐⭐ Fixed version of your solution
        """
        count = 0
        prefix_xor = 0
        xor_freq = {0: 1}  # Base case: XOR 0 appears once
        
        for num in nums:
            prefix_xor ^= num
            
            # Check if there's a previous prefix XOR such that:
            # current_xor ⊕ previous_xor = k
            # Which means: previous_xor = current_xor ⊕ k
            if (prefix_xor ^ k) in xor_freq:
                count += xor_freq[prefix_xor ^ k]
            
            # Update frequency of current prefix XOR
            xor_freq[prefix_xor] = xor_freq.get(prefix_xor, 0) + 1
        
        return count
    



"""
============================================================================
DETAILED EXPLANATION: Why XOR Works Like Prefix Sum
============================================================================

XOR Properties Review:
---------------------
1. a ⊕ a = 0 (self-canceling)
2. a ⊕ 0 = a (identity)
3. a ⊕ b = c → a = b ⊕ c (reversible)
4. XOR is commutative: a ⊕ b = b ⊕ a
5. XOR is associative: (a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)


How Prefix XOR Works:
--------------------
Similar to prefix sum, but using XOR operation!

Array:     [4,  2,  2,  6,  4]
Index:      0   1   2   3   4
Prefix XOR: 4   6   4   2   6

Prefix XOR[i] = nums[0] ⊕ nums[1] ⊕ ... ⊕ nums[i]

To get XOR of subarray [i+1...j]:
subarray_xor = prefix_xor[j] ⊕ prefix_xor[i]

Why? Because XOR is self-canceling!
prefix_xor[j] = nums[0]⊕nums[1]⊕...⊕nums[i]⊕nums[i+1]⊕...⊕nums[j]
prefix_xor[i] = nums[0]⊕nums[1]⊕...⊕nums[i]
prefix_xor[j] ⊕ prefix_xor[i] = nums[i+1]⊕...⊕nums[j] ✓


Example Walkthrough: nums = [4, 2, 2, 6, 4], k = 6
---------------------------------------------------------

Step-by-step execution:

Initial state:
  count = 0
  prefix_xor = 0
  xor_count = {0: 1}

Index 0: num = 4
  prefix_xor = 0 ⊕ 4 = 4
  needed_xor = 4 ⊕ 6 = 2
  Is 2 in {0: 1}? No
  count = 0
  xor_count = {0: 1, 4: 1}

Index 1: num = 2
  prefix_xor = 4 ⊕ 2 = 6
  needed_xor = 6 ⊕ 6 = 0
  Is 0 in {0: 1, 4: 1}? Yes! count += 1
  count = 1  ← Found [4, 2]
  xor_count = {0: 1, 4: 1, 6: 1}

Index 2: num = 2
  prefix_xor = 6 ⊕ 2 = 4
  needed_xor = 4 ⊕ 6 = 2
  Is 2 in {0: 1, 4: 1, 6: 1}? No
  count = 1
  xor_count = {0: 1, 4: 2, 6: 1}  ← 4 appears twice now!

Index 3: num = 6
  prefix_xor = 4 ⊕ 6 = 2
  needed_xor = 2 ⊕ 6 = 4
  Is 4 in {0: 1, 4: 2, 6: 1}? Yes! count += 2
  count = 3  ← Found [2, 2, 6] and another
  xor_count = {0: 1, 4: 2, 6: 1, 2: 1}

Index 4: num = 4
  prefix_xor = 2 ⊕ 4 = 6
  needed_xor = 6 ⊕ 6 = 0
  Is 0 in {0: 1, 4: 2, 6: 1, 2: 1}? Yes! count += 1
  count = 4  ← Found [6] or full array
  xor_count = {0: 1, 4: 2, 6: 2, 2: 1}

Final answer: 4 ✓


The 4 subarrays found:
1. [4, 2] (indices 0-1): 4 ⊕ 2 = 6
2. [2, 2, 6] (indices 1-3): 2 ⊕ 2 ⊕ 6 = 6
3. [6] (index 3): 6
4. [4, 2, 2, 6, 4] (indices 0-4): 4 ⊕ 2 ⊕ 2 ⊕ 6 ⊕ 4 = 6

"""