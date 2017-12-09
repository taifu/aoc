data = open("input").read().strip()


def size(data, expand=False):
    l = 0
    while True:
        pos = data.find("(")
        if pos == -1:
            l += len(data)
            break
        l += pos
        pos2 = data.index(")")
        cont, mult = [int(p) for p in data[pos + 1: pos2].split("x")]
        buf, data = data[pos2 + 1: pos2 + 1 + cont], data[pos2 + 1 + cont:]
        if expand:
            l += mult * size(buf, expand)
        else:
            l += mult * cont
    return l

print(size(data))
print(size(data, True))
