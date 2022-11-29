from collections import defaultdict, deque


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


class Section:
    def __init__(self):
        self.cells = {}
        self.min_x = self.max_x = self.min_y = self.max_y = 0

    def add(self, position, status):
        x, y = position
        self.cells[x, y] = status
        if status == 'o':
            self.oxygen = (x, y)
        self.min_x = min(x, self.min_x)
        self.max_x = max(x, self.max_x)
        self.min_y = min(y, self.min_y)
        self.max_y = max(y, self.max_y)

    def paint(self):
        print("\033[2J")
        print("\033[0;0H")
        for y in range(self.min_y, self.max_y + 1):
            row = ""
            for x in range(self.min_x, self.max_x + 1):
                if x == 0 and y == 0:
                    row += 'x'
                else:
                    row += self.cells.get((x, y), '#')
            print(row)


def flood_fill(computer, section, position, status):
    section.add(position, status)
    for direction, back_direction in ((1, 2), (2, 1), (3, 4), (4, 3)):
        next_position = (position[0] + (1 if direction == 4 else -1 if direction == 3 else 0),
                         position[1] + (1 if direction == 2 else -1 if direction == 1 else 0))
        if next_position not in section.cells:
            try:
                computer.run(input=direction)
                assert Exception("Unexpected halt 99")
            except StopException:
                pass
            status = computer.output.pop(0)
            if status in (1, 2):
                flood_fill(computer, section, next_position, '.' if status == 1 else 'o')
                try:
                    computer.run(input=back_direction)
                    assert Exception("Unexpected halt 99")
                except StopException:
                    pass
                assert computer.output.pop() in (1, 2)
            elif status == 0:
                section.add(next_position, '#')
            else:
                raise Exception("Unexpected status {}".format(status))


def breadth_first_search(section, pos, goal):
    queue = deque([[pos]])
    all_paths = {}
    goal_path = None
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node not in all_paths:
            for next_pos in ((node[0] + 1, node[1]), (node[0] - 1, node[1]), (node[0], node[1] + 1), (node[0], node[1] - 1)):
                if next_pos in all_paths:
                    continue
                cell = section.cells.get(next_pos, None)
                if cell in ('.', 'o'):
                    new_path = path + [next_pos]
                    if next_pos == goal:
                        goal_path = new_path
                    queue.append(new_path)
            all_paths[node] = path
    return goal_path, all_paths


if __name__ == "__main__":
    computer = Computer(open('input.txt').read())
    position = (0, 0)  # x, y
    direction = 1  # 1=north 2=south 3=west 4=east
    section = Section()
    flood_fill(computer, section, position, '.')
    section.paint()
    goal, paths = breadth_first_search(section, section.oxygen, (0, 0))
    print(len(goal) - 1)
    print(max(len(v) - 1 for v in paths.values()))
