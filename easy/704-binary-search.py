"""
704. Binary Search
Easy

Given an array of integers nums which is sorted in ascending order, and an 
integer target, write a function to search target in nums. If target exists, 
then return its index. Otherwise, return -1.

You must write an algorithm with O(log n) runtime complexity.

Example 1:
Input: nums = [-1,0,3,5,9,12], target = 9
Output: 4
Explanation: 9 exists in nums and its index is 4

Example 2:
Input: nums = [-1,0,3,5,9,12], target = 2
Output: -1
Explanation: 2 does not exist in nums so return -1

Constraints:
- 1 <= nums.length <= 10^4
- -10^4 < nums[i], target < 10^4
- All the integers in nums are unique
- nums is sorted in ascending order
"""


class Solution(object):
    def search_original(self, nums, target):
        """
        ORIGINAL SOLUTION (Your Approach)
        
        Runtime: 100%
        Memory: 5%
        
        Approach: Standard binary search
        
        Issues:
        1. Unnecessary check: if len(nums) < 1 (constraints guarantee >= 1)
        2. Returns None instead of -1 for empty array
        3. Calculates index before loop (redundant)
        4. Uses high != low which is less clear than high >= low
        5. Checks index > -1 (unnecessary if logic is correct)
        
        Logic Flow:
        - Initialize low, high, and index
        - While high != low:
          * If found, set high = low to exit
          * If target larger, move low up
          * If target smaller, move high down
          * Recalculate index
        - Final check if nums[index] == target
        
        Time Complexity: O(log n)
        Space Complexity: O(1)
        
        Works correctly but has unnecessary code!
        """
        if len(nums) < 1:
            return None  # Should return -1
        
        high = len(nums) - 1
        low = 0
        index = (high + low) // 2  # Calculated here but also in loop
        
        while high != low and index > -1:
            if nums[index] == target:
                high = low  # Clever way to exit loop
            else:
                if nums[index] < target:
                    low = index + 1
                else:
                    high = index - 1
                index = (high + low) // 2
        
        # Final check needed because loop exits when high == low
        return index if nums[index] == target else -1
    
    def search_optimal(self, nums, target):
        """
        OPTIMAL SOLUTION (From Screenshot - Clean Standard Binary Search)
        
        Improvements:
        1. No unnecessary checks
        2. Clear loop condition: while l <= r
        3. Calculates mid inside loop only
        4. Returns immediately when found
        5. Returns -1 at end (cleaner flow)
        
        Algorithm:
        1. Initialize left (l) and right (r) pointers
        2. While left <= right:
           a. Calculate middle index
           b. If nums[m] == target: return m (found!)
           c. If nums[m] < target: search right half (l = m + 1)
           d. If nums[m] > target: search left half (r = m - 1)
        3. If loop exits, target not found: return -1
        
        Why This is Better:
        - More intuitive loop condition (l <= r)
        - Early return on match (no extra check needed)
        - Cleaner code structure
        - Standard implementation pattern
        
        Example Trace: nums = [-1,0,3,5,9,12], target = 9
        
        Initial: l=0, r=5
        
        Iteration 1:
          m = 0 + (5-0)//2 = 0 + 2 = 2
          nums[2] = 3
          3 < 9 → search right half
          l = 2 + 1 = 3
        
        Iteration 2:
          m = 3 + (5-3)//2 = 3 + 1 = 4
          nums[4] = 9
          9 == 9 → Found!
          return 4
        
        Time Complexity: O(log n)
        - Each iteration halves search space
        - Binary search standard complexity
        
        Space Complexity: O(1)
        - Only uses three variables (l, r, m)
        
        This is the STANDARD binary search implementation!
        Clean, efficient, and widely recognized pattern.
        """
        l, r = 0, len(nums) - 1
        
        while l <= r:
            # Calculate middle index
            # Using l + (r-l)//2 prevents overflow in other languages
            # In Python, // operator is safe
            m = l + ((r - l) // 2)
            
            if nums[m] > target:
                # Target is in left half
                r = m - 1
            elif nums[m] < target:
                # Target is in right half
                l = m + 1
            else:
                # Found target!
                return m
        
        # Target not found
        return -1
    
    # Main function uses optimal solution
    def search(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        return self.search_optimal(nums, target)
