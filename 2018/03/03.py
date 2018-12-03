SIZE = 1000
fabric = [[0] * SIZE for x in range(SIZE)]

patches = {}

for line in open("input.txt").readlines():
    # Format: #16 @ 646,318: 24x21
    parts = line.strip().split(" ")
    id = int(parts[0][1:])
    x, y = [int(p) for p in parts[2][:-1].split(",")]
    w, h = [int(p) for p in parts[3].split("x")]
    patches[id] = (x, y, w, h)

for X, Y, W, H in patches.values():
    for x in range(X, X + W):
        for y in range(Y, Y + H):
            fabric[x][y] += 1

over = 0
for x in range(SIZE):
    for y in range(SIZE):
        if fabric[x][y] > 1:
            over += 1

print(over)

for id, (X, Y, W, H) in patches.items():
    found = True
    for x in range(X, X + W):
        for y in range(Y, Y + H):
            if fabric[x][y] > 1:
                found = False
                break
        if not found:
            break
    if found:
        print(id)
        break
