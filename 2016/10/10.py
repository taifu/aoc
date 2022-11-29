instructions = [i.strip() for i in open("input").readlines()]

bots = {}
gives = {}

for instruction in instructions[:]:
    parts = instruction.split()
    if parts[0] == "value":
        name = parts[-1]
        bots[name] = sorted(bots.get(name, []) + [int(parts[1])])
        instructions.remove(instruction)
    else:
        name = parts[1]
        assert name not in gives
        gives[name] = (parts[5], parts[6], parts[10], parts[11])

while True:
    twos = 0
    for name, chips in bots.items():
        if len(chips) == 2:
            twos += 1
            if chips == [17, 61]:
                print(name)
            type_low, name_low, type_high, name_high  = gives[name]
            if type_low == "output":
                name_low += "o"
            if type_high == "output":
                name_high += "o"
            bots[name_low] = sorted(bots.get(name_low, []) + [chips[0]])
            bots[name_high] = sorted(bots.get(name_high, []) + [chips[1]])
            bots[name] = []
    if twos == 0:
        break
print(bots["0o"][0] * bots["1o"][0] * bots["2o"][0])
