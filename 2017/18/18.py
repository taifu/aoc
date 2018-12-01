import Queue
from threading import Thread


def get_val(registers, reg):
    if reg.isdigit() or reg[0] == '-':
        return int(reg)
    return registers[reg]


def execute(program, registers, queue_send=None, queue_receive=None):
    SND, SET, ADD, MUL, MOD, RCV, JGZ = 'snd', 'set', 'add', 'mul', 'mod', 'rcv', 'jgz'

    last_played = None
    step = 0

    while step < len(program):
        instr, regs = program[step][0], program[step][1:]
        if instr == SND:
            if queue_send:
                try:
                    queue_send.put(get_val(registers, regs[0]), timeout=1)
                    registers['z'] += 1
                except (Queue.Full, Queue.Empty):
                    break
            else:
                last_played = get_val(registers, regs[0])
        elif instr in RCV:
            if queue_receive:
                try:
                    registers[regs[0]] = queue_receive.get(timeout=1)
                except (Queue.Full, Queue.Empty):
                    break
            else:
                if get_val(registers, regs[0]) != 0:
                    return last_played
        elif instr == SET:
            registers[regs[0]] = get_val(registers, regs[1])
        elif instr in ADD:
            registers[regs[0]] = get_val(registers, regs[0]) + get_val(registers, regs[1])
        elif instr in MUL:
            registers[regs[0]] = get_val(registers, regs[0]) * get_val(registers, regs[1])
        elif instr in MOD:
            registers[regs[0]] = registers[regs[0]] % get_val(registers, regs[1])
        elif instr == JGZ:
            if get_val(registers, regs[0]) > 0:
                step += get_val(registers, regs[1]) - 1
        step += 1

    if queue_send:
        if registers['x'] == 1:
            print(registers['z'])


program, registers = [l.strip().split(" ") for l in open("input").readlines()], {'p': 0}
print(execute(program, registers))

q0 = Queue.Queue()
q1 = Queue.Queue()

register0 = {'p': 0, 'x': 0, 'z': 0}
register1 = {'p': 1, 'x': 1, 'z': 0}

program = [l.strip().split(" ") for l in open("input").readlines()]
t0 = Thread(target=execute, args=(program, register0, q0, q1))
t1 = Thread(target=execute, args=(program, register1, q1, q0))

t0.start()
t1.start()
