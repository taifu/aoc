import sys


class Computer:
    def __init__(self, program: str):
        self.program = [int(c.strip()) for c in program.split(',')]
        self._backup = self.program[:]

    def reset(self):
        self.program = self._backup[:]

    def run(self, pos=0):
        while True:
            if self.program[pos] == 99:
                break
            op1, op2 = self.program[self.program[pos + 1]], self.program[self.program[pos + 2]]
            func = self.program[pos]
            assert func in (1, 2)
            self.program[self.program[pos + 3]] = op1 + op2 if func == 1 else op1 * op2
            pos += 4


def test_programs():
    c = Computer("1,0,0,0,99")
    c.run()
    assert c.program == [2, 0, 0, 0, 99]


if __name__ == "__main__":
    c = Computer(open('input.txt').read())
    c.program[1] = 12
    c.program[2] = 2
    c.run()
    print(c.program[0])

    for x in range(100):
        for y in range(100):
            c.reset()
            c.program[1] = x
            c.program[2] = y
            c.run()
            if c.program[0] == 19690720:
                print("{:02d}{:02d}".format(x, y))
                sys.exit(0)
