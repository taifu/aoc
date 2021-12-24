class ALU:
    def __init__(self, data):
        self.instructions = []
        self.variables = {}
        for raw_instruction in data.strip().split('\n'):
            op, remainder = raw_instruction[:3], raw_instruction[4:]
            try:
                func = getattr(self, op)
            except AttributeError:
                raise Exception(f"Instruction not implemented: {raw_instruction}")
            arguments = []
            for argument in remainder.split(' '):
                if argument.isalpha():
                    arguments.append(argument)
                    self.variables[argument] = 0
                else:
                    arguments.append(int(argument))
            self.instructions.append((func, arguments))

    def value(self, variable):
        if isinstance(variable, int):
            return variable
        return self.variables[variable]

    def inp(self, arguments):
        self.variables[arguments[0]] = self.inputs.pop(0)

    def add(self, arguments):
        self.variables[arguments[0]] += self.value(arguments[1])

    def mul(self, arguments):
        self.variables[arguments[0]] *= self.value(arguments[1])

    def div(self, arguments):
        self.variables[arguments[0]] /= self.value(arguments[1])

    def mod(self, arguments):
        self.variables[arguments[0]] %= self.value(arguments[1])

    def eql(self, arguments):
        self.variables[arguments[0]] = 1 if self.variables[arguments[0]] == self.value(arguments[1]) else 0

    def run(self, inputs):
        self.inputs = inputs
        for instruction, arguments in self.instructions:
            instruction(arguments)
        return self.variables


class Monad:
    cache = None

    def __init__(self, data):
        raws = [("inp " + alu).strip().split('\n') for alu in data.split("inp ") if alu.strip()]
        #
        # Example of one of 14 ALU
        #
        #  0: inp w
        #  1: mul x 0                 .
        #  2: add x z                 .
        #  3: mod x 26                .=> x = z % 26
        #  4: div z 1   <---- M         . if 1 does nothing otherwise z = z // 26
        #  5: add x 10  <---- N         .
        #  6: eql x w                   . = x = 1 if (input == z % 26 + N) else 0
        #  7: eql x 0                   . = invert x => x = 1 if (input != z % 26 + N) else 0
        #  8: mul y 0                 .
        #  9: add y 25                .
        # 10: mul y x                 .
        # 11: add y 1                 . => y == 26 if (input != z % 26 + N) else 1
        # 12: mul z y                 z = z * (26 if y == 26 else 1)
        # 13: mul y 0                   .
        # 14: add y w                   .
        # 15: add y 8   <---- P         . => y = input + P if (input != z % 26 + N) else 0
        # 16: mul y x                 z = z + [y (input + P) if (input != z % 26 + N) else 0]
        #
        # Only differences are line 4, 5, 15 (zero based)
        assert all(raws[0][x] == raws[n][x] for x in list(range(4)) + list(range(6, 15)) + [16, 17] for n in range(1, 14))
        #
        #     ------0---1--2--3--4---5--6---7---8--9-10-11-12--13
        #  4: div z 1   1  1  1  1  26  1  26  26  1 26 26 26  26 (Ms)
        #  5: add x 10 12 10 12 11 -16 10 -11 -13 13 -8 -1 -4 -14 (Ns)
        #
        # 15: add y 12  7  8  8 15  12  8  13   3 13  3  9  4  13 (Ps)
        #
        # 17: add z y
        #
        # when (4) is  1 -> (5) is positive among 10, 11, 12, 13
        # when (4) is 26 -> (5) is negative among -1, -4, -8, -11, -13, -14, -16
        #
        # when (4) is 1 it does nothing
        # when (4) is 26 it pops a value from the stack z
        #
        # the program is a sequence of push and pop and somethime other push (if M == 26)
        #
        # Save all different values for N, M and P
        self.Ms = [int(raw[4].split(' ')[-1]) for raw in raws]
        self.Ns = [int(raw[5].split(' ')[-1]) for raw in raws]
        self.Ps = [int(raw[15].split(' ')[-1]) for raw in raws]

    def run(self):
        if self.cache:
            return self.cache
        stack = []
        digits_deps = []
        for n, op in enumerate(self.Ms):
            if op == 1:  # push
                stack.append((n, self.Ps[n]))
            elif op == 26:  # pop
                n_constraining, value = stack.pop()
                digits_deps.append((n, n_constraining, value + self.Ns[n]))

        assert len(digits_deps) == 7
        min_digits, max_digits = {}, {}
        for digit_main, digit_dep, offset in digits_deps:
            first = True
            for digit in range(1, 10):
                if 0 < (digit + offset) < 10:
                    if first:
                        min_digits[digit_dep] = digit
                        min_digits[digit_main] = digit + offset
                        first = False
                    max_digits[digit_dep] = digit
                    max_digits[digit_main] = digit + offset

        self.cache = ["".join(str(v) for k, v in sorted(digits.items())) for digits in (max_digits, min_digits)]
        return self.cache


def solve1(data):
    return Monad(data).run()[0]


def solve2(data):
    return Monad(data).run()[1]


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
