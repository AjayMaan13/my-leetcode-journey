"""
ALLOCATE MINIMUM NUMBER OF PAGES

Problem Statement:
Given an array 'arr' of integer numbers, 'arr[i]' represents the number of pages 
in the 'i-th' book. There are 'm' number of students, and the task is to allocate 
all the books to the students.

Allocate books in such a way that:
- Each student gets at least one book.
- Each book should be allocated to only one student.
- Book allocation should be in a contiguous manner.

You have to allocate the book to 'm' students such that the maximum number of 
pages assigned to a student is minimum. If the allocation of books is not 
possible, return -1.

Example 1:
Input: n = 4, m = 2, arr[] = {12, 34, 67, 90}
Output: 113
Explanation: The allocation of books will be 12, 34, 67 | 90. One student will 
get the first 3 books and the other will get the last one.

Example 2:
Input: n = 5, m = 4, arr[] = {25, 46, 28, 49, 24}
Output: 71
Explanation: The allocation of books will be 25, 46 | 28 | 49 | 24.
"""


# ==============================================================================
# APPROACH 1: BRUTE FORCE
# ==============================================================================
# Time Complexity: O(N * (sum - max))
# Space Complexity: O(1)
#
# Intuition: Try every possible value from max(arr) to sum(arr) and find the
# first value where we can allocate books to exactly m students.

def countStudents_brute(arr, pages):
    """
    Count how many students are needed if each student can read max 'pages'
    
    Logic: Greedily assign books to current student until adding next book
    would exceed 'pages' limit, then move to next student.
    """
    n = len(arr)
    students = 1  # Start with first student
    pagesStudent = 0  # Pages currently assigned to this student
    
    for i in range(n):
        # Can current student handle this book?
        if pagesStudent + arr[i] <= pages:
            # Yes, add pages to current student
            pagesStudent += arr[i]
        else:
            # No, need a new student for this book
            students += 1
            pagesStudent = arr[i]  # New student starts with this book
    
    return students


def findPages_bruteforce(arr, n, m):
    """
    Find minimum of maximum pages allocated to any student (Brute Force)
    
    Approach: Test every possible maximum from max(arr) to sum(arr).
    The first value that allows exactly m students is our answer.
    """
    # Edge case: More students than books? Impossible!
    if m > n:
        return -1

    # Define search range:
    low = max(arr)   # Minimum possible: largest single book
    high = sum(arr)  # Maximum possible: all books to one student

    # Try each possible maximum page count
    for pages in range(low, high + 1):
        # Check how many students needed for this max
        if countStudents_brute(arr, pages) == m:
            return pages  # Found the minimum maximum!
    
    return low  # Fallback (shouldn't reach here normally)


# ==============================================================================
# APPROACH 2: BINARY SEARCH (OPTIMAL)
# ==============================================================================
# Time Complexity: O(N * log(sum - max))
# Space Complexity: O(1)
#
# Intuition: Answer space is sorted. If 'x' pages works for m students,
# then any value > x also works. If 'x' doesn't work, values < x won't work.
# This monotonic property allows binary search on the answer!

def countStudents(arr, pages):
    """
    Count how many students are needed if each student can read max 'pages'
    
    Logic: Greedily assign books to current student until adding next book
    would exceed 'pages' limit, then move to next student.
    """
    n = len(arr)
    students = 1  # Start with first student
    pagesStudent = 0  # Pages currently assigned to this student
    
    for i in range(n):
        # Can current student handle this book?
        if pagesStudent + arr[i] <= pages:
            # Yes, add pages to current student
            pagesStudent += arr[i]
        else:
            # No, need a new student for this book
            students += 1
            pagesStudent = arr[i]  # New student starts with this book
    
    return students


def findPages(arr, n, m):
    """
    Find minimum of maximum pages allocated to any student (Binary Search)
    
    Approach: Binary search on answer space (max pages per student).
    We eliminate half the search space each iteration.
    """
    # Edge case: More students than books? Impossible!
    if m > n:
        return -1

    # Define search space:
    low = max(arr)   # Minimum possible: largest single book (every student needs ≥1 book)
    high = sum(arr)  # Maximum possible: all books to one student
    
    # Binary search on the answer space
    while low <= high:
        mid = (low + high) // 2  # Try this as max pages per student
        
        # How many students needed if max is 'mid' pages?
        students = countStudents(arr, mid)
        
        if students > m:
            # Too many students needed! Max is too low.
            # We need to increase the max pages per student.
            low = mid + 1  # Search right half (larger values)
        else:
            # students <= m: This max works! But can we do better?
            # Try to find a smaller max (minimize the maximum).
            high = mid - 1  # Search left half (smaller values)
    
    # When loop ends, low points to the smallest valid answer
    # (the minimum of maximum pages)
    return low
