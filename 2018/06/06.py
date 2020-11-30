from collections import defaultdict

points = dict((n, tuple(int(p.strip()) for p in l.strip().split(",")))
              for n, l in enumerate(open("input.txt").readlines()))

X, Y = [max(p[0] for p in points.values()) + 1, max(p[1] for p in points.values()) + 1]

border = set()
areas = defaultdict(int)
less10000 = 0

for x in range(X + 1):
    for y in range(Y + 1):
        distance = defaultdict(list)
        tot_distance = 0
        for n, (px, py) in points.items():
            d = abs(px - x) + abs(py - y)
            distance[d].append(n)
            tot_distance += d
        if tot_distance < 10000:
            less10000 += 1
        d, ns = min(distance.items())
        if len(ns) == 1:
            n = ns[0]
            if x == 0 or y == 0 or x == X or y == Y:
                border.add(n)
            areas[n] += 1

print(max(a for n, a in areas.items() if n not in border))
print(less10000)
