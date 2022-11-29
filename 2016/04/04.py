from collections import Counter

tot = 0

def dec(n, letter):
    if letter == ' ':
        return ' '
    return chr(ord('a') + (ord(letter) - ord('a') + n) % 26)

for room in open("input", "r").readlines():
    parts = room.strip().split("-")
    name = " ".join(parts[:-1])
    count = Counter(name.replace(" ", ""))
    parts = parts[-1].split("[")
    id = int(parts[0])
    check = parts[1][:-1]
    if check == "".join(c[3] for c in sorted(["{:03d}".format(1000 - v) + k for k, v in count.most_common()])[:5]):
        tot += id
        name = "".join(dec(id, letter) for letter in name)
        if "north" in name:
            print(name, id)

print(tot)


