"""
LeetCode 1. Two Sum
https://leetcode.com/problems/two-sum/
Difficulty: Easy

Intuition:
    For every number, I need its partner: target - n.
    Searching the list again for it is slow.
    So I remember every number I've seen in a dict (number -> index).
    If the partner is already in the dict, that's the pair.

Complexity:
    Time:  O(n)  - one pass
    Space: O(n)  - the dict
"""


class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen = {}

        for i, n in enumerate(nums):
            complement = target - n
            if complement in seen:
                return [seen[complement], i]
            seen[n] = i


if __name__ == "__main__":
    sol = Solution()
    assert sol.twoSum([2, 7, 11, 15], 9) == [0, 1]
    assert sol.twoSum([3, 2, 4], 6) == [1, 2]
    assert sol.twoSum([3, 3], 6) == [0, 1]
    assert sol.twoSum([-3, 4, 3, 90], 0) == [0, 2]
    print("All tests passed.")
