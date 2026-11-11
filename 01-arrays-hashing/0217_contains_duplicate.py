"""
LeetCode 217. Contains Duplicate
https://leetcode.com/problems/contains-duplicate/
Difficulty: Easy

Intuition:
    Comparing every pair is O(n^2), too slow.
    I keep a set of numbers I've already seen.
    If the current number is already in the set, it's a duplicate.
    If I finish the loop without finding one, there are none.

Complexity:
    Time:  O(n)  - one pass, set lookups are O(1)
    Space: O(n)  - the set
"""


class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:

        Set = set()

        for num in nums:
            if num in Set:
                return True
            Set.add(num)

        return False


if __name__ == "__main__":
    sol = Solution()
    assert sol.containsDuplicate([1, 2, 3, 1]) is True
    assert sol.containsDuplicate([1, 2, 3, 4]) is False
    assert sol.containsDuplicate([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]) is True
    assert sol.containsDuplicate([7]) is False
    print("All tests passed.")
