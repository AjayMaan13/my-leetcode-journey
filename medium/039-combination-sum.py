"""
LeetCode 39. Combination Sum  |  Medium

Problem Statement:
    Given an array of DISTINCT integers `candidates` and a target integer,
    return all unique combinations where the chosen numbers sum to target.
    The SAME number may be chosen UNLIMITED times.

Examples:
    candidates=[2,3,6,7], target=7  →  [[2,2,3],[7]]
    candidates=[2,3,5],   target=8  →  [[2,2,2,2],[2,3,3],[3,5]]
    candidates=[2],       target=1  →  []

Key Insight:
    At each index i, we have two choices:
      1. INCLUDE candidates[i] again (stay at index i — allows reuse)
      2. MOVE ON to index i+1 (don't pick candidates[i] anymore)

    This is different from the subsequence problems where we moved to i+1
    for both include and exclude. Here the "include" branch stays at i
    to allow picking the same element again.

    Recursion tree for [2,3,6,7], target=7:
                        solve(0, [], 7)
                       /                \\
           solve(0,[2],5)           solve(1,[],7)
           /            \\           /         \\
    solve(0,[2,2],3) solve(1,[2],5) ...       solve(2,[],7)
       /         \\                                  ...
 solve(0,[2,2,2],1) solve(1,[2,2],3)
    /        \\
solve(0,[2,2,2,2],-1) solve(1,[2,2,2],1)   ← -1 pruned
  pruned         ...
                ...
    ✓ [2,2,3] found when solve(2,[2,2,3],0) hits base case
    ✓ [7] found when solve(3,[7],0) hits base case
"""


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1: YOUR ORIGINAL (creates new list each call — no backtracking)
# Time  : O(2^t)  where t = target/min(candidates)  — branching factor analysis
# Space : O(t/min_candidate)  — max depth of recursion
#
# Correct but inefficient — creates a fresh temp list by copying `nums` at
# every call. This is O(n) per call for the copy, and avoids needing to undo
# because each branch has its own independent copy.
#
# The `remaining -= candidates[i]; ...; remaining += candidates[i]` pattern
# is manual undo for a single variable — but it would be cleaner to just
# pass `remaining - candidates[i]` as an argument (no undo needed for ints).
# ─────────────────────────────────────────────────────────────────────────────
def combinationSum_v1(candidates: list, target: int) -> list:
    if not candidates or target < 0:
        return []

    def solve(index, nums, remaining, result):
        if remaining == 0:
            result.append(nums)    # nums is already a fresh copy, safe to append
            return
        elif remaining < 0:        # overshot — prune
            return

        for i in range(index, len(candidates)):
            # Create a new copy of nums with candidates[i] added
            # (This is the "no backtracking" approach — each branch gets its own list)
            temp = nums + [candidates[i]]     # cleaner than the manual copy loop

            remaining -= candidates[i]        # temporary decrement (could just pass as arg)
            solve(i, temp, remaining, result)
            remaining += candidates[i]        # undo decrement

    result = []
    solve(0, [], target, result)
    return result


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: YOUR OPTIMISED (backtracking + sort + pruning) ← best of yours
# Time  : O(2^t)  — same asymptotic, but pruning cuts branches early
# Space : O(t/min_candidate)  — recursion depth
#
# Two key improvements over Approach 1:
#   1. Sort candidates → once candidates[i] > remaining, all further candidates
#      are also too large → `break` instead of continuing the loop (pruning)
#   2. Backtracking → mutate a SINGLE shared list, undo with pop() after each
#      recursive call. Avoids creating O(n) copies at every level.
#
# `nums[:]` at the base case creates one copy only when a solution is found —
# much cheaper than copying at every single recursive call.
# ─────────────────────────────────────────────────────────────────────────────
def combinationSum_v2(candidates: list, target: int) -> list:
    if not candidates or target < 0:
        return []

    candidates.sort()   # enables the break-pruning below

    def solve(index, nums, remaining, result):
        # Base case: valid combination found
        if remaining == 0:
            result.append(nums[:])  # shallow copy only here — O(solution_length)
            return

        for i in range(index, len(candidates)):
            # Pruning: since array is sorted, if current candidate exceeds
            # remaining sum, all further candidates will too → stop early
            if candidates[i] > remaining:
                break

            nums.append(candidates[i])                    # choose
            solve(i, nums, remaining - candidates[i], result)  # explore (stay at i for reuse)
            nums.pop()                                    # undo (backtrack)

    result = []
    solve(0, [], target, result)
    return result


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 3: INCLUDE / EXCLUDE (binary decision style)
# Time  : O(2^t)
# Space : O(t/min_candidate)
#
# Instead of a loop over remaining candidates, make exactly 2 choices at each
# step — this is the same pattern as count subsequences with sum K:
#
#   Choice A: INCLUDE candidates[index] again → stay at same index
#   Choice B: MOVE to next index             → don't pick candidates[index] anymore
#
# This is equivalent to Approach 2 but expressed as binary branching
# instead of a loop. Both produce the same results.
#
# When to prefer this style: cleaner to reason about for interview explanations.
# When to prefer the loop: natural when you want the pruning break statement.
# ─────────────────────────────────────────────────────────────────────────────
def combinationSum_v3(candidates: list, target: int) -> list:
    if not candidates or target < 0:
        return []

    result = []

    def solve(index: int, curr: list, remaining: int) -> None:
        # Base case: found a valid combination
        if remaining == 0:
            result.append(curr[:])
            return

        # Overshot or exhausted all candidates
        if remaining < 0 or index == len(candidates):
            return

        # Choice A: pick candidates[index] again (stay at same index)
        curr.append(candidates[index])
        solve(index, curr, remaining - candidates[index])
        curr.pop()   # backtrack

        # Choice B: move past candidates[index] (never pick it again)
        solve(index + 1, curr, remaining)

    solve(0, [], target)
    return result
