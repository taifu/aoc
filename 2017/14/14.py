key = "jzgqcdpd"


def zero_adjacent(grid, x, y, visited=set()):
    visited.add((x, y))
    grid[y][x] = 0
    if x < 127:
        if grid[y][x + 1] == 1:
            zero_adjacent(grid, x + 1, y)
    if x > 0:
        if grid[y][x - 1] == 1:
            zero_adjacent(grid, x - 1, y)
    if y < 127:
        if grid[y + 1][x] == 1:
            zero_adjacent(grid, x, y + 1)
    if y > 0:
        if grid[y - 1][x] == 1:
            zero_adjacent(grid, x, y - 1)


def knothash(value):
    data = [n for n in range(256)]
    lengths = [ord(c) for c in value] + [17, 31, 73, 47, 23]

    pos = skip = 0
    l = len(data)

    for round in range(64):
        for length in lengths:
            new_data = [data[d % l] for d in range(pos + length - 1, pos - 1, -1)]
            if pos + length <= l:
                data[pos:pos + length] = new_data
            else:
                delta = pos + length - l
                data[pos:pos + length - delta] = new_data[:-delta]
                data[:delta] = new_data[-delta:]

            pos = (pos + length + skip) % l
            skip += 1

    dense = ""
    for n in range(16):
        d = data[n * 16]
        for m in range(16 * n + 1, 16 * (n + 1)):
            d = d ^ data[m]
        dense += hex(256 + d)[-2:]
    return dense

total_used = 0
grid = []
for row in range(128):
    hash = knothash("{}-{}".format(key, row))
    current = []
    for c in hash:
        for u in ("000" + bin(int(c, 16))[2:])[-4:]:
            used = 1 if u == "1" else 0
            total_used += used
            current.append(used)
    grid.append(current)

print(total_used)

regions = 0

for x in range(128):
    for y in range(128):
        if grid[y][x] == 0:
            continue
        regions += 1
        zero_adjacent(grid, x, y)

print(regions)
