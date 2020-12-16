def closest_times(target, buses):
    time = 0
    for bus in buses:
        while time < target:
            time += bus
        yield bus, time
        time = 0

def solve_part_1(lines):
    target = int(lines[0])
    buses = [int(x) for x in lines[1].split(",") if x != "x"]
    bus, time = min(closest_times(target, buses), key=lambda x: x[1])
    return bus * (time - target)

def solve_part_2(lines):
    [first_bus, *other_buses] = [(idx, int(x)) for idx, x in enumerate(lines[1].split(",")) if x != "x"]
    time = 0
    sequential = False
    while not sequential:
        time += first_bus[1]
        sequential = True
        for offset, bus_id in other_buses:
            if (time + offset) % bus_id != 0:
                sequential = False
    return time

if __name__ == "__main__":
    with open("day13_test_input.txt") as f:
        lines = [line.strip() for line in f.readlines()]
        print(solve_part_1(lines))
        print(solve_part_2(lines))