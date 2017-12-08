registers = {}

max_v = 0

for instruction in open("input", "r").readlines():
    parts = instruction.split()
    reg = parts[0]
    op = parts[1]
    value = int(parts[2])
    reg_if = parts[4]
    op_if = parts[5]
    value_if = parts[6]
    if eval("{} {} {}".format(registers.get(reg_if, 0), op_if, value_if)):
        registers[reg] = registers.get(reg, 0) + (value if op == "inc" else - value)
    max_v = max(max_v, max(registers.values()))

print(max(registers.values()))
print(max_v)
