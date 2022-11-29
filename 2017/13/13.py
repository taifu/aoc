raw = open("input").read().strip()

layers = dict((int(l.strip()), int(r.strip())) for d in raw.split("\n") for l, r in [d.split(":")])

poses = tuple(layers.keys())


def gotcha(pos, time):
    try:
        return time % ((layers[pos] - 1) * 2) == 0
    except KeyError:
        return False

delay = 0

travel = max(layers.keys()) + 1

while True:
    if delay == 0:
        print(sum(pos * layers[pos] for pos in range(travel) if gotcha(pos, pos)))
    else:
        for pos in poses:
            if gotcha(pos, delay + pos):
                break
        else:
            print(delay)
            break

    delay += 1
