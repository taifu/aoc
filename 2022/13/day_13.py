from functools import cmp_to_key


def load(data):
    pairs = []
    for lines in data.strip().split("\n\n"):
        pairs.append([eval(line) for line in lines.split("\n")])
    return pairs


def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if right == left:
            return None
        return right >= left
    if isinstance(left, int):
        left = [left]
    if isinstance(right, int):
        right = [right]
    assert type(left) == type(right) == list, f"{left} != {right}"
    last_more = False
    for left_item, right_item in zip(left, right):
        ret = compare(left_item, right_item)
        if ret is not None:
            return ret
    if len(left) < len(right):
        return True
    if len(left) > len(right):
        return False
    return None


def compute(pairs):
    return sum(n for n, couple in enumerate(pairs, 1) if compare(*couple))


def sort(pairs):
    p2 = [[2]]
    p6 = [[6]]
    ordered = sorted((p for pair in pairs + [[p2, p6]] for p in pair),
                      key=cmp_to_key(lambda x, y: 1 if compare(x, y) else -1),
                      reverse=True)
    return (1 + ordered.index(p2)) * (1 + ordered.index(p6))


def solve1(data):
    return compute(load(data))


def solve2(data):
    return sort(load(data))


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
