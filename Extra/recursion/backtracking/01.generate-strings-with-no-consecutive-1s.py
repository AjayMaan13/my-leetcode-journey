"""
Generate All Binary Strings Without Consecutive 1s  |  TUF Problem

Problem Statement:
    Given an integer n, return all binary strings of length n that do NOT
    contain consecutive 1s, in lexicographically increasing order.

Examples:
    n = 3  →  ["000", "001", "010", "100", "101"]
    n = 2  →  ["00", "01", "10"]

Core Idea (Backtracking / Recursion Tree):
    At each position we have two choices: place '0' or place '1'.
    Constraint: we can only place '1' if the PREVIOUS character was NOT '1'.

    Recursion tree for n=3:
    
                            ""
                          /   \\ 
                        /       \\
                      /           \\
                    /               \\
                  "0"               "1"
               /      \\           /
            "00"      "01"       "10"
           /    \\        \\      /    \\
        "000"  "001"    "010" "100"  "101"   ← all valid, no consecutive 1s
                                "11" skipped ← lastChar was '1', blocked
"""


# ─────────────────────────────────────────────────────────────────────────────
# YOUR SOLUTION  (cleaned up + commented)
# Time  : O(2^n)  — at most 2^n strings explored (fewer due to pruning)
# Space : O(n)    — recursion depth = n, current string length = n
#
# Parameters of generate():
#   index    — current position being filled (0 to n-1)
#   result   — list collecting completed strings
#   curr     — string built so far
#   lastChar — the character placed at the previous position
#              used to enforce the "no consecutive 1s" rule
# ─────────────────────────────────────────────────────────────────────────────
def generateStrings(n: int) -> list:
    if n < 1:
        return []

    def generate(index: int, result: list, curr: str, lastChar: str) -> None:
        # Base case: string is complete (length == n)
        if index == n:
            result.append(curr)
            return

        # Choice 1: always safe to place '0'
        # '0' never causes consecutive 1s regardless of lastChar
        generate(index + 1, result, curr + "0", "0")

        # Choice 2: place '1' ONLY if the previous character was not '1'
        # If lastChar == '1', adding another '1' would create "11" → skip
        if lastChar != "1":
            generate(index + 1, result, curr + "1", "1")

    result = []
    generate(0, result, "", "")   # start with empty string, no lastChar
    return result


# ─────────────────────────────────────────────────────────────────────────────
# ALTERNATIVE: same logic but track last char as a boolean flag
# Slightly cleaner — avoids string comparison, uses bool instead
# ─────────────────────────────────────────────────────────────────────────────
def generateStrings_bool(n: int) -> list:
    if n < 1:
        return []

    result = []

    def generate(index: int, curr: str, last_was_one: bool) -> None:
        if index == n:
            result.append(curr)
            return

        # '0' is always allowed
        generate(index + 1, curr + "0", False)

        # '1' only allowed if previous was not '1'
        if not last_was_one:
            generate(index + 1, curr + "1", True)

    generate(0, "", False)
    return result


# ─────────────────────────────────────────────────────────────────────────────
# ALTERNATIVE: iterative BFS-style using a queue (no recursion)
# Time  : O(2^n)
# Space : O(2^n)  — queue holds all partial strings at current level
#
# Instead of recursion, grow all strings level by level (like BFS).
# Each iteration extends every current partial string by one character.
# ─────────────────────────────────────────────────────────────────────────────
def generateStrings_iterative(n: int) -> list:
    if n < 1:
        return []

    # Each entry in queue is (partial_string, last_char)
    queue = [("", "")]

    for _ in range(n):
        next_queue = []
        for curr, lastChar in queue:
            # Always extend with '0'
            next_queue.append((curr + "0", "0"))
            # Extend with '1' only if last wasn't '1'
            if lastChar != "1":
                next_queue.append((curr + "1", "1"))
        queue = next_queue

    return [s for s, _ in queue]   # strip the lastChar tracking, return strings only
