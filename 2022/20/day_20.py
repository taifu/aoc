def load(data):
    return [int(line) for line in data.strip().split("\n")]


class Item:
    def __init__(self, n):
        self.n = n
        self.next = self.prev = None

    def move(self, delta):
        assert delta > 0
        item = self
        while delta:
            item = item.next
            delta -= 1
        if item.next is self:
            return
        self.prev.next, self.next.prev = self.next, self.prev
        self.prev, self.next = item, item.next
        item.next.prev = item.next = self


def decrypt(data, times=1, key=1):
    length = len(data)
    msg = {}
    zero = None
    for pos, value in enumerate(data):
        value *= key
        msg[pos] = Item(value)
        if value == 0:
            zero = msg[pos]
        if pos > 0:
            msg[pos - 1].next = msg[pos]
            msg[pos].prev = msg[pos - 1]
    msg[pos].next = msg[0]
    msg[0].prev = msg[pos]
    for time in range(times):
        for pos in range(length):
            delta = msg[pos].n
            skip = (length - 1) * abs(delta // (length - 1))
            if delta < 0:
                delta += skip
            if delta >= length:
                delta += -skip
            if delta:
                msg[pos].move(delta)
    item = zero
    n = tot = 0
    which = set([1000, 2000, 3000])
    while which:
        item = item.next
        n += 1
        if n in which:
            tot += item.n
            which.remove(n)
    return tot


def solve1(data):
    return decrypt(load(data))


def solve2(data):
    return decrypt(load(data), times=10, key=811589153)


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
