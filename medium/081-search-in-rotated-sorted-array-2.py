"""
81. Search in Rotated Sorted Array II
Medium

There is an integer array nums sorted in non-decreasing order (not necessarily 
with distinct values).

Before being passed to your function, nums is rotated at an unknown pivot index k 
(0 <= k < nums.length) such that the resulting array is 
[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed). 

For example, [0,1,2,4,4,4,5,6,6,7] might be rotated at pivot index 5 and become 
[4,5,6,6,7,0,1,2,4,4].

Given the array nums after the rotation and an integer target, return true if 
target is in nums, or false if it is not in nums.

You must decrease the overall operation steps as much as possible.

Example 1:
Input: nums = [2,5,6,0,0,1,2], target = 0
Output: true

Example 2:
Input: nums = [2,5,6,0,0,1,2], target = 3
Output: false

Constraints:
- 1 <= nums.length <= 5000
- -10^4 <= nums[i] <= 10^4
- nums is guaranteed to be rotated at some pivot
- -10^4 <= target <= 10^4

Follow up: This problem is similar to Search in Rotated Sorted Array, but nums may 
contain duplicates. Would this affect the runtime complexity? How and why?
"""


class Solution(object):
    def search_original(self, nums, target):
        """
        ORIGINAL SOLUTION (My Approach)
        
        Approach: Modified binary search with duplicate handling
        
        Key Difference from Problem 33:
        - Duplicates can make it ambiguous which half is sorted
        - When nums[low] == nums[mid] == nums[high], we can't determine rotation
        - Solution: Shrink search space by incrementing low and decrementing high
        
        Algorithm:
        1. If nums[mid] == target: return True
        2. If nums[low] == nums[mid] == nums[high]: shrink both ends
        3. If left sorted and target in range: search left
        4. If right sorted and target in range: search right
        
        Example: nums = [2,5,6,0,0,1,2], target = 0
        
        The duplicate 2's at both ends make it hard to determine which half is sorted
        
        Time Complexity: O(log n) average, O(n) worst case
        - Worst case: [1,1,1,1,1,1,1] target = 2
        - Must shrink one by one
        
        Space Complexity: O(1)
        """
        low, high = 0, len(nums) - 1
        
        while low <= high:
            mid = (high + low) // 2
            
            if target == nums[mid]:
                return True
            
            # Cannot determine which side is sorted due to duplicates
            # Shrink search space from both ends
            if nums[low] == nums[mid] == nums[high]:
                low += 1
                high -= 1
            
            # Left half is sorted
            elif nums[low] <= nums[mid]:
                if nums[low] <= target < nums[mid]:
                    high = mid - 1 
                else:
                    low = mid + 1
            
            # Right half is sorted
            else:
                if nums[mid] < target <= nums[high]:
                    low = mid + 1 
                else:
                    high = mid - 1
        
        return False
    
    def search_optimized(self, nums, target):
        """
        OPTIMIZED SOLUTION: More Efficient Duplicate Handling
        
        Improvement:
        - Instead of shrinking both ends when nums[low] == nums[mid] == nums[high],
        - Only shrink low when nums[low] == nums[mid] (more targeted)
        - This handles duplicates more efficiently in most cases
        
        Key Insight:
        - When nums[low] == nums[mid], we can't determine if left is sorted
        - But we can safely skip nums[low] (duplicate of mid)
        - This is more efficient than shrinking both ends
        
        Example: nums = [1,0,1,1,1], target = 0
        
        Your approach:
        Step 1: nums[0]=1, nums[2]=1, nums[4]=1 → shrink both: low=1, high=3
        Step 2: nums[1]=0, nums[2]=1, nums[3]=1 → left sorted, search
        
        Optimized:
        Step 1: nums[0]=1 == nums[2]=1 → increment low: low=1
        Step 2: nums[1]=0 != nums[2]=1 → determine sorted half
        
        Time Complexity: O(log n) average, O(n) worst case
        - Same worst case but better average performance
        
        Space Complexity: O(1)
        """
        low, high = 0, len(nums) - 1
        
        while low <= high:
            mid = (low + high) // 2
            
            # Found target
            if nums[mid] == target:
                return True
            
            # Cannot determine which side is sorted
            # Skip duplicate at low position
            if nums[low] == nums[mid]:
                low += 1
                continue
            
            # Left half is sorted (nums[low] < nums[mid])
            if nums[low] < nums[mid]:
                # Target is in sorted left half
                if nums[low] <= target < nums[mid]:
                    high = mid - 1
                else:
                    low = mid + 1
            
            # Right half is sorted (nums[mid] < nums[high])
            else:
                # Target is in sorted right half
                if nums[mid] < target <= nums[high]:
                    low = mid + 1
                else:
                    high = mid - 1
        
        return False
    
    # Main function uses optimized solution
    def search(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: bool
        """
        return self.search_optimized(nums, target)