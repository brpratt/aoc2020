from collections import namedtuple
import re

_record_re = re.compile("(\d+)-(\d+) (\w): (\w+)")

OldPolicy = namedtuple("OldPolicy", ["min", "max", "letter"])
NewPolicy = namedtuple("NewPolicy", ["pos1", "pos2", "letter"])

def parse_old_record(record):
    match = re.match(_record_re, record)
    (raw_min, raw_max, letter, password) = match.groups()
    return OldPolicy(int(raw_min), int(raw_max), letter), password

def parse_new_record(record):
    match = re.match(_record_re, record)
    (raw_pos1, raw_pos2, letter, password) = match.groups()
    return NewPolicy(int(raw_pos1), int(raw_pos2), letter), password

def passes_old_policy(policy, password):
    count = 0
    for letter in password:
        if letter == policy.letter:
            count += 1
    return count >= policy.min and count <= policy.max

def passes_new_policy(policy, password):
    pos1_matches, pos2_matches = False, False
    if len(password) >= policy.pos1 and password[policy.pos1-1] == policy.letter:
        pos1_matches = True
    if len(password) >= policy.pos2 and password[policy.pos2-1] == policy.letter:
        pos2_matches = True
    if pos1_matches and pos2_matches:
        return False
    return pos1_matches or pos2_matches

def solve_part_1(records):
    valid_count = 0
    for record in records:
        (policy, password) = parse_old_record(record)
        if passes_old_policy(policy, password):
            valid_count += 1
    return valid_count

def solve_part_2(records):
    valid_count = 0
    for record in records:
        (policy, password) = parse_new_record(record)
        if passes_new_policy(policy, password):
            valid_count += 1
    return valid_count

if __name__ == "__main__":
    with open("day02_input.txt") as f:
        lines = f.readlines()
        print(solve_part_1(lines))
        print(solve_part_2(lines))