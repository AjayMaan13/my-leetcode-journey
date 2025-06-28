"""
LeetCode 189. Rotate Array
Difficulty: Medium

📜 Problem Statement:
Given an integer array nums, rotate the array to the right by k steps, where k is non-negative.

✍️ Example 1:
Input: nums = [1,2,3,4,5,6,7], k = 3
Output: [5,6,7,1,2,3,4]
Explanation:
rotate 1 step to the right: [7,1,2,3,4,5,6]
rotate 2 steps to the right: [6,7,1,2,3,4,5]
rotate 3 steps to the right: [5,6,7,1,2,3,4]

✍️ Example 2:
Input: nums = [-1,-100,3,99], k = 2
Output: [3,99,-1,-100]
Explanation:
rotate 1 step to the right: [99,-1,-100,3]
rotate 2 steps to the right: [3,99,-1,-100]

✅ Constraints:
- 1 <= nums.length <= 10^5
- -2^31 <= nums[i] <= 2^31 - 1
- 0 <= k <= 10^5

🚀 Follow Up:
- Try to come up with as many solutions as you can.
- There are at least three different ways to solve this problem.
- Can you do it in-place with O(1) extra space?
"""


# 🔥 Solution 1 — Reverse Method (without helper function)
# Time Complexity: O(n)
# Space Complexity: O(1) (in-place)
def rotate_reverse(nums, k):
    k %= len(nums)
    n = len(nums)

    # Reverse the entire array
    left, right = 0, n - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1

    # Reverse first k elements
    left, right = 0, k - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1

    # Reverse the rest
    left, right = k, n - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1


# 🔥 Solution 2 — Reverse Method (with helper function)
# Time Complexity: O(n)
# Space Complexity: O(1) (in-place)
def rotate_reverse_with_helper(nums, k):
    k %= len(nums)
    n = len(nums)

    def reverse(start, end):
        while start < end:
            nums[start], nums[end] = nums[end], nums[start]
            start += 1
            end -= 1

    reverse(0, n - 1)
    reverse(0, k - 1)
    reverse(k, n - 1)


# 🔥 Solution 3 — Extra Array Copy Method
# Time Complexity: O(n)
# Space Complexity: O(n)
def rotate_extra_array(nums, k):
    n = len(nums)
    k %= n
    temp = nums[:]

    for i in range(n):
        nums[(i + k) % n] = temp[i]


# 🔥 Solution 4 — Cycle Replacement Method
# Time Complexity: O(n)
# Space Complexity: O(1) (in-place)
def rotate_cycle(nums, k):
    n = len(nums)
    k %= n
    count = 0

    for start in range(n):
        if count >= n:
            break

        current = start
        prev = nums[start]

        while True:
            next_idx = (current + k) % n
            nums[next_idx], prev = prev, nums[next_idx]
            current = next_idx
            count += 1

            if start == current:
                break


# ✅ Main function to test all solutions
def main():
    nums_list = [
        [1, 2, 3, 4, 5, 6, 7],
        [-1, -100, 3, 99]
    ]
    k_list = [3, 2]

    print("===== Testing Rotate Array Solutions =====\n")

    for nums, k in zip(nums_list, k_list):
        print(f"Original Array: {nums}")
        print(f"k = {k}\n")

        for func in [
            rotate_reverse,
            rotate_reverse_with_helper,
            rotate_extra_array,
            rotate_cycle,
        ]:
            nums_copy = nums[:]  # Copy array to avoid modifying original
            func(nums_copy, k)
            print(f"{func.__name__}: {nums_copy}")

        print("\n----------------------------------------\n")


if __name__ == "__main__":
    main()
