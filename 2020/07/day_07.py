from collections import defaultdict


def count(tree, main_bag):
    tot = 0
    for bag, how_many in tree[main_bag].items():
        tot += how_many + how_many * count(tree, bag)
    return tot


def explore(tree, what, main_bag):
    if what in tree[main_bag]:
        return True
    for bag, contain in tree[main_bag].items():
        if bag == what:
            return True
        else:
            if explore(tree, what, bag):
                return True
    return False


def solve(data):
    tree = defaultdict(dict)
    for rule in data.strip().split("\n"):
        parts = rule.strip(".").split(" bags contain ")
        main_bag = parts[0]
        others = parts[1].split(", ")
        if others[0] == 'no other bags':
            tree[main_bag] = {}
        else:
            for other in others:
                other = other.rstrip("s")[:-4]
                parts = other.split(" ")
                how_many = int(parts[0].replace("no", "0"))
                bag = " ".join(parts[1:])
                tree[main_bag][bag] = how_many
    what = 'shiny gold'
    bags = list(tree.keys())
    tot = 0
    for main_bag in bags:
        if main_bag == what:
            continue
        if explore(tree, what, main_bag):
            tot += 1
    tot2 = 0
    for main_bag, how_many in tree[what].items():
        tot2 += how_many + how_many * count(tree, main_bag)
    return tot, tot2


if __name__ == "__main__":
    data = open("input.txt").read()
    part1, part2 = solve(data)
    print(part1)
    print(part2)
