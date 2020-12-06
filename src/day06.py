def read_groups(lines):
    group = []
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            yield group
            group = []
        else:
            group.append(set(line))
    yield group

def solve_part_1(groups):
    return sum(len(set().union(*group)) for group in groups)

def solve_part_2(groups):
    return sum(len(group[0].intersection(*group[1:])) for group in groups)

if __name__ == "__main__":
    with open("day06_input.txt") as f:
        groups = list(read_groups(f.readlines()))
        print(solve_part_1(groups))
        print(solve_part_2(groups))