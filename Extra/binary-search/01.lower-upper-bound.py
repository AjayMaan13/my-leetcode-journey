"""
Binary Search: Lower Bound and Upper Bound Algorithms

Lower Bound: Finds the first index where arr[ind] >= x
Upper Bound: Finds the first index where arr[ind] > x

Both algorithms use binary search for O(log n) time complexity.
"""

# ============================================================================
# LOWER BOUND ALGORITHM
# ============================================================================

class LowerBoundFinder:
    """
    Lower Bound: Find the smallest index where arr[index] >= x
    
    Examples:
    - arr = [1,2,2,3], x = 2 → Result: 1 (arr[1] = 2 >= 2)
    - arr = [3,5,8,15,19], x = 9 → Result: 3 (arr[3] = 15 >= 9)
    """
    
    def lower_bound(self, arr, x):
        """
        Binary search to find lower bound
        
        Args:
            arr: Sorted array of integers
            x: Target value
            
        Returns:
            Index of lower bound, or len(arr) if not found
        """
        low, high = 0, len(arr) - 1     # Search range
        ans = len(arr)                  # Default value if not found

        while low <= high:
            mid = (low + high) // 2     # Find middle index
            
            if arr[mid] >= x:
                ans = mid               # Store possible answer
                high = mid - 1          # Move to the left for smaller index
            else:
                low = mid + 1           # Move to the right for larger values
                
        return ans                      # Return result


# ============================================================================
# UPPER BOUND ALGORITHM
# ============================================================================

class UpperBoundFinder:
    """
    Upper Bound: Find the smallest index where arr[index] > x
    
    Examples:
    - arr = [1,2,2,3], x = 2 → Result: 3 (arr[3] = 3 > 2)
    - arr = [3,5,8,9,15,19], x = 9 → Result: 4 (arr[4] = 15 > 9)
    """
    
    def upper_bound_linear(self, arr, x):
        """
        Linear search to find upper bound (Brute Force)
        Time Complexity: O(N)
        Space Complexity: O(1)
        """
        for i in range(len(arr)):
            if arr[i] > x:
                return i  # First element greater than x
        return len(arr)   # Return size if no such element found
    
    def upper_bound(self, arr, x):
        """
        Binary search to find upper bound (Optimal)
        Time Complexity: O(log N)
        Space Complexity: O(1)
        
        Args:
            arr: Sorted array of integers
            x: Target value
            
        Returns:
            Index of upper bound, or len(arr) if not found
        """
        low, high = 0, len(arr) - 1
        ans = len(arr)  # Default to length if no element > x

        while low <= high:
            mid = (low + high) // 2

            if arr[mid] > x:
                ans = mid      # Store current mid as answer
                high = mid - 1 # Search left for smaller index
            else:
                low = mid + 1  # Search right for larger values
                
        return ans

