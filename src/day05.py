def seat_id(part):
    binary = (
        part.replace('F', '0')
            .replace('B', '1')
            .replace('L', '0')
            .replace('R', '1')
    )
    row = int(binary[:-3], 2)
    col = int(binary[-3:], 2)
    return (row * 8) + col

def solve_part_1(parts):
    return max(seat_id(part) for part in parts)

def sum_1_to_n(n):
    return n * (n + 1) // 2

def solve_part_2(parts):
    ids = [seat_id(part) for part in parts]
    expected_sum = sum_1_to_n(max(ids)) - sum_1_to_n(min(ids) - 1)
    return expected_sum - sum(ids)

if __name__ == "__main__":
    with open("day05_input.txt") as f:
        lines = [line.strip() for line in f.readlines()]
        print(solve_part_1(lines))
        print(solve_part_2(lines))