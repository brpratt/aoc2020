from typing import Union


SubRule = list[int]
Rule = Union[str, list[SubRule]]
Rules = dict[int, Rule]


def separate(lines: list[str]) -> tuple[list[str], list[str]]:
    i = 0
    while i < len(lines) and lines[i] != "":
        i += 1
    return lines[0:i], lines[i:]


def parse_rules(lines: list[str]) -> Rules:
    rules: Rules = {}
    for line in lines:
        number, raw_pattern = line.split(": ")
        if raw_pattern.startswith('"'):
            rules[int(number)] = raw_pattern[1]
        else:
            rules[int(number)] = [
                [int(num) for num in nums.split()] for nums in raw_pattern.split(" | ")
            ]
    return rules


def assemble(rules: Rules, number: int) -> set[str]:
    patterns = set()
    rule = rules[number]
    if isinstance(rule, str):
        patterns.add(rule)
        return patterns
    for subrule in rule:
        subpatterns = assemble(rules, subrule[0])
        for i in range(1, len(subrule)):
            tails = assemble(rules, subrule[i])
            heads = subpatterns.copy()
            subpatterns.clear()
            for head in heads:
                for tail in tails:
                    subpatterns.add(head+tail)
        patterns.update(subpatterns)
    return patterns

def solve_part_1(lines: list[str]) -> int:
    rule_lines, messages = separate(lines)
    rules = parse_rules(rule_lines)
    patterns = assemble(rules, 0)
    return sum(1 for message in messages if message in patterns)

if __name__ == "__main__":
    with open("day19_input.txt") as f:
        lines = [line.strip() for line in f.readlines()]
        print(solve_part_1(lines))
