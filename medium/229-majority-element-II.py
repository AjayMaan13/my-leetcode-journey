"""
229. Majority Element II
Medium

Given an integer array of size n, find all elements that appear more than ⌊n/3⌋ times.

Example 1:
Input: nums = [3,2,3]
Output: [3]
Explanation: 3 appears 2 times, which is > 3/3 = 1

Example 2:
Input: nums = [1]
Output: [1]
Explanation: 1 appears 1 time, which is > 1/3 = 0.33

Example 3:
Input: nums = [1,2]
Output: [1,2]
Explanation: Both appear 1 time, which is > 2/3 = 0.66

Constraints:
- 1 <= nums.length <= 5 * 10^4
- -10^9 <= nums[i] <= 10^9

Follow up: Could you solve the problem in linear time and in O(1) space?
"""

from collections import defaultdict


class Solution(object):
    def majorityElement_original(self, nums):
        """
        ORIGINAL SOLUTION (My Original Approach)
        
        Approach: HashMap frequency count
        
        Issues:
        1. Unnecessary check: if len(nums) < 1 (constraints guarantee len >= 1)
        2. Returns None instead of []
        3. Uses float division (/) instead of integer division (//)
           - Python 2: 5/3 = 1 ✓
           - Python 3: 5/3 = 1.666... ❌
           - Should use: 5//3 = 1 ✓
        4. Uses set then converts to list (unnecessary conversion)
        
        Time Complexity: O(n) - single pass + set operations
        Space Complexity: O(n) - hashmap can store up to n unique elements
        
        Pros:
        - Simple and straightforward
        - Easy to understand
        
        Cons:
        - O(n) space (doesn't meet follow-up requirement)
        - Float division issue
        """
        if len(nums) < 1:
            return  # Returns None
        
        output = set()
        freq = {}
        n = len(nums) / 3  # Float division in Python 3
        
        for num in nums:
            freq[num] = freq.get(num, 0) + 1 
            if freq[num] > n:
                output.add(num)
        
        return list(output)
    
    def majorityElement_hashmap_clean(self, nums):
        """
        APPROACH 1: Clean HashMap (Fixed Version of Original)
        
        Improvements:
        1. Removed unnecessary check
        2. Fixed division to use integer division (//)
        3. Use list directly instead of set conversion
        4. Return empty list for edge cases
        
        Time Complexity: O(n)
        Space Complexity: O(n)
        
        ⭐ Rating: Good for readability, but uses O(n) space
        """
        freq = {}
        threshold = len(nums) // 3
        result = []
        
        for num in nums:
            freq[num] = freq.get(num, 0) + 1
        
        for num, count in freq.items():
            if count > threshold:
                result.append(num)
        
        return result
    
    def majorityElement_boyer_moore(self, nums):
        """
        APPROACH 2: Boyer-Moore Voting Algorithm (OPTIMAL!) ⭐⭐⭐
        
        Key Insight:
        - At most 2 elements can appear more than ⌊n/3⌋ times
        - Use two candidates and two counters
        
        Algorithm (2 Phases):
        
        Phase 1 - Find Candidates:
        - Maintain two candidates (cand1, cand2) and their counts
        - For each element:
          a. If matches cand1, increment count1
          b. If matches cand2, increment count2
          c. If count1 is 0, assign to cand1
          d. If count2 is 0, assign to cand2
          e. Otherwise, decrement both counts (voting out)
        
        Phase 2 - Verify Candidates:
        - The candidates are only POTENTIAL majority elements
        - Must verify they actually appear > n/3 times
        
        Why Verification Needed?
        Example: [1,2,3]
        After phase 1: cand1=3, cand2=2 (or similar)
        But none appear > 3/3 = 1 time
        So result should be [1,2,3] or depend on actual counts
        
        Time Complexity: O(n) - two passes through array
        Space Complexity: O(1) - only 4 variables used
        
        ⭐⭐⭐ MOST OPTIMAL: Meets follow-up requirement!
        This is the BEST solution for interviews!
        """
        # Phase 1: Find potential candidates
        cand1 = cand2 = None
        count1 = count2 = 0
        
        for num in nums:
            # Check if num matches existing candidates
            if num == cand1:
                count1 += 1
            elif num == cand2:
                count2 += 1
            # Assign to empty slot
            elif count1 == 0:
                cand1 = num
                count1 = 1
            elif count2 == 0:
                cand2 = num
                count2 = 1
            # Vote out both candidates
            else:
                count1 -= 1
                count2 -= 1
        
        # Phase 2: Verify candidates
        count1 = count2 = 0
        for num in nums:
            if num == cand1:
                count1 += 1
            elif num == cand2:
                count2 += 1
        
        result = []
        threshold = len(nums) // 3
        
        if count1 > threshold:
            result.append(cand1)
        if count2 > threshold:
            result.append(cand2)
        
        return result
    
    def majorityElement_modified_boyer_moore(self, nums):
        """
        APPROACH 3: Modified Boyer-Moore with Pruning
        
        This is the third solution.
        
        Key Idea:
        - Maintain a counter dictionary
        - When dict size > 2, prune elements with count = 1
        - This keeps only strong candidates
        
        Issues:
        1. Uses nums.count(n) which scans entire array (O(n) per candidate)
        2. More complex logic
        3. Not actually O(1) space due to defaultdict
        4. Slower due to multiple passes
        
        Time Complexity: O(n × k) where k = candidates
        - Building count: O(n)
        - Pruning: O(n) worst case
        - Final verification: O(n) per candidate with nums.count()
        
        Space Complexity: O(n) worst case for count dictionary
        
        ⭐ Rating: Clever but NOT better than Boyer-Moore
        The nums.count() calls make it slower!
        """
        count = defaultdict(int)
        
        for n in nums:
            count[n] += 1
            
            # Prune when we have more than 2 candidates
            if len(count) <= 2:
                continue
            
            new_count = defaultdict(int)
            for num, c in count.items():
                if c > 1:
                    new_count[num] = c - 1
            count = new_count
        
        # Verify candidates (SLOW due to nums.count())
        res = []
        for n in count:
            if nums.count(n) > len(nums) // 3:  # ❌ O(n) operation!
                res.append(n)
        
        return res
    