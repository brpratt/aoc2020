
from itertools import islice

def nth(iterable, n):
    return next(islice(iterable, n - 1, None))

def gameseq(nums):
    i = 0
    spoken = {}
    while i < len(nums) - 1:
        yield nums[i]
        spoken[nums[i]] = i
        i += 1
    curr = nums[-1]
    while True:
        yield curr
        n = 0
        if curr in spoken:
            n = i - spoken[curr]
        spoken[curr] = i
        curr = n
        i += 1

def solve_part_1(nums):
    return nth(gameseq(nums), 2020)

def solve_part_2(nums):
    return nth(gameseq(nums), 30000000)

if __name__ == "__main__":
    with open("day15_input.txt") as f:
        nums = [int(x) for x in f.readline().split(',')]
        print(solve_part_1(nums))
        print(solve_part_2(nums))