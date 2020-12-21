from typing import Optional, Tuple, Union, cast


Token = Union[int, str]


class Node:
    def __init__(self, value: Token):
        self.value = value
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.sealed = False


def tokenize(expr: str) -> list[Token]:
    i = 0
    tokens: list[Token] = []
    while i < len(expr):
        j = i
        if expr[j].isnumeric():
            while j < len(expr) and expr[j].isnumeric():
                j += 1
            tokens.append(int(expr[i:j]))
        else:
            tokens.append(expr[j])
            j += 1
        i = j
        while i < len(expr) and expr[i] == " ":
            i += 1
    return tokens


def normalize(tokens: list[Token]) -> list[Token]:
    return ["(", *tokens, ")"]


def parse(tokens: list[Token], index: int, precedence: bool) -> Tuple[Node, int]:
    assert tokens[index] == "("
    nodes: list[Node] = []
    index += 1
    while tokens[index] != ")":
        if tokens[index] == "(":
            node, adj = parse(tokens, index, precedence)
            nodes.append(node)
            index = adj
        else:
            nodes.append(Node(tokens[index]))
            index += 1
        if len(nodes) == 3:
            operand2, operator, operand1 = nodes.pop(), nodes.pop(), nodes.pop()
            if (
                precedence
                and operand1.value == "*"
                and operator.value == "+"
                and not operand1.sealed
            ):
                operator.left = operand1.right
                operator.right = operand2
                operand1.right = operator
                operator = operand1
            else:
                operator.left = operand1
                operator.right = operand2
            nodes.append(operator)
    assert len(nodes) == 1
    node = nodes.pop()
    node.sealed = True
    return node, index + 1


def calc(expr: str, precedence: bool = False) -> int:
    def calcrec(node: Node) -> int:
        if type(node.value) == int:
            return cast(int, node.value)
        else:
            assert node.left != None
            assert node.right != None
            if node.value == "+":
                return calcrec(node.left) + calcrec(node.right)
            else:
                return calcrec(node.left) * calcrec(node.right)

    node, _ = parse(normalize(tokenize(expr)), 0, precedence)
    return calcrec(node)


def solve_part_1(exprs: list[str]) -> int:
    return sum(calc(expr) for expr in exprs)


def solve_part_2(exprs: list[str]) -> int:
    return sum(calc(expr, True) for expr in exprs)


if __name__ == "__main__":
    with open("day18_input.txt") as f:
        exprs = [line.strip() for line in f.readlines()]
        print(solve_part_1(exprs))
        print(solve_part_2(exprs))
