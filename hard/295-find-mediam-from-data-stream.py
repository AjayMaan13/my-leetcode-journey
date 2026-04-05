# 295. Find Median from Data Stream
# https://leetcode.com/problems/find-median-from-data-stream/
import bisect
import heapq


# Brute Force - O(n log n) addNum, O(1) findMedian
class MedianFinderBrute:

    def __init__(self):
        self.arr = []  # stores all elements; re-sorted on every insert

    def addNum(self, num: int) -> None:
        self.arr.append(num)
        self.arr.sort()  # keep array sorted so findMedian is O(1)

    def findMedian(self) -> float:
        n = len(self.arr)
        if n % 2 == 1:
            return float(self.arr[n // 2])          # odd: exact middle element
        else:
            return (self.arr[n // 2 - 1] + self.arr[n // 2]) / 2.0  # even: avg of two middles


# Better - O(n) addNum, O(1) findMedian
class MedianFinderBisect:

    def __init__(self):
        self.arr = []

    def addNum(self, num: int) -> None:
        # binary search finds insertion point in O(log n),
        # but shifting elements still costs O(n) — faster in practice than full sort
        bisect.insort(self.arr, num)

    def findMedian(self) -> float:
        n = len(self.arr)
        if n % 2 == 1:
            return float(self.arr[n // 2])
        else:
            return (self.arr[n // 2 - 1] + self.arr[n // 2]) / 2.0


# Optimal - Two Heaps - O(log n) addNum, O(1) findMedian
class MedianFinder:
    # Invariant: left (max-heap) holds the smaller half,
    #            right (min-heap) holds the larger half.
    # Sizes are kept equal, or left has exactly one extra element.
    # This guarantees the median is always at one or both heap tops.

    def __init__(self):
        self.left = []   # max heap (negate values so heapq acts as max-heap)
        self.right = []  # min heap

    def addNum(self, num: int) -> None:
        # Step 1: push to left (max-heap side)
        heapq.heappush(self.left, -num)

        # Step 2: pop the largest from left → push to right
        # ensures every element in left <= every element in right
        heapq.heappush(self.right, -heapq.heappop(self.left))

        # Step 3: rebalance — left must never be smaller than right
        if len(self.right) > len(self.left):
            heapq.heappush(self.left, -heapq.heappop(self.right))

    def findMedian(self) -> float:
        if len(self.left) > len(self.right):
            return float(-self.left[0])              # odd total: left has the extra element
        else:
            return (-self.left[0] + self.right[0]) / 2.0  # even total: avg of both tops


# Follow-up 1: All numbers in [0, 100] - O(1) addNum, O(1) findMedian
class MedianFinderCount:
    # When input is bounded to [0, 100], use a frequency array instead of sorting.
    # The array index is the value; count[i] is how many times i has appeared.

    def __init__(self):
        self.count = [0] * 101  # indices 0–100 cover the full input range
        self.n = 0              # total elements inserted

    def addNum(self, num: int) -> None:
        self.count[num] += 1   # increment frequency bucket
        self.n += 1

    def findMedian(self) -> float:
        # mid1 and mid2 are the 1-indexed positions of the median element(s)
        # e.g. n=5 → mid1=mid2=3 (same element); n=6 → mid1=3, mid2=4
        mid1 = (self.n + 1) // 2
        mid2 = (self.n + 2) // 2

        m1 = m2 = 0
        total = 0

        # walk the frequency array in value order (inherently sorted)
        # accumulate counts until we reach each median position
        for i in range(101):
            total += self.count[i]
            if m1 == 0 and total >= mid1:
                m1 = i  # found the first median element
            if m2 == 0 and total >= mid2:
                m2 = i  # found the second median element
                break

        return (m1 + m2) / 2.0


# Follow-up 2: 99% of numbers in [0, 100] - Hybrid approach
class MedianFinderHybrid:
    # Split the number line into three regions:
    #   negatives  → max-heap (self.left)
    #   [0, 100]   → frequency count array
    #   > 100      → min-heap (self.right)
    # get_kth walks all three regions in sorted order to find any k-th element.

    def __init__(self):
        self.count = [0] * 101
        self.n = 0

        self.left = []   # max heap (store negatives) for values < 0
        self.right = []  # min heap for values > 100

    def addNum(self, num: int) -> None:
        # route each number to its region
        if 0 <= num <= 100:
            self.count[num] += 1
        elif num < 0:
            heapq.heappush(self.left, -num)  # negate so heapq works as max-heap
        else:
            heapq.heappush(self.right, num)

        self.n += 1

    def findMedian(self) -> float:
        mid1 = (self.n + 1) // 2
        mid2 = (self.n + 2) // 2

        def get_kth(k: int) -> int:
            total = 0

            # region 1: negatives, sorted ascending (smallest first)
            left_sorted = sorted([-x for x in self.left])
            for num in left_sorted:
                total += 1
                if total == k:
                    return num

            # region 2: [0, 100] via frequency array (already in value order)
            for i in range(101):
                total += self.count[i]
                if total >= k:
                    return i

            # region 3: values > 100, sorted ascending
            right_sorted = sorted(self.right)
            for num in right_sorted:
                total += 1
                if total == k:
                    return num

            return 0  # unreachable if k is valid

        return (get_kth(mid1) + get_kth(mid2)) / 2.0
