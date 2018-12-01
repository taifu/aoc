from collections import defaultdict

def triple(part):
    return [int(v) for v in part.strip().split(",")]


def load(filename):
    particles = {}
    for i, l in enumerate(open(filename).readlines()):
        parts = l.strip().replace("<", ">").split(">")
        particles[i] = [triple(parts[1]),  # p
                        triple(parts[3]),  # v
                        triple(parts[5]),  # a
                        ]
    return particles


def evolve(particles, remove=False):
    last_closest = []
    last_removed = []
    while True:
        min_d = None, None
        positions = defaultdict(set)
        for n, [p, v, a] in particles.items():
            for i in range(3):
                v[i] += a[i]
                p[i] += v[i]
            d = sum(abs(c) for c in p)
            if min_d[0] is None or d < min_d[0]:
                min_d = d, n
            positions[tuple(p)].add(n)
        if remove:
            i = 0
            for k, v in positions.items():
                if len(v) > 1:
                    for n in v:
                        i += 1
                        del particles[n]
            if i not in last_removed:
                last_removed = [i]
            else:
                last_removed.append(i)
        if remove:
            if last_removed[0] == 0 and len(last_removed) > 1000:
                return len(particles)
        else:
            closest = min_d[1]
            if closest not in last_closest:
                last_closest = [closest]
            else:
                last_closest.append(closest)
                if len(last_closest) == 500:
                    return last_closest[0]


print(evolve(load("input")))
print(evolve(load("input"), remove=True))
