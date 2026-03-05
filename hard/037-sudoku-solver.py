"""
37. SUDOKU SOLVER

Problem Statement:
Write a program to solve a Sudoku puzzle by filling the empty cells.

Rules:
1. Each digit 1-9 must occur exactly once in each row
2. Each digit 1-9 must occur exactly once in each column
3. Each digit 1-9 must occur exactly once in each 3x3 sub-box

The '.' character indicates empty cells.
It is guaranteed that the input board has only one solution.

Constraints:
* board.length == 9
* board[i].length == 9
* board[i][j] is a digit or '.'
"""


# ==============================================================================
# YOUR SOLUTION 1: WRONG APPROACH
# ==============================================================================
# Issues: 
# - Random directional search (up, down, left, right) doesn't make sense
# - Copying board constantly is inefficient
# - Doesn't properly backtrack

class Solution_V1_Wrong:
    """
    First attempt - fundamentally flawed approach.
    
    Issues:
    1. Random directional exploration (row+1, row-1, col+1, col-1)
       - Sudoku should be solved systematically, not randomly
    2. Board copying is inefficient
    3. Backtracking logic is broken
    4. Missing proper state management
    
    Learning: Need systematic cell-by-cell traversal!
    """
    def solveSudoku(self, board):
        """
    :type board: List[List[str]]
    :rtype: None Do not return anything, modify board in-place instead.
    """
        if not board:
            return board

        rowsCols_to_Index = {0:0, 1:0, 2:0, 3:3, 4:3, 5:3, 6:6, 7:6, 8:6}
        missingN = 0
        for row in range(9):
            for col in range(9):
                if board[row][col] == ".":
                    missingN += 1


        def findNums(board, row, col):
            nums = []
            seen = set()

            for r in range(9):
                if board[r][col] != ".":
                    seen.add(board[r][col])
            for c in range(9):
                if board[row][c] != ".":
                    seen.add(board[row][c])
            for r in range(rowsCols_to_Index[row], rowsCols_to_Index[row] + 3):
                for c in range(rowsCols_to_Index[col], rowsCols_to_Index[col] + 3):
                    if board[r][c] != ".":
                        seen.add(board[r][c])

            if len(seen) == 9:
                return []
            for i in range(1, 10):

                if str(i) not in seen:
                    nums.append(str(i))
            return nums

        def solve(board, row, col, missingN):
            if row == -1 or row == 9 or col == -1 or col == 9:
                return []
            if board[row][col] == ".":
                print(f"board[{row}][{col}]: {board[row][col]}")
                nums = findNums(board, row, col)

                if not nums:
                    return []
                for n in nums:
                    print(f"Possible N: {n}")
                    board[row][col] = n
                    missingN -= 1
                    if missingN == 0:
                        return board.copy()


            d = ( solve(board, row + 1, col, missingN) or
                solve(board, row - 1, col, missingN) or
                solve(board, row, col + 1, missingN) or
                solve(board, row, col - 1, missingN) )

            if d:
                return d
            else:
                missingN += 1
                board[row][col] = "."
                return []


        resBoard = solve(board.copy(), 0, 0, missingN)
        return resBoard


# ==============================================================================
# YOUR SOLUTION 2: WORKS BUT TLE (TIME LIMIT EXCEEDED)
# ==============================================================================
# Time Complexity: O(9^(empty cells)) - tries all possibilities
# Space Complexity: O(empty cells) - recursion stack

