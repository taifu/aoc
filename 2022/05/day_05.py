def load(data):
    moves, crates = [], []
    for line in data.split("\n"):
        if not line:
            continue
        if line[1] == "1":
            stacks = [[] for n in range(len(line.split()))]
        elif line[0] == "m":
            moves.append([int(line.split()[n]) - (1 if n > 1 else 0) for n in (1, 3, 5)])
        else:
            crates.append(line)
    for line in crates[::-1]:
        for n, pile in enumerate(stacks):
            crate = line[1 + 4*n].strip()
            if crate:
                pile.append(crate)
    return stacks, moves


def move(stacks, moves, stacking=True):
    for how_many, pile_from, pile_to in moves:
        for n in range(how_many, 0, -1):
            stacks[pile_to].append(stacks[pile_from].pop(-1 if stacking else -n))
    return "".join(pile.pop() for pile in stacks)

def solve1(data):
    return move(*load(data))


def solve2(data):
    return move(*load(data), stacking=False)


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
