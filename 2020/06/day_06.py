def solve(data):
    tot = common = 0
    for group in data.split("\n\n"):
        subcommon = None
        for subgroup in group.strip().split("\n"):
            answers = set(subgroup)
            if subcommon is None:
                subcommon = answers
            else:
                subcommon = subcommon.intersection(answers)
        common += len(subcommon)
        tot += len(set(group.replace("\n", "").replace(" ", "")))
    return tot, common


if __name__ == "__main__":
    data = open("input.txt").read()
    tot, common = solve(data)
    print(tot)
    print(common)
