"""
AGGRESSIVE COWS

Problem Statement:
You are given an array 'arr' of size 'n' which denotes the position of stalls.
You are also given an integer 'k' which denotes the number of aggressive cows.
You are given the task of assigning stalls to 'k' cows such that the minimum 
distance between any two of them is the maximum possible.
Find the maximum possible minimum distance.

Example 1:
Input: N = 6, k = 4, arr[] = {0,3,4,7,10,9}
Output: 3
Explanation: The maximum possible minimum distance between any two cows will be 3 
when 4 cows are placed at positions {0, 3, 7, 10}. Here the distances between 
cows are 3, 4, and 3 respectively.

Example 2:
Input: N = 5, k = 2, arr[] = {4,2,1,3,6}
Output: 5
Explanation: The maximum possible minimum distance will be 5 when 2 cows are 
placed at positions {1, 6}.
"""


# ==============================================================================
# APPROACH 1: BRUTE FORCE
# ==============================================================================
# Time Complexity: O(N * (max - min))
# Space Complexity: O(1)

def canWePlace(stalls, cows, dist):
    """Check if we can place all cows with minimum distance dist"""
    count = 1  # Place first cow at first stall
    last = stalls[0]
    
    for i in range(1, len(stalls)):
        if stalls[i] - last >= dist:
            count += 1  # Place cow here
            last = stalls[i]
        if count >= cows:
            return True
    return False


def aggressiveCows_bruteforce(stalls, cows):
    """Find maximum possible minimum distance using brute force"""
    stalls.sort()
    
    # Try every distance from max to 1
    for dist in range(stalls[-1] - stalls[0], 0, -1):
        if canWePlace(stalls, cows, dist):
            return dist
    return 1


# ==============================================================================
# APPROACH 2: BINARY SEARCH (OPTIMAL)
# ==============================================================================
# Time Complexity: O(N log N) + O(N * log(max - min))
# Space Complexity: O(1)

def canPlace(stalls, cows, d):
    """Check if cows can be placed with distance d"""
    # Place first cow at first stall
    count = 1
    lastPos = stalls[0]

    # Loop through stalls
    for i in range(1, len(stalls)):
        # If stall is at least d away from last placed cow
        if stalls[i] - lastPos >= d:
            # Place cow here
            count += 1
            # Update last position
            lastPos = stalls[i]
        # If all cows placed
        if count >= cows:
            return True
    # Could not place all cows
    return False


def aggressiveCows(stalls, cows):
    """Find maximum possible minimum distance using binary search"""
    # Sort stalls
    stalls.sort()

    # Define search space
    low = 1
    high = stalls[-1] - stalls[0]
    ans = 0

    # Binary search
    while low <= high:
        # Find mid distance
        mid = (low + high) // 2

        # If placement possible
        if canPlace(stalls, cows, mid):
            # Store answer
            ans = mid
            # Try larger distance
            low = mid + 1
        else:
            # Try smaller distance
            high = mid - 1

    # Return result
    return ans
