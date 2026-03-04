"""
PROBLEM: N-Queens (LeetCode 51)
================================

The n-queens puzzle is the problem of placing n queens on an n x n chessboard
such that no two queens attack each other.

Given an integer n, return all distinct solutions to the n-queens puzzle.
You may return the answer in any order.

Each solution contains a distinct board configuration of the n-queens' placement,
where 'Q' and '.' both indicate a queen and an empty space, respectively.

Examples:
    solveNQueens(4) -> [[".Q..","...Q","Q...","..Q."],
                        ["..Q.","Q...","...Q",".Q.."]]
    solveNQueens(1) -> [["Q"]]

Constraints:
    - 1 <= n <= 9

A queen attacks any cell in the same row, column, or diagonal.
Key insight: place exactly ONE queen per row → only need to track which
columns and diagonals are occupied.
"""


# ─────────────────────────────────────────────────────────────────────────────
# SOLUTION 1: Your original approach — manual diagonal check via queens list
# ─────────────────────────────────────────────────────────────────────────────
# Works correctly but does O(k) work per placement to scan existing queens
# for diagonal conflicts. Also uses a colRemoved list for O(k) column checks.
#
# Time:  O(n! * n)   — n! placements, O(n) diagonal check each
# Space: O(n^2)      — board + recursion stack

def solveNQueens_v1(n):
    if n < 1:
        return []

    board      = ["." * n for _ in range(n)]
    result     = []

    def copyBoard(board):
        return list(board)

    def checkPosition(queens, r, c):
        """Return True if (r, c) is safe from all placed queens diagonally."""
        for queen in queens:
            if abs(queen[0] - r) == abs(queen[1] - c):
                return False
        return True

    def dfs(board, queens, colRemoved, r):
        if r == n:                                  # all rows filled → valid solution
            result.append(copyBoard(board))
            return

        for c in range(n):
            if c in colRemoved:                     # column already used
                continue
            if not checkPosition(queens, r, c):     # diagonal conflict
                continue

            # place queen
            board[r]  = board[r][:c] + "Q" + board[r][c + 1:]
            queens.append([r, c])
            colRemoved.append(c)

            dfs(board, queens, colRemoved, r + 1)

            # backtrack
            board[r]  = board[r][:c] + "." + board[r][c + 1:]
            queens.pop()
            colRemoved.pop()

    dfs(board, [], [], 0)
    return result


# ─────────────────────────────────────────────────────────────────────────────
# SOLUTION 2: Optimised — O(1) conflict detection via sets  ← RECOMMENDED
# ─────────────────────────────────────────────────────────────────────────────
# Instead of scanning every placed queen on each step, maintain three sets:
#
#   col      — columns that are occupied
#   posDiag  — (r + c) is constant along every "/" diagonal
#   negDiag  — (r - c) is constant along every "\" diagonal
#
# All three checks become O(1) lookups, cutting the per-step cost from O(n)
# to O(1).  This is the NeetCode / canonical interview solution.
#
# Time:  O(n!)    — same search space, but O(1) per conflict check
# Space: O(n^2)   — board + recursion stack

class Solution:
    def solveNQueens(self, n: int):
        col     = set()
        posDiag = set()   # r + c
        negDiag = set()   # r - c

        res   = []
        board = [["." ] * n for _ in range(n)]

        def backtrack(r):
            if r == n:
                res.append(["".join(row) for row in board])
                return

            for c in range(n):
                if c in col or (r + c) in posDiag or (r - c) in negDiag:
                    continue

                # place
                col.add(c)
                posDiag.add(r + c)
                negDiag.add(r - c)
                board[r][c] = "Q"

                backtrack(r + 1)

                # backtrack
                col.remove(c)
                posDiag.remove(r + c)
                negDiag.remove(r - c)
                board[r][c] = "."

        backtrack(0)
        return res


# ─────────────────────────────────────────────────────────────────────────────
# Comparison of both approaches
# ─────────────────────────────────────────────────────────────────────────────
#
#  Feature                  Solution 1 (v1)          Solution 2 (v2 / sets)
#  ─────────────────────── ──────────────────────── ───────────────────────────
#  Column conflict check    O(k) list scan           O(1) set lookup
#  Diagonal conflict check  O(k) abs-diff loop       O(1) set lookup  (r±c trick)
#  Code clarity             Moderate                 Clean & concise
#  Interview preference     Acceptable               Preferred
#
# The r+c / r-c diagonal trick is the key insight worth memorising:
#   • All cells on the same "/"  diagonal share the same (r + c) value
#   • All cells on the same "\"  diagonal share the same (r - c) value
