"""
846. Hand of Straights
https://leetcode.com/problems/hand-of-straights/
Difficulty: Medium
Topics: Array, Hash Table, Greedy, Sorting

Problem:
    Given an array `hand` and integer `groupSize`, return True if the cards
    can be rearranged into groups of `groupSize` consecutive integers.

Examples:
    hand = [1,2,3,6,2,3,4,7,8], groupSize = 3  →  True   ([1,2,3],[2,3,4],[6,7,8])
    hand = [1,2,3,4,5],          groupSize = 4  →  False

Constraints:
    1 <= hand.length <= 10^4
    0 <= hand[i] <= 10^9
    1 <= groupSize <= hand.length
"""

import heapq
from collections import Counter


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1: BRUTE FORCE — Sort + Linear Scan
# ─────────────────────────────────────────────────────────────────────────────
# Idea:
#   Sort the cards. Greedily try to start a new group from the smallest
#   remaining card. For each group, look for the next `groupSize - 1`
#   consecutive values and remove them.
#
#   Use a list and mark used cards (or remove them). To avoid O(N^2) removals,
#   we can use a Counter and always start from the current minimum.
#
# Time:  O(N log N)  — sort dominates
# Space: O(N)        — sorted copy + counter
# ─────────────────────────────────────────────────────────────────────────────

def isNStraightHand_brute(hand, groupSize):
    if len(hand) % groupSize != 0:
        return False

    hand_sorted = sorted(hand)
    count = Counter(hand_sorted)

    for card in hand_sorted:
        if count[card] == 0:       # already consumed
            continue
        # Try to build a group starting at `card`
        for i in range(groupSize):
            if count[card + i] == 0:
                return False
            count[card + i] -= 1

    return True


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: YOUR SOLUTION — Two Heaps (Analysis + Bugs)
# ─────────────────────────────────────────────────────────────────────────────
# Your original idea: separate "unique" cards into one heap and "duplicate"
# cards into another, then pull from the smaller minimum to form groups.
#
# The core intuition (always process the smallest available card first) is
# actually correct — that's what the optimal solution does too. But there are
# several structural bugs here:
#
# BUG 1 — Two-heap model can't represent frequency ≥ 3:
#   `if cur in heap` is a raw list membership check (O(N), not O(log N)).
#   More critically: the model only has two buckets — "heap" (first copy) and
#   "dupHeap" (all subsequent copies). A card appearing 3+ times puts all
#   extra copies in dupHeap together, losing track of how many groups need it.
#   Example: hand=[1,1,1,2,2,2,3,3,3], groupSize=3
#     heap=[1,2,3], dupHeap=[1,1,2,2,3,3]
#   This is OK for 3 copies, but the downstream logic can't correctly pair
#   the right copies into groups.
#
# BUG 2 — First group is hardcoded to pop from `heap` only:
#   The first loop pops exactly `groupSize` elements from `heap`, assuming
#   they form the first valid group. But `heap` only holds the first copy
#   of each card. If the first group's cards happen to include a card whose
#   first occurrence is in dupHeap (impossible by construction, but the
#   whole model breaks for multi-group scenarios).
#
# BUG 3 — `val` is never appended to `cur` inside the while loop:
#   After the first group is handled, `cur` is reset to [].
#   Inside the while loop: val is popped, the `cur and val != cur[-1]+1`
#   check runs — but val is NEVER appended to cur afterward.
#   So cur is perpetually empty, the condition is always False (short-circuit),
#   and len(cur) == groupSize is never True. The whole while loop just drains
#   both heaps without any real validation.
#
# BUG 4 — Group boundary reset happens before appending:
#   Even if BUG 3 were fixed by appending val, the reset `cur = []` fires
#   BEFORE val is appended in the next iteration, so the first card of every
#   new group is silently dropped.
#
# The fix requires rethinking the data structure entirely — see Approach 3.
#
# ─── Your original code, preserved exactly (returns wrong answers) ───────────

def isNStraightHand_yours_original(hand, groupSize):
    """Your original submission — kept for reference. Contains the bugs above."""
    if len(hand) % groupSize != 0:
        return False

    heap = []
    dupHeap = []

    for i in range(len(hand)):
        cur = hand[i]
        if cur in heap:                         # BUG 1: O(N) list scan; 2-bucket model
            heapq.heappush(dupHeap, cur)
        else:
            heapq.heappush(heap, cur)

    cur = []
    for i in range(groupSize):
        val = heapq.heappop(heap)
        if cur:
            if val == cur[-1] + 1:
                cur.append(val)
            else:
                return False
        else:
            cur.append(val)

    cur = []

    while heap or dupHeap:
        val = 0
        if heap:
            if dupHeap:
                if heap[0] < dupHeap[0]:
                    val = heapq.heappop(heap)
                else:
                    val = heapq.heappop(dupHeap)
            else:
                val = heapq.heappop(heap)
        else:
            val = heapq.heappop(dupHeap)

        if cur and val != cur[-1] + 1:          # BUG 3: val never appended below
            return False

        if len(cur) == groupSize:
            cur = []
        # ← val never appended to cur (BUG 3)
        # ← even if it were, reset fires before next append (BUG 4)

    if heap or dupHeap:
        return False
    return True


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 3: OPTIMAL — Min-Heap + Counter (your idea, fixed)
# ─────────────────────────────────────────────────────────────────────────────
# Idea:
#   Replace the broken two-heap model with a Counter (tracks exact frequency
#   of each card) + a min-heap of unique card values (to always find the
#   current smallest card efficiently).
#
#   Algorithm:
#     1. Build Counter of all cards.
#     2. Push all unique values into a min-heap.
#     3. While the heap is non-empty:
#        a. Peek at the minimum value (don't pop yet — it might have been
#           fully consumed already; skip those).
#        b. Pop the minimum. Try to form a group starting here:
#           for each of the next `groupSize` consecutive values,
#           decrement its count. If any is missing → False.
#        c. Values whose count reaches 0 are naturally skipped next iteration.
#
#   Why always start from the minimum?
#     The smallest remaining card can ONLY be the start of a group —
#     there's no smaller card to pair it with. If we can't form a complete
#     consecutive group starting from it, the answer is False.
#
# Time:  O(N log N)  — building heap + N group-formation steps each O(groupSize)
# Space: O(N)        — counter + heap
# ─────────────────────────────────────────────────────────────────────────────

