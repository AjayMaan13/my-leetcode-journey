"""
33. Search in Rotated Sorted Array
Medium

There is an integer array nums sorted in ascending order (with distinct values).

Prior to being passed to your function, nums is possibly left rotated at an 
unknown index k (1 <= k < nums.length) such that the resulting array is 
[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed). 

For example, [0,1,2,4,5,6,7] might be left rotated by 3 indices and become [4,5,6,7,0,1,2].

Given the array nums after the possible rotation and an integer target, return 
the index of target if it is in nums, or -1 if it is not in nums.

You must write an algorithm with O(log n) runtime complexity.

Example 1:
Input: nums = [4,5,6,7,0,1,2], target = 0
Output: 4

Example 2:
Input: nums = [4,5,6,7,0,1,2], target = 3
Output: -1

Example 3:
Input: nums = [1], target = 0
Output: -1

Constraints:
- 1 <= nums.length <= 5000
- -10^4 <= nums[i] <= 10^4
- All values of nums are unique
- nums is an ascending array that is possibly rotated
- -10^4 <= target <= 10^4
"""


class Solution(object):
    def search_solution1_find_k(self, nums, target):
        """
        SOLUTION 1: Find Rotation Point, Then Binary Search
        
        Approach:
        1. Find rotation point k (where array was rotated)
        2. Perform binary search on "virtually unrotated" array using index mapping
        
        Key Insight:
        - Left part values > last element
        - Right part values ≤ last element
        - Find the boundary between these parts
        
        Index Mapping:
        - Original index i maps to (i + k) % n in rotated array
        - This "unrotates" the array virtually
        
        Time Complexity: O(log n) + O(log n) = O(log n)
        - Find k: O(log n)
        - Binary search: O(log n)
        
        Space Complexity: O(1)
        """
        if len(nums) < 1:
            return -1
        
        def findK(nums):
            """Find rotation point (index of smallest element)"""
            low, high = 0, len(nums) - 1
            
            # Array not rotated
            if nums[low] < nums[high]:
                return 0
            
            while low < high:
                mid = (high + low) // 2
                
                # In left part (larger values)
                if nums[mid] > nums[low]:
                    low = mid
                # In right part (smaller values)
                else:
                    high = mid
            
            return low + 1
        
        def newIndex(i, k, n):
            """Map index i to rotated array index"""
            return (i + k) % n
        
        # Find rotation point
        k = findK(nums)
        
        # Binary search with index mapping
        low, high = 0, len(nums) - 1
        while low <= high:
            mid = (high + low) // 2
            newMid = newIndex(mid, k, len(nums))
            
            if nums[newMid] == target:
                return newMid
            elif nums[newMid] > target:
                high = mid - 1 
            else:
                low = mid + 1
        
        return -1
    
    def search_solution2_one_pass(self, nums, target):
        """
        SOLUTION 2: Single Pass Binary Search (Optimal!)
        
        Approach:
        1. At each step, identify which half is sorted
        2. Check if target is in the sorted half
        3. Adjust search space accordingly
        
        Key Insight:
        - In rotated array, at least one half is always sorted
        - If nums[low] <= nums[mid]: left half is sorted
        - Else: right half is sorted
        
        Logic:
        - If left sorted and target in range [nums[low], nums[mid]): search left
        - If right sorted and target in range (nums[mid], nums[high]]: search right
        - Otherwise: search the other half
        
        Example: nums = [4,5,6,7,0,1,2], target = 0
        
        Step 1: low=0, high=6, mid=3
          nums = [4,5,6,7,0,1,2]
                  l     m     h
          nums[0]=4 <= nums[3]=7 → left sorted
          target=0 not in [4,7) → search right
          low = 4
        
        Step 2: low=4, high=6, mid=5
          nums = [4,5,6,7,0,1,2]
                        l m h
          nums[4]=0 > nums[5]=1 → right sorted
          target=0 in (0,2]? No, 0 not > 0 → search left
          high = 4
        
        Step 3: low=4, high=4, mid=4
          nums[4] = 0 == target
          return 4
        
        Time Complexity: O(log n)
        Space Complexity: O(1)
        
        This is MORE EFFICIENT than Solution 1!
        """
        if len(nums) < 1:
            return -1
        
        low, high = 0, len(nums) - 1 
        
        while low <= high:
            mid = (high + low) // 2
            
            # Found target
            if nums[mid] == target:
                return mid
            
            # Left half is sorted
            if nums[low] <= nums[mid]:
                # Target is in sorted left half
                if target >= nums[low] and target < nums[mid]:
                    high = mid - 1
                else:
                    low = mid + 1
            
            # Right half is sorted
            else: 
                # Target is in sorted right half
                if target <= nums[high] and target > nums[mid]:
                    low = mid + 1
                else: 
                    high = mid - 1
        
        return -1
    
    # Main function uses optimal one-pass solution
    def search(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        return self.search_solution2_one_pass(nums, target)