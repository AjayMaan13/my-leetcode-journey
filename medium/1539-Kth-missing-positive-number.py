"""
1539. Kth Missing Positive Number
Easy

Given an array arr of positive integers sorted in a strictly increasing order, and an 
integer k.

Return the kth positive integer that is missing from this array.

Example 1:
Input: arr = [2,3,4,7,11], k = 5
Output: 9
Explanation: The missing positive integers are [1,5,6,8,9,10,12,13,...]. The 5th missing 
positive integer is 9.

Example 2:
Input: arr = [1,2,3,4], k = 2
Output: 6
Explanation: The missing positive integers are [5,6,7,...]. The 2nd missing positive 
integer is 6.

Constraints:
- 1 <= arr.length <= 1000
- 1 <= arr[i] <= 1000
- 1 <= k <= 1000
- arr[i] < arr[j] for 1 <= i < j <= arr.length
"""


class Solution(object):
    def findKthPositive_original(self, arr, k):
        """
        ORIGINAL SOLUTION (Your Approach)
        
        Approach: Linear search with optimization for numbers after array
        
        Issues:
        - O(n) lookup: "if i not in arr" checks entire array each time
        - Overall O(m * n) where m = arr[-1], n = len(arr)
        - Inefficient for large arrays or large missing counts
        
        Time: O(m * n) worst case where m = arr[-1]
        Space: O(1)
        """
        missingInBetween = arr[-1] - len(arr)
        
        # If k-th missing is after the last element
        if k > missingInBetween:
            return arr[-1] + (k - missingInBetween)
        
        # Linear search for k-th missing
        for i in range(1, arr[-1]):
            if i not in arr:  # O(n) lookup!
                k -= 1
                if k == 0:
                    return i
    
    def findKthPositive_optimal(self, arr, k):
        """
        OPTIMAL SOLUTION: Binary Search
        
        Key Insight:
        At index i, number of missing positives = arr[i] - (i + 1)
        
        Why?
        - If no numbers missing: arr[i] should be i + 1
        - Actual missing count = arr[i] - (i + 1)
        
        Example: arr = [2,3,4,7,11], k = 5
        
        Index 0: arr[0]=2, missing = 2 - 1 = 1  [missing: 1]
        Index 1: arr[1]=3, missing = 3 - 2 = 1  [missing: 1]
        Index 2: arr[2]=4, missing = 4 - 3 = 1  [missing: 1]
        Index 3: arr[3]=7, missing = 7 - 4 = 3  [missing: 1,5,6]
        Index 4: arr[4]=11, missing = 11 - 5 = 6 [missing: 1,5,6,8,9,10]
        
        Binary search to find rightmost index where missing < k
        Answer = arr[index] + (k - missing_at_index)
        OR if all missing counts >= k: answer = k
        
        Algorithm:
        1. Binary search to find largest index where missing count < k
        2. If no such index (all >= k): return k
        3. Otherwise: return arr[left] + (k - missing_count_at_left)
        
        Time: O(log n)
        Space: O(1)
        
        Much more efficient!
        """
        left, right = 0, len(arr) - 1
        
        # Binary search for position
        while left <= right:
            mid = (left + right) // 2
            missing = arr[mid] - (mid + 1)
            
            if missing < k:
                left = mid + 1
            else:
                right = mid - 1
        
        # At this point, left is the insertion point
        # Missing count at position left-1 is < k
        # Missing count at position left is >= k (or left is beyond array)
        
        # If left is 0, all missing are before arr[0]
        # Answer is simply k
        
        # Otherwise, k-th missing is after arr[left-1]
        # Missing at arr[left-1] = arr[left-1] - left
        # Need (k - missing_at_left-1) more numbers after arr[left-1]
        # Answer = arr[left-1] + (k - (arr[left-1] - left))
        #        = arr[left-1] + k - arr[left-1] + left
        #        = left + k
        
        return left + k
    
    # Main function uses optimal solution
    def findKthPositive(self, arr, k):
        """
        :type arr: List[int]
        :type k: int
        :rtype: int
        """
        return self.findKthPositive_optimal(arr, k)