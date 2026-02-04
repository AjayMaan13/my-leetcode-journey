"""
31. Next Permutation
Medium

A permutation of an array of integers is an arrangement of its members into a 
sequence or linear order.

The next permutation of an array of integers is the next lexicographically greater 
permutation of its integer. More formally, if all the permutations of the array are 
sorted in one container according to their lexicographical order, then the next 
permutation of that array is the permutation that follows it in the sorted container. 
If such arrangement is not possible, the array must be rearranged as the lowest 
possible order (i.e., sorted in ascending order).

Example 1:
Input: nums = [1,2,3]
Output: [1,3,2]

Example 2:
Input: nums = [3,2,1]
Output: [1,2,3]

Example 3:
Input: nums = [1,1,5]
Output: [1,5,1]

Constraints:
- 1 <= nums.length <= 100
- 0 <= nums[i] <= 100
"""


class Solution(object):
    def nextPermutation(self, nums):
        """
        :type nums: List[int]
        :rtype: None Do not return anything, modify nums in-place instead.
        
        Algorithm:
        1. Find pivot: From right to left, find first position where nums[i] < nums[i+1]
           - This is the rightmost position where we can increase the value
           - Everything after this position is in descending order
        
        2. Find successor: From right to left, find smallest element > nums[pivot]
           - This gives us the next larger value to place at pivot position
        
        3. Swap pivot with successor
        
        4. Reverse suffix: Reverse everything after pivot position
           - The suffix is in descending order, reversing makes it ascending
           - This gives us the smallest possible arrangement of remaining elements
        
        Edge case: If no pivot found (array is descending), reverse entire array
        
        Time Complexity: O(n) - at most three passes through array
        Space Complexity: O(1) - in-place modifications only
        
        Example walkthrough: [1, 3, 5, 4, 2]
        Step 1: Find pivot
                [1, 3, 5, 4, 2]
                    ↑ (i=1, value=3, because 3 < 5)
        
        Step 2: Find successor
                [1, 3, 5, 4, 2]
                       ↑ (j=3, value=4, smallest element > 3 from right)
        
        Step 3: Swap
                [1, 4, 5, 3, 2]
                    ↑     ↑
        
        Step 4: Reverse suffix after i
                [1, 4, | 5, 3, 2] → [1, 4, | 2, 3, 5]
                       ↑________↑       ↑________↑
        
        Result: [1, 4, 2, 3, 5] ✓
        """
        n = len(nums)
        
        # Step 1: Find pivot (rightmost i where nums[i] < nums[i+1])
        i = n - 2
        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1
        
        # Step 2: If pivot exists, find successor and swap
        if i >= 0:
            # Find smallest element greater than nums[i] from the right
            j = n - 1
            while nums[j] <= nums[i]:
                j -= 1
            # Swap
            nums[i], nums[j] = nums[j], nums[i]
        
        # Step 3: Reverse suffix after pivot position
        # When i == -1 (no pivot), this reverses entire array
        # When i >= 0 (pivot found), this reverses suffix after pivot
        left, right = i + 1, n - 1
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1