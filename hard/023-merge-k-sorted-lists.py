"""
23. MERGE K SORTED LISTS

Problem Statement:
You are given an array of k linked-lists lists, each linked-list is sorted
in ascending order. Merge all the linked-lists into one sorted linked-list
and return it.

Example 1:
Input: lists = [[1,4,5],[1,3,4],[2,6]]
Output: [1,1,2,3,4,4,5,6]

Example 2:
Input: lists = []
Output: []

Example 3:
Input: lists = [[]]
Output: []

Constraints:
* k == lists.length
* 0 <= k <= 10^4
* 0 <= lists[i].length <= 500
* -10^4 <= lists[i][j] <= 10^4
* lists[i] is sorted in ascending order
* The sum of lists[i].length will not exceed 10^4
"""

import heapq

# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ==============================================================================
# SOLUTION 1: BRUTE FORCE — Collect All Values & Sort
# ==============================================================================
# Time Complexity: O(N log N) — sorting all N values
# Space Complexity: O(N) — stores all values + creates new nodes

class Solution_Brute:
    def mergeKLists(self, lists):
        """
        Dump all values into an array, sort it, rebuild the list.

        Pros: Dead simple to implement
        Cons: Creates new nodes, O(N) space, doesn't reuse original list
        """
        nodes = []
        for l in lists:
            while l:
                nodes.append(l.val)
                l = l.next

        dummy = ListNode(0)
        head = dummy
        for val in sorted(nodes):
            head.next = ListNode(val)
            head = head.next
        return dummy.next


# ==============================================================================
# SOLUTION 2: COMPARE K HEADS ONE BY ONE
# ==============================================================================
# Time Complexity: O(N * k) — for each of N nodes, scan all k list heads
# Space Complexity: O(1)

class Solution_KHeads:
    def mergeKLists(self, lists):
        """
        At each step, find the minimum among all k current heads.

        Pros: O(1) space
        Cons: Slow when k is large (e.g. 10,000 lists)
        """
        dummy = ListNode(0)
        head = dummy

        while True:
            min_val, min_idx = float('inf'), -1
            for i, l in enumerate(lists):
                if l and l.val < min_val:
                    min_val, min_idx = l.val, i

            if min_idx == -1:
                break

            head.next = lists[min_idx]
            head = head.next
            lists[min_idx] = lists[min_idx].next

        return dummy.next


# ==============================================================================
# SOLUTION 3: MERGE LISTS ONE BY ONE (SEQUENTIAL)
# ==============================================================================
# Time Complexity: O(N * k) — first list gets touched k times in worst case
# Space Complexity: O(1)

class Solution_Sequential:
    def mergeKLists(self, lists):
        """
        Merge pairs sequentially: merge(L0, L1), then merge(result, L2), etc.

        Pros: Simple to reason about
        Cons: Still O(N*k) because the running result grows with each merge
        """
        def mergeTwoLists(l1, l2):
            dummy = ListNode(0)
            head = dummy
            while l1 and l2:
                if l1.val <= l2.val:
                    head.next, l1 = l1, l1.next
                else:
                    head.next, l2 = l2, l2.next
                head = head.next
            head.next = l1 or l2
            return dummy.next

        if not lists:
            return None
        result = lists[0]
        for i in range(1, len(lists)):
            result = mergeTwoLists(result, lists[i])
        return result


# ==============================================================================
# SOLUTION 4: DIVIDE & CONQUER
# ==============================================================================
# Time Complexity: O(N log k) — log k rounds, each touching N nodes total
# Space Complexity: O(1)
#
# Like merge sort: merge lists in pairs, halving the problem each round.
# Round 1: k   lists → k/2 merged lists
# Round 2: k/2 lists → k/4 merged lists
# ...
# log k rounds total

