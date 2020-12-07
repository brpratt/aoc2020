def parse_child(s):
    splits = s.split(' ')
    return int(splits[0]), f"{splits[1]} {splits[2]}"

def parse_rule(line):
    [parent, children] = line.strip().split(" contain ")
    parent = parent[:-5]
    if "no other bags" in children:
        return parent, []
    return parent, [parse_child(child) for child in children.split(", ")]

def parent_graph(rules):
    graph = dict()
    for (parent, children) in rules:
        if parent not in graph:
            graph[parent] = []
        for (_, color) in children:
            if color in graph:
                graph[color].append(parent)
            else:
                graph[color] = [parent]
    return graph

def parent_colors(graph, color):
    colors = set(graph[color])
    for parent in graph[color]:
        colors |= parent_colors(graph, parent)
    return colors

def child_count(graph, color):
    count = 0
    for child in graph[color]:
        count += child[0]
        count += child[0] * child_count(graph, child[1])
    return count

def solve_part_1(rules):
    graph = parent_graph(rules)
    return len(parent_colors(graph, "shiny gold"))

def solve_part_2(rules):
    graph = dict(rules)
    return child_count(graph, "shiny gold")

if __name__ == "__main__":
    with open("day07_input.txt") as f:
        rules = [parse_rule(line) for line in f.readlines()]
        print(solve_part_1(rules))
        print(solve_part_2(rules))
