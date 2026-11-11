"""
LeetCode 49. Group Anagrams
https://leetcode.com/problems/group-anagrams/
Difficulty: Medium

Intuition:
    Anagrams have the same letters, so sorting them gives the same string.
    I use that sorted string as a key in a dict.
    Every word goes into the list for its key; each list is one group.

Complexity:
    Time:  O(n * m log m)  - sort each of n words (m = max word length)
    Space: O(n * m)        - the dict stores all words
"""

import collections


class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        groups = collections.defaultdict(list)

        for s in strs:
            key = ''.join(sorted(s))
            groups[key].append(s)

        return list(groups.values())


if __name__ == "__main__":
    sol = Solution()

    def norm(groups):
        return sorted(sorted(g) for g in groups)

    assert norm(sol.groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"])) == [
        ["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]
    assert norm(sol.groupAnagrams([""])) == [[""]]
    assert norm(sol.groupAnagrams(["a"])) == [["a"]]
    assert norm(sol.groupAnagrams(["ab", "ba", "abc"])) == [["ab", "ba"], ["abc"]]
    print("All tests passed.")
