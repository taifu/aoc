def load(data):
    return [int(line) for line in data.strip().split("\n")]


class Item:
    def __init__(self, n):
        self.n = n
        self.next = self.prev = None

    def move(self, delta):
        if delta:
            skip = sign(delta)
            if skip == -1:
                delta -= 1
            item = self
            while delta:
                if skip == -1:
                    item = item.prev
                else:
                    item = item.next
                delta += -skip
            if item.next is self:
                return
            p1, p2 = self.next, self.prev
            p3, p4 = item, item.next
            p5 = self
            self.prev.next, self.next.prev = p1, p2
            self.prev, self.next = p3, p4
            item.next.prev, item.next = p5, p5


def sign(n):
    return (n > 0) - (n < 0)


def show(first):
    item = first
    print()
    print("======================")
    while True:
        print(item.n, end=" ")
        item = item.next
        if item is first:
            break
    print()
    item = first.prev
    while True:
        print(item.n, end=" ")
        item = item.prev
        if item is first.prev:
            break
    print()
    print("======================")
    print()


def decrypt(data):
    length = len(data)
    msg = {}
    last = first = zero = None
    for pos, value in enumerate(data):
        msg[pos] = Item(value)
        if value == 0:
            zero = msg[pos]
        if first is None:
            first = msg[pos]
        else:
            msg[pos - 1].next = msg[pos]
        if not last is None:
            msg[pos].prev = last
        last = msg[pos]
    last.next = first
    first.prev = last
    for i, (pos, item) in enumerate(sorted(msg.items())):
        old_prev, old_next = first.prev, first.next
        delta = item.n
        #if delta % length == 0:
            #continue
        while delta < 0:
            delta = length + delta - 1
        while delta >= length:
            delta = delta - length + 1
        #if abs(delta) > length // 2:
            #import pdb; pdb.set_trace()
            #delta %= length
            #delta = length - abs(delta) * sign(delta)
        #print(item.n)
        #print(delta)
        #show(first)
        #import pdb; pdb.set_trace()
        item.move(delta)
        #show(first)
        if item is first:
            first = old_next

    #show(first)
    item = zero
    n = 0
    tot = 0
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
    pass
    #return decrypt(load(data))


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
