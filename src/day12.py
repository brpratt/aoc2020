from collections import namedtuple

Action = namedtuple("Action", ["kind", "amount"])

def parse_action(s):
    return Action(s[0], int(s[1:]))

class Ship1:
    x = 0
    y = 0
    dirx = 1
    diry = 0

    def _move_n(self, amount):
        self.y += amount

    def _move_s(self, amount):
        self.y -= amount

    def _move_e(self, amount):
        self.x += amount

    def _move_w(self, amount):
        self.x -= amount

    def _move_f(self, amount):
        self.x += self.dirx * amount
        self.y += self.diry * amount

    def _move_l(self, amount):
        cos = 0
        sin = 0
        if amount == 90:
            sin = 1
        elif amount == 180:
            cos = -1
        else:
            sin = -1
        newdirx = self.dirx * cos - self.diry * sin
        newdiry = self.dirx * sin + self.diry * cos
        self.dirx, self.diry = newdirx, newdiry

    def _move_r(self, amount):
        self._move_l(360 - amount)

    _movements = {
        "N": _move_n,
        "S": _move_s,
        "E": _move_e,
        "W": _move_w,
        "F": _move_f,
        "L": _move_l,
        "R": _move_r
    }

    def move(self, action):
        self._movements[action.kind](self, action.amount)


class Ship2:
    x = 0
    y = 0
    wayx = 10
    wayy = 1

    def _move_n(self, amount):
        self.wayy += amount

    def _move_s(self, amount):
        self.wayy -= amount

    def _move_e(self, amount):
        self.wayx += amount

    def _move_w(self, amount):
        self.wayx -= amount

    def _move_f(self, amount):
        self.x += self.wayx * amount
        self.y += self.wayy * amount

    def _move_l(self, amount):
        cos = 0
        sin = 0
        if amount == 90:
            sin = 1
        elif amount == 180:
            cos = -1
        else:
            sin = -1
        newwayx = self.wayx * cos - self.wayy * sin
        newwayy = self.wayx * sin + self.wayy * cos
        self.wayx, self.wayy = newwayx, newwayy

    def _move_r(self, amount):
        self._move_l(360 - amount)

    _movements = {
        "N": _move_n,
        "S": _move_s,
        "E": _move_e,
        "W": _move_w,
        "F": _move_f,
        "L": _move_l,
        "R": _move_r
    }

    def move(self, action):
        self._movements[action.kind](self, action.amount)


def solve_part_1(actions):
    ship = Ship1()
    for action in actions:
        ship.move(action)
    return abs(ship.x) + abs(ship.y)

def solve_part_2(actions):
    ship = Ship2()
    for action in actions:
        ship.move(action)
    return abs(ship.x) + abs(ship.y)

if __name__ == "__main__":
    with open("day12_input.txt") as f:
        actions = [parse_action(line) for line in f.readlines()]
        print(solve_part_1(actions))
        print(solve_part_2(actions))