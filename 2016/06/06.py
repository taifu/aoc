from collections import Counter

counts = [[] for i in range(8)]

for line in open("input").readlines():
    for i, c in enumerate(line.strip()):
        counts[i].append(c)

print("".join(Counter(count).most_common()[0][0] for count in counts))
print("".join(Counter(count).most_common()[-1][0] for count in counts))
