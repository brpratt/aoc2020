def step(layout):
    max_row = len(layout)
    max_col = len(layout[0])

    def neighbors(row, col):
        count = 0
        has_top = row - 1 >= 0
        has_bot = row + 1 < max_row
        has_lft = col - 1 >= 0
        has_rgt = col + 1 < max_col

        if has_top and has_lft and layout[row-1][col-1] == "#":
            count += 1
        if has_top and layout[row-1][col] == "#":
            count += 1
        if has_top and has_rgt and layout[row-1][col+1] == "#":
            count += 1
        if has_lft and layout[row][col-1] == "#":
            count += 1
        if has_rgt and layout[row][col+1] == "#":
            count += 1
        if has_bot and has_lft and layout[row+1][col-1] == "#":
            count += 1
        if has_bot and layout[row+1][col] == "#":
            count += 1
        if has_bot and has_rgt and layout[row+1][col+1] == "#":
            count += 1
        return count

    new = [[' ' for col in range(max_col)] for row in range(max_row)]
    changed = False
    for row in range(len(layout)):
        for col in range(len(layout[row])):
            n = neighbors(row, col)
            tile = layout[row][col]
            if tile == "L" and n == 0:
                new[row][col] = "#"
                changed = True
            elif tile == "#" and n >= 4:
                new[row][col] = "L"
                changed = True
            else:
                new[row][col] = tile
    return (new, changed)

def step2(layout):
    max_row = len(layout)
    max_col = len(layout[0])

    def hit_occupied(row, col, row_off, col_off):
        row += row_off
        col += col_off
        if row < 0 or row >= max_row:
            return False
        if col < 0 or col >= max_col:
            return False
        if layout[row][col] == "L":
            return False
        if layout[row][col] == "#":
            return True
        return hit_occupied(row, col, row_off, col_off)


    def neighbors(row, col):
        return (int(hit_occupied(row, col, -1, -1)) +
            int(hit_occupied(row, col, -1, 0)) +
            int(hit_occupied(row, col, -1, 1)) +
            int(hit_occupied(row, col, 0, -1)) +
            int(hit_occupied(row, col, 0, 1)) +
            int(hit_occupied(row, col, 1, -1)) +
            int(hit_occupied(row, col, 1, 0)) +
            int(hit_occupied(row, col, 1, 1)))

    new = [[' ' for col in range(max_col)] for row in range(max_row)]
    changed = False
    for row in range(len(layout)):
        for col in range(len(layout[row])):
            n = neighbors(row, col)
            tile = layout[row][col]
            if tile == "L" and n == 0:
                new[row][col] = "#"
                changed = True
            elif tile == "#" and n >= 5:
                new[row][col] = "L"
                changed = True
            else:
                new[row][col] = tile
    return (new, changed)

def count_occupied(layout):
    count = 0
    for row in layout:
        for seat in row:
            if seat == "#":
                count += 1
    return count

def solve_part_1(layout):
    changed = True
    while changed:
        layout, changed = step(layout)
    return count_occupied(layout)

def solve_part_2(layout):
    changed = True
    while changed:
        layout, changed = step2(layout)
    return count_occupied(layout)

if __name__ == "__main__":
    with open("day11_input.txt") as f:
        layout = [list(line.strip()) for line in f.readlines()]
        print(solve_part_1(layout))
        print(solve_part_2(layout))