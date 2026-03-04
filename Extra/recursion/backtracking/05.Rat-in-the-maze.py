"""
PROBLEM: Rat in a Maze
=======================

Given a grid of dimensions n x n. A rat is placed at (0, 0) and wants to
reach (n-1, n-1). Find all possible paths the rat can take.

Directions: 'U' (up), 'D' (down), 'L' (left), 'R' (right)
  - 0 → blocked cell
  - 1 → open cell
  - Cell (0,0) == 0 → no path possible

Examples:
    n=4, grid = [[1,0,0,0],
                 [1,1,0,1],
                 [1,1,0,0],
                 [0,1,1,1]]
    Output: ["DDRDRR", "DRDDRR"]

    n=2, grid = [[1,0],[1,0]]
    Output: []

Constraints:
    - 1 <= n <= 5
    - grid[i][j] is 0 or 1
"""


# ─────────────────────────────────────────────────────────────────────────────
# SOLUTION 1: TUF / Classic — separate visited array + isSafe helper
# ─────────────────────────────────────────────────────────────────────────────
# Uses a dedicated visited[][] matrix to track cells in the current path.
# Directions tried in lexicographical order: D → L → R → U
# (guarantees output is already sorted without extra sorting step)
#
# Time:  O(4^(n²))  — at most 4 choices per cell, n² cells deep
# Space: O(n²)      — visited array + recursion stack

class Solution:
    def isSafe(self, x, y, n, maze, visited):
        """Check bounds, cell is open, and not already in current path."""
        return (0 <= x < n and
                0 <= y < n and
                maze[x][y] == 1 and
                visited[x][y] == 0)

    def solve(self, x, y, n, maze, visited, path, res):
        # Base case: reached destination
        if x == n - 1 and y == n - 1:
            res.append(path)
            return

        visited[x][y] = 1   # mark current cell as part of path

        # Try all 4 directions in lexicographical order (D, L, R, U)
        if self.isSafe(x + 1, y, n, maze, visited):
            self.solve(x + 1, y, n, maze, visited, path + "D", res)
        if self.isSafe(x, y - 1, n, maze, visited):
            self.solve(x, y - 1, n, maze, visited, path + "L", res)
        if self.isSafe(x, y + 1, n, maze, visited):
            self.solve(x, y + 1, n, maze, visited, path + "R", res)
        if self.isSafe(x - 1, y, n, maze, visited):
            self.solve(x - 1, y, n, maze, visited, path + "U", res)

        visited[x][y] = 0   # backtrack: unmark so other paths can use it

    def findPath(self, maze, n):
        res     = []
        visited = [[0] * n for _ in range(n)]
        if maze[0][0] == 1:
            self.solve(0, 0, n, maze, visited, "", res)
        return res


# ─────────────────────────────────────────────────────────────────────────────
# SOLUTION 2: Cleaner approach — in-place marking, directions table
# ─────────────────────────────────────────────────────────────────────────────
# Same backtracking logic but written more concisely:
#   • No separate visited array — temporarily set maze[r][c] = 0 to block it,
#     then restore it to 1 on backtrack. One less n×n array to maintain.
#   • Directions stored in a list of (dr, dc, label) tuples so the loop is
#     just 4 lines instead of 4 repeated if-blocks.
#   • Much easier to read and extend (e.g. add diagonal moves by appending
#     to the directions list).
#
# Time:  O(4^(n²))  — same search space
# Space: O(n²)      — recursion stack only (no extra visited array)

def findPath(maze, n):
    result = []

    # (row_delta, col_delta, direction_label) — lexicographical order
    directions = [(1, 0, "D"), (0, -1, "L"), (0, 1, "R"), (-1, 0, "U")]

    def dfs(r, c, path):
        # Base case: reached bottom-right corner
        if r == n - 1 and c == n - 1:
            result.append(path)
            return

        # Temporarily mark cell as blocked so we don't revisit it
        maze[r][c] = 0

        for dr, dc, move in directions:
            nr, nc = r + dr, c + dc
            # Move only if in-bounds and cell is open
            if 0 <= nr < n and 0 <= nc < n and maze[nr][nc] == 1:
                dfs(nr, nc, path + move)

        # Restore cell (backtrack)
        maze[r][c] = 1

    if maze[0][0] == 1:
        dfs(0, 0, "")

    return result


# ─────────────────────────────────────────────────────────────────────────────
# Side-by-side comparison
# ─────────────────────────────────────────────────────────────────────────────
#
#  Feature                    Solution 1 (TUF)          Solution 2 (Clean)
#  ──────────────────────── ─────────────────────────  ────────────────────────
#  Visited tracking           Separate visited[][]       In-place maze[r][c] = 0
#  Direction handling         4 separate if-blocks       1 loop over directions[]
#  Extra space                O(n²) for visited array    O(1) extra
#  Readability                Moderate                   High ← easier in interviews
#  Modify directions easily   No (copy-paste 4 blocks)   Yes (append to list)


# ─────────────────────────────────────────────────────────────────────────────
# Quick tests
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import copy

    maze1 = [
        [1, 0, 0, 0],
        [1, 1, 0, 1],
        [1, 1, 0, 0],
        [0, 1, 1, 1]
    ]
    maze2 = [[1, 0], [1, 0]]
    maze3 = [[1]]

    sol = Solution()

    # Solution 1 tests
    assert sol.findPath(copy.deepcopy(maze1), 4) == ["DDRDRR", "DRDDRR"]
    assert sol.findPath(copy.deepcopy(maze2), 2) == []
    assert sol.findPath(copy.deepcopy(maze3), 1) == [""]

    # Solution 2 tests
    assert findPath(copy.deepcopy(maze1), 4) == ["DDRDRR", "DRDDRR"]
    assert findPath(copy.deepcopy(maze2), 2) == []
    assert findPath(copy.deepcopy(maze3), 1) == [""]

    print("All test cases passed ✓")

    # Pretty print paths for maze1
    paths = findPath(copy.deepcopy(maze1), 4)
    print(f"\nPaths found for 4x4 maze: {paths}")
    for p in paths:
        print(f"  {p}  ({len(p)} steps)")