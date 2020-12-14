from collections import defaultdict


def parse(data):
    masks = []
    for line in data.strip().split('\n'):
        parts = line.split(" = ")
        if line[:4] == 'mask':
            masks.append((parts[1], []))
        else:
            masks[-1][1].append((int(parts[0][4:-1]), int(parts[1])))
    return masks


def masked(value, size=36):
    return bin(value)[2:].rjust(size, '0')


def apply_mask(mask, value):
    bits = masked(value)
    value_masked = ''
    for n, bit in enumerate(mask):
        if bit == 'X':
            value_masked += bits[n]
        else:
            value_masked += bit
    return int(value_masked, 2)


def apply_mask2(mask, value):
    bits = masked(value)
    value_masked = ''
    xs = []
    for n, bit in enumerate(mask):
        if bit == '0':
            value_masked += bits[n]
        elif bit == '1':
            value_masked += '1'
        else:
            value_masked += '_'
            xs.append(n)
    addrs = []
    for floating in range(2**(len(xs))):
        new_addr = list(value_masked)
        bits = masked(floating, len(xs))
        for n, pos in enumerate(xs):
            new_addr[pos] = bits[n]
        addrs.append(int(''.join(new_addr), 2))
    return addrs


def solve(data, step=1):
    masks = parse(data)
    values = defaultdict(int)
    for mask, ops in masks:
        for add, value in ops:
            if step == 1:
                values[add] = apply_mask(mask, value)
            else:
                for addr in apply_mask2(mask, add):
                    values[addr] = value
    return sum(values.values())


def solve2(data):
    return solve(data, 2)


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve(data))
    print(solve2(data))
