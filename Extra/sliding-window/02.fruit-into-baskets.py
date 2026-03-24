"""
FRUIT INTO BASKETS (LeetCode 904)

Problem Statement:
You have a row of fruit trees (fruits[i] = type of fruit at tree i).
With two baskets (each holds only ONE type, unlimited quantity),
pick from a contiguous sequence of trees — return the max fruits you can collect.

Equivalent to: Find the longest subarray with at most 2 distinct values.

Example 1:
Input:  fruits = [1, 2, 1]
Output: 3
Explanation: Pick all three — basket1=type1, basket2=type2.

Example 2:
Input:  fruits = [1, 2, 3, 2, 2]
Output: 4
Explanation: Start at index 1 → [2, 3, 2, 2] — basket1=type2, basket2=type3.

Constraints:
- 1 <= fruits.length <= 10^5
- 0 <= fruits[i] < fruits.length
"""

from collections import defaultdict


# ==============================================================================
# APPROACH 1: BRUTE FORCE
# ==============================================================================
# Check every possible starting point and extend right while at most 2 types.
# Time: O(n^2) | Space: O(1) (basket holds at most 2 keys)

class SolutionBrute:
    def totalFruit(self, fruits):
        max_fruits = 0

        for start in range(len(fruits)):
            basket = {}             # fruit_type -> count in current window

            for end in range(start, len(fruits)):
                basket[fruits[end]] = basket.get(fruits[end], 0) + 1

                if len(basket) > 2:  # third type found — window invalid
                    break

                max_fruits = max(max_fruits, end - start + 1)

        return max_fruits


# ==============================================================================
# APPROACH 2: SLIDING WINDOW WITH HASHMAP (BETTER)
# ==============================================================================
# Maintain window [left, right] with at most 2 distinct fruit types.
# When a 3rd type enters, shrink from the left until window is valid again.
# Time: O(n) | Space: O(1) — basket holds at most 3 keys momentarily

class SolutionSliding:
    def totalFruit(self, fruits):
        basket     = defaultdict(int)  # fruit_type -> count in current window
        left       = 0
        max_fruits = 0

        for right in range(len(fruits)):
            basket[fruits[right]] += 1          # add fruit to right of window

            while len(basket) > 2:              # 3rd type entered — shrink left
                basket[fruits[left]] -= 1
                if basket[fruits[left]] == 0:
                    del basket[fruits[left]]    # remove type entirely when count hits 0
                left += 1

            max_fruits = max(max_fruits, right - left + 1)

        return max_fruits


# ==============================================================================
# APPROACH 3: OPTIMAL — O(1) SPACE (NO HASHMAP)
# ==============================================================================
# Instead of a map, track just the last two fruit types and the streak of the
# most recent one. When a 3rd type appears, the window resets to:
#   (streak of lastfruit) + 1
# because only the tail of lastfruit + the new fruit can form a valid window.
#
# Variables:
#   lastfruit       — most recently seen fruit type
#   secondlastfruit — the other active type in the window
#   lastfruitstreak — how many consecutive fruits of lastfruit are at the tail
#   currcount       — current valid window size
#
# NOTE: original code had a typo (lastfruit_streak vs lastfruitstreak) — fixed here.
# Time: O(n) | Space: O(1)

class SolutionOptimal:
    def totalFruit(self, fruits):
        maxlen          = 0
        lastfruit       = -1
        secondlastfruit = -1
        currcount       = 0
        lastfruitstreak = 0

        for fruit in fruits:
            if fruit == lastfruit or fruit == secondlastfruit:
                currcount += 1                      # fruit fits in one of the two baskets
            else:
                # 3rd type found — reset window to: streak of lastfruit + this new fruit
                currcount = lastfruitstreak + 1

            if fruit == lastfruit:
                lastfruitstreak += 1                # extend the tail streak
            else:
                lastfruitstreak = 1                 # new fruit resets the tail streak to 1
                secondlastfruit = lastfruit         # old last becomes second
                lastfruit       = fruit             # new fruit becomes last

            maxlen = max(maxlen, currcount)

        return maxlen


# ==============================================================================
# TEST CASES
# ==============================================================================
if __name__ == "__main__":
    brute   = SolutionBrute()
    sliding = SolutionSliding()
    optimal = SolutionOptimal()

    test_cases = [
        ([1, 2, 1],          3),
        ([1, 2, 3, 2, 2],    4),
        ([1, 2, 1, 2, 3],    4),
        ([3, 3, 3, 1, 2, 1, 1, 2, 3, 3, 4], 5),
        ([1],                1),
        ([1, 1, 1, 1],       4),
    ]

    for fruits, expected in test_cases:
        r1 = brute.totalFruit(fruits[:])
        r2 = sliding.totalFruit(fruits[:])
        r3 = optimal.totalFruit(fruits[:])
        status = "PASS" if r1 == expected and r2 == expected and r3 == expected else "FAIL"
        print(f"{status} fruits={fruits} -> brute={r1}, sliding={r2}, optimal={r3} (expected {expected})")
