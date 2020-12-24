from collections import defaultdict


DELTA = {"e": (1, -1, 0),
         "se": (1, 0, -1),
         "sw": (0, 1, -1),
         "w": (-1, 1, 0),
         "nw": (-1, 0, 1),
         "ne": (0, -1, 1),
         }


def parse_line(line):
    chars, move = list(line), ""
    while chars:
        move += chars.pop(0)
        try:
            yield DELTA[move]
            move = ""
        except KeyError:
            pass


def parse(data):
    return [list(parse_line(line)) for line in data.strip().split("\n")]


def adjacent(tile, move):
    return (tile[0] + move[0], tile[1] + move[1], tile[2] + move[2])


def move(tile, moves):
    for move in moves:
        tile = adjacent(tile, move)
    return tile


def solve1(data):
    rows, tiles = parse(data), set()
    for moves in rows:
        tile = move((0, 0, 0), moves)
        try:
            tiles.remove((tile))
        except KeyError:
            tiles.add((tile))
    return tiles


def solve2(blacks, steps=100):
    for step in range(steps):
        count_blacks = defaultdict(int)
        for black in blacks:
            for delta in DELTA.values():
                next_tile = adjacent(black, delta)
                count_blacks[next_tile] += 1
        next_blacks = set()
        for tile, count_black in count_blacks.items():
            if count_black in (1, 2) and tile in blacks:
                next_blacks.add(tile)
            elif count_black == 2 and tile not in blacks:
                next_blacks.add(tile)
        blacks = next_blacks
    return len(blacks)


if __name__ == "__main__":
    data = open("input.txt").read()
    blacks = solve1(data)
    print(len(blacks))
    print(solve2(blacks))
