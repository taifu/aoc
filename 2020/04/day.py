import re

FIELDS = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid'])


def load_passports(data):
    passports = []
    current = {}
    for line in (data + "\n").split("\n"):
        if not line:
            if current:
                passports.append(current)
            current = {}
            continue
        for part in line.strip().split(" "):
            k, v = part.split(":")
            current[k] = v
    return passports


def part1(data, validation=False):
    passports = load_passports(data)
    optionals = set(['cid'])
    valid = 0

    for passport in passports:
        missing = FIELDS - set(passport.keys())
        if not missing or missing == optionals:
            if validation:
                year = int(passport['byr'])
                if not 1920 <= year <= 2002:
                    continue
                year = int(passport['iyr'])
                if not 2010 <= year <= 2020:
                    continue
                year = int(passport['eyr'])
                if not 2020 <= year <= 2030:
                    continue
                hgt = passport['hgt']
                if not re.fullmatch(r"\d+(in|cm)", hgt):
                    continue
                value, measure = int(hgt[:-2]), hgt[-2:]
                if measure == 'cm' and not 150 <= value <= 193:
                    continue
                if measure == 'in' and not 59 <= value <= 76:
                    continue
                hcl = passport['hcl']
                if not re.fullmatch(r"#[0-9a-f]{6}", hcl):
                    continue
                if passport['ecl'] not in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'):
                    continue
                if not re.fullmatch(r"[0-9]{9}", passport['pid']):
                    continue
            valid += 1
    return valid


if __name__ == "__main__":
    data = open("input.txt").read()
    print(part1(data))

    print(part1(data, True))
