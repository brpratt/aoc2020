from enum import Enum
import functools
import itertools
import math
from typing import Optional, Tuple


class Orientation(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4


class Tile:
    def __init__(self, num: int, data: list[list[str]]):
        self.num = num
        self.data = data

    def border(self, o: Orientation) -> str:
        if o == Orientation.NORTH:
            return "".join(self.data[0])
        elif o == Orientation.EAST:
            return functools.reduce(lambda a, b: a + b[-1], self.data, "")
        elif o == Orientation.SOUTH:
            return "".join(self.data[-1])
        else:
            return functools.reduce(lambda a, b: a + b[0], self.data, "")

    def borders(self) -> Tuple[str, str, str, str]:
        return (
            self.border(Orientation.NORTH),
            self.border(Orientation.EAST),
            self.border(Orientation.SOUTH),
            self.border(Orientation.WEST),
        )

    # 90 degrees clockwise
    def rotate(self):
        length = len(self.data)
        data = [["x" for _ in row] for row in self.data]
        for i, row in enumerate(self.data):
            for j, ch in enumerate(row):
                data[j][length - (i + 1)] = ch
        self.data = data

    def flipx(self):
        length = len(self.data)
        data = [["x" for _ in row] for row in self.data]
        for i, row in enumerate(self.data):
            for j, ch in enumerate(row):
                data[length - (i + 1)][j] = ch
        self.data = data

    def flipy(self):
        length = len(self.data)
        data = [["x" for _ in row] for row in self.data]
        for i, row in enumerate(self.data):
            for j, ch in enumerate(row):
                data[i][length - (j + 1)] = ch
        self.data = data


def load_tiles(lines: list[str]) -> list[Tile]:
    tiles: list[Tile] = []
    i = 0
    while i < len(lines):
        num = int(lines[i].rstrip(":").split()[1])
        data = lines[i + 1 : i + 11]
        tiles.append(Tile(num, [[ch for ch in row] for row in data]))
        i += 12
    return tiles


def find_adjacent(tiles: list[Tile]) -> dict[int, list[int]]:
    borders: dict[str, list[int]] = {}
    for tile in tiles:
        for border in tile.borders():
            rborder = border[::-1]
            if border in borders:
                borders[border].append(tile.num)
            elif rborder in borders:
                borders[rborder].append(tile.num)
            else:
                borders[border] = [tile.num]
    adjacent: dict[int, list[int]] = dict((tile.num, []) for tile in tiles)
    for nums in borders.values():
        assert len(nums) == 1 or len(nums) == 2
        if len(nums) == 2:
            adjacent[nums[0]].append(nums[1])
            adjacent[nums[1]].append(nums[0])
    return adjacent


def find_alignment(t1: Tile, t2: Tile) -> Optional[Tuple[Orientation, Orientation]]:
    orientations = list(Orientation)
    for o1 in orientations:
        b1 = t1.border(o1)
        for o2 in orientations:
            b2 = t2.border(o2)
            if b1 == b2 or b1 == b2[::-1]:
                return o1, o2
    return None


def align(t1: Tile, t2: Tile):
    alignment = find_alignment(t1, t2)
    assert alignment is not None
    o1, o2 = alignment
    while abs(o1.value - o2.value) != 2:
        t2.rotate()
        alignment = find_alignment(t1, t2)
        assert alignment is not None
        o1, o2 = alignment
    b1, b2 = t1.border(o1), t2.border(o2)
    if b1 != b2:
        if o1 == Orientation.NORTH or o1 == Orientation.SOUTH:
            t2.flipy()
        else:
            t2.flipx()


def solve_part_1(adjacent: dict[int, list[int]]) -> int:
    corners = [num for num, others in adjacent.items() if len(others) == 2]
    return corners[0] * corners[1] * corners[2] * corners[3]


def draw(tiles: list[Tile], adjacent: dict[int, list[int]]) -> Tile:
    tiles_by_num = dict((tile.num, tile) for tile in tiles)
    tile_length = len(tiles[0].data) - 2
    tiles_per_side = int(math.sqrt(len(tiles)))
    image_length = tiles_per_side * tile_length
    image = [["x" for _ in range(image_length)] for _ in range(image_length)]

    def fill(tile: Tile, x: int, y: int):
        for i, row in enumerate(tile.data):
            for j, ch in enumerate(row):
                if i == 0 or i == len(tile.data) - 1:
                    continue
                if j == 0 or j == len(tile.data) - 1:
                    continue
                image[(y * tile_length) + (i - 1)][(x * tile_length) + (j - 1)] = ch

    def seed_aligned(seed: Tile) -> bool:
        neighbor1 = tiles_by_num[adjacent[seed.num][0]]
        neighbor2 = tiles_by_num[adjacent[seed.num][1]]
        alignment1 = find_alignment(seed, neighbor1)
        alignment2 = find_alignment(seed, neighbor2)
        assert alignment1 is not None and alignment2 is not None
        if alignment1[0] == Orientation.EAST and alignment2[0] == Orientation.SOUTH:
            return True
        if alignment1[0] == Orientation.SOUTH and alignment2[0] == Orientation.EAST:
            return True
        return False

    def find_seed() -> Tile:
        seed = None
        for num, others in adjacent.items():
            if len(others) == 2:
                seed = tiles_by_num[num]
                break
        assert seed is not None
        while not seed_aligned(seed):
            seed.rotate()
        return seed

    def find_tile_right(tile: Tile) -> Optional[Tile]:
        tile_right = None
        for adj in adjacent[tile.num]:
            alignment = find_alignment(tile, tiles_by_num[adj])
            assert alignment is not None
            if alignment[0] == Orientation.EAST:
                tile_right = tiles_by_num[adj]
                align(tile, tile_right)
                return tile_right

    def find_tile_down(tile: Tile) -> Optional[Tile]:
        tile_down = None
        for adj in adjacent[tile.num]:
            alignment = find_alignment(tile, tiles_by_num[adj])
            assert alignment is not None
            if alignment[0] == Orientation.SOUTH:
                tile_down = tiles_by_num[adj]
                align(tile, tile_down)
                return tile_down

    seed = find_seed()
    for y in range(tiles_per_side):
        assert seed is not None
        fill(seed, 0, y)
        tile = seed
        for x in range(1, tiles_per_side):
            tile = find_tile_right(tile)
            assert tile is not None
            fill(tile, x, y)
        seed = find_tile_down(seed)

    return Tile(0, image)


# fmt: off
_monster = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   "
]
# fmt: on
_monster_pieces = [
    (x, y) for y, row in enumerate(_monster) for x, ch in enumerate(row) if ch == "#"
]


