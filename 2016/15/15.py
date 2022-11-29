def solve(discs):
    wait = 0

    while True:
        second = wait + 1
        for disc in discs:
            if (disc[1] + second) % disc[0] != 0:
                break
            second += 1
        else:
            return wait
            break
        wait += 1


rows = [l.strip().split() for l in open("input").readlines()]
discs = [[int(parts[3]), int(parts[11][:-1])] for parts in rows]

print(solve(discs))

discs += [[11, 0]]

print(solve(discs))
