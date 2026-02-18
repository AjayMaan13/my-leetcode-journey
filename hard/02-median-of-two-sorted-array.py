"""
4. MEDIAN OF TWO SORTED ARRAYS

Problem Statement:
Given two sorted arrays nums1 and nums2 of size m and n respectively, return 
the median of the two sorted arrays.

The overall run time complexity should be O(log(m+n)).

Example 1:
Input: nums1 = [1,3], nums2 = [2]
Output: 2.00000
Explanation: merged array = [1,2,3] and median is 2.

Example 2:
Input: nums1 = [1,2], nums2 = [3,4]
Output: 2.50000
Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.
"""


# ==============================================================================
# APPROACH 1: YOUR SOLUTION (MERGE UNTIL MIDDLE)
# ==============================================================================
# Time Complexity: O(m + n)
# Space Complexity: O(1)

class Solution:
    def findMedianSortedArrays(self, nums1, nums2):
        """
        Merge arrays like merge sort until we reach the middle element(s).
        
        Key Idea: We don't need to merge the entire arrays - just go until
        we reach the median position(s).
        """
        n1, n2 = len(nums1), len(nums2)
        total = n1 + n2

        # Position of median (0-indexed)
        middle = total // 2
        is_even = (total % 2 == 0)

        # Two pointers for nums1 and nums2
        i = j = 0
        count = 0
        prev = curr = 0  # Track current and previous elements

        # Merge until we reach middle position
        while count <= middle:
            prev = curr  # Save previous element (needed for even case)

            # Choose next element like merge sort
            if i < n1 and j < n2:
                # Both arrays have elements - pick smaller one
                if nums1[i] <= nums2[j]:
                    curr = nums1[i]
                    i += 1
                else:
                    curr = nums2[j]
                    j += 1

            elif i < n1:  # nums2 finished, use remaining nums1
                curr = nums1[i]
                i += 1
            else:  # nums1 finished, use remaining nums2
                curr = nums2[j]
                j += 1

            count += 1

        # For even total: median is average of two middle elements
        if is_even:
            return (prev + curr) / 2.0
        # For odd total: median is the middle element
        return curr


# ==============================================================================
# APPROACH 2: BINARY SEARCH (OPTIMAL)
# ==============================================================================
# Time Complexity: O(log(min(m, n)))
# Space Complexity: O(1)
#
# Key Insight: Binary search on the smaller array to find the correct partition
# that divides both arrays such that left half ≤ right half.

class Solution_Optimal:
    def findMedianSortedArrays(self, nums1, nums2):
        """
        Binary search approach - partition arrays to find median in O(log(min(m,n)))
        
        Strategy: Find a partition in both arrays such that:
        1. Left half has same number of elements as right half (or 1 more)
        2. max(left_A, left_B) <= min(right_A, right_B)
        """
        A, B = nums1, nums2
        total = len(nums1) + len(nums2)
        half = total // 2

        # Always binary search on the smaller array for efficiency
        if len(B) < len(A):
            A, B = B, A

        # Binary search on array A
        l, r = 0, len(A) - 1

        while True:
            # Partition index for A (mid point)
            i = (l + r) // 2  # A
            # Partition index for B (to balance the halves)
            j = half - i - 2  # B (subtract 2 because of 0-indexing)

            # Get values at partition boundaries
            # If partition is at edge, use infinity/-infinity
            Aleft = A[i] if i >= 0 else float("-infinity")
            Aright = A[i + 1] if (i + 1) < len(A) else float("infinity")
            Bleft = B[j] if j >= 0 else float("-infinity")
            Bright = B[j + 1] if (j + 1) < len(B) else float("infinity")

            # Check if partition is correct
            # Correct partition: max(left) <= min(right)
            if Aleft <= Bright and Bleft <= Aright:
                # Partition is correct! Calculate median

                # If total is odd, median is min of right halves
                if total % 2:
                    return min(Aright, Bright)

                # If total is even, median is average of max(left) and min(right)
                return (max(Aleft, Bleft) + min(Aright, Bright)) / 2

            # Partition is wrong - adjust binary search
            elif Aleft > Bright:
                # A's left is too large, move partition left in A
                r = i - 1
            else:
                # A's left is too small, move partition right in A
                l = i + 1

