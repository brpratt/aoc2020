from collections import namedtuple
import re

Mask = namedtuple("Mask", "mask")
Store = namedtuple("Store", ["address", "value"])

def parse_instruction(s: str):
    if match := re.match(r"mask = (\w+)", s):
        return Mask(match.groups()[0])
    match = re.match(r"mem\[(\d+)\] = (\d+)", s)
    return Store(int(match.groups()[0]), int(match.groups()[1]))

def apply_mask(num, mask):
    num = num | int(mask.replace("X", "0"), base=2)
    num = num & int(mask.replace("X", "1"), base=2)
    return num

def apply_floating(template):
    results = []

    def iter(i, digits):
        if i == len(template):
            results.append(int(''.join(digits), base=2))
        elif template[i] == '1' or template[i] == '0':
            iter(i+1, digits + [template[i]])
        else:
            iter(i+1, digits + ['0'])
            iter(i+1, digits + ['1'])
    
    iter(0, [])
    return results

def apply_mask_v2(num, mask):
    binary = bin(num)[2:]
    binary = ("0" * (36 - len(binary))) + binary
    bits = list(binary)
    for n in range(len(bits)):
        if mask[n] == "1" or mask[n] == "X":
            bits[n] = mask[n]
    return apply_floating(''.join(bits))

def solve_part_1(program):
    mask = ""
    mem = {}
    for instr in program:
        if isinstance(instr, Mask):
            mask = instr[0]
        else:
            mem[instr[0]] = apply_mask(instr[1], mask)
    return sum(mem.values())

def solve_part_2(program):
    mask = []
    mem = {}
    for instr in program:
        if isinstance(instr, Mask):
            mask = instr[0]
        else:
            addr, value = instr
            for masked in apply_mask_v2(addr, mask):
                mem[masked] = value
    return sum(mem.values())

if __name__ == "__main__":
    with open("day14_input.txt") as f:
        program = [parse_instruction(line) for line in f.readlines()]
        print(solve_part_1(program))
        print(solve_part_2(program))