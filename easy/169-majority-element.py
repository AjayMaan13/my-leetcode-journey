"""
169. Majority Element

Given an array nums of size n, return the majority element.
The majority element is the element that appears more than ⌊n / 2⌋ times. 
You may assume that the majority element always exists in the array.

Example 1:
Input: nums = [3,2,3]
Output: 3

Example 2:
Input: nums = [2,2,1,1,1,2,2]
Output: 2

Constraints:
- n == nums.length
- 1 <= n <= 5 * 10^4
- Majority element always exists
"""

# ============================================================================
# MY SOLUTION - HashMap/Dictionary Counting
# Time: O(n), Space: O(n)
# ============================================================================

class Solution(object):
    def majorityElement(self, nums):
        """
        Count frequency of each element using hashmap
        Return when count exceeds n/2
        """
        if len(nums) < 1:
            return None
        if len(nums) == 1:
            return nums[0]
        
        hashMap = {}
        length = len(nums) / 2  # Majority threshold
        
        for num in nums:
            if num in hashMap:
                hashMap[num] += 1 
                if hashMap[num] > length:
                    return num
            else:
                hashMap[num] = 1


# ============================================================================
# ALTERNATIVE HASHMAP - Cleaner One-Liner Update
# Time: O(n), Space: O(n)
# ============================================================================

class SolutionHashMapCleaner:
    def majorityElement(self, nums: List[int]) -> int:
        """
        HashMap with dict.get() for cleaner code
        Track both result and maxCount simultaneously
        """
        count = {}
        res, maxCount = 0, 0
        
        for n in nums:
            count[n] = 1 + count.get(n, 0)  # Cleaner than if-else
            res = n if count[n] > maxCount else res
            maxCount = max(count[n], maxCount)
        
        return res


# ============================================================================
# SOLUTION 2 - Sorting Approach ❌
# Time: O(n log n), Space: O(1) or O(n) depending on sort implementation
# ============================================================================

