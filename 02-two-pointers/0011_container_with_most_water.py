"""
LeetCode 11. Container With Most Water
https://leetcode.com/problems/container-with-most-water/
Difficulty: Medium

Intuition:
    Trying every pair of lines is too slow.
    I start with the widest container: left at the start, right at the end.
    The shorter line limits the water, so I move the shorter one inward
    (moving the taller one can never help). If both are equal, I move both.

Complexity:
    Time:  O(n)  - one loop of n steps
    Space: O(1)  - a few variables
"""


class Solution:
    def maxArea(self, height: list[int]) -> int:
        max_water = 0
        left = 0
        right = len(height) - 1

        for i in range(len(height)):
            water = min(height[left], height[right]) * (right - left)
            max_water = max(water, max_water)

            if height[left] < height[right]:
                left += 1
            elif height[left] > height[right]:
                right -= 1
            else:
                left += 1
                right -= 1
        return max_water


if __name__ == "__main__":
    sol = Solution()
    assert sol.maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    assert sol.maxArea([1, 1]) == 1
    assert sol.maxArea([4, 3, 2, 1, 4]) == 16
    assert sol.maxArea([1, 2, 1]) == 2
    assert sol.maxArea([2, 2, 2, 2]) == 6
    print("All tests passed.")
