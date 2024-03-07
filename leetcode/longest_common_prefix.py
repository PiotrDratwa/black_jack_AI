
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
