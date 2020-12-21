from typing import Union


def tokenize(expr: str) -> list[Union[int, str]]:
    i = 0
    tokens = []
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

def calc(expr: str) -> int:
    stack = []

    for token in tokenize(expr):
        stack.append(token)

        if stack[-1] == ")":
            assert type(stack[-2]) == int
            assert stack[-3] == "("
            _, num, _ = stack.pop(), stack.pop(), stack.pop()
            stack.append(num)
        if type(stack[-1]) == int and len(stack) > 1:
            if stack[-2] == "+":
                num1, _, num2 = stack.pop(), stack.pop(), stack.pop()
                stack.append(num1 + num2)
            elif stack[-2] == "*":
                num1, _, num2 = stack.pop(), stack.pop(), stack.pop()
                stack.append(num1 * num2)
    return stack.pop()


def solve_part_1(exprs: list[str]) -> int:
    return sum(calc(expr) for expr in exprs)

if __name__ == "__main__":
    with open("day18_input.txt") as f:
        exprs = [line.strip() for line in f.readlines()]
        print(solve_part_1(exprs))
    