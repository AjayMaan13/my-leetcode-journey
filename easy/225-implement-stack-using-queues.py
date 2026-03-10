"""
225. Implement Stack using Queues

Implement a last-in-first-out (LIFO) stack using only two queues.
The implemented stack should support all the functions of a normal stack
(push, top, pop, and empty).

Valid queue operations ONLY:
- push to back
- peek/pop from front
- size
- is empty

Example:
Input:  ["MyStack", "push", "push", "top", "pop", "empty"]
        [[], [1], [2], [], [], []]
Output: [null, null, null, 2, 2, false]

Constraints:
- 1 <= x <= 9
- At most 100 calls will be made to push, pop, top, and empty.

Follow-up: Can you implement the stack using only one queue?
"""

# ===== My Original Solution (VIOLATES CONSTRAINTS) =====
# ❌ Uses list.pop() and list[-1] — these access the END of the list,
#    which is NOT a valid queue operation. A queue only allows pop from FRONT.
#    This is essentially just using a stack directly — defeats the problem.

class MyStackOriginal(object):
    def __init__(self):
        self.items = []

    def push(self, x):
        self.items.append(x)

    def pop(self):
        return self.items.pop()                     # ❌ pop from end — not a queue op

    def top(self):
        return self.items[len(self.items) - 1]      # ❌ index access from end — not a queue op

    def empty(self):
        return len(self.items) == 0


# ===== Two-Queue Solution (plain list, valid ops only) =====
# Uses two plain lists but ONLY valid queue ops: append (back), pop(0) (front), len
# Push to q2, drain q1 into q2, swap — top always sits at front of q1
# Time: push O(n), pop O(1), top O(1), empty O(1) | Space: O(n)

class MyStackTwoQueues(object):
    def __init__(self):
        self.q1 = []  # main queue — front is always the stack top
        self.q2 = []  # temp queue used during push

    def push(self, x):
        self.q2.append(x)                       # put new element in temp queue first
        while self.q1:
            self.q2.append(self.q1.pop(0))      # drain main into temp (new elem stays at front)
        self.q1, self.q2 = self.q2, self.q1    # swap: q1 updated, q2 reset to empty

    def pop(self):
        return self.q1.pop(0)   # top of stack is at front of queue

    def top(self):
        return self.q1[0]       # peek front

    def empty(self):
        return len(self.q1) == 0


# ===== Two-Queue Solution (using collections.deque) =====
# Same logic as above but deque makes popleft() O(1) instead of O(n)
# Time: push O(n), pop O(1), top O(1), empty O(1) | Space: O(n)

from collections import deque

class MyStackTwoQueuesDeque(object):
    def __init__(self):
        self.q1 = deque()  # main queue — front(left) is always the stack top
        self.q2 = deque()  # temp queue used during push

    def push(self, x):
        self.q2.append(x)                        # put new element in temp queue first
        while self.q1:
            self.q2.append(self.q1.popleft())    # drain main into temp (new elem stays at front)
        self.q1, self.q2 = self.q2, self.q1     # swap: q1 updated, q2 reset to empty

    def pop(self):
        return self.q1.popleft()  # top of stack is at front of queue

    def top(self):
        return self.q1[0]         # peek front

    def empty(self):
        return len(self.q1) == 0


# ===== Follow-up: Single Queue Solution (using collections.deque) =====
# After each push, rotate all PREVIOUS elements to the back
# so the newest element always ends up at the front (stack top)
# Time: push O(n), pop O(1), top O(1), empty O(1) | Space: O(n)

class MyStackOneQueue(object):
    def __init__(self):
        self.q = deque()  # single queue — front always holds stack top

    def push(self, x):
        self.q.append(x)                          # add new element to back
        for _ in range(len(self.q) - 1):
            self.q.append(self.q.popleft())        # rotate all previous elements to back

    def pop(self):
        return self.q.popleft()   # top is always at front

    def top(self):
        return self.q[0]          # peek front

    def empty(self):
        return len(self.q) == 0


# ===== Test Cases =====
if __name__ == "__main__":
    solutions = [
        ("TwoQueues (plain list)", MyStackTwoQueues),
        ("TwoQueues (deque)", MyStackTwoQueuesDeque),
        ("OneQueue (deque) - Follow-up", MyStackOneQueue),
    ]

    for name, MyStack in solutions:
        print(f"\nTesting {name}:")
        stack = MyStack()
        stack.push(1)
        stack.push(2)
        print(f"top()   = {stack.top()}    (expected 2)")
        print(f"pop()   = {stack.pop()}    (expected 2)")
        print(f"empty() = {stack.empty()}  (expected False)")
        stack.pop()
        print(f"empty() = {stack.empty()}  (expected True)")
