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
        #
        # A factor of 2*3 add one number to the output
        #    0 [2, 4, 1, 5, 7, 5, 1, 6, 4, 1, 5, 5, 0, 3, 3, 0] [3] 16 1
        #    8 [2, 4, 1, 5, 7, 5, 1, 6, 4, 1, 5, 5, 0, 3, 3, 0] [3, 2] 16 2
        #   64 [2, 4, 1, 5, 7, 5, 1, 6, 4, 1, 5, 5, 0, 3, 3, 0] [1, 3, 2] 16 3
        #  512 [2, 4, 1, 5, 7, 5, 1, 6, 4, 1, 5, 5, 0, 3, 3, 0] [3, 1, 3, 2] 16 4
        #
        # Registers: A=??? B=0 C=0
        # Program: 2,4,1,5,7,5,1,6,4,1,5,5,0,3,3,0
        #
        # 2,4 ->  B = A % 8
        # 1,5 ->  B = B ^ 5       5 -> B_xor_1
        # 7,5 ->  C = A // 2**B   => A >> B
        # 1,6 ->  B = B ^ 6       6 -> B_xor_2
        # 4,1 ->  B = B ^ C
        # 5,5 ->  out (B % 8)
        # 0,3 ->  A = A // 2**3   => A >> 3
        # 3,0 ->  IF A goto 0
        #
        A_registers = [0]
        B_xor_1 = self.program[3]
        start_diff = 6  # Changing part of input
        for n, instr in enumerate(self.program[start_diff::2]):
            if instr == 1:  # bxl
                B_xor_2 = self.program[start_diff + n * 2 + 1]
                break
        for last_digit in reversed(self.program):
            next_A_registers = []
            for current_A in A_registers:
                for new_digit_A in range(8):
                    # Append the new digit after shifting 3 bits
                    # 0b111 -> 0b111001
                    register_A = (current_A << 3) + new_digit_A
                    # First step: 2,4
                    register_B = (register_A % 8)
                    # Second step: 1,5
                    register_B ^= B_xor_1
                    # Third step: 7,5
                    register_C = register_A >> register_B
                    # Fourth step: 1,6
                    register_B ^= B_xor_2
                    # Fifth step: 4,1
                    register_B ^= register_C
                    # Sixth step: 5,5 (unused)
                    # out (B % 8)
                    # Seventh step: 0,3 (unused)
                    # register_A >>= 3
                    # Eighth step: 3,0 (unused)
                    # IF A goto 0
                    if last_digit == register_B % 8:
                        next_A_registers.append(register_A)
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
