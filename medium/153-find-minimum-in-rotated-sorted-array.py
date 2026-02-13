"""
153. Find Minimum in Rotated Sorted Array
Medium

Suppose an array of length n sorted in ascending order is rotated between 1 and n times. 
For example, the array nums = [0,1,2,4,5,6,7] might become:
- [4,5,6,7,0,1,2] if it was rotated 4 times.
- [0,1,2,4,5,6,7] if it was rotated 7 times.

Notice that rotating an array [a[0], a[1], a[2], ..., a[n-1]] 1 time results in 
the array [a[n-1], a[0], a[1], a[2], ..., a[n-2]].

Given the sorted rotated array nums of unique elements, return the minimum element 
of this array.

You must write an algorithm that runs in O(log n) time.

Example 1:
Input: nums = [3,4,5,1,2]
Output: 1
Explanation: The original array was [1,2,3,4,5] rotated 3 times.

Example 2:
Input: nums = [4,5,6,7,0,1,2]
Output: 0
Explanation: The original array was [0,1,2,4,5,6,7] and it was rotated 4 times.

Example 3:
Input: nums = [11,13,15,17]
Output: 11
Explanation: The original array was [11,13,15,17] and it was rotated 4 times (fully rotated).

Constraints:
- n == nums.length
- 1 <= n <= 5000
- -5000 <= nums[i] <= 5000
- All the integers of nums are unique
- nums is sorted and rotated between 1 and n times
"""


class Solution(object):
    def findMin_original(self, nums):
        """
        ORIGINAL SOLUTION (Your Approach)
        
        Approach: Binary search to find rotation point
        
        Key Insight:
        - Minimum element is at the rotation point
        - If array is sorted (nums[low] < nums[high]): return nums[low]
        - If left half sorted (nums[low] <= nums[mid]): min is in right half
        - Otherwise: min is in left half (including mid)
        
        Algorithm:
        1. If array already sorted: return nums[low]
        2. If left sorted: search right (low = mid + 1)
        3. Otherwise: search left (high = mid)
        4. Return nums[low] when low == high
        
        Example: nums = [4,5,6,7,0,1,2]
        
        Step 1: low=0, high=6, mid=3
          nums[0]=4 < nums[6]=2? No (not sorted)
          nums[0]=4 <= nums[3]=7? Yes (left sorted)
          Min in right: low = 4
        
        Step 2: low=4, high=6, mid=5
          nums[4]=0 < nums[6]=2? Yes (sorted!)
          Return nums[4] = 0
        
        Time Complexity: O(log n)
        Space Complexity: O(1)
        
        Works correctly!
        """
        low, high = 0, len(nums) - 1 
        
        while low < high:
            mid = (high + low) // 2
            
            # Array is sorted, minimum is at low
            if nums[low] < nums[high]:
                return nums[low]
            
            # Left half is sorted, minimum is in right half
            elif nums[low] <= nums[mid]:
                low = mid + 1
            
            # Right half is sorted, minimum is in left half (including mid)
            else:
                high = mid
        
        return nums[low]
    
    def findMin_optimized(self, nums):
        """
        OPTIMIZED SOLUTION: Cleaner Binary Search
        
        Improvement:
        - Remove the sorted array check inside loop
        - Simpler logic: only compare nums[mid] with nums[high]
        - More straightforward and efficient
        
        Key Insight:
        - Compare mid with right boundary (not left)
        - If nums[mid] > nums[high]: min is in right half (low = mid + 1)
        - If nums[mid] < nums[high]: min is in left half including mid (high = mid)
        
        Why This is Better:
        - No need to check if array is sorted each iteration
        - Single comparison instead of two
        - Cleaner code structure
        
        Example: nums = [4,5,6,7,0,1,2]
        
        Step 1: low=0, high=6, mid=3
          nums[3]=7 > nums[6]=2? Yes
          Min in right: low = 4
        
        Step 2: low=4, high=6, mid=5
          nums[5]=1 > nums[6]=2? No
          Min in left: high = 5
        
        Step 3: low=4, high=5, mid=4
          nums[4]=0 > nums[5]=1? No
          Min in left: high = 4
        
        Step 4: low=4, high=4
          Exit loop
          Return nums[4] = 0
        
        Time Complexity: O(log n)
        Space Complexity: O(1)
        
        More efficient and elegant!
        """
        low, high = 0, len(nums) - 1
        
        while low < high:
            mid = (low + high) // 2
            
            # Mid is in the larger half (rotation point is to the right)
            if nums[mid] > nums[high]:
                low = mid + 1
            
            # Mid is in the smaller half or at minimum (rotation point is to the left or at mid)
            else:
                high = mid
        
        return nums[low]
    
    # Main function uses optimized solution
    def findMin(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        return self.findMin_optimized(nums)