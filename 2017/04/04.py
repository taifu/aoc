passphrases = [l.split() for l in open("input", "r").readlines()]

passphrases_ordered = [["".join(sorted(p)) for p in l] for l in passphrases]

for p in (passphrases, passphrases_ordered):
    print(sum(1 if len(set(l)) == len(l) else 0 for l in p))
