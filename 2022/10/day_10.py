def noop(registers):
    return 1


def addx(registers, value):
    registers['x'] += value
    return 2


def load(data):
    instructions = []
    for line in data.strip().split("\n"):
        if line == "noop":
            instructions.append((noop, []))
        elif line.startswith("addx"):
            instructions.append((addx, [int(line[5:])]))
        else:
            assert False, f"Unknown instruction: \"{line}\""
    return instructions


def read(pixels, width):
    n = 0
    screen = ""
    while n < len(pixels):
        screen += "".join(pixels[n:n + width]) + '\n'
        n += width
    return screen.strip()


def compute(instructions):
    registers = {'x': 1}
    clock, strength, check, width = 0, 0, 20, 40
    cycle, scan, pixels = 0, 0, []
    for func, args in instructions:
        prev = registers['x']
        clock += func(*([registers] + args))
        while scan < clock:
            pixels.append('#' if scan % width >= prev - 1 and scan % width < prev + 2 else '.')
            scan += 1
        if clock >= check:
            strength += check * prev
            check += width
    return strength, read(pixels, width)


def solve1(data):
    return compute(load(data))[0]


def solve2(data):
    return compute(load(data))[1]


if __name__ == "__main__":
    data = open("input.txt").read()

    print(solve1(data))
    print(solve2(data))
