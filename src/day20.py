import functools


class Tile:
    def __init__(self, num: int, data: list[str]):
        self.num = num
        self.data = data
        self.borders: list[str] = [
            data[0],
            functools.reduce(lambda a, b: a + b[-1], data, ""),
            data[-1],
            functools.reduce(lambda a, b: a + b[0], data, ""),
        ]


def load_tiles(lines: list[str]) -> list[Tile]:
    tiles: list[Tile] = []
    i = 0
    while i < len(lines):
        id = int(lines[i].rstrip(":").split()[1])
        data = lines[i + 1 : i + 11]
        tiles.append(Tile(id, data))
        i += 12
    return tiles


def update(
    borders: dict[str, list[int]], shared_borders: dict[int, int], border: str, num: int
):
    def inc_shared_borders(num: int):
        if num in shared_borders:
            shared_borders[num] += 1
        else:
            shared_borders[num] = 1

    rborder = border[::-1]
    if border in borders:
        borders[border].append(num)
        for num in borders[border]:
            inc_shared_borders(num)
    elif rborder in borders:
        borders[rborder].append(num)
        for num in borders[rborder]:
            inc_shared_borders(num)
    else:
        borders[border] = [num]


def solve_part_1(tiles: list[Tile]) -> int:
    borders: dict[str, list[int]] = {}
    shared_borders: dict[int, int] = {}
    for tile in tiles:
        update(borders, shared_borders, tile.borders[0], tile.num)
        update(borders, shared_borders, tile.borders[1], tile.num)
        update(borders, shared_borders, tile.borders[2], tile.num)
        update(borders, shared_borders, tile.borders[3], tile.num)
    corner_nums = [num for num, count in shared_borders.items() if count == 2]
    return corner_nums[0] * corner_nums[1] * corner_nums[2] * corner_nums[3]


if __name__ == "__main__":
    with open("day20_input.txt") as f:
        lines = [line.strip() for line in f]
        tiles = load_tiles(lines)
        print(solve_part_1(tiles))