class Solution_V2_TLE:
    def solveSudoku(self, board):
        """
        Correct backtracking but too slow.
        
        What's Right:
        ✓ Systematic row-by-row traversal
        ✓ Proper backtracking logic
        ✓ Correct candidate finding
        
        Why TLE:
        ❌ Recalculates candidates every time (O(81) per call)
        ❌ No optimization - always picks first empty cell
        ❌ No pruning of search space
        
        This is the "naive backtracking" solution.
        Works correctly but explores too many branches.
        """
        if not board:
            return board

        rowsCols_to_Index = {0:0, 1:0, 2:0, 3:3, 4:3, 5:3, 6:6, 7:6, 8:6}

        def findNums(board, row, col):
            """Find valid candidates for cell (row, col)"""
            seen = set()
            
            # Check row
            for r in range(9):
                if board[r][col] != ".":
                    seen.add(board[r][col])
            
            # Check column
            for c in range(9):
                if board[row][c] != ".":
                    seen.add(board[row][c])
            
            # Check 3x3 box
            box_r = rowsCols_to_Index[row]
            box_c = rowsCols_to_Index[col]
            for r in range(box_r, box_r + 3):
                for c in range(box_c, box_c + 3):
                    if board[r][c] != ".":
                        seen.add(board[r][c])
            
            # Return available digits
            if len(seen) == 9:
                return []
            return [str(i) for i in range(1, 10) if str(i) not in seen]

        def solve(board, row, col, res):
            """Backtracking solver"""
            # Base case: reached end of board
            if row == 9:
                res.append([row[:] for row in board])
                return
            
            # Calculate next position
            newR, newC = row, (col + 1) % 9
            if newC == 0:
                newR += 1
            
            if board[row][col] == ".":
                # Find candidates
                nums = findNums(board, row, col)
                
                if not nums:
                    return  # No valid candidates, backtrack
                
                # Try each candidate
                for n in nums:
                    board[row][col] = n
                    solve(board, newR, newC, res)
                    
                    if res:  # Found solution
                        return
                    
                    board[row][col] = "."  # Backtrack
            else:
                # Cell already filled, move to next
                solve(board, newR, newC, res)

        res = []
        solve(board, 0, 0, res)
        return res[0] if res else board


# ==============================================================================
# YOUR SOLUTION 3: OPTIMAL WITH MRV HEURISTIC
# ==============================================================================
# Time Complexity: Much better in practice (hard to analyze exactly)
# Space Complexity: O(1) - modifies board in-place

