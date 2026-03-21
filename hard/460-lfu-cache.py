# 460. LFU Cache (Hard)
# Tags: Design, Doubly Linked List, Hash Map, Ordered Dict
#
# Eviction policy: remove the LEAST FREQUENTLY USED key.
# Tie-break: among keys with the same frequency, evict the LEAST RECENTLY USED.
# get and put must both run in O(1) average time.


# ─────────────────────────────────────────────
# BRUTE FORCE — O(n) per put, O(1) get — O(n) space
# ─────────────────────────────────────────────
# Store key→val and key→freq in plain dicts.
# On eviction, scan all keys to find the minimum frequency,
# then among those pick the one that was used least recently (tracked by order).
# Simple but O(n) per eviction — not acceptable for large caches.

class LFUCacheBrute:
    def __init__(self, capacity):
        self.cap     = capacity
        self.vals    = {}        # key → value
        self.freqs   = {}        # key → frequency
        self.order   = []        # insertion/access order (LRU within same freq)

    def _touch(self, key):
        self.freqs[key] = self.freqs.get(key, 0) + 1
        if key in self.order:
            self.order.remove(key)
        self.order.append(key)   # most recently used goes to end

    def get(self, key):
        if key not in self.vals:
            return -1
        self._touch(key)
        return self.vals[key]

    def put(self, key, value):
        if self.cap == 0:
            return
        if key not in self.vals and len(self.vals) == self.cap:
            # find LFU key (O(n) scan); among ties pick LRU (earliest in order)
            min_freq = min(self.freqs[k] for k in self.order)
            for k in self.order:                    # order is LRU→MRU
                if self.freqs[k] == min_freq:
                    self.order.remove(k)
                    del self.vals[k]
                    del self.freqs[k]
                    break
        self.vals[key] = value
        self._touch(key)


# ─────────────────────────────────────────────
# SOLUTION 1 — Custom Doubly Linked List per freq bucket — O(1) true
# ─────────────────────────────────────────────
# Three maps:
#   valMap   : key → value
#   countMap : key → current frequency
#   listMap  : freq → DoublyLinkedList of keys (LRU at left, MRU at right)
#
# Each freq bucket is its own doubly linked list so we can:
#   - O(1) remove a key from its current freq bucket
#   - O(1) push it to the tail (MRU) of the next freq bucket
#
# lfuCnt tracks the minimum frequency in the cache at all times.
# When a bucket becomes empty AND its freq == lfuCnt, increment lfuCnt.
# On eviction, pop the leftmost (LRU) key from listMap[lfuCnt].
#
# counter(key) handles the freq promotion logic shared by get and put.

from collections import defaultdict

class ListNode:
    def __init__(self, val):
        self.val  = val
        self.prev = None
        self.next = None

class LinkedList:
    def __init__(self):
        self.left  = ListNode(0)   # dummy head (LRU side)
        self.right = ListNode(0)   # dummy tail (MRU side)
        self.left.next  = self.right
        self.right.prev = self.left
        self.map = {}              # val → node (for O(1) removal)

    def length(self):
        return len(self.map)

    def pushRight(self, val):
        # insert at MRU end
        node      = ListNode(val)
        prev      = self.right.prev
        prev.next = node
        node.prev = prev
        node.next = self.right
        self.right.prev  = node
        self.map[val]    = node

    def pop(self, val):
        # remove a specific node by val in O(1) using the internal map
        if val in self.map:
            node      = self.map[val]
            node.prev.next = node.next
            node.next.prev = node.prev
            del self.map[val]

    def popLeft(self):
        # evict LRU: the node right after the dummy head
        if self.left.next == self.right:
            return None
        val = self.left.next.val
        self.pop(val)
        return val

    def update(self, val):
        self.pop(val)
        self.pushRight(val)  # move to MRU end (refresh within same bucket)


class LFUCache(object):

    def __init__(self, capacity):
        self.cap      = capacity
        self.lfuCnt   = 0                          # current minimum frequency
        self.valMap   = {}                         # key → value
        self.countMap = defaultdict(int)           # key → freq
        self.listMap  = defaultdict(LinkedList)    # freq → LinkedList of keys

    def _promote(self, key):
        # move key from its current freq bucket to freq+1 bucket
        cnt = self.countMap[key]
        self.countMap[key] += 1

        self.listMap[cnt].pop(key)              # remove from old bucket
        self.listMap[cnt + 1].pushRight(key)    # push to MRU end of new bucket

        # if old bucket is now empty and was the minimum, bump lfuCnt
        if cnt == self.lfuCnt and self.listMap[cnt].length() == 0:
            self.lfuCnt += 1

    def get(self, key):
        if key not in self.valMap:
            return -1
        self._promote(key)
        return self.valMap[key]

    def put(self, key, value):
        if self.cap == 0:
            return

        if key not in self.valMap and len(self.valMap) == self.cap:
            # evict the LRU key from the lowest-frequency bucket
            lru = self.listMap[self.lfuCnt].popLeft()
            del self.valMap[lru]
            del self.countMap[lru]

        self.valMap[key] = value
        self._promote(key)
        # new key starts at freq 1 after _promote; if it's a fresh insert,
        # lfuCnt must be 1 (a new key always has the lowest freq)
        self.lfuCnt = min(self.lfuCnt, self.countMap[key])


# ─────────────────────────────────────────────
# SOLUTION 2 — OrderedDict per freq bucket — O(1) amortized, Pythonic
# ─────────────────────────────────────────────
# Same three-map idea but uses OrderedDict instead of a custom linked list.
# OrderedDict preserves insertion order AND supports popitem(last=False) to
# evict the oldest (LRU) entry in O(1).
#
# Slightly less code, but hides the underlying linked list mechanics.
# In an interview, prefer Solution 1 to show you understand the internals.
#
# Clever trick in put: if key already exists, call self.get(key) to reuse
# the frequency-promotion logic rather than duplicating it.

from collections import defaultdict, OrderedDict

class LFUCache2:

    def __init__(self, capacity):
        self.cap         = capacity
        self.minFreq     = 0
        self.keyToVal    = {}                           # key → value
        self.keyToFreq   = {}                           # key → frequency
        self.freqToKeys  = defaultdict(OrderedDict)    # freq → {key: None} ordered LRU→MRU

    def get(self, key):
        if key not in self.keyToVal:
            return -1

        freq = self.keyToFreq[key]
        del self.freqToKeys[freq][key]           # remove from current freq bucket

        if not self.freqToKeys[freq]:            # bucket now empty
            del self.freqToKeys[freq]
            if self.minFreq == freq:             # if it was the minimum, bump up
                self.minFreq += 1

        self.keyToFreq[key] += 1
        self.freqToKeys[freq + 1][key] = None    # insert at MRU end of next bucket

        return self.keyToVal[key]

    def put(self, key, value):
        if self.cap == 0:
            return

        if key in self.keyToVal:
            self.keyToVal[key] = value
            self.get(key)        # reuse get's promotion logic; return value ignored
            return

        if len(self.keyToVal) == self.cap:
            # evict LRU from the minimum-frequency bucket
            lru_key, _ = self.freqToKeys[self.minFreq].popitem(last=False)
            del self.keyToVal[lru_key]
            del self.keyToFreq[lru_key]

        self.keyToVal[key]          = value
        self.keyToFreq[key]         = 1
        self.freqToKeys[1][key]     = None   # brand new key → freq 1, MRU in bucket
        self.minFreq                = 1      # new key always resets minimum to 1


# Your LFUCache object will be instantiated and called as such:
# obj = LFUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
