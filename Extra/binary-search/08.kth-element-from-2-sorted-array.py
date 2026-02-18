# HARD: similar to 4. Median of Two Sorted Arrays


"""
K-TH ELEMENT OF TWO SORTED ARRAYS

Problem Statement:
Given two sorted arrays a and b of size m and n respectively, find the kth 
element of the final sorted array (1-indexed).

Example 1:
Input: a = [2, 3, 6, 7, 9], b = [1, 4, 8, 10], k = 5
Output: 6
Explanation: Final sorted array = [1, 2, 3, 4, 6, 7, 8, 9, 10]
The 5th element is 6.

Example 2:
Input: a = [100, 112, 256, 349, 770], b = [72, 86, 113, 119, 265, 445, 892], k = 7
Output: 256
Explanation: Final sorted array = [72, 86, 100, 112, 113, 119, 256, 265, 349, 445, 770, 892]
The 7th element is 256.
"""


# ==============================================================================
# YOUR APPROACH (WITH CORRECTIONS)
# ==============================================================================
# Time Complexity: O(log(min(m, n)))
# Space Complexity: O(1)

def findKthSortedArray_corrected(nums1, nums2, k):
    """
    Find kth element using binary search 
    
    Key fixes:
    1. Correct boundary checks (>= 0 instead of > 0)
    2. Proper calculation of left partition size
    3. Fixed edge case handling
    """
    A, B = nums1, nums2
    
    # Always search on smaller array for efficiency
    if len(A) > len(B):
        A, B = B, A
    
    # Number of elements that should be in LEFT partition
    # Since k is 1-indexed, we want k elements total in left partition
    left_partition_size = k
    
    # Binary search boundaries
    low = 0
    high = len(A)  # Should be len(A), not len(A) - 1
    
    while low <= high:
        # Partition indices (number of elements from each array in left partition)
        Aindex = (low + high) // 2  # Elements from A in left partition
        Bindex = left_partition_size - Aindex  # Elements from B in left partition
        
        # Get boundary values with proper edge case handling
        # Aleft: rightmost element in A's left partition
        Aleft = A[Aindex - 1] if Aindex > 0 else float('-inf')
        # Aright: leftmost element in A's right partition
        Aright = A[Aindex] if Aindex < len(A) else float('inf')
        # Bleft: rightmost element in B's left partition
        Bleft = B[Bindex - 1] if Bindex > 0 else float('-inf')
        # Bright: leftmost element in B's right partition
        Bright = B[Bindex] if Bindex < len(B) else float('inf')
        
        # Check if partition is correct
        # Correct when: max(left) <= min(right)
        if Aleft <= Bright and Bleft <= Aright:
            # Found correct partition!
            # Kth element is the max of left partition
            return max(Aleft, Bleft)
        
        elif Aleft > Bright:
            # A's left is too large, need fewer elements from A
            high = Aindex - 1
        else:
            # A's left is too small, need more elements from A
            low = Aindex + 1
    
    return -1  # Should never reach here


# ==============================================================================
# OPTIMAL SOLUTION (CLEANER VERSION)
# ==============================================================================
# Time Complexity: O(log(min(m, n)))
# Space Complexity: O(1)

def findKthElement(nums1, nums2, k):
    """
    Find kth element using binary search - optimal approach
    
    Strategy: Partition both arrays such that left partition has exactly k elements
    and max(left) <= min(right). The kth element is max(left partition).
    """
    A, B = nums1, nums2
    
    # Ensure A is the smaller array for efficiency
    if len(A) > len(B):
        A, B = B, A
    
    m, n = len(A), len(B)
    
    # Binary search on A (smaller array)
    low = max(0, k - n)  # Must take at least (k - n) from A if B doesn't have enough
    high = min(k, m)     # Can't take more than k or more than A's length
    
    while low <= high:
        # Number of elements to take from A in left partition
        partitionA = (low + high) // 2
        # Number of elements to take from B in left partition
        partitionB = k - partitionA
        
        # Get boundary elements
        # Elements at partition-1 are in LEFT, elements at partition are in RIGHT
        maxLeftA = A[partitionA - 1] if partitionA > 0 else float('-inf')
        minRightA = A[partitionA] if partitionA < m else float('inf')
        
        maxLeftB = B[partitionB - 1] if partitionB > 0 else float('-inf')
        minRightB = B[partitionB] if partitionB < n else float('inf')
        
        # Check if partition is valid
        if maxLeftA <= minRightB and maxLeftB <= minRightA:
            # Perfect partition! Kth element is max of left partition
            return max(maxLeftA, maxLeftB)
        
        elif maxLeftA > minRightB:
            # Too many elements from A, reduce
            high = partitionA - 1
        else:
            # Too few elements from A, increase
            low = partitionA + 1
    
    return -1


# ==============================================================================
# BRUTE FORCE (FOR COMPARISON)
# ==============================================================================
# Time Complexity: O(m + n)
# Space Complexity: O(1)

def findKthElement_bruteforce(nums1, nums2, k):
    """
    Merge arrays until kth element - simple approach
    """
    i = j = 0
    count = 0
    
    while i < len(nums1) and j < len(nums2):
        if nums1[i] <= nums2[j]:
            count += 1
            if count == k:
                return nums1[i]
            i += 1
        else:
            count += 1
            if count == k:
                return nums2[j]
            j += 1
    
    # One array exhausted
    while i < len(nums1):
        count += 1
        if count == k:
            return nums1[i]
        i += 1
    
    while j < len(nums2):
        count += 1
        if count == k:
            return nums2[j]
        j += 1
    
    return -1

