"""
Count Inversions in an Array

Problem Statement: 
Given an array of N integers, count the inversion of the array.

An inversion is a pair of indices (i, j) such that:
- i < j (i comes before j)
- arr[i] > arr[j] (but element at i is greater than element at j)

This measures how far the array is from being sorted.

Example 1:
Input: N = 5, array[] = {1,2,3,4,5}
Output: 0
Explanation: Array is already sorted, so no inversions.

Example 2:
Input: N = 5, array[] = {5,4,3,2,1}
Output: 10
Explanation: Array is reverse sorted (worst case).
Inversions: (5,4), (5,3), (5,2), (5,1), (4,3), (4,2), (4,1), (3,2), (3,1), (2,1)
Formula for reverse sorted: n * (n-1) / 2 = 5 * 4 / 2 = 10

Example 3:
Input: N = 5, array[] = {5,3,2,1,4}
Output: 7
Explanation: Inversions are (5,3), (5,2), (5,1), (5,4), (3,2), (3,1), (2,1)
Not inversions: (2,4), (1,4) because 2 < 4 and 1 < 4

Constraints:
- 1 <= N <= 10^5
- 1 <= arr[i] <= 10^9
"""


class Solution(object):
    def countInversions_brute_force(self, arr):
        """
        BRUTE FORCE APPROACH
        
        Algorithm:
        1. Use two nested loops
        2. For each pair (i, j) where i < j:
           - If arr[i] > arr[j], it's an inversion
           - Increment counter
        
        Time Complexity: O(n²)
        - Two nested loops, each runs n times
        - Total: n * n = O(n²)
        
        Space Complexity: O(1)
        - Only using a counter variable
        
        Drawback: Too slow for large arrays (n > 10,000)
        """
        cnt = 0  # Initialize inversion count
        n = len(arr)
        
        # Check all pairs (i, j) where i < j
        for i in range(n):
            for j in range(i + 1, n):
                # If element at i is greater than element at j
                # Then (i, j) is an inversion
                if arr[i] > arr[j]:
                    cnt += 1
        
        return cnt
    
    def countInversions_merge_sort(self, arr):
        """
        OPTIMAL APPROACH: Using Merge Sort
        
        Key Insight:
        During merge sort, when merging two sorted halves:
        - Left half: [low...mid] (sorted)
        - Right half: [mid+1...high] (sorted)
        
        If arr[left] > arr[right]:
        - Then arr[left] is greater than arr[right]
        - AND all elements after arr[left] in left half are also greater
        - Because left half is sorted!
        - So we can count (mid - left + 1) inversions at once
        
        Time Complexity: O(n log n)
        - Same as merge sort
        - Divide: O(log n) levels
        - Merge: O(n) at each level
        - Total: O(n log n)
        
        Space Complexity: O(n)
        - Temporary array for merging: O(n)
        - Recursion stack: O(log n)
        - Total: O(n)
        
        This is OPTIMAL for comparison-based counting!
        """
        def merge(arr, low, mid, high):
            """
            Merge two sorted halves and count inversions
            
            Parameters:
            - arr: array to merge
            - low: starting index of left half
            - mid: ending index of left half
            - high: ending index of right half
            
            Returns: number of inversions during merge
            """
            temp = []  # Temporary array to store merged result
            
            left = low      # Pointer for left half
            right = mid + 1 # Pointer for right half
            cnt = 0         # Count inversions
            
            # Merge two sorted halves
            while left <= mid and right <= high:
                if arr[left] <= arr[right]:
                    # Left element is smaller or equal
                    # No inversion, just add to temp
                    temp.append(arr[left])
                    left += 1
                else:
                    # arr[left] > arr[right]
                    # This means arr[left], arr[left+1], ..., arr[mid]
                    # are ALL greater than arr[right]
                    # Because left half is sorted!
                    # So we have (mid - left + 1) inversions
                    temp.append(arr[right])
                    cnt += (mid - left + 1)  # COUNT INVERSIONS
                    right += 1
            
            # Copy remaining elements from left half
            while left <= mid:
                temp.append(arr[left])
                left += 1
            
            # Copy remaining elements from right half
            while right <= high:
                temp.append(arr[right])
                right += 1
            
            # Copy merged elements back to original array
            for i in range(low, high + 1):
                arr[i] = temp[i - low]
            
            return cnt
        
        def mergeSort(arr, low, high):
            """
            Recursive merge sort with inversion counting
            
            Returns: number of inversions in arr[low...high]
            """
            cnt = 0  # Count inversions
            
            # Base case: single element or invalid range
            if low >= high:
                return cnt
            
            # Find middle point
            mid = (low + high) // 2
            
            # Count inversions in left half
            cnt += mergeSort(arr, low, mid)
            
            # Count inversions in right half
            cnt += mergeSort(arr, mid + 1, high)
            
            # Count inversions during merge (cross inversions)
            cnt += merge(arr, low, mid, high)
            
            return cnt
        
        # Start merge sort from entire array
        return mergeSort(arr, 0, len(arr) - 1)
    