def count_monsters(tile: Tile) -> int:
    def has_monster(x: int, y: int):
        for piecex, piecey in _monster_pieces:
            if tile.data[y + piecey][x + piecex] != "#":
                return False
        return True

    offsetymax = len(tile.data) - len(_monster) + 1
    offsetxmax = len(tile.data[0]) - len(_monster[0]) + 1
    offsets = itertools.product(range(offsetymax), range(offsetxmax))
    count = 0
    for offy, offx in offsets:
        if has_monster(offx, offy):
            count += 1
    return count


def solve_part_2(tiles: list[Tile], adjacent: dict[int, list[int]]) -> int:
    image = draw(tiles, adjacent)
    counts = []
    for _ in range(4):
        counts.append(count_monsters(image))
        image.rotate()
    image.flipx()
    for _ in range(4):
        counts.append(count_monsters(image))
        image.rotate()
    num_monsters = max(counts)
    num_targets = sum(1 for row in image.data for ch in row if ch == "#")
    return num_targets - (num_monsters * len(_monster_pieces))


if __name__ == "__main__":
    with open("day20_input.txt") as f:
        lines = [line.strip() for line in f]
        tiles = load_tiles(lines)
        adjacent = find_adjacent(tiles)
        print(solve_part_1(adjacent))
        print(solve_part_2(tiles, adjacent))
