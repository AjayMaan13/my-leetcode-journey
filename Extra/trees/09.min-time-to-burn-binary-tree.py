"""
Minimum Time to Burn Binary Tree from a Node
----------------------------------------------

Problem Statement:
Given a binary tree and a target node, find the minimum time (in seconds)
to burn the entire tree if the target node is set on fire. Each second, fire
spreads to all directly connected nodes (left child, right child, parent).

Example 1:
Input:  root = [1, 2, 3, 4, null, 5, 6, null, 7], target = 1
Output: 3
  t=1: burns 2, 3
  t=2: burns 4, 5, 6
  t=3: burns 7

Example 2:
Input:  root = [1, 2, 3, null, 5, null, 4], target = 4
Output: 4
  t=1: burns 3
  t=2: burns 1
  t=3: burns 2
  t=4: burns 5

Approach:
Identical to "All Nodes Distance K" — build a parent map so we can walk
upward, then BFS from the target. The answer is the number of BFS levels
needed to visit every node (i.e. the maximum distance from the target).

Related: medium/863-all-nodes-distance-k.py
"""

from collections import deque


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def minTimeToBurn(root, target):
    # Step 1: build parent map
    parent = {}

    def buildParents(node, par):
        if not node:
            return
        parent[node] = par
        buildParents(node.left, node)
        buildParents(node.right, node)

    buildParents(root, None)

    # Step 2: find the target node
    def findNode(node, val):
        if not node:
            return None
        if node.val == val:
            return node
        return findNode(node.left, val) or findNode(node.right, val)

    start = findNode(root, target)

    # Step 3: BFS — count levels until all nodes are burned
    queue = deque([start])
    visited = {start}
    time = 0

    while queue:
        # process one full level (= one second)
        burned_this_second = False
        for _ in range(len(queue)):
            node = queue.popleft()
            for neighbour in (node.left, node.right, parent[node]):
                if neighbour and neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)
                    burned_this_second = True
        if burned_this_second:
            time += 1

    return time


if __name__ == "__main__":
    # Example 1: expected 3
    root1 = TreeNode(1)
    root1.left = TreeNode(2)
    root1.right = TreeNode(3)
    root1.left.left = TreeNode(4)
    root1.right.left = TreeNode(5)
    root1.right.right = TreeNode(6)
    root1.left.left.right = TreeNode(7)

    print("Example 1:", minTimeToBurn(root1, 1))  # 3

    # Example 2: expected 4
    root2 = TreeNode(1)
    root2.left = TreeNode(2)
    root2.right = TreeNode(3)
    root2.left.right = TreeNode(5)
    root2.right.right = TreeNode(4)

    print("Example 2:", minTimeToBurn(root2, 4))  # 4
