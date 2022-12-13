def my_eval(parts, stack=None):
    if stack is None:
        stack, parts = [], line.replace(",", " ").replace("[", " [ ").replace("]", " ] ").split(" ")[::-1]
    while parts:
        part = parts.pop()
        if part.isdigit():
            stack.append(int(part))
        elif part == "[":
            stack.append(my_eval(parts, []))
        elif part == "]":
            return stack
    return stack[0]


for line in open("input.txt").read().split("\n"):
    if line:
        l1 = eval(line)
        l2 = my_eval(line)
        assert l1 == l2, f"\n{l1}\n !=\n{l2}"
