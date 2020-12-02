valid = valid2 = 0

for l in open("input.txt").readlines():
    parts = l.split(' ')
    min_l, max_l = [int(p) for p in parts[0].split("-")]
    letter, password = parts[1][0], parts[2]
    if min_l <= password.count(letter) <= max_l:
        valid += 1
    if (password[min_l - 1] + password[max_l - 1]).count(letter) == 1:
        valid2 += 1

print(valid)
print(valid2)
