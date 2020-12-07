def solve(data):
    valid = valid2 = 0

    for l in data.strip().split('\n'):
        parts = l.split(' ')
        min_l, max_l = [int(p) for p in parts[0].split("-")]
        letter, password = parts[1][0], parts[2]
        if min_l <= password.count(letter) <= max_l:
            valid += 1
        if (password[min_l - 1] + password[max_l - 1]).count(letter) == 1:
            valid2 += 1
    return valid, valid2


if __name__ == "__main__":
    print(solve(open("input.txt").read()))