"""
============================================================================
VISUAL EXAMPLE: How Merge Sort Counts Inversions
============================================================================

Array: [5, 3, 2, 1, 4]

STEP 1: Divide into smallest subarrays
---------------------------------------
                    [5, 3, 2, 1, 4]
                   /               \
            [5, 3, 2]              [1, 4]
           /         \             /     \
        [5, 3]      [2]         [1]     [4]
       /     \
     [5]     [3]


STEP 2: Merge and count inversions
-----------------------------------

Level 1: Merge [5] and [3]
  5 > 3 → inversion! Count = 1
  Result: [3, 5]

Level 1: Merge [1] and [4]
  1 < 4 → no inversion
  Result: [1, 4]

Level 2: Merge [3, 5] and [2]
  3 > 2 → inversions: (3,2), (5,2)
  Count = 2 (mid - left + 1 = 1 - 0 + 1 = 2)
  Result: [2, 3, 5]

Level 3: Merge [2, 3, 5] and [1, 4]
  Comparisons:
  - 2 > 1 → inversions: (2,1), (3,1), (5,1) = 3
  - 2 < 4 → no inversion
  - 3 < 4 → no inversion
  - 5 > 4 → inversion: (5,4) = 1
  Count = 3 + 1 = 4
  Result: [1, 2, 3, 4, 5]

Total inversions: 1 + 2 + 4 = 7 ✓


============================================================================
WHY MID - LEFT + 1 COUNTS ALL INVERSIONS
============================================================================

Scenario: Merging sorted left and right halves

Left:  [3, 5, 7, 9]  (indices: left=0, mid=3)
Right: [2, 4, 6, 8]  (indices: right=0)

When we compare:
- left points to 3 (index 0)
- right points to 2 (index 0)
- arr[left] = 3 > arr[right] = 2

Since left half is SORTED:
- If 3 > 2, then 5 > 2, 7 > 2, 9 > 2
- All elements from left to mid form inversions with 2

Count = mid - left + 1 = 3 - 0 + 1 = 4

Inversions: (3,2), (5,2), (7,2), (9,2) ✓


============================================================================
COMPLEXITY COMPARISON
============================================================================

Approach              Time           Space        Notes
------------------------------------------------------------------------
Brute Force          O(n²)          O(1)         Too slow for n > 10^4
Merge Sort           O(n log n)     O(n)         Optimal!


Why Merge Sort is Better:
- Brute force checks n² pairs
- Merge sort counts multiple inversions in one comparison
- Example: Instead of checking (3,2), (5,2), (7,2) separately
  We count all 3 at once with (mid - left + 1)


============================================================================
STEP-BY-STEP TRACE: [5, 4, 3, 2, 1]
============================================================================

Initial: [5, 4, 3, 2, 1]

mergeSort(0, 4):
  mid = 2
  mergeSort(0, 2):  # Left half
    mid = 1
    mergeSort(0, 1):  # [5, 4]
      mid = 0
      mergeSort(0, 0): return 0  # [5]
      mergeSort(1, 1): return 0  # [4]
      merge(0, 0, 1):
        5 > 4 → cnt = 1
        Result: [4, 5]
      return 1
    mergeSort(2, 2): return 0  # [3]
    merge(0, 1, 2):
      4 > 3 → cnt = 2 (4,3), (5,3)
      Result: [3, 4, 5]
    return 1 + 2 = 3
  
  mergeSort(3, 4):  # Right half
    mid = 3
    mergeSort(3, 3): return 0  # [2]
    mergeSort(4, 4): return 0  # [1]
    merge(3, 3, 4):
      2 > 1 → cnt = 1
      Result: [1, 2]
    return 1
  
  merge(0, 2, 4):
    3 > 1 → cnt = 3 (3,1), (4,1), (5,1)
    3 > 2 → cnt = 3 (3,2), (4,2), (5,2)
    Result: [1, 2, 3, 4, 5]
    return 6

Total: 3 + 1 + 6 = 10 ✓

Verification: n*(n-1)/2 = 5*4/2 = 10 ✓


============================================================================
KEY TAKEAWAYS
============================================================================

1. Inversion Definition:
   - Pair (i, j) where i < j but arr[i] > arr[j]
   - Measures how "unsorted" the array is

2. Brute Force:
   - Check all n² pairs
   - O(n²) time - too slow

3. Merge Sort Optimization:
   - Count multiple inversions at once
   - Uses sorted property of subarrays
   - O(n log n) time - optimal!

4. Key Insight:
   - When arr[left] > arr[right] during merge
   - All elements from left to mid form inversions
   - Count: (mid - left + 1)

5. Total Inversions:
   - Sum of inversions in left half
   - Sum of inversions in right half
   - Sum of cross-inversions during merge
"""