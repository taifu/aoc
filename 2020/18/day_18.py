from operator import add, mul


def parse(data):
    exprs = []
    for line in data.strip().split('\n'):
        line = line.replace("(", "( ").replace(")", " )")
        exprs.append(list(int(x) if x.isdigit() else (add if x == '+' else mul if x == '*' else x) for x in line.split(" ")))
    return exprs


def find_closing(expr, pos):
    opened = 1
    while opened > 0:
        pos += 1
        if expr[pos] == ")":
            opened -= 1
        elif expr[pos] == "(":
            opened += 1
    return pos


def evaluate(expr, precedence):
    while "(" in expr:
        pos = expr.index("(")
        closing = find_closing(expr, pos)
        expr[pos:closing + 1] = [evaluate(expr[pos + 1:closing], precedence)]
    while precedence in expr:
        pos = expr.index(precedence)
        expr[pos - 1:pos + 2] = [precedence(expr[pos - 1], expr[pos + 1])]
    tot = expr.pop(0)
    while len(expr) > 1:
        tot = expr.pop(0)(tot, expr.pop(0))
    return tot


def solve(data, precedence=None):
    exprs = parse(data)
    tot = 0
    for expr in exprs:
        tot += evaluate(expr, precedence)
    return tot


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve(data))
    print(solve(data, precedence=add))
    print(solve(data, precedence=mul))
