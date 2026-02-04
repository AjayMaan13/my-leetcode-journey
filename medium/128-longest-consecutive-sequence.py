"""
128. Longest Consecutive Sequence
Medium

Given an unsorted array of integers nums, return the length of the longest 
consecutive elements sequence.

You must write an algorithm that runs in O(n) time.

Example 1:
Input: nums = [100,4,200,1,3,2]
Output: 4
Explanation: The longest consecutive elements sequence is [1, 2, 3, 4]. 
Therefore its length is 4.

Example 2:
Input: nums = [0,3,7,2,5,8,4,6,0,1]
Output: 9

Example 3:
Input: nums = [1,0,1,2]
Output: 3

Constraints:
- 0 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9
"""


class Solution(object):
    def longestConsecutive(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        
        Approach: HashSet for O(1) lookups
        
        Key Insight:
        - Only start counting from the BEGINNING of a sequence
        - A number is the start of a sequence if (num - 1) is NOT in the set
        - This ensures we count each sequence only once
        
        Algorithm:
        1. Convert array to set for O(1) lookup
        2. For each number, check if it's the start of a sequence
        3. If yes, count consecutive numbers from this start
        4. Track the maximum length found
        
        Example walkthrough: [100, 4, 200, 1, 3, 2]
        Set: {100, 4, 200, 1, 3, 2}
        
        Check 100: (99 not in set) → START ✓
            Count: 100 → length 1
        
        Check 4: (3 in set) → NOT START ✗ (skip)
        
        Check 200: (199 not in set) → START ✓
            Count: 200 → length 1
        
        Check 1: (0 not in set) → START ✓
            Count: 1 → 2 → 3 → 4 → length 4 ✓
        
        Check 3: (2 in set) → NOT START ✗ (skip)
        
        Check 2: (1 in set) → NOT START ✗ (skip)
        
        Result: max_length = 4
        
        Time Complexity: O(n)
        - Converting to set: O(n)
        - Iterating through nums: O(n)
        - Inner while loop: Each number visited at most twice
          (once as potential start, once when counting from actual start)
        - Total: O(n) + O(n) = O(n)
        
        Space Complexity: O(n) - for the set
        """
        if not nums:
            return 0
        
        num_set = set(nums)
        max_length = 0
        
        for num in num_set:
            # Only start counting if this is the beginning of a sequence
            if num - 1 not in num_set:
                current_num = num
                current_length = 1
                
                # Count consecutive numbers
                while current_num + 1 in num_set:
                    current_num += 1
                    current_length += 1
                
                max_length = max(max_length, current_length)
        
        return max_length


class SolutionAlternative(object):
    def longestConsecutive(self, nums):
        """
        Alternative approach: Using visited tracking
        
        This is similar but explicitly marks visited numbers to avoid recounting.
        Still O(n) time and space.
        """
        if not nums:
            return 0
        
        num_set = set(nums)
        visited = set()
        max_length = 0
        
        for num in nums:
            if num in visited:
                continue
            
            # Mark as visited
            visited.add(num)
            
            # Expand in both directions
            left = num - 1
            right = num + 1
            
            while left in num_set:
                visited.add(left)
                left -= 1
            
            while right in num_set:
                visited.add(right)
                right += 1
            
            # Calculate length
            current_length = right - left - 1
            max_length = max(max_length, current_length)
        
        return max_length