class Solution_DivideConquer:
    def mergeKLists(self, lists):
        """
        Merge lists in pairs iteratively until one remains.

        Visual (k=4 lists: A B C D):
          Round 1: merge(A,B)=AB  merge(C,D)=CD
          Round 2: merge(AB,CD)=ABCD
        """
        def mergeTwoLists(l1, l2):
            dummy = ListNode(0)
            head = dummy
            while l1 and l2:
                if l1.val <= l2.val:
                    head.next, l1 = l1, l1.next
                else:
                    head.next, l2 = l2, l2.next
                head = head.next
            head.next = l1 or l2
            return dummy.next

        if not lists:
            return None

        while len(lists) > 1:
            merged = []
            for i in range(0, len(lists), 2):
                l1 = lists[i]
                l2 = lists[i + 1] if i + 1 < len(lists) else None
                merged.append(mergeTwoLists(l1, l2))
            lists = merged

        return lists[0]


# ==============================================================================
# SOLUTION 5: MIN HEAP (YOUR SOLUTION — OPTIMAL)
# ==============================================================================
# Time Complexity: O(N log k) — each of N nodes: one push + one pop = O(log k)
# Space Complexity: O(k) — heap holds at most k nodes at once
#
# Key insight: maintain a heap of size k (one entry per list).
# Always extract the global minimum in O(log k), push its successor.

class Solution:
    def mergeKLists(self, lists):
        """
        Use a min-heap to always pick the smallest current head across all lists.

        Why `i` (list index) in the tuple?
        Python can't compare ListNode objects, so when two nodes have equal .val,
        the heap tries to compare the next element — which would crash on ListNode.
        Using `i` as a tiebreaker prevents that comparison entirely.

        Heap tuple: (node.val, list_index, node)
        """
        heap = []
        dummy = ListNode(0)
        head = dummy

        # Push the first node of each non-empty list
        for i, l in enumerate(lists):
            if l:
                heapq.heappush(heap, (l.val, i, l))

        while heap:
            val, i, node = heapq.heappop(heap)
            head.next = node
            head = node
            if node.next:
                heapq.heappush(heap, (node.next.val, i, node.next))

        return dummy.next


# ==============================================================================
# COMPARISON
# ==============================================================================

"""
| Approach              | Time        | Space  | Notes                          |
|-----------------------|-------------|--------|--------------------------------|
| Brute (collect+sort)  | O(N log N)  | O(N)   | Simple but wasteful            |
| Compare k heads       | O(N·k)      | O(1)   | Slow for large k               |
| Merge one by one      | O(N·k)      | O(1)   | Better but same complexity     |
| Divide & Conquer      | O(N log k)  | O(1)   | Optimal space                  |
| Min Heap (yours) ⭐   | O(N log k)  | O(k)   | Optimal, clean, interview-ready|

Both Divide & Conquer and Min Heap are optimal at O(N log k).
Heap is more intuitive; D&C uses less space.
"""


# ==============================================================================
# TESTING
# ==============================================================================

if __name__ == "__main__":
    def create_list(vals):
        if not vals:
            return None
        head = ListNode(vals[0])
        curr = head
        for v in vals[1:]:
            curr.next = ListNode(v)
            curr = curr.next
        return head

    def to_array(head):
        vals = []
        while head:
            vals.append(head.val)
            head = head.next
        return vals

    test_cases = [
        ([[1,4,5],[1,3,4],[2,6]], [1,1,2,3,4,4,5,6]),
        ([], []),
        ([[]], []),
        ([[1],[0]], [0,1]),
    ]

    sol = Solution()
    print("Testing Min Heap Solution:")
    print("=" * 50)
    for lists_vals, expected in test_cases:
        lists = [create_list(v) for v in lists_vals]
        result = to_array(sol.mergeKLists(lists))
        status = "PASS" if result == expected else "FAIL"
        print(f"Input:    {lists_vals}")
        print(f"Output:   {result}")
        print(f"Expected: {expected}")
        print(f"[{status}]\n")
