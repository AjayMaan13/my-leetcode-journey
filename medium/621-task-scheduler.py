"""
621. Task Scheduler
https://leetcode.com/problems/task-scheduler/
Difficulty: Medium
Topics: Array, Hash Table, Greedy, Sorting, Heap (Priority Queue), Counting

Problem:
    Given an array of CPU tasks (each labeled A-Z) and a cooldown n,
    find the minimum number of CPU intervals to complete all tasks.
    Between two tasks of the same label, at least n intervals must pass.

Examples:
    tasks = ["A","A","A","B","B","B"], n = 2  → 8
    tasks = ["A","C","A","B","D","B"], n = 1  → 6
    tasks = ["A","A","A","B","B","B"], n = 3  → 10

Constraints:
    1 <= tasks.length <= 10^4
    tasks[i] is an uppercase English letter
    0 <= n <= 100
"""

import heapq
from collections import deque, Counter


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1: BRUTE FORCE SIMULATION
# ─────────────────────────────────────────────────────────────────────────────
# Idea:
#   Simulate time tick by tick. At each tick, pick the available task with
#   the highest frequency (greedy choice — always reduce the most frequent
#   task to minimise idle gaps). Track cooldown with a dict that records
#   the next available time for each task.
#
# Time:  O(T * |tasks|)  where T = total CPU intervals (could be >> len(tasks))
# Space: O(26) = O(1)  — at most 26 distinct tasks
# ─────────────────────────────────────────────────────────────────────────────

def leastInterval_brute(tasks, n):
    freq = Counter(tasks)              # {task: remaining count}
    available_at = {}                  # {task: next usable time}
    time = 0
    remaining = len(tasks)

    while remaining > 0:
        time += 1
        # Pick the available task with highest remaining frequency
        best_task = None
        best_freq = 0
        for task, count in freq.items():
            if count > 0 and available_at.get(task, 0) <= time:
                if count > best_freq:
                    best_freq = count
                    best_task = task

        if best_task:
            freq[best_task] -= 1
            if freq[best_task] == 0:
                del freq[best_task]
            available_at[best_task] = time + n + 1   # can use again after n gap
            remaining -= 1
        # else: idle this tick (time already incremented)

    return time


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: AJAY'S HEAP + COOLDOWN QUEUE SIMULATION  ← your solution
# ─────────────────────────────────────────────────────────────────────────────
# Idea:
#   Use a max-heap (simulated with negated frequencies) to always pick the
#   task with the highest remaining count. When a task is executed, push it
#   onto a cooldown deque with the earliest time it can re-enter the heap.
#   Increment a time counter each tick. Before popping from the heap, drain
#   any tasks whose cooldown has expired back into the heap.
#
# Key structures:
#   freqHeap  — max-heap of (-freq, task); always gives most-frequent available task
#   cooldown  — deque of (freq_after_use, task, available_at_time)
#   count     — current time tick
#
# Time:  O(T log 26) ≈ O(T)  — heap ops on at most 26 elements
# Space: O(26) = O(1)
#
# Bug in your original: `return count` was indented inside the while loop,
# so it returned after the very first tick. Fixed below (dedented one level).
# ─────────────────────────────────────────────────────────────────────────────

def leastInterval_heap(tasks, n):
    countMap = {}
    for task in tasks:
        countMap[task] = 1 + countMap.get(task, 0)

    freqHeap = []
    for key, freq in countMap.items():
        heapq.heappush(freqHeap, (-freq, key))   # max-heap via negation

    cooldown = deque()   # (neg_freq_remaining, task, time_available)
    count = 0            # current time tick

    while freqHeap or cooldown:
        count += 1

        # Re-activate any tasks whose cooldown period has elapsed
        while cooldown and cooldown[0][2] <= count:
            freq, key, _ = cooldown.popleft()
            heapq.heappush(freqHeap, (freq, key))

        if freqHeap:
            freq, key = heapq.heappop(freqHeap)   # most frequent available task
            # freq is negative; if there are still copies left after this use:
            if freq < -1:                          # i.e., remaining count > 1
                cooldown.append((freq + 1, key, count + n + 1))
        # else: no task available → idle tick (count still increments)

    return count   # ← FIX: was inside while loop in your original


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 3: OPTIMAL MATH / GREEDY FORMULA
# ─────────────────────────────────────────────────────────────────────────────
# Insight:
#   The most frequent task(s) determine the structure of the schedule.
#   Let maxFreq = highest frequency among all tasks.
#   Let maxCount = number of tasks that share this maximum frequency.
#
#   Imagine arranging tasks in a grid:
#       Each row has (n + 1) slots (one task + n cooldown slots).
#       The most-frequent task anchors the start of each of (maxFreq - 1) rows,
#       with a final partial row for the last batch.
#
#   "Ideal" intervals (if there are enough idle slots to fill):
#       (maxFreq - 1) * (n + 1) + maxCount
#
#   But if we have so many *different* tasks that no idle slots are needed,
#   the answer is just len(tasks).
#
#   Answer = max(len(tasks), (maxFreq - 1) * (n + 1) + maxCount)
#
#   Why does this work?
#   - The formula counts (maxFreq - 1) full frames of width (n+1) for the
#     most-frequent task, plus the final frame with maxCount tasks.
#   - If other tasks are numerous enough to fill the idle slots in every
#     frame, no idles are needed → answer = len(tasks).
#   - We never need fewer than len(tasks) intervals.
#
# Time:  O(|tasks|)  — one pass to count frequencies
# Space: O(26) = O(1)
# ─────────────────────────────────────────────────────────────────────────────

def leastInterval_optimal(tasks, n):
    freq = list(Counter(tasks).values())
    maxFreq = max(freq)
    maxCount = freq.count(maxFreq)          # how many tasks share the top frequency

    # Minimum intervals if we have to enforce cooling:
    ideal = (maxFreq - 1) * (n + 1) + maxCount

    # But we always need at least as many intervals as total tasks:
    return max(len(tasks), ideal)


# ─────────────────────────────────────────────────────────────────────────────
# TESTS
# ─────────────────────────────────────────────────────────────────────────────

def run_tests():
    test_cases = [
        # (tasks, n, expected)
        (["A","A","A","B","B","B"], 2, 8),
        (["A","C","A","B","D","B"], 1, 6),
        (["A","A","A","B","B","B"], 3, 10),
        (["A"],                     0, 1),   # single task, no cooldown
        (["A","A","A"],             2, 7),   # A -> idle -> idle -> A -> idle -> idle -> A
        (["A","B","C","D","E","F"], 2, 6),   # all unique, no idles needed
        (["A","A","A","A"],         3, 13),  # only one task type, lots of idles
    ]

    approaches = [
        ("Brute Force",    leastInterval_brute),
        ("Heap Simulation (Ajay)", leastInterval_heap),
        ("Optimal Math",   leastInterval_optimal),
    ]

    all_passed = True
    for tasks, n, expected in test_cases:
        for name, fn in approaches:
            result = fn(tasks, n)
            status = "✓" if result == expected else "✗"
            if result != expected:
                all_passed = False
                print(f"  {status} FAIL | {name} | tasks={tasks}, n={n} | got {result}, expected {expected}")

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
# Approach              Time            Space   Notes
# ──────────────────────────────────────────────────────────────────────────
# Brute Force           O(T · 26)       O(26)   T = total intervals (slow)
# Heap + Cooldown Queue O(T · log 26)   O(26)   Simulation, clean mental model
# Optimal Math Formula  O(N)            O(26)   N = len(tasks), one-liner logic
#
# Recommended: Optimal for interviews; Heap for intuition-building.