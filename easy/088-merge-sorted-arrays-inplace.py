"""
88. Merge Sorted Array
Easy

You are given two integer arrays nums1 and nums2, sorted in non-decreasing order, 
and two integers m and n, representing the number of elements in nums1 and nums2 
respectively.

Merge nums1 and nums2 into a single array sorted in non-decreasing order.

The final sorted array should not be returned by the function, but instead be 
stored inside the array nums1. To accommodate this, nums1 has a length of m + n, 
where the first m elements denote the elements that should be merged, and the 
last n elements are set to 0 and should be ignored. nums2 has a length of n.

Example 1:
Input: nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3
Output: [1,2,2,3,5,6]
Explanation: The arrays we are merging are [1,2,3] and [2,5,6].
The result of the merge is [1,2,2,3,5,6].

Example 2:
Input: nums1 = [1], m = 1, nums2 = [], n = 0
Output: [1]
Explanation: The arrays we are merging are [1] and [].
The result of the merge is [1].

Example 3:
Input: nums1 = [0], m = 0, nums2 = [1], n = 1
Output: [1]
Explanation: The arrays we are merging are [] and [1].
The result of the merge is [1].

Constraints:
- nums1.length == m + n
- nums2.length == n
- 0 <= m, n <= 200
- 1 <= m + n <= 200
- -10^9 <= nums1[i], nums2[j] <= 10^9
"""


class Solution(object):
    def merge_solution1(self, nums1, m, nums2, n):
        """
        SOLUTION 1 (First Attempt - Forward Insertion with Shifting)
        
        Time Complexity: O(m × n)
        Space Complexity: O(1)
        
        Issues:
        - Uses moveList() which shifts elements (O(m) per insertion)
        - Fills unused space with sentinel values
        - Complex and inefficient
        """
        if nums2:
            def moveList(i, m, nums1):
                for j in range(m - 1, i, -1):
                    nums1[j] = nums1[j - 1]
                    
            pointer1 = pointer2 = 0
            for i in range(m, m + n):
                nums1[i] = nums2[-1] + 1
            
            while pointer1 < m + n and pointer2 < n:
                if nums1[pointer1] > nums2[pointer2]:
                    moveList(pointer1, m + n, nums1)
                    nums1[pointer1] = nums2[pointer2]
                    pointer2 += 1
                pointer1 += 1
    
    def merge_solution2(self, nums1, m, nums2, n):
        """
        SOLUTION 2 (Backward Merging with Edge Case)
        
        Time Complexity: O(m + n)
        Space Complexity: O(1)
        
        Improvements:
        - Merges from back to front (no shifting needed)
        - Much faster than Solution 1
        
        Issues:
        - Requires separate loop to handle leftover nums2 elements
        - More complex condition checks
        """
        pointer1 = m - 1
        pointer2 = n - 1
        curr = m + n - 1
        
        while curr > -1 and pointer2 > -1 and pointer1 > -1:
            if nums2[pointer2] >= nums1[pointer1]:
                nums1[curr] = nums2[pointer2]
                pointer2 -= 1
            else:
                nums1[curr] = nums1[pointer1]
                pointer1 -= 1
            curr -= 1
        
        # Handle leftover nums2 elements
        if pointer2 != -1:
            for i in range(pointer2 + 1):
                nums1[i] = nums2[i]
    
    def merge_optimal(self, nums1, m, nums2, n):
        """
        OPTIMAL SOLUTION 
        
        Time Complexity: O(m + n)
        Space Complexity: O(1)
        
        Key Improvements:
        - Single while loop handles all cases elegantly
        - No need for separate edge case handling
        - Simpler and cleaner logic
        
        
        
        
        If nums2 is finished → stop
        If nums1 is finished → just copy nums2
        """
        # Start from the last valid index in nums1
        last = m + n - 1
        
        # Merge in reverse order
        while m > 0 and n > 0:
            if nums1[m - 1] > nums2[n - 1]:
                nums1[last] = nums1[m - 1]
                m -= 1
            else:
                nums1[last] = nums2[n - 1]
                n -= 1
            last -= 1
        
        # Fill nums1 with leftover nums2 elements
        while n > 0:
            nums1[last] = nums2[n - 1]
            n, last = n - 1, last - 1
            
    def merge_optimal_cleaner(self, nums1, m, nums2, n):
        """
        OPTIMAL SOLUTION with Cleaner approach
        
        Time Complexity: O(m + n)
        Space Complexity: O(1)
        
        Key Improvements:
        - Single while loop handles all cases elegantly
        - No need for separate edge case handling
        - Simpler and cleaner logic
        """      
            
        last = m + n - 1

        while n - 1 >= 0:
            if m - 1>= 0 and nums1[ m - 1] > nums2[ n - 1 ]:
                nums1[ last ] = nums1[ m - 1]
                m -= 1
            else:
                nums1[ last ] = nums2[ n - 1 ]
                n -= 1
            last -= 1
    
    # Main function uses optimal solution
    def merge(self, nums1, m, nums2, n):
        """
        :type nums1: List[int]
        :type m: int
        :type nums2: List[int]
        :type n: int
        :rtype: None Do not return anything, modify nums1 in-place instead.
        """
        return self.merge_optimal(nums1, m, nums2, n)