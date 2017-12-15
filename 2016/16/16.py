def checksum(s):
    for n in range(0, len(s), 2):
        if s[n] == s[n + 1]:
            s[n / 2] = "1"
        else:
            s[n / 2] = "0"
    return s[:len(s) / 2]


def fill(size, initial):
    while len(initial) < size:
        initial = initial + "0" + "".join("1" if c == "0" else "0" for c in initial[::-1])
    initial = list(initial[:size])
    while len(initial) % 2 == 0:
        initial = checksum(initial)
    return "".join(initial)


size, initial = 20, "10000"

print(fill(size, initial))

print(fill(272, "10001110011110000"))

print(fill(35651584, "10001110011110000"))
