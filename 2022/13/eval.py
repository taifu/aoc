def compile(parts, stack):
    while parts:
        part = parts.pop(0)
        if part.isdigit():
            stack.append(int(part))
        elif part == "[":
            stack.append(compile(parts, []))
        elif part == "]":
            return stack
    return stack


def my_eval(line):
    return compile([p for p in line.replace(",", " ").replace("[", " [ ").replace("]", " ] ").split(" ") if p], [])[0]


for line in open("input.txt").read().split("\n"):
    if line:
        l1 = eval(line)
        l2 = my_eval(line)
        assert l1 == l2, f"\n{l1}\n !=\n{l2}"