class Solution:
    def solveSudoku(self, board):
        """
        OPTIMAL solution using constraint sets + MRV heuristic.
        
        Key Optimizations:
        
        1. Constraint Sets (O(1) lookups):
           - rows[r]: digits used in row r
           - cols[c]: digits used in col c
           - boxes[b]: digits used in box b
           - Finding candidates: ALL - rows[r] - cols[c] - boxes[b]
           - No more scanning 27 cells every time!
        
        2. MRV (Most Constrained Variable) Heuristic:
           - Always pick empty cell with FEWEST candidates
           - Cell with 1 candidate = no branching (free!)
           - Cell with 0 candidates = fail immediately
           - Dramatically reduces search tree size
        
        3. Early Termination:
           - Return immediately on success
           - No need to explore other branches
        
        Why This is Fast:
        - O(1) candidate finding vs O(81) scanning
        - Smart cell selection reduces branching factor
        - Fails fast when no solution possible
        
        This is a PROFESSIONAL-LEVEL implementation!
        """
        # Initialize constraint sets
        rows  = [set() for _ in range(9)]
        cols  = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]
        
        # Collect empty cells and populate constraints
        empty = []
        for r in range(9):
            for c in range(9):
                val = board[r][c]
                if val == ".":
                    empty.append((r, c))
                else:
                    b = (r // 3) * 3 + (c // 3)
                    rows[r].add(val)
                    cols[c].add(val)
                    boxes[b].add(val)
        
        ALL = {"1","2","3","4","5","6","7","8","9"}
        
        def candidates(r, c):
            """O(1) candidate finding using constraint sets"""
            b = (r // 3) * 3 + (c // 3)
            return ALL - rows[r] - cols[c] - boxes[b]
        
        def solve(idx):
            """Backtracking with MRV heuristic"""
            # Base case: all cells filled
            if idx == len(empty):
                return True
            
            r, c = empty[idx]
            
            # MRV HEURISTIC: Find cell with fewest candidates
            best_idx = idx
            best_count = len(candidates(r, c))
            
            for i in range(idx + 1, len(empty)):
                if best_count <= 1:
                    break  # Can't do better than 0 or 1
                cr, cc = empty[i]
                cnt = len(candidates(cr, cc))
                if cnt < best_count:
                    best_count = cnt
                    best_idx = i
            
            # Swap best cell to front
            empty[idx], empty[best_idx] = empty[best_idx], empty[idx]
            r, c = empty[idx]
            b = (r // 3) * 3 + (c // 3)
            
            # Try each candidate
            for n in candidates(r, c):
                # Place digit and update constraints
                board[r][c] = n
                rows[r].add(n)
                cols[c].add(n)
                boxes[b].add(n)
                
                if solve(idx + 1):
                    return True
                
                # Backtrack
                board[r][c] = "."
                rows[r].remove(n)
                cols[c].remove(n)
                boxes[b].remove(n)
            
            # Undo MRV swap
            empty[idx], empty[best_idx] = empty[best_idx], empty[idx]
            return False
        
        solve(0)
        return board


# ==============================================================================
# COMPLEXITY ANALYSIS
# ==============================================================================

"""
SOLUTION 1 (Wrong):
❌ Fundamentally broken approach
❌ Random directional search makes no sense
❌ Doesn't solve sudoku correctly

SOLUTION 2 (TLE):
✓ Correct backtracking logic
✓ Systematic traversal
❌ O(81) to find candidates each time
❌ No optimization - explores too many branches
❌ TLE on hard puzzles

Time: O(9^m) where m = empty cells
Space: O(m) recursion

SOLUTION 3 (Optimal): ⭐
✓ O(1) candidate finding using constraint sets
✓ MRV heuristic dramatically reduces branches
✓ Early termination on success
✓ Professional-level implementation

Time: Much better in practice (exact analysis complex)
Space: O(1) if not counting recursion stack

RECOMMENDATION:
Solution 3 is what you should know for interviews!
Shows understanding of:
- Backtracking
- Constraint satisfaction
- Heuristics for optimization
"""


# ==============================================================================
# KEY INSIGHTS
# ==============================================================================

"""
Why Solution 3 is SO Much Faster:

1. Constraint Sets (HUGE improvement):
   Before: Scan 9 + 9 + 9 = 27 cells each time → O(81) per candidate check
   After: Set operations → O(1) per candidate check
   
   With 40 empty cells, millions of candidate checks happen!
   This alone is a massive speedup.

2. MRV Heuristic (CRITICAL optimization):
   Example scenario:
   - Cell A has 7 candidates → 7 branches to explore
   - Cell B has 1 candidate → 1 branch (no choice!)
   
   Always pick Cell B first → no wasted exploration!
   
   In practice, this reduces the search tree from exponential
   to nearly linear for most puzzles.

3. Early Termination:
   Return immediately when solution found.
   No need to explore alternative branches.

4. Fail Fast:
   If any cell has 0 candidates → impossible state
   Return immediately without trying anything.

These optimizations combined make the difference between
TLE and passing all test cases!
"""


# ==============================================================================
# TESTING
# ==============================================================================

if __name__ == "__main__":
    from copy import deepcopy
    
    board = [["5","3",".",".","7",".",".",".","."],
             ["6",".",".","1","9","5",".",".","."],
             [".","9","8",".",".",".",".","6","."],
             ["8",".",".",".","6",".",".",".","3"],
             ["4",".",".","8",".","3",".",".","1"],
             ["7",".",".",".","2",".",".",".","6"],
             [".","6",".",".",".",".","2","8","."],
             [".",".",".","4","1","9",".",".","5"],
             [".",".",".",".","8",".",".","7","9"]]
    
    expected = [["5","3","4","6","7","8","9","1","2"],
                ["6","7","2","1","9","5","3","4","8"],
                ["1","9","8","3","4","2","5","6","7"],
                ["8","5","9","7","6","1","4","2","3"],
                ["4","2","6","8","5","3","7","9","1"],
                ["7","1","3","9","2","4","8","5","6"],
                ["9","6","1","5","3","7","2","8","4"],
                ["2","8","7","4","1","9","6","3","5"],
                ["3","4","5","2","8","6","1","7","9"]]
    
    print("=" * 70)
    print("TESTING SUDOKU SOLVER")
    print("=" * 70)
    print()
    
    # Test optimal solution
    test_board = deepcopy(board)
    sol = Solution()
    result = sol.solveSudoku(test_board)
    
    print("Result:")
    for row in result:
        print(row)
    print()
    
    if result == expected:
        print("✓ PASS - Solution is correct!")
    else:
        print("✗ FAIL - Solution is incorrect")
    
    print()
    print("=" * 70)
    print("WHAT YOU LEARNED:")
    print("=" * 70)
    print()
    print("V1 → V2: Fixed fundamental approach")
    print("  - Systematic traversal instead of random search")
    print("  - Proper backtracking logic")
    print()
    print("V2 → V3: Optimization!")
    print("  - Constraint sets: O(81) → O(1) candidate finding")
    print("  - MRV heuristic: Smart cell selection")
    print("  - Result: TLE → AC (Accepted)")
    print()
    print("This progression shows excellent problem-solving!")
    print("=" * 70)