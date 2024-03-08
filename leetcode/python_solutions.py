#problem 14. Longest common prefix
#runtime 11 ms (better than 92% of Python users) memory 12 mb (better than 26% of Python users)
#https://leetcode.com/problems/longest-common-prefix/submissions/1180285966/?envType=featured-list&envId=top-interview-questions?envType=featured-list&envId=top-interview-questions
class Solution(object):
    def longestCommonPrefix(self, strs):
        if "" in strs:
            return ""

        I = 0
        prefix = ""
        for I in range(0, len(max(strs))):
            i = 0
            for i in range(0, len(strs)):
                if strs[0][:I+1] != strs[i][:I+1]:
                    return prefix
                i+=1

            prefix = strs[0][:I+1]
            I+=1
        return prefix

solution = Solution()
print(solution.longestCommonPrefix(["a"]))
