def find_sum_pair(nums, sum):
    for x in range(len(nums)-1):
        for y in range(x+1, len(nums)):
            if nums[x] + nums[y] == sum:
                return (nums[x], nums[y])

def find_sum_thrice(nums, sum):
    for x in range(len(nums)-2):
        for y in range(x+1, len(nums)-1):
            for z in range(y+1, len(nums)):
                if nums[x] + nums[y] + nums[z] == sum:
                    return (nums[x], nums[y], nums[z])

def solve_part_1(nums):
    (x, y) = find_sum_pair(nums, 2020)
    return x * y

def solve_part_2(nums):
    (x, y, z) = find_sum_thrice(nums, 2020)
    return x * y * z

if __name__ == "__main__":
    with open("day01_input.txt") as f:
        nums = [int(x) for x in f.readlines()]
        print(solve_part_1(nums))
        print(solve_part_2(nums))