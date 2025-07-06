"""
LeetCode 100. Same Tree (Easy)

Given the roots of two binary trees p and q, write a function to check if they are the same or not.

Two binary trees are considered the same if they are structurally identical, and the nodes have the same value.

Example 1:
Input: p = [1,2,3], q = [1,2,3]
Output: true

Example 2:
Input: p = [1,2], q = [1,null,2]
Output: false

Example 3:
Input: p = [1,2,1], q = [1,1,2]
Output: false

Constraints:
- The number of nodes in both trees is in the range [0, 100].
- -10^4 <= Node.val <= 10^4
"""

from collections import deque

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# 1. Your Original Solution
class OriginalSolution:
    def isSameTree(self, p, q):
        if p and q:
            left = deque([p])
            right = deque([q])

            while left or right:
                if len(left) != len(right):
                    return False

                for _ in range(len(left)):
                    leftPop = left.popleft()
                    rightPop = right.popleft()

                    if (leftPop.val if leftPop else None) != (rightPop.val if rightPop else None):
                        return False

                    if leftPop is not None:
                        left.append(leftPop.left)
                        left.append(leftPop.right)
                    if rightPop is not None:
                        right.append(rightPop.left)
                        right.append(rightPop.right)

            return True
        elif not p and not q:
            return True
        else:
            return False

# 2. DFS Recursive Solution
class DFSSolution:
    def isSameTree(self, p, q):
        if not p and not q:
            return True
        if not p or not q or p.val != q.val:
            return False
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)

# 3. Modified BFS Solution (Better Memory)
class ModifiedBFSSolution:
    def isSameTree(self, p, q):
        queue = deque([(p, q)])

        while queue:
            node1, node2 = queue.popleft()

            if not node1 and not node2:
                continue
            if not node1 or not node2 or node1.val != node2.val:
                return False

            queue.append((node1.left, node2.left))
            queue.append((node1.right, node2.right))

        return True

# ----------------------
# Test Tree Construction
# ----------------------
def build_test_trees():
    # Tree A:      1
    #             / \
    #            2   3
    treeA = TreeNode(1)
    treeA.left = TreeNode(2)
    treeA.right = TreeNode(3)

    # Tree B:      1
    #             / \
    #            2   3
    treeB = TreeNode(1)
    treeB.left = TreeNode(2)
    treeB.right = TreeNode(3)

    # Tree C:      1
    #             / 
    #            2   
    treeC = TreeNode(1)
    treeC.left = TreeNode(2)

    # Tree D:      1
    #               \
    #                2
    treeD = TreeNode(1)
    treeD.right = TreeNode(2)

    # Tree E:      1
    #             / \
    #            2   4
    treeE = TreeNode(1)
    treeE.left = TreeNode(2)
    treeE.right = TreeNode(4)

    return (treeA, treeB, treeC, treeD, treeE)

# ----------------------
# Run Tests
# ----------------------
def test_solution(name, solution_class):
    print(f"\nTesting {name}")
    solution = solution_class()
    treeA, treeB, treeC, treeD, treeE = build_test_trees()

    print("Test 1 (A vs B):", solution.isSameTree(treeA, treeB))  # True
    print("Test 2 (A vs C):", solution.isSameTree(treeA, treeC))  # False
    print("Test 3 (C vs D):", solution.isSameTree(treeC, treeD))  # False
    print("Test 4 (A vs E):", solution.isSameTree(treeA, treeE))  # False
    print("Test 5 (C vs C):", solution.isSameTree(treeC, treeC))  # True

# Run all three versions
if __name__ == "__main__":
    test_solution("OriginalSolution", OriginalSolution)
    test_solution("DFSSolution", DFSSolution)
    test_solution("ModifiedBFSSolution", ModifiedBFSSolution)
