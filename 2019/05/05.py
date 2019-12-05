import operator


class Computer:
    OUTPUT = None
    PROGRAM = None
    INPUT = None
    POS = 0

    def op_input():
        return Computer.INPUT

    def op_output(value):
        Computer.OUTPUT.append(value)

    def op_jump_true(value, pointer):
        if value != 0:
            Computer.POS = pointer

    def op_jump_false(value, pointer):
        if value == 0:
            Computer.POS = pointer

    def op_less_than(value1, value2):
        if value1 < value2:
            return 1
        return 0

    def op_equals(value1, value2):
        if value1 == value2:
            return 1
        return 0

    LANG = {1: (2, 1, operator.add),
            2: (2, 1, operator.mul),
            3: (0, 1, op_input),
            4: (1, 0, op_output),
            5: (2, 0, op_jump_true),
            6: (2, 0, op_jump_false),
            7: (2, 1, op_less_than),
            8: (2, 1, op_equals),
            }

    def __init__(self, program: str):
        Computer.PROGRAM = [int(c.strip()) for c in program.split(',')]
        self._backup = Computer.PROGRAM[:]

    def reset(self, input, pos):
        Computer.PROGRAM = self._backup[:]
        Computer.OUTPUT = []
        Computer.POS = pos
        Computer.INPUT = input

    def run(self, input, pos=0):
        self.reset(input, pos)
        while True:
            parameters_mode, opcode = ('000' + str(Computer.PROGRAM[Computer.POS] // 100))[-3:], Computer.PROGRAM[Computer.POS] % 100
            if opcode == 99:
                break
            parameters_input, parameters_output, operator = self.LANG[opcode]
            tot_parameters = parameters_input + parameters_output
            parameters = []
            for n in range(parameters_input):
                parameter = Computer.PROGRAM[Computer.POS + 1 + n]
                if parameters_mode[2 - n] == '0':
                    parameter = Computer.PROGRAM[parameter]
                parameters.append(parameter)
            old_pos = Computer.POS
            result = operator(*parameters)
            if old_pos == Computer.POS:
                Computer.POS += tot_parameters + 1
            if parameters_output:
                Computer.PROGRAM[Computer.PROGRAM[Computer.POS - 1]] = result


def test_programs():
    c = Computer("1002,4,3,4,33")
    c.run(1)
    assert c.PROGRAM == [1002, 4, 3, 4, 99]

    c = Computer("3,9,8,9,10,9,4,9,99,-1,8")
    c.run(8)
    assert c.OUTPUT == [1]
    c.run(9)
    assert c.OUTPUT == [0]

    c = Computer("3,9,7,9,10,9,4,9,99,-1,8")
    c.run(7)
    assert c.OUTPUT == [1]
    c.run(9)
    assert c.OUTPUT == [0]

    c = Computer("3,3,1108,-1,8,3,4,3,99")
    c.run(8)
    assert c.OUTPUT == [1]
    c.run(9)
    assert c.OUTPUT == [0]

    c = Computer("3,3,1107,-1,8,3,4,3,99")
    c.run(7)
    assert c.OUTPUT == [1]
    c.run(9)
    assert c.OUTPUT == [0]

    c = Computer("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99")
    c.run(7)
    assert c.OUTPUT == [999]
    c.run(8)
    assert c.OUTPUT == [1000]
    c.run(9)
    assert c.OUTPUT == [1001]


if __name__ == "__main__":
    c = Computer(open('input.txt').read())
    c.run(1)
    print(c.OUTPUT[-1])
    c.run(5)
    print(c.OUTPUT[-1])
