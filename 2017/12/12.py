from collections import defaultdict
graph = defaultdict(list)

for l in open("input").readlines():
    parts = l.strip().split(" ")
    root = parts[0]
    children = [p.strip(",") for p in parts[2:]]
    graph[root].extend(children)
    for child in children:
        if child != root:
            graph[root].append(child)


def visitable(graph, current, seen=None):
    if seen is None:
        seen = set()
    for child in graph.get(current, ()):
        if child in seen:
            continue
        seen.add(child)
        for s in visitable(graph, child, seen):
            seen.add(s)
    return seen


seen = visitable(graph, '0')

print(len(seen))

group = 1

for current in graph.keys():
    if current in seen:
        continue
    new_seen = visitable(graph, current)
    group += 1
    for s in new_seen:
        seen.add(s)

print(group)
