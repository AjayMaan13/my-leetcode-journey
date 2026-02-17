"""
HARD: MINIMISE MAXIMUM DISTANCE BETWEEN GAS STATIONS

Problem Statement:
You are given a sorted array 'arr' of length 'n', which contains positive integer 
positions of 'n' gas stations on the X-axis. You are also given an integer 'k'. 
You have to place 'k' new gas stations on the X-axis. You can place them anywhere 
on the non-negative side of the X-axis, even on non-integer positions.

Let 'dist' be the maximum value of the distance between adjacent gas stations 
after adding k new gas stations. Find the minimum value of 'dist'.

Example 1:
Input: N = 5, arr[] = {1,2,3,4,5}, k = 4
Output: 0.5
Explanation: One possible placement is {1,1.5,2,2.5,3,3.5,4,4.5,5}.
The maximum difference between adjacent stations is 0.5.

Example 2:
Input: N = 10, arr[] = {1,2,3,4,5,6,7,8,9,10}, k = 1
Output: 1
Explanation: One possible placement keeps max distance at 1.
"""

import heapq


# ==============================================================================
# APPROACH 1: BRUTE FORCE
# ==============================================================================
# Time Complexity: O(k * n) - for each of k stations, scan all n-1 sections
# Space Complexity: O(n) - for the howMany array

def minimise_max_distance_brute(arr, k):
    """
    Place gas stations one at a time, always inserting into the largest gap.

    Key Idea: For each of the k stations, find the section with the maximum
    current distance and place the new station there to reduce that gap.
    """
    n = len(arr)

    # Track how many stations are placed in each section between arr[i] and arr[i+1]
    howMany = [0] * (n - 1)

    # Place k gas stations one at a time
    for _ in range(k):
        max_dist = -1
        max_idx = -1

        # Find the section with the current maximum distance
        for i in range(n - 1):
            # If we've added howMany[i] stations in section i,
            # the section is split into (howMany[i] + 1) equal parts
            section_dist = (arr[i + 1] - arr[i]) / (howMany[i] + 1)

            if section_dist > max_dist:
                max_dist = section_dist
                max_idx = i

        # Place new station in the section with largest distance
        howMany[max_idx] += 1

    # After placing all k stations, compute the actual maximum distance
    max_dist = -1
    for i in range(n - 1):
        # Each section is split into (howMany[i] + 1) equal parts
        section_dist = (arr[i + 1] - arr[i]) / (howMany[i] + 1)
        max_dist = max(max_dist, section_dist)

    return max_dist


# ==============================================================================
# APPROACH 2: BETTER APPROACH (PRIORITY QUEUE / MAX HEAP)
# ==============================================================================
# Time Complexity: O(n log n + k log n) - heap operations
# Space Complexity: O(n) - for heap and howMany array

def minimise_max_distance_heap(arr, k):
    """
    Use a max-heap to always find the largest section in O(log n) time.

    Key Improvement over brute force: Instead of scanning all sections every
    time to find the max, we use a max-heap to get it in O(log n).
    """
    n = len(arr)

    # Track how many stations placed in each section
    howMany = [0] * (n - 1)

    # Max heap: store (-distance, section_index)
    # Python has min-heap, so negate distance to simulate max-heap
    heap = []
    for i in range(n - 1):
        # Push negative distance (to simulate max-heap) and section index
        heapq.heappush(heap, (-(arr[i + 1] - arr[i]), i))

    # Place k gas stations one at a time
    for _ in range(k):
        # Get the section with maximum current distance
        dist, sec_idx = heapq.heappop(heap)
        dist = -dist  # Convert back to positive

        # Place station in this section
        howMany[sec_idx] += 1

        # Recalculate distance for this section after placing new station
        initial_section_length = arr[sec_idx + 1] - arr[sec_idx]
        new_dist = initial_section_length / (howMany[sec_idx] + 1)

        # Push updated distance back into heap
        heapq.heappush(heap, (-new_dist, sec_idx))

    # The top of heap is the maximum distance after placing all k stations
    return -heap[0][0]


# ==============================================================================
# APPROACH 3: BINARY SEARCH (OPTIMAL)
# ==============================================================================
# Time Complexity: O(n * log((max_dist) / 1e-6)) - binary search iterations
# Space Complexity: O(1)
#
# Key Insight: Binary search on the answer (distance) itself.
# If a distance 'd' requires more than k stations, it's too small.
# If it requires k or fewer, it might be our answer — but try smaller.

def number_of_gas_stations_required(dist, arr):
    """
    Calculate how many extra gas stations are needed if the maximum
    allowed distance between any two adjacent stations is 'dist'.

    For each section of length L, we can fit floor(L / dist) stations,
    but if L is exactly divisible by dist, we subtract 1 to avoid
    placing a station right on top of an existing one.
    """
    count = 0
    n = len(arr)

    for i in range(1, n):
        # How many stations fit in this section at max distance 'dist'?
        number_in_between = int((arr[i] - arr[i - 1]) / dist)

        # If section length divides evenly, we overcounted by 1
        if (arr[i] - arr[i - 1]) == dist * number_in_between:
            number_in_between -= 1

        count += number_in_between

    return count


def minimise_max_distance(arr, k):
    """
    Binary search on the answer space (possible distance values).

    Search between 0 (impossible minimum) and max gap (worst case).
    Narrow down until precision of 1e-6 is achieved.
    """
    n = len(arr)

    # Search space: 0 to the largest gap between existing stations
    low = 0
    high = max(arr[i + 1] - arr[i] for i in range(n - 1))

    # Stop when low and high are within 1e-6 of each other
    diff = 1e-6

    while high - low > diff:
        mid = (low + high) / 2.0  # Try this as the maximum allowed distance

        # How many stations do we need with this max distance?
        count = number_of_gas_stations_required(mid, arr)

        if count > k:
            # Need more than k stations — distance is too small, increase it
            low = mid
        else:
            # k or fewer stations needed — valid! Try reducing further
            high = mid

    # high and low are within 1e-6, either works as the answer
    return high
