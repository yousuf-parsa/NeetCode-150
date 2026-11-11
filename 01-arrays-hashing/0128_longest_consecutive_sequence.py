"""
LeetCode 128. Longest Consecutive Sequence
https://leetcode.com/problems/longest-consecutive-sequence/
Difficulty: Medium

Intuition:
    Sorting would work but costs O(n log n).
    I put all numbers in a set so lookups are O(1).
    A number x starts a sequence only if x - 1 is NOT in the set.
    From each start, I count x+1, x+2, ... while they exist, and keep the longest.

Complexity:
    Time:  O(n)  - each number is counted in only one sequence
    Space: O(n)  - the set
"""


class Solution:
    def longestConsecutive(self, nums: list[int]) -> int:
        r = set(nums)
        best = 0
        for x in r:
            if x - 1 not in r:
                length = 1
                while x + length in r:
                    length += 1
                best = max(best, length)

        return best


if __name__ == "__main__":
    sol = Solution()
    assert sol.longestConsecutive([100, 4, 200, 1, 3, 2]) == 4
    assert sol.longestConsecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
    assert sol.longestConsecutive([]) == 0
    assert sol.longestConsecutive([1, 0, 1, 2]) == 3
    assert sol.longestConsecutive([-1, -2, 5]) == 2
    print("All tests passed.")
