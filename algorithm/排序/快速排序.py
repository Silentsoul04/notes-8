
class Solution(object):
    def sort(self, arrays):
        for i in range(len(arrays)):
            print(i)
            current = arrays[i]
            while i > 0 and arrays[i-1] > current:
                arrays[i-1], arrays[i] = arrays[i], arrays[i - 1]
                i -= 1

        return sorted(arrays)


print(Solution().sort([2, 3, 1, 4]))
print(Solution().sort([4, 2, 3, 1]))