"""
LeetCode 40. Combination Sum II  |  Medium

Problem Statement:
    Given a collection of candidate numbers (may contain DUPLICATES) and a
    target number, find all UNIQUE combinations where numbers sum to target.
    Each number may only be used ONCE.

    Key differences from Combination Sum I:
      ┌─────────────────────┬──────────────────┬─────────────────────────┐
      │                     │ Combination Sum  │ Combination Sum II      │
      ├─────────────────────┼──────────────────┼─────────────────────────┤
      │ Duplicates in input │ No               │ Yes                     │
      │ Reuse same element  │ Yes (unlimited)  │ No (once each)          │
      │ Duplicate results   │ Not possible     │ Must be prevented       │
      │ Move index on pick  │ Stay at i        │ Move to i+1             │
      └─────────────────────┴──────────────────┴─────────────────────────┘

Examples:
    candidates=[10,1,2,7,6,1,5], target=8
      sorted → [1,1,2,5,6,7,10]
      output → [[1,1,6],[1,2,5],[1,7],[2,6]]

    candidates=[2,5,2,1,2], target=5
      sorted → [1,2,2,2,5]
      output → [[1,2,2],[5]]
"""


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1: YOUR V1 — Include/Exclude with `nums not in result` check
# Time  : O(2^n * n)  — 2^n subsets explored, plus O(n) for the "in result" check
# Space : O(n)        — recursion depth = n
#
# Correctly solves the problem but uses a SLOW deduplication strategy.
# `nums not in result` does a LINEAR SCAN of the entire result list
# every time we find a valid combination — very expensive when there are
# many valid combinations.
#
# How it works:
#   - At every index, make 2 binary choices: INCLUDE or EXCLUDE candidates[index]
#   - When the end of the array is reached, if remaining==0 AND the combination
#     isn't already in the result, add it.
#
# The sort ensures that duplicate combinations (e.g. [1,7] appearing twice
# from two different '1's) always appear in the same order, so the
# `nums not in result` check can correctly detect them.
# Without sorting, [1,7] and [1,7] would still match, but [7,1] and [1,7]
# would NOT — so the sort is load-bearing here.
# ─────────────────────────────────────────────────────────────────────────────
def combinationSum2_v1(candidates: list, target: int) -> list:
    if not candidates or target < 0:
        return []

    candidates.sort()   # required for dedup check to work correctly

    def solve(index, nums, remaining, result):
        # Base case: processed all candidates
        if index == len(candidates):
            # Only add if sum matches AND we haven't seen this combination before
            # NOTE: this `not in` check is O(n * |result|) — the bottleneck
            if remaining == 0 and nums not in result:
                result.append(nums[:])
            return

        # Choice 1: INCLUDE candidates[index]
        nums.append(candidates[index])
        solve(index + 1, nums, remaining - candidates[index], result)
        nums.pop()   # backtrack

        # Choice 2: EXCLUDE candidates[index]
        solve(index + 1, nums, remaining, result)

    result = []
    solve(0, [], target, result)
    return result


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: YOUR V2 — Loop-based with smart SKIP (optimal) ← use this one
# Time  : O(2^n)   — pruning eliminates duplicate branches before they recurse
# Space : O(n)     — recursion depth = n
#
# This avoids duplicate results WITHOUT any post-hoc checking.
# Instead, duplicates are PREVENTED at the point of branching.
#
# Three changes from V1:
#   1. Loop over candidates[index:] instead of binary include/exclude
#      → naturally handles "pick one and move to next" for each candidate
#
#   2. SKIP duplicates at the same recursion level (the key dedup logic):
#      `if i > index and candidates[i] == candidates[i-1]: continue`
#
#   3. EARLY TERMINATION via break:
#      `if candidates[i] > remaining: break`
#      → since array is sorted, all subsequent candidates are also too large
#
# ── HOW THE SKIP LOGIC WORKS ─────────────────────────────────────────────────
# After sorting, duplicate values sit next to each other.
# e.g. sorted [1,1,2,5,6,7,10] → two 1s at indices 0 and 1
#
# When we're at a given recursion level (same `index`), we're choosing
# "which candidate to pick NEXT for this position in the combination."
# If we pick candidates[0]=1 first, explore all combos starting with that 1,
# then come back and try candidates[1]=1 — we'd generate the EXACT SAME
# combos again (since both 1s are identical values).
#
# The skip prevents re-picking the same VALUE at the same LEVEL:
#
#   i > index   → ensures we're looking at a non-first element of the loop
#                 (i == index is always allowed — it's the first pick at this level)
#   candidates[i] == candidates[i-1]  → same value as the one we just tried
#
# Both conditions together: "we've ALREADY explored all combos starting with
# this value at this recursion level, so skip this duplicate."
#
# WITHOUT the skip (using V1 approach on input [1,1,2,5,6,7,10], target=8):
#
#   Level 0 picks candidates[0]=1:
#     → explores [1,1,6], [1,2,5], [1,7]  ✓
#   Level 0 picks candidates[1]=1:  ← same value!
#     → explores [1,1,6], [1,2,5], [1,7]  ✗ duplicates!
#
# WITH the skip (i=1 > index=0 AND candidates[1]==candidates[0]) → skip!
#
# ── WHY i > index AND NOT JUST i > 0 ────────────────────────────────────────
# The condition is `i > index`, NOT `i > 0`.
#
# Consider [1,1,2,5,6,7,10], target=8, and we're inside a recursive call
# with index=1 (we already picked candidates[0]=1 in an outer level):
#
#   Outer call picked candidates[0]=1, so now we're at solve(index=1, [1], 7)
#   Inner loop starts at i=1  (i == index → allowed, first pick at this level)
#     → picks candidates[1]=1 → [1,1], remaining=6
#     → continue recursing → finds [1,1,6] ✓
#   Inner loop moves to i=2 (candidates[2]=2)
#     → `i > index` is True (2>1) BUT candidates[2]=2 ≠ candidates[1]=1
#     → NOT skipped → picks 2 → [1,2], remaining=5 → finds [1,2,5] ✓
#
# If we used `i > 0` instead of `i > index`:
#   At solve(index=1, [1], 7), i=1 → `i > 0` is True AND candidates[1]==candidates[0]
#   → we'd SKIP picking the second 1 entirely!
#   → [1,1,6] would NEVER be found ← WRONG
#
# So `i > index` lets us pick the FIRST occurrence of a value at each recursion
# level (i == index) while blocking REPEAT occurrences of that same value
# at the same level (i > index and value matches previous).
# ─────────────────────────────────────────────────────────────────────────────
def combinationSum2_v2(candidates: list, target: int) -> list:
    if not candidates or target < 0:
        return []

    candidates.sort()   # groups duplicates together AND enables break-pruning

    def solve(index: int, nums: list, remaining: int, result: list) -> None:
        # Base case: valid combination found
        if remaining == 0:
            result.append(nums[:])
            return

        # Stop if array exhausted or we've already overshot
        if index == len(candidates) or remaining < 0:
            return

        for i in range(index, len(candidates)):

            # ── SKIP DUPLICATES AT SAME RECURSION LEVEL ──────────────────────
            # If i > index: we're NOT on the first iteration of this loop level.
            # If candidates[i] == candidates[i-1]: same value as the previous pick.
            # Together: we already explored ALL combos using this value at this level.
            # Picking it again here would produce identical combinations → skip.
            if i > index and candidates[i] == candidates[i - 1]:
                continue

            # ── EARLY TERMINATION (PRUNING) ───────────────────────────────────
            # Array is sorted → if current candidate exceeds remaining sum,
            # all subsequent candidates are also too large → no point continuing.
            if candidates[i] > remaining:
                break

            nums.append(candidates[i])                       # choose
            solve(i + 1, nums, remaining - candidates[i], result)   # move to i+1 (no reuse)
            nums.pop()                                       # backtrack (undo)

    result = []
    solve(0, [], target, result)
    return result
