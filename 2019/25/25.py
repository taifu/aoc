from collections import defaultdict


class StopException(Exception):
    pass


class Computer:
    def op_add(self, value1, value2):
        return value1 + value2

    def op_mul(self, value1, value2):
        return value1 * value2

    def op_input(self):
        if not self.input:
            raise StopException
        return self.input.pop(0)

    def op_output(self, value):
        self.output.append(value)

    def op_jump_true(self, value, pointer):
        if value != 0:
            self.pos = pointer

    def op_jump_false(self, value, pointer):
        if value == 0:
            self.pos = pointer

    def op_less_than(self, value1, value2):
        if value1 < value2:
            return 1
        return 0

    def op_equals(self, value1, value2):
        if value1 == value2:
            return 1
        return 0

    def op_adjust_relative(self, value):
        self.relative_base += value

    def __init__(self, program: str):
        self.program = defaultdict(int)
        for n, c in enumerate(program.split(',')):
            self.program[n] = int(c.strip())
        self._backup = self.program.copy()
        self.started = False
        self.lang = {1: (2, 1, self.op_add),
                     2: (2, 1, self.op_mul),
                     3: (0, 1, self.op_input),
                     4: (1, 0, self.op_output),
                     5: (2, 0, self.op_jump_true),
                     6: (2, 0, self.op_jump_false),
                     7: (2, 1, self.op_less_than),
                     8: (2, 1, self.op_equals),
                     9: (1, 0, self.op_adjust_relative),
                     }
        self.reset()

    def reset(self):
        self.started = True
        self.program = self._backup.copy()
        self.output = []
        self.pos = 0
        self.relative_base = 0
        self.input = []

    def set_input(self, input=None):
        if input is not None:
            if not isinstance(input, list):
                input = [input]
            self.input = input
        else:
            self.input = []

    def do(self, command):
        self.set_input_string(command)
        try:
            self.run()
        except StopException:
            pass
        return self.show()

    def show(self, clean=True):
        value = ("".join(chr(c) for c in self.output))
        print(value)
        if clean:
            self.output = []
        return value

    def set_input_string(self, string, append_newline=True):
        self.set_input([ord(c) for c in string + ("\n" if append_newline else "")])

    def run(self, input=None, reset=False):
        if reset:
            self.reset()
        if input is not None:
            self.set_input(input)
        while True:
            parameters_mode, opcode = ('000' + str(self.program[self.pos] // 100))[-3:], self.program[self.pos] % 100
            if opcode == 99:
                break
            parameters_input, parameters_output, operator = self.lang[opcode]
            tot_parameters = parameters_input + parameters_output
            parameters = []
            for n in range(parameters_input):
                parameter = self.program[self.pos + 1 + n]
                parameter_mode = parameters_mode[2 - n]
                if parameter_mode == '2':  # Relative mode (the value stored at value position + relative base)
                    parameter = self.program[parameter + self.relative_base]
                elif parameter_mode == '0':  # Position mode (the value stored at value position)
                    parameter = self.program[parameter]
                elif parameter_mode != '1':  # Immediate (the value)
                    raise Exception("Unexpected parameter mode: {}".format(parameter_mode))
                parameters.append(parameter)
            if parameters_output:
                assert parameters_output == 1
                parameter_mode = parameters_mode[2 - parameters_input]
                pos_output = self.program[self.pos + tot_parameters]
                if parameter_mode == '2':  # Relative mode (the value stored at value position + relative base)
                    pos_output += self.relative_base
            old_pos = self.pos
            result = operator(*parameters)
            if old_pos == self.pos:
                self.pos += tot_parameters + 1
            if parameters_output:
                self.program[pos_output] = result


if __name__ == "__main__":
    # See map.png
    raw = open('input.txt').read()
    computer = Computer(raw)
    commands = ["west",   # GIFT WRAPPING CENTER
                "take hologram",
                "north",  # WARP DRIVE MAINTENANCE
                "north",  # CREW QUARTERS
                "take prime number",
                "south",  # WARP DRIVE MAINTENANCE
                "east",   # ENGINEERING
                "take space law space brochure",
                "west",   # WARP DRIVE MAINTENANCE
                "south",  # GIFT WRAPPING CENTER
                "east",   # HULL BREACH
                "north",  # KITCHEN
                "north",  # CORRIDOR
                "take astrolabe",
                "south",  # KITCHEN
                "take polygon",
                "south",  # HULL BREACH
                "south",  # STORAGE
                "east",   # SCIENCE LAB
                "take weather machine",
                "west",   # STORAGE
                "south",  # ARCADE
                "take manifold",
                "west",   # SICK BAY
                "take mouse",
                "north",  # HALLWAY
                "north",  # SECURITY CHECKPOINT
                "inv",
                ]
    while True:
        try:
            computer.run()
        except StopException:
            pass
        computer.show()
        if commands:
            computer.set_input_string(commands.pop(0))
        else:
            break
    items = ["space law space brochure", "manifold", "weather machine", "prime number", "polygon", "astrolabe", "mouse", "hologram"]
    for start in range(2**len(items)):
        print(start)
        which = bin(start)[2:].zfill(len(items))
        for n, item in enumerate(items):
            action = "take" if which[n] == '1' else "drop"
            computer.do(action + " " + item)
        ret = computer.do("east")
        if "heavier" not in ret and "lighter" not in ret:
            break
