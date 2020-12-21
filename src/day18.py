from enum import Enum
from typing import Iterator

class Token:
    pass

class Number(Token):
    def __init__(self, value: int):
        self.value = value

class Operator(Token):
    def __init__(self, value: str):
        self.value = value

class OpenParen(Token):
    pass

class CloseParen(Token):
    pass

def tokenize(expr: str) -> Iterator[Token]:
    i = 0
    while i < len(expr):
        j = i
        if expr[j].isnumeric():
            while j < len(expr) and expr[j].isnumeric():
                j += 1
            yield Number(int(expr[i:j]))
        elif expr[j] == "+" or expr[j] == "*":
            yield Operator(expr[j])
            j += 1
        elif expr[j] == "(":
            yield OpenParen()
            j += 1
        elif expr[j] == ")":
            yield CloseParen()
            j += 1
        i = j
        while i < len(expr) and expr[i] == " ":
            i += 1


class Operation(Enum):
    OPERAND1 = 1,
    OPERATOR = 2,
    OPERAND2 = 3

def calc(expr: str) -> int:
    stack = []
    
    def compute():
        if len(stack) > 2 and isinstance(stack[-2], Operator):
            num1, op, num2 = stack.pop(), stack.pop(), stack.pop()
            if op.value == "+":
                stack.append(Number(num1.value + num2.value))
            else:
                stack.append(Number(num1.value * num2.value))

    for token in tokenize(expr):
        if isinstance(token, Number):
            stack.append(token)
            compute()        
        elif isinstance(token, CloseParen):
            num, _ = stack.pop(), stack.pop()
            stack.append(num)
            compute()
        else:
            stack.append(token)
    return stack.pop().value

def solve_part_1(exprs: list[str]) -> int:
    return sum(calc(expr) for expr in exprs)

if __name__ == "__main__":
    with open("day18_input.txt") as f:
        exprs = [line.strip() for line in f.readlines()]
        print(solve_part_1(exprs))
    