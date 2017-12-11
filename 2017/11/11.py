def dist(raw):
    data = raw.split(",")

    pos = [0, 0, 0]  # x, y, z
    furthest = 0

    for move in data:
        if move == "n":
            pos[1] += 1
            pos[2] -= 1
        elif move == "s":
            pos[1] -= 1
            pos[2] += 1
        elif move == "ne":
            pos[0] -= 1
            pos[1] += 1
        elif move == "nw":
            pos[0] += 1
            pos[2] -= 1
        elif move == "se":
            pos[0] -= 1
            pos[2] += 1
        elif move == "sw":
            pos[0] += 1
            pos[1] -= 1
        else:
            assert False, move
        furthest = max(furthest, abs(pos[0]), abs(pos[1]), abs(pos[2]))

    return(max(abs(pos[0]), abs(pos[1]), abs(pos[2])), furthest)


raw = "ne,ne,ne"         # is 3 steps away.
print(dist(raw))

raw = "ne,ne,sw,sw"     # is 0 steps away (back where you started).
print(dist(raw))

raw = "ne,ne,s,s"       # is 2 steps away (se,se).
print(dist(raw))

raw = "se,sw,se,sw,sw"  # is 3 steps away (s,s,sw).
print(dist(raw))

raw = open("input").read().strip()
print(dist(raw))
