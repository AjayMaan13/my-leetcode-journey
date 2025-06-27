"""
26. Remove Duplicates from Sorted Array
https://leetcode.com/problems/remove-duplicates-from-sorted-array/

Difficulty: Easy
Topics: Array, Two Pointers
Date Solved: 2024-06-14

Problem:
Given an integer array nums sorted in non-decreasing order, remove the duplicates 
in-place such that each unique element appears only once. The relative order of 
the elements should be kept the same. Then return the number of unique elements in nums.

Consider the number of unique elements of nums to be k, to get accepted, you need 
to do the following things:
- Change the array nums such that the first k elements of nums contain the unique 
  elements in the order they were present in nums initially.
- The remaining elements of nums are not important as well as the size of nums.
- Return k.

Example 1:
Input: nums = [1,1,2]
Output: 2, nums = [1,2,_]
Explanation: Your function should return k = 2, with the first two elements of nums 
being 1 and 2 respectively. It does not matter what you leave beyond the returned k.

Example 2:
Input: nums = [0,0,1,1,1,2,2,3,3,4]
Output: 5, nums = [0,1,2,3,4,_,_,_,_,_]
Explanation: Your function should return k = 5, with the first five elements of nums 
being 0, 1, 2, 3, and 4 respectively.

Constraints:
- 1 <= nums.length <= 3 * 10^4
- -100 <= nums[i] <= 100
- nums is sorted in non-decreasing order
"""

# My Original Solution - Working but can be optimized
class MySolution(object):
    def removeDuplicates(self, nums):
        """
        My Approach: Two Pointers with explicit tracking
        - Use left pointer to track position for next unique element
        - Use right pointer to scan through array
        - Only place element when it's different from previous
        
        Time: O(n) where n is length of array
        Space: O(1) constant space
        """
        length = len(nums)
        if length < 2:
            return length
        
        left = 1  # Position for next unique element
        right = 1  # Scanning pointer
        
        while right < length:
            if nums[left - 1] != nums[right]:
                nums[left] = nums[right]
                left += 1
            right += 1
        
        return left

# Optimized Solution - Better memory efficiency and cleaner code
class OptimizedSolution(object):
    def removeDuplicates(self, nums):
        """
        Optimized Two Pointers: Cleaner implementation
        - Use left pointer to track position for unique elements
        - Use right pointer to scan through array
        - More standard two-pointer pattern with descriptive names
        
        Time: O(n)
        Space: O(1) - better memory efficiency
        """
        # Problem Statement
        """
        Removes duplicates from a sorted array in-place.
        :type nums: List[int]
        :rtype: int
        """
        if not nums:
            return 0

        write_index = 1

        for read_index in range(1, len(nums)):
            if nums[read_index] != nums[write_index - 1]:
                nums[write_index] = nums[read_index]
                write_index += 1

        return write_index


# Test cases
if __name__ == "__main__":
    # Initialize solutions
    my_sol = MySolution()
    opt_sol = OptimizedSolution()
    
    print("=== Remove Duplicates from Sorted Array - Solution Comparison ===\n")
    
    # Test case 1: Example 1
    print("Test 1: [1,1,2]")
    nums1_my = [1, 1, 2]
    nums1_opt = [1, 1, 2]
    
    k1_my = my_sol.removeDuplicates(nums1_my)
    k1_opt = opt_sol.removeDuplicates(nums1_opt)
    
    print(f"My Solution:       k = {k1_my}, nums = {nums1_my[:k1_my]} (first k elements)")
    print(f"Optimized:         k = {k1_opt}, nums = {nums1_opt[:k1_opt]} (first k elements)")
    print(f"Expected:          k = 2, nums = [1, 2]")
    print()
    
    # Test case 2: Example 2
    print("Test 2: [0,0,1,1,1,2,2,3,3,4]")
    nums2_my = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    nums2_opt = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    
    k2_my = my_sol.removeDuplicates(nums2_my)
    k2_opt = opt_sol.removeDuplicates(nums2_opt)
    
    print(f"My Solution:       k = {k2_my}, nums = {nums2_my[:k2_my]}")
    print(f"Optimized:         k = {k2_opt}, nums = {nums2_opt[:k2_opt]}")
    print(f"Expected:          k = 5, nums = [0, 1, 2, 3, 4]")
    print()
    
    # Test case 3: Single element
    print("Test 3: [1] (single element)")
    nums3_my = [1]
    nums3_opt = [1]
    
    k3_my = my_sol.removeDuplicates(nums3_my)
    k3_opt = opt_sol.removeDuplicates(nums3_opt)
    
    print(f"My Solution:       k = {k3_my}, nums = {nums3_my[:k3_my]}")
    print(f"Optimized:         k = {k3_opt}, nums = {nums3_opt[:k3_opt]}")
    print(f"Expected:          k = 1, nums = [1]")
    print()
    
    # Test case 4: All same elements
    print("Test 4: [2,2,2,2] (all duplicates)")
    nums4_my = [2, 2, 2, 2]
    nums4_opt = [2, 2, 2, 2]
    
    k4_my = my_sol.removeDuplicates(nums4_my)
    k4_opt = opt_sol.removeDuplicates(nums4_opt)
    
    print(f"My Solution:       k = {k4_my}, nums = {nums4_my[:k4_my]}")
    print(f"Optimized:         k = {k4_opt}, nums = {nums4_opt[:k4_opt]}")
    print(f"Expected:          k = 1, nums = [2]")
    print()
    
    # Test case 5: No duplicates
    print("Test 5: [1,2,3,4,5] (no duplicates)")
    nums5_my = [1, 2, 3, 4, 5]
    nums5_opt = [1, 2, 3, 4, 5]
    
    k5_my = my_sol.removeDuplicates(nums5_my)
    k5_opt = opt_sol.removeDuplicates(nums5_opt)
    
    print(f"My Solution:       k = {k5_my}, nums = {nums5_my[:k5_my]}")
    print(f"Optimized:         k = {k5_opt}, nums = {nums5_opt[:k5_opt]}")
    print(f"Expected:          k = 5, nums = [1, 2, 3, 4, 5]")

"""
Performance Analysis:

My Original Solution:
✅ Correct two-pointer implementation
✅ Handles edge cases properly
✅ Clear variable naming (left, right)
❌ More variables than needed (length, left, right)
❌ Extra edge case check (length < 2)
❌ While loop structure is less standard

Optimized Solution:
✅ Standard two-pointer pattern with descriptive names
✅ Cleaner for-loop structure  
✅ Clear variable purposes (left=write, right=read)
✅ More concise edge case handling
✅ Better memory efficiency
✅ More readable and maintainable

Key Insights:
- Two pointers: left for writing position, right for reading
- Sorted array allows comparing adjacent elements
- In-place modification with O(1) extra space
- Only need to care about first k elements

What I Learned:
- Two-pointer technique for in-place array modification
- Leveraging sorted property for duplicate detection
- Standard patterns for array compaction problems
- Importance of descriptive variable names

Patterns Used:
- Two Pointers (Read/Write positions)
- In-place Array Modification
- Sorted Array Properties

Recommendation: Use OptimizedSolution for better memory ranking and cleaner code!
"""