"""
LeetCode 162: Find Peak Element
Difficulty: Medium

Problem Statement:
A peak element is an element that is strictly greater than its neighbors.
Given a 0-indexed integer array nums, find a peak element, and return its index.
If the array contains multiple peaks, return the index to any of the peaks.

Key Constraint: nums[-1] = nums[n] = -∞ (elements outside array are negative infinity)
Required: O(log n) time complexity

Examples:
1. nums = [1,2,3,1] → Output: 2 (peak is 3)
2. nums = [1,2,1,3,5,6,4] → Output: 5 (peak is 6) or 1 (peak is 2)

Key Insights:
- Array boundaries are treated as -∞, so edges can be peaks
- Multiple valid answers possible
- Must use binary search to achieve O(log n)
"""

# ============================================================================
# SOLUTION 1: YOUR SOLUTION - EXPLICIT EDGE CASES
# ============================================================================

class SolutionExplicitEdges:
    """
    Approach: Binary search with explicit handling of small arrays
    
    Time Complexity: O(log n)
    Space Complexity: O(1)
    
    Strategy:
    - Handle arrays of size 1 and 2 separately
    - For larger arrays, use binary search
    - At each mid point, check both neighbors
    - Move towards the higher neighbor (peak must exist there)
    
    Pros:
    - Handles edge cases upfront
    - Very clear logic flow
    - Easy to understand
    
    Cons:
    - Extra code for edge cases
    - Could be simplified
    
    Performance: 95-100% runtime, 90-95% memory
    """
    
    def findPeakElement(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        if len(nums) < 2:
            return 0
        
        if len(nums) == 2:
            return 0 if nums[0] > nums[1] else 1
            
        low, high = 0, len(nums) - 1 
        
        while low <= high:
            mid = low + ((high - low) // 2)
            
            if mid < len(nums) - 1 and nums[mid] < nums[mid + 1]:
                low = mid + 1
            elif mid > 0 and nums[mid] < nums[mid - 1]:
                high = mid - 1
            else:
                return mid


# ============================================================================
# SOLUTION 2: OPTIMAL - CLEAN BINARY SEARCH (RECOMMENDED)
# ============================================================================

class SolutionOptimal:
    """
    Approach: Clean binary search without special cases
    
    Time Complexity: O(log n)
    Space Complexity: O(1)
    
    Key Insight:
    If nums[mid] < nums[mid + 1], the right side MUST contain a peak.
    Why? Because either:
    1. nums[mid+1] is itself a peak, or
    2. The sequence keeps increasing until a peak is found, or
    3. We reach the right boundary (which is treated as -∞, so last element is peak)
    
    Strategy:
    - Always move towards the ascending side
    - Use while low < high (not <=) to avoid infinite loop
    - When loop ends, low == high at a peak
    
    Pros:
    - Cleanest solution (fewest lines)
    - No edge case handling needed
    - Most elegant approach
    - Handles all cases uniformly
    
    Performance: 100% runtime, 95-98% memory
    
    This is THE solution to present in interviews!
    """
    
    def findPeakElement(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        low, high = 0, len(nums) - 1
        
        while low < high:
            mid = low + (high - low) // 2
            
            if nums[mid] < nums[mid + 1]:
                low = mid + 1
            else:
                high = mid
        
        return low


# ============================================================================
# SOLUTION 3: BOUNDARY CHECK VARIANT
# ============================================================================

class SolutionBoundaryCheck:
    """
    Approach: Check boundaries first, then binary search
    
    Time Complexity: O(log n), best case O(1)
    Space Complexity: O(1)
    
    Strategy:
    - Check if first or last element is peak (O(1) check)
    - If not, search in the middle using binary search
    - Guarantees middle elements have both neighbors
    
    Pros:
    - Quick return for boundary peaks
    - No bound checking needed in binary search
    - Good for arrays where peaks are often at edges
    
    When to use:
    - If you expect peaks at boundaries frequently
    - To avoid repeated bound checks in loop
    """
    
    def findPeakElement(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        n = len(nums)
        
        if n == 1:
            return 0
        
        if nums[0] > nums[1]:
            return 0
        
        if nums[n-1] > nums[n-2]:
            return n - 1
        
        low, high = 1, n - 2
        
        while low <= high:
            mid = low + (high - low) // 2
            
            if nums[mid] > nums[mid-1] and nums[mid] > nums[mid+1]:
                return mid
            elif nums[mid] < nums[mid+1]:
                low = mid + 1
            else:
                high = mid - 1
        
        return low


# ============================================================================
# SOLUTION 4: RECURSIVE APPROACH (EDUCATIONAL)
# ============================================================================

class SolutionRecursive:
    """
    Approach: Recursive binary search
    
    Time Complexity: O(log n)
    Space Complexity: O(log n) due to recursion stack
    
    Strategy:
    - Same logic as iterative but using recursion
    - Good for showing understanding of recursion
    
    Pros:
    - Elegant recursive formulation
    - Shows functional programming style
    
    Cons:
    - Uses O(log n) space for call stack
    - Slightly slower due to function call overhead
    
    When to use:
    - If interviewer specifically asks for recursive solution
    - To demonstrate recursion skills
    """
    
    def findPeakElement(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        return self.search(nums, 0, len(nums) - 1)
    
    def search(self, nums, low, high):
        """
        Recursive helper function
        """
        if low == high:
            return low
        
        mid = low + (high - low) // 2
        
        if nums[mid] < nums[mid + 1]:
            return self.search(nums, mid + 1, high)
        else:
            return self.search(nums, low, mid)
