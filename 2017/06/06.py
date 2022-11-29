banks = [4, 1, 15, 12, 0, 9, 9, 5, 5, 8, 7, 3, 14, 5, 12, 3]

L = len(banks)


for c in range(2):
    step = 0
    seen = set()

    while not tuple(banks) in seen:
        seen.add(tuple(banks))
        p = banks.index(max(banks))
        m, banks[p] = banks[p], 0
        while m > 0:
            p += 1
            banks[p % L] += 1
            m -= 1
        step += 1

    print(step)
