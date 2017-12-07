from collections import defaultdict

weights = {}
balances = {}

balances = {}
which_childs = {}
which_father = {}
levels = defaultdict(list)

for l in open("input", "r").readlines():
    parts = l.strip().split(" ")
    name = parts[0]
    number = int(parts[1][1:-1])
    if len(parts) > 3:
        childs = "".join(parts[3:]).split(",")
    else:
        childs = []

    weights[name] = number
    which_childs[name] = childs
    balances[name] = 0
    for child in childs:
        which_father[child] = name

root = list(which_father.keys())[0]
while root in which_father:
    root = which_father[root]
print(root)

nodes = list(weights.keys())
level = 0
levels[level] = [root]
nodes.remove(root)
while nodes:
    level += 1
    for father in levels[level - 1]:
        for child in which_childs[father]:
            levels[level].append(child)
            nodes.remove(child)

original_weights = weights.copy()

found = False

for level in reversed(sorted(levels.keys())):
    fathers = set()
    for child in levels[level]:
        if child == root:
            continue
        fathers.add(which_father[child])
    for father in fathers:
        child_weights = defaultdict(list)
        for child in which_childs[father]:
            child_weights[weights[child]].append(child)
            weights[father] += weights[child]
        if len(child_weights) > 1:
            for k, v in child_weights.items():
                if len(v) == 1:
                    wrong, wrong_weight = v[0], k
                else:
                    right, right_weight = v[0], k
            print(original_weights[wrong] + right_weight - wrong_weight)
            found = True
            break
    if found:
        break
