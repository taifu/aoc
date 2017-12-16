mine = tuple(0 if c == "." else 1 for c in open("input").read().strip())
steps = 40

#mine = [0, 1, 1, 0, 1, 0, 1, 1, 1, 1]
#steps = 10

def next_row(mine, seen={}):
    try:
        return seen[mine]
    except KeyError:
        new_mine = []
        for n, trap in enumerate(mine):
            trap_left = mine[n - 1] if n > 0 else 0
            trap_right = mine[n + 1] if n < len(mine) - 1 else 0
            new_mine.append(1 if (trap_left, trap, trap_right) in ((1, 0, 0), (0, 0, 1), (1, 1, 0), (0, 1, 1)) else 0)
        new_mine = tuple(new_mine)
        seen[mine] = new_mine
        return new_mine

tot_mine = sum(mine)

row = 1

while row < steps:
    mine = next_row(mine)
    tot_mine += sum(mine)
    row += 1

print(steps * len(mine) - tot_mine)

steps = 400000

while row < steps:
    mine = next_row(mine)
    tot_mine += sum(mine)
    row += 1

print(steps * len(mine) - tot_mine)
