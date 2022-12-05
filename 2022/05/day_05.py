def load(data):
    moves, crates = [], []
    for line in data.split("\n"):
        if not line:
            continue
        if line[1] == "1":
            piles = [[] for n in range(len(line.split()))]
        elif line[0] == "m":
            parts = line.split()
            moves.append([int(parts[n]) - (1 if n > 1 else 0) for n in (1, 3, 5)])
        else:
            crates.append(line)
    for line in crates[::-1]:
        for n, pile in enumerate(piles):
            crate = line[1 + 4*n].strip()
            if crate:
                pile.append(crate)
    return piles, moves


def move(piles, moves, normal=True):
    for how_many, pile_from, pile_to in moves:
        if normal:
            for n in range(how_many):
                piles[pile_to].append(piles[pile_from].pop())
        else:
            for n in range(how_many, 0, -1):
                piles[pile_to].append(piles[pile_from].pop(-n))
    return "".join(pile.pop() for pile in piles)

def solve1(data):
    return move(*load(data))


def solve2(data):
    return move(*load(data), False)


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
