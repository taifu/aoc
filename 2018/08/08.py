raw = open("input.txt").read().strip()
# raw = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"

data = [int(p) for p in raw.split(" ")]


def explore(data):
    tot_meta = 0
    n_childs, n_meta, data, childs = data[0], data[1], data[2:], []
    for child in range(n_childs):
        newborn, add_meta, data = explore(data)
        tot_meta += add_meta
        childs.append(newborn)
    meta, data = data[:n_meta], data[n_meta:]
    tot_meta += sum(meta)
    if n_childs == 0:
        value = tot_meta
    else:
        value = sum(childs[idx - 1][1] for idx in meta if idx <= n_childs)
    return [meta, value, childs], tot_meta, data


tree, tot_meta = explore(data)[:2]

print(tot_meta)
print(tree[1])
