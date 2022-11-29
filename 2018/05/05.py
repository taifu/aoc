data = open("input.txt").read().strip()


def react(data):
    p = 0
    while p < len(data) - 1:
        if data[p].lower() == data[p + 1].lower() and data[p] != data[p + 1]:
            data = data[:p] + data[p + 2:]
            if p > 0:
                p -= 1
        else:
            p += 1
    return data


print(len(react(data)))
print(min(len(react(data.replace(c, "").replace(c.upper(), ""))) for c in "abcdefghijklmnopqrstuvwxyz"))
