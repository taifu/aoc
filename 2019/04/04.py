def count(from_, to_):
    tot = tot2 = 0
    for pwd in range(from_, to_ + 1):
        parts = [int(p) for p in str(pwd)]
        if all(parts[n] <= parts[n + 1] for n in range(0, 5)) and any(parts[n] == parts[n + 1] for n in range(0, 5)):
            tot += 1
            simil = set()
            adiac = n = 0
            while True:
                if n == 5 or parts[n] != parts[n + 1]:
                    simil.add(adiac + 1)
                    if n == 5:
                        break
                    adiac = -1
                adiac += 1
                n += 1
            if 2 in simil:
                tot2 += 1
    return tot, tot2


if __name__ == "__main__":
    from_, to_ = [int(p) for p in "357253-892942".split("-")]
    tot, tot2 = count(from_, to_)
    print(tot)
    print(tot2)
