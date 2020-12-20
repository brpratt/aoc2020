from typing import NamedTuple
import itertools


class Point3(NamedTuple):
    x: int
    y: int
    z: int


class Point4(NamedTuple):
    x: int
    y: int
    z: int
    w: int


class Grid3:
    def __init__(self):
        self.active_points: set[Point3] = set()

    def __setitem__(self, point: Point3, active: bool):
        if active:
            self.active_points.add(point)
        else:
            if point in self.active_points:
                self.active_points.remove(point)

    def __getitem__(self, point: Point3):
        if point in self.active_points:
            return True
        return False


class Grid4:
    def __init__(self):
        self.active_points: set[Point4] = set()

    def __setitem__(self, point: Point4, active: bool):
        if active:
            self.active_points.add(point)
        else:
            if point in self.active_points:
                self.active_points.remove(point)

    def __getitem__(self, point: Point4):
        if point in self.active_points:
            return True
        return False


def point_with_neighbors3(point: Point3) -> list[Point3]:
    seen: dict[Point3, list[Point3]] = {}

    def calc() -> list[Point3]:
        points: list[Point3] = []
        for offx, offy, offz in itertools.product(range(-1, 2), repeat=3):
            points.append(Point3(point.x + offx, point.y + offy, point.z + offz))
        return points

    if point in seen:
        return seen[point]
    points = calc()
    seen[point] = points
    return points


def point_with_neighbors4(point: Point4) -> list[Point4]:
    seen: dict[Point4, list[Point4]] = {}

    def calc() -> list[Point4]:
        points: list[Point4] = []
        for offx, offy, offz, offw in itertools.product(range(-1, 2), repeat=4):
            points.append(
                Point4(point.x + offx, point.y + offy, point.z + offz, point.w + offw)
            )
        return points

    if point in seen:
        return seen[point]
    points = calc()
    seen[point] = points
    return points


def active_neighbors3(point: Point3, grid: Grid3) -> int:
    count = 0
    for offx, offy, offz in itertools.product(range(-1, 2), repeat=3):
        if offx == 0 and offy == 0 and offz == 0:
            continue
        if grid[Point3(point.x + offx, point.y + offy, point.z + offz)]:
            count += 1
    return count


def active_neighbors4(point: Point4, grid: Grid4) -> int:
    count = 0
    for offx, offy, offz, offw in itertools.product(range(-1, 2), repeat=4):
        if offx == 0 and offy == 0 and offz == 0 and offw == 0:
            continue
        if grid[
            Point4(
                point.x + offx,
                point.y + offy,
                point.z + offz,
                point.w + offw,
            )
        ]:
            count += 1
    return count


def next_state3(point: Point3, grid: Grid3) -> bool:
    n = active_neighbors3(point, grid)
    if grid[point]:
        return n == 2 or n == 3
    return n == 3


def next_state4(point: Point4, grid: Grid4) -> bool:
    n = active_neighbors4(point, grid)
    if grid[point]:
        return n == 2 or n == 3
    return n == 3


def solve_part_1(lines: list[str]):
    grid = Grid3()
    for y, line in enumerate(lines):
        for x, token in enumerate(line):
            grid[Point3(x, y, 0)] = token == "#"
    for _ in range(6):
        next_grid = Grid3()
        for active_point in grid.active_points:
            for point in point_with_neighbors3(active_point):
                next_grid[point] = next_state3(point, grid)
        grid = next_grid
    return len(grid.active_points)


def solve_part_2(lines: list[str]):
    grid = Grid4()
    for y, line in enumerate(lines):
        for x, token in enumerate(line):
            grid[Point4(x, y, 0, 0)] = token == "#"
    for _ in range(6):
        next_grid = Grid4()
        for active_point in grid.active_points:
            for point in point_with_neighbors4(active_point):
                next_grid[point] = next_state4(point, grid)
        grid = next_grid
    return len(grid.active_points)


if __name__ == "__main__":
    with open("day17_input.txt") as f:
        lines = [line.strip() for line in f.readlines()]
        print(solve_part_1(lines))
        print(solve_part_2(lines))
