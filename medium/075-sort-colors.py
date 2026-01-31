"""
75. Sort Colors (Dutch National Flag Problem)

Given an array nums with n objects colored red, white, or blue, sort them 
in-place so that objects of the same color are adjacent, with the colors 
in the order red, white, and blue.

Use integers 0, 1, and 2 to represent red, white, and blue respectively.
Must solve without using library's sort function.

Example 1:
Input: nums = [2,0,2,1,1,0]
Output: [0,0,1,1,2,2]

Example 2:
Input: nums = [2,0,1]
Output: [0,1,2]

Constraints:
- 1 <= n <= 300
- nums[i] is either 0, 1, or 2

Follow-up: One-pass algorithm using O(1) space?
"""

# ============================================================================
# MY SOLUTION - Counting Sort (Two Pass)
# Time: O(2n) = O(n), Space: O(1)
# ============================================================================

class Solution(object):
    def sortColors(self, nums):
        """
        Two-pass solution: Count frequencies, then overwrite array
        """
        if len(nums) < 1:
            return None
        
        # Pass 1: Count occurrences
        zeroCount = oneCount = twoCount = 0
        for num in nums:
            if num == 0:
                zeroCount += 1
            elif num == 1:
                oneCount += 1 
            else:
                twoCount += 1 
        
        # Pass 2: Overwrite array with sorted values
        for i in range(len(nums)):
            if zeroCount != 0:
                nums[i] = 0
                zeroCount -= 1 
            elif oneCount != 0:
                nums[i] = 1
                oneCount -= 1
            else:
                nums[i] = 2
        
        return None


# ============================================================================
# OPTIMAL SOLUTION - Bucket Sort / Dutch National Flag Algorithm (One Pass)
# Time: O(n), Space: O(1)
# ============================================================================

class Solution:
    def sortColors(self, nums):
        """
        One-pass three-pointer solution with helper swap function
        
        Concept: Maintain three regions
        - [0...low-1]: all 0s
        - [low...mid-1]: all 1s
        - [mid...high]: unsorted (to be processed)
        - [high+1...n-1]: all 2s
        
        Algorithm:
        - If nums[mid] == 0: swap with low, increment both low and mid
        - If nums[mid] == 1: just increment mid (already in correct region)
        - If nums[mid] == 2: swap with high, decrement high (don't increment mid, 
          need to process swapped element)
        """
        
        def swap(i, j):
            """Helper function to swap elements at indices i and j"""
            tmp = nums[i]
            nums[i] = nums[j]
            nums[j] = tmp
        
        low = 0                   # Pointer for next position of 0
        mid = 0                   # Current element being examined
        high = len(nums) - 1      # Pointer for next position of 2
        
        while mid <= high:
            if nums[mid] == 0:
                # Swap 0 to the left region
                swap(low, mid)
                low += 1
                mid += 1
            elif nums[mid] == 1:
                # 1 is already in correct region
                mid += 1
            else:  # nums[mid] == 2
                # Swap 2 to the right region
                swap(mid, high)
                high -= 1
                # Don't increment mid - need to process swapped element


# ============================================================================
# ALTERNATIVE: Using Python's tuple unpacking for swap (more Pythonic)
# ============================================================================

class SolutionPythonic:
    def sortColors(self, nums):
        """Same algorithm but using Python's tuple unpacking for swap"""
        
        low = 0
        mid = 0
        high = len(nums) - 1
        
        while mid <= high:
            if nums[mid] == 0:
                nums[low], nums[mid] = nums[mid], nums[low]  # Pythonic swap
                low += 1
                mid += 1
            elif nums[mid] == 1:
                mid += 1
            else:  # nums[mid] == 2
                nums[mid], nums[high] = nums[high], nums[mid]  # Pythonic swap
                high -= 1


# ============================================================================
# VISUAL EXAMPLE: [2, 0, 2, 1, 1, 0]
# ============================================================================

"""
Initial: [2, 0, 2, 1, 1, 0]
         low=0, mid=0, high=5

Step 1: nums[mid]=2, swap(0,5) → swap with high
        [0, 0, 2, 1, 1, 2]  low=0, mid=0, high=4

Step 2: nums[mid]=0, swap(0,0) → swap with low
        [0, 0, 2, 1, 1, 2]  low=1, mid=1, high=4

Step 3: nums[mid]=0, swap(1,1) → swap with low
        [0, 0, 2, 1, 1, 2]  low=2, mid=2, high=4

Step 4: nums[mid]=2, swap(2,4) → swap with high
        [0, 0, 1, 1, 2, 2]  low=2, mid=2, high=3

Step 5: nums[mid]=1, just move mid
        [0, 0, 1, 1, 2, 2]  low=2, mid=3, high=3

Step 6: nums[mid]=1, just move mid
        [0, 0, 1, 1, 2, 2]  low=2, mid=4, high=3

Done! mid > high
"""


# ============================================================================
# COMPLEXITY COMPARISON
# ============================================================================

"""
Approach                    Time        Space       Passes
--------                    ----        -----       ------
My Solution (Counting)      O(n)        O(1)        2
Optimal (Dutch Flag)        O(n)        O(1)        1

Both are technically O(n) time and O(1) space, but Dutch National Flag 
is more efficient with a single pass and is the standard interview solution.
"""


# ============================================================================
# TEST CASES
# ============================================================================

def test_sort_colors():
    solution = Solution()
    
    # Test 1
    nums1 = [2, 0, 2, 1, 1, 0]
    solution.sortColors(nums1)
    print(f"Test 1: {nums1}")  # [0, 0, 1, 1, 2, 2]
    
    # Test 2
    nums2 = [2, 0, 1]
    solution.sortColors(nums2)
    print(f"Test 2: {nums2}")  # [0, 1, 2]
    
    # Test 3: All same
    nums3 = [1, 1, 1]
    solution.sortColors(nums3)
    print(f"Test 3: {nums3}")  # [1, 1, 1]
    
    # Test 4: Already sorted
    nums4 = [0, 1, 2]
    solution.sortColors(nums4)
    print(f"Test 4: {nums4}")  # [0, 1, 2]


if __name__ == "__main__":
    test_sort_colors()