def isNStraightHand_optimal(hand, groupSize):
    if len(hand) % groupSize != 0:
        return False

    count = Counter(hand)                      # {card_value: frequency}
    min_heap = list(count.keys())
    heapq.heapify(min_heap)                    # min-heap of unique card values

    while min_heap:
        start = min_heap[0]                    # peek — smallest remaining card

        # Skip values that have been fully consumed
        if count[start] == 0:
            heapq.heappop(min_heap)
            continue

        # Try to form a group of `groupSize` consecutive cards starting at `start`
        for i in range(groupSize):
            card = start + i
            if count[card] == 0:
                return False                   # consecutive card missing
            count[card] -= 1

    return True


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 4: CLEANEST OPTIMAL — Sorted Keys + Counter
# ─────────────────────────────────────────────────────────────────────────────
# Same greedy logic as Approach 3 but without a heap — just iterate over
# sorted unique keys. Works because we process cards in ascending order anyway.
#
# This is the most readable version and what most top solutions look like.
#
# Time:  O(N log N)  — sorting unique keys
# Space: O(N)        — counter
# ─────────────────────────────────────────────────────────────────────────────

def isNStraightHand_sorted(hand, groupSize):
    if len(hand) % groupSize != 0:
        return False

    count = Counter(hand)

    for card in sorted(count):                 # iterate unique values in order
        freq = count[card]
        if freq == 0:
            continue
        # This card must be the start of `freq` groups
        for i in range(groupSize):
            count[card + i] -= freq            # consume `freq` copies of each card
            if count[card + i] < 0:
                return False

    return True


# ─────────────────────────────────────────────────────────────────────────────
# TESTS
# ─────────────────────────────────────────────────────────────────────────────

def run_tests():
    test_cases = [
        # (hand, groupSize, expected)
        ([1,2,3,6,2,3,4,7,8],       3, True),   # [1,2,3],[2,3,4],[6,7,8]
        ([1,2,3,4,5],                4, False),  # 5 cards, groupSize=4: 5%4≠0
        ([1,2,3],                    3, True),   # single group
        ([1,1,2,2,3,3],              3, True),   # [1,2,3],[1,2,3]
        ([1,2,3,4],                  2, True),   # [1,2],[3,4]
        ([1,2,3,4],                  3, False),  # 4%3≠0
        ([1,1,1,2,2,2,3,3,3],        3, True),   # [1,2,3],[1,2,3],[1,2,3]
        ([1,2,3,4,5,6,7,8,9],        3, True),   # [1,2,3],[4,5,6],[7,8,9]
        ([0,0],                      1, True),   # groupSize=1, always True if N%1=0
        ([1,2,3,4,5,6],              4, False),  # can't make consecutive groups of 4
        ([1,2,3,3,4,5],              3, True),   # [1,2,3],[3,4,5]
        ([9,8,7,6,5,4,3,2,1,0],      5, True),   # [0,1,2,3,4],[5,6,7,8,9]
    ]

    # Only test approaches that are correct (exclude the buggy original)
    approaches = [
        ("Brute Force (Sort+Counter)", isNStraightHand_brute),
        ("Optimal (Heap+Counter)",     isNStraightHand_optimal),
        ("Optimal (Sorted Keys)",      isNStraightHand_sorted),
    ]

    all_passed = True
    for hand, groupSize, expected in test_cases:
        for name, fn in approaches:
            result = fn(hand[:], groupSize)   # pass a copy — brute modifies nothing but be safe
            status = "✓" if result == expected else "✗"
            if result != expected:
                all_passed = False
                print(f"  {status} FAIL | {name} | hand={hand}, g={groupSize} | got {result}, expected {expected}")

    if all_passed:
        print("All tests passed ✓")
    else:
        print("\nSome tests FAILED — see above.")


if __name__ == "__main__":
    run_tests()


# ─────────────────────────────────────────────────────────────────────────────
# COMPLEXITY SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
#
# Approach                  Time          Space   Notes
# ──────────────────────────────────────────────────────────────────────────────
# Brute (Sort + Counter)    O(N log N)    O(N)    Simple, readable
# Optimal (Heap + Counter)  O(N log N)    O(N)    Your idea — fixed
# Optimal (Sorted Keys)     O(N log N)    O(N)    Cleanest; top solution pattern
#
# All three are the same asymptotic complexity. The "Sorted Keys" approach is
# the interview gold standard — Counter + sorted() + one greedy loop.
#
# ─────────────────────────────────────────────────────────────────────────────
# README — Heap Section Update
# ─────────────────────────────────────────────────────────────────────────────
#
# | # | Problem | Difficulty | Approach |
# |---|---------|------------|----------|
# | 846 | Hand of Straights | Medium | Greedy from smallest card; Counter tracks
# |     |                   |        | frequency; min-heap or sorted keys to
# |     |                   |        | always find current minimum in O(log N) |