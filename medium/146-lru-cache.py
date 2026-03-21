# 146. LRU Cache (Medium)
# Tags: Design, Doubly Linked List, Hash Map
#
# Design a cache that evicts the Least Recently Used key when over capacity.
# get(key)        → return value or -1; mark key as recently used
# put(key, value) → insert/update; if over capacity evict the LRU key
# Both operations must run in O(1) average time.


# ─────────────────────────────────────────────
# BRUTE FORCE — OrderedDict — O(1) amortized, O(n) space
# ─────────────────────────────────────────────
# Python's OrderedDict remembers insertion order AND supports move_to_end().
# Use the front (oldest) as LRU and the back (newest) as MRU.
#
# get  → move accessed key to back (MRU)
# put  → move updated key to back; if new and over cap, pop front (LRU)
#
# This works but uses a built-in that hides the real mechanics.
# Interviewers usually want you to implement the underlying structure yourself.

from collections import OrderedDict

class LRUCacheBrute:
    def __init__(self, capacity):
        self.cap = capacity
        self.cache = OrderedDict()   # key → value, ordered LRU→MRU

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)  # mark as most recently used
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)  # refresh position
        self.cache[key] = value
        if len(self.cache) > self.cap:
            self.cache.popitem(last=False)  # evict LRU (front)


# ─────────────────────────────────────────────
# OPTIMAL — HashMap + Doubly Linked List — O(1) true, O(n) space
# ─────────────────────────────────────────────
# This is the classic from-scratch implementation.
#
# WHY doubly linked list?
#   - O(1) insert and remove from any position (given the node pointer)
#   - We maintain: LEFT dummy (LRU end) ↔ ... nodes ... ↔ RIGHT dummy (MRU end)
#   - Most recently used → always inserted at RIGHT (next to right dummy)
#   - Least recently used → always at LEFT.next
#
# WHY hash map?
#   - O(1) lookup: key → node pointer in the list
#   - Without this, finding a node in the list is O(n)
#
# Together: map gives us the node instantly, list lets us reorder in O(1).
#
# Diagram (cap=3, after puts 1,2,3 and get(1)):
#   LEFT ↔ [2] ↔ [3] ↔ [1] ↔ RIGHT
#             LRU              MRU
#
# Operations:
#   get(key):
#     - not found → return -1
#     - found     → remove node, re-insert at MRU end, return value
#
#   put(key, value):
#     - exists    → remove old node (to re-insert fresh)
#     - create new node, insert at MRU end, add to map
#     - over cap  → evict LEFT.next (LRU), delete from map

class Node:
    def __init__(self, key, val):
        self.key  = key
        self.val  = val
        self.prev = None
        self.next = None

class LRUCache(object):

    def __init__(self, capacity):
        self.cap   = capacity
        self.cache = {}              # key → Node

        # sentinel dummies so we never have to handle edge cases (empty list, etc.)
        self.left  = Node(0, 0)     # LRU side (oldest is left.next)
        self.right = Node(0, 0)     # MRU side (newest is right.prev)

        self.left.next  = self.right
        self.right.prev = self.left

    def _remove(self, node):
        # unlink node from wherever it sits in the list
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert(self, node):
        # insert node just before the right dummy (= MRU position)
        prev       = self.right.prev
        prev.next  = node
        node.prev  = prev
        node.next  = self.right
        self.right.prev = node

    def get(self, key):
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)    # take it out of its current position
        self._insert(node)    # re-insert at MRU end (marks as recently used)
        return node.val

    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])   # remove stale node

        node = Node(key, value)
        self.cache[key] = node
        self._insert(node)                  # place at MRU end

        if len(self.cache) > self.cap:
            lru = self.left.next            # oldest node is right after left dummy
            self._remove(lru)
            del self.cache[lru.key]         # clean up map too


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key, value)
