from collections import Counter

threes = twos = 0

ids = [id.strip() for id in open("input.txt").readlines()]

for id in ids:
    count = Counter(id.strip())
    twos += 1 if 2 in count.values() else 0
    threes += 1 if 3 in count.values() else 0

print(twos * threes)

for n in range(len(ids[0])):
    new_ids = [id[:n] + id[n + 1:] for id in ids]
    most_common = Counter(new_ids).most_common()[0]
    if most_common[1] == 2:
        print(most_common[0])
        break
