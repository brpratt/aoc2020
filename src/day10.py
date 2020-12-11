def pairs(iter):
    for i in range(len(iter)-1):
        yield iter[i], iter[i+1]

def solve_part_1(nums):
    hist = dict([(1, 0), (2, 0), (3, 0)])
    for j0, j1 in pairs(nums):
        hist[j1-j0] += 1
    return hist[1] * hist[3]

def solve_part_2(nums):
    _count = dict()

    def count_options(i, nums):
        if i in _count:
            return _count[i]
        if i == len(nums)-1:
            return 1
        j = i + 1
        count = 0
        while j < len(nums) and nums[j] - nums[i] <= 3:
            count += count_options(j, nums)
            j += 1
        _count[i] = count
        return count

    return count_options(0, nums)

if __name__ == "__main__":
    with open("day10_input.txt") as f:
        nums = sorted(int(line) for line in f.readlines())
        nums = [0] + nums + [max(nums) + 3]
        print(solve_part_1(nums))
        print(solve_part_2(nums))