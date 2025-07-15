# test_symmetric_tree.py

# TreeNode definition
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Import your solution here
# from your_solution_file import Solution

# Create test trees
def build_tree1():
    # Symmetric tree: [1,2,2,3,4,4,3]
    return TreeNode(1,
        TreeNode(2, TreeNode(3), TreeNode(4)),
        TreeNode(2, TreeNode(4), TreeNode(3))
    )

def build_tree2():
    # Not symmetric: [1,2,2,null,3,null,3]
    return TreeNode(1,
        TreeNode(2, None, TreeNode(3)),
        TreeNode(2, None, TreeNode(3))
    )

def build_tree3():
    # Single node
    return TreeNode(1)

def build_tree4():
    # Symmetric: [1,2,2]
    return TreeNode(1, TreeNode(2), TreeNode(2))

def build_tree5():
    # Asymmetric by structure
    return TreeNode(1, TreeNode(2, TreeNode(3)), TreeNode(2))

# Test runner
def run_tests(solution):
    test_cases = [
        (build_tree1(), True),
        (build_tree2(), False),
        (build_tree3(), True),
        (build_tree4(), True),
        (build_tree5(), False),
    ]

    for i, (root, expected) in enumerate(test_cases, 1):
        result = solution.isSymmetric(root)
        print(f"Test case {i}: {'PASS' if result == expected else 'FAIL'} — Expected: {expected}, Got: {result}")

from collections import deque
if __name__ == "__main__":
    # My Solution: Recursive DFS
    class Solution(object):
        def isSymmetric(self, root):
            """
            :type root: Optional[TreeNode]
            :rtype: bool
            """
            def isSymmetricNodes(l, r):
                if not l and not r:
                    return True
                if not l or not r or l.val != r.val:
                    return False
                
                return isSymmetricNodes(l.left, r.right) and  isSymmetricNodes(l.right, r.left)
            
            if not root:
                return True
            return isSymmetricNodes(root.left, root.right)
    
    # Alternate Solution Using BFS
    from collections import deque
    class Solution(object):
        def isSymmetric(self, root):
            if not root:
                return True

            queue = deque([(root.left, root.right)])

            while queue:
                left, right = queue.popleft()

                if not left and not right:
                    continue
                if not left or not right or left.val != right.val:
                    return False

                queue.append((left.left, right.right))
                queue.append((left.right, right.left))

            return True


    run_tests(Solution())