class Solution2:
    def majorityElement(self, nums):
        """
        Sort the array and return middle element
        
        Why it works:
        Since majority element appears > n/2 times, after sorting,
        the middle element MUST be the majority element.
        
        Example: [2,2,1,1,1,2,2] → sorted: [1,1,1,2,2,2,2]
        Middle index (n//2) = 3, nums[3] = 2 (majority element)
        """
        nums.sort()
        return nums[len(nums) // 2]


# ============================================================================
# SOLUTION 3 - Moore's Voting Algorithm (OPTIMAL)
# Time: O(n), Space: O(1)
# ============================================================================

class Solution3:
    def majorityElement(self, nums):
        """
        Boyer-Moore Majority Voting Algorithm
        
        Concept: 
        - Treat array like a voting system
        - Maintain a candidate and count
        - When count reaches 0, switch candidate
        - The majority element will always survive
        
        Why it works:
        If we cancel out each occurrence of majority element with 
        a different element, majority will still have elements left
        (since it appears > n/2 times)
        
        Algorithm:
        1. Initialize candidate and count
        2. For each element:
           - If count is 0, set current element as candidate
           - If element matches candidate, increment count
           - Otherwise, decrement count
        3. Return candidate (guaranteed to be majority)
        """
        candidate = None
        count = 0
        
        for num in nums:
            if count == 0:
                candidate = num  # New candidate
                count = 1
            elif num == candidate:
                count += 1       # Vote for candidate
            else:
                count -= 1       # Vote against candidate
        
        return candidate


# ============================================================================
# SOLUTION 4 - Moore's Voting (Compact/Shortened Version)
# Time: O(n), Space: O(1)
# ============================================================================

class Solution4:
    def majorityElement(self, nums: List[int]) -> int:
        """
        Most compact version of Boyer-Moore algorithm
        Uses inline if-else for count update
        """
        res, count = 0, 0
        
        for n in nums:
            if count == 0:
                res = n
            count += (1 if n == res else -1)
        
        return res


# ============================================================================
# VISUAL EXAMPLE: Moore's Voting Algorithm
# ============================================================================

"""
Example: nums = [2, 2, 1, 1, 1, 2, 2]

Step-by-step:
Index | Element | Candidate | Count | Action
------|---------|-----------|-------|---------------------------
  0   |    2    |     2     |   1   | count=0, set candidate=2
  1   |    2    |     2     |   2   | matches candidate, count++
  2   |    1    |     2     |   1   | doesn't match, count--
  3   |    1    |     2     |   0   | doesn't match, count--
  4   |    1    |     1     |   1   | count=0, set candidate=1
  5   |    2    |     1     |   0   | doesn't match, count--
  6   |    2    |     2     |   1   | count=0, set candidate=2

Final candidate = 2 (correct!)

Intuition:
Think of it as a battle where majority element fights all others.
Since majority > n/2, it will always win even if all others team up.
"""


# ============================================================================
# SOLUTION 5 - Using Python Counter (Cleaner HashMap)
# Time: O(n), Space: O(n)
# ============================================================================

from collections import Counter

class Solution5:
    def majorityElement(self, nums):
        """
        Use Python's Counter for cleaner code
        Returns the most common element
        """
        counts = Counter(nums)
        return counts.most_common(1)[0][0]


# ============================================================================
# COMPLEXITY COMPARISON
# ============================================================================

"""
Approach                    Time            Space       Notes
--------                    ----            -----       -----
HashMap Counting            O(n)            O(n)        Early exit optimization
HashMap (Cleaner)           O(n)            O(n)        Tracks max simultaneously
Sorting                     O(n log n)      O(1)-O(n)   Simple but slower
Moore's Voting (Standard)   O(n)            O(1)        Most common solution
Moore's Voting (Compact)    O(n)            O(1)        Shortest code
Python Counter              O(n)            O(n)        Most readable

For interviews: Moore's Voting Algorithm is the expected optimal solution
"""


# ============================================================================
# DETAILED EXPLANATION: Why Moore's Algorithm Works
# ============================================================================

"""
Mathematical Proof:

Let majority element appear 'm' times, others appear 'o' times.
Given: m > n/2, which means m > o (since m + o = n)

In Moore's algorithm:
- Each occurrence of majority element increases count
- Each occurrence of other elements decreases count
- Even in worst case where all others cancel majority:
  Final count = m - o > 0 (since m > o)

Therefore, majority element will always be the final candidate.

Example with extreme case:
[1, 1, 1, 1, 2, 2, 3]  (1 appears 4 times out of 7)

Cancellations:
1 vs 2 → cancel (2 times)
1 vs 3 → cancel (1 time)
Result: 1 remaining (1 time) ✓

No matter how we arrange, majority will survive!
"""


# ============================================================================
# TEST CASES
# ============================================================================

def test_majority_element():
    # Test all solutions
    solutions = [
        Solution(), 
        SolutionHashMapCleaner(), 
        Solution2(), 
        Solution3(), 
        Solution4(),
        Solution5()
    ]
    
    test_cases = [
        ([3, 2, 3], 3),
        ([2, 2, 1, 1, 1, 2, 2], 2),
        ([1], 1),
        ([1, 1, 1, 2, 2], 1),
        ([6, 5, 5], 5)
    ]
    
    for i, solution in enumerate(solutions, 1):
        print(f"\n--- Testing Solution {i} ---")
        for nums, expected in test_cases:
            result = solution.majorityElement(nums[:])  # Pass copy
            status = "✓" if result == expected else "✗"
            print(f"{status} Input: {nums} → Output: {result} (Expected: {expected})")


if __name__ == "__main__":
    test_majority_element()


# ============================================================================
# INTERVIEW TIPS
# ============================================================================

"""
1. Start with HashMap approach (easiest to explain)
2. Mention sorting approach as alternative
3. Discuss Moore's Voting as optimal solution
4. Be ready to prove why Moore's algorithm works

Follow-up questions to prepare for:
- What if majority element doesn't always exist? 
  → Need second pass to verify candidate
- What if we want element appearing > n/3 times?
  → Need modified algorithm with 2 candidates
- Can we do it without modifying array?
  → Yes, Moore's algorithm doesn't modify
"""