"""
56. Merge Intervals
Medium

Given an array of intervals where intervals[i] = [start_i, end_i], merge all 
overlapping intervals, and return an array of the non-overlapping intervals 
that cover all the intervals in the input.

Example 1:
Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].

Example 2:
Input: intervals = [[1,4],[4,5]]
Output: [[1,5]]
Explanation: Intervals [1,4] and [4,5] are considered overlapping.

Example 3:
Input: intervals = [[4,7],[1,4]]
Output: [[1,7]]
Explanation: Intervals [1,4] and [4,7] are considered overlapping.

Constraints:
- 1 <= intervals.length <= 10^4
- intervals[i].length == 2
- 0 <= start_i <= end_i <= 10^4
"""


class Solution(object):
    def merge_first_attempt(self, intervals):
        """
        FIRST SOLUTION (My Initial Approach)
        
        Approach: In-place merging with pop
        
        Issues:
        1. Unnecessary type conversions: int(max(intervals[i])) etc.
           - intervals[i] is already a list [start, end]
           - max/min on 2-element list is inefficient
           - Should use: intervals[i][0] for start, intervals[i][1] for end
        2. Modifying list while iterating (using pop)
           - Can lead to index issues and complexity
        3. Excessive int() calls (intervals already contain integers)
        4. Less readable with nested max/min calls
        
        Time Complexity: O(n² log n)
        - Sort: O(n log n)
        - While loop with pop: O(n²) worst case (pop is O(n))
        - Total: O(n²)
        
        Space Complexity: O(1) - modifies input in place
        
        ⭐ Rating: Works but inefficient due to pop()
        """
        if len(intervals) < 2:
            return intervals
        
        intervals.sort()
        i = 0
        
        while i < len(intervals) - 1:
            # Check if current interval overlaps with next
            if int(max(intervals[i])) >= int(min(intervals[i + 1])):
                # Merge: [min(both starts), max(both ends)]
                intervals[i] = [
                    int(min(intervals[i])), 
                    max(int(max(intervals[i + 1])), int(max(intervals[i])))
                ]
                intervals.pop(i + 1)  # ❌ O(n) operation!
            else:
                i += 1
        
        return intervals
    
    def merge_second_attempt(self, intervals):
        """
        SECOND SOLUTION (Your Improved Approach)
        
        Approach: Build result list instead of in-place modification
        
        Issues:
        1. Still using int(max(curr)), int(min(...)) unnecessarily
        2. Complex logic with curr variable tracking
        3. Special case handling for last element
        4. Nested min/max calls make it hard to read
        5. Edge case handling with "if curr" at end
        
        Improvements over first:
        ✅ No pop() operations (better performance)
        ✅ Builds new list instead of modifying input
        
        Time Complexity: O(n log n)
        - Sort: O(n log n)
        - Single pass: O(n)
        - Total: O(n log n)
        
        Space Complexity: O(n) - result list
        
        ⭐⭐ Rating: Better performance but still complex
        """
        if len(intervals) < 2:
            return intervals
        
        intervals.sort()
        res = []
        curr = []
        i = 0
        
        while i < len(intervals) - 1:
            if not curr:
                curr = intervals[i]
            
            # Check overlap
            if int(max(curr)) >= int(min(intervals[i + 1])):
                # Merge intervals
                curr = [
                    min(int(min(curr)), int(min(intervals[i + 1]))), 
                    max(int(max(intervals[i + 1])), int(max(curr)))
                ]
            else:
                res.append(curr)
                curr = []
                # Special case for last element
                if i == len(intervals) - 2:
                    res.append(intervals[i + 1])
            
            i += 1
        
        # Handle remaining current interval
        if curr:
            res.append(curr)
        
        return res
    
    def merge_optimal_screenshot(self, intervals):
        """
        OPTIMAL SOLUTION (BEST!) ⭐⭐⭐
        
        Key Improvements:
        1. Sort by start time: intervals.sort(key=lambda i: i[0])
        2. Use output[-1] to access last added interval
        3. Simple and elegant logic
        4. No extra variables needed
        
        Algorithm:
        1. Sort intervals by start time
        2. Add first interval to output
        3. For each remaining interval:
           a. If overlaps with last interval in output: merge by updating end
           b. Otherwise: append as new interval
        
        Why This is Best:
        - Most readable
        - Fewest lines of code
        - No complex conditionals
        - Direct array access
        - Industry standard solution
        
        Time Complexity: O(n log n) - dominated by sorting
        Space Complexity: O(n) - output array
        
        ⭐⭐⭐ OPTIMAL SOLUTION - This is what you should use!
        """
        # Sort intervals by start time
        # Note: intervals.sort() also works since Python sorts by first element by default
        # Step 1: Sort intervals by start time
        # This ensures we process intervals in order from left to right
        # Example: [[4,7],[1,4]] becomes [[1,4],[4,7]]
        intervals.sort(key=lambda i: i[0])
        
        # Initialize output with first interval
        output = [intervals[0]]
        
        # Process remaining intervals
        for start, end in intervals[1:]:
            lastEnd = output[-1][1]  # End time of last interval in output
            
            # Check if current interval overlaps with last interval
            if start <= lastEnd:
                # Overlapping: merge by extending the end time
                output[-1][1] = max(lastEnd, end)
            else:
                # Non-overlapping: add as new interval
                output.append([start, end])
        
        return output
    