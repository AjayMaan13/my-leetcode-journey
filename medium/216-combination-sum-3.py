"""
LeetCode 216. Combination Sum III  |  Medium

Problem Statement:
    Find all valid combinations of k numbers that sum to n such that:
      - Only numbers 1 through 9 are used
      - Each number is used AT MOST ONCE
    Return all unique combinations (no duplicates).

Examples:
    k=3, n=7   →  [[1,2,4]]
    k=3, n=9   →  [[1,2,6],[1,3,5],[2,3,4]]
    k=4, n=1   →  []  (smallest 4-number sum = 1+2+3+4 = 10 > 1)

How this fits the pattern:
    ┌─────────────────┬────────────┬────────────┬──────────────────────────┐
    │ Problem         │ Input      │ Reuse      │ Extra constraint         │
    ├─────────────────┼────────────┼────────────┼──────────────────────────┤
    │ Comb. Sum I     │ any array  │ Yes        │ None                     │
    │ Comb. Sum II    │ has dupes  │ No         │ Skip duplicate values    │
    │ Comb. Sum III   │ 1..9 only  │ No         │ Exactly k numbers        │
    │ Subsets         │ unique     │ No         │ All subsets              │
    └─────────────────┴────────────┴────────────┴──────────────────────────┘

    Comb. Sum III = Comb. Sum II (no dupes in 1..9, no reuse) + length == k check.
"""


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1: YOUR V1 — explicit nums array [1..9]
# Time  : O(C(9,k))  — at most C(9,k) valid combinations (9 choose k)
# Space : O(k)       — recursion depth = k (we stop once len == k)
#
# Uses an explicit nums=[1..9] list and loops over it.
# Logic is correct but has a subtle issue:
#   The pruning `if index == 9 or nums[index] > remaining: return`
#   is OUTSIDE the loop — it only checks the FIRST element of the range,
#   not each element inside the loop. The loop itself has no break.
#   This means the loop still iterates even after elements exceed remaining.
#
#   Example: remaining=3, loop reaches nums[i]=7 → still enters the call,
#   only to immediately return inside. This is redundant work.
#   Fix: add `if nums[i] > remaining: break` inside the loop (done in V2).
#
# Also: `if k > n: return []` at the top is a weak early exit.
#   A tighter guard is k*(k+1)//2 > n (min possible sum of k distinct numbers).
# ─────────────────────────────────────────────────────────────────────────────
def combinationSum3_v1(k: int, n: int) -> list:
    # Weak early exit: if k > n, even [1,2,...,k] won't work since min sum = k*(k+1)//2
    if k > n:
        return []

    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]   # fixed digit pool

    def solve(index: int, currList: list, remaining: int, result: list) -> None:
        # Valid combination: sum == n AND exactly k numbers picked
        if remaining == 0 and len(currList) == k:
            result.append(currList[:])

        # Pruning: end of array OR current element already exceeds remaining
        # Note: this checks only nums[index] (the loop's first element), not each i
        if index == 9 or nums[index] > remaining:
            return

        for i in range(index, len(nums)):
            currList.append(nums[i])
            solve(i + 1, currList, remaining - nums[i], result)
            currList.pop()   # backtrack

    result = []
    solve(0, [], n, result)
    return result


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: YOUR V2 — range(start, 10) with strong pruning ← preferred
# Time  : O(C(9,k))
# Space : O(k)
#
# Cleaner version:
#   1. Iterates range(start, 10) directly — no need for an explicit nums list
#   2. Strong pruning INSIDE the loop: `if num > remaining: break`
#      Since we iterate 1→9 in order, once num > remaining, all further nums
#      are also too large → break saves unnecessary recursive calls
#   3. `if len(path) > k: return` — stops as soon as we've picked too many
#
# ── TWO-CONDITION BASE CASE ──────────────────────────────────────────────────
# `remaining == 0 AND len(path) == k` must BOTH be true:
#   - remaining == 0 alone: correct sum but wrong count (e.g. [7] for k=3,n=7)
#   - len(path) == k alone: right count but wrong sum
#   Both together: exactly k numbers that sum to n ✓
#
# ── PRUNING INTERACTION ───────────────────────────────────────────────────────
# `if remaining < 0 or len(path) > k: return`  at the TOP
#   → kills any path that overshot sum OR picked too many numbers
# `if num > remaining: break`  INSIDE the loop
#   → kills the loop early when remaining digits are all too large
#
# Both work together: the top guard handles cases where we've already
# overshot; the loop break prevents us from even trying nums that are too big.
# ─────────────────────────────────────────────────────────────────────────────
def combinationSum3_v2(k: int, n: int) -> list:
    result = []

    def backtrack(start: int, remaining: int, path: list) -> None:
        # ── PRUNING: exit early if path is already invalid ────────────────────
        if remaining < 0 or len(path) > k:
            return

        # ── BASE CASE: valid combination found ───────────────────────────────
        if remaining == 0 and len(path) == k:
            result.append(path[:])
            return

        for num in range(start, 10):   # digits 1..9, no explicit array needed
            # ── LOOP PRUNING: sorted range, so once num > remaining, stop ─────
            # All subsequent nums are larger → none can contribute to a valid sum
            if num > remaining:
                break

            path.append(num)
            backtrack(num + 1, remaining - num, path)   # num+1: no reuse
            path.pop()   # backtrack

    backtrack(1, n, [])
    return result


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 3: TIGHTER EARLY EXIT + BOTH PRUNINGS
# Adds one more guard at the entry: k*(k+1)//2 > n
#   The minimum possible sum using k distinct numbers from 1..9 is 1+2+...+k = k(k+1)/2
#   If even the minimum exceeds n, there's no solution at all → return early.
#   Similarly, max sum = (9+8+...+(10-k)) = k*(19-k)//2 — if n exceeds this, no solution.
# ─────────────────────────────────────────────────────────────────────────────
def combinationSum3_v3(k: int, n: int) -> list:
    # Min sum of k distinct digits from 1..9 = 1+2+...+k = k*(k+1)//2
    min_sum = k * (k + 1) // 2
    # Max sum of k distinct digits from 1..9 = 9+8+...+(10-k) = k*(19-k)//2
    max_sum = k * (19 - k) // 2

    if n < min_sum or n > max_sum:
        return []   # mathematically impossible → skip all recursion

    result = []

    def backtrack(start: int, remaining: int, path: list) -> None:
        if remaining == 0 and len(path) == k:
            result.append(path[:])
            return
        if len(path) == k:   # used k numbers but sum not reached
            return

        for num in range(start, 10):
            if num > remaining:
                break
            path.append(num)
            backtrack(num + 1, remaining - num, path)
            path.pop()

    backtrack(1, n, [])
    return result

