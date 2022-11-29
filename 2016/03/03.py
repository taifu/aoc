wrong = right = 0

for l in open("input", "r").readlines():
    side = [int(s) for s in l.split()]
    if side[0] >= side[1] + side[2] or side[1] >= side[0] + side[2] or side[2] >= side[1] + side[0]:
        wrong += 1
    else:
        right += 1

print(right)


wrong = right = 0

side = []
for l in open("input", "r").readlines():
    side.append([int(s) for s in l.split()])
    if len(side) == 3:
        for n in range(3):
            if side[0][n] >= side[1][n] + side[2][n] or side[1][n] >= side[0][n] + side[2][n] or side[2][n] >= side[1][n] + side[0][n]:
                wrong += 1
            else:
                right += 1
        side = []

print(right)

