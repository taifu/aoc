def count(from_, to_):
    tot = 0
    tot2 = 0
    for pwd in range(from_, to_ + 1):
        a, b, c, d, e, f = [int(p) for p in str(pwd)]
        if a <= b <= c <= d <= e <= f and (a == b or b == c or c == d or d == e or e == f):
            tot += 1
            parts = [a, b, c, d, e, f]
            simil = set()
            adiac = 1
            n = 0
            while n < 5:
                if parts[n] != parts[n + 1]:
                    simil.add(adiac)
                    adiac = 1
                else:
                    adiac += 1
                n += 1
            simil.add(adiac)
            if 2 in simil:
                tot2 += 1
    return tot, tot2


if __name__ == "__main__":
    from_, to_ = [int(p) for p in "357253-892942".split("-")]
    tot, tot2 = count(from_, to_)
    print(tot)
    print(tot2)
