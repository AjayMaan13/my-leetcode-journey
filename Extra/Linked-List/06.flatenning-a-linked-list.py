"""
Problem Statement: Given a linked list containing 'N' head nodes where every node in the 
linked list contains two pointers:

  - 'Next' points to the next node in the list
  - 'Child' pointer to a linked list where the current node is the head

Each of these child linked lists is in sorted order and connected by a 'child' pointer.
Your task is to flatten this linked list such that all nodes appear in a single layer or 
level in a 'sorted order'.

Example:
    Input:
        5 -> 10 -> 12 -> 7
        |     |     |     |
        14    4    20    17
                    |
                   13

    Output: 4 -> 5 -> 7 -> 10 -> 12 -> 13 -> 14 -> 17 -> 20
"""


class ListNode:
    def __init__(self, val=0, next=None, child=None):
        self.val = val
        self.next = next
        self.child = child


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1: BRUTE FORCE
# Time Complexity  : O(N * M * log(N * M)) — collecting all nodes then sorting
# Space Complexity : O(N * M)              — storing all values in an array
# ─────────────────────────────────────────────────────────────────────────────
class BruteForceSolution:

    def convertArrToLinkedList(self, arr):
        """Convert a sorted array into a linked list connected via child pointers."""
        dummy = ListNode(-1)
        temp = dummy
        for val in arr:
            temp.child = ListNode(val)
            temp = temp.child
        return dummy.child

    def flattenLinkedList(self, head):
        """
        Steps:
          1. Traverse every top-level node (via next) and every child node (via child),
             collecting all values into an array.
          2. Sort the array.
          3. Rebuild and return a new linked list from the sorted array.
        """
        arr = []

        # Traverse the top-level list
        while head is not None:
            t2 = head
            # Traverse each child chain
            while t2 is not None:
                arr.append(t2.val)
                t2 = t2.child
            head = head.next

        arr.sort()  # Sort all collected values
        return self.convertArrToLinkedList(arr)


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: OPTIMAL — Recursive Merge (like Merge Sort on linked lists)
# Time Complexity  : O(N * M)  — each node is visited a constant number of times
# Space Complexity : O(N)      — recursion stack depth equals number of top-level nodes
# ─────────────────────────────────────────────────────────────────────────────
class OptimalSolution:

    def merge(self, list1, list2):
        """
        Merge two sorted linked lists (connected via child pointers) into one
        sorted linked list, also connected via child pointers.
        Works similarly to merging two sorted arrays.
        """
        dummy = ListNode(-1)
        res = dummy

        # Pick the smaller node at each step and attach it via child
        while list1 is not None and list2 is not None:
            if list1.val < list2.val:
                res.child = list1
                res = list1
                list1 = list1.child
            else:
                res.child = list2
                res = list2
                list2 = list2.child
            res.next = None  # Clear next pointer to avoid stale links

        # Attach any remaining nodes
        res.child = list1 if list1 else list2

        # Ensure the first merged node has no next pointer
        if dummy.child:
            dummy.child.next = None

        return dummy.child

    def flattenLinkedList(self, head):
        """
        Steps:
          1. Base case: if head is None or has no next, return head as-is.
          2. Recursively flatten the rest of the list (head.next onward).
          3. Merge the current node's child chain with the already-flattened rest.
          4. Return the merged result.
        """
        # Base case: nothing left to flatten
        if head is None or head.next is None:
            return head

        # Recursively flatten everything after the current head
        mergedHead = self.flattenLinkedList(head.next)

        # Merge current chain with the flattened remainder
        head = self.merge(head, mergedHead)
        return head

