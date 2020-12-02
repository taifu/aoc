from itertools import combinations

numbers = [int(l) for l in open("input.txt").readlines() if l]

for a, b in combinations(numbers, 2):
    if a + b == 2020:
        print(a * b)
        break

for a, b, c in combinations(numbers, 3):
    if a + b + c == 2020:
        print(a * b * c)
        break
