"""
232. Implement Queue using Stacks

Implement a first in first out (FIFO) queue using only two stacks.
The implemented queue should support all the functions of a normal queue
(push, peek, pop, and empty).

Valid stack operations ONLY:
- push to top
- peek/pop from top
- size
- is empty

Example:
Input:  ["MyQueue", "push", "push", "peek", "pop", "empty"]
        [[], [1], [2], [], [], []]
Output: [null, null, null, 1, 1, false]

Constraints:
- 1 <= x <= 9
- At most 100 calls will be made to push, pop, peek, and empty.

Follow-up: Can you implement the queue such that each operation is
amortized O(1)? (n operations take O(n) total even if one takes longer)
"""

# ===== My Original Solution (✅ Correct, O(n) push) =====
# Uses two stacks. On every push: dump s1 → s2, push new, dump s2 → s1.
# This keeps the front of queue at the TOP of s1, so pop/peek are O(1).
# Downside: every push is O(n) because of two full transfers.

class MyQueueOriginal(object):
    def __init__(self):
        self.s1 = []  # main stack — top is always the queue front
        self.s2 = []  # temp stack used during push

    def push(self, x):
        while self.s1:
            self.s2.append(self.s1.pop())   # dump s1 into s2 (reverses order)
        self.s1.append(x)                   # push new element (now at bottom)
        while self.s2:
            self.s1.append(self.s2.pop())   # dump s2 back into s1 (new elem at bottom, old front at top)

    def pop(self):
        return self.s1.pop()                # front of queue is at top of s1

    def peek(self):
        return self.s1[len(self.s1) - 1]   # peek top of s1 = queue front

    def empty(self):
        return len(self.s1) == 0


# ===== Two-Stack Solution (using collections.deque as stack) =====
# Same O(n) push logic as above, but uses deque for clarity
# deque used as STACK: append (push to top), pop (pop from top)
# Time: push O(n), pop O(1), peek O(1), empty O(1) | Space: O(n)

from collections import deque

class MyQueueTwoStacks(object):
    def __init__(self):
        self.s1 = deque()  # main stack — top(right) is always the queue front
        self.s2 = deque()  # temp stack used during push

    def push(self, x):
        while self.s1:
            self.s2.append(self.s1.pop())   # dump s1 into s2
        self.s1.append(x)                   # push new element (will end up at bottom)
        while self.s2:
            self.s1.append(self.s2.pop())   # dump s2 back — old front returns to top

    def pop(self):
        return self.s1.pop()    # front of queue is at top of s1

    def peek(self):
        return self.s1[-1]      # peek top of s1 = queue front

    def empty(self):
        return len(self.s1) == 0


# ===== Follow-up: Amortized O(1) — Lazy Transfer =====
# Key insight: don't transfer on every push — only transfer when outbox is empty.
# inbox  → receives all pushes (O(1) each)
# outbox → serves all pops/peeks; when empty, dump entire inbox into it (reverses order)
# Each element is moved at most ONCE total → amortized O(1) per operation
# Time: push O(1), pop amortized O(1), peek amortized O(1), empty O(1) | Space: O(n)

class MyQueueAmortized(object):
    def __init__(self):
        self.inbox  = []  # new elements always pushed here
        self.outbox = []  # elements served from here (reversed order = correct FIFO)

    def push(self, x):
        self.inbox.append(x)    # always O(1) — just push to inbox

    def _transfer(self):
        if not self.outbox:                         # only transfer when outbox is empty
            while self.inbox:
                self.outbox.append(self.inbox.pop()) # reverse inbox into outbox → front is now at top

    def pop(self):
        self._transfer()
        return self.outbox.pop()    # top of outbox = front of queue

    def peek(self):
        self._transfer()
        return self.outbox[-1]      # peek top of outbox = front of queue

    def empty(self):
        return not self.inbox and not self.outbox   # empty only if both stacks are empty


# ===== Test Cases =====
if __name__ == "__main__":
    solutions = [
        ("Original (O(n) push)", MyQueueOriginal),
        ("TwoStacks (deque)", MyQueueTwoStacks),
        ("Amortized O(1) - Follow-up", MyQueueAmortized),
    ]

    for name, MyQueue in solutions:
        print(f"\nTesting {name}:")
        q = MyQueue()
        q.push(1)
        q.push(2)
        print(f"peek()  = {q.peek()}    (expected 1)")
        print(f"pop()   = {q.pop()}    (expected 1)")
        print(f"empty() = {q.empty()}  (expected False)")
        q.pop()
        print(f"empty() = {q.empty()}  (expected True)")
