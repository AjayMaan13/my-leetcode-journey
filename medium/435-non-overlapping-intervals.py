# 435. Non-overlapping Intervals
# https://leetcode.com/problems/non-overlapping-intervals/
#
# Given an array of intervals, return the minimum number of intervals to remove
# to make the rest non-overlapping.
# Note: intervals that only touch at a point (e.g. [1,2] and [2,3]) are non-overlapping.
#
# Example 1:
#   Input: intervals = [[1,2],[2,3],[3,4],[1,3]]
#   Output: 1  ([1,3] can be removed)
#
# Example 2:
#   Input: intervals = [[1,2],[1,2],[1,2]]
#   Output: 2
#
# Example 3:
#   Input: intervals = [[1,2],[2,3]]
#   Output: 0  (already non-overlapping)
#
# Constraints:
#   1 <= intervals.length <= 10^5
#   -5 * 10^4 <= start < end <= 5 * 10^4


# Approach 1: Sort by Start, Greedy Remove - O(n log n) time, O(1) space
#
# Sort by start time. Walk through intervals tracking prevEnd (end of last kept interval).
# When an overlap is detected (current start < prevEnd):
#   - increment removal count
#   - greedily keep the interval with the SMALLER end (prevEnd = min(end, prevEnd))
#     because a shorter interval leaves more room for future intervals to fit.
# When no overlap: just advance prevEnd to current end.
class SolutionSortByStart:
    def eraseOverlapIntervals(self, intervals):
        intervals.sort()               # sort by start time (then end time as tiebreak)
        prevEnd = intervals[0][1]
        res = 0

        for start, end in intervals[1:]:
            if start >= prevEnd:
                prevEnd = end          # no overlap — move window forward
            else:
                res += 1              # overlap — remove one interval
                prevEnd = min(end, prevEnd)  # keep the one ending sooner

        return res


# Approach 2: Sort by End, Count Kept (Interval Scheduling Maximization) - O(n log n) time, O(1) space
#
# Classic greedy insight: to minimize removals, maximize the number of intervals we KEEP.
# Sort by end time. Greedily select an interval if it starts at or after the last kept end.
# Always picking the earliest-ending compatible interval leaves the most room for the rest.
#
# This is the "Activity Selection Problem" — a foundational greedy algorithm.
# Answer = total intervals - max kept intervals.
class Solution:
    def eraseOverlapIntervals(self, intervals):
        intervals.sort(key=lambda x: x[1])  # sort by end time — earlier end = better greedy choice

        count = 0               # number of intervals we can keep
        last_end = float('-inf')

        for start, end in intervals:
            if start >= last_end:   # no overlap with last kept interval
                count += 1
                last_end = end      # update the end of the last kept interval

        return len(intervals) - count   # removals = total - kept


intervals = [[1, 2], [2, 3], [3, 4], [1, 3]]
sol = Solution()
print(sol.eraseOverlapIntervals(intervals))  # 1

intervals = [[1, 2], [1, 2], [1, 2]]
print(sol.eraseOverlapIntervals(intervals))  # 2

intervals = [[1, 2], [2, 3]]
print(sol.eraseOverlapIntervals(intervals))  # 0
