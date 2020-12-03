from itertools import count
from math import prod

def count_trees(map, slope):
    ys = range(0, len(map), slope[1])
    xs = count(0, slope[0])
    positions = [(next(xs) % len(map[0]), y) for y in ys]
    return len([pos for pos in positions if map[pos[1]][pos[0]] == '#'])

def solve_part_1(map):
    return count_trees(map, (3, 1))

def solve_part_2(map):
    return prod([count_trees(map, slope) for slope in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]])

if __name__ == "__main__":
    with open("day03_input.txt") as f:
        map = [line.strip() for line in f.readlines()]
        print(solve_part_1(map))
        print(solve_part_2(map))