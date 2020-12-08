class Console:
    def _op_acc(self, arg):
        self.pc += 1
        self.acc += arg

    def _op_jmp(self, arg):
        self.pc += arg

    def _op_nop(self, arg):
        self.pc += 1

    _operation = {
        "acc": _op_acc,
        "jmp": _op_jmp,
        "nop": _op_nop
    }

    def __init__(self, program):
        self.acc = 0
        self.pc = 0
        self.program = program
        self.terminated = False

    def step(self):
        op, arg = self.program[self.pc]
        self._operation[op](self, arg)
        if self.pc >= len(self.program):
            self.terminated = True

def parse_instruction(line):
    [arg, op] = line.strip().split(" ")
    return arg, int(op)

def run(program):
    console = Console(program)
    pc_set = set()
    while not console.terminated and console.pc not in pc_set:
        pc_set.add(console.pc)
        console.step()
    return console

def solve_part_1(program):
    console = run(program)
    return console.acc

def solve_part_2(program):
    index = 0
    while index < len(program):
        op, arg = program[index]
        try_op = "acc"
        if op == "nop":
            try_op = "jmp"
        if op == "jmp":
            try_op = "nop"
        program[index] = try_op, arg
        console = run(program)
        if console.terminated:
            return console.acc
        program[index] = op, arg
        index += 1

if __name__ == "__main__":
    with open("day08_input.txt") as f:
        program = [parse_instruction(line) for line in f.readlines()]
        print(solve_part_1(program))
        print(solve_part_2(program))