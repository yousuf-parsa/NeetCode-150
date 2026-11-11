"""
LeetCode 121. Best Time to Buy and Sell Stock
https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
Difficulty: Easy

Intuition:
    Trying every buy/sell pair is too slow.
    left is my buy day, right is my sell day.
    If today's price is lower than my buy price, I just buy today instead.
    Otherwise I try selling today and keep the best profit.

Complexity:
    Time:  O(n)  - one pass
    Space: O(1)  - two variables
"""


class Solution:
    def maxProfit(self, prices: list[int]) -> int:

        left, profit = 0, 0

        for right in range(len(prices)):
            if prices[left] > prices[right]:
                left = right
            else:
                profit = max(profit, prices[right] - prices[left])

        return profit


if __name__ == "__main__":
    sol = Solution()
    assert sol.maxProfit([7, 1, 5, 3, 6, 4]) == 5
    assert sol.maxProfit([7, 6, 4, 3, 1]) == 0
    assert sol.maxProfit([1]) == 0
    assert sol.maxProfit([2, 4, 1]) == 2
    assert sol.maxProfit([3, 2, 6, 1, 4]) == 4
    print("All tests passed.")
