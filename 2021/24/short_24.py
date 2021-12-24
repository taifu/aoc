raws = [("inp " + alu).strip().split('\n') for alu in open("input.txt").read().split("inp ") if alu.strip()]
Ms = [int(raw[4].split(' ')[-1]) for raw in raws]
Ns = [int(raw[5].split(' ')[-1]) for raw in raws]
Ps = [int(raw[15].split(' ')[-1]) for raw in raws]
stack, digits_deps = [], []
for n, op in enumerate(Ms):
    if op == 1:  # push
        stack.append((n, Ps[n]))
    elif op == 26:  # pop
        n_constraining, value = stack.pop()
        digits_deps.append((n, n_constraining, value + Ns[n]))
min_digits, max_digits = {}, {}
for digit_main, digit_dep, offset in digits_deps:
    first = True
    for digit in range(1, 10):
        if 0 < (digit + offset) < 10:
            if first:
                min_digits[digit_dep], min_digits[digit_main] = digit, digit + offset
                first = False
            max_digits[digit_dep], max_digits[digit_main] = digit, digit + offset
print('\n'.join("".join(str(v) for k, v in sorted(digits.items())) for digits in (max_digits, min_digits)))
