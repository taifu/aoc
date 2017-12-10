data = [n for n in range(256)]
lengths = [46,41,212,83,1,255,157,65,139,52,39,254,2,86,0,204]

pos = skip = 0
l = len(data)

for length in lengths:
    new_data = [data[d % l] for d in range(pos + length - 1, pos - 1, -1)]
    if pos + length <= l:
        data[pos:pos + length] = new_data
    else:
        delta = pos + length - l
        data[pos:pos + length - delta] = new_data[:-delta]
        data[:delta] = new_data[-delta:]

    pos = (pos + length + skip) % l
    skip += 1

print(data[0] * data[1])

data = [n for n in range(256)]
lengths = [ord(c) for c in "46,41,212,83,1,255,157,65,139,52,39,254,2,86,0,204"] + [17, 31, 73, 47, 23]


pos = skip = 0
l = len(data)

for round in range(64):
    for length in lengths:
        new_data = [data[d % l] for d in range(pos + length - 1, pos - 1, -1)]
        if pos + length <= l:
            data[pos:pos + length] = new_data
        else:
            delta = pos + length - l
            data[pos:pos + length - delta] = new_data[:-delta]
            data[:delta] = new_data[-delta:]

        pos = (pos + length + skip) % l
        skip += 1

dense = ""
for n in range(16):
    d = data[n * 16]
    for m in range(16 * n + 1, 16 * (n + 1)):
        d = d ^ data[m]
    dense += hex(256 + d)[-2:]

print(dense)
