istructions = [l.strip() for l in open("input", "r").readlines()[0].split(",")]

def check(pos, seen=set()):
    if not None in seen:
        if tuple(pos[:2]) in seen:
            print("2: {}".format(sum(abs(x) for x in pos[:2])))
            seen.add(None)
        else:
            seen.add(tuple(pos[:2]))

def go(pos, where, step):
    if where == 'R':
        pos[2] -= 90
    else:
        pos[2] += 90
    pos[2] %= 360
    if pos[2] == 90:
        for s in range(step):
            pos[1] += 1
            check(pos)
    elif pos[2] == 180:
        for s in range(step):
            pos[0] -= 1
            check(pos)
    elif pos[2] == 270:
        for s in range(step):
            pos[1] -= 1
            check(pos)
    else:
        for s in range(step):
            pos[0] += 1
            check(pos)

pos = [0, 0, 90]

for instruction in istructions:
    where, step = instruction[0], int(instruction[1:])
    go(pos, where, step)

print("1: {}".format(sum(abs(x) for x in pos[:2])))
