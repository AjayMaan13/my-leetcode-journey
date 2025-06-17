"""
27. Remove Element
https://leetcode.com/problems/remove-element/

Difficulty: Easy
Topics: Array, Two Pointers
Date Solved: 2024-06-14

Problem:
Given an integer array nums and an integer val, remove all occurrences of val 
in nums in-place. The order of the elements may be changed. Then return the 
number of elements in nums which are not equal to val.

Consider the number of elements in nums which are not equal to val be k, to get 
accepted, you need to do the following things:
- Change the array nums such that the first k elements of nums contain the 
  elements which are not equal to val.
- The remaining elements of nums are not important as well as the size of nums.
- Return k.

Example 1:
Input: nums = [3,2,2,3], val = 3
Output: 2, nums = [2,2,_,_]
Explanation: Your function should return k = 2, with the first two elements of nums being 2.
It does not matter what you leave beyond the returned k (hence they are underscores).

Example 2:
Input: nums = [0,1,2,2,3,0,4,2], val = 2
Output: 5, nums = [0,1,4,0,3,_,_,_]
Explanation: Your function should return k = 5, with the first five elements of nums 
containing 0, 0, 1, 3, and 4. Note that the five elements can be returned in any order.
It does not matter what you leave beyond the returned k (hence they are underscores).

Constraints:
- 0 <= nums.length <= 100
- 0 <= nums[i] <= 50
- 0 <= val <= 100
"""

class Solution:

    # Submission, Runtime: 100%, Memory: 80.57%
    def removeElement(self, nums, val):
        """
        Alternative approach: Count valid elements while overwriting
        """
        k = len(nums)  # Start with total count
        index = 0
        
        for num in nums:
            if num == val:
                k -= 1  # Decrement count for invalid element
            else:
                nums[index] = num  # Keep valid element
                index += 1
        
        return k
    
    # Alternative solution
    def removeElement(self, nums, val):
        """
        Approach: Two Pointers (Fast-Slow)
        - Use one pointer (index) to track position for valid elements
        - Use another pointer (implicit in for loop) to scan through array
        - When we find a valid element (not equal to val), place it at index position
        - Only increment index when we place a valid element
        
        Time: O(n) - single pass through array
        Space: O(1) - only using constant extra space
        """
        index = 0  # Slow pointer - tracks position for next valid element
        
        for num in nums:  # Fast pointer - scans through array
            if num != val:  # Found valid element
                nums[index] = num  # Place it at correct position
                index += 1  # Move to next position
        
        return index  # Number of valid elements



# Test cases
if __name__ == "__main__":
    solution = Solution()
    alternative = SolutionAlternative()
    
    # Test case 1
    nums1 = [3, 2, 2, 3]
    val1 = 3
    nums1_copy = nums1.copy()
    k1 = solution.removeElement(nums1, val1)
    k1_alt = alternative.removeElement(nums1_copy, val1)
    print(f"Test 1:")
    print(f"Input: nums = [3,2,2,3], val = 3")
    print(f"Output: k = {k1}, nums = {nums1[:k1]} (first k elements)")
    print(f"Alternative: k = {k1_alt}, nums = {nums1_copy[:k1_alt]}")
    print(f"Expected: k = 2, nums = [2,2]")
    print()
    
    # Test case 2
    nums2 = [0, 1, 2, 2, 3, 0, 4, 2]
    val2 = 2
    nums2_copy = nums2.copy()
    k2 = solution.removeElement(nums2, val2)
    k2_alt = alternative.removeElement(nums2_copy, val2)
    print(f"Test 2:")
    print(f"Input: nums = [0,1,2,2,3,0,4,2], val = 2")
    print(f"Output: k = {k2}, nums = {nums2[:k2]} (first k elements)")
    print(f"Alternative: k = {k2_alt}, nums = {nums2_copy[:k2_alt]}")
    print(f"Expected: k = 5, nums = [0,1,3,0,4] (any order)")
    print()
    
    # Test case 3 - Edge case: empty array
    nums3 = []
    val3 = 1
    k3 = solution.removeElement(nums3, val3)
    print(f"Test 3 (Edge case):")
    print(f"Input: nums = [], val = 1")
    print(f"Output: k = {k3}, nums = {nums3}")
    print(f"Expected: k = 0, nums = []")
    print()
    
    # Test case 4 - Edge case: all elements are val
    nums4 = [2, 2, 2, 2]
    val4 = 2
    k4 = solution.removeElement(nums4, val4)
    print(f"Test 4 (Edge case):")
    print(f"Input: nums = [2,2,2,2], val = 2")
    print(f"Output: k = {k4}, nums = {nums4[:k4] if k4 > 0 else []}")
    print(f"Expected: k = 0, nums = []")

"""
Key Insights:
- Two pointers technique: fast pointer scans, slow pointer places valid elements
- In-place modification: we overwrite the array as we go
- Order doesn't matter: we can rearrange elements freely
- Only first k elements matter: everything after index k is ignored
"""