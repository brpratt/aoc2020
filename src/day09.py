_window = 25

def is_valid(nums, num):
    for i in range(len(nums)):
        check = num - nums[i]
        if check in nums[i+1:]:
            return True
    return False

def solve_part_1(nums):
    for i in range(len(nums)):
        window = nums[i:_window+i]
        target = nums[_window+i]
        if not is_valid(window, target):
            return target

def solve_part_2(nums, target):
    for i in range(len(nums)):
        j = 1
        check_nums = nums[i:i+j]
        while sum(check_nums) < target:
            j += 1
            check_nums = nums[i:i+j]
        if sum(check_nums) == target:
            return min(check_nums) + max(check_nums)

if __name__ == "__main__":
    with open("day09_input.txt") as f:
        nums = [int(line) for line in f.readlines()]
        target = solve_part_1(nums)
        print(target)
        print(solve_part_2(nums, target))