from typing import TypeAlias, List, Tuple, Generator, Set, Optional  # noqa: F401

A, B, C = range(3)


class Computer:
    def __init__(self, raw: str) -> None:
        parts = raw.split('\n\n')
        self.registers = [int(x.split(':')[1].strip()) for x in parts[0].split('\n')]  # A B C
        self.program = [int(x.strip()) for x in parts[1].split(':')[1].split(',')]
        self.pointer = 0
        self.output: List[int] = []

    def combo(self, operand: int) -> int:
        if operand < 4:
            return operand
        return self.registers[operand - 4]

    def do_output(self, value: int) -> None:
        self.output.append(value)

    def do_op(self) -> None:
        next_pointer = self.pointer + 2
        match self.program[self.pointer]:
            case 0:  # adv
                self.registers[A] //= 2**self.combo(self.program[self.pointer + 1])
            case 1:  # bxl
                self.registers[B] ^= self.program[self.pointer + 1]
            case 2:  # bst
                self.registers[B] = self.combo(self.program[self.pointer + 1]) % 8
            case 3:  # jnz
                if self.registers[A] != 0:
                    next_pointer = self.program[self.pointer + 1]
            case 4:  # bxc
                self.registers[B] ^= self.registers[C]
            case 5:  # out
                self.do_output(self.combo(self.program[self.pointer + 1]) % 8)
            case 6:  # bdv
                self.registers[B] = self.registers[A] // 2**self.combo(self.program[self.pointer + 1])
            case 7:  # cdv
                self.registers[C] = self.registers[A] // 2**self.combo(self.program[self.pointer + 1])
        self.pointer = next_pointer

    def execute(self) -> None:
        while self.pointer < len(self.program):
            self.do_op()

    def count(self) -> str:
        self.execute()
        return ",".join(str(v) for v in self.output)

    def count2(self) -> int:
        # Registers: A=??? B=0 C=0
        # Program: 2,4,1,5,7,5,1,6,4,1,5,5,0,3,3,0
        #
        # 2,4 ->  B = A % 8
        # 1,5 ->  B = B ^ 5     -> B_xor_1
        # 7,5 ->  C = A // 2**B
        # 1,6 ->  B = B ^ 6     -> B_xor_2
        # 4,1 ->  B = B ^ C
        # 5,5 ->  out B
        # 0,3 ->  A = A % 8
        # 3,0 ->  IF A goto 0
        #
        A_registers = [0]
        B_xor_1, B_xor_2 = self.program[3], self.program[7]
        for last_digit in reversed(self.program):
            next_A_registers = []
            for current_A in A_registers:
                for check_A in range(current_A * 8, (current_A + 1) * 8):
                    register_B = (check_A % 8)
                    register_B = register_B ^ B_xor_1
                    register_C = check_A // (2 ** register_B)
                    register_B = register_B ^ B_xor_2
                    register_B = register_B ^ register_C
                    if (last_digit ^ register_B) % 8 == check_A % 8:
                        next_A_registers.append((current_A * 8) + register_B)
            A_registers = next_A_registers
        return min(A_registers)


solution = None


def solve1(data: str) -> str:
    global solution
    if solution is None:
        solution = Computer(data)
    assert solution
    return solution.count()


def solve2(data: str) -> int:
    global solution
    if solution is None:
        solution = Computer(data)
    assert solution
    return solution.count2()


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
