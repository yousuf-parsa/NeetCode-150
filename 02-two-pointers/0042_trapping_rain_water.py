"""
LeetCode 42. Trapping Rain Water
https://leetcode.com/problems/trapping-rain-water/
Difficulty: Hard

Intuition:
    Water above a bar = min(tallest bar on its left, tallest on its right) - its height.
    Finding those two maxes again for every bar is slow.
    So I precompute them once: max_left from the left, max_right from the right.
    Then one more pass adds up the water at each bar.

Complexity:
    Time:  O(n)  - three passes
    Space: O(n)  - the two max arrays
"""


class Solution:
    def trap(self, height: list[int]) -> int:
        n = len(height)

        if n == 0:
            return 0

        max_left = [0] * n
        max_right = [0] * n

        max_left[0] = height[0]
        for i in range(1, n):
            max_left[i] = max(max_left[i - 1], height[i])

        max_right[n - 1] = height[n - 1]

        for i in range(n - 2, -1, -1):
            max_right[i] = max(max_right[i + 1], height[i])

        total = 0

        for i in range(n):

            water_level = min(max_left[i], max_right[i])
            water = water_level - height[i]
            total += water

        return total


if __name__ == "__main__":
    sol = Solution()
    assert sol.trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    assert sol.trap([4, 2, 0, 3, 2, 5]) == 9
    assert sol.trap([]) == 0
    assert sol.trap([5]) == 0
    assert sol.trap([1, 2, 3]) == 0
    print("All tests passed.")
