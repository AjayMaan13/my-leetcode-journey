"""
Floor and Ceil in Sorted Array
Difficulty: Easy-Medium

Problem Statement:
Given a sorted array arr of n integers and an integer x, find the floor and 
ceiling of x in the array.

Definitions:
- Floor: Largest element in the array which is smaller than or equal to x
- Ceil: Smallest element in the array which is greater than or equal to x

Examples:
1. arr = [3, 4, 4, 7, 8, 10], x = 5 → Output: [4, 7]
2. arr = [3, 4, 4, 7, 8, 10], x = 8 → Output: [8, 8]
3. arr = [3, 4, 4, 7, 8, 10], x = 2 → Output: [-1, 3]
4. arr = [3, 4, 4, 7, 8, 10], x = 11 → Output: [10, -1]
"""

# ============================================================================
# SOLUTION 1: STANDARD TWO-PASS APPROACH
# ============================================================================

class FloorCeilFinder:
    """
    Approach: Two separate binary searches (one for floor, one for ceil)
    
    Time Complexity: O(2 * log n) = O(log n)
    Space Complexity: O(1)
    
    Pros: Clear separation of concerns, easy to understand
    Cons: Makes two passes through the array
    """
    
    def find_floor(self, arr, x):
        """
        Find the largest element <= x
        """
        low, high = 0, len(arr) - 1
        ans = -1
        
        while low <= high:
            mid = (low + high) // 2
            
            if arr[mid] <= x:
                ans = arr[mid]  # Potential floor
                low = mid + 1   # Search for larger value in right half
            else:
                high = mid - 1  # Search in left half
                
        return ans

    def find_ceil(self, arr, x):
        """
        Find the smallest element >= x
        """
        low, high = 0, len(arr) - 1
        ans = -1
        
        while low <= high:
            mid = (low + high) // 2
            
            if arr[mid] >= x:
                ans = arr[mid]  # Potential ceil
                high = mid - 1  # Search for smaller value in left half
            else:
                low = mid + 1   # Search in right half
                
        return ans

    def get_floor_and_ceil(self, arr, x):
        """Get both floor and ceil"""
        floor = self.find_floor(arr, x)
        ceil = self.find_ceil(arr, x)
        return [floor, ceil]


# ============================================================================
# SOLUTION 2: OPTIMIZED ONE-PASS APPROACH (Your Solution - Elegant!)
# ============================================================================

class FloorCeilOptimized:
    """
    Approach: Single binary search with pointer tracking
    
    Time Complexity: O(log n) - Single pass!
    Space Complexity: O(1)
    
    Key Insight: After binary search ends:
    - 'high' points to the largest element < target (floor candidate)
    - 'low' points to the smallest element > target (ceil candidate)
    
    This is the most efficient approach!
    """
    
    def get_floor_and_ceil(self, nums, target):
        """
        Single-pass solution using binary search pointer properties
        """
        if len(nums) < 1:
            return [-1, -1]
            
        low, high = 0, len(nums) - 1
        
        while low <= high:
            mid = (low + high) // 2
            
            if nums[mid] == target:
                # Found exact match - both floor and ceil are the same
                return [target, target]
            elif nums[mid] > target:
                high = mid - 1
            else:
                low = mid + 1
        
        # After loop ends:
        # - high points to largest element < target (floor)
        # - low points to smallest element > target (ceil)
        
        floor_val = nums[high] if high >= 0 else -1
        ceil_val = nums[low] if low < len(nums) else -1
        
        return [floor_val, ceil_val]
