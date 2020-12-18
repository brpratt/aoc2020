import re

def parse_notes(lines):
    i = 0
    rules = {}
    while lines[i] != "":
        match = re.match(r"(.+): (\d+)-(\d+) or (\d+)-(\d+)", lines[i])
        groups = match.groups()
        name = groups[0]
        ranges = [(int(groups[1]), int(groups[2])), (int(groups[3]), int(groups[4]))]
        rules[name] = ranges
        i += 1
    yours = [int(x) for x in lines[i+2].split(",")]
    others = [[int(x) for x in line.split(",")] for line in lines[i+5:]]
    return rules, yours, others

def within_ranges(num, ranges):
    return any(lower <= num <= upper for lower, upper in ranges)

def within_rules(num, rules):
    return any(within_ranges(num, ranges) for ranges in rules.values())

def invalid_fields(ticket, rules):
    return [field for field in ticket if not within_rules(field, rules)]

def solve_part_1(notes):
    rules, _, others = notes
    acc = 0
    for ticket in others:
        acc += sum(invalid_fields(ticket, rules))
    return acc

def identify_positions(rules, others):
    possible_positions = [set() for _ in range(len(others[0]))]
    for s in possible_positions:
        for name in rules:
            s.add(name)
    for ticket in others:
        for i, num in enumerate(ticket):
            for name, ranges in rules.items():
                if not within_ranges(num, ranges):
                    possible_positions[i].remove(name)
    positions = {}
    while len(positions) != len(rules):
        for name, i in positions.items():
            for s in possible_positions:
                s.discard(name)
        for i, s in enumerate(possible_positions):
            if len(s) == 1:
                name = s.pop()
                positions[name] = i
    return positions

def solve_part_2(notes):
    rules, yours, others = notes
    others = [other for other in others if len(invalid_fields(other, rules)) == 0]
    positions = identify_positions(rules, others)
    acc = 1
    for position, index in positions.items():
        if position.startswith("departure"):
            acc *= yours[index]
    return acc

if __name__ == "__main__":
    with open("day16_input.txt") as f:
        notes = parse_notes([line.strip() for line in f.readlines()])
        print(solve_part_1(notes))
        print(solve_part_2(notes))