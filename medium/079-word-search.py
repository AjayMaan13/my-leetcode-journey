"""
PROBLEM: Word Search (LeetCode 79)
==================================

Given an m x n grid of characters `board` and a string `word`, return True if
the word exists in the grid.

The word can be constructed from letters of sequentially adjacent cells, where
adjacent cells are horizontally or vertically neighboring. The same letter cell
may not be used more than once.

Examples:
    board = [["A","B","C","E"],
             ["S","F","C","S"],
             ["A","D","E","E"]]

    exist(board, "ABCCED") -> True
    exist(board, "SEE")    -> True
    exist(board, "ABCB")   -> False

Constraints:
    - m == board.length
    - n == board[i].length
    - 1 <= m, n <= 6
    - 1 <= word.length <= 15
    - board and word consist of only lowercase and uppercase English letters
"""


# ─────────────────────────────────────────────────────────────
# SOLUTION 1: Classic DFS + Backtracking  (your original)
# ─────────────────────────────────────────────────────────────
# Time:  O(m * n * 4^L)  where L = len(word)
# Space: O(L)            recursion stack depth

class Solution:
    def exist(self, board: list[list[str]], word: str) -> bool:
        if not board or not word:
            return False

        rows, cols = len(board), len(board[0])

        def dfs(r, c, index):
            if index == len(word):
                return True
            if (r < 0 or r >= rows or
                    c < 0 or c >= cols or
                    board[r][c] != word[index]):
                return False

            temp = board[r][c]
            board[r][c] = "#"           # mark visited

            found = (
                dfs(r, c - 1, index + 1) or
                dfs(r, c + 1, index + 1) or
                dfs(r - 1, c, index + 1) or
                dfs(r + 1, c, index + 1)
            )

            board[r][c] = temp          # restore (backtrack)
            return found

        for r in range(rows):
            for c in range(cols):
                if dfs(r, c, 0):
                    return True
        return False


# ─────────────────────────────────────────────────────────────
# SOLUTION 2: DFS + Backtracking + Search Pruning  (your follow-up)
# ─────────────────────────────────────────────────────────────
# Extra optimisations on top of Solution 1:
#
#   PRUNE 1 — Letter-frequency early exit
#       Before doing any DFS, count every character on the board and in the
#       word. If the word requires more of any character than the board
#       contains, it's impossible → return False immediately.
#
#   PRUNE 2 — Start from the rarer end
#       Compare how often word[0] appears on the board vs word[-1].
#       Start searching from whichever end has fewer matching cells, so the
#       very first character check eliminates more starting positions.
#
# Time:  O(m * n * 4^L) worst-case, but much faster in practice
# Space: O(L)

from collections import Counter


def exist(board: list[list[str]], word: str) -> bool:
    rows, cols = len(board), len(board[0])

    # ── PRUNE 1: letter frequency check ──────────────────────
    board_count = Counter(ch for row in board for ch in row)
    word_count  = Counter(word)
    for ch, cnt in word_count.items():
        if cnt > board_count[ch]:
            return False

    # ── PRUNE 2: search from the rarer end ───────────────────
    if board_count[word[0]] > board_count[word[-1]]:
        word = word[::-1]

    def dfs(r, c, index):
        if index == len(word):
            return True
        if (r < 0 or r >= rows or
                c < 0 or c >= cols or
                board[r][c] != word[index]):
            return False

        temp = board[r][c]
        board[r][c] = "#"

        found = (
            dfs(r + 1, c, index + 1) or
            dfs(r - 1, c, index + 1) or
            dfs(r, c + 1, index + 1) or
            dfs(r, c - 1, index + 1)
        )

        board[r][c] = temp
        return found

    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True
    return False


# ─────────────────────────────────────────────────────────────
# Quick tests
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    board1 = [["A","B","C","E"],
              ["S","F","C","S"],
              ["A","D","E","E"]]

    sol = Solution()

    # Solution 1 tests
    import copy
    assert sol.exist(copy.deepcopy(board1), "ABCCED") == True
    assert sol.exist(copy.deepcopy(board1), "SEE")    == True
    assert sol.exist(copy.deepcopy(board1), "ABCB")   == False

    # Solution 2 tests
    assert exist(copy.deepcopy(board1), "ABCCED") == True
    assert exist(copy.deepcopy(board1), "SEE")    == True
    assert exist(copy.deepcopy(board1), "ABCB")   == False

    print("All test cases passed ✓")