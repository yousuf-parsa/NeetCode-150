"""
LeetCode 167. Two Sum II - Input Array Is Sorted
https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/
Difficulty: Medium

Intuition:
    The array is sorted, so I put left at the smallest and right at the biggest.
    Sum too small -> move left up to get a bigger number.
    Sum too big -> move right down to get a smaller number.
    Equal -> found it (answer is 1-indexed).

Complexity:
    Time:  O(n)  - each pointer moves at most n times
    Space: O(1)  - two pointers
"""


class Solution:
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        left, right = 0, len(numbers) - 1

        while left < right:
            if numbers[left] + numbers[right] < target:
                left += 1
            elif numbers[left] + numbers[right] > target:
                right -= 1
            else:
                return [left + 1, right + 1]

        return []


if __name__ == "__main__":
    sol = Solution()
    assert sol.twoSum([2, 7, 11, 15], 9) == [1, 2]
    assert sol.twoSum([2, 3, 4], 6) == [1, 3]
    assert sol.twoSum([-1, 0], -1) == [1, 2]
    assert sol.twoSum([1, 2, 3, 4, 4, 9, 56, 90], 8) == [4, 5]
    print("All tests passed.")
