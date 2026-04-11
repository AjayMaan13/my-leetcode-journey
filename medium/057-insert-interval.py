# 57. Insert Interval
# https://leetcode.com/problems/insert-interval/
#
# You are given an array of non-overlapping intervals sorted by start time.
# Insert a new interval and merge any overlapping intervals.
# Return the resulting list of non-overlapping intervals in sorted order.
#
# Example 1:
#   Input: intervals = [[1,3],[6,9]], newInterval = [2,5]
#   Output: [[1,5],[6,9]]
#
# Example 2:
#   Input: intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]
#   Output: [[1,2],[3,10],[12,16]]
#   Explanation: [4,8] overlaps with [3,5], [6,7], [8,10] — all merged into [3,10].
#
# Constraints:
#   0 <= intervals.length <= 10^4
#   intervals is sorted by start in ascending order
#   0 <= start <= end <= 10^5


# Greedy (Three-Phase Scan) - O(n) time, O(n) space
#
# The array has three regions relative to newInterval:
#   Phase 1 — intervals that end BEFORE newInterval starts: no overlap, add as-is.
#             Condition: intervals[i][1] < newInterval[0]
#
#   Phase 2 — intervals that OVERLAP with newInterval: merge them all into newInterval
#             by expanding its start/end to cover the union.
#             Condition: intervals[i][0] <= newInterval[1]
#             (interval starts before or at newInterval's end)
#
#   Phase 3 — intervals that start AFTER newInterval ends: no overlap, add as-is.
#
# After phase 2, append the (possibly expanded) newInterval, then the rest.
class Solution:
    def insert(self, intervals, newInterval):
        result = []
        i = 0
        n = len(intervals)

        # Phase 1: add all intervals that end before newInterval starts
        while i < n and intervals[i][1] < newInterval[0]:
            result.append(intervals[i])
            i += 1

        # Phase 2: merge all intervals that overlap with newInterval
        # an interval overlaps if it starts before or when newInterval ends
        while i < n and intervals[i][0] <= newInterval[1]:
            newInterval[0] = min(newInterval[0], intervals[i][0])  # expand left if needed
            newInterval[1] = max(newInterval[1], intervals[i][1])  # expand right if needed
            i += 1

        result.append(newInterval)  # add the fully merged interval

        # Phase 3: add all remaining intervals (they start after newInterval ends)
        while i < n:
            result.append(intervals[i])
            i += 1

        return result


intervals = [[1, 3], [6, 9]]
newInterval = [2, 5]
sol = Solution()
print(sol.insert(intervals, newInterval))  # [[1,5],[6,9]]

intervals = [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]]
newInterval = [4, 8]
print(sol.insert(intervals, newInterval))  # [[1,2],[3,10],[12,16]]